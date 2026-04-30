"""Concept coverage evaluation with deterministic matching and optional strict judge."""

from __future__ import annotations

import re
from collections.abc import Callable
from difflib import SequenceMatcher
from typing import Any


TOKEN_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "should",
    "the",
    "to",
    "with",
}
SPECIAL_STEMS = {
    "analyses": "analysis",
    "analyze": "analysis",
    "analyzed": "analysis",
    "analyzing": "analysis",
    "guardrails": "guardrail",
    "metrics": "metric",
    "segments": "segment",
    "segmented": "segment",
    "cohorts": "cohort",
    "conversions": "conversion",
    "converted": "conversion",
    "converting": "conversion",
    "complaints": "complaint",
    "complained": "complaint",
    "randomized": "randomization",
    "randomize": "randomization",
    "randomisation": "randomization",
    "assignments": "assignment",
    "assigned": "assignment",
    "logs": "logging",
    "logged": "logging",
    "valid": "validity",
    "invalid": "validity",
    "experiments": "experiment",
    "experimental": "experiment",
    "advertisers": "advertiser",
    "sellers": "seller",
    "markets": "market",
    "rollouts": "rollout",
    "rollout": "rollout",
    "roll": "rollout",
}
ConceptJudge = Callable[[str, list[str]], list[dict[str, Any]]]


def normalize_text(text: str) -> str:
    text = text.lower().replace("-", " ").replace("_", " ")
    return re.sub(r"\s+", " ", text).strip()


def _stem(token: str) -> str:
    token = SPECIAL_STEMS.get(token, token)
    if token in SPECIAL_STEMS.values():
        return token
    for suffix in ("ingly", "edly", "ing", "ed", "ies", "s"):
        if len(token) > len(suffix) + 3 and token.endswith(suffix):
            if suffix == "ies":
                return token[: -len(suffix)] + "y"
            return token[: -len(suffix)]
    return token


def concept_tokens(text: str) -> list[str]:
    return [_stem(token) for token in TOKEN_RE.findall(normalize_text(text)) if token not in STOPWORDS]


def _window_similarity(concept: str, answer: str) -> float:
    concept_norm = normalize_text(concept)
    answer_tokens = TOKEN_RE.findall(normalize_text(answer))
    concept_len = max(1, len(TOKEN_RE.findall(concept_norm)))
    best = 0.0
    for size in range(max(1, concept_len - 1), concept_len + 3):
        for start in range(0, max(0, len(answer_tokens) - size) + 1):
            window = " ".join(answer_tokens[start : start + size])
            best = max(best, SequenceMatcher(None, concept_norm, window).ratio())
    return best


def _coverage(covered: list[str], expected_concepts: list[str]) -> float | None:
    return round(len(covered) / len(expected_concepts), 4) if expected_concepts else None


def _apply_judge_results(
    matches: list[dict[str, Any]],
    judge_results: list[dict[str, Any]],
    judge_min_confidence: float,
) -> None:
    by_concept = {normalize_text(str(item.get("concept", ""))): item for item in judge_results}
    for match in matches:
        if match["covered"]:
            continue
        judged = by_concept.get(normalize_text(str(match["concept"])))
        if not judged:
            continue
        try:
            confidence = float(judged.get("confidence", 0.0) or 0.0)
        except (TypeError, ValueError):
            confidence = 0.0
        raw_covered = bool(judged.get("covered", False))
        judge_covered = raw_covered and confidence >= judge_min_confidence
        match["judge_covered"] = judge_covered
        match["judge_raw_covered"] = raw_covered
        match["judge_confidence"] = round(max(0.0, min(1.0, confidence)), 4)
        match["judge_rationale"] = str(judged.get("rationale", ""))[:240]
        if judge_covered:
            match["covered"] = True
            match["method"] = "strict_llm_judge"
            match["score"] = round(confidence, 4)


def evaluate_concepts(
    answer: str,
    expected_concepts: list[str],
    semantic_threshold: float = 0.8,
    fuzzy_threshold: float = 0.88,
    coverage_target: float = 0.8,
    llm_judge: ConceptJudge | None = None,
    judge_min_confidence: float = 0.8,
) -> dict[str, Any]:
    """Evaluate concept coverage.

    The first pass is deterministic and cheap: exact normalized phrases, stemmed
    content-token overlap, and conservative fuzzy phrase windows. If that score
    is below coverage_target, an optional strict LLM judge can review only the
    still-missing concepts. The judge is intentionally a final check, not the
    default source of truth for every concept.
    """

    answer_norm = normalize_text(answer)
    answer_token_set = set(concept_tokens(answer))
    matches: list[dict[str, Any]] = []

    for concept in expected_concepts:
        concept_norm = normalize_text(concept)
        tokens = concept_tokens(concept)
        token_hits = sorted(token for token in set(tokens) if token in answer_token_set)
        token_score = len(token_hits) / len(set(tokens)) if tokens else 0.0
        fuzzy_score = _window_similarity(concept, answer) if concept_norm not in answer_norm else 1.0
        covered_flag = False
        method = "missing"
        score = max(token_score, fuzzy_score)

        if concept_norm and concept_norm in answer_norm:
            covered_flag = True
            method = "exact"
            score = 1.0
        elif tokens and token_score >= semantic_threshold:
            covered_flag = True
            method = "semantic_token_overlap"
        elif fuzzy_score >= fuzzy_threshold:
            covered_flag = True
            method = "fuzzy_phrase_window"

        matches.append(
            {
                "concept": concept,
                "covered": covered_flag,
                "method": method,
                "score": round(score, 4),
                "matched_terms": token_hits,
            }
        )

    deterministic_covered = [str(match["concept"]) for match in matches if match["covered"]]
    deterministic_coverage = _coverage(deterministic_covered, expected_concepts)
    judge_used = False
    judge_error = None

    if (
        llm_judge
        and expected_concepts
        and deterministic_coverage is not None
        and deterministic_coverage < coverage_target
    ):
        missing_for_judge = [str(match["concept"]) for match in matches if not match["covered"]]
        if missing_for_judge:
            judge_used = True
            try:
                judge_results = llm_judge(answer, missing_for_judge)
                _apply_judge_results(matches, judge_results, judge_min_confidence)
            except Exception as exc:  # pragma: no cover - defensive eval telemetry
                judge_error = str(exc)

    covered = [str(match["concept"]) for match in matches if match["covered"]]
    missing = [str(match["concept"]) for match in matches if not match["covered"]]
    coverage = _coverage(covered, expected_concepts)
    method = "exact_or_deterministic_semantic"
    if judge_used:
        method = "exact_or_deterministic_semantic_then_strict_llm_judge"
    return {
        "concept_coverage": coverage,
        "deterministic_concept_coverage": deterministic_coverage,
        "covered_concepts": covered,
        "missing_concepts": missing,
        "concept_matches": matches,
        "concept_coverage_method": method,
        "concept_judge_used": judge_used,
        "concept_judge_error": judge_error,
    }
