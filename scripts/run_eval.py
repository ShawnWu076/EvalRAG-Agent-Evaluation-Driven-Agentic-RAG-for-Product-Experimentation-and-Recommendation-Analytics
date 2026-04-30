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
        "decision": None,
        "expected_sources": item.get("expected_sources", []),
        "expected_concepts": item.get("expected_concepts", []),
        "expected_decision": item.get("expected_decision"),
        "evaluation": evaluation,
        "latency_seconds": latency,
        "model": None,
        "generator_backend": "retrieval_only",
    }


def run_eval(
    path: Path,
    top_k: int,
    alpha: float,
    write_logs: bool,
    limit: int | None = None,
    save_records: Path | None = None,
    generation_enabled: bool = True,
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
            )
            record["eval_id"] = item["id"]
        else:
            record = _retrieval_only_record(pipeline, item)
        records.append(record)

    source_hit = [1.0 if record["evaluation"]["source_hit"] else 0.0 for record in records]
    source_match = [
        record["evaluation"]["source_match_rate"]
        for record in records
        if record["evaluation"]["source_match_rate"] is not None
    ]
    all_sources_found = [
        1.0 if record["evaluation"]["all_expected_sources_found"] else 0.0
        for record in records
        if record["evaluation"]["all_expected_sources_found"] is not None
    ]
    top1_source_match = [
        1.0 if record["evaluation"]["top1_source_match"] else 0.0
        for record in records
        if record["evaluation"]["top1_source_match"] is not None
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
    mrr = [
        reciprocal_rank(record["retrieved_chunks"], item.get("expected_sources", []))
        for item, record in zip(questions, records, strict=True)
    ]
    latency = [record["latency_seconds"] for record in records]

    failures = [
        {
            "id": record["eval_id"],
            "decision": record["decision"],
            "expected_decision": item.get("expected_decision"),
            "matched_sources": record["evaluation"]["matched_sources"],
            "missing_sources": record["evaluation"]["missing_sources"],
            "concept_coverage": record["evaluation"]["concept_coverage"],
            "top_sources": [chunk["source"] for chunk in record["retrieved_chunks"][:3]],
            "generator_backend": record.get("generator_backend"),
            "generator_error": record.get("generator_error"),
        }
        for item, record in zip(questions, records, strict=True)
        if record["evaluation"].get("all_expected_sources_found") is False
        or record["evaluation"].get("top1_source_match") is False
        or record["evaluation"].get("decision_correct") is False
    ]

    if save_records is not None:
        save_records.parent.mkdir(parents=True, exist_ok=True)
        save_records.write_text(json.dumps(records, indent=2), encoding="utf-8")

    return {
        "question_count": len(records),
        "top_k": top_k,
        "alpha": alpha,
        "generation_enabled": generation_enabled,
        "metrics": {
            "source_hit_at_k": _mean(source_hit),
            "source_match_rate": _mean(source_match),
            "all_expected_sources_found_rate": _mean(all_sources_found),
            "top1_source_match_rate": _mean(top1_source_match),
            "source_precision_at_k": _mean(source_precision_at_k),
            "mean_reciprocal_rank": _mean(mrr),
            "concept_coverage": _mean(concept_coverage),
            "decision_accuracy": _mean(decision_accuracy),
            "avg_latency_seconds": _mean(latency),
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
    args = parser.parse_args()

    result = run_eval(
        args.eval_path,
        args.top_k,
        args.alpha,
        args.write_logs,
        limit=args.limit,
        save_records=args.save_records,
        generation_enabled=not args.retrieval_only,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
