from __future__ import annotations

import unittest

from app.concept_coverage import evaluate_concepts


class ConceptCoverageTests(unittest.TestCase):
    def test_exact_match_counts_as_covered(self) -> None:
        result = evaluate_concepts("Run segment analysis before launch.", ["segment analysis"])
        self.assertEqual(result["concept_coverage"], 1.0)
        self.assertEqual(result["concept_matches"][0]["method"], "exact")

    def test_stemmed_token_overlap_counts_as_semantic_coverage(self) -> None:
        result = evaluate_concepts(
            "Check guardrails and metrics by user segments.",
            ["guardrail metric", "segment analysis"],
        )
        self.assertEqual(result["concept_coverage"], 0.5)
        self.assertEqual(result["concept_matches"][0]["method"], "semantic_token_overlap")
        self.assertEqual(result["missing_concepts"], ["segment analysis"])

    def test_missing_concept_is_reported(self) -> None:
        result = evaluate_concepts("Revenue increased.", ["sample ratio mismatch"])
        self.assertEqual(result["concept_coverage"], 0.0)
        self.assertEqual(result["missing_concepts"], ["sample ratio mismatch"])

    def test_strict_judge_runs_only_when_deterministic_coverage_is_low(self) -> None:
        calls: list[list[str]] = []

        def fake_judge(answer: str, concepts: list[str]) -> list[dict[str, object]]:
            calls.append(concepts)
            return [
                {
                    "concept": "segment analysis",
                    "covered": True,
                    "confidence": 0.91,
                    "rationale": "Answer says to inspect user cohorts.",
                }
            ]

        result = evaluate_concepts(
            "Inspect user cohorts before rollout.",
            ["segment analysis"],
            llm_judge=fake_judge,
        )

        self.assertEqual(calls, [["segment analysis"]])
        self.assertEqual(result["concept_coverage"], 1.0)
        self.assertEqual(result["deterministic_concept_coverage"], 0.0)
        self.assertTrue(result["concept_judge_used"])
        self.assertEqual(result["concept_matches"][0]["method"], "strict_llm_judge")

    def test_strict_judge_does_not_run_when_deterministic_coverage_passes(self) -> None:
        calls: list[list[str]] = []

        def fake_judge(answer: str, concepts: list[str]) -> list[dict[str, object]]:
            calls.append(concepts)
            return []

        result = evaluate_concepts(
            "Run segment analysis before launch.",
            ["segment analysis"],
            llm_judge=fake_judge,
        )

        self.assertEqual(calls, [])
        self.assertFalse(result["concept_judge_used"])

    def test_low_confidence_judge_approval_does_not_count(self) -> None:
        def fake_judge(answer: str, concepts: list[str]) -> list[dict[str, object]]:
            return [
                {
                    "concept": "sample ratio mismatch",
                    "covered": True,
                    "confidence": 0.6,
                    "rationale": "Only loosely related.",
                }
            ]

        result = evaluate_concepts(
            "The result needs more caution.",
            ["sample ratio mismatch"],
            llm_judge=fake_judge,
        )

        self.assertEqual(result["concept_coverage"], 0.0)
        self.assertEqual(result["missing_concepts"], ["sample ratio mismatch"])


if __name__ == "__main__":
    unittest.main()
