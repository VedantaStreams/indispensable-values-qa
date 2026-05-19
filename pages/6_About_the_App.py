"""
pages/4_About_the_App.py — What this app does and what makes it unique.
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
    page_title="About the App | Indispensable Values",
    page_icon="✨",
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

.swamiji-quote{background:linear-gradient(135deg,#EDF3EC,#F8F9F5);border-left:5px solid #4A7C59;border-radius:0 14px 14px 0;padding:1.2rem 1.8rem;margin:1rem 0;font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.08rem;color:#2A4A38;line-height:1.8;}
.swamiji-quote-attr{font-family:'Lato',sans-serif;font-style:normal;font-size:.78rem;font-weight:700;color:#4A7C59;letter-spacing:.5px;margin-top:.5rem;}
.page-header{background:linear-gradient(135deg,#EDF3EC,#E4EDE4);border:2px solid #B8D4BC;border-radius:18px;padding:2.5rem;text-align:center;margin-bottom:2rem;box-shadow:0 4px 20px rgba(74,124,89,.08);}
.page-header-title{font-family:'Playfair Display',serif;font-size:2.4rem;font-weight:800;color:#2A5C3A;}
.page-header-sub{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.2rem;color:#4A7C59;}

.feature-card{background:white;border:1.5px solid #B8D4BC;border-radius:14px;padding:1.6rem;margin-bottom:1rem;box-shadow:0 2px 10px rgba(74,124,89,.06);height:100%;}
.feature-icon{font-size:2.2rem;margin-bottom:.6rem;}
.feature-title{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:#2A5C3A;margin-bottom:.5rem;}
.feature-desc{color:#1A3A28;font-size:.92rem;line-height:1.75;}

.section-card{background:white;border:2px solid #B8D4BC;border-radius:16px;padding:2rem;margin-bottom:1.5rem;box-shadow:0 4px 16px rgba(74,124,89,.07);}
.section-title{font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:700;color:#2A5C3A;margin:2rem 0 1rem;padding-bottom:.4rem;border-bottom:2px solid #B8D4BC;}
.body-para{color:#1A3A28;font-size:.95rem;line-height:1.9;margin-bottom:.9rem;}

.flow-step{display:flex;align-items:flex-start;gap:1rem;background:#EDF3EC;border:1.5px solid #B8D4BC;border-radius:12px;padding:1rem 1.3rem;margin-bottom:.7rem;}
.flow-num{font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:800;color:#4A7C59;min-width:36px;}
.flow-text{color:#1A3A28;font-size:.92rem;line-height:1.65;}
.flow-text strong{color:#2A5C3A;}

.unique-item{display:flex;align-items:flex-start;gap:.8rem;margin-bottom:.8rem;}
.unique-bullet{color:#4A7C59;font-size:1.2rem;flex-shrink:0;}
.unique-text{color:#1A3A28;font-size:.93rem;line-height:1.7;}
.unique-text strong{color:#2A5C3A;}

.tech-badge{display:inline-block;background:#EDF3EC;border:1.5px solid #B8D4BC;color:#2A5C3A;border-radius:20px;padding:.25rem .9rem;font-size:.83rem;margin:.2rem;font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:600;}

.quote-block{background:linear-gradient(135deg,#EDF3EC,#F8F9F5);border-left:5px solid #4A7C59;border-radius:0 12px 12px 0;padding:1.2rem 1.5rem;margin:1.2rem 0;font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.1rem;color:#2A5C3A;line-height:1.8;}
</style>
""", unsafe_allow_html=True)


render_page_quote(
    "That which is <strong>infinite, all-pervading</strong> cannot have a form. But for the sake of the devotee, Bhagawān <strong>takes up a form</strong>."
)
# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div style="font-size:2.5rem;margin-bottom:.5rem;">✨</div>
    <div class="page-header-title">About This App</div>
    <div class="page-header-sub">
        A reverential AI-powered study companion for Indispensable Values
    </div>
