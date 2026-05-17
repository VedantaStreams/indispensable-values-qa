"""
pages/0_Gratitude_and_Reverence.py — Devotional page honouring the Guru Paramparā.
"""

import streamlit as st
from src.page_header import render_header

st.set_page_config(page_title="Gratitude & Reverence · Indispensable Values Q&A", page_icon="🙏", layout="wide")

render_header("Gratitude & Reverence")

st.markdown(
    """
    <div style="text-align:center; margin-bottom:1.5rem;">
        <span style="font-size:3rem;">🙏</span>
        <h2 style="font-family:'Playfair Display',serif; color:#4A7C59;">
            Guru Paramparā — The Lineage of Light
        </h2>
        <p style="font-family:'Cormorant Garamond',serif; font-size:1.2rem; color:#8B6914;">
            <em>Gurur Brahmā, Gurur Viṣṇuḥ, Gurur Devo Maheśvaraḥ<br>
            Guruḥ Sākṣāt Parabrahma, Tasmai Śrī Gurave Namaḥ</em>
        </p>
        <p style="font-family:'Lato',sans-serif; font-size:0.9rem; color:#555;">
            The Guru is Brahmā, the Guru is Viṣṇu, the Guru is Maheśvara;<br>
            The Guru is verily the Supreme Brahman — salutations to that revered Guru.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Paramparā section
# ---------------------------------------------------------------------------
st.markdown(
    """
    <h3 style="font-family:'Playfair Display',serif; color:#4A7C59;">The Chinmaya Mission Lineage</h3>
    """,
    unsafe_allow_html=True,
)

lineage = [
    ("Ādi Śaṅkarācārya", "The great Advaitin who systematised Vedānta and revived Sanātana Dharma."),
    ("Swāmī Tapovanam", "The Himalayan sage and Guru of Swāmī Chinmayānanda."),
    ("Swāmī Chinmayānanda", "Founder of Chinmaya Mission; brought Vedānta to the masses worldwide."),
    ("Swāmī Tejomayananda", "Head of Chinmaya Mission worldwide; prolific teacher and author."),
    ("Pūjya Swāmī Aparājitānandajī", "Author of 'Indispensable Values'; teacher of the 20 jñāna sādhana."),
]

for name, desc in lineage:
    st.markdown(
        f"""
        <div style="
            background:#EDF3EC; border-left:4px solid #8B6914;
            border-radius:8px; padding:0.8rem 1.2rem; margin-bottom:0.8rem;
        ">
            <strong style="font-family:'Playfair Display',serif; color:#4A7C59;">{name}</strong>
            <p style="font-family:'Lato',sans-serif; font-size:0.9rem; color:#444; margin:0.2rem 0 0 0;">{desc}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Invocation
# ---------------------------------------------------------------------------
st.markdown(
    """
    <h3 style="font-family:'Playfair Display',serif; color:#4A7C59;">Invocation</h3>
    <div style="
        background:#F8F9F5; border:1px solid #4A7C59; border-radius:12px;
        padding:1.5rem 2rem; margin-bottom:1.5rem; text-align:center;
    ">
        <p style="font-family:'Cormorant Garamond',serif; font-size:1.3rem; color:#3A3A3A; line-height:1.8;">
            <em>
            Om saha nāvavatu · saha nau bhunaktu<br>
            Saha vīryaṃ karavāvahai<br>
            Tejasvi nāvadhītam astu · mā vidviṣāvahai<br>
            Om śāntiḥ śāntiḥ śāntiḥ
            </em>
        </p>
        <p style="font-family:'Lato',sans-serif; font-size:0.85rem; color:#888;">
            May we be protected together, may we be nourished together,<br>
            may we work with great energy together.<br>
            May our study be enlightening. May there be no conflict between us.<br>
            Om Peace, Peace, Peace.
        </p>
    </div>
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
