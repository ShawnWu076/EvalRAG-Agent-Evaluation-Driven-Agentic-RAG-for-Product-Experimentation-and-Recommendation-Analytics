#!/usr/bin/env python3
"""Run EvalRAG scenario evaluation."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.rag_pipeline import EvalRAGPipeline  # noqa: E402


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


def run_eval(
    path: Path,
    top_k: int,
    alpha: float,
    write_logs: bool,
    limit: int | None = None,
    save_records: Path | None = None,
) -> dict[str, Any]:
    questions = load_jsonl(path)
    if limit is not None:
        questions = questions[:limit]
    pipeline = EvalRAGPipeline(top_k=top_k, alpha=alpha)
    records: list[dict[str, Any]] = []
    for item in questions:
        record = pipeline.answer(
            item["question"],
            expected_sources=item.get("expected_sources", []),
            expected_concepts=item.get("expected_concepts", []),
            expected_decision=item.get("expected_decision"),
            log=write_logs,
        )
        record["eval_id"] = item["id"]
        records.append(record)

    source_hit = [1.0 if record["evaluation"]["source_hit"] else 0.0 for record in records]
    source_match = [
        record["evaluation"]["source_match_rate"]
        for record in records
        if record["evaluation"]["source_match_rate"] is not None
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
        reciprocal_rank(record["retrieved_chunks"], load_jsonl(path)[idx].get("expected_sources", []))
        for idx, record in enumerate(records)
    ]
    latency = [record["latency_seconds"] for record in records]

    failures = [
        {
            "id": record["eval_id"],
            "decision": record["decision"],
            "expected_decision": load_jsonl(path)[idx].get("expected_decision"),
            "matched_sources": record["evaluation"]["matched_sources"],
            "concept_coverage": record["evaluation"]["concept_coverage"],
            "top_sources": [chunk["source"] for chunk in record["retrieved_chunks"][:3]],
        }
        for idx, record in enumerate(records)
        if not record["evaluation"]["source_hit"] or record["evaluation"]["decision_correct"] is False
    ]

    if save_records is not None:
        save_records.parent.mkdir(parents=True, exist_ok=True)
        save_records.write_text(json.dumps(records, indent=2), encoding="utf-8")

    return {
        "question_count": len(records),
        "top_k": top_k,
        "alpha": alpha,
        "metrics": {
            "source_hit_at_k": round(statistics.mean(source_hit), 4) if source_hit else None,
            "source_match_rate": round(statistics.mean(source_match), 4) if source_match else None,
            "mean_reciprocal_rank": round(statistics.mean(mrr), 4) if mrr else None,
            "concept_coverage": round(statistics.mean(concept_coverage), 4) if concept_coverage else None,
            "decision_accuracy": round(statistics.mean(decision_accuracy), 4) if decision_accuracy else None,
            "avg_latency_seconds": round(statistics.mean(latency), 4) if latency else None,
        },
        "failures": failures[:12],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-path", type=Path, default=DEFAULT_EVAL_PATH)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--alpha", type=float, default=0.65, help="Hybrid score weight for vector score.")
    parser.add_argument("--write-logs", action="store_true")
    parser.add_argument("--limit", type=int, default=None, help="Evaluate only the first N questions.")
    parser.add_argument("--save-records", type=Path, default=None, help="Write per-question eval records to a JSON file.")
    args = parser.parse_args()

    result = run_eval(
        args.eval_path,
        args.top_k,
        args.alpha,
        args.write_logs,
        limit=args.limit,
        save_records=args.save_records,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

