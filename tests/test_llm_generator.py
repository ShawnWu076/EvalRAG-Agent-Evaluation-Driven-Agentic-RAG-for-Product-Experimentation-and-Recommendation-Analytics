from __future__ import annotations

import unittest

from app.llm_generator import build_llm_messages, strip_thinking_blocks


class LLMGeneratorTests(unittest.TestCase):
    def test_strip_thinking_blocks(self) -> None:
        text = "<think>hidden reasoning</think>## Short Answer\nUse the memo."
        self.assertEqual(strip_thinking_blocks(text), "## Short Answer\nUse the memo.")

    def test_build_messages_includes_decision_and_sources(self) -> None:
        messages = build_llm_messages(
            "Revenue increased but retention dropped. Should we launch?",
            [
                {
                    "chunk_id": "guardrail_metrics_001",
                    "source": "guardrail_metrics.md",
                    "heading": "Guardrail Metrics",
                    "score": 0.91,
                    "text": "Retention is a guardrail metric.",
                }
            ],
            "investigate_further",
        )
        prompt = messages[-1]["content"]
        self.assertIn("investigate_further", prompt)
        self.assertIn("guardrail_metrics.md", prompt)
        self.assertIn("Retention is a guardrail metric", prompt)


if __name__ == "__main__":
    unittest.main()
