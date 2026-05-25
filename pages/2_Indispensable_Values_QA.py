import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st
import datetime
from pathlib import Path
import sys
from pathlib import Path as _Path
_ROOT = _Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from src.page_header import render_om_symbol, render_page_quote


st.set_page_config(
    page_title="Indispensable Values Q&A",
    page_icon="🪷",
    layout="wide",
)

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ui_components import inject_global_css, render_chunk_card
from src.rag_chain import get_rag_answer, estimate_query_cost
from src.vector_store import get_collection_stats
from src.export_utils import export_to_txt, export_to_pdf, export_to_docx
from src.prompts import INDISPENSABLE_VALUES

inject_global_css()

# ── Page CSS ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.swamiji-quote{background:linear-gradient(135deg,#FFFFFF,#E8F4F6);border-left:5px solid #0D5C6B;border-radius:0 14px 14px 0;padding:1rem 1.5rem;margin:.8rem 0;font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1rem;color:#0A1E28;line-height:1.7;}
.swamiji-quote-attr{font-family:'Lato',sans-serif;font-style:normal;font-size:.75rem;font-weight:700;color:#0D5C6B;letter-spacing:.5px;margin-top:.4rem;}

.om-box-qa {
    background:linear-gradient(135deg,#FFFFFF,#D0EDF1);
    border:2px solid #062E3A;border-radius:16px;
    width:90px;height:90px;
    display:inline-flex;align-items:center;justify-content:center;
    margin-bottom:.8rem;
    box-shadow:0 4px 16px rgba(212,175,55,.20);
}
.om-box-qa img{width:70px;height:70px;object-fit:contain;border-radius:10px;}

.qa-header {
    background: linear-gradient(135deg, #FFFFFF 0%, #D0EDF1 50%, #FFFFFF 100%);
    border: 2px solid #88C5D0;
    border-radius: 18px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,.08);
}
.qa-header-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #062E3A;
    margin-bottom: 0.3rem;
}
.qa-header-sub {
    color: #0D5C6B;
    font-style: italic;
    font-size: 1rem;
    font-family: 'Cormorant Garamond', serif;
}

/* Starter question buttons — Royal Maroon */
.stButton > button {
    background: linear-gradient(135deg, #FFFFFF, #D0EDF1) !important;
    color: #062E3A !important;
    border: 1.5px solid #062E3A !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1rem !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-style: italic !important;
    font-size: 0.92rem !important;
    transition: all 0.2s !important;
    text-align: left !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 3rem !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0D5C6B, #2C95A8) !important;
    color: white !important;
    border-color: #062E3A !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(26,122,140,0.3) !important;
}
.chat-wrapper {
    max-height: 58vh;
    overflow-y: auto;
    padding-right: 0.5rem;
    margin-bottom: 1rem;
}
.user-bubble {
    background: linear-gradient(135deg, #0D5C6B, #2C95A8);
    border: 1px solid #88C5D0;
    border-radius: 16px 16px 4px 16px;
    padding: 0.85rem 1.15rem;
    margin: 0.5rem 0 0.5rem 18%;
    color: white;
    font-size: 0.95rem;
    line-height: 1.6;
}
.bot-bubble {
    background: #FFFFFF;
    border: 1.5px solid #88C5D0;
    border-radius: 4px 16px 16px 16px;
    padding: 1rem 1.3rem;
    margin: 0.5rem 18% 0.5rem 0;
    color: #0A1E28;
    font-size: 0.93rem;
    line-height: 1.75;
}
.role-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    margin-bottom: 0.3rem;
    opacity: 0.85;
}
.user-label { color: #0D5C6B; text-align: right; }
.bot-label  { color: #062E3A; }
.sample-q {
    background: #FFFFFF;
    border: 1.5px solid #88C5D0;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
    color: #062E3A;
    cursor: pointer;
    margin-bottom: 0.4rem;
    transition: background 0.2s;
}
.sample-q:hover { background: rgba(212,175,55,0.15); }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Filters & Controls
# ════════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🎛️ Filters")
    st.caption("Narrow retrieval to specific sources")

    filter_speaker = st.text_input(
        "Speaker", placeholder="e.g. Swami Aparajitananda", key="f_speaker"
    )
    filter_scripture = st.text_input(
        "Scripture", placeholder="e.g. Bhagavad Gītā", key="f_scripture"
    )
    filter_chapter = st.text_input(
        "Chapter", placeholder="e.g. 13", key="f_chapter"
    )
    filter_source_type = st.selectbox(
        "Source Type",
        ["All", "youtube_video", "youtube_playlist", "pdf_book", "transcript", "notes"],
        key="f_src_type",
    )
    filter_language = st.selectbox(
        "Language", ["All", "English", "Sanskrit", "Hindi", "Tamil", "Telugu"],
        key="f_lang",
    )
    filter_value = st.selectbox(
        "Value / Topic",
        ["All"] + INDISPENSABLE_VALUES,
        key="f_value",
    )

    st.divider()
    st.markdown("## ⚙️ Retrieval")
    n_chunks = st.slider("Chunks to retrieve", 3, 10, 6)
    model = st.selectbox("Chat Model", ["gpt-4o-mini", "gpt-4o"], index=0)
    show_sources = st.checkbox("Show retrieved chunks", value=True)

    st.divider()
    st.markdown("## 📊 Status")
    try:
        stats = get_collection_stats()
        st.metric("Chunks indexed", stats.get("total_chunks", 0))
        st.metric("Sources", stats.get("total_sources", 0))
        if stats.get("total_chunks", 0) == 0:
            st.warning("Knowledge base is empty. Build it first.")
    except Exception:
        st.error("Could not reach vector store.")

# ── Build filter dict ──────────────────────────────────────────────────────────
filters = {}
if filter_speaker.strip():
    filters["speaker"] = filter_speaker.strip()
if filter_scripture.strip():
    filters["scripture"] = filter_scripture.strip()
if filter_chapter.strip():
    filters["chapter"] = filter_chapter.strip()
if filter_source_type != "All":
    filters["source_type"] = filter_source_type
if filter_language != "All":
    filters["language"] = filter_language

# ════════════════════════════════════════════════════════════════════════════════
# MAIN — Header
# ════════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="qa-header">
    <div class="om-box-qa">
        <img src="data:image/jpeg;base64,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" alt="Om"/>
    </div><br>
    <div class="qa-header-title">Indispensable Values Q&amp;A</div>
    <div class="qa-header-sub">
        Ask questions grounded in Swamiji's teachings on Bhagavad Gītā Chapters 13 &amp; 16 — Jñāna Sādhana values &amp; Daivī / Āsurī qualities
    </div>
</div>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_chunks" not in st.session_state:
    st.session_state.last_chunks = []
if "last_usage" not in st.session_state:
    st.session_state.last_usage = {}
if "story_value" not in st.session_state:
    st.session_state.story_value = None
if "story_result" not in st.session_state:
    st.session_state.story_result = None
if "story_chunks" not in st.session_state:
    st.session_state.story_chunks = []

# ── Toolbar ────────────────────────────────────────────────────────────────────
col_clear, col_dl1, col_dl2, col_dl3 = st.columns([2, 1, 1, 1])
with col_clear:
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_chunks = []
        st.session_state.last_usage = {}
        st.rerun()

msgs = st.session_state.messages
if msgs:
    with col_dl1:
        txt_bytes = export_to_txt(msgs)
        st.download_button(
            "⬇️ TXT", txt_bytes,
            file_name=f"iv_qa_{datetime.date.today()}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col_dl2:
        pdf_bytes = export_to_pdf(msgs)
        if pdf_bytes:
            st.download_button(
                "⬇️ PDF", pdf_bytes,
                file_name=f"iv_qa_{datetime.date.today()}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.caption("Install reportlab for PDF")
    with col_dl3:
        docx_bytes = export_to_docx(msgs)
        if docx_bytes:
            st.download_button(
                "⬇️ DOCX", docx_bytes,
                file_name=f"iv_qa_{datetime.date.today()}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        else:
            st.caption("Install python-docx for DOCX")

st.divider()

# ── 20 Starter Questions ──────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style="background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:12px;
        padding:1rem 1.4rem;margin-bottom:1rem;border-left:5px solid #0D5C6B;">
        <div style="font-family:'Playfair Display',serif;font-weight:700;
            color:#062E3A;font-size:1.05rem;margin-bottom:.3rem;">
            ✨ Starter Questions
        </div>
        <div style="font-size:.88rem;color:#1A3A45;line-height:1.6;">
            New to the app? Choose a chapter tab and click any question to begin your inquiry.
            Questions are drawn from <strong>Bhagavad Gītā Chapters 13 &amp; 16</strong>
            — as unfolded by Swamiji in his discourses.
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_ch13, tab_ch16, tab_stories = st.tabs([
        "📖 BG Ch.13 — 20 Jñāna Values",
        "📖 BG Ch.16 — 26 Daivī Values",
        "🪷 Stories from Swamiji's Talks",
    ])

    # ── TAB 1: Chapter 13 ─────────────────────────────────────────────────────
    with tab_ch13:
        st.markdown("""
        <div style="background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:14px;
             padding:1.2rem 1.5rem;margin-bottom:1.2rem;">
          <div style="font-family:'Playfair Display',serif;font-size:1.05rem;
               font-weight:800;color:#062E3A;margin-bottom:.7rem;">
            📖 The 20 Indispensable Values (BG 13.7–11)
          </div>
          <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:.4rem .8rem;font-size:.88rem;color:#0A1E28;">
            <div>1. amānitvam</div><div>2. adambhitvam</div>
            <div>3. ahiṃsā</div><div>4. kṣāntiḥ</div>
            <div>5. ārjavam</div><div>6. ācāryopāsanam</div>
            <div>7. śaucam</div><div>8. sthairyam</div>
            <div>9. ātmavinigrahaḥ</div><div>10. indriyārtheṣu vairāgyam</div>
            <div>11. anahaṅkāra</div><div>12. janma-mṛtyu darśanam</div>
            <div>13. asaktiḥ</div><div>14. anabhiṣvaṅga</div>
            <div>15. samacittatvam</div><div>16. bhakti avyabhicāriṇī</div>
            <div>17. viviktadeśa-sevitvam</div><div>18. aratir janasaṃsadi</div>
            <div>19. adhyātma-jñāna-nityatvam</div><div>20. tattva-jñānārtha-darśanam</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        starter_themes_ch13 = {
            "🌸 BG 13.7 — Humility & Non-Injury": [
                "What is *amānitvam* (humility / absence of pride) in Vedānta?",
                "What is *adambhitvam* — freedom from hypocrisy and ostentation?",
                "What is *ahiṃsā* (non-injury) as taught in Bhagavad Gītā Chapter 13?",
                "What is *kṣāntiḥ* (forgiveness and forbearance) and why is it indispensable?",
                "What is *ārjavam* (simplicity / straightforwardness)?",
            ],
            "🪷 BG 13.7 — Devotion, Purity & Restraint": [
                "What is *ācāryopāsanam* — devotion and service to the teacher?",
                "What is *śaucam* (purity of body and mind) in Chapter 13?",
                "What is *sthairyam* (steadfastness) in spiritual practice?",
                "What is *ātmavinigrahaḥ* — self-control over the senses?",
                "What is *indriyārtheṣu vairāgyam* — dispassion towards sense objects?",
            ],
            "🧘 BG 13.8–9 — Detachment & Equanimity": [
                "What is *anahaṅkāra* (absence of ego) and how do I cultivate it?",
                "What is *janma-mṛtyu darśanam* — seeing sorrow in birth, death, and disease?",
                "What is *asaktiḥ* (non-attachment to people and things)?",
                "What is *anabhiṣvaṅga* — freedom from blind attachment to family?",
                "What is *samacittatvam* (equanimity) in daily life?",
            ],
            "🙏 BG 13.10–11 — Higher Values & Liberation": [
                "What is *bhakti avyabhicāriṇī* — unswerving devotion to the Lord?",
                "What is *viviktadeśa-sevitvam* — love of solitude for spiritual practice?",
                "What is *aratir janasaṃsadi* — disinterest in worldly gatherings?",
                "What is *adhyātma-jñāna-nityatvam* — constancy in self-knowledge?",
                "What is *tattva-jñānārtha-darśanam* — seeing liberation as the goal of life?",
            ],
            "💡 Chapter 13 — Application & Reflection": [
                "Why are these 20 values called 'indispensable' for knowledge (jñāna)?",
                "How are the 20 values of Chapter 13 different from the 26 values of Chapter 16?",
                "Which of the 20 values is the hardest to cultivate and why?",
                "How does Swamiji explain the link between these values and Self-knowledge?",
                "How do I bring the 20 values of Chapter 13 into my daily life?",
            ],
        }

        for theme, questions in starter_themes_ch13.items():
            st.markdown(f"**{theme}**")
            cols = st.columns(2)
            for i, q in enumerate(questions):
                clean_q = q.replace("*", "")
                with cols[i % 2]:
                    if st.button(q, key=f"ch13_{theme}_{i}", use_container_width=True):
                        st.session_state.messages.append({"role": "user", "content": clean_q})
                        st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)

    # ── TAB 2: Chapter 16 ─────────────────────────────────────────────────────
    with tab_ch16:
        st.markdown("""
        <div style="background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:14px;
             padding:1.2rem 1.5rem;margin-bottom:1.2rem;">
          <div style="font-family:'Playfair Display',serif;font-size:1.05rem;
               font-weight:800;color:#062E3A;margin-bottom:.7rem;">
            📖 The 26 Indispensable Values (BG 16.01–16.03)
          </div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.4rem .8rem;font-size:.88rem;">
            <div><strong>BG 16.01</strong></div><div></div><div></div>
            <div>1. abhayam</div><div>2. sattva-saṁśuddhiḥ</div><div>3. jñāna-yoga-vyavasthitiḥ</div>
            <div>4. dānam</div><div>5. damaḥ</div><div>6. yajñaḥ</div>
            <div>7. svādhyāyaḥ</div><div>8. tapas</div><div>9. ārjavam</div>
            <div style="margin-top:.5rem"><strong>BG 16.02</strong></div><div></div><div></div>
            <div>10. ahiṃsā</div><div>11. satyam</div><div>12. akrodhaḥ</div>
            <div>13. tyāgaḥ</div><div>14. śāntiḥ</div><div>15. apaiśunam</div>
            <div>16. dayā bhūteṣu</div><div>17. aloluptvam</div><div>18. mārdavam</div>
            <div>19. hrīḥ</div><div>20. acāpalam</div><div></div>
            <div style="margin-top:.5rem"><strong>BG 16.03</strong></div><div></div><div></div>
            <div>21. tejaḥ</div><div>22. kṣamā</div><div>23. dhṛtiḥ</div>
            <div>24. śaucam</div><div>25. adrohaḥ</div><div>26. nātimānitā</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        starter_themes = {
            "🌱 BG 16.01 — Nine Values": [
                "What does *abhayam* (fearlessness) mean in Vedānta?",
                "What is *sattva-saṁśuddhiḥ* (purity of being) and how do I cultivate it?",
                "What is *jñāna-yoga-vyavasthitiḥ* — steadfastness in knowledge and yoga?",
                "What role does *dānam* (giving) play in spiritual growth?",
                "What is *damaḥ* (self-restraint) and how does it differ from suppression?",
                "What is *yajñaḥ* (sacrifice / worship) in daily life?",
                "What is *svādhyāyaḥ* (scriptural study) and why is it indispensable?",
                "What does *tapas* (austerity) mean for a modern seeker?",
            ],
            "🌸 BG 16.01 — Tenth Value": [
                "What is *ārjavam* (straightforwardness / integrity)?",
                "How does integrity in thought, word, and deed connect to spiritual progress?",
            ],
            "❤️ BG 16.02 — Eleven Values": [
                "What is true *ahiṃsā* (non-violence) in daily life?",
                "What is *satyam* (truthfulness) and when is silence more truthful than speech?",
                "What is *akrodhaḥ* (freedom from anger) and how do I cultivate it?",
                "What is *tyāgaḥ* (renunciation) in the context of Chapter 16?",
                "How do I develop *śāntiḥ* (inner peace) amid life's challenges?",
                "What is *apaiśunam* (absence of fault-finding / non-slander)?",
                "What is *dayā bhūteṣu* — compassion toward all beings?",
                "What is *aloluptvam* (non-covetousness / freedom from greed)?",
                "What is *mārdavam* (gentleness) and how is it different from weakness?",
                "What is *hrīḥ* (modesty / sense of honour) in Vedānta?",
                "What is *acāpalam* (steadiness / freedom from restlessness)?",
            ],
            "🔥 BG 16.03 — Six Values": [
                "What is *tejaḥ* (vigour / radiance) as a spiritual quality?",
                "What is *kṣamā* (forgiveness) and why is it a divine virtue?",
                "What is *dhṛtiḥ* (fortitude / endurance) in spiritual life?",
                "What is *śaucam* (inner and outer purity)?",
                "What is *adrohaḥ* (absence of malice / non-hatred)?",
                "What is *nātimānitā* (absence of excessive pride / humility)?",
            ],
            "🧘 Inner Discipline": [
                "How are the 26 values of Chapter 16 different from the 20 values of Chapter 13?",
                "Why are these values called 'indispensable' for spiritual progress?",
                "Which of the 26 values is the hardest to cultivate and why?",
                "How do I balance tapas (austerity) with enjoyment in daily life?",
                "What does Chapter 16 say about divine vs demoniac qualities?",
                "How do I know if I am progressing in my spiritual values?",
            ],
            "💕 Devotion & Practice": [
                "How do I bring these 26 values into my daily routine?",
                "Which value should I focus on first as a beginner?",
                "How does Swamiji explain the link between values and meditation?",
                "What is the relationship between values and Self-knowledge in Vedānta?",
                "How do I maintain these values when I feel stressed or overwhelmed?",
                "How do I balance worldly responsibilities with spiritual life?",
            ],
        }

        for theme, questions in starter_themes.items():
            st.markdown(f"**{theme}**")
            cols = st.columns(2)
            for i, q in enumerate(questions):
                clean_q = q.replace("*", "")
                with cols[i % 2]:
                    if st.button(q, key=f"start_{theme}_{i}", use_container_width=True):
                        st.session_state.messages.append(
                            {"role": "user", "content": clean_q}
                        )
                        st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)

    # ── TAB 3: Stories from Swamiji's Talks ───────────────────────────────────
    with tab_stories:
        st.markdown("""
        <div style="background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:12px;
            padding:1rem 1.4rem;margin-bottom:1.2rem;border-left:5px solid #0D5C6B;">
            <div style="font-family:'Playfair Display',serif;font-weight:700;
                color:#062E3A;font-size:1.05rem;margin-bottom:.3rem;">
                🪷 Stories from Swamiji's Talks
            </div>
            <div style="font-size:.88rem;color:#1A3A45;line-height:1.6;">
                Select any value below to retrieve a story or illustration Swamiji used
                in his discourses to illuminate that value. Stories are drawn directly
                from <strong>Swamiji's indexed talks and writings</strong> — nothing is invented.
                If no specific story exists in the knowledge base for that value, the app
                will say so honestly.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Ch.13 Value Buttons ────────────────────────────────────────────────
        st.markdown("""
        <div style="font-family:'Playfair Display',serif;font-size:.95rem;font-weight:800;
            color:#062E3A;margin:.6rem 0 .4rem;">
            📖 BG 13.7–11 — Jñāna Sādhana (20 Values)
        </div>
        """, unsafe_allow_html=True)
        ch13_values = [
            "amānitvam", "adambhitvam", "ahiṃsā", "kṣāntiḥ", "ārjavam",
            "ācāryopāsanam", "śaucam", "sthairyam", "ātmavinigrahaḥ",
            "indriyārtheṣu vairāgyam", "anahaṅkāra", "janma-mṛtyu darśanam",
            "asaktiḥ", "anabhiṣvaṅga", "samacittatvam", "bhakti avyabhicāriṇī",
            "viviktadeśa-sevitvam", "aratir janasaṃsadi",
            "adhyātma-jñāna-nityatvam", "tattva-jñānārtha-darśanam",
        ]
        cols_s13 = st.columns(4)
        for i, val in enumerate(ch13_values):
            with cols_s13[i % 4]:
                if st.button(val, key=f"story_ch13_{i}", use_container_width=True):
                    st.session_state.story_value = val
                    st.session_state.story_result = None
                    st.session_state.story_chunks = []
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Ch.16 Value Buttons ────────────────────────────────────────────────
        st.markdown("""
        <div style="font-family:'Playfair Display',serif;font-size:.95rem;font-weight:800;
            color:#062E3A;margin:.6rem 0 .4rem;">
            📖 BG 16.01–16.03 — Daivī Sampat (26 Values)
        </div>
        """, unsafe_allow_html=True)
        ch16_values = [
            "abhayam", "sattva-saṁśuddhiḥ", "jñāna-yoga-vyavasthitiḥ",
            "dānam", "damaḥ", "yajñaḥ", "svādhyāyaḥ", "tapas", "ārjavam",
            "ahiṃsā", "satyam", "akrodhaḥ", "tyāgaḥ", "śāntiḥ", "apaiśunam",
            "dayā bhūteṣu", "aloluptvam", "mārdavam", "hrīḥ", "acāpalam",
            "tejaḥ", "kṣamā", "dhṛtiḥ", "śaucam", "adrohaḥ", "nātimānitā",
        ]
        cols_s16 = st.columns(4)
        for i, val in enumerate(ch16_values):
            with cols_s16[i % 4]:
                if st.button(val, key=f"story_ch16_{i}", use_container_width=True):
                    st.session_state.story_value = val
                    st.session_state.story_result = None
                    st.session_state.story_chunks = []
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Story Result ───────────────────────────────────────────────────────
        if st.session_state.story_value:
            selected_val = st.session_state.story_value

            # Fire RAG query if no result yet
            if st.session_state.story_result is None:
                story_query = (
                    f"Please share a story, parable, or illustration that Pūjya Swāmī "
                    f"Aparājitānanda used in his teachings to explain the value of "
                    f"{selected_val}. Narrate the story as Swamiji told it, with as much "
                    f"detail as the knowledge base contains. Then offer a short reflection "
                    f"prompt to help the reader contemplate this value in their daily life."
                )
                with st.spinner(f"🔍 Searching Swamiji's talks for a story on {selected_val}…"):
                    result = get_rag_answer(
                        question=story_query,
                        filters=None,
                        n_chunks=n_chunks,
                        model=model,
                    )
                st.session_state.story_result = result.get("answer", "")
                st.session_state.story_chunks = result.get("chunks", [])
                st.rerun()

            # Display story card
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#FFFFFF,#E8F4F6);
                border:2px solid #88C5D0;border-left:5px solid #0D5C6B;
                border-radius:0 16px 16px 0;
                padding:1.5rem 2rem;margin:1rem 0;
                box-shadow:0 4px 16px rgba(0,0,0,.08);">
                <div style="font-family:'Playfair Display',serif;font-size:1.15rem;
                    font-weight:800;color:#062E3A;margin-bottom:.6rem;">
                    🪷 &nbsp; Story on <em>{selected_val}</em>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(st.session_state.story_result)

            if st.button("🔄 Clear Story & Choose Another", key="clear_story",
                         use_container_width=False):
                st.session_state.story_value = None
                st.session_state.story_result = None
                st.session_state.story_chunks = []
                st.rerun()

            # Source chunks
            if show_sources and st.session_state.story_chunks:
                st.divider()
                st.markdown("### 📌 Retrieved Context Chunks")
                st.caption(
                    f"Top {len(st.session_state.story_chunks)} chunk(s) retrieved "
                    "from the knowledge base."
                )
                for i, chunk in enumerate(st.session_state.story_chunks, 1):
                    render_chunk_card(chunk, i)
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="role-label user-label">You</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="role-label bot-label">🪷 Swamiji\'s Teachings</div>', unsafe_allow_html=True)
            # Render markdown inside the bubble via st.markdown for bold/italic support
            with st.container():
                st.markdown(msg["content"])
            st.markdown("---")

# ── Process Last Pending User Message ─────────────────────────────────────────
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_q = st.session_state.messages[-1]["content"]

    with st.spinner("🔍 Searching knowledge base and composing answer…"):
        result = get_rag_answer(
            question=last_q,
            filters=filters if filters else None,
            n_chunks=n_chunks,
            model=model,
        )

    answer      = result.get("answer", "")
    chunks      = result.get("chunks", [])
    usage       = result.get("usage", {})
    gw          = result.get("guardrail_warning", "")

    # Append assistant answer
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.last_chunks = chunks
    st.session_state.last_usage  = usage

    if gw:
        st.session_state.messages[-1]["content"] += f"\n\n{gw}"

    st.rerun()

# ── Chat Input ─────────────────────────────────────────────────────────────────
user_input = st.chat_input(
    "Ask a question about Indispensable Values…",
    key="chat_input_main",
)
if user_input and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    st.rerun()

# ── Retrieved Chunks (expandable) ──────────────────────────────────────────────
if show_sources and st.session_state.last_chunks:
    st.divider()
    st.markdown("### 📌 Retrieved Context Chunks")
    st.caption(
        f"Top {len(st.session_state.last_chunks)} chunk(s) retrieved from the knowledge base "
        "and passed to the model."
    )
    for i, chunk in enumerate(st.session_state.last_chunks, 1):
        render_chunk_card(chunk, i)

# ── Usage Footer ───────────────────────────────────────────────────────────────
if st.session_state.last_usage:
    u = st.session_state.last_usage
    pt = u.get("prompt_tokens", 0)
    ct = u.get("completion_tokens", 0)
    cost = estimate_query_cost(pt, ct, model)
    st.caption(
        f"💡 Last query: {pt} prompt + {ct} completion tokens "
        f"≈ ${cost:.5f} | Queries today: {u.get('queries_today', 0)}"
    )
