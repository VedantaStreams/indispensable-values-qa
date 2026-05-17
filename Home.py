"""
Home.py — Hero page for Indispensable Values Q&A.

Displays the Gurudev/Swamiji photo placeholder, app title, visitor counter,
and navigation overview.
"""

import streamlit as st

from src.page_header import inject_fonts_and_css
from src.visitor_counter import record_visit

st.set_page_config(
    page_title="Indispensable Values Q&A",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_fonts_and_css()

# Record this session's visit
visitor_count = record_visit()

# ---------------------------------------------------------------------------
# Hero section
# ---------------------------------------------------------------------------
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown(
        """
        <div style="text-align:center; padding:1rem;">
            <div style="
                width:220px; height:280px; margin:auto;
                border-radius:12px;
                background: linear-gradient(135deg, #FFB6C1 0%, #D4A017 100%);
                display:flex; align-items:center; justify-content:center;
                font-size:5rem; color:white;
            ">🙏</div>
            <p style="
                font-family:'Cormorant Garamond',serif;
                font-size:0.9rem; color:#8B6914; margin-top:0.5rem;
            ">Pūjya Swāmī Aparājitānandajī</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div style="padding-top:1.5rem;">
            <span style="font-size:2.8rem; color:#8B6914; font-family:'Cormorant Garamond',serif;">ॐ</span>
            <h1 style="font-family:'Playfair Display',serif; color:#4A7C59; margin-top:0;">
                Indispensable Values Q&amp;A
            </h1>
            <h3 style="font-family:'Cormorant Garamond',serif; color:#8B6914; font-weight:400;">
                A Reverential AI Study Companion
            </h3>
            <p style="font-family:'Lato',sans-serif; font-size:1rem; color:#3A3A3A; line-height:1.7;">
                Grounded in the authentic teachings of
                <strong>Pūjya Swāmī Aparājitānandajī</strong> of Chinmaya Mission,
                this application answers your questions about the
                <strong>20 Indispensable Values (jñāna sādhana)</strong>
                from Bhagavad Gītā Chapter 13, verses 7–11.
                Every answer is drawn exclusively from Swamiji's video talks,
                transcripts, stories, and published books — never fabricated.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.3; margin:0.5rem 0;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Visitor counter
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <div style="text-align:center; margin: 0.5rem 0 1.5rem 0;">
        <span style="
            background:#EDF3EC; border:1px solid #4A7C59; border-radius:20px;
            padding:0.4rem 1.2rem; font-family:'Lato',sans-serif;
            font-size:0.9rem; color:#4A7C59;
        ">
            🙏 Blessed seekers who have visited: <strong>{visitor_count:,}</strong>
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Navigation cards
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>Explore the App</h3>",
    unsafe_allow_html=True,
)

nav_items = [
    ("🙏", "Gratitude & Reverence", "Honour the Guru Paramparā and the lineage of wisdom."),
    ("📖", "About Pūjya Swamiji", "Learn about Swāmī Aparājitānandajī and Chinmaya Mission."),
    ("💬", "Q&A — Indispensable Values", "Ask questions; receive source-cited answers from Swamiji's teachings."),
    ("📚", "Source Library", "Browse all indexed discourse transcripts and books."),
    ("ℹ️", "About the App", "Technical overview of the RAG pipeline and design."),
    ("❓", "FAQ", "Frequently asked questions about the values and this app."),
    ("📲", "Get the App", "How to access and share this companion."),
]

cols = st.columns(3)
for i, (icon, title, desc) in enumerate(nav_items):
    with cols[i % 3]:
        st.markdown(
            f"""
            <div style="
                background:#EDF3EC; border-radius:10px; padding:1rem;
                border-left:4px solid #4A7C59; margin-bottom:1rem;
            ">
                <span style="font-size:1.5rem;">{icon}</span>
                <strong style="font-family:'Playfair Display',serif; color:#4A7C59; display:block; margin:0.3rem 0;">
                    {title}
                </strong>
                <span style="font-family:'Lato',sans-serif; font-size:0.85rem; color:#555;">{desc}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(
    """
    <hr style='border-top:1px solid #4A7C59; opacity:0.2; margin-top:2rem;'>
    <div style='text-align:center; font-family:"Lato",sans-serif; font-size:0.8rem; color:#888; margin-top:0.5rem;'>
        Built with reverence · Chinmaya Mission · Bhagavad Gītā Chapter 13
    </div>
    """,
    unsafe_allow_html=True,
)
