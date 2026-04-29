from __future__ import annotations

import unittest

from app.rag_pipeline import EvalRAGPipeline, infer_decision


class PipelineTests(unittest.TestCase):
    def test_srm_question_routes_to_do_not_trust(self) -> None:
        decision = infer_decision("The experiment has sample ratio mismatch in a 50/50 split.")
        self.assertEqual(decision, "do_not_trust_result")

    def test_retention_drop_routes_to_investigation(self) -> None:
        decision = infer_decision("Revenue increased, but 7-day retention dropped.")
        self.assertEqual(decision, "investigate_further")

    def test_retrieval_finds_srm_source(self) -> None:
        pipeline = EvalRAGPipeline(top_k=3, alpha=0.65)
        record = pipeline.answer(
            "Treatment has 30% more users than control in a planned 50/50 experiment.",
            expected_sources=["sample_ratio_mismatch.md"],
            expected_decision="do_not_trust_result",
            log=False,
        )
        sources = {chunk["source"] for chunk in record["retrieved_chunks"]}
        self.assertIn("sample_ratio_mismatch.md", sources)
        self.assertTrue(record["evaluation"]["decision_correct"])


if __name__ == "__main__":
    unittest.main()

