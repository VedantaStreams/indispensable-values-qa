"""
pages/4_About_the_App.py — App documentation and technical overview.
"""

import streamlit as st
from src.page_header import render_header

st.set_page_config(
    page_title="About the App · Indispensable Values Q&A",
    page_icon="ℹ️",
    layout="wide",
)

render_header("About the App")

st.markdown(
    """
    <h3 style="font-family:'Playfair Display',serif; color:#4A7C59;">Purpose</h3>
    <p style="font-family:'Lato',sans-serif; color:#3A3A3A; line-height:1.8;">
        <strong>Indispensable Values Q&amp;A</strong> is a reverential AI-powered study companion
        grounded in the teachings of Pūjya Swāmī Aparājitānandajī of Chinmaya Mission.
        It answers questions about the <strong>20 Indispensable Values (jñāna sādhana)</strong>
        from Bhagavad Gītā Chapter 13, verses 7–11, drawing exclusively from
        Swamiji's authenticated video talks, transcripts, stories, and published books.
        Answers are always source-cited and never fabricated.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# The 20 Values
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>The 20 Indispensable Values</h3>",
    unsafe_allow_html=True,
)

values_20 = [
    ("1", "Amānitvam", "Humility / Absence of pride"),
    ("2", "Adambhitvam", "Absence of ostentation / Unpretentiousness"),
    ("3", "Ahiṃsā", "Non-violence"),
    ("4", "Kṣāntiḥ", "Forbearance / Patience"),
    ("5", "Ārjavam", "Straightforwardness / Sincerity"),
    ("6", "Ācāryopāsanam", "Service and devotion to the Teacher"),
    ("7", "Śaucam", "Purity (of body, mind, and intellect)"),
    ("8", "Sthairyam", "Steadfastness"),
    ("9", "Ātmavinigrahaḥ", "Self-control / Mind-mastery"),
    ("10", "Indriyārtheṣu vairāgyam", "Dispassion toward sense objects"),
    ("11", "Anahaṅkāraḥ", "Absence of ego"),
    ("12", "Janma-mṛtyu-jarā-vyādhi-duḥkha-doṣānudarśanam", "Seeing the evil in birth, death, old age, sickness, and suffering"),
    ("13", "Asaktih", "Non-attachment"),
    ("14", "Anabhiṣvaṅgaḥ putra-dāra-gṛhādiṣu", "Non-clinging to son, wife, home, etc."),
    ("15", "Nityaṃ ca sama-cittatvam", "Constant even-mindedness in pleasant and unpleasant events"),
    ("16", "Mayi cānanya-yogena bhaktiḥ", "Unswerving devotion to Me (the Lord)"),
    ("17", "Vivikta-deśa-sevitvam", "Love of solitude"),
    ("18", "Aratir jana-saṃsadi", "Distaste for excessive socialising"),
    ("19", "Adhyātma-jñāna-nityatvam", "Constancy in self-knowledge"),
    ("20", "Tattva-jñānārtha-darśanam", "Seeing the goal as knowledge of Truth"),
]

cols = st.columns(2)
for i, (num, sanskrit, english) in enumerate(values_20):
    with cols[i % 2]:
        st.markdown(
            f"""
            <div style="
                background:#EDF3EC; border-radius:8px; padding:0.6rem 1rem;
                margin-bottom:0.6rem; border-left:3px solid #8B6914;
            ">
                <span style="font-family:'Cormorant Garamond',serif; color:#8B6914; font-size:0.8rem;">
                    {num}.
                </span>
                <strong style="font-family:'Cormorant Garamond',serif; color:#4A7C59; font-size:1rem;">
                    {sanskrit}
                </strong>
                <br>
                <span style="font-family:'Lato',sans-serif; font-size:0.85rem; color:#444;">
                    {english}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Tech stack
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>Tech Stack</h3>",
    unsafe_allow_html=True,
)

tech_items = [
    ("🖥️ Frontend", "Streamlit (multi-page app, 10 pages)"),
    ("🤖 LLM", "OpenAI GPT-4o-mini (temperature 0.2)"),
    ("🔢 Embeddings", "OpenAI text-embedding-3-small"),
    ("🗄️ Vector DB", "ChromaDB (local persistent)"),
    ("🐍 Language", "Python 3.11"),
    ("📐 Similarity Threshold", "0.15 (cosine relevance score)"),
    ("📦 Chunks Retrieved", "8 per query (configurable up to 16)"),
]

for label, value in tech_items:
    st.markdown(
        f"""
        <div style="display:flex; gap:1rem; margin-bottom:0.5rem; align-items:baseline;">
            <span style="font-family:'Playfair Display',serif; color:#4A7C59; min-width:180px;">
                {label}
            </span>
            <span style="font-family:'Lato',sans-serif; color:#3A3A3A;">{value}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Design system
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>Design System</h3>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p style="font-family:'Lato',sans-serif; color:#3A3A3A; line-height:1.7;">
        <strong>Theme:</strong> Sandalwood &amp; Sage<br>
        <strong>Primary colour:</strong> Forest green #4A7C59<br>
        <strong>Accent:</strong> Sandalwood gold #8B6914<br>
        <strong>Background:</strong> #F8F9F5 &nbsp;·&nbsp; Secondary: #EDF3EC<br>
        <strong>Fonts:</strong> Playfair Display (headings), Lato (body),
        Cormorant Garamond (Sanskrit / quotes)<br>
        <strong>Sanskrit:</strong> All diacritical marks preserved throughout
    </p>
    """,
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
