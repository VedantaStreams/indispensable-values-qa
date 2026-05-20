import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

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
.swamiji-quote{background:linear-gradient(135deg,#FFFFFF,#E8F4F6);border-left:5px solid #0D5C6B;border-radius:0 14px 14px 0;padding:1rem 1.5rem;margin:.8rem 0;font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1rem;color:#0A1E28;line-height:1.7;}
.swamiji-quote-attr{font-family:'Lato',sans-serif;font-style:normal;font-size:.75rem;font-weight:700;color:#0D5C6B;letter-spacing:.5px;margin-top:.4rem;}

.om-box-qa {
    background:linear-gradient(135deg,#FFFFFF,#D0EDF1);
    border:2px solid #062E3A;border-radius:16px;
    width:90px;height:90px;
    display:inline-flex;align-items:center;justify-content:center;
    margin-bottom:.8rem;
    box-shadow:0 4px 16px rgba(212,175,55,.20);
}
.om-box-qa img{width:70px;height:70px;object-fit:contain;border-radius:10px;}

.qa-header {
    background: linear-gradient(135deg, #FFFFFF 0%, #D0EDF1 50%, #FFFFFF 100%);
    border: 2px solid #88C5D0;
    border-radius: 18px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,.08);
}
.qa-header-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #062E3A;
    margin-bottom: 0.3rem;
}
.qa-header-sub {
    color: #0D5C6B;
    font-style: italic;
    font-size: 1rem;
    font-family: 'Cormorant Garamond', serif;
}

/* Starter question buttons — Royal Maroon */
.stButton > button {
    background: linear-gradient(135deg, #FFFFFF, #D0EDF1) !important;
    color: #062E3A !important;
    border: 1.5px solid #062E3A !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1rem !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-style: italic !important;
    font-size: 0.92rem !important;
    transition: all 0.2s !important;
    text-align: left !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 3rem !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0D5C6B, #2C95A8) !important;
    color: white !important;
    border-color: #062E3A !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(26,122,140,0.3) !important;
}
.chat-wrapper {
    max-height: 58vh;
    overflow-y: auto;
    padding-right: 0.5rem;
    margin-bottom: 1rem;
}
.user-bubble {
    background: linear-gradient(135deg, #0D5C6B, #2C95A8);
    border: 1px solid #88C5D0;
    border-radius: 16px 16px 4px 16px;
    padding: 0.85rem 1.15rem;
    margin: 0.5rem 0 0.5rem 18%;
    color: white;
    font-size: 0.95rem;
    line-height: 1.6;
}
.bot-bubble {
    background: #FFFFFF;
    border: 1.5px solid #88C5D0;
    border-radius: 4px 16px 16px 16px;
    padding: 1rem 1.3rem;
    margin: 0.5rem 18% 0.5rem 0;
    color: #0A1E28;
    font-size: 0.93rem;
    line-height: 1.75;
}
.role-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    margin-bottom: 0.3rem;
    opacity: 0.85;
}
.user-label { color: #0D5C6B; text-align: right; }
.bot-label  { color: #062E3A; }
.sample-q {
    background: #FFFFFF;
    border: 1.5px solid #88C5D0;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
    color: #062E3A;
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
    <div class="om-box-qa">
        <img src="data:image/jpeg;base64,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" alt="Om"/>
    </div><br>
    <div class="qa-header-title">Indispensable Values Q&amp;A</div>
    <div class="qa-header-sub">
        Ask questions grounded in Swamiji's teachings on Bhagavad Gītā Chapters 13 &amp; 16 — Jñāna Sādhana values &amp; Daivī / Āsurī qualities
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
    <div style="background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:12px;
        padding:1rem 1.4rem;margin-bottom:1rem;border-left:5px solid #0D5C6B;">
        <div style="font-family:'Playfair Display',serif;font-weight:700;
            color:#062E3A;font-size:1.05rem;margin-bottom:.3rem;">
            ✨ Starter Questions
        </div>
        <div style="font-size:.88rem;color:#1A3A45;line-height:1.6;">
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
