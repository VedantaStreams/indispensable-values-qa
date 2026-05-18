import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
"""
pages/3_Indispensable_Values_QA.py — The main RAG-powered Q&A chatbot page.
"""

import streamlit as st
import datetime
from pathlib import Path
import sys
from pathlib import Path as _Path
_ROOT = _Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from src.page_header import render_om_symbol, render_page_quote


st.set_page_config(
    page_title="Indispensable Values Q&A",
    page_icon="🪷",
    layout="wide",
)

render_om_symbol()

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ui_components import inject_global_css, render_chunk_card
from src.rag_chain import get_rag_answer, estimate_query_cost
from src.vector_store import get_collection_stats
from src.export_utils import export_to_txt, export_to_pdf, export_to_docx
from src.prompts import INDISPENSABLE_VALUES

inject_global_css()

# ── Page CSS ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.swamiji-quote{background:linear-gradient(135deg,#EDF3EC,#F8F9F5);border-left:5px solid #4A7C59;border-radius:0 14px 14px 0;padding:1rem 1.5rem;margin:.8rem 0;font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1rem;color:#2A4A38;line-height:1.7;}
.swamiji-quote-attr{font-family:'Lato',sans-serif;font-style:normal;font-size:.75rem;font-weight:700;color:#4A7C59;letter-spacing:.5px;margin-top:.4rem;}
.qa-header {
    background: linear-gradient(135deg, #0d0a1e 0%, #1a1230 50%, #0a1a12 100%);
    border: 1px solid rgba(212,175,55,0.35);
    border-radius: 14px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 1.5rem;
    text-align: center;
}
.qa-header-title {
    font-family: 'Lora', serif;
    font-size: 2rem;
    color: #f5e6c8;
    margin-bottom: 0.3rem;
}
.qa-header-sub {
    color: #d4af57;
    font-style: italic;
    font-size: 0.95rem;
}
.chat-wrapper {
    max-height: 58vh;
    overflow-y: auto;
    padding-right: 0.5rem;
    margin-bottom: 1rem;
}
.user-bubble {
    background: linear-gradient(135deg, #2d1b4e, #3a2060);
    border: 1px solid rgba(212,175,55,0.3);
    border-radius: 16px 16px 4px 16px;
    padding: 0.85rem 1.15rem;
    margin: 0.5rem 0 0.5rem 18%;
    color: #f5e6c8;
    font-size: 0.95rem;
    line-height: 1.6;
}
.bot-bubble {
    background: linear-gradient(135deg, #0d1822, #152030);
    border: 1px solid rgba(212,175,55,0.2);
    border-radius: 4px 16px 16px 16px;
    padding: 1rem 1.3rem;
    margin: 0.5rem 18% 0.5rem 0;
    color: #e8d5b0;
    font-size: 0.93rem;
    line-height: 1.75;
}
.role-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    margin-bottom: 0.3rem;
    opacity: 0.75;
}
.user-label { color: #d4af57; text-align: right; }
.bot-label  { color: #7ec8a0; }
.sample-q {
    background: rgba(212,175,55,0.07);
    border: 1px solid rgba(212,175,55,0.2);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
    color: #d4af57;
    cursor: pointer;
    margin-bottom: 0.4rem;
    transition: background 0.2s;
}
.sample-q:hover { background: rgba(212,175,55,0.15); }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Filters & Controls
# ════════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🎛️ Filters")
    st.caption("Narrow retrieval to specific sources")

    filter_speaker = st.text_input(
        "Speaker", placeholder="e.g. Swami Aparajitananda", key="f_speaker"
    )
    filter_scripture = st.text_input(
        "Scripture", placeholder="e.g. Bhagavad Gītā", key="f_scripture"
    )
    filter_chapter = st.text_input(
        "Chapter", placeholder="e.g. 13", key="f_chapter"
    )
    filter_source_type = st.selectbox(
        "Source Type",
        ["All", "youtube_video", "youtube_playlist", "pdf_book", "transcript", "notes"],
        key="f_src_type",
    )
    filter_language = st.selectbox(
        "Language", ["All", "English", "Sanskrit", "Hindi", "Tamil", "Telugu"],
        key="f_lang",
    )
    filter_value = st.selectbox(
        "Value / Topic",
        ["All"] + INDISPENSABLE_VALUES,
        key="f_value",
    )

    st.divider()
    st.markdown("## ⚙️ Retrieval")
    n_chunks = st.slider("Chunks to retrieve", 3, 10, 6)
    model = st.selectbox("Chat Model", ["gpt-4o-mini", "gpt-4o"], index=0)
    show_sources = st.checkbox("Show retrieved chunks", value=True)

    st.divider()
    st.markdown("## 📊 Status")
    try:
        stats = get_collection_stats()
        st.metric("Chunks indexed", stats.get("total_chunks", 0))
        st.metric("Sources", stats.get("total_sources", 0))
        if stats.get("total_chunks", 0) == 0:
            st.warning("Knowledge base is empty. Build it first.")
    except Exception:
        st.error("Could not reach vector store.")

# ── Build filter dict ──────────────────────────────────────────────────────────
filters = {}
if filter_speaker.strip():
    filters["speaker"] = filter_speaker.strip()
if filter_scripture.strip():
    filters["scripture"] = filter_scripture.strip()
if filter_chapter.strip():
    filters["chapter"] = filter_chapter.strip()
if filter_source_type != "All":
    filters["source_type"] = filter_source_type
if filter_language != "All":
    filters["language"] = filter_language

# ════════════════════════════════════════════════════════════════════════════════
# MAIN — Header
# ════════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="qa-header">
    <div style="font-size:2.5rem; margin-bottom:0.4rem;">🪷</div>
    <div class="qa-header-title">Indispensable Values Q&amp;A</div>
    <div class="qa-header-sub">
        Ask questions grounded in Swamiji's teachings on the Jñāna Sādhana values of Bhagavad Gītā Chapter 13
    </div>
</div>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_chunks" not in st.session_state:
    st.session_state.last_chunks = []
if "last_usage" not in st.session_state:
    st.session_state.last_usage = {}

# ── Toolbar ────────────────────────────────────────────────────────────────────
col_clear, col_dl1, col_dl2, col_dl3 = st.columns([2, 1, 1, 1])
with col_clear:
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_chunks = []
        st.session_state.last_usage = {}
        st.rerun()

msgs = st.session_state.messages
if msgs:
    with col_dl1:
        txt_bytes = export_to_txt(msgs)
        st.download_button(
            "⬇️ TXT", txt_bytes,
            file_name=f"iv_qa_{datetime.date.today()}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col_dl2:
        pdf_bytes = export_to_pdf(msgs)
        if pdf_bytes:
            st.download_button(
                "⬇️ PDF", pdf_bytes,
                file_name=f"iv_qa_{datetime.date.today()}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.caption("Install reportlab for PDF")
    with col_dl3:
        docx_bytes = export_to_docx(msgs)
        if docx_bytes:
            st.download_button(
                "⬇️ DOCX", docx_bytes,
                file_name=f"iv_qa_{datetime.date.today()}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        else:
            st.caption("Install python-docx for DOCX")

st.divider()

# ── 20 Starter Questions ──────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style="background:#EDF3EC;border:1.5px solid #B8D4BC;border-radius:12px;
        padding:1rem 1.4rem;margin-bottom:1rem;border-left:5px solid #4A7C59;">
        <div style="font-family:'Playfair Display',serif;font-weight:700;
            color:#2A5C3A;font-size:1.05rem;margin-bottom:.3rem;">
            ✨ Starter Questions
        </div>
        <div style="font-size:.88rem;color:#3A5040;line-height:1.6;">
            New to the app? Click any question below to begin your inquiry.
            Questions are drawn from <strong>Bhagavad Gītā Chapters 13 &amp; 16</strong>
            — the divine and demoniac qualities Swamiji unfolds in his discourses.
        </div>
    </div>
    """, unsafe_allow_html=True)

    starter_themes = {
        "🌱 Foundation": [
            "What are the 20 Indispensable Values from Bhagavad Gītā Chapter 13?",
            "Why are these values called 'indispensable' for spiritual progress?",
            "What does *amānitvam* (humility) mean in Vedānta?",
            "How is humility different from low self-esteem?",
        ],
        "❤️ Heart & Emotions": [
            "What is true *ahiṃsā* (non-violence) in daily life?",
            "How can I cultivate *kṣāntiḥ* (forbearance)?",
            "What is the difference between forgiveness and weakness?",
            "How do I deal with anger from a spiritual perspective?",
        ],
        "🧘 Inner Discipline": [
            "How do I practice *ātma-vinigraha* (self-control)?",
            "What is the role of *vairāgya* (dispassion) in daily life?",
            "How do I overcome attachment to results of my actions?",
            "What is the right attitude toward success and failure?",
        ],
        "👤 Self & Ego": [
            "What is *anahaṅkāra* and how do I let go of ego?",
            "How is non-doership understood in Vedānta?",
            "What is the difference between confidence and pride?",
            "What does Chapter 16 say about divine vs demoniac qualities?",
        ],
        "💕 Devotion & Practice": [
            "What is *bhakti avyabhicāriṇī* — unswerving devotion?",
            "How do I deepen my relationship with God?",
            "What is the right time and way to practice spiritual values?",
            "How do I balance worldly responsibilities with spiritual life?",
        ],
    }

    for theme, questions in starter_themes.items():
        st.markdown(f"**{theme}**")
        cols = st.columns(2)
        for i, q in enumerate(questions):
            # Strip markdown for actual question
            clean_q = q.replace("*", "")
            with cols[i % 2]:
                if st.button(q, key=f"start_{theme}_{i}", use_container_width=True):
                    st.session_state.messages.append(
                        {"role": "user", "content": clean_q}
                    )
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

# ── Chat History ───────────────────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="role-label user-label">You</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="role-label bot-label">🪷 Swamiji\'s Teachings</div>', unsafe_allow_html=True)
            # Render markdown inside the bubble via st.markdown for bold/italic support
            with st.container():
                st.markdown(msg["content"])
            st.markdown("---")

# ── Process Last Pending User Message ─────────────────────────────────────────
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_q = st.session_state.messages[-1]["content"]

    with st.spinner("🔍 Searching knowledge base and composing answer…"):
        result = get_rag_answer(
            question=last_q,
            filters=filters if filters else None,
            n_chunks=n_chunks,
            model=model,
        )

    answer      = result.get("answer", "")
    chunks      = result.get("chunks", [])
    usage       = result.get("usage", {})
    gw          = result.get("guardrail_warning", "")

    # Append assistant answer
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.last_chunks = chunks
    st.session_state.last_usage  = usage

    if gw:
        st.session_state.messages[-1]["content"] += f"\n\n{gw}"

    st.rerun()

# ── Chat Input ─────────────────────────────────────────────────────────────────
user_input = st.chat_input(
    "Ask a question about Indispensable Values…",
    key="chat_input_main",
)
if user_input and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    st.rerun()

# ── Retrieved Chunks (expandable) ──────────────────────────────────────────────
if show_sources and st.session_state.last_chunks:
    st.divider()
    st.markdown("### 📌 Retrieved Context Chunks")
    st.caption(
        f"Top {len(st.session_state.last_chunks)} chunk(s) retrieved from the knowledge base "
        "and passed to the model."
    )
    for i, chunk in enumerate(st.session_state.last_chunks, 1):
        render_chunk_card(chunk, i)

# ── Usage Footer ───────────────────────────────────────────────────────────────
if st.session_state.last_usage:
    u = st.session_state.last_usage
    pt = u.get("prompt_tokens", 0)
    ct = u.get("completion_tokens", 0)
    cost = estimate_query_cost(pt, ct, model)
    st.caption(
        f"💡 Last query: {pt} prompt + {ct} completion tokens "
        f"≈ ${cost:.5f} | Queries today: {u.get('queries_today', 0)}"
    )
