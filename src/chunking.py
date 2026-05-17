"""
src/chunking.py — Semantic chunking for spiritual texts.
Preserves verse blocks, analogies, Sanskrit terms, and scriptural references.
"""

import re
import uuid
from typing import Optional


# ── Sanskrit / Scripture Protection ───────────────────────────────────────────
# These patterns should never be split mid-way
PROTECT_PATTERNS = [
    # Sanskrit verses in Devanāgarī
    r"[\u0900-\u097F]{10,}",
    # Transliterated verse lines (contain diacritics)
    r"[a-zA-Zāīūṛṝḷṃḥṅñṭḍṇśṣ̄]{3,}(?:\s+[a-zA-Zāīūṛṝḷṃḥṅñṭḍṇśṣ̄]{2,}){2,}",
    # Gita verse refs like "BG 13.7" or "13.7" or "verse 7"
    r"(?:BG|Bhagavad\s*Gītā?|Gita)\s*\d+\.\d+",
    r"\bverse\s+\d+\b",
]

# Story boundary markers — chunk boundaries should align with these
STORY_BOUNDARY_PATTERNS = [
    r"\n\nSo there was (?:this|a|one)",
    r"\n\nSo (?:let me|today I am going to)",
    r"\n\nNow,?\s+what is the (?:lesson|moral|message|point)",
    r"\n\nSo what is the lesson",
    r"\n\nThe lesson (?:is|to be learnt)",
    r"\n\n\[End of Discourse\]",
]

# Section headers that indicate topic boundaries
SECTION_HEADERS = [
    r"^#+\s+",                          # Markdown headings
    r"^\d+\.\s+[A-Z]",                  # Numbered sections
    r"^[A-Z][A-Z\s]{4,}:?\s*$",        # ALL CAPS headings
    r"^Value\s+\d+",                    # "Value 1", "Value 2"
    r"^(amānitvam|adambhitvam|ahiṃsā|kṣāntiḥ|ārjavam)",  # Sanskrit value names
]


def detect_chunk_type(text: str) -> str:
    """Heuristically detect the type of content in a chunk."""
    text_lower = text.lower()

    # Verse chunk: contains Devanāgarī or dense transliteration
    if re.search(r"[\u0900-\u097F]", text):
        return "verse_chunk"

    # Sanskrit diacritic density
    diacritic_chars = len(re.findall(r"[āīūṛṝḷṃḥṅñṭḍṇśṣ]", text))
    if diacritic_chars > 10:
        return "verse_chunk"

    # Analogy/story chunk: contains story markers
    analogy_markers = [
        "for example", "just as", "like a", "imagine", "story",
        "once upon", "there was", "illustration", "analogy",
        "so there was this", "this incident happened", "let me tell you",
        "so this girl", "so this boy", "so this lady", "so this doctor",
        "so this story", "the lesson", "what is the lesson",
        "moral of", "so what did", "finally what happened",
    ]
    if any(m in text_lower for m in analogy_markers):
        return "analogy_chunk"

    # Value definition chunk: contains definition markers
    def_markers = ["is defined as", "means", "refers to", "the term", "literally means",
                   "the word", "is called", "is known as"]
    if any(m in text_lower for m in def_markers):
        return "value_definition_chunk"

    # Practical application chunk
    practical_markers = ["in practice", "in daily life", "we should", "one must",
                         "the seeker", "for the student", "how to", "practise", "practice"]
    if any(m in text_lower for m in practical_markers):
        return "practical_application_chunk"

    # Explanation chunk (default for substantial paragraphs)
    if len(text) > 300:
        return "explanation_chunk"

    return "general"


