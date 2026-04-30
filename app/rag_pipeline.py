"""RAG orchestration, deterministic memo generation, and lightweight evaluation."""

from __future__ import annotations

import re
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from app.chunking import build_chunks, load_chunks
from app.config import PLAYBOOK_DIR, settings
from app.llm_generator import LLMGenerationConfig, LLMGenerationError, generate_llm_answer
from app.retrieval import (
    SimpleHybridRetriever,
    results_to_dicts,
)
from app.telemetry import append_log, new_query_id, utc_timestamp


DECISIONS = {
    "launch",
    "do_not_launch",
    "investigate_further",
    "partial_rollout",
    "do_not_trust_result",
    "use_did_or_quasi_experiment",
}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def infer_decision(question: str, tool_summary: dict[str, Any] | None = None) -> str:
    text = normalize_text(question)
    if tool_summary:
        if tool_summary.get("srm", {}).get("classification") == "fail":
            return "do_not_trust_result"
        guardrail_flags = [
            item
            for item in tool_summary.get("metric_lifts", [])
            if item.get("metric") in {"retained_7d", "complained"} and item.get("risk_flag")
        ]
        if guardrail_flags:
            return "investigate_further"

    if any(
        term in text
        for term in [
            "sample ratio mismatch",
            "srm failed",
            "srm fail",
            "srm at p",
            "70/30",
            "70 30",
            "30% more users",
            "exposure logs are missing",
            "missing exposure",
            "assignment changed",
            "assignment bug",
            "eligible users than expected",
            "population drifted",
            "logging failure",
        ]
    ):
        return "do_not_trust_result"
    if any(
        term in text
        for term in [
            "non-random",
            "not randomized",
            "one city",
            "one market",
            "pre/post",
            "pre post",
            "difference-in-differences",
            "quasi-experimental",
            "policy changed",
            "comparison group",
        ]
    ):
        return "use_did_or_quasi_experiment"
    segment_terms = ["segment harm", "power users", "high-value", "returning high-value", "android users", "germany", "new users improved"]
    harm_terms = ["harmed", "harm", "hurt", "negative", "lower", "fell", "dropped", "worse", "complaints"]
    if any(term in text for term in segment_terms) and any(term in text for term in harm_terms):
        return "partial_rollout"
    if "retention" in text and any(term in text for term in ["drop", "dropped", "down", "decrease", "decreased", "worse", "hurt"]):
        return "investigate_further"
    if any(
        term in text
        for term in [
            "complaint rate increased",
            "complaints increased",
            "complaints worsened",
            "report rate increased",
            "hide rate increased",
            "unsubscribe rate worsened",
            "complaints and unsubscribe rate worsened",
        ]
    ):
        return "investigate_further"
    if ("ctr" in text or "click" in text) and any(term in text for term in ["cvr down", "conversion down", "conversion rate decreased", "conversions decreased"]):
        return "investigate_further"
    if any(
        term in text
        for term in [
            "all guardrails stable",
            "guardrails stable",
            "retention stable",
            "retention is stable",
            "complaints are stable",
            "clean win",
            "no guardrail",
            "no harm",
        ]
    ) and any(term in text for term in ["revenue increased", "revenue up", "significantly up", "improved"]):
        return "launch"
    return "investigate_further"


def evaluate_trace(
    answer: str,
    retrieved_sources: list[str],
    decision: str,
    expected_sources: list[str] | None = None,
    expected_concepts: list[str] | None = None,
    expected_decision: str | None = None,
) -> dict[str, Any]:
    expected_sources = expected_sources or []
    expected_concepts = expected_concepts or []
    source_set = set(retrieved_sources)
    expected_source_set = set(expected_sources)
    matched_sources = sorted(source_set & expected_source_set)
    answer_text = normalize_text(answer)
    covered_concepts = [
        concept
        for concept in expected_concepts
        if normalize_text(concept) in answer_text
    ]
    return {
        "source_hit": bool(expected_source_set and matched_sources),
        "source_match_rate": round(len(matched_sources) / len(expected_source_set), 4) if expected_source_set else None,
        "matched_sources": matched_sources,
        "concept_coverage": round(len(covered_concepts) / len(expected_concepts), 4) if expected_concepts else None,
        "covered_concepts": covered_concepts,
        "decision_correct": decision == expected_decision if expected_decision else None,
    }


