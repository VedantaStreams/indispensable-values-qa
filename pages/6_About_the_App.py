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

html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#E8F4F6;color:#0A1E28;font-weight:500;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#062E3A!important;font-weight:800!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#FFFFFF,#A8D8E0)!important;border-right:2px solid #88C5D0;}
div[data-testid="stSidebar"] *{color:#0A1E28!important;font-weight:600!important;}

.swamiji-quote{background:linear-gradient(135deg,#FFFFFF,#E8F4F6);border-left:5px solid #0D5C6B;border-radius:0 14px 14px 0;padding:1.2rem 1.8rem;margin:1rem 0;font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.08rem;color:#0A1E28;line-height:1.8;}
.swamiji-quote-attr{font-family:'Lato',sans-serif;font-style:normal;font-size:.78rem;font-weight:700;color:#0D5C6B;letter-spacing:.5px;margin-top:.5rem;}
.page-header{background:linear-gradient(135deg,#FFFFFF,#D0EDF1);border:2px solid #88C5D0;border-radius:18px;padding:2.5rem;text-align:center;margin-bottom:2rem;box-shadow:0 4px 20px rgba(0,0,0,.08);}
.page-header-title{font-family:'Playfair Display',serif;font-size:2.4rem;font-weight:800;color:#062E3A;}
.page-header-sub{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.2rem;color:#0D5C6B;}

.feature-card{background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:14px;padding:1.6rem;margin-bottom:1rem;box-shadow:0 2px 10px rgba(0,0,0,.06);height:100%;}
.feature-icon{font-size:2.2rem;margin-bottom:.6rem;}
.feature-title{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:#062E3A;margin-bottom:.5rem;}
.feature-desc{color:#0A1E28;font-size:.92rem;line-height:1.75;}

.section-card{background:#FFFFFF;border:2px solid #88C5D0;border-radius:16px;padding:2rem;margin-bottom:1.5rem;box-shadow:0 4px 16px rgba(0,0,0,.07);}
.section-title{font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:700;color:#062E3A;margin:2rem 0 1rem;padding-bottom:.4rem;border-bottom:2px solid #88C5D0;}
.body-para{color:#0A1E28;font-size:.95rem;line-height:1.9;margin-bottom:.9rem;}

.flow-step{display:flex;align-items:flex-start;gap:1rem;background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:12px;padding:1rem 1.3rem;margin-bottom:.7rem;}
.flow-num{font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:800;color:#0D5C6B;min-width:36px;}
.flow-text{color:#0A1E28;font-size:.92rem;line-height:1.65;}
.flow-text strong{color:#062E3A;}

.unique-item{display:flex;align-items:flex-start;gap:.8rem;margin-bottom:.8rem;}
.unique-bullet{color:#0D5C6B;font-size:1.2rem;flex-shrink:0;}
.unique-text{color:#0A1E28;font-size:.93rem;line-height:1.7;}
.unique-text strong{color:#062E3A;}

.tech-badge{display:inline-block;background:#FFFFFF;border:1.5px solid #88C5D0;color:#062E3A;border-radius:20px;padding:.25rem .9rem;font-size:.83rem;margin:.2rem;font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:600;}

.quote-block{background:linear-gradient(135deg,#FFFFFF,#E8F4F6);border-left:5px solid #0D5C6B;border-radius:0 12px 12px 0;padding:1.2rem 1.5rem;margin:1.2rem 0;font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.1rem;color:#062E3A;line-height:1.8;}

.om-box-pg{
    background:linear-gradient(135deg,#D0EDF1,#B8E4EC);
    border:2px solid #1A7A8C;border-radius:16px;
    width:90px;height:90px;
    display:inline-flex;align-items:center;justify-content:center;
    margin-bottom:.8rem;
    box-shadow:0 4px 16px rgba(26,122,140,.15);
}
.om-box-pg img{width:70px;height:70px;object-fit:contain;border-radius:10px;}
.swamiji-quote-pg{
    text-align:center;max-width:780px;margin:.5rem auto 1.8rem;
    font-family:'Cormorant Garamond',serif;font-style:italic;
    font-size:1.35rem;font-weight:700;color:#03202A;
    line-height:1.75;padding:0 1.5rem;
}
.swamiji-quote-pg-attr{display:block;font-family:'Playfair Display',serif;
    font-style:normal;font-size:1rem;font-weight:700;
    color:#0D5C6B;margin-top:.7rem;}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="swamiji-quote-pg">
    &ldquo;<strong>True happiness</strong> shouldn&rsquo;t be because of! <strong>True happiness</strong> should be in spite of!&rdquo;
    <span class="swamiji-quote-pg-attr">— Swāmī Aparājitānanda</span>
</div>
""", unsafe_allow_html=True)
# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="om-box-pg"><img src="data:image/jpeg;base64,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" alt="Om"/></div>
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
        that answers your questions about Bhagavad Gītā <strong>Chapters 13 and 16</strong> —
        the 20 indispensable values (jñāna sādhana) and the divine vs demoniac qualities
        (daivī sampat &amp; āsurī sampat) — drawing exclusively from the authentic
        teachings of <strong>Swāmī Aparājitānanda</strong>.
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
        Bhagavān declares these virtues as Knowledge itself —
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
            Chapters 13 and 16 discourses, and Swamiji's published works</strong>
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
        The knowledge base is built from Swāmī Aparājitānanda's authentic teachings:
    </div>
""", unsafe_allow_html=True)

sources = [
    ("📹", "Bhagavad Gītā Chapter 13 — 7 Discourses",
     "Complete transcripts of Swamiji's 7-discourse series unfolding the 20 Indispensable Values (jñāna sādhana) from BG 13.7–11"),
    ("📹", "Bhagavad Gītā Chapter 16 — 7 Discourses",
     "Swamiji's 7-discourse series on Daivī Sampat & Āsurī Sampat — the divine vs demoniac qualities from BG 16"),
    ("📹", "Value of Values — 8 Full Discourses",
     "Earlier 8-discourse series by Swamiji covering all 20 Indispensable Values from BG 13.7–11"),
    ("🏕️", "Value Based Stories for All — 6 Discourses",
     "Heart-touching real-life stories told at children's summer camps, illustrating each value through narrative"),
    ("📖", "Indispensable Values — Book (2022)",
     "Swamiji's published book covering 37 values from BG Chapters 13 and 16 — 320 pages of authoritative teaching"),
    ("📖", "Gurudev's Quotes — Volumes I, II, III",
     "Selected quotes from Pūjya Swāmī Chinmayānanda compiled by Swāmī Aparājitānanda"),
    ("📖", "Read Daily, Live Fully",
     "Daily spiritual companion by Swāmī Aparājitānanda for seekers"),
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
    <div class="swamiji-quote-attr">— Swāmī Aparājitānanda</div>
</div>
''', unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:2rem;padding:1.5rem;
    border-top:2px solid #88C5D0;color:#B8956B;
    font-family:'Cormorant Garamond',serif;font-style:italic;font-size:.95rem;">
    🪷 &nbsp; Hari Om &nbsp; 🪷 <br>
    <em>Built with devotion · Grounded in authentic teachings · For sincere seekers</em>
</div>
""", unsafe_allow_html=True)
