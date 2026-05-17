"""
pages/6_Get_the_App.py — How to access and share the app.
"""

import streamlit as st

import sys
from pathlib import Path
import sys
from pathlib import Path as _Path
_ROOT = _Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from src.page_header import render_om_symbol, render_page_quote

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="Get the App | Indispensable Values",
    page_icon="📱",
    layout="wide",
)

render_om_symbol()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,600&family=Lato:wght@300;400;700&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&display=swap');

[data-testid="stImage"] {
    margin-bottom:-1.5rem!important;
    padding-bottom:0!important;
    line-height:0!important;
}
[data-testid="stImage"] img {
    display:block!important;
}

html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#F8F9F5;color:#1A3A28;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#2A5C3A!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#EDF3EC,#E0EBE2)!important;border-right:2px solid #B8D4BC;}
div[data-testid="stSidebar"] *{color:#2A4A38!important;font-weight:600!important;}

.page-header{background:linear-gradient(135deg,#EDF3EC,#E4EDE4);border:2px solid #B8D4BC;border-radius:18px;padding:2.5rem;text-align:center;margin-bottom:2rem;box-shadow:0 4px 20px rgba(74,124,89,.08);}
.page-header-title{font-family:'Playfair Display',serif;font-size:2.4rem;font-weight:800;color:#2A5C3A;}
.page-header-sub{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.2rem;color:#4A7C59;}

.access-card{background:white;border:2px solid #B8D4BC;border-radius:16px;padding:2rem;margin-bottom:1.5rem;box-shadow:0 4px 16px rgba(74,124,89,.07);text-align:center;}
.access-icon{font-size:3rem;margin-bottom:.8rem;}
.access-title{font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;color:#2A5C3A;margin-bottom:.5rem;}
.access-desc{color:#1A3A28;font-size:.93rem;line-height:1.8;margin-bottom:1rem;}
.access-url{background:#EDF3EC;border:1.5px solid #B8D4BC;border-radius:10px;padding:.8rem 1.2rem;font-family:'Lato',monospace;font-size:.9rem;color:#2A5C3A;font-weight:700;letter-spacing:.3px;margin-bottom:.8rem;}

.step-card{display:flex;align-items:flex-start;gap:1rem;background:#EDF3EC;border:1.5px solid #B8D4BC;border-radius:12px;padding:1rem 1.3rem;margin-bottom:.7rem;}
.step-num{font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:800;color:#4A7C59;min-width:36px;}
.step-text{color:#1A3A28;font-size:.92rem;line-height:1.65;}

.section-card{background:white;border:1.5px solid #B8D4BC;border-radius:14px;padding:1.8rem;margin-bottom:1.5rem;box-shadow:0 2px 10px rgba(74,124,89,.06);}
.section-title{font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700;color:#2A5C3A;margin:2rem 0 1rem;padding-bottom:.4rem;border-bottom:2px solid #B8D4BC;}
.body-para{color:#1A3A28;font-size:.95rem;line-height:1.9;margin-bottom:.9rem;}

.platform-item{display:flex;align-items:center;gap:.8rem;margin-bottom:.7rem;}
.platform-icon{font-size:1.5rem;flex-shrink:0;}
.platform-text{color:#1A3A28;font-size:.92rem;line-height:1.6;}
.platform-text strong{color:#2A5C3A;}

.coming-soon{display:inline-block;background:#EDF3EC;border:1.5px solid #B8D4BC;color:#4A7C59;border-radius:20px;padding:.2rem .8rem;font-size:.78rem;font-weight:700;margin-left:.5rem;vertical-align:middle;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <div style="font-size:2.5rem;margin-bottom:.5rem;">📱</div>
    <div class="page-header-title">Get the App</div>
    <div class="page-header-sub">Access Indispensable Values Q&amp;A anytime, anywhere</div>
</div>
""", unsafe_allow_html=True)


render_page_quote(
    "Remember, in life, the <strong>only permanent relationship</strong> is our relationship with <strong>God</strong>."
)
# ── Web Access ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Access the App</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="access-card">
        <div class="access-icon">🌐</div>
        <div class="access-title">Web Browser</div>
        <div class="access-desc">
            Access the app directly in any web browser —
            on desktop, laptop, tablet, or mobile phone.
            No download or installation required.
        </div>
        <div class="access-url">Coming Soon</div>
        <div style="font-family:'Cormorant Garamond',serif;font-style:italic;
            font-size:.88rem;color:#4A6B54;">
            The app will be accessible at a dedicated URL once deployed.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="access-card">
        <div class="access-icon">📱</div>
        <div class="access-title">Mobile Phone</div>
        <div class="access-desc">
            Open the app URL in <strong>Safari</strong> (iPhone/iPad) or
            <strong>Chrome</strong> (Android). For the best experience,
            add it to your Home Screen as a shortcut.
        </div>
        <div style="margin-top:.8rem;font-family:'Cormorant Garamond',serif;
            font-style:italic;font-size:.9rem;color:#3A5040;">
            On iPhone: Open in Safari → Share → Add to Home Screen<br>
            On Android: Open in Chrome → Menu → Add to Home Screen
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── How to Get Started ─────────────────────────────────────────────────────────
st.markdown('<div class="section-title">How to Get Started</div>', unsafe_allow_html=True)

steps = [
    ("Open the app", "Visit the app URL in your web browser on any device."),
    ("Go to Indispensable Values Q&A",
     "Click <strong>Indispensable Values Q&A</strong> in the left sidebar."),
    ("Ask your first question",
     "Type a question about any of the 20 Indispensable Values in the chat box. "
     "Or click one of the sample questions to get started instantly."),
    ("Read the answer",
     "The answer will include the teaching, a scriptural connection, a reflection, "
     "and the exact source it came from."),
    ("Download if needed",
     "Use the TXT, PDF, or DOCX download buttons to save the conversation "
     "for study or sharing."),
]

for i, (title, desc) in enumerate(steps, 1):
    st.markdown(f"""
    <div class="step-card">
        <div class="step-num">{i}</div>
        <div class="step-text"><strong>{title}</strong><br>{desc}</div>
    </div>""", unsafe_allow_html=True)

# ── Share the App ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Share with Fellow Seekers</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="section-card">
    <div class="body-para">
        This app is designed to be shared freely with anyone who wishes to study
        Swamiji's teachings on the Indispensable Values. Share the app link with:
    </div>
""", unsafe_allow_html=True)

platforms = [
    ("🏛️", "Satsang groups and study circles",
     "Perfect for group study — ask a question before satsang and bring the answer for discussion."),
    ("🎓", "Vedānta students and seekers",
     "A study companion for anyone going through the Value of Values discourse series."),
    ("👨‍👩‍👧", "Families and Balavihar parents",
     "The stories and practical reflections make values accessible for all ages."),
    ("📲", "WhatsApp and community groups",
     "Simply share the app URL — it works instantly in any mobile browser."),
]

for icon, title, desc in platforms:
    st.markdown(f"""
    <div class="platform-item">
        <div class="platform-icon">{icon}</div>
        <div class="platform-text"><strong>{title}</strong> — {desc}</div>
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── What's Coming ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">What\'s Coming</div>', unsafe_allow_html=True)

st.markdown("""
<div class="section-card">
    <div class="platform-item">
        <div class="platform-icon">📹</div>
        <div class="platform-text">
            <strong>More of Swamiji's talks</strong> — expanding the knowledge base
            with additional playlists and discourse series
        </div>
    </div>
    <div class="platform-item">
        <div class="platform-icon">🔍</div>
        <div class="platform-text">
            <strong>Advanced search and filtering</strong> — search by value name,
            story type, or scripture reference
        </div>
    </div>
    <div class="platform-item">
        <div class="platform-icon">🌐</div>
        <div class="platform-text">
            <strong>Multi-language support</strong> — answers in additional Indian
            languages <span class="coming-soon">Planned</span>
        </div>
    </div>
    <div class="platform-item">
        <div class="platform-icon">🎙️</div>
        <div class="platform-text">
            <strong>Voice input</strong> — ask questions by speaking
            <span class="coming-soon">Planned</span>
        </div>
    </div>
    <div class="platform-item">
        <div class="platform-icon">💬</div>
        <div class="platform-text">
            <strong>Ask Swamiji</strong> — a full 600-video knowledge base covering
            all of Swamiji's YouTube talks
            <span class="coming-soon">Coming</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:2rem;padding:1.5rem;
    border-top:2px solid #B8D4BC;color:#4A6B54;
    font-family:'Cormorant Garamond',serif;font-style:italic;font-size:.95rem;">
    🪷 &nbsp; Hari Om &nbsp; 🪷 <br>
    <em>May this tool serve every sincere seeker on the path of knowledge.</em>
</div>
""", unsafe_allow_html=True)
