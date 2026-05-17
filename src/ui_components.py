"""
src/ui_components.py — Reusable Streamlit UI components for the app.
"""

import streamlit as st


GOLD = "#d4af57"
DARK_BG = "#1a0a2e"


def render_page_header(title: str, subtitle: str = "", icon: str = "🪷"):
    """Render a styled page header."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1a0a2e, #2d1b4e);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid {GOLD};
    ">
        <div style="font-size:1.8rem; font-weight:700; color:#f5e6c8; font-family:'Georgia',serif;">
            {icon} {title}
        </div>
        {f'<div style="color:{GOLD}; font-style:italic; margin-top:0.3rem; font-size:0.95rem;">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def render_source_badge(source_type: str) -> str:
    """Return HTML badge for a source type."""
    colors_map = {
        "youtube_video": ("#ff4444", "▶ YouTube"),
        "youtube_playlist": ("#ff6644", "▶ Playlist"),
        "pdf": ("#4488ff", "📄 PDF"),
        "docx": ("#44aaff", "📝 DOCX"),
        "txt": ("#44ccaa", "📃 TXT"),
        "document": ("#8866ff", "📖 Doc"),
    }
    color, label = colors_map.get(source_type, ("#888888", "📁 Source"))
    return f'<span style="background:{color}22; color:{color}; border:1px solid {color}55; border-radius:12px; padding:2px 10px; font-size:0.78rem; font-weight:600;">{label}</span>'


def render_chunk_card(chunk: dict, index: int):
    """Render a retrieved chunk as an expandable card."""
    meta = chunk.get("metadata", {})
    score = chunk.get("score", 0)
    score_pct = int(score * 100)
    score_color = "#22bb55" if score > 0.7 else "#ddaa22" if score > 0.5 else "#cc5555"

    source_title = meta.get("source_title", "Unknown Source")
    speaker = meta.get("speaker", "")
    chapter = meta.get("chapter", "")
    verse = meta.get("verse_range", "")
    page = meta.get("page_number", "")
    ts = meta.get("timestamp", "")
    chunk_type = meta.get("chunk_type", "general")

    ref_parts = []
    if speaker:
        ref_parts.append(speaker)
    if chapter:
        ref_parts.append(f"Ch. {chapter}")
    if verse:
        ref_parts.append(f"v. {verse}")
    if page:
        ref_parts.append(f"p. {page}")
    if ts:
        ref_parts.append(f"⏱ {ts}")
    ref_str = " · ".join(ref_parts)

    with st.expander(
        f"📌 Chunk {index} — {source_title[:50]} "
        f"({'...' if len(source_title) > 50 else ''}) | Relevance: {score_pct}%",
        expanded=False,
    ):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.caption(ref_str)
        with col2:
            st.markdown(
                f'<span style="color:{score_color}; font-weight:bold;">Score: {score_pct}%</span>',
                unsafe_allow_html=True,
            )

        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.03);
            border-left: 3px solid {GOLD}55;
            padding: 0.8rem 1rem;
            border-radius: 6px;
            font-size: 0.88rem;
            line-height: 1.6;
            color: rgba(245,230,200,0.85);
        ">{chunk['text']}</div>
        """, unsafe_allow_html=True)

        if meta.get("source_url"):
            st.markdown(f"🔗 [Open source]({meta['source_url']})")


def render_chat_message(role: str, content: str):
    """Render a styled chat message."""
    if role == "user":
        st.markdown(f"""
        <div style="
            display:flex; justify-content:flex-end; margin-bottom:1rem;
        ">
            <div style="
                background: linear-gradient(135deg, #2d1b4e, #3a2060);
                border: 1px solid {GOLD}44;
                border-radius: 16px 16px 4px 16px;
                padding: 0.9rem 1.2rem;
                max-width: 75%;
                color: #f5e6c8;
                font-size: 0.95rem;
                line-height: 1.6;
            ">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            display:flex; justify-content:flex-start; margin-bottom:1rem;
        ">
            <div style="margin-right:0.6rem; font-size:1.4rem; align-self:flex-start;">🪷</div>
            <div style="
                background: linear-gradient(135deg, #0d1a2e, #152035);
                border: 1px solid rgba(212,175,57,0.25);
                border-radius: 4px 16px 16px 16px;
                padding: 0.9rem 1.2rem;
                max-width: 85%;
                color: #e8d5b0;
                font-size: 0.93rem;
                line-height: 1.7;
            ">{content}</div>
        </div>
        """, unsafe_allow_html=True)


def render_status_banner(message: str, type: str = "info"):
    """Render a styled status banner."""
    colors_map = {
        "info": (GOLD, "#d4af5722"),
        "success": ("#22bb55", "#22bb5522"),
        "error": ("#cc4444", "#cc444422"),
        "warning": ("#ddaa22", "#ddaa2222"),
    }
    border_color, bg_color = colors_map.get(type, (GOLD, "#d4af5722"))
    st.markdown(f"""
    <div style="
        background: {bg_color};
        border: 1px solid {border_color}55;
        border-left: 4px solid {border_color};
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        color: #f5e6c8;
        font-size: 0.9rem;
    ">{message}</div>
    """, unsafe_allow_html=True)


def inject_global_css():
    """Inject global CSS for dark Vedantic theme."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Source Sans 3', sans-serif;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: #1a1a2e !important;
        color: #f5e6c8 !important;
        border-color: rgba(212,175,57,0.3) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #2d1b4e, #1a3a2e);
        color: #f5e6c8;
        border: 1px solid rgba(212,175,57,0.4);
        border-radius: 8px;
        font-family: 'Lora', serif;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        border-color: #d4af57;
        transform: translateY(-1px);
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0a1e 0%, #1a1230 100%);
    }
    h1, h2, h3 { font-family: 'Lora', serif !important; color: #f5e6c8 !important; }
    </style>
    """, unsafe_allow_html=True)
