"""
ingestion.py — PDF/DOCX/TXT ingestion with discourse/story text cleaners.

Supports:
- PDF via pypdf
- DOCX via python-docx
- TXT plain text
- Basic discourse cleaning (removes timestamps, speaker labels, filler words)
- Story cleaning (normalises story heading markers)
"""

from __future__ import annotations

import io
import os
import re
from typing import List, Tuple

from langchain_core.documents import Document

from src.chunking import chunk_document

# ---------------------------------------------------------------------------
# Text extraction helpers
# ---------------------------------------------------------------------------

def _extract_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file."""
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(file_bytes))
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return "\n\n".join(pages)


def _extract_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX file."""
    import docx

    doc = docx.Document(io.BytesIO(file_bytes))
    paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n\n".join(paragraphs)


def _extract_txt(file_bytes: bytes) -> str:
    """Decode plain text, trying UTF-8 then latin-1."""
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return file_bytes.decode("latin-1")


# ---------------------------------------------------------------------------
# Text cleaners
# ---------------------------------------------------------------------------

# Timestamp patterns like [00:12:34] or (00:12:34)
_TIMESTAMP_RE = re.compile(r"[\[\(]\d{1,2}:\d{2}(?::\d{2})?[\]\)]")

# Speaker label patterns like "Swamiji:" or "Devotee:"
_SPEAKER_RE = re.compile(r"^[A-Z][A-Za-z ]{1,30}:\s*", re.MULTILINE)

# Filler / transcript artefacts
_FILLER_RE = re.compile(r"\b(um|uh|hmm|er|ah)\b", re.IGNORECASE)


def _clean_discourse(text: str) -> str:
    """Clean a discourse transcript: remove timestamps, speaker labels, fillers."""
    text = _TIMESTAMP_RE.sub("", text)
    text = _SPEAKER_RE.sub("", text)
    text = _FILLER_RE.sub("", text)
    # Collapse excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def _clean_story(text: str) -> str:
    """Normalise story heading markers to a consistent format."""
    # Standardise "Story N:" or "Story N —" to "Story N:"
    text = re.sub(r"^(Story\s*\d*)\s*[—–-]+", r"\1:", text, flags=re.MULTILINE)
    # Remove duplicate blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def ingest_file(
    file_bytes: bytes,
    filename: str,
    source_type: str = "discourse",
) -> Tuple[List[Document], int]:
    """Ingest a single file and return (documents, chunk_count).

    Args:
        file_bytes: Raw file content.
        filename: Original filename (used to detect extension and set metadata).
        source_type: "discourse", "story", "book", or "transcript".

    Returns:
        A tuple of (list_of_Documents, number_of_chunks).
    """
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        raw_text = _extract_pdf(file_bytes)
    elif ext in (".docx", ".doc"):
        raw_text = _extract_docx(file_bytes)
    elif ext == ".txt":
        raw_text = _extract_txt(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    # Apply appropriate cleaner
    if source_type in ("discourse", "transcript"):
        cleaned_text = _clean_discourse(raw_text)
    elif source_type == "story":
        cleaned_text = _clean_story(raw_text)
    else:
        cleaned_text = raw_text.strip()

    source_meta = {
        "source": filename,
        "type": source_type,
    }

    documents = chunk_document(cleaned_text, source_meta, source_type=source_type)
    return documents, len(documents)
