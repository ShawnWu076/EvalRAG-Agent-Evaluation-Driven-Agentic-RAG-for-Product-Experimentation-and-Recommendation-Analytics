#!/usr/bin/env python3
"""Ask EvalRAG a single question from the command line."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.rag_pipeline import EvalRAGPipeline  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--show-metadata", action="store_true")
    args = parser.parse_args()

    pipeline = EvalRAGPipeline(top_k=args.top_k)
    record = pipeline.answer(args.question)
    print(record["answer"])
    if args.show_metadata:
        print("\n## Generation Metadata")
        print(f"model: {record['model']}")
        print(f"generator_backend: {record.get('generator_backend', 'openai_compatible')}")
        if record.get("generator_error"):
            print(f"generator_error: {record['generator_error']}")


if __name__ == "__main__":
    main()

