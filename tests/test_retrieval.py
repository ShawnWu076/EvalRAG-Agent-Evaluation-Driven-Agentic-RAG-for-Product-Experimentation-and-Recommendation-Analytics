from __future__ import annotations

import unittest

from app.chunking import chunk_markdown


class ChunkingTests(unittest.TestCase):
    def test_markdown_uses_section_level_chunks_when_sections_are_short(self) -> None:
        text = """# A/B Testing Playbook

## Purpose

Randomized experiments estimate causal impact.

## Validity Checks

Check SRM, logging, and eligibility drift before reading lift.
"""
        chunks = chunk_markdown("ab_testing.md", text, chunk_size=80, overlap=10)

        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0].heading, "A/B Testing Playbook > Purpose")
        self.assertEqual(chunks[0].section_path, ["A/B Testing Playbook", "Purpose"])
        self.assertIn("causal impact", chunks[0].text)
        self.assertEqual(chunks[1].heading, "A/B Testing Playbook > Validity Checks")
        self.assertIn("SRM", chunks[1].text)

    def test_long_parent_section_falls_back_to_child_headings(self) -> None:
        text = """# Playbook

## Decision Principles

This introduction is intentionally a bit longer but still short enough to stay in one chunk.

### Primary Metric

Pick one primary metric before reading the result and avoid changing it midstream.

### Guardrails

Keep retention, complaints, and trust metrics stable before launching broadly.
"""
        chunks = chunk_markdown("playbook.md", text, chunk_size=18, overlap=3)
        headings = [chunk.heading for chunk in chunks]

        self.assertIn("Playbook > Decision Principles", headings)
        self.assertIn("Playbook > Decision Principles > Primary Metric", headings)
        self.assertIn("Playbook > Decision Principles > Guardrails", headings)

    def test_headingless_text_falls_back_to_sentence_windows(self) -> None:
        text = (
            "This is a long paragraph without headings. It should still split cleanly into "
            "multiple chunks when the paragraph exceeds the target size. Each sentence should "
            "stay reasonably intact before the code falls back to raw word windows."
        )
        chunks = chunk_markdown("notes.md", text, chunk_size=12, overlap=2)

        self.assertGreaterEqual(len(chunks), 2)
        self.assertTrue(all(chunk.heading == "Notes" for chunk in chunks))


if __name__ == "__main__":
    unittest.main()
