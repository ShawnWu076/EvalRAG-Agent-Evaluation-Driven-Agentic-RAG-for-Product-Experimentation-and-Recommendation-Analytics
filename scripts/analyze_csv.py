#!/usr/bin/env python3
"""Analyze a synthetic experiment CSV and generate a launch memo."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.rag_pipeline import EvalRAGPipeline  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument(
        "--question",
        default="Should we launch this recommendation experiment?",
    )
    parser.add_argument("--show-tools", action="store_true")
    args = parser.parse_args()

    csv_text = args.csv_path.read_text(encoding="utf-8")
    pipeline = EvalRAGPipeline()
    record = pipeline.answer(args.question, csv_text=csv_text)

    print(record["answer"])
    if args.show_tools:
        print("\n## Tool Summary JSON")
        print(json.dumps(record.get("tool_summary", {}), indent=2))


if __name__ == "__main__":
    main()
