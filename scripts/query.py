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
    args = parser.parse_args()

    pipeline = EvalRAGPipeline(top_k=args.top_k)
    record = pipeline.answer(args.question)
    print(record["answer"])


if __name__ == "__main__":
    main()

