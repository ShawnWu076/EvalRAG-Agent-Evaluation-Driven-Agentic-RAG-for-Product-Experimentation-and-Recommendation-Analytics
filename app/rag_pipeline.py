"""RAG orchestration, LLM generation, telemetry, and lightweight evaluation."""

from __future__ import annotations

import re
import time
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
UNKNOWN_DECISION = "unknown"


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_decision(answer: str) -> str:
    """Extract the exact decision label the LLM placed in the decision section."""

    section_match = re.search(
        r"##\s*Decision Recommendation\s*(.*?)(?:\n##\s+|\Z)",
        answer,
        flags=re.IGNORECASE | re.DOTALL,
    )
    search_space = section_match.group(1) if section_match else answer
    normalized = normalize_text(search_space)
    for decision in sorted(DECISIONS, key=len, reverse=True):
        pattern = rf"(?<![a-z0-9_]){re.escape(decision)}(?![a-z0-9_])"
        if re.search(pattern, normalized):
            return decision
    return UNKNOWN_DECISION


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
    unique_retrieved_sources = list(dict.fromkeys(retrieved_sources))
    source_set = set(unique_retrieved_sources)
    expected_source_set = set(expected_sources)
    matched_sources = [source for source in expected_sources if source in source_set]
    missing_sources = [source for source in expected_sources if source not in source_set]
    unexpected_sources = [source for source in unique_retrieved_sources if source not in expected_source_set]
    answer_text = normalize_text(answer)
    covered_concepts = [
        concept
        for concept in expected_concepts
        if normalize_text(concept) in answer_text
    ]
    source_hit = bool(expected_source_set and matched_sources)
    source_match_rate = round(len(matched_sources) / len(expected_source_set), 4) if expected_source_set else None
    all_sources_found = len(matched_sources) == len(expected_source_set) if expected_source_set else None
    top1_source_match = (
        unique_retrieved_sources[0] in expected_source_set
        if expected_source_set and unique_retrieved_sources
        else None
    )
    source_precision_at_k = (
        round(len([source for source in unique_retrieved_sources if source in expected_source_set]) / len(unique_retrieved_sources), 4)
        if unique_retrieved_sources and expected_source_set
        else None
    )
    return {
        "source_hit": source_hit,
        "source_match_rate": source_match_rate,
        "all_expected_sources_found": all_sources_found,
        "top1_source_match": top1_source_match,
        "source_precision_at_k": source_precision_at_k,
        "matched_sources": matched_sources,
        "missing_sources": missing_sources,
        "unexpected_sources": unexpected_sources,
        "concept_coverage": round(len(covered_concepts) / len(expected_concepts), 4) if expected_concepts else None,
        "covered_concepts": covered_concepts,
        "decision_correct": decision == expected_decision if expected_decision else None,
    }


def _primary_llm_config() -> LLMGenerationConfig:
    return LLMGenerationConfig(
        base_url=settings.llm_base_url,
        model=settings.llm_model,
        api_key=settings.llm_api_key,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
        timeout_seconds=settings.llm_timeout_seconds,
        token_parameter=settings.llm_token_parameter,
    )


def _fallback_llm_config() -> LLMGenerationConfig:
    return LLMGenerationConfig(
        base_url=settings.fallback_llm_base_url,
        model=settings.fallback_llm_model,
        api_key=settings.fallback_llm_api_key,
        temperature=settings.fallback_llm_temperature,
        max_tokens=settings.fallback_llm_max_tokens,
        timeout_seconds=settings.fallback_llm_timeout_seconds,
        token_parameter=settings.fallback_llm_token_parameter,
    )


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

    def retrieve(self, question: str) -> list[dict[str, Any]]:
        retrieved_results = self.retriever.search(question, top_k=self.top_k, alpha=self.alpha)
        return results_to_dicts(retrieved_results)

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
        retrieved = self.retrieve(question)
        generator_backend = settings.generator_backend
        if generator_backend not in {"openai_compatible", "local_llm", "llm"}:
            raise ValueError(
                f"Unsupported generator backend {generator_backend!r}. "
                "Use an OpenAI-compatible LLM endpoint."
            )

        model_name = settings.llm_model
        generator_error = None
        fallback_error = None
        try:
            answer = generate_llm_answer(
                question,
                retrieved,
                _primary_llm_config(),
                tool_summary=tool_summary,
                allowed_decisions=sorted(DECISIONS),
            )
        except LLMGenerationError as exc:
            if not settings.llm_fallback_enabled:
                raise
            generator_error = str(exc)
            try:
                answer = generate_llm_answer(
                    question,
                    retrieved,
                    _fallback_llm_config(),
                    tool_summary=tool_summary,
                    allowed_decisions=sorted(DECISIONS),
                )
                generator_backend = "local_llm_fallback"
                model_name = settings.fallback_llm_model
            except LLMGenerationError as fallback_exc:
                fallback_error = str(fallback_exc)
                raise LLMGenerationError(
                    f"Primary LLM failed: {generator_error}; fallback local LLM failed: {fallback_error}"
                ) from fallback_exc

        decision = extract_decision(answer)
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
        if fallback_error:
            record["fallback_error"] = fallback_error
        if decision == UNKNOWN_DECISION:
            record["decision_parse_error"] = "LLM answer did not contain one allowed decision label."
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
        "generator_backend": record.get("generator_backend", "openai_compatible"),
        "generator_error": record.get("generator_error"),
    }
