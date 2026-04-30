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


if __name__ == "__main__":
    unittest.main()
