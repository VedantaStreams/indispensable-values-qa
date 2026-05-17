"""
src/ingestion.py — Text extraction from PDFs, DOCX, and TXT files.
Handles uploaded documents with metadata tracking.
"""

import json
import uuid
import hashlib
from pathlib import Path
from typing import Optional


# ── PDF Extraction ─────────────────────────────────────────────────────────────
def extract_text_from_pdf(file_path: Path) -> tuple[str, dict]:
    """
    Extract text from a PDF file.
    Returns (full_text, {page_texts: list, page_count: int})
    Tries pdfplumber first (better formatting), falls back to PyPDF2.
    """
    page_texts = []
    try:
        import pdfplumber
        with pdfplumber.open(str(file_path)) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                page_texts.append({"page": i + 1, "text": text})
        full_text = "\n\n".join(p["text"] for p in page_texts if p["text"])
        return full_text, {"page_texts": page_texts, "page_count": len(page_texts), "method": "pdfplumber"}

    except ImportError:
        pass

    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(str(file_path))
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            page_texts.append({"page": i + 1, "text": text})
        full_text = "\n\n".join(p["text"] for p in page_texts if p["text"])
        return full_text, {"page_texts": page_texts, "page_count": len(page_texts), "method": "PyPDF2"}

    except ImportError:
        raise ImportError("Install pdfplumber or PyPDF2: pip install pdfplumber")


# ── DOCX Extraction ────────────────────────────────────────────────────────────
def extract_text_from_docx(file_path: Path) -> str:
    """Extract text from a DOCX file, preserving paragraph structure."""
    try:
        import docx
        doc = docx.Document(str(file_path))
        paragraphs = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                paragraphs.append(text)
        return "\n\n".join(paragraphs)
    except ImportError:
        raise ImportError("Install python-docx: pip install python-docx")


# ── TXT Extraction ─────────────────────────────────────────────────────────────
def extract_text_from_txt(file_path: Path) -> str:
    """Read plain text file with encoding detection."""
    encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
    for enc in encodings:
        try:
            return file_path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return file_path.read_text(encoding="utf-8", errors="replace")


# ── Universal Dispatcher ───────────────────────────────────────────────────────
def extract_text(file_path: Path) -> tuple[str, dict]:
    """
    Extract text from any supported file format.
    Returns (text, extra_metadata).
    """
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        return extract_text_from_pdf(file_path)
    elif suffix == ".docx":
        text = extract_text_from_docx(file_path)
        return text, {}
    elif suffix in (".txt", ".md"):
        text = extract_text_from_txt(file_path)
        return text, {}
    else:
        raise ValueError(f"Unsupported file type: {suffix}")


