from __future__ import annotations

import unittest
from unittest.mock import patch

from app.llm_generator import LLMGenerationError
from app.rag_pipeline import EvalRAGPipeline, evaluate_trace, extract_decision


INVESTIGATE_ANSWER = """## Short Answer
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

LAUNCH_ANSWER = """## Short Answer
Launch looks reasonable.

## Decision Recommendation
`launch`

## Reasoning
Revenue improved.

## Metrics to Check
- revenue

## Suggested Next Steps
1. Monitor launch.

## Risks / Caveats
- Evidence may be incomplete.

## Retrieved Sources
- launch_decision.md
"""


class PipelineTests(unittest.TestCase):
    def test_extract_decision_from_decision_section(self) -> None:
        self.assertEqual(extract_decision(INVESTIGATE_ANSWER), "investigate_further")

    def test_strict_source_metrics_track_missing_and_top1(self) -> None:
        evaluation = evaluate_trace(
            INVESTIGATE_ANSWER,
            ["guardrail_metrics.md", "unrelated.md"],
            "investigate_further",
            expected_sources=["guardrail_metrics.md", "launch_decision.md"],
            expected_concepts=["guardrail metric", "segment analysis"],
            expected_decision="investigate_further",
            llm_decision="investigate_further",
        )
        self.assertTrue(evaluation["source_hit"])
        self.assertEqual(evaluation["source_match_rate"], 0.5)
        self.assertFalse(evaluation["all_expected_sources_found"])
        self.assertTrue(evaluation["top1_source_match"])
        self.assertEqual(evaluation["source_precision_at_k"], 0.5)
        self.assertEqual(evaluation["missing_sources"], ["launch_decision.md"])
        self.assertTrue(evaluation["decision_correct"])
        self.assertTrue(evaluation["llm_decision_correct"])

    def test_pipeline_records_llm_policy_and_final_decisions(self) -> None:
        pipeline = EvalRAGPipeline(top_k=3, alpha=0.65)
        with patch("app.rag_pipeline.generate_llm_answer", return_value=INVESTIGATE_ANSWER):
            record = pipeline.answer(
                "Revenue increased, but 7-day retention dropped.",
                expected_sources=["guardrail_metrics.md"],
                expected_decision="investigate_further",
                log=False,
            )
        self.assertEqual(record["llm_decision"], "investigate_further")
        self.assertEqual(record["policy_decision"], "investigate_further")
        self.assertEqual(record["final_decision"], "investigate_further")
        self.assertEqual(record["decision"], "investigate_further")
        self.assertTrue(record["evaluation"]["decision_correct"])
        self.assertTrue(record["evaluation"]["llm_decision_correct"])
        self.assertEqual(record["model"], "gpt-5.4-mini")

    def test_policy_override_updates_visible_answer_and_final_decision(self) -> None:
        pipeline = EvalRAGPipeline(top_k=3, alpha=0.65)
        with patch("app.rag_pipeline.generate_llm_answer", return_value=LAUNCH_ANSWER):
            record = pipeline.answer(
                "Revenue increased, but 7-day retention dropped.",
                expected_decision="investigate_further",
                log=False,
            )
        self.assertEqual(record["llm_decision"], "launch")
        self.assertEqual(record["policy_decision"], "investigate_further")
        self.assertEqual(record["final_decision"], "investigate_further")
        self.assertTrue(record["policy_validation"]["policy_override"])
        self.assertTrue(record["evaluation"]["decision_correct"])
        self.assertFalse(record["evaluation"]["llm_decision_correct"])
        self.assertIn("## Policy Validation", record["answer"])
        self.assertIn("`investigate_further`", record["answer"])

    def test_pipeline_falls_back_to_local_llm_when_primary_fails(self) -> None:
        pipeline = EvalRAGPipeline(top_k=3, alpha=0.65)
        with patch(
            "app.rag_pipeline.generate_llm_answer",
            side_effect=[LLMGenerationError("primary down"), INVESTIGATE_ANSWER],
        ):
            record = pipeline.answer("Revenue increased, but retention dropped.", log=False)
        self.assertEqual(record["generator_backend"], "local_llm_fallback")
        self.assertEqual(record["model"], "qwen3:8b")
        self.assertIn("primary down", record["generator_error"])


if __name__ == "__main__":
    unittest.main()
