#!/usr/bin/env python3
"""Run EvalRAG scenario evaluation."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.config import settings  # noqa: E402

CONCEPT_FAILURE_THRESHOLD = settings.concept_coverage_failure_threshold
from app.rag_pipeline import EvalRAGPipeline, evaluate_trace  # noqa: E402


DEFAULT_EVAL_PATH = ROOT / "data" / "eval" / "eval_questions.jsonl"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def reciprocal_rank(retrieved: list[dict[str, Any]], expected_sources: list[str]) -> float:
    expected = set(expected_sources)
    for item in retrieved:
        if item["source"] in expected:
            return 1.0 / item["rank"]
    return 0.0


def _mean(values: list[float]) -> float | None:
    return round(statistics.mean(values), 4) if values else None


def _bool_mean(records: list[dict[str, Any]], key: str) -> float | None:
    values = [record["evaluation"].get(key) for record in records]
    filtered = [1.0 if value else 0.0 for value in values if value is not None]
    return _mean(filtered)


def _retrieval_only_record(pipeline: EvalRAGPipeline, item: dict[str, Any]) -> dict[str, Any]:
    started = time.perf_counter()
    retrieved = pipeline.retrieve(item["question"])
    latency = round(time.perf_counter() - started, 4)
    evaluation = evaluate_trace(
        "",
        [chunk["source"] for chunk in retrieved],
        "",
        expected_sources=item.get("expected_sources", []),
    )
    return {
        "eval_id": item["id"],
        "question": item["question"],
        "retrieved_chunks": retrieved,
        "answer": "",
        "llm_decision": None,
        "policy_decision": None,
        "final_decision": None,
        "decision": None,
        "policy_validation": {},
        "expected_sources": item.get("expected_sources", []),
        "expected_concepts": item.get("expected_concepts", []),
        "expected_decision": item.get("expected_decision"),
        "category": item.get("category"),
        "ground_truth": item.get("ground_truth") or item.get("reference"),
        "reference_contexts": item.get("reference_contexts", []),
        "evaluation": evaluation,
        "latency_seconds": latency,
        "model": None,
        "generator_backend": "retrieval_only",
    }


def _failure_hypothesis(record: dict[str, Any]) -> str | None:
    evaluation = record.get("evaluation", {})
    if evaluation.get("all_expected_sources_found") is False or evaluation.get("top1_source_match") is False:
        return "retrieval_or_playbook_gap"
    if evaluation.get("decision_correct") is False and evaluation.get("llm_decision_correct") is False:
        if evaluation.get("source_match_rate") == 1.0:
            return "llm_reasoning_or_prompt_gap"
        return "retrieval_then_llm_decision_gap"
    if evaluation.get("decision_correct") is False and evaluation.get("policy_override"):
        return "policy_validator_overreach"
    concept_coverage = evaluation.get("concept_coverage")
    if concept_coverage is not None and concept_coverage < CONCEPT_FAILURE_THRESHOLD:
        return "answer_concept_coverage_gap"
    return None


def _policy_correction_counts(records: list[dict[str, Any]]) -> tuple[int, int, int]:
    corrections = 0
    regressions = 0
    overrides = 0
    for record in records:
        evaluation = record.get("evaluation", {})
        if not evaluation.get("policy_override"):
            continue
        overrides += 1
        llm_correct = evaluation.get("llm_decision_correct")
        final_correct = evaluation.get("decision_correct")
        if llm_correct is False and final_correct is True:
            corrections += 1
        if llm_correct is True and final_correct is False:
            regressions += 1
    return corrections, regressions, overrides


def run_eval(
    path: Path,
    top_k: int,
    alpha: float,
    write_logs: bool,
    limit: int | None = None,
    save_records: Path | None = None,
    generation_enabled: bool = True,
    concept_judge_enabled: bool | None = None,
) -> dict[str, Any]:
    questions = load_jsonl(path)
    if limit is not None:
        questions = questions[:limit]
    pipeline = EvalRAGPipeline(top_k=top_k, alpha=alpha)
    records: list[dict[str, Any]] = []
    for item in questions:
        if generation_enabled:
            record = pipeline.answer(
                item["question"],
                expected_sources=item.get("expected_sources", []),
                expected_concepts=item.get("expected_concepts", []),
                expected_decision=item.get("expected_decision"),
                log=write_logs,
                concept_judge_enabled=concept_judge_enabled,
            )
            record["eval_id"] = item["id"]
            record["category"] = item.get("category")
            record["ground_truth"] = item.get("ground_truth") or item.get("reference")
            record["reference_contexts"] = item.get("reference_contexts", [])
        else:
            record = _retrieval_only_record(pipeline, item)
        records.append(record)

    source_hit = [1.0 if record["evaluation"]["source_hit"] else 0.0 for record in records]
    source_match = [
        record["evaluation"]["source_match_rate"]
        for record in records
        if record["evaluation"]["source_match_rate"] is not None
    ]
    source_precision_at_k = [
        record["evaluation"]["source_precision_at_k"]
        for record in records
        if record["evaluation"]["source_precision_at_k"] is not None
    ]
    concept_coverage = [
        record["evaluation"]["concept_coverage"]
        for record in records
        if record["evaluation"]["concept_coverage"] is not None
    ]
    decision_accuracy = [
        1.0 if record["evaluation"]["decision_correct"] else 0.0
        for record in records
        if record["evaluation"]["decision_correct"] is not None
    ]
    llm_decision_accuracy = [
        1.0 if record["evaluation"]["llm_decision_correct"] else 0.0
        for record in records
        if record["evaluation"].get("llm_decision_correct") is not None
    ]
    policy_decision_accuracy = [
        1.0 if record["evaluation"]["policy_decision_correct"] else 0.0
        for record in records
        if record["evaluation"].get("policy_decision_correct") is not None
    ]
    mrr = [
        reciprocal_rank(record["retrieved_chunks"], item.get("expected_sources", []))
        for item, record in zip(questions, records, strict=True)
    ]
    latency = [record["latency_seconds"] for record in records]
    corrections, regressions, overrides = _policy_correction_counts(records)
    expected_count = len([item for item in questions if item.get("expected_decision")])

    failures = [
        {
            "id": record["eval_id"],
            "llm_decision": record.get("llm_decision"),
            "policy_decision": record.get("policy_decision"),
            "final_decision": record.get("final_decision", record.get("decision")),
            "expected_decision": item.get("expected_decision"),
            "matched_sources": record["evaluation"]["matched_sources"],
            "missing_sources": record["evaluation"]["missing_sources"],
            "concept_coverage": record["evaluation"].get("concept_coverage"),
            "deterministic_concept_coverage": record["evaluation"].get("deterministic_concept_coverage"),
            "concept_judge_used": record["evaluation"].get("concept_judge_used"),
            "concept_judge_error": record["evaluation"].get("concept_judge_error"),
            "missing_concepts": record["evaluation"].get("missing_concepts", []),
            "concept_matches": record["evaluation"].get("concept_matches", []),
            "top_sources": [chunk["source"] for chunk in record["retrieved_chunks"][:3]],
            "policy_action": record.get("policy_validation", {}).get("policy_action"),
            "policy_findings": record.get("policy_validation", {}).get("policy_findings", []),
            "failure_hypothesis": _failure_hypothesis(record),
            "generator_backend": record.get("generator_backend"),
            "generator_error": record.get("generator_error"),
        }
        for item, record in zip(questions, records, strict=True)
        if record["evaluation"].get("all_expected_sources_found") is False
        or record["evaluation"].get("top1_source_match") is False
        or record["evaluation"].get("decision_correct") is False
        or (record["evaluation"].get("concept_coverage") is not None and record["evaluation"].get("concept_coverage") < CONCEPT_FAILURE_THRESHOLD)
    ]

    if save_records is not None:
        save_records.parent.mkdir(parents=True, exist_ok=True)
        save_records.write_text(json.dumps(records, indent=2), encoding="utf-8")

    return {
        "question_count": len(records),
        "top_k": top_k,
        "alpha": alpha,
        "generation_enabled": generation_enabled,
        "concept_judge_enabled": bool(concept_judge_enabled if concept_judge_enabled is not None else settings.concept_judge_enabled) if generation_enabled else False,
        "concept_failure_threshold": CONCEPT_FAILURE_THRESHOLD,
        "metrics": {
            "source_hit_at_k": _mean(source_hit),
            "source_match_rate": _mean(source_match),
            "all_expected_sources_found_rate": _bool_mean(records, "all_expected_sources_found"),
            "top1_source_match_rate": _bool_mean(records, "top1_source_match"),
            "source_precision_at_k": _mean(source_precision_at_k),
            "mean_reciprocal_rank": _mean(mrr),
            "concept_coverage": _mean(concept_coverage),
            "llm_decision_accuracy": _mean(llm_decision_accuracy),
            "policy_decision_accuracy_when_triggered": _mean(policy_decision_accuracy),
            "final_decision_accuracy": _mean(decision_accuracy),
            "decision_accuracy": _mean(decision_accuracy),
            "policy_trigger_rate": _bool_mean(records, "policy_triggered") if generation_enabled else None,
            "policy_override_rate": _bool_mean(records, "policy_override") if generation_enabled else None,
            "policy_correction_rate": round(corrections / expected_count, 4) if generation_enabled and expected_count else None,
            "policy_regression_rate": round(regressions / expected_count, 4) if generation_enabled and expected_count else None,
            "avg_latency_seconds": _mean(latency),
        },
        "policy_correction_summary": {
            "overrides": overrides if generation_enabled else None,
            "corrections": corrections if generation_enabled else None,
            "regressions": regressions if generation_enabled else None,
        },
        "failures": failures[:12],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-path", type=Path, default=DEFAULT_EVAL_PATH)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--alpha", type=float, default=settings.hybrid_alpha, help="Hybrid score weight for vector score.")
    parser.add_argument("--write-logs", action="store_true")
    parser.add_argument("--limit", type=int, default=None, help="Evaluate only the first N questions.")
    parser.add_argument("--save-records", type=Path, default=None, help="Write per-question eval records to a JSON file.")
    parser.add_argument("--retrieval-only", action="store_true", help="Evaluate retrieval metrics without calling an LLM.")
    judge_group = parser.add_mutually_exclusive_group()
    judge_group.add_argument(
        "--concept-judge",
        dest="concept_judge_enabled",
        action="store_true",
        default=settings.concept_judge_enabled,
        help="Use a strict LLM judge for missing concepts when deterministic coverage is below the failure threshold.",
    )
    judge_group.add_argument(
        "--no-concept-judge",
        dest="concept_judge_enabled",
        action="store_false",
        help="Disable strict LLM concept judging even if EVALRAG_CONCEPT_JUDGE_ENABLED=true.",
    )
    args = parser.parse_args()

    result = run_eval(
        args.eval_path,
        args.top_k,
        args.alpha,
        args.write_logs,
        limit=args.limit,
        save_records=args.save_records,
        generation_enabled=not args.retrieval_only,
        concept_judge_enabled=args.concept_judge_enabled,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
