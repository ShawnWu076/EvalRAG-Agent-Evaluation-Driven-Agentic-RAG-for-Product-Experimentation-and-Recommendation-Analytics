from __future__ import annotations

import unittest
from unittest.mock import patch

from app.llm_generator import LLMGenerationError
from app.rag_pipeline import EvalRAGPipeline, evaluate_trace, extract_decision


ANSWER = """## Short Answer
Do not fully launch yet.

## Decision Recommendation
`investigate_further`

## Reasoning
Retention is a guardrail metric and should be investigated.

## Metrics to Check
- retention

## Suggested Next Steps
1. Run segment analysis.

## Risks / Caveats
- Evidence may be incomplete.

## Retrieved Sources
- guardrail_metrics.md
"""


class PipelineTests(unittest.TestCase):
    def test_extract_decision_from_decision_section(self) -> None:
        self.assertEqual(extract_decision(ANSWER), "investigate_further")

    def test_strict_source_metrics_track_missing_and_top1(self) -> None:
        evaluation = evaluate_trace(
            ANSWER,
            ["guardrail_metrics.md", "unrelated.md"],
            "investigate_further",
            expected_sources=["guardrail_metrics.md", "launch_decision.md"],
            expected_concepts=["guardrail metric", "segment analysis"],
            expected_decision="investigate_further",
        )
        self.assertTrue(evaluation["source_hit"])
        self.assertEqual(evaluation["source_match_rate"], 0.5)
        self.assertFalse(evaluation["all_expected_sources_found"])
        self.assertTrue(evaluation["top1_source_match"])
        self.assertEqual(evaluation["source_precision_at_k"], 0.5)
        self.assertEqual(evaluation["missing_sources"], ["launch_decision.md"])
        self.assertTrue(evaluation["decision_correct"])

    def test_pipeline_uses_llm_decision_for_evaluation(self) -> None:
        pipeline = EvalRAGPipeline(top_k=3, alpha=0.65)
        with patch("app.rag_pipeline.generate_llm_answer", return_value=ANSWER):
            record = pipeline.answer(
                "Revenue increased, but 7-day retention dropped.",
                expected_sources=["guardrail_metrics.md"],
                expected_decision="investigate_further",
                log=False,
            )
        self.assertEqual(record["decision"], "investigate_further")
        self.assertTrue(record["evaluation"]["decision_correct"])
        self.assertEqual(record["model"], "gpt-5.4-mini")

    def test_pipeline_falls_back_to_local_llm_when_primary_fails(self) -> None:
        pipeline = EvalRAGPipeline(top_k=3, alpha=0.65)
        with patch(
            "app.rag_pipeline.generate_llm_answer",
            side_effect=[LLMGenerationError("primary down"), ANSWER],
        ):
            record = pipeline.answer("Revenue increased, but retention dropped.", log=False)
        self.assertEqual(record["generator_backend"], "local_llm_fallback")
        self.assertEqual(record["model"], "qwen3:8b")
        self.assertIn("primary down", record["generator_error"])


if __name__ == "__main__":
    unittest.main()
