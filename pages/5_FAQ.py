"""
pages/5_FAQ.py — Frequently asked questions about the values and this app.
"""

import streamlit as st
from src.page_header import render_header

st.set_page_config(
    page_title="FAQ · Indispensable Values Q&A",
    page_icon="❓",
    layout="wide",
)

render_header("Frequently Asked Questions")

faqs = [
    (
        "What are the 20 Indispensable Values?",
        "The 20 Indispensable Values (jñāna sādhana) are the spiritual qualities described "
        "by Lord Kṛṣṇa in Bhagavad Gītā Chapter 13, verses 7–11, as prerequisites for "
        "Self-knowledge. They range from amānitvam (humility) to tattva-jñānārtha-darśanam "
        "(seeing the goal as knowledge of Truth). Together they constitute the inner wealth "
        "that prepares the seeker for liberation (mokṣa).",
    ),
    (
        "Where does the Q&A content come from?",
        "All answers are drawn exclusively from Pūjya Swāmī Aparājitānandajī's "
        "authenticated teachings: His video discourse transcripts on 'Value of Values', "
        "Bhagavad Gītā Chapter 13, and 'Value Based Stories for All', "
        "as well as His published book Indispensable Values (2022). "
        "No information is fabricated or sourced from the internet.",
    ),
    (
        "Can the AI make up Swamiji's words?",
        "No. The application uses Retrieval-Augmented Generation (RAG): it searches the "
        "vector database of actual source texts, retrieves relevant passages, and asks the "
        "LLM to answer only from those passages. If no sufficiently similar passage is found, "
        "the app honestly says so rather than fabricating an answer.",
    ),
    (
        "What language models power the app?",
        "The app uses OpenAI GPT-4o-mini for answer generation (temperature 0.2 for accuracy) "
        "and OpenAI text-embedding-3-small for creating the semantic vector database.",
    ),
    (
        "Why are Sanskrit terms used throughout?",
        "Sanskrit diacritical marks are integral to the precision of Vedāntic vocabulary. "
        "Terms like amānitvam, kṣāntiḥ, and ārjavam carry specific philosophical meanings "
        "that are preserved by faithful transliteration. The app follows Swamiji's own usage.",
    ),
    (
        "Who can use this app?",
        "Any sincere seeker of Vedāntic wisdom — students, disciples, and practitioners "
        "interested in Bhagavad Gītā Chapter 13 and the 20 values. "
        "Admin pages (for uploading sources and building the knowledge base) "
        "are password-protected and restricted to authorised administrators.",
    ),
    (
        "How do I get the most accurate answers?",
        "Ask specific questions referencing the value name (e.g., 'amānitvam', 'kṣāntiḥ') "
        "or the topic you are studying. The more context you provide, the better the "
        "retrieval. You can also adjust the number of retrieved passages in the sidebar.",
    ),
    (
        "Is my conversation stored?",
        "No conversation content is stored. Only an anonymous session count is tracked "
        "for the visitor counter on the Home page. No personal data is retained.",
    ),
    (
        "Can I suggest additional sources?",
        "Yes! Please contact the administrator to request that additional authentic "
        "teachings of Pūjya Swāmī Aparājitānandajī be indexed.",
    ),
]

for question, answer in faqs:
    with st.expander(f"❓ {question}", expanded=False):
        st.markdown(
            f"<p style='font-family:\"Lato\",sans-serif; color:#3A3A3A; line-height:1.8;'>"
            f"{answer}</p>",
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
