"""
pages/8_Admin_Build_Knowledge_Base.py — 🔐 Password-protected KB builder.

Allows admins to view KB status, rebuild from scratch, or verify the collection.
"""

import json
import os
from datetime import datetime, timezone

import streamlit as st
from src.admin_guard import require_admin
from src.page_header import render_header
from src.vector_store import get_collection_count, reset_collection

st.set_page_config(
    page_title="🔐 Admin: Build KB · Indispensable Values Q&A",
    page_icon="🔐",
    layout="wide",
)

require_admin()
render_header("🔐 Admin — Build Knowledge Base")

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


# ---------------------------------------------------------------------------
# Current status
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>Knowledge Base Status</h3>",
    unsafe_allow_html=True,
)

kb = _load_kb_status()
try:
    live_count = get_collection_count()
except Exception:
    live_count = 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Chunks", f"{live_count:,}")
with col2:
    st.metric("Sources Indexed", len(kb.get("sources", [])))
with col3:
    st.metric("Status", "✅ Active" if live_count > 0 else "⚠️ Empty")

if kb.get("last_built"):
    st.caption(f"Last built: {kb['last_built']}")

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Indexed sources list
# ---------------------------------------------------------------------------
sources = kb.get("sources", [])
if sources:
    st.markdown(
        "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>Indexed Sources</h3>",
        unsafe_allow_html=True,
    )
    for src in sources:
        name = src if isinstance(src, str) else src.get("name", str(src))
        st.markdown(
            f"<span style='font-family:\"Lato\",sans-serif; color:#444;'>📄 {name}</span>",
            unsafe_allow_html=True,
        )

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Mark KB as built (after manual upload workflow)
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>Mark Knowledge Base as Built</h3>",
    unsafe_allow_html=True,
)
st.markdown(
    """
    <p style="font-family:'Lato',sans-serif; color:#444;">
        After uploading and indexing all source documents via the Upload Sources page,
        click here to mark the knowledge base as fully built. This updates the status
        banner shown to end users.
    </p>
    """,
    unsafe_allow_html=True,
)

if st.button("✅ Mark as Built", type="primary"):
    count = get_collection_count()
    kb["built"] = True
    kb["last_built"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    kb["num_chunks"] = count
    _save_kb_status(kb)
    st.success(f"Knowledge base marked as built — {count:,} chunks active.")
    st.rerun()

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Reset / rebuild
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59; color:#C0392B;'>"
    "⚠️ Reset Knowledge Base</h3>",
    unsafe_allow_html=True,
)
st.warning(
    "Resetting will permanently delete ALL indexed chunks from ChromaDB. "
    "You will need to re-upload and re-index all sources. This cannot be undone.",
    icon="⚠️",
)

confirm_reset = st.checkbox("I understand — delete all indexed data")
if st.button("🗑️ Reset Knowledge Base", disabled=not confirm_reset):
    with st.spinner("Deleting ChromaDB collection…"):
        try:
            reset_collection()
            kb["built"] = False
            kb["last_built"] = None
            kb["num_chunks"] = 0
            kb["sources"] = []
            _save_kb_status(kb)
            st.success("✅ Knowledge base has been reset. Please re-upload all sources.")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Reset failed: {e}")

st.markdown(
    """
    <div style='text-align:center; font-family:"Lato",sans-serif; font-size:0.8rem; color:#888; margin-top:2rem;'>
        Admin area — restricted access
    </div>
    """,
    unsafe_allow_html=True,
)
