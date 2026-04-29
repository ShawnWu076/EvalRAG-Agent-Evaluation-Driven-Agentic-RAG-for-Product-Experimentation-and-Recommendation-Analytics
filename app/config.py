"""Project configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PLAYBOOK_DIR = DATA_DIR / "playbook"
INDEX_DIR = DATA_DIR / "index"
DEFAULT_INDEX_PATH = INDEX_DIR / "chunks.json"
LOG_DIR = PROJECT_ROOT / "logs"
DEFAULT_LOG_PATH = LOG_DIR / "rag_logs.jsonl"


@dataclass(frozen=True)
class Settings:
    """Runtime settings with environment-variable overrides."""

    model_name: str = os.getenv("EVALRAG_MODEL", "local-rule-generator")
    top_k: int = int(os.getenv("EVALRAG_TOP_K", "5"))
    chunk_size: int = int(os.getenv("EVALRAG_CHUNK_SIZE", "420"))
    chunk_overlap: int = int(os.getenv("EVALRAG_CHUNK_OVERLAP", "80"))
    hybrid_alpha: float = float(os.getenv("EVALRAG_HYBRID_ALPHA", "0.65"))
    log_path: Path = Path(os.getenv("EVALRAG_LOG_PATH", DEFAULT_LOG_PATH))
    index_path: Path = Path(os.getenv("EVALRAG_INDEX_PATH", DEFAULT_INDEX_PATH))


settings = Settings()

