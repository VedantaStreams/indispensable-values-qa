"""
pages/2_Indispensable_Values_QA.py — Main RAG Q&A interface.
"""

import streamlit as st
from src.page_header import render_header
from src.rag_chain import answer_question, DEFAULT_K
from src.vector_store import get_collection_count

st.set_page_config(
    page_title="Q&A · Indispensable Values",
    page_icon="💬",
    layout="wide",
)

render_header("Indispensable Values Q&A")

# ---------------------------------------------------------------------------
# Knowledge-base status banner
# ---------------------------------------------------------------------------
try:
    kb_count = get_collection_count()
except Exception:
    kb_count = 0

if kb_count == 0:
    st.warning(
        "⚠️ The knowledge base is not yet built. "
        "Please ask an administrator to upload sources and build the knowledge base "
        "before using this Q&A interface.",
        icon="⚠️",
    )

# ---------------------------------------------------------------------------
# Sidebar: advanced settings
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        "<h4 style='font-family:\"Playfair Display\",serif; color:#4A7C59;'>⚙️ Search Settings</h4>",
        unsafe_allow_html=True,
    )
    num_chunks = st.slider(
        "Chunks to retrieve",
        min_value=1,
        max_value=16,
        value=DEFAULT_K,
        step=1,
        help="Number of source passages to retrieve for each question.",
    )
    show_sources = st.checkbox("Show retrieved sources", value=True)
    st.markdown(
        "<hr style='border-top:1px solid #4A7C59; opacity:0.3;'>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <small style="font-family:'Lato',sans-serif; color:#888;">
        Answers are drawn exclusively from Swamiji's authenticated teachings.
        No information is fabricated.
        </small>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Question input
# ---------------------------------------------------------------------------
st.markdown(
    """
    <p style="font-family:'Lato',sans-serif; color:#444; line-height:1.7;">
        Ask any question about the <strong>20 Indispensable Values (jñāna sādhana)</strong>
        from Bhagavad Gītā Chapter 13, verses 7–11, as taught by
        Pūjya Swāmī Aparājitānandajī.
    </p>
    """,
    unsafe_allow_html=True,
)

# Sample questions for inspiration
with st.expander("💡 Sample questions to get started", expanded=False):
    sample_questions = [
        "What is amānitvam and how does Swamiji explain it?",
        "How does Swamiji distinguish kṣāntiḥ (forbearance) from mere tolerance?",
        "What stories does Swamiji use to illustrate ahiṃsā?",
        "Explain ārjavam (straightforwardness) in Swamiji's words.",
        "What is the relationship between vairāgyam and renunciation?",
        "How does Swamiji describe the role of the teacher (ācāryopāsanam)?",
        "What does Swamiji say about purity of mind (śaucam)?",
    ]
    for q in sample_questions:
        if st.button(q, key=f"sample_{q[:20]}", use_container_width=False):
            st.session_state["current_question"] = q

question = st.text_area(
    "Your question:",
    value=st.session_state.get("current_question", ""),
    height=100,
    placeholder="e.g. What does Swamiji teach about humility (amānitvam)?",
    key="question_input",
)

ask_col, clear_col = st.columns([4, 1])
with ask_col:
    ask_button = st.button("🙏 Ask Swamiji's Teachings", type="primary", use_container_width=True)
with clear_col:
    if st.button("Clear", use_container_width=True):
        st.session_state.pop("current_question", None)
        st.rerun()

# ---------------------------------------------------------------------------
# Answer display
# ---------------------------------------------------------------------------
if ask_button and question.strip():
    with st.spinner("Searching through Swamiji's teachings…"):
        result = answer_question(question.strip(), k=num_chunks)

    st.markdown("<hr style='border-top:2px solid #4A7C59; opacity:0.2;'>", unsafe_allow_html=True)

    if result["on_topic"] and result["num_chunks"] > 0:
        st.markdown(
            f"""
            <div style="
                background:#EDF3EC; border-radius:10px; padding:1.2rem 1.5rem;
                border-left:5px solid #4A7C59; margin-bottom:1rem;
            ">
                <span style="font-size:1.3rem;">🙏</span>
                <strong style="font-family:'Playfair Display',serif; color:#4A7C59; margin-left:0.4rem;">
                    Answer from Swamiji's Teachings
                </strong>
                <div style="font-family:'Lato',sans-serif; font-size:1rem; color:#2C2C2C;
                            line-height:1.8; margin-top:0.8rem; white-space:pre-wrap;">
                    {result["answer"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if show_sources and result["sources"]:
            st.markdown(
                "<p style='font-family:\"Lato\",sans-serif; font-size:0.85rem; color:#8B6914;'>"
                "📚 <strong>Retrieved from:</strong> "
                + " · ".join(result["sources"])
                + f" ({result['num_chunks']} passages)"
                + "</p>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            f"""
            <div style="
                background:#FFF8F0; border-left:4px solid #8B6914;
                border-radius:8px; padding:1rem 1.5rem;
            ">
                <span style="font-family:'Lato',sans-serif; color:#555;">{result["answer"]}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

elif ask_button and not question.strip():
    st.info("Please enter a question before asking.")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(
    """
    <hr style='border-top:1px solid #4A7C59; opacity:0.2; margin-top:2rem;'>
    <div style='text-align:center; font-family:"Lato",sans-serif; font-size:0.8rem; color:#888;'>
        Answers drawn exclusively from authenticated teachings of Pūjya Swāmī Aparājitānandajī
    </div>
    """,
    unsafe_allow_html=True,
)
