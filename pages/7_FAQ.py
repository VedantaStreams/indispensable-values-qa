"""
pages/5_FAQ.py — Frequently Asked Questions.
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
    page_title="FAQ | Indispensable Values",
    page_icon="❓",
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

html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#2A0F0F;color:#F5E6C8;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#D4AF37!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#4A1F1F,#6A2828)!important;border-right:2px solid #8B3A2E;}
div[data-testid="stSidebar"] *{color:#F5E6C8!important;font-weight:600!important;}

.page-header{background:linear-gradient(135deg,#4A1F1F,#5A2424);border:2px solid #8B3A2E;border-radius:18px;padding:2.5rem;text-align:center;margin-bottom:2rem;box-shadow:0 4px 20px rgba(0,0,0,.08);}
.page-header-title{font-family:'Playfair Display',serif;font-size:2.4rem;font-weight:800;color:#D4AF37;}
.page-header-sub{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.2rem;color:#C0392B;}

.faq-q{font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:700;color:#D4AF37;margin-bottom:.5rem;}
.faq-a{color:#F5E6C8;font-size:.93rem;line-height:1.85;margin-bottom:0;}
.faq-a em{color:#C9A961;font-style:italic;}
.faq-a strong{color:#D4AF37;}

.section-title{font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700;color:#D4AF37;margin:2rem 0 1rem;padding-bottom:.4rem;border-bottom:2px solid #8B3A2E;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <div style="font-size:2.5rem;margin-bottom:.5rem;">❓</div>
    <div class="page-header-title">Frequently Asked Questions</div>
    <div class="page-header-sub">Everything you need to know about this study companion</div>
</div>
""", unsafe_allow_html=True)


