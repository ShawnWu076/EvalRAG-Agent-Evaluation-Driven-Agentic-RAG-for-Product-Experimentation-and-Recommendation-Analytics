"""Strict LLM judge for concept coverage evaluation."""

from __future__ import annotations

import json
import re
from typing import Any

from app.llm_generator import LLMGenerationConfig, LLMGenerationError, call_openai_compatible_chat


def _truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "\n...[truncated]"


def _extract_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", stripped, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        stripped = fenced.group(1).strip()
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        parsed = json.loads(stripped[start : end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("Concept judge response must be a JSON object.")
    return parsed


def build_concept_judge_messages(answer: str, concepts: list[str]) -> list[dict[str, str]]:
    concept_lines = "\n".join(f"- {concept}" for concept in concepts)
    system = """You are a strict evaluator for RAG answer concept coverage.

You must judge whether the answer explicitly expresses the same operational idea as each expected concept.
Be conservative:
- Mark covered=true only when the answer and concept mean the same thing in this product experimentation context.
- Topical overlap, vague caution, or adjacent ideas are not enough.
- Do not reward a concept just because the answer mentions one related word.
- Do not infer missing details from the question, playbook, or your own background knowledge.
- If a concept requires an action, risk, metric, or design idea, the answer must state that idea clearly.
- If uncertain, mark covered=false.
- Use confidence >= 0.80 only for genuinely equivalent coverage.

Return valid JSON only. Do not include markdown.
"""
    user = f"""Answer to evaluate:
{_truncate(answer, 7000)}

Expected concepts:
{concept_lines}

Return this JSON schema exactly:
{{
  "results": [
    {{
      "concept": "one expected concept copied exactly",
      "covered": false,
      "confidence": 0.0,
      "rationale": "brief reason, 25 words or fewer"
    }}
  ]
}}
"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def judge_concepts(
    answer: str,
    concepts: list[str],
    config: LLMGenerationConfig,
    min_confidence: float = 0.8,
) -> list[dict[str, Any]]:
    """Use an OpenAI-compatible model as a strict judge for missing concepts."""

    if not concepts:
        return []
    messages = build_concept_judge_messages(answer, concepts)
    raw = call_openai_compatible_chat(messages, config)
    try:
        parsed = _extract_json_object(raw)
    except (json.JSONDecodeError, ValueError) as exc:
        raise LLMGenerationError(f"Concept judge returned invalid JSON: {raw[:500]}") from exc

    raw_results = parsed.get("results", [])
    if not isinstance(raw_results, list):
        raise LLMGenerationError("Concept judge response must contain a results list.")

    by_concept: dict[str, dict[str, Any]] = {}
    for item in raw_results:
        if not isinstance(item, dict):
            continue
        concept = str(item.get("concept", "")).strip()
        if concept:
            by_concept[concept.lower()] = item

    normalized: list[dict[str, Any]] = []
    for concept in concepts:
        item = by_concept.get(concept.lower(), {})
        try:
            confidence = float(item.get("confidence", 0.0))
        except (TypeError, ValueError):
            confidence = 0.0
        raw_covered = bool(item.get("covered", False))
        covered = raw_covered and confidence >= min_confidence
        normalized.append(
            {
                "concept": concept,
                "covered": covered,
                "raw_covered": raw_covered,
                "confidence": round(max(0.0, min(1.0, confidence)), 4),
                "rationale": str(item.get("rationale", "")).strip()[:240],
            }
        )
    return normalized