def _decision_sentence(decision: str) -> str:
    return {
        "launch": "Launch is reasonable if the reported lifts are statistically reliable and guardrails remain stable.",
        "do_not_launch": "Do not launch on the current evidence.",
        "investigate_further": "Do not fully launch yet; investigate the guardrail or validity risk before expanding exposure.",
        "partial_rollout": "Avoid a full launch; consider a constrained rollout only for segments where harms are not present.",
        "do_not_trust_result": "Do not trust the measured lift until the experiment allocation and logging issue is resolved.",
        "use_did_or_quasi_experiment": "Do not treat this as a clean randomized A/B test; use DiD or another quasi-experimental design.",
    }.get(decision, "Investigate further before launch.")


def _reasoning_bullets(question: str, decision: str, tool_summary: dict[str, Any] | None) -> list[str]:
    text = normalize_text(question)
    bullets: list[str] = []
    if decision == "do_not_trust_result":
        bullets.append("A sample ratio mismatch or allocation imbalance threatens experiment validity, so metric lifts may reflect randomization or logging problems rather than product impact.")
    if decision == "use_did_or_quasi_experiment":
        bullets.append("The rollout does not appear randomized, which means simple treatment/control comparisons can be confounded by market, timing, or user-mix differences.")
    if "retention" in text:
        bullets.append("Retention is a guardrail metric for recommendation systems because short-term clicks or revenue can come at the expense of long-term user value.")
    if any(term in text for term in ["ctr", "click"]):
        bullets.append("CTR is useful, but it should not dominate launch decisions when conversion quality, revenue, retention, or complaints move in the wrong direction.")
    if any(term in text for term in ["segment", "power users", "high-value", "new users"]):
        bullets.append("Segment analysis matters because an overall win can hide harm to high-value, new, or otherwise strategically important users.")
    if tool_summary:
        for metric in tool_summary.get("metric_lifts", [])[:5]:
            bullets.append(
                f"Computed {metric['metric']} lift is {metric['lift_pct']:.2f}% "
                f"(control={metric['control_mean']:.4f}, treatment={metric['treatment_mean']:.4f})."
            )
    if not bullets:
        bullets.append("The launch decision should weigh primary metrics against guardrails, experiment validity, and segment-level tradeoffs.")
    return bullets


def _metrics_to_check(question: str, decision: str) -> list[str]:
    text = normalize_text(question)
    metrics = ["primary metric lift", "statistical significance", "sample ratio mismatch"]
    if any(term in text for term in ["recommendation", "ranking", "feed", "search"]):
        metrics.extend(["CTR", "conversion rate", "7-day retention", "complaint / hide / report rate"])
    if "revenue" in text:
        metrics.append("revenue per user")
    if "retention" in text:
        metrics.append("cohort retention by user segment")
    if decision in {"partial_rollout", "investigate_further"}:
        metrics.append("new vs. returning and high-value user segments")
    return list(dict.fromkeys(metrics))


def generate_structured_answer(
    question: str,
    retrieved: list[dict[str, Any]],
    decision: str,
    tool_summary: dict[str, Any] | None = None,
) -> str:
    sources = list(dict.fromkeys(item["source"] for item in retrieved))
    source_lines = "\n".join(f"- {source}" for source in sources)
    reasoning_lines = "\n".join(f"- {item}" for item in _reasoning_bullets(question, decision, tool_summary))
    metrics_lines = "\n".join(f"- {item}" for item in _metrics_to_check(question, decision))

    next_steps = {
        "launch": [
            "Confirm confidence intervals and guardrails one final time.",
            "Prepare a staged launch monitor with rollback thresholds.",
            "Track post-launch retention and complaint metrics.",
        ],
        "do_not_trust_result": [
            "Investigate assignment, bucketing, eligibility filters, and logging joins.",
            "Re-run or repair the experiment before making a product decision.",
            "Do not use apparent metric lift as launch evidence until SRM is resolved.",
        ],
        "use_did_or_quasi_experiment": [
            "Define pre/post windows and comparable control markets.",
            "Check parallel pre-trends before relying on DiD estimates.",
            "Avoid simple before/after claims as launch evidence.",
        ],
        "partial_rollout": [
            "Identify segments where the treatment is beneficial and guardrails are stable.",
            "Exclude or redesign for harmed segments before broader rollout.",
            "Continue monitoring retention, complaints, and long-term value.",
        ],
        "investigate_further": [
            "Verify statistical significance and confidence intervals for primary and guardrail metrics.",
            "Run segment analysis for new, returning, high-value, device, and country cohorts.",
            "Consider a longer experiment or partial rollout if the downside is isolated.",
        ],
    }.get(decision, ["Run follow-up diagnostics before launch."])
    next_step_lines = "\n".join(f"{idx}. {item}" for idx, item in enumerate(next_steps, start=1))

    caveats = [
        "This memo is only as reliable as the retrieved playbook context and observed experiment data.",
        "A launch recommendation should include business context, uncertainty, and known implementation risks.",
    ]
    caveat_lines = "\n".join(f"- {item}" for item in caveats)

    return f"""## Short Answer
{_decision_sentence(decision)}

## Decision Recommendation
`{decision}`

## Reasoning
{reasoning_lines}

## Metrics to Check
{metrics_lines}

## Suggested Next Steps
{next_step_lines}

## Risks / Caveats
{caveat_lines}

## Retrieved Sources
{source_lines}
"""