render_page_quote(
    "Reforming oneself is like <strong>chiselling a stone</strong> to perfection!"
)
# ── FAQ Data ───────────────────────────────────────────────────────────────────
faqs = {
    "About the App": [
        (
            "What is the Indispensable Values Q&A app?",
            "It is an AI-powered study companion that answers questions about the "
            "Indispensable Values of Bhagavad Gītā Chapter 13, drawing exclusively from "
            "the authentic teachings of <strong>Swāmī Aparājitānandajī</strong>. "
            "It is not a general chatbot — every answer comes from Swamiji's actual talks, "
            "transcripts, and published writings."
        ),
        (
            "Who built this app and why?",
            "This app was built as a humble sevā — an offering — to make Swamiji's "
            "teachings on Indispensable Values accessible to seekers anytime, anywhere. "
            "The goal is to support śravaṇa (listening), manana (reflection), and "
            "nididhyāsana (contemplation) of these sacred values."
        ),
        (
            "Is this app affiliated with Chinmaya Mission?",
            "This app is an independent initiative offered in reverence to "
            "<strong>Pūjya Swāmī Chinmayānandajī</strong> and "
            "<strong>Swāmī Aparājitānandajī</strong>. "
            "It is not an official Chinmaya Mission product, but is built entirely "
            "from their authentic teachings and offered in the spirit of the Mission's vision."
        ),
    ],
    "Using the App": [
        (
            "How do I ask a question?",
            "Go to the <strong>Indispensable Values Q&A</strong> page from the sidebar. "
            "Type your question in the chat box at the bottom and press Enter. "
            "Sample questions are provided if you need inspiration."
        ),
        (
            "What kinds of questions can I ask?",
            "You can ask about any of the 20 Indispensable Values — their meaning, "
            "how Swamiji explains them, how to practise them in daily life, how they "
            "relate to scripture, what stories illustrate them, and more. "
            "<em>For example: 'What is amānitvam?', 'How does kṣāntiḥ help a seeker?', "
            "'What is the difference between humility and inferiority complex?'</em>"
        ),
        (
            "Can I ask questions in Sanskrit?",
            "Yes — you can use Sanskrit terms in your questions and the app will "
            "recognise them. For example, asking about <em>amānitvam</em>, "
            "<em>vairāgyam</em>, or <em>ahiṃsā</em> works just as well as asking "
            "in plain English."
        ),
        (
            "Can I download my conversation?",
            "Yes! Every conversation can be downloaded as a <strong>TXT, PDF, or DOCX</strong> "
            "file using the download buttons at the top of the Q&A page. "
            "This is useful for study notes, satsang preparation, or sharing with others."
        ),
        (
            "Can I filter answers by topic or source?",
            "Yes — the sidebar on the Q&A page has filters for Speaker, Scripture, "
            "Chapter, Source Type, and Language. This lets you narrow retrieval "
            "to specific talks or source types."
        ),
    ],
    "About the Answers": [
        (
            "Will the app make up answers?",
            "No. This is the most important design principle of the app. "
            "It only answers from the uploaded knowledge base — Swamiji's actual talks "
            "and writings. If the answer is not in the knowledge base, the app will say "
            "so clearly and gently, rather than inventing a response."
        ),
        (
            "Why does the app sometimes say it cannot find an answer?",
            "This means the specific topic was not found in the uploaded knowledge base, "
            "or the question used different terminology than Swamiji's teachings. "
            "Try rephrasing your question using the Sanskrit terms or the exact value name. "
            "If the topic genuinely isn't covered, more sources may need to be added."
        ),
        (
            "How accurate are the answers?",
            "The answers are as accurate as the source material. Since all content comes "
            "directly from Swamiji's talks and book, the teachings are authentic. "
            "However, always verify important points with the original source, "
            "and approach the app as a study aid — not a replacement for listening to "
            "Swamiji's discourses directly."
        ),
        (
            "Does the app distinguish between Swamiji's words and general interpretation?",
            "Yes — the app is instructed to clearly distinguish between "
            "<em>'Swamiji explains...'</em> and general Vedantic understanding. "
            "It will never present AI-generated interpretation as Swamiji's words."
        ),
    ],
    "The Knowledge Base": [
        (
            "What sources does this app draw from?",
            "The knowledge base includes: <strong>Value of Values — 8 full discourse transcripts</strong>, "
            "<strong>Bhagavad Gītā Chapter 13 — 2 discourses</strong>, "
            "<strong>Value Based Stories for All — 6 discourses</strong> from children's summer camps, "
            "and Swamiji's published book <strong>Indispensable Values (2022)</strong>. "
            "More sources will be added over time."
        ),
        (
            "Which values does this app cover?",
            "All 20 Indispensable Values from Bhagavad Gītā 13.7–11: "
            "<em>amānitvam, adambhitvam, ahiṃsā, kṣāntiḥ, ārjavam, ācāryopāsanam, "
            "śaucam, sthairyam, ātmavinigrahaḥ, indriyārtheṣu vairāgyam, anahaṅkāra, "
            "janma-mṛtyu darśanam, asaktiḥ, anabhiṣvaṅga, samacittatvam, bhakti, "
            "viviktadeśa-sevitvam, aratir janasaṃsadi, adhyātma-jñāna-nityatvam, "
            "and tattva-jñānārtha-darśanam.</em>"
        ),
    ],
    "Privacy & Technical": [
        (
            "Is my conversation stored or shared?",
            "No conversation data is stored beyond your current session. "
            "When you close the browser or clear the chat, everything is gone. "
            "This app does not collect personal information."
        ),
        (
            "Does this app work on mobile?",
            "Yes — the app is fully accessible on mobile browsers. "
            "Open the app URL in Safari or Chrome on your phone or tablet and "
            "it will work just as well as on a desktop."
        ),
        (
            "What AI model powers this app?",
            "The app uses <strong>OpenAI GPT-4o-mini</strong> for answer generation "
            "and <strong>OpenAI text-embedding-3-small</strong> for semantic search. "
            "These are cost-effective, high-quality models well-suited for "
            "knowledge-grounded question answering."
        ),
    ],
}

# ── Render FAQs ────────────────────────────────────────────────────────────────
for section, questions in faqs.items():
    st.markdown(f'<div class="section-title">{section}</div>', unsafe_allow_html=True)
    for q, a in questions:
        with st.expander(q):
            st.markdown(f'<div class="faq-a">{a}</div>', unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:2.5rem;padding:1.5rem;
    border-top:2px solid #8B3A2E;color:#B8956B;
    font-family:'Cormorant Garamond',serif;font-style:italic;font-size:.95rem;">
    🪷 &nbsp; Still have a question? Use the Q&amp;A page — Swamiji's teachings may have the answer! &nbsp; 🪷
</div>
""", unsafe_allow_html=True)