# ── Metadata Management ────────────────────────────────────────────────────────
def compute_file_hash(file_path: Path) -> str:
    """SHA-256 hash of file for deduplication."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()[:16]


def build_source_record(
    file_path: Path,
    metadata: dict,
    extra: dict = None,
    source_type: str = "document",
) -> dict:
    """
    Build a standardized source record dict for JSON storage.

    Keys:
        source_id, file_name, file_hash, source_type,
        speaker, topic, scripture, chapter, verse_range,
        language, date_session, source_url, page_count,
        processed, created_at
    """
    import datetime

    file_hash = compute_file_hash(file_path) if file_path.exists() else ""
    return {
        "source_id": str(uuid.uuid4()),
        "file_name": file_path.name,
        "file_path": str(file_path),
        "file_hash": file_hash,
        "source_type": source_type,
        "speaker": metadata.get("speaker", "Swamiji"),
        "topic": metadata.get("topic", "Indispensable Values"),
        "scripture": metadata.get("scripture", "Bhagavad Gītā"),
        "chapter": metadata.get("chapter", "13"),
        "verse_range": metadata.get("verse_range", ""),
        "language": metadata.get("language", "English"),
        "date_session": metadata.get("date_session", ""),
        "source_url": metadata.get("source_url", ""),
        "page_count": (extra or {}).get("page_count", 0),
        "processed": False,
        "chunk_count": 0,
        "created_at": datetime.datetime.now().isoformat(),
    }


def save_source_registry(records: list[dict], registry_path: Path):
    """Save source registry JSON file."""
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def load_source_registry(registry_path: Path) -> list[dict]:
    """Load source registry from JSON."""
    if not registry_path.exists():
        return []
    with open(registry_path, "r", encoding="utf-8") as f:
        return json.load(f)


def mark_source_processed(source_id: str, chunk_count: int, registry_path: Path):
    """Update source registry to mark a source as processed."""
    records = load_source_registry(registry_path)
    for rec in records:
        if rec["source_id"] == source_id:
            rec["processed"] = True
            rec["chunk_count"] = chunk_count
            break
    save_source_registry(records, registry_path)


def clean_discourse_transcript(text: str) -> str:
    """
    Clean the specific 'Discourse Summary — Transcript' PDF format
    produced by the Wisdom Distiller / audio summarizer app.

    Handles:
    - Strips repetitive opening "Aum Aum Aum..." chant lines
    - Strips devotional closing songs / Devanagari chant blocks
    - Strips the header metadata block (we extract it separately)
    - Re-paragraphs flowing speech text at sentence boundaries
    - Preserves Sanskrit terms and scripture references
    """
    import re

    # ── Strip header block ─────────────────────────────────────────────────
    # Remove everything up to and including the KEY TERMS line
    text = re.sub(
        r"Discourse Summary.*?KEY TERMS.*?\n",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # ── Strip repetitive Aum opening ───────────────────────────────────────
    # Lines that are mostly "Aum" repeated
    text = re.sub(r"(Aum\s+){5,}", "\n", text)
    text = re.sub(r"^Aum\s+Aum.*\n", "", text, flags=re.MULTILINE)

    # ── Strip opening Sanskrit invocation chant (before main content) ──────
    # Chant lines before substantive content (Sahanavavatu etc.)
    text = re.sub(
        r"(Sahanavavatu|Sahanobhunaktu|Shri Rama Jaya Rama|Jaya Jaya Rama).*?Hari Om\s*",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # ── Strip closing devotional songs ─────────────────────────────────────
    # After "Om Shanti Shanti Shanti" the discourse ends; strip everything after
    text = re.sub(
        r"Om Shanti Shanti Shanti.*$",
        "\n[End of Discourse]",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # ── Strip Devanagari / garbled Unicode chant blocks ───────────────────
    text = re.sub(r"[\u0900-\u097F\u1CD0-\u1CFF]{3,}", "", text)

    # ── Re-paragraph: insert line breaks at sentence endings ──────────────
    # This format has no paragraph breaks — add them at sentence boundaries
    # Insert break after ". " followed by capital letter (new sentence/thought)
    text = re.sub(r"\.\s+([A-Z])", r".\n\n\1", text)

    # Also break at natural discourse transitions
    transitions = [
        r"(So\s+)(what|now|therefore|here|we|this|that|let|you|it)",
        r"(Now\s+)(what|let us|we|the|this|that|suppose|look)",
        r"(Look at\s+)",
        r"(In the same way\s+)",
        r"(What about\s+)",
        r"(What is\s+the\s+)",
        r"(The question is\s+)",
    ]
    for pattern in transitions:
        text = re.sub(pattern, r"\n\n\1\2" if r"\2" in pattern else r"\n\n\1", text)

    # ── Clean up whitespace ────────────────────────────────────────────────
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    text = text.strip()

    return text


def extract_discourse_metadata(text: str) -> dict:
    """
    Extract metadata from the 'Discourse Summary — Transcript' header block.
    Returns dict with speaker, topic, scripture, language, verses, key_terms.
    """
    import re
    meta = {}

    speaker_match = re.search(r"SPEAKER\s*\n([^\n]+)", text)
    if speaker_match:
        meta["speaker"] = speaker_match.group(1).strip()

    topic_match = re.search(r"TOPIC\s*\n([^\n]+)", text)
    if topic_match:
        meta["topic"] = topic_match.group(1).strip()

    scripture_match = re.search(r"SCRIPTURE\s*\n([^\n]+)", text)
    if scripture_match:
        meta["scripture"] = scripture_match.group(1).strip()

    language_match = re.search(r"LANGUAGE\s*\n([^\n]+)", text)
    if language_match:
        lang = language_match.group(1).strip()
        meta["language"] = lang.replace("(default)", "").strip()

    verses_match = re.search(r"VERSES REFERENCED\s+([^\n]+)", text)
    if verses_match:
        meta["verse_range"] = verses_match.group(1).strip()

    key_terms_match = re.search(r"KEY TERMS\s+([^\n]+(?:\n[^\n]+)*?)(?=\n\n)", text)
    if key_terms_match:
        meta["key_terms"] = key_terms_match.group(1).strip()

    return meta


def clean_story_transcript(text: str) -> str:
    """
    Clean the 'Value Based Stories for All' summer camp transcript format.

    Different from discourse transcripts:
    - No repetitive Aum opening (starts with "Hari Om")
    - No long chant ending (ends with "Hari Om" / "Hari Om children")
    - Has interactive classroom prompts to strip
    - Stories must remain intact — no mid-story splitting

    Strips:
    - Header metadata block
    - Interactive classroom prompts ("fingers", "quiz", "note down", etc.)
    - Audience Q&A interjections
    - Closing "Hari Om" signoff
    Preserves:
    - Full story narratives
    - Sanskrit verses and terms
    - Swamiji's explanations of values
    - Moral lessons at story end
    """
    import re

    # ── Strip header block ─────────────────────────────────────────────────────
    text = re.sub(
        r"Discourse Summary.*?KEY TERMS.*?\n",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # ── Strip interactive classroom prompts ────────────────────────────────────
    classroom_patterns = [
        # "show me with fingers" / "fingers, fingers" variants
        r"[Ss]how\s+(?:me\s+)?(?:with\s+)?(?:your\s+)?fingers?[,.]?\s*",
        r"[Ff]ingers?,?\s+fingers?,?\s+fingers?\.?\s*",
        r"[Nn]ow\s+you\s+(?:will\s+)?(?:have\s+to\s+)?(?:show|indicate)\s+(?:with\s+)?(?:your\s+)?fingers?\s*",
        # Notebook / quiz instructions
        r"[Ww]rite\s+(?:it\s+)?down\s+(?:in\s+)?(?:your\s+)?(?:notebook|notes?)\.?\s*",
        r"[Nn]ote\s+(?:it\s+)?down\s*[.,]?\s*",
        r"[Qq]uiz\s+(?:will\s+come|tomorrow|questions?)[^.]*\.",
        r"[Qq]uestions?\s+(?:are\s+going\s+to\s+come|will\s+come)[^.]*\.",
        r"[Yy]ou\s+will\s+have\s+to\s+(?:answer|submit)[^.]*\.",
        r"[Ii]\s+will\s+also\s+see\s+the\s+answers[^.]*\.",
        r"[Rr]emember\s+every\s+little\s+(?:point|detail)[^.]*\.",
        r"[Yy]ou\s+(?:have\s+this\s+)?notebook\s+with\s+you[^.]*\.",
        r"[Bb]y\s+the\s+way,?\s+I\s+hope\s+you\s+are\s+noting[^.]*\.",
        r"[Ss]o\s+you\s+will\s+have\s+to\s+indicate\s+with[^.]*\.",
        # Audience response interjections
        r"\b[Vv]ery\s+good\.\s*",
        r"[Ss]ome\s+of\s+them\s+(?:got\s+it\s+right|remember)[^.]*\.",
        r"[Hh]ow\s+many\s+of\s+you\s+have\s+heard[^?]*\?\s*(?:[Hh]ands?\s+raised\.)?\s*(?:Yes\.)?\s*",
        r"(?:Yes\.|Very\s+good\.|Good\.|Ready\?|Thank\s+you\s+very\s+much\.)\s*",
        # Spelling out words for children
        r"[Tt]he\s+spelling\s+is\s+[A-Z][-A-Z\s]+\.\s*",
        r"O-M-N-[A-Z-\s]+\.\s*",
    ]
    for pattern in classroom_patterns:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE)

    # ── Strip closing Hari Om signoff ──────────────────────────────────────────
    text = re.sub(
        r"Hari\s+Om(?:\s+(?:all\s+of\s+you|children|Thank\s+you\s+children))?\.?\s*$",
        "\n[End of Discourse]",
        text,
        flags=re.IGNORECASE | re.MULTILINE,
    )

    # ── Strip Devanāgarī / garbled Unicode ────────────────────────────────────
    text = re.sub(r"[\u0900-\u097F\u1CD0-\u1CFF]{3,}", "", text)

    # ── Re-paragraph at story/lesson boundaries ────────────────────────────────
    story_transitions = [
        r"(So\s+)(what\s+is\s+the\s+lesson)",
        r"(So\s+)(what\s+(?:is\s+the\s+)?(?:moral|message|point|lesson))",
        r"(Now\s+)(continuing(?:\s+with\s+our\s+story)?)",
        r"(Now\s+)(the\s+question\s+is)",
        r"(Right\.\s+)(So\s+)",
        r"(\.\s+)(So\s+today\s+we\s+(?:will|are\s+going\s+to))",
        r"(\.\s+)(Now\s+a\s+(?:very\s+)?(?:nice|important|interesting))",
    ]
    for pattern in story_transitions:
        text = re.sub(pattern, r"\1\n\n\2", text)

    # ── Add story title markers where value is clear ───────────────────────────
    # (This helps the chunker detect story boundaries)
    story_markers = [
        r"(So\s+(?:there\s+was\s+this|let\s+me\s+start\s+with|today\s+we\s+(?:will\s+see|are\s+going\s+to\s+see)))",
    ]
    for pattern in story_markers:
        text = re.sub(pattern, r"\n\n\1", text)

    # ── Clean up whitespace ────────────────────────────────────────────────────
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def detect_story_format(text: str) -> bool:
    """Return True if this PDF is a 'Value Based Stories for All' transcript."""
    indicators = [
        "Value Based Stories for All" in text,
        "Value Based Stories" in text,
        "summer camp" in text.lower(),
        # Story format starts with "Hari Om" not "Aum Aum Aum"
        bool(__import__("re").search(r"^Hari\s+Om", text.strip()[:200])),
    ]
    return any(indicators)


def save_raw_text(source_id: str, text: str, raw_dir: Path):
    """Save raw extracted text for a source."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    out_file = raw_dir / f"{source_id}.txt"
    out_file.write_text(text, encoding="utf-8")
    return out_file


def load_raw_text(source_id: str, raw_dir: Path) -> Optional[str]:
    """Load raw extracted text for a source."""
    out_file = raw_dir / f"{source_id}.txt"
    if out_file.exists():
        return out_file.read_text(encoding="utf-8")
    return None
