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


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    """Runtime settings with environment-variable overrides."""

    model_name: str = os.getenv("EVALRAG_MODEL", "local-rule-generator")
    generator_backend: str = os.getenv("EVALRAG_GENERATOR", "rule").strip().lower()
    llm_base_url: str = os.getenv("EVALRAG_LLM_BASE_URL", "http://localhost:11434/v1")
    llm_model: str = os.getenv("EVALRAG_LLM_MODEL", "qwen3:14b")
    llm_api_key: str = os.getenv("EVALRAG_LLM_API_KEY", "ollama")
    llm_temperature: float = float(os.getenv("EVALRAG_LLM_TEMPERATURE", "0.2"))
    llm_max_tokens: int = int(os.getenv("EVALRAG_LLM_MAX_TOKENS", "1400"))
    llm_timeout_seconds: float = float(os.getenv("EVALRAG_LLM_TIMEOUT_SECONDS", "90"))
    llm_fallback_enabled: bool = _env_bool("EVALRAG_LLM_FALLBACK_ENABLED", True)
    top_k: int = int(os.getenv("EVALRAG_TOP_K", "5"))
    chunk_size: int = int(os.getenv("EVALRAG_CHUNK_SIZE", "420"))
    chunk_overlap: int = int(os.getenv("EVALRAG_CHUNK_OVERLAP", "80"))
    chunk_semantic_enable: bool = _env_bool("EVALRAG_CHUNK_SEMANTIC_ENABLE", True)
    chunk_semantic_model: str = os.getenv("EVALRAG_CHUNK_SEMANTIC_MODEL", "BAAI/bge-small-en-v1.5")
    chunk_semantic_device: str = os.getenv("EVALRAG_CHUNK_SEMANTIC_DEVICE", "cpu")
    chunk_semantic_offline: bool = _env_bool("EVALRAG_CHUNK_SEMANTIC_OFFLINE", True)
    chunk_semantic_min_size: int = int(os.getenv("EVALRAG_CHUNK_SEMANTIC_MIN_SIZE", "160"))
    hybrid_alpha: float = float(os.getenv("EVALRAG_HYBRID_ALPHA", "0.65"))
    log_path: Path = Path(os.getenv("EVALRAG_LOG_PATH", DEFAULT_LOG_PATH))
    index_path: Path = Path(os.getenv("EVALRAG_INDEX_PATH", DEFAULT_INDEX_PATH))


settings = Settings()
