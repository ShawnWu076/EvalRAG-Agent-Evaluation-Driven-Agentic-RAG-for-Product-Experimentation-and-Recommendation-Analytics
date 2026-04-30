from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from app.llm_generator import LLMGenerationConfig, build_llm_messages, call_openai_compatible_chat, strip_thinking_blocks


class _FakeResponse:
    def __init__(self, body: dict) -> None:
        self.body = body

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.body).encode("utf-8")


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

    def test_chat_request_uses_configured_token_parameter(self) -> None:
        captured_payload: dict = {}

        def fake_urlopen(request, timeout):
            nonlocal captured_payload
            captured_payload = json.loads(request.data.decode("utf-8"))
            self.assertEqual(timeout, 30)
            return _FakeResponse({"choices": [{"message": {"content": "## Short Answer\nOK"}}]})

        config = LLMGenerationConfig(
            base_url="https://api.openai.com/v1",
            model="gpt-test",
            api_key="test-key",
            temperature=0.2,
            max_tokens=123,
            timeout_seconds=30,
            token_parameter="max_completion_tokens",
        )
        with patch("urllib.request.urlopen", fake_urlopen):
            call_openai_compatible_chat([{"role": "user", "content": "hello"}], config)

        self.assertNotIn("max_tokens", captured_payload)
        self.assertEqual(captured_payload["max_completion_tokens"], 123)


if __name__ == "__main__":
    unittest.main()
