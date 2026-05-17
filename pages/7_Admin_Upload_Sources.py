"""
pages/7_Admin_Upload_Sources.py — 🔐 Password-protected file upload for source ingestion.
"""

import json
import os

import streamlit as st
from src.admin_guard import require_admin
from src.page_header import render_header
from src.ingestion import ingest_file
from src.vector_store import add_documents
from src.transcription import fetch_transcript

st.set_page_config(
    page_title="🔐 Admin: Upload Sources · Indispensable Values Q&A",
    page_icon="🔐",
    layout="wide",
)

require_admin()
render_header("🔐 Admin — Upload Sources")

_KB_STATUS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "kb_status.json")


def _load_kb_status() -> dict:
    try:
        with open(_KB_STATUS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"built": False, "last_built": None, "num_chunks": 0, "sources": []}


def _save_kb_status(data: dict) -> None:
    os.makedirs(os.path.dirname(_KB_STATUS_PATH), exist_ok=True)
    with open(_KB_STATUS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


st.markdown(
    """
    <p style="font-family:'Lato',sans-serif; color:#444; line-height:1.7;">
        Upload PDF, DOCX, or TXT files to index into the knowledge base,
        or add a YouTube URL to fetch and index a transcript.
        Each uploaded file will be chunked and added to ChromaDB immediately.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# File upload section
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>Upload Document</h3>",
    unsafe_allow_html=True,
)

source_type = st.selectbox(
    "Source type",
    options=["discourse", "story", "book", "transcript"],
    format_func=lambda x: {
        "discourse": "📣 Discourse transcript",
        "story": "📖 Story collection",
        "book": "📚 Published book",
        "transcript": "🎙️ Video transcript",
    }[x],
)

uploaded_file = st.file_uploader(
    "Choose a file (PDF, DOCX, or TXT)",
    type=["pdf", "docx", "doc", "txt"],
    accept_multiple_files=False,
)

if uploaded_file is not None:
    st.write(f"**File:** {uploaded_file.name}  |  **Size:** {uploaded_file.size / 1024:.1f} KB")

    if st.button("➕ Add to Knowledge Base", type="primary"):
        with st.spinner(f"Processing {uploaded_file.name}…"):
            file_bytes = uploaded_file.read()
            try:
                docs, count = ingest_file(file_bytes, uploaded_file.name, source_type=source_type)
                added = add_documents(docs)

                # Update kb_status
                kb = _load_kb_status()
                sources = kb.get("sources", [])
                if uploaded_file.name not in sources:
                    sources.append(uploaded_file.name)
                kb["sources"] = sources
                kb["num_chunks"] = kb.get("num_chunks", 0) + added
                _save_kb_status(kb)

                st.success(
                    f"✅ Successfully indexed **{uploaded_file.name}** — "
                    f"{count} chunks created, {added} added to the knowledge base."
                )
            except Exception as e:
                st.error(f"❌ Error processing file: {e}")

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# YouTube transcript section
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>Fetch YouTube Transcript</h3>",
    unsafe_allow_html=True,
)

yt_url = st.text_input(
    "YouTube URL or video ID",
    placeholder="https://www.youtube.com/watch?v=...",
)
yt_source_name = st.text_input(
    "Source name (for citation in answers)",
    placeholder="e.g. Value of Values — Discourse 1",
)
yt_source_type = st.selectbox(
    "Transcript source type",
    options=["transcript", "discourse"],
    key="yt_source_type",
)

if st.button("📥 Fetch & Index Transcript", type="primary"):
    if not yt_url.strip():
        st.warning("Please enter a YouTube URL.")
    elif not yt_source_name.strip():
        st.warning("Please enter a source name for citation purposes.")
    else:
        with st.spinner("Fetching transcript from YouTube…"):
            try:
                text = fetch_transcript(yt_url.strip())
                if text is None:
                    st.error("❌ Transcript not available for this video (disabled or not found).")
                else:
                    from src.chunking import chunk_document
                    from src.vector_store import add_documents as _add

                    source_meta = {"source": yt_source_name.strip(), "type": yt_source_type}
                    docs = chunk_document(text, source_meta, source_type=yt_source_type)
                    added = _add(docs)

                    kb = _load_kb_status()
                    sources = kb.get("sources", [])
                    if yt_source_name.strip() not in sources:
                        sources.append(yt_source_name.strip())
                    kb["sources"] = sources
                    kb["num_chunks"] = kb.get("num_chunks", 0) + added
                    _save_kb_status(kb)

                    st.success(
                        f"✅ Transcript indexed as **{yt_source_name}** — "
                        f"{len(docs)} chunks, {added} added."
                    )
            except ValueError as e:
                st.error(f"❌ {e}")
            except Exception as e:
                st.error(f"❌ Error fetching transcript: {e}")

st.markdown(
    """
    <div style='text-align:center; font-family:"Lato",sans-serif; font-size:0.8rem; color:#888; margin-top:2rem;'>
        Admin area — restricted access
    </div>
    """,
    unsafe_allow_html=True,
)
