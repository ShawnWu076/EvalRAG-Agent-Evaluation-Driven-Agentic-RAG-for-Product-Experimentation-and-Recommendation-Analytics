#!/usr/bin/env python3
"""Inspect Ragas failures with retrieved chunks and answer evidence.

The Ragas aggregate report is useful, but failure analysis needs the actual
question, answer, reference, expected sources, and retrieved chunks side by side.
This script joins `scripts/run_eval.py --save-records` output with
`scripts/run_ragas_eval.py` output and writes a compact Markdown diagnostic.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


DEFAULT_RECORDS = Path("logs/openai_eval_playbook_v2_top8.json")
DEFAULT_RAGAS = Path("logs/ragas_eval_playbook_v2_top8.json")
DEFAULT_OUTPUT = Path("logs/failure_analysis_playbook_v2_top8.md")
METRICS = ["faithfulness", "answer_relevancy", "context_precision", "context_recall", "answer_correctness"]


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def clip(text: Any, limit: int) -> str:
    value = str(text or "").strip()
    value = "\n".join(line.rstrip() for line in value.splitlines())
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def metric_value(row: dict[str, Any], metric: str) -> float | None:
    value = row.get(metric)
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def fmt_metric(value: float | None) -> str:
    return "NA" if value is None else f"{value:.3f}"


def case_diagnosis(weak: dict[str, float], ragas_row: dict[str, Any], eval_record: dict[str, Any]) -> str:
    precision = metric_value(ragas_row, "context_precision")
    recall = metric_value(ragas_row, "context_recall")
    correctness = metric_value(ragas_row, "answer_correctness")
    faithfulness = metric_value(ragas_row, "faithfulness")
    relevancy = metric_value(ragas_row, "answer_relevancy")
    missing_sources = eval_record.get("evaluation", {}).get("missing_sources", [])
    top_sources = [chunk.get("source") for chunk in eval_record.get("retrieved_chunks", [])[:3]]

    if precision is not None and precision < 0.7:
        return "Likely retrieval ranking/noise: Ragas says retrieved contexts include less useful chunks. Inspect top sources and query terms."
    if recall is not None and recall < 0.7 and precision is not None and precision >= 0.85:
        if missing_sources:
            return f"Likely coverage gap: retrieved chunks are relevant but missing expected source(s): {', '.join(missing_sources)}."
        return "Likely reference/chunk coverage gap: retrieved chunks are relevant, but they do not cover the ideal answer broadly enough."
    if faithfulness is not None and faithfulness < 0.7:
        return "Likely grounding gap: answer includes useful claims that Ragas cannot directly infer from retrieved chunks."
    if correctness is not None and correctness < 0.7:
        return "Likely answer/reference alignment gap: final answer may be reasonable, but it differs from the current ground-truth wording."
    if relevancy is not None and relevancy < 0.7:
        return "Likely response-style gap: answer may be too broad, indirect, or over-explanatory for the question."
    if top_sources:
        return f"No obvious single cause from metrics; inspect top sources: {', '.join(str(s) for s in top_sources)}."
    return "No obvious single cause from metrics."


def build_joined_cases(records_path: Path, ragas_path: Path) -> list[dict[str, Any]]:
    records = load_json(records_path)
    ragas_report = load_json(ragas_path)
    if not isinstance(records, list):
        raise ValueError(f"{records_path} should contain a JSON list of eval records.")
    record_by_id = {str(row.get("eval_id") or row.get("query_id")): row for row in records}
    failure_by_id = {str(row.get("eval_id")): row for row in ragas_report.get("failure_analysis", [])}
    ragas_by_id = {str(row.get("eval_id")): row for row in ragas_report.get("records", [])}

    joined = []
    for eval_id, failure in failure_by_id.items():
        record = record_by_id.get(eval_id, {})
        ragas_row = ragas_by_id.get(eval_id, {})
        joined.append(
            {
                "eval_id": eval_id,
                "category": failure.get("category") or record.get("category") or record.get("expected_decision"),
                "failure_hypothesis": failure.get("failure_hypothesis", "unknown"),
                "weak_metrics": failure.get("weak_metrics", {}),
                "question": failure.get("question") or record.get("question") or ragas_row.get("user_input"),
                "record": record,
                "ragas": ragas_row,
            }
        )
    return sorted(joined, key=lambda row: row["eval_id"])


def write_report(cases: list[dict[str, Any]], output: Path, max_chunks: int, max_chunk_chars: int, max_answer_chars: int) -> str:
    by_failure = defaultdict(list)
    by_category = defaultdict(list)
    weak_metric_counts = Counter()
    for case in cases:
        by_failure[case["failure_hypothesis"]].append(case)
        by_category[case["category"]].append(case)
        weak_metric_counts.update(case["weak_metrics"].keys())

    lines: list[str] = []
    lines.append("# Ragas Failure Inspection")
    lines.append("")
    lines.append(f"Failure cases: {len(cases)}")
    lines.append("")
    lines.append("## Weak Metric Counts")
    for metric, count in weak_metric_counts.most_common():
        lines.append(f"- {metric}: {count}")
    lines.append("")
    lines.append("## Failure Hypothesis Groups")
    for group, items in sorted(by_failure.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        ids = ", ".join(case["eval_id"] for case in items)
        lines.append(f"- {group}: {len(items)} cases ({ids})")
    lines.append("")
    lines.append("## Decision Category Groups")
    for group, items in sorted(by_category.items(), key=lambda kv: (-len(kv[1]), str(kv[0]))):
        ids = ", ".join(case["eval_id"] for case in items)
        lines.append(f"- {group}: {len(items)} cases ({ids})")
    lines.append("")

    for group, items in sorted(by_failure.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        lines.append(f"## Failure Type: {group}")
        lines.append("")
        for case in items:
            record = case["record"]
            ragas = case["ragas"]
            evaluation = record.get("evaluation", {})
            lines.append(f"### {case['eval_id']} | expected={record.get('expected_decision') or case['category']}")
            lines.append("")
            lines.append(f"Question: {case['question']}")
            lines.append("")
            lines.append("Metrics: " + ", ".join(f"{m}={fmt_metric(metric_value(ragas, m))}" for m in METRICS))
            lines.append("Weak metrics: " + json.dumps(case["weak_metrics"], ensure_ascii=False))
            lines.append(f"Diagnosis: {case_diagnosis(case['weak_metrics'], ragas, record)}")
            lines.append("")
            lines.append("Expected sources: " + ", ".join(record.get("expected_sources", []) or []))
            lines.append("Matched sources: " + ", ".join(evaluation.get("matched_sources", []) or []))
            missing_sources = evaluation.get("missing_sources", []) or []
            if missing_sources:
                lines.append("Missing sources: " + ", ".join(missing_sources))
            top_sources = []
            for chunk in record.get("retrieved_chunks", [])[:max_chunks]:
                top_sources.append(f"{chunk.get('rank')}. {chunk.get('source')} | {chunk.get('heading')} | score={chunk.get('score')}")
            lines.append("Top retrieved chunks:")
            for source in top_sources:
                lines.append(f"- {source}")
            lines.append("")
            lines.append("Reference:")
            lines.append(clip(ragas.get("reference") or record.get("ground_truth") or "", 700))
            lines.append("")
            lines.append("Answer preview:")
            lines.append(clip(record.get("answer") or ragas.get("response") or "", max_answer_chars))
            lines.append("")
            lines.append("Retrieved chunk previews:")
            for chunk in record.get("retrieved_chunks", [])[:max_chunks]:
                lines.append(f"- [{chunk.get('rank')}] {chunk.get('source')} / {chunk.get('heading')}")
                lines.append("  " + clip(chunk.get("text"), max_chunk_chars).replace("\n", "\n  "))
            lines.append("")

    text = "\n".join(lines).rstrip() + "\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    return text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", type=Path, default=DEFAULT_RECORDS)
    parser.add_argument("--ragas-report", type=Path, default=DEFAULT_RAGAS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-chunks", type=int, default=4)
    parser.add_argument("--max-chunk-chars", type=int, default=650)
    parser.add_argument("--max-answer-chars", type=int, default=1400)
    parser.add_argument("--print", action="store_true", help="Also print the report to stdout.")
    args = parser.parse_args()

    cases = build_joined_cases(args.records, args.ragas_report)
    report = write_report(
        cases,
        output=args.output,
        max_chunks=args.max_chunks,
        max_chunk_chars=args.max_chunk_chars,
        max_answer_chars=args.max_answer_chars,
    )
    print(json.dumps({"failure_cases": len(cases), "output": str(args.output)}, indent=2))
    if args.print:
        print(report)


if __name__ == "__main__":
    main()
