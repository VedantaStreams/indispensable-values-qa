"""
pages/6_Get_the_App.py — Access and sharing instructions.
"""

import streamlit as st
from src.page_header import render_header

st.set_page_config(
    page_title="Get the App · Indispensable Values Q&A",
    page_icon="📲",
    layout="wide",
)

render_header("Get the App")

st.markdown(
    """
    <h3 style="font-family:'Playfair Display',serif; color:#4A7C59;">Accessing This App</h3>
    <p style="font-family:'Lato',sans-serif; color:#3A3A3A; line-height:1.8;">
        <strong>Indispensable Values Q&amp;A</strong> is a web app accessible from any device
        with a modern browser — desktop, tablet, or mobile. No installation is required.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Access methods
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>How to Access</h3>",
    unsafe_allow_html=True,
)

access_methods = [
    (
        "🌐 Web Browser",
        "Open the app URL in any browser (Chrome, Firefox, Safari, Edge). "
        "Bookmark it for quick access.",
    ),
    (
        "📱 Mobile",
        "On iOS: tap Share → Add to Home Screen for an app-like shortcut. "
        "On Android: tap ⋮ → Add to Home Screen.",
    ),
    (
        "💻 Self-Hosting",
        "Clone the repository from GitHub, install requirements with "
        "`pip install -r requirements.txt`, configure `.streamlit/secrets.toml` "
        "with your OpenAI key and admin password, then run `streamlit run Home.py`.",
    ),
]

for icon_title, desc in access_methods:
    st.markdown(
        f"""
        <div style="
            background:#EDF3EC; border-left:4px solid #4A7C59;
            border-radius:8px; padding:0.8rem 1.2rem; margin-bottom:0.8rem;
        ">
            <strong style="font-family:'Playfair Display',serif; color:#4A7C59;">{icon_title}</strong>
            <p style="font-family:'Lato',sans-serif; font-size:0.9rem; color:#444;
                      margin:0.3rem 0 0 0; line-height:1.7;">
                {desc}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sharing
# ---------------------------------------------------------------------------
st.markdown(
    "<h3 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>Sharing with Fellow Seekers</h3>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p style="font-family:'Lato',sans-serif; color:#3A3A3A; line-height:1.8;">
        Please share this app freely with Chinmaya Mission students, Bala Vihar teachers,
        Vedānta study group members, and any sincere seekers of the Gītā's wisdom.
        The app is meant to support <em>śravaṇam</em> (listening / studying) and
        <em>mananam</em> (reflection) of the 20 Indispensable Values.
    </p>
    <p style="font-family:'Lato',sans-serif; color:#3A3A3A; line-height:1.8;">
        This is a study companion — not a substitute for the living Guru,
        personal sādhana, or attending Swamiji's discourses.
        Always use this app in the spirit of devotion and sincerity.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Setup secrets note
# ---------------------------------------------------------------------------
with st.expander("⚙️ Self-Hosting: Configuring secrets", expanded=False):
    st.markdown(
        """
        Create `.streamlit/secrets.toml` with:
        ```toml
        OPENAI_API_KEY = "sk-..."
        ADMIN_PASSWORD = "your-admin-password"
        ```
        This file is gitignored and should never be committed to version control.
        """,
    )

st.markdown(
    """
    <div style='text-align:center; font-family:"Lato",sans-serif; font-size:0.8rem; color:#888; margin-top:2rem;'>
        Built with reverence · Chinmaya Mission · Bhagavad Gītā Chapter 13
    </div>
    """,
    unsafe_allow_html=True,
)
