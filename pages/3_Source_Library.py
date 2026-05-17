"""
pages/3_Source_Library.py — Browse indexed sources in the knowledge base.
"""

import json
import os

import streamlit as st
from src.page_header import render_header
from src.vector_store import get_collection_count

st.set_page_config(
    page_title="Source Library · Indispensable Values Q&A",
    page_icon="📚",
    layout="wide",
)

render_header("Source Library")

_KB_STATUS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "kb_status.json")


def _load_kb_status() -> dict:
    try:
        with open(_KB_STATUS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"built": False, "last_built": None, "num_chunks": 0, "sources": []}


st.markdown(
    """
    <p style="font-family:'Lato',sans-serif; color:#444; line-height:1.7;">
        The knowledge base is built from the following authenticated sources —
        video talks, discourse transcripts, stories, and published books of
        Pūjya Swāmī Aparājitānandajī of Chinmaya Mission.
    </p>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# KB status banner
# ---------------------------------------------------------------------------
kb = _load_kb_status()
try:
    live_count = get_collection_count()
except Exception:
    live_count = 0

if kb.get("built") and live_count > 0:
    st.success(
        f"✅ Knowledge base is active — {live_count:,} passages indexed"
        + (f" (last built: {kb['last_built']})" if kb.get("last_built") else ""),
        icon="✅",
    )
else:
    st.warning(
        "⚠️ Knowledge base has not been built yet. "
        "Contact an administrator to upload sources and build the KB.",
    )

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Canonical source list (static, as described in problem statement)
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>Canonical Sources</h3>",
    unsafe_allow_html=True,
)

canonical_sources = [
    {
        "category": "Value of Values — Discourse Series",
        "type": "Discourse Transcripts",
        "icon": "🎙️",
        "items": [
            "Value of Values — Discourse 1",
            "Value of Values — Discourse 2",
            "Value of Values — Discourse 3",
            "Value of Values — Discourse 4",
            "Value of Values — Discourse 5",
            "Value of Values — Discourse 6",
            "Value of Values — Discourse 7",
            "Value of Values — Discourse 8",
        ],
    },
    {
        "category": "Bhagavad Gītā Chapter 13 — Discourse Series",
        "type": "Discourse Transcripts",
        "icon": "📜",
        "items": [
            "BG Chapter 13 — Discourse 1",
            "BG Chapter 13 — Discourse 2",
        ],
    },
    {
        "category": "Value Based Stories for All — Discourse Series",
        "type": "Story Transcripts",
        "icon": "📖",
        "items": [
            "Value Based Stories — Discourse 1",
            "Value Based Stories — Discourse 2",
            "Value Based Stories — Discourse 3",
            "Value Based Stories — Discourse 4",
            "Value Based Stories — Discourse 5",
            "Value Based Stories — Discourse 6",
        ],
    },
    {
        "category": "Indispensable Values Book (2022)",
        "type": "Published Book",
        "icon": "📚",
        "items": [
            "Indispensable Values — 320 pages",
        ],
    },
]

for source_group in canonical_sources:
    with st.expander(
        f"{source_group['icon']} {source_group['category']} ({source_group['type']})",
        expanded=False,
    ):
        for item in source_group["items"]:
            st.markdown(
                f"<span style='font-family:\"Lato\",sans-serif; color:#444;'>▪ {item}</span>",
                unsafe_allow_html=True,
            )

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Uploaded sources (from KB status file)
# ---------------------------------------------------------------------------
uploaded = kb.get("sources", [])
if uploaded:
    st.markdown(
        "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>Uploaded Sources</h3>",
        unsafe_allow_html=True,
    )
    for src in uploaded:
        name = src if isinstance(src, str) else src.get("name", str(src))
        st.markdown(
            f"<span style='font-family:\"Lato\",sans-serif; color:#444;'>📄 {name}</span>",
            unsafe_allow_html=True,
        )

st.markdown(
    """
    <div style='text-align:center; font-family:"Lato",sans-serif; font-size:0.8rem; color:#888; margin-top:2rem;'>
        Built with reverence · Chinmaya Mission · Bhagavad Gītā Chapter 13
    </div>
    """,
    unsafe_allow_html=True,
)
