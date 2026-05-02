#!/usr/bin/env python3
"""Run Ragas evaluation over saved EvalRAG records.

This script intentionally consumes records produced by scripts/run_eval.py instead
of re-running the RAG pipeline. That lets us separate generation cost from judge
cost and reuse the same answer/retrieval traces for multiple evaluators.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DEFAULT_RECORDS_PATH = ROOT / "logs" / "openai_eval_full.json"
DEFAULT_OUTPUT_PATH = ROOT / "logs" / "ragas_eval_report.json"
DEFAULT_CSV_OUTPUT_PATH = ROOT / "logs" / "ragas_eval_report.csv"

CANONICAL_METRICS = {
    "faithfulness": ["faithfulness"],
    "answer_relevancy": ["answer_relevancy", "response_relevancy"],
    "context_precision": ["context_precision", "llm_context_precision_with_reference"],
}


def load_records(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"Expected {path} to contain a JSON list of eval records.")
    return data


def _reference_from_record(record: dict[str, Any]) -> str:
    explicit = record.get("ground_truth") or record.get("reference")
    if explicit:
        return str(explicit)
    expected_decision = record.get("expected_decision") or "unknown"
    concepts = record.get("expected_concepts") or []
    concept_text = ", ".join(str(concept) for concept in concepts) if concepts else "the relevant experimentation concepts"
    return (
        f"The ideal answer should recommend `{expected_decision}` and clearly explain the decision using: "
        f"{concept_text}. It should stay grounded in the retrieved playbook context."
    )


def _contexts_from_record(record: dict[str, Any], max_context_chars: int) -> list[str]:
    contexts: list[str] = []
    for chunk in record.get("retrieved_chunks", []):
        text = str(chunk.get("text") or chunk.get("text_preview") or "").strip()
        if text:
            contexts.append(text[:max_context_chars])
    return contexts


def build_ragas_rows(
    records: list[dict[str, Any]],
    max_context_chars: int = 2200,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        answer = str(record.get("answer") or "").strip()
        question = str(record.get("question") or "").strip()
        contexts = _contexts_from_record(record, max_context_chars=max_context_chars)
        if not question or not answer or not contexts:
            continue
        rows.append(
            {
                "eval_id": record.get("eval_id") or record.get("query_id") or f"row_{index + 1}",
                "category": record.get("category") or record.get("expected_decision") or "uncategorized",
                "user_input": question,
                "response": answer,
                "retrieved_contexts": contexts,
                "reference": _reference_from_record(record),
                "expected_decision": record.get("expected_decision"),
                "final_decision": record.get("final_decision") or record.get("decision"),
                "source_match_rate": record.get("evaluation", {}).get("source_match_rate"),
                "custom_failure_hypothesis": record.get("evaluation", {}).get("failure_hypothesis"),
            }
        )
    return rows


def _float_or_none(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def _canonical_metric_value(row: dict[str, Any], metric: str) -> float | None:
    for name in CANONICAL_METRICS[metric]:
        if name in row:
            return _float_or_none(row.get(name))
    return None


def summarize_metric_rows(metric_rows: list[dict[str, Any]]) -> dict[str, float | None]:
    summary: dict[str, float | None] = {}
    for metric in CANONICAL_METRICS:
        values = [value for row in metric_rows if (value := _canonical_metric_value(row, metric)) is not None]
        summary[metric] = round(statistics.mean(values), 4) if values else None
    return summary


def classify_ragas_failures(
    metric_rows: list[dict[str, Any]],
    threshold: float = 0.7,
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for row in metric_rows:
        weak_metrics = {
            metric: value
            for metric in CANONICAL_METRICS
            if (value := _canonical_metric_value(row, metric)) is not None and value < threshold
        }
        if not weak_metrics:
            continue
        if "context_precision" in weak_metrics:
            hypothesis = "retrieval_fail"
        elif "faithfulness" in weak_metrics:
            hypothesis = "hallucination_or_grounding_fail"
        else:
            hypothesis = "answer_relevance_or_reasoning_fail"
        failures.append(
            {
                "eval_id": row.get("eval_id"),
                "category": row.get("category"),
                "failure_hypothesis": hypothesis,
                "weak_metrics": weak_metrics,
                "question": row.get("user_input"),
            }
        )
    return failures


def _dataframe_records(dataframe: Any, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = dataframe.to_dict(orient="records")
    for index, record in enumerate(records):
        if index < len(rows):
            record.setdefault("eval_id", rows[index].get("eval_id"))
            record.setdefault("category", rows[index].get("category"))
            record.setdefault("user_input", rows[index].get("user_input"))
    return records


def _run_modern_ragas(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], Any]:
    from ragas import EvaluationDataset, evaluate

    try:
        from ragas import SingleTurnSample
    except ImportError:  # pragma: no cover - version compatibility
        from ragas.dataset_schema import SingleTurnSample

    from ragas.metrics import Faithfulness, LLMContextPrecisionWithReference, ResponseRelevancy

    samples = [
        SingleTurnSample(
            user_input=row["user_input"],
            response=row["response"],
            retrieved_contexts=row["retrieved_contexts"],
            reference=row["reference"],
        )
        for row in rows
    ]
    dataset = EvaluationDataset(samples=samples)
    result = evaluate(
        dataset,
        metrics=[Faithfulness(), ResponseRelevancy(), LLMContextPrecisionWithReference()],
    )
    dataframe = result.to_pandas()
    return _dataframe_records(dataframe, rows), dataframe


def _run_legacy_ragas(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], Any]:
    from datasets import Dataset
    from ragas import evaluate
    from ragas.metrics import answer_relevancy, context_precision, faithfulness

    dataset = Dataset.from_list(
        [
            {
                "question": row["user_input"],
                "answer": row["response"],
                "contexts": row["retrieved_contexts"],
                "ground_truth": row["reference"],
            }
            for row in rows
        ]
    )
    result = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision],
    )
    dataframe = result.to_pandas()
    return _dataframe_records(dataframe, rows), dataframe


def run_ragas(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], Any]:
    try:
        return _run_modern_ragas(rows)
    except ImportError:
        return _run_legacy_ragas(rows)


def write_report(
    output_path: Path,
    prepared_rows: list[dict[str, Any]],
    metric_rows: list[dict[str, Any]],
    threshold: float,
) -> dict[str, Any]:
    report = {
        "record_count": len(prepared_rows),
        "ragas_metrics": summarize_metric_rows(metric_rows),
        "failure_threshold": threshold,
        "failure_analysis": classify_ragas_failures(metric_rows, threshold=threshold),
        "records": metric_rows,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", type=Path, default=DEFAULT_RECORDS_PATH, help="Saved records from scripts/run_eval.py --save-records.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH, help="JSON report output path.")
    parser.add_argument("--csv-output", type=Path, default=DEFAULT_CSV_OUTPUT_PATH, help="Optional CSV output path.")
    parser.add_argument("--limit", type=int, default=None, help="Evaluate only the first N saved records.")
    parser.add_argument("--failure-threshold", type=float, default=0.7, help="Scores below this are surfaced in failure_analysis.")
    parser.add_argument("--max-context-chars", type=int, default=2200, help="Max characters kept per retrieved context.")
    parser.add_argument("--prepare-only", action="store_true", help="Prepare the Ragas dataset JSON without calling Ragas or an LLM judge.")
    args = parser.parse_args()

    records = load_records(args.records)
    if args.limit is not None:
        records = records[: args.limit]
    rows = build_ragas_rows(records, max_context_chars=args.max_context_chars)
    if not rows:
        raise SystemExit("No usable records found. Run scripts/run_eval.py --save-records first.")

    if args.prepare_only:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps({"record_count": len(rows), "records": rows}, indent=2), encoding="utf-8")
        print(json.dumps({"record_count": len(rows), "prepared_dataset": str(args.output)}, indent=2))
        return

    try:
        metric_rows, dataframe = run_ragas(rows)
    except ImportError as exc:
        raise SystemExit(
            "Ragas is not installed. Install dependencies with `pip install -r requirements.txt`, "
            "then rerun this command."
        ) from exc

    args.csv_output.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(args.csv_output, index=False)
    report = write_report(args.output, rows, metric_rows, threshold=args.failure_threshold)
    print(json.dumps({k: v for k, v in report.items() if k != "records"}, indent=2))


if __name__ == "__main__":
    main()
