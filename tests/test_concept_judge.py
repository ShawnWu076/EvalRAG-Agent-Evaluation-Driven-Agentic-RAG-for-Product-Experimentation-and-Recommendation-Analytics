from __future__ import annotations

import unittest
from unittest.mock import patch

from app.concept_judge import judge_concepts
from app.llm_generator import LLMGenerationConfig


class ConceptJudgeTests(unittest.TestCase):
    def test_judge_parses_json_and_applies_confidence_gate(self) -> None:
        config = LLMGenerationConfig(
            base_url="http://example.test/v1",
            model="judge-model",
            api_key="test",
            temperature=0,
            max_tokens=200,
            timeout_seconds=1,
            token_parameter="max_tokens",
        )
        raw = (
            '{"results":['
            '{"concept":"segment analysis","covered":true,"confidence":0.93,"rationale":"Answer discusses cohorts."},'
            '{"concept":"sample ratio mismatch","covered":true,"confidence":0.61,"rationale":"Only vaguely cautious."}'
            ']}'
        )
        with patch("app.concept_judge.call_openai_compatible_chat", return_value=raw):
            result = judge_concepts(
                "Inspect cohorts, but be cautious.",
                ["segment analysis", "sample ratio mismatch"],
                config,
                min_confidence=0.8,
            )

        self.assertTrue(result[0]["covered"])
        self.assertFalse(result[1]["covered"])
        self.assertTrue(result[1]["raw_covered"])


if __name__ == "__main__":
    unittest.main()