</div>
""", unsafe_allow_html=True)

# ── What Does It Do ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">What Does This App Do?</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="section-card">
    <div class="body-para">
        <strong>Indispensable Values Q&amp;A</strong> is an AI-powered study companion
        that answers your questions about the Indispensable Values of Bhagavad Gītā
        Chapter 13 — drawing exclusively from the authentic teachings of
        <strong>Swāmī Aparājitānandajī</strong>.
    </div>
    <div class="body-para">
        Ask a question. Get a grounded answer — with the source cited, the scripture
        referenced, and a gentle reflection to carry into your daily life. Every answer
        comes directly from Swamiji's talks, transcripts, and published writings.
        Nothing is invented. Nothing is fabricated.
    </div>
    <div class="quote-block">
        "etat jñānam iti proktam — This is declared to be Knowledge."
        &nbsp;—&nbsp; Bhagavad Gītā 13.12<br><br>
        <span style="font-size:.9rem;">
        Bhagavān declares these 20 virtues as Knowledge itself —
        and this app exists to help seekers understand and live them.
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── How It Works ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">How Does It Work?</div>',
            unsafe_allow_html=True)

steps = [
    ("You ask a question",
     "Type any question about the Indispensable Values — for example, "
     "<em>'What is amānitvam?'</em> or <em>'How does Swamiji explain kṣāntiḥ?'</em>"),
    ("The app searches the knowledge base",
     "Your question is matched against thousands of chunks from Swamiji's talks, "
     "transcripts, stories, and book — using AI-powered semantic search."),
    ("Relevant teachings are retrieved",
     "The most relevant passages are retrieved from the knowledge base — "
     "including timestamps, page numbers, and source titles."),
    ("The AI composes a grounded answer",
     "Only the retrieved content is used to compose the answer. "
     "The AI is strictly forbidden from inventing or hallucinating."),
    ("Sources are cited",
     "Every answer shows exactly which talk, which page, or which timestamp "
     "the answer came from — so you can go back to the original source."),
]

for i, (title, desc) in enumerate(steps, 1):
    st.markdown(f"""
    <div class="flow-step">
        <div class="flow-num">{i}</div>
        <div class="flow-text"><strong>{title}</strong><br>{desc}</div>
    </div>""", unsafe_allow_html=True)

# ── What Makes It Unique ───────────────────────────────────────────────────────
st.markdown('<div class="section-title">What Makes This App Unique?</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="section-card">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Grounded in Authentic Sources</div>
        <div class="feature-desc">
            Unlike a general AI chatbot, this app <strong>only answers from
            Swamiji's actual teachings</strong>. It never draws on outside
            knowledge, never invents quotes, and never fabricates scripture
            references. If the answer isn't in the knowledge base, it says so
            clearly and gently.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="section-card">
        <div class="feature-icon">🪷</div>
        <div class="feature-title">Sanskrit Terms Preserved</div>
        <div class="feature-desc">
            The app preserves all Sanskrit terms exactly as Swamiji uses them —
            <em>amānitvam, adambhitvam, ahiṃsā, kṣāntiḥ, ārjavam</em> — with
            their diacritical marks intact. Seekers can study in the authentic
            language of the tradition, not a diluted transliteration.
        </div>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="section-card">
        <div class="feature-icon">📚</div>
        <div class="feature-title">Multiple Source Types</div>
        <div class="feature-desc">
            The knowledge base draws from <strong>video talk transcripts,
            value-based stories from children's summer camps, Bhagavad Gītā
            Chapter 13 discourses, and Swamiji's published book</strong>
            — giving answers that are both philosophically deep and
            practically illustrated.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="section-card">
        <div class="feature-icon">🛡️</div>
        <div class="feature-title">Built-In Guardrails</div>
        <div class="feature-desc">
            The app has strict guardrails — it <strong>will not invent Swamiji's
            words</strong>, will not answer disrespectful questions, and will
            always maintain a reverential and devotional tone. It is designed
            to serve sincere seekers, not casual curiosity.
        </div>
    </div>
    """, unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    st.markdown("""
    <div class="section-card">
        <div class="feature-icon">🙏</div>
        <div class="feature-title">Reverential Tone</div>
        <div class="feature-desc">
            Every answer is structured for study, reflection, and note-taking —
            with a clear <strong>Answer, Relevant Teaching, Scriptural
            Connection, Reflection, and Sources</strong> section. Suitable
            for satsang preparation, personal study, and spiritual journalling.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="section-card">
        <div class="feature-icon">💾</div>
        <div class="feature-title">Download Your Chat</div>
        <div class="feature-desc">
            Every conversation can be <strong>downloaded as a TXT, PDF, or
            DOCX file</strong> — making it easy to save Swamiji's teachings
            for later study, share with fellow seekers, or use in
            study groups and satsangs.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Knowledge Base ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">What Is in the Knowledge Base?</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="section-card">
    <div class="body-para">
        The knowledge base is built from Swāmī Aparājitānandajī's authentic teachings:
    </div>
""", unsafe_allow_html=True)

