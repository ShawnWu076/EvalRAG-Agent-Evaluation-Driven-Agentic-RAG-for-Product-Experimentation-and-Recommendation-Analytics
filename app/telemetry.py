"""JSONL telemetry logging for RAG traces."""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any

from app.config import settings


def new_query_id(prefix: str = "q") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def utc_timestamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def append_log(record: dict[str, Any], log_path: Path | None = None) -> None:
    path = Path(log_path or settings.log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True) + "\n")

