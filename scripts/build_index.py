#!/usr/bin/env python3
"""Build a JSON chunk index from the playbook markdown files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.chunking import build_chunks, save_chunks  # noqa: E402
from app.config import DEFAULT_INDEX_PATH, PLAYBOOK_DIR, settings  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--playbook-dir", type=Path, default=PLAYBOOK_DIR)
    parser.add_argument("--index-path", type=Path, default=DEFAULT_INDEX_PATH)
    parser.add_argument("--chunk-size", type=int, default=settings.chunk_size)
    parser.add_argument("--overlap", type=int, default=settings.chunk_overlap)
    args = parser.parse_args()

    chunks = build_chunks(
        args.playbook_dir,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        semantic_enabled=settings.chunk_semantic_enable,
        semantic_model=settings.chunk_semantic_model,
        semantic_device=settings.chunk_semantic_device,
        semantic_offline=settings.chunk_semantic_offline,
        semantic_min_size=settings.chunk_semantic_min_size,
    )
    save_chunks(chunks, args.index_path)
    print(f"Built {len(chunks)} chunks from {args.playbook_dir} -> {args.index_path}")


if __name__ == "__main__":
    main()
