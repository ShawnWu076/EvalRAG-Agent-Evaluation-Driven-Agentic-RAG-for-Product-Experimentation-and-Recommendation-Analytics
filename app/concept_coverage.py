"""Deterministic concept coverage evaluation."""

from __future__ import annotations

import re
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


def evaluate_concepts(
    answer: str,
    expected_concepts: list[str],
    semantic_threshold: float = 0.8,
    fuzzy_threshold: float = 0.88,
) -> dict[str, Any]:
    """Evaluate expected concept coverage with exact and deterministic semantic matching.

    This intentionally avoids LLM-as-judge. It first checks exact normalized phrase
    matches, then checks stemmed content-token coverage, then a conservative fuzzy
    phrase-window score. The output is inspectable and repeatable.
    """

    answer_norm = normalize_text(answer)
    answer_token_set = set(concept_tokens(answer))
    matches: list[dict[str, Any]] = []
    covered: list[str] = []
    missing: list[str] = []

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

        if covered_flag:
            covered.append(concept)
        else:
            missing.append(concept)

        matches.append(
            {
                "concept": concept,
                "covered": covered_flag,
                "method": method,
                "score": round(score, 4),
                "matched_terms": token_hits,
            }
        )

    coverage = round(len(covered) / len(expected_concepts), 4) if expected_concepts else None
    return {
        "concept_coverage": coverage,
        "covered_concepts": covered,
        "missing_concepts": missing,
        "concept_matches": matches,
        "concept_coverage_method": "exact_or_deterministic_semantic",
    }
