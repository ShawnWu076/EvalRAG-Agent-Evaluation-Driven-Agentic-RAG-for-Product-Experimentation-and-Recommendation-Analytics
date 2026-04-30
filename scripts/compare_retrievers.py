#!/usr/bin/env python3
"""Compare BM25-only, vector-only, and hybrid retrieval settings."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.run_eval import DEFAULT_EVAL_PATH, run_eval  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-path", type=Path, default=DEFAULT_EVAL_PATH)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    configs = {
        "bm25_only": 0.0,
        "vector_only": 1.0,
        "hybrid_35_vector": 0.35,
        "hybrid_65_vector": 0.65,
    }
    results = {}
    for name, alpha in configs.items():
        results[name] = run_eval(
            args.eval_path,
            args.top_k,
            alpha,
            write_logs=False,
            generation_enabled=False,
        )["metrics"]
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
