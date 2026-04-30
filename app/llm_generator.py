"""OpenAI-compatible local LLM answer generation."""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


class LLMGenerationError(RuntimeError):
    """Raised when an OpenAI-compatible generation backend cannot produce text."""


@dataclass(frozen=True)
class LLMGenerationConfig:
    base_url: str
    model: str
    api_key: str
    temperature: float
    max_tokens: int
    timeout_seconds: float


def strip_thinking_blocks(text: str) -> str:
    """Remove visible reasoning blocks from models that emit <think>...</think>."""

    stripped = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
    return stripped.strip()


def _truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "\n...[truncated]"


def _format_retrieved_context(retrieved: list[dict[str, Any]], max_chars_per_chunk: int = 1400) -> str:
    blocks: list[str] = []
    for item in retrieved:
        source = item.get("source", "unknown")
        heading = item.get("heading", "")
        score = item.get("score", "")
        text = _truncate(str(item.get("text", "")), max_chars_per_chunk)
        blocks.append(
            f"[chunk_id={item.get('chunk_id', '')} source={source} heading={heading} score={score}]\n{text}"
        )
    return "\n\n".join(blocks)


def _format_tool_summary(tool_summary: dict[str, Any] | None) -> str:
    if not tool_summary:
        return "No tool outputs were provided."
    return _truncate(json.dumps(tool_summary, indent=2, sort_keys=True), 6000)


def build_llm_messages(
    question: str,
    retrieved: list[dict[str, Any]],
    decision: str,
    tool_summary: dict[str, Any] | None = None,
) -> list[dict[str, str]]:
    """Build a grounded prompt for a local or hosted OpenAI-compatible chat model."""

    sources = ", ".join(dict.fromkeys(str(item.get("source", "unknown")) for item in retrieved))
    system = """You are EvalRAG Agent, an analytics copilot for product experimentation and recommendation analytics.

Your job is to write a concise, source-grounded launch decision memo using only:
1. the user question,
2. retrieved playbook context,
3. statistical tool outputs when provided.

Rules:
- Keep the final decision label exactly as provided by the system.
- Do not invent exact thresholds, company policies, p-values, or metric results that are not present.
- If evidence is missing, say what is missing and how it affects the decision.
- If SRM, logging, assignment, or validity checks fail, do not treat metric lift as causal launch evidence.
- Cite retrieved source filenames in the Retrieved Sources section.
- Return markdown only.
"""
    user = f"""User question:
{question}

Required decision label:
`{decision}`

Retrieved playbook context:
{_format_retrieved_context(retrieved)}

Statistical tool outputs:
{_format_tool_summary(tool_summary)}

Write the answer in exactly this structure:

## Short Answer

## Decision Recommendation
Use exactly this label: `{decision}`

## Reasoning

## Metrics to Check

## Suggested Next Steps

## Risks / Caveats

## Retrieved Sources
Include these source filenames when relevant: {sources}
"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def _chat_completions_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    return f"{base}/chat/completions"


def call_openai_compatible_chat(messages: list[dict[str, str]], config: LLMGenerationConfig) -> str:
    """Call a local or hosted OpenAI-compatible /chat/completions endpoint."""

    payload = {
        "model": config.model,
        "messages": messages,
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
        "stream": False,
    }
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if config.api_key:
        headers["Authorization"] = f"Bearer {config.api_key}"

    req = urllib.request.Request(
        _chat_completions_url(config.base_url),
        data=data,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=config.timeout_seconds) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        detail = body[:500] if body else str(exc)
        raise LLMGenerationError(f"LLM endpoint returned HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise LLMGenerationError(f"LLM endpoint request failed: {exc}") from exc

    try:
        body = json.loads(raw)
        content = body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise LLMGenerationError(f"Unexpected LLM response format: {raw[:500]}") from exc

    if not isinstance(content, str) or not content.strip():
        raise LLMGenerationError("LLM endpoint returned an empty message.")
    return strip_thinking_blocks(content)


def generate_llm_answer(
    question: str,
    retrieved: list[dict[str, Any]],
    decision: str,
    config: LLMGenerationConfig,
    tool_summary: dict[str, Any] | None = None,
) -> str:
    messages = build_llm_messages(question, retrieved, decision, tool_summary)
    answer = call_openai_compatible_chat(messages, config)
    if "## Retrieved Sources" not in answer:
        sources = "\n".join(f"- {source}" for source in dict.fromkeys(str(item.get("source", "unknown")) for item in retrieved))
        answer = answer.rstrip() + f"\n\n## Retrieved Sources\n{sources}\n"
    return answer
