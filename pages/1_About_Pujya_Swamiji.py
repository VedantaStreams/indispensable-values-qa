"""
pages/1_About_Pujya_Swamiji.py — Bio of Swāmī Aparājitānandajī.
"""

import streamlit as st
from src.page_header import render_header

st.set_page_config(
    page_title="About Pūjya Swamiji · Indispensable Values Q&A",
    page_icon="📖",
    layout="wide",
)

render_header("About Pūjya Swāmī Aparājitānandajī")

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown(
        """
        <div style="text-align:center; padding:1rem;">
            <div style="
                width:200px; height:250px; margin:auto; border-radius:12px;
                background: linear-gradient(135deg, #FFB6C1 0%, #D4A017 100%);
                display:flex; align-items:center; justify-content:center;
                font-size:4rem; color:white;
            ">🙏</div>
            <p style="
                font-family:'Cormorant Garamond',serif; font-size:0.9rem;
                color:#8B6914; margin-top:0.6rem;
            ">Pūjya Swāmī Aparājitānandajī<br>Chinmaya Mission</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <h3 style="font-family:'Playfair Display',serif; color:#4A7C59;">Swāmī Aparājitānandajī</h3>
        <p style="font-family:'Lato',sans-serif; font-size:1rem; color:#3A3A3A; line-height:1.8;">
            Pūjya Swāmī Aparājitānandajī is a revered teacher and monk of
            <strong>Chinmaya Mission</strong>, the global Vedānta movement founded by
            Swāmī Chinmayānanda. With deep scholarship in Bhagavad Gītā, Upaniṣads, and
            Vedāntic philosophy, Swamiji has dedicated His life to making the profound
            wisdom of Sanātana Dharma accessible to sincere seekers worldwide.
        </p>
        <p style="font-family:'Lato',sans-serif; font-size:1rem; color:#3A3A3A; line-height:1.8;">
            Swamiji is the author of <em>Indispensable Values</em> (2022), a 320-page
            exposition of the 20 jñāna sādhana from Bhagavad Gītā Chapter 13, verses 7–11.
            His unique gift lies in illuminating ancient wisdom through contemporary stories,
            modern examples, and the compassionate voice of a true Guru.
        </p>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Key works
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>Key Teachings & Works</h3>",
    unsafe_allow_html=True,
)

works = [
    (
        "📚 Indispensable Values (2022)",
        "320-page exposition of the 20 jñāna sādhana — "
        "the knowledge-values prescribed in Bhagavad Gītā 13.7–11.",
    ),
    (
        "🎙️ Value of Values — Discourse Series",
        "8-part video discourse series exploring each value in depth with stories and scriptural analysis.",
    ),
    (
        "🎙️ Bhagavad Gītā Chapter 13 — Discourse Series",
        "Detailed verse-by-verse exposition of the Kṣetra-Kṣetrajña chapter.",
    ),
    (
        "📖 Value Based Stories for All",
        "6-part discourse series presenting value-illuminating stories accessible to all ages.",
    ),
]

for title, desc in works:
    st.markdown(
        f"""
        <div style="
            background:#EDF3EC; border-left:4px solid #4A7C59;
            border-radius:8px; padding:0.8rem 1.2rem; margin-bottom:0.8rem;
        ">
            <strong style="font-family:'Playfair Display',serif; color:#4A7C59;">{title}</strong>
            <p style="font-family:'Lato',sans-serif; font-size:0.9rem; color:#444; margin:0.3rem 0 0 0;">
                {desc}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# About Chinmaya Mission
# ---------------------------------------------------------------------------
st.markdown(
    """
    <h3 style="font-family:'Playfair Display',serif; color:#4A7C59;">Chinmaya Mission</h3>
    <p style="font-family:'Lato',sans-serif; font-size:1rem; color:#3A3A3A; line-height:1.8;">
        Founded in 1953 by Swāmī Chinmayānanda, Chinmaya Mission is a worldwide
        spiritual and cultural organisation dedicated to the dissemination of Advaita Vedānta.
        With centres in over 50 countries, the Mission provides systematic Vedāntic education
        through Bala Vihar, Yuva Kendra, study groups, and resident camps.
        Learn more at <a href="https://www.chinmayamission.com" target="_blank"
        style="color:#4A7C59;">chinmayamission.com</a>.
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
