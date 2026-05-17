"""
pages/9_Admin_Settings.py — 🔐 Password-protected settings page.
"""

import json
import os

import streamlit as st
from src.admin_guard import require_admin
from src.page_header import render_header
from src.visitor_counter import get_count

st.set_page_config(
    page_title="🔐 Admin: Settings · Indispensable Values Q&A",
    page_icon="🔐",
    layout="wide",
)

require_admin()
render_header("🔐 Admin — Settings")

_KB_STATUS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "kb_status.json")
_VISITORS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "visitors.json")

# ---------------------------------------------------------------------------
# App diagnostics
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>App Diagnostics</h3>",
    unsafe_allow_html=True,
)

openai_key = st.secrets.get("OPENAI_API_KEY", "")
admin_pw = st.secrets.get("ADMIN_PASSWORD", "")

diag_items = [
    ("🔑 OpenAI API Key", "✅ Configured" if openai_key else "❌ Not set"),
    ("🔐 Admin Password", "✅ Configured" if admin_pw else "❌ Not set"),
    ("👥 Total Visitors", f"{get_count():,}"),
]

for label, value in diag_items:
    color = "#4A7C59" if "✅" in value else "#C0392B"
    st.markdown(
        f"""
        <div style="display:flex; gap:1rem; margin-bottom:0.5rem; align-items:baseline;">
            <span style="font-family:'Playfair Display',serif; color:#3A3A3A; min-width:220px;">
                {label}
            </span>
            <span style="font-family:'Lato',sans-serif; color:{color}; font-weight:600;">{value}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# RAG settings display
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>RAG Pipeline Settings</h3>",
    unsafe_allow_html=True,
)

rag_settings = [
    ("LLM Model", "gpt-4o-mini"),
    ("LLM Temperature", "0.2"),
    ("Embedding Model", "text-embedding-3-small"),
    ("Default Chunks (k)", "8"),
    ("Similarity Threshold", "0.15"),
    ("Vector DB", "ChromaDB (local persistent)"),
    ("Collection Name", "indispensable_values"),
]

for label, value in rag_settings:
    st.markdown(
        f"""
        <div style="display:flex; gap:1rem; margin-bottom:0.4rem; align-items:baseline;">
            <span style="font-family:'Lato',sans-serif; color:#555; min-width:220px;">{label}</span>
            <code style="background:#EDF3EC; padding:0.1rem 0.4rem; border-radius:4px;
                         color:#4A7C59; font-size:0.9rem;">{value}</code>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Reset visitor count
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>Reset Visitor Counter</h3>",
    unsafe_allow_html=True,
)
st.warning("This will reset the visitor count to zero. This action cannot be undone.", icon="⚠️")

confirm_reset = st.checkbox("I understand — reset visitor count to zero")
if st.button("🔄 Reset Visitor Count", disabled=not confirm_reset):
    os.makedirs(os.path.dirname(_VISITORS_PATH), exist_ok=True)
    with open(_VISITORS_PATH, "w", encoding="utf-8") as f:
        json.dump({"count": 0, "sessions": []}, f, indent=2)
    st.success("✅ Visitor count has been reset to zero.")
    st.rerun()

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sign out
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>Session</h3>",
    unsafe_allow_html=True,
)

if st.button("🔓 Sign Out of Admin"):
    st.session_state.pop("admin_authenticated", None)
    st.success("Signed out. Admin session cleared.")
    st.rerun()

st.markdown(
    """
    <div style='text-align:center; font-family:"Lato",sans-serif; font-size:0.8rem; color:#888; margin-top:2rem;'>
        Admin area — restricted access
    </div>
    """,
    unsafe_allow_html=True,
)