sources = [
    ("📹", "Value of Values — 8 Full Discourses",
     "Complete transcripts of Swamiji's 8-discourse series covering all 20 Indispensable Values from BG 13.7–11"),
    ("📹", "Bhagavad Gītā Chapter 13 — 2 Discourses",
     "Swamiji's in-depth exposition of Kṣetra, Kṣetrajña, and why these values prepare the mind for self-knowledge"),
    ("🏕️", "Value Based Stories for All — 6 Discourses",
     "Heart-touching real-life stories told at children's summer camps, illustrating each value through narrative"),
    ("📖", "Indispensable Values — Book (2022)",
     "Swamiji's published book covering 37 values from BG Chapters 13 and 16 — 320 pages of authoritative teaching"),
]

for icon, title, desc in sources:
    st.markdown(f"""
    <div class="unique-item">
        <div class="unique-bullet">{icon}</div>
        <div class="unique-text"><strong>{title}</strong><br>{desc}</div>
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Technology ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Technology Behind the App</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="section-card">
    <div class="body-para">
        This app uses <strong>Retrieval-Augmented Generation (RAG)</strong> —
        a method where the AI retrieves relevant passages from the knowledge base
        before composing an answer. This ensures answers are always grounded in
        the actual source material, not generated from general AI training data.
    </div>
    <div style="margin-top:.8rem;">
        <span class="tech-badge">Retrieval-Augmented Generation</span>
        <span class="tech-badge">ChromaDB Vector Database</span>
        <span class="tech-badge">OpenAI Embeddings</span>
        <span class="tech-badge">GPT-4o-mini</span>
        <span class="tech-badge">Semantic Search</span>
        <span class="tech-badge">Streamlit</span>
        <span class="tech-badge">Verse-aware Chunking</span>
        <span class="tech-badge">Sanskrit Preservation</span>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown('''
<div class="swamiji-quote">
    &ldquo;That which is infinite, all-pervading cannot have a form. But for the sake of
    the devotee, Bhagawān takes up a form. Just like formless water takes a particular
    form when cooled below 0°. In the same way, formless God takes a form under the
    extreme devotion of devotees.&rdquo;
    <div class="swamiji-quote-attr">— Swāmī Aparājitānandajī</div>
</div>
''', unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:2rem;padding:1.5rem;
    border-top:2px solid #B8D4BC;color:#4A6B54;
    font-family:'Cormorant Garamond',serif;font-style:italic;font-size:.95rem;">
    🪷 &nbsp; Hari Om &nbsp; 🪷 <br>
    <em>Built with devotion · Grounded in authentic teachings · For sincere seekers</em>
</div>
""", unsafe_allow_html=True)