def split_preserving_verses(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """
    Split text into chunks while preserving verse blocks and scriptural references.
    Uses paragraph-boundary splitting with target chunk sizes.
    """
    # First split by double newlines (paragraphs)
    paragraphs = re.split(r"\n\s*\n", text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    chunks = []
    current_chunk = []
    current_size = 0

    for para in paragraphs:
        para_size = len(para)

        # If a single paragraph exceeds chunk_size, split it by sentences
        if para_size > chunk_size * 1.5:
            sentences = re.split(r"(?<=[.!?])\s+", para)
            for sent in sentences:
                sent_size = len(sent)
                if current_size + sent_size > chunk_size and current_chunk:
                    # Save current chunk
                    chunks.append("\n\n".join(current_chunk))
                    # Keep overlap: take last portion
                    overlap_text = current_chunk[-1] if current_chunk else ""
                    current_chunk = [overlap_text, sent] if overlap_text else [sent]
                    current_size = len(overlap_text) + sent_size
                else:
                    current_chunk.append(sent)
                    current_size += sent_size
        else:
            if current_size + para_size > chunk_size and current_chunk:
                # Save current chunk
                chunks.append("\n\n".join(current_chunk))
                # Overlap: keep last paragraph for context
                overlap_paras = []
                overlap_chars = 0
                for prev in reversed(current_chunk):
                    if overlap_chars + len(prev) <= overlap:
                        overlap_paras.insert(0, prev)
                        overlap_chars += len(prev)
                    else:
                        break
                current_chunk = overlap_paras + [para]
                current_size = overlap_chars + para_size
            else:
                current_chunk.append(para)
                current_size += para_size

    # Add remaining
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return [c.strip() for c in chunks if c.strip()]


def build_chunk_documents(
    text: str,
    source_metadata: dict,
    page_texts: Optional[list] = None,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[dict]:
    """
    Main chunking function. Takes full source text and returns a list of chunk dicts
    ready for embedding and storage.

    Each chunk dict:
    {
        chunk_id, text, chunk_type, chunk_index,
        source_id, source_title, speaker, scripture,
        chapter, verse_range, source_url,
        page_number, timestamp, language, source_type
    }
    """
    if page_texts:
        # Chunk page-by-page for better page number attribution
        all_chunks = []
        for page_info in page_texts:
            page_num = page_info.get("page", 0)
            page_text = page_info.get("text", "")
            if not page_text.strip():
                continue
            page_chunks = split_preserving_verses(page_text, chunk_size, overlap)
            for chunk_text in page_chunks:
                all_chunks.append((chunk_text, page_num, ""))
    else:
        raw_chunks = split_preserving_verses(text, chunk_size, overlap)
        all_chunks = [(chunk_text, 0, "") for chunk_text in raw_chunks]

    documents = []
    for idx, (chunk_text, page_num, timestamp) in enumerate(all_chunks):
        chunk_type = detect_chunk_type(chunk_text)
        doc = {
            "chunk_id": str(uuid.uuid4()),
            "text": chunk_text,
            "chunk_type": chunk_type,
            "chunk_index": idx,
            "source_id": source_metadata.get("source_id", ""),
            "source_title": source_metadata.get("file_name", source_metadata.get("title", "")),
            "speaker": source_metadata.get("speaker", ""),
            "topic": source_metadata.get("topic", ""),
            "scripture": source_metadata.get("scripture", "Bhagavad Gītā"),
            "chapter": source_metadata.get("chapter", "13"),
            "verse_range": source_metadata.get("verse_range", ""),
            "source_url": source_metadata.get("source_url", ""),
            "page_number": str(page_num) if page_num else "",
            "timestamp": timestamp,
            "language": source_metadata.get("language", "English"),
            "source_type": source_metadata.get("source_type", "document"),
        }
        documents.append(doc)

    return documents


def chunk_transcript_with_timestamps(
    segments: list[dict],
    source_metadata: dict,
    words_per_chunk: int = 300,
) -> list[dict]:
    """
    Chunk a transcript that has timestamp segments.
    Groups segments into ~words_per_chunk word chunks preserving timestamps.
    """
    documents = []
    current_texts = []
    current_words = 0
    chunk_start_time = None
    chunk_idx = 0

    for seg in segments:
        text = seg.get("text", "").strip()
        start = seg.get("start", 0)
        word_count = len(text.split())

        if chunk_start_time is None:
            chunk_start_time = start

        current_texts.append(text)
        current_words += word_count

        if current_words >= words_per_chunk:
            chunk_text = " ".join(current_texts)
            minutes = int(chunk_start_time // 60)
            seconds = int(chunk_start_time % 60)
            timestamp_str = f"{minutes:02d}:{seconds:02d}"

            chunk_type = detect_chunk_type(chunk_text)
            doc = {
                "chunk_id": str(uuid.uuid4()),
                "text": chunk_text,
                "chunk_type": chunk_type,
                "chunk_index": chunk_idx,
                "source_id": source_metadata.get("source_id", ""),
                "source_title": source_metadata.get("title", ""),
                "speaker": source_metadata.get("speaker", ""),
                "topic": source_metadata.get("topic", ""),
                "scripture": source_metadata.get("scripture", "Bhagavad Gītā"),
                "chapter": source_metadata.get("chapter", "13"),
                "verse_range": source_metadata.get("verse_range", ""),
                "source_url": source_metadata.get("source_url", ""),
                "page_number": "",
                "timestamp": timestamp_str,
                "language": source_metadata.get("language", "English"),
                "source_type": "youtube_video",
            }
            documents.append(doc)

            # Reset with overlap
            overlap_segs = segments[max(0, len(segments) - 2):]
            current_texts = [s.get("text", "") for s in overlap_segs]
            current_words = sum(len(t.split()) for t in current_texts)
            chunk_start_time = None
            chunk_idx += 1

    # Final chunk
    if current_texts:
        chunk_text = " ".join(current_texts)
        if chunk_text.strip():
            minutes = int((chunk_start_time or 0) // 60)
            seconds = int((chunk_start_time or 0) % 60)
            timestamp_str = f"{minutes:02d}:{seconds:02d}"
            documents.append({
                "chunk_id": str(uuid.uuid4()),
                "text": chunk_text,
                "chunk_type": detect_chunk_type(chunk_text),
                "chunk_index": chunk_idx,
                "source_id": source_metadata.get("source_id", ""),
                "source_title": source_metadata.get("title", ""),
                "speaker": source_metadata.get("speaker", ""),
                "topic": source_metadata.get("topic", ""),
                "scripture": source_metadata.get("scripture", "Bhagavad Gītā"),
                "chapter": source_metadata.get("chapter", "13"),
                "verse_range": source_metadata.get("verse_range", ""),
                "source_url": source_metadata.get("source_url", ""),
                "page_number": "",
                "timestamp": timestamp_str,
                "language": source_metadata.get("language", "English"),
                "source_type": "youtube_video",
            })

    return documents
