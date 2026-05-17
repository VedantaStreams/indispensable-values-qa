"""
tests/test_core.py — Unit tests for core src modules.

Tests can be run with:  pytest tests/
"""

import sys
import types
import unittest
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Bootstrap: stub out streamlit before any src import
# ---------------------------------------------------------------------------
_st = MagicMock()
_st.secrets = {"OPENAI_API_KEY": "sk-test", "ADMIN_PASSWORD": "test-pw"}
sys.modules.setdefault("streamlit", _st)


# ---------------------------------------------------------------------------
# prompts
# ---------------------------------------------------------------------------
class TestPrompts(unittest.TestCase):
    def test_system_prompt_contains_key_instruction(self):
        from src.prompts import SYSTEM_PROMPT
        self.assertIn("NEVER fabricate", SYSTEM_PROMPT)

    def test_rag_prompt_template_has_placeholders(self):
        from src.prompts import RAG_PROMPT_TEMPLATE
        self.assertIn("{context}", RAG_PROMPT_TEMPLATE)
        self.assertIn("{question}", RAG_PROMPT_TEMPLATE)

    def test_no_results_response_is_string(self):
        from src.prompts import NO_RESULTS_RESPONSE
        self.assertIsInstance(NO_RESULTS_RESPONSE, str)
        self.assertGreater(len(NO_RESULTS_RESPONSE), 10)


# ---------------------------------------------------------------------------
# guardrails
# ---------------------------------------------------------------------------
class TestGuardrails(unittest.TestCase):
    def setUp(self):
        from src.guardrails import is_on_topic, is_reverent_response
        self.is_on_topic = is_on_topic
        self.is_reverent = is_reverent_response

    def test_sanskrit_value_name_is_on_topic(self):
        self.assertTrue(self.is_on_topic("What is amānitvam?"))
        self.assertTrue(self.is_on_topic("Explain kṣāntiḥ"))
        self.assertTrue(self.is_on_topic("Tell me about ahimsa"))

    def test_gita_context_is_on_topic(self):
        self.assertTrue(self.is_on_topic("What does Swamiji teach in Bhagavad Gita Chapter 13?"))

    def test_clearly_off_topic_long_question(self):
        self.assertFalse(self.is_on_topic(
            "What is the best way to cook pasta with tomato sauce and parmesan cheese?"
        ))

    def test_short_question_passes_by_default(self):
        self.assertTrue(self.is_on_topic("hello"))
        self.assertTrue(self.is_on_topic("What is this?"))

    def test_reverent_response_passes(self):
        response = "According to the retrieved passages, amānitvam refers to humility."
        self.assertTrue(self.is_reverent(response))

    def test_fabricated_quote_fails_reverence(self):
        response = 'Swamiji said that "humility is the greatest virtue"'
        self.assertFalse(self.is_reverent(response))


# ---------------------------------------------------------------------------
# chunking
# ---------------------------------------------------------------------------
class TestChunking(unittest.TestCase):
    def setUp(self):
        from src.chunking import chunk_document
        self.chunk_document = chunk_document

    def test_basic_chunking_returns_documents(self):
        long_text = "This is a test sentence about Vedānta. " * 100
        docs = self.chunk_document(long_text, {"source": "test.txt", "type": "discourse"})
        self.assertGreater(len(docs), 0)
        for doc in docs:
            self.assertIsInstance(doc.page_content, str)
            self.assertIn("source", doc.metadata)

    def test_verse_aware_chunking(self):
        verse_text = (
            "BG 13.7 amānitvam adambhitvam. This value requires humility of the highest order.\n\n"
            "BG 13.8 ahiṃsā kṣāntiḥ. Non-violence and forbearance are twin virtues.\n\n"
            "BG 13.9 ārjavam. Straightforwardness means inner and outer alignment.\n\n"
        )
        docs = self.chunk_document(verse_text, {"source": "bg13.txt"}, source_type="discourse")
        self.assertGreater(len(docs), 0)

    def test_story_aware_chunking(self):
        story_text = (
            "Story 1: The Humble King\nOnce there was a king who bowed to everyone.\n\n"
            "Story 2: The Forbearing Sage\nA sage who never reacted to insults became famous.\n\n"
        )
        docs = self.chunk_document(story_text, {"source": "stories.txt"}, source_type="story")
        self.assertGreater(len(docs), 0)

    def test_metadata_preserved(self):
        text = "Short text " * 10
        meta = {"source": "my_file.pdf", "type": "book"}
        docs = self.chunk_document(text, meta, source_type="book")
        for doc in docs:
            self.assertEqual(doc.metadata["source"], "my_file.pdf")


# ---------------------------------------------------------------------------
# ingestion text cleaners
# ---------------------------------------------------------------------------
class TestIngestionCleaners(unittest.TestCase):
    def setUp(self):
        from src.ingestion import _clean_discourse, _clean_story, _extract_txt
        self.clean_discourse = _clean_discourse
        self.clean_story = _clean_story
        self.extract_txt = _extract_txt

    def test_discourse_removes_timestamps(self):
        text = "[00:01:23] Swamiji: The value of humility."
        cleaned = self.clean_discourse(text)
        self.assertNotIn("[00:01:23]", cleaned)

    def test_discourse_removes_fillers(self):
        text = "Um, this is, uh, very important."
        cleaned = self.clean_discourse(text)
        self.assertNotIn("Um", cleaned)
        self.assertNotIn("uh", cleaned)

    def test_story_normalises_headings(self):
        text = "Story 1 — The Humble King\nContent here."
        cleaned = self.clean_story(text)
        self.assertIn("Story 1:", cleaned)
        self.assertNotIn("—", cleaned)

    def test_txt_extraction_utf8(self):
        content = "Hello Vedānta World"
        result = self.extract_txt(content.encode("utf-8"))
        self.assertEqual(result, content)

    def test_txt_extraction_latin1_fallback(self):
        content = b"Hello \xe9 World"  # latin-1 byte
        result = self.extract_txt(content)
        self.assertIn("Hello", result)


# ---------------------------------------------------------------------------
# transcription URL parsing
# ---------------------------------------------------------------------------
class TestTranscription(unittest.TestCase):
    def setUp(self):
        from src.transcription import _extract_video_id
        self.extract_id = _extract_video_id

    def test_full_youtube_url(self):
        vid = self.extract_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.assertEqual(vid, "dQw4w9WgXcQ")

    def test_short_youtu_be_url(self):
        vid = self.extract_id("https://youtu.be/dQw4w9WgXcQ")
        self.assertEqual(vid, "dQw4w9WgXcQ")

    def test_bare_video_id(self):
        vid = self.extract_id("dQw4w9WgXcQ")
        self.assertEqual(vid, "dQw4w9WgXcQ")

    def test_embed_url(self):
        vid = self.extract_id("https://www.youtube.com/embed/dQw4w9WgXcQ")
        self.assertEqual(vid, "dQw4w9WgXcQ")

    def test_invalid_url_returns_none(self):
        vid = self.extract_id("not-a-url")
        self.assertIsNone(vid)


# ---------------------------------------------------------------------------
# visitor_counter (file-based)
# ---------------------------------------------------------------------------
class TestVisitorCounter(unittest.TestCase):
    def test_get_count_returns_int(self):
        from src.visitor_counter import get_count
        count = get_count()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
