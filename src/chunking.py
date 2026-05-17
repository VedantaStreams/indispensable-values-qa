"""
chunking.py — Verse-aware and story-aware text chunking for Indispensable Values Q&A.

Strategies:
- Verse-aware: splits on Bhagavad Gītā verse markers (e.g. "7.", "8.", BG 13.7)
- Story-aware: splits on story headings (Story:, Title:, — followed by a name)
- Default: recursive character splitting with overlap
"""

from __future__ import annotations

import re
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Default chunk settings
DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 120

# Verse heading patterns for Bhagavad Gītā transcripts
_VERSE_PATTERN = re.compile(
    r"(?:(?:BG|Bhagavad\s*G[iī]t[aā])\s*(?:Ch(?:apter)?\.?\s*)?\d+\.\d+|"
    r"(?:Verse|śloka|Shloka)\s*\d+[-–]\d+|"
    r"^\s*(?:[Vv]erse\s*)?\d{1,2}\.\s)",
    re.MULTILINE,
)

# Story heading patterns
_STORY_PATTERN = re.compile(
    r"(?:^Story\s*\d*\s*[:—–]|^Title\s*[:—–]|^\*{1,3}Story\b)",
    re.MULTILINE | re.IGNORECASE,
)


def _split_by_pattern(text: str, pattern: re.Pattern, source_meta: dict) -> List[Document]:
    """Split text on pattern boundaries, returning Document objects."""
    positions = [m.start() for m in pattern.finditer(text)]
    if not positions:
        return []

    chunks: List[Document] = []
    for i, start in enumerate(positions):
        end = positions[i + 1] if i + 1 < len(positions) else len(text)
        chunk_text = text[start:end].strip()
        if len(chunk_text) > 50:  # skip trivially short chunks
            chunks.append(Document(page_content=chunk_text, metadata=dict(source_meta)))
    return chunks


def chunk_document(text: str, source_meta: dict, source_type: str = "discourse") -> List[Document]:
    """Chunk a source document into LangChain Documents.

    Args:
        text: Raw document text.
        source_meta: Metadata dict (e.g. {"source": "filename", "type": "discourse"}).
        source_type: One of "discourse", "story", "book", or "transcript".

    Returns:
        List of Document objects ready for embedding.
    """
    # Try verse-aware splitting for discourse/transcript types
    if source_type in ("discourse", "transcript", "book"):
        verse_chunks = _split_by_pattern(text, _VERSE_PATTERN, source_meta)
        if verse_chunks:
            # Further split any over-long verse chunks
            return _refine_chunks(verse_chunks)

    # Try story-aware splitting for story collections
    if source_type == "story":
        story_chunks = _split_by_pattern(text, _STORY_PATTERN, source_meta)
        if story_chunks:
            return _refine_chunks(story_chunks)

    # Fallback: recursive character splitting
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=DEFAULT_CHUNK_SIZE,
        chunk_overlap=DEFAULT_CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    raw_chunks = splitter.split_text(text)
    return [
        Document(page_content=chunk, metadata=dict(source_meta))
        for chunk in raw_chunks
        if chunk.strip()
    ]


def _refine_chunks(chunks: List[Document]) -> List[Document]:
    """Further split any Document whose text exceeds DEFAULT_CHUNK_SIZE * 2."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=DEFAULT_CHUNK_SIZE,
        chunk_overlap=DEFAULT_CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    refined: List[Document] = []
    for doc in chunks:
        if len(doc.page_content) > DEFAULT_CHUNK_SIZE * 2:
            sub_texts = splitter.split_text(doc.page_content)
            for sub in sub_texts:
                if sub.strip():
                    refined.append(Document(page_content=sub, metadata=dict(doc.metadata)))
        else:
            refined.append(doc)
    return refined