class EvalRAGPipeline:
    def __init__(
        self,
        index_path: Path | None = None,
        playbook_dir: Path = PLAYBOOK_DIR,
        top_k: int | None = None,
        alpha: float | None = None,
    ) -> None:
        self.index_path = Path(index_path or settings.index_path)
        self.playbook_dir = playbook_dir
        self.top_k = top_k or settings.top_k
        self.alpha = settings.hybrid_alpha if alpha is None else alpha
        if self.index_path.exists():
            chunks = load_chunks(self.index_path)
        else:
            chunks = build_chunks(
                playbook_dir,
                settings.chunk_size,
                settings.chunk_overlap,
                semantic_enabled=settings.chunk_semantic_enable,
                semantic_model=settings.chunk_semantic_model,
                semantic_device=settings.chunk_semantic_device,
                semantic_offline=settings.chunk_semantic_offline,
                semantic_min_size=settings.chunk_semantic_min_size,
            )
        self.retriever = SimpleHybridRetriever(chunks, alpha=self.alpha)

    def answer(
        self,
        question: str,
        expected_sources: list[str] | None = None,
        expected_concepts: list[str] | None = None,
        expected_decision: str | None = None,
        tool_summary: dict[str, Any] | None = None,
        log: bool = True,
    ) -> dict[str, Any]:
        started = time.perf_counter()
        query_id = new_query_id()
        retrieved_results = self.retriever.search(question, top_k=self.top_k, alpha=self.alpha)
        retrieved = results_to_dicts(retrieved_results)
        decision = infer_decision(question, tool_summary)
        generator_backend = settings.generator_backend
        generator_error = None
        model_name = settings.model_name
        if generator_backend in {"local_llm", "llm", "openai_compatible"}:
            llm_config = LLMGenerationConfig(
                base_url=settings.llm_base_url,
                model=settings.llm_model,
                api_key=settings.llm_api_key,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens,
                timeout_seconds=settings.llm_timeout_seconds,
                token_parameter=settings.llm_token_parameter,
            )
            try:
                answer = generate_llm_answer(question, retrieved, decision, llm_config, tool_summary)
                model_name = settings.llm_model
            except LLMGenerationError as exc:
                if not settings.llm_fallback_enabled:
                    raise
                generator_error = str(exc)
                answer = generate_structured_answer(question, retrieved, decision, tool_summary)
                model_name = settings.model_name
                generator_backend = "rule_fallback"
        else:
            answer = generate_structured_answer(question, retrieved, decision, tool_summary)
        latency = round(time.perf_counter() - started, 4)
        retrieved_sources = [item["source"] for item in retrieved]
        evaluation = evaluate_trace(
            answer,
            retrieved_sources,
            decision,
            expected_sources=expected_sources,
            expected_concepts=expected_concepts,
            expected_decision=expected_decision,
        )
        record = {
            "query_id": query_id,
            "timestamp": utc_timestamp(),
            "question": question,
            "retrieved_chunks": [
                {
                    **item,
                    "text_preview": item["text"][:240],
                }
                for item in retrieved
            ],
            "answer": answer,
            "decision": decision,
            "expected_sources": expected_sources or [],
            "expected_concepts": expected_concepts or [],
            "expected_decision": expected_decision,
            "evaluation": evaluation,
            "latency_seconds": latency,
            "model": model_name,
            "generator_backend": generator_backend,
        }
        if generator_error:
            record["generator_error"] = generator_error
        if tool_summary:
            record["tool_summary"] = tool_summary
        if log:
            append_log(record)
        return record


def record_to_public_response(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "query_id": record["query_id"],
        "answer": record["answer"],
        "decision": record["decision"],
        "retrieved_chunks": record["retrieved_chunks"],
        "evaluation": record["evaluation"],
        "latency_seconds": record["latency_seconds"],
        "model": record["model"],
        "generator_backend": record.get("generator_backend", "rule"),
        "generator_error": record.get("generator_error"),
    }
