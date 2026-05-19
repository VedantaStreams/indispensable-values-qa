"""
pages/3_Source_Library.py — Browse the knowledge base sources.
Shows the full intended source list (always visible) PLUS dynamically loaded
records from the source_registry.json (when KB has been built).
"""
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import sys
import json
from pathlib import Path

_ROOT = Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st
from src.page_header import render_om_symbol, render_page_quote

st.set_page_config(
    page_title="Source Library | Indispensable Values",
    page_icon="📚",
    layout="wide",
)

DATA_DIR      = _ROOT / "data"
REGISTRY_PATH = DATA_DIR / "processed" / "source_registry.json"

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Lato:wght@300;400;700&family=Cormorant+Garamond:ital,wght@0,500;1,500&display=swap');
html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#E8F4F6;color:#1A3A45;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#0A4A58!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#FFFFFF,#A8D8E0)!important;border-right:2px solid #88C5D0;}
div[data-testid="stSidebar"] *{color:#1A3A45!important;font-weight:600!important;}

.page-header{background:linear-gradient(135deg,#FFFFFF,#D0EDF1);border:2px solid #88C5D0;
    border-radius:18px;padding:2rem;text-align:center;margin-bottom:1.5rem;
    box-shadow:0 4px 20px rgba(0,0,0,.08);}
.page-header-title{font-family:'Playfair Display',serif;font-size:2.2rem;font-weight:800;color:#0A4A58;}
.page-header-sub{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.1rem;color:#1A7A8C;}

.section-card{background:#FFFFFF;border:2px solid #88C5D0;border-radius:14px;
    padding:1.8rem;margin-bottom:1.5rem;box-shadow:0 2px 10px rgba(0,0,0,.06);}
.section-title{font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:700;
    color:#0A4A58;margin-bottom:1rem;padding-bottom:.4rem;border-bottom:2px solid #88C5D0;}

.chapter-card{background:linear-gradient(135deg,#FFFFFF,#E8F4F6);
    border:1.5px solid #88C5D0;border-left:5px solid #1A7A8C;
    border-radius:0 12px 12px 0;padding:1.2rem 1.5rem;margin-bottom:1rem;}
.chapter-title{font-family:'Playfair Display',serif;font-weight:800;color:#0A4A58;
    font-size:1.2rem;margin-bottom:.3rem;}
.chapter-skt{font-family:'Cormorant Garamond',serif;font-style:italic;
    color:#0A4A58;font-size:1rem;margin-bottom:.6rem;}
.chapter-desc{color:#1A3A45;font-size:.92rem;line-height:1.7;}

.discourse-row{background:#FFFFFF;border:1px solid #88C5D0;border-radius:8px;
    padding:.6rem 1rem;margin-bottom:.4rem;display:flex;align-items:center;gap:.7rem;}
.discourse-icon{font-size:1.1rem;}
.discourse-name{font-weight:700;color:#1A3A45;font-size:.92rem;flex:1;}
.discourse-badge{background:#FFFFFF;color:#1A7A8C;font-size:.72rem;font-weight:700;
    padding:.2rem .6rem;border-radius:10px;letter-spacing:.3px;}

.book-card{background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:10px;
    padding:1rem 1.2rem;margin-bottom:.6rem;}
.book-title{font-family:'Playfair Display',serif;font-weight:700;color:#0A4A58;font-size:1rem;}
.book-meta{color:#B8956B;font-size:.82rem;margin-top:.2rem;font-style:italic;}

.stat-row{display:flex;align-items:center;justify-content:center;gap:2rem;
    background:linear-gradient(135deg,#FFFFFF,#E8F4F6);border:1.5px solid #88C5D0;
    border-radius:12px;padding:1rem 1.5rem;margin:1rem 0;flex-wrap:wrap;}
.stat-num{font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:800;color:#1A7A8C;}
.stat-lbl{font-size:.72rem;font-weight:700;color:#3A5C68;
    text-transform:uppercase;letter-spacing:.5px;}
</style>
""", unsafe_allow_html=True)

render_om_symbol()

st.markdown("""
<div class="page-header">
    <div style="font-size:2rem;margin-bottom:.3rem;">📚</div>
    <div class="page-header-title">Source Library</div>
    <div class="page-header-sub">All teaching sources indexed in this knowledge base</div>
</div>
""", unsafe_allow_html=True)

render_page_quote(
    "Rate your <strong>spiritual progress</strong> with the "
    "<strong>intensity of Peace</strong> which you experience."
)

# ── Try to load actual indexed sources ─────────────────────────────────────────
indexed_records = []
if REGISTRY_PATH.exists():
    try:
        indexed_records = json.loads(REGISTRY_PATH.read_text())
    except Exception:
        indexed_records = []

n_indexed = sum(1 for r in indexed_records if r.get("processed"))
total_chunks = sum(r.get("chunk_count", 0) for r in indexed_records)

# ── Stats Bar ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stat-row">
    <div style="text-align:center;">
        <div class="stat-num">14</div>
        <div class="stat-lbl">Discourses</div>
    </div>
    <div style="color:#88C5D0;font-size:1.3rem;">·</div>
    <div style="text-align:center;">
        <div class="stat-num">5</div>
        <div class="stat-lbl">Books</div>
    </div>
    <div style="color:#88C5D0;font-size:1.3rem;">·</div>
    <div style="text-align:center;">
        <div class="stat-num">{n_indexed}</div>
        <div class="stat-lbl">Indexed</div>
    </div>
    <div style="color:#88C5D0;font-size:1.3rem;">·</div>
    <div style="text-align:center;">
        <div class="stat-num">{total_chunks:,}</div>
        <div class="stat-lbl">Chunks</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Two tabs: Overview + Indexed Sources ──────────────────────────────────────
tab_overview, tab_indexed = st.tabs(["📖 Knowledge Base Overview", "✅ Indexed Sources"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — KNOWLEDGE BASE OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab_overview:
    # ── Bhagavad Gita Chapter 13 ──────────────────────────────────────────────
    st.markdown("""
    <div class="chapter-card">
        <div class="chapter-title">📖 Bhagavad Gītā · Chapter 13</div>
        <div class="chapter-skt">Kṣetra–Kṣetrajña Yoga · The 20 Indispensable Values (Jñāna Sādhana)</div>
        <div class="chapter-desc">
            The field of action and the knower of the field. Lord Kṛṣṇa lists 20 essential
            qualities — humility, non-injury, forbearance, simplicity, devotion to teacher,
            purity, steadfastness, self-control, dispassion, equanimity, unswerving devotion,
            and discrimination — that prepare the mind for Self-knowledge.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**🎙️ 7 Discourses by Swāmī Aparājitānandajī**")
    bg13_discourses = [
        ("BG 13 — Discourse 1", "Introduction to Chapter 13 · Kṣetra–Kṣetrajña"),
        ("BG 13 — Discourse 2", "The Knower and the Field · Verses 1–6"),
        ("BG 13 — Discourse 3", "amānitvam, adambhitvam, ahiṃsā · Verse 7"),
        ("BG 13 — Discourse 4", "kṣāntiḥ, ārjavam, ācāryopāsanam · Verse 7"),
        ("BG 13 — Discourse 5", "śaucam, sthairyam, ātmavinigrahaḥ · Verse 7"),
        ("BG 13 — Discourse 6", "vairāgyam, anahaṅkāra, dukha–doṣa darśana · Verses 8–9"),
        ("BG 13 — Discourse 7", "asaktiḥ, samacittatvam, bhakti, viveka · Verses 10–11"),
    ]
    for title, desc in bg13_discourses:
        st.markdown(f"""
        <div class="discourse-row">
            <div class="discourse-icon">🎙️</div>
            <div class="discourse-name">{title} <span style="color:#B8956B;font-weight:400;">— {desc}</span></div>
            <div class="discourse-badge">PDF</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Bhagavad Gita Chapter 16 ──────────────────────────────────────────────
    st.markdown("""
    <div class="chapter-card">
        <div class="chapter-title">📖 Bhagavad Gītā · Chapter 16</div>
        <div class="chapter-skt">Daivāsura Sampad Vibhāga Yoga · Divine vs Demoniac Qualities</div>
        <div class="chapter-desc">
            Lord Kṛṣṇa distinguishes between daivī sampat (divine wealth) and āsurī sampat
            (demoniac qualities). The divine qualities — fearlessness, purity of mind,
            charity, austerity, truthfulness, non-violence — lead to liberation, while
            their opposites bind one to saṃsāra. A guide for self-examination on the path.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**🎙️ 7 Discourses by Swāmī Aparājitānandajī**")
    bg16_discourses = [
        ("BG 16 — Discourse 1", "Introduction · Daivī vs Āsurī Sampat"),
        ("BG 16 — Discourse 2", "abhayaṁ, sattva-saṁśuddhiḥ, jñāna-yoga · Verse 1"),
        ("BG 16 — Discourse 3", "dānam, damaḥ, yajñaḥ, svādhyāya, tapas · Verse 1"),
        ("BG 16 — Discourse 4", "ahiṃsā, satyam, akrodhaḥ, tyāgaḥ, śāntiḥ · Verse 2"),
        ("BG 16 — Discourse 5", "apaiśunam, dayā, mārdavam · Verses 2–3"),
        ("BG 16 — Discourse 6", "The Demoniac Qualities · Verses 4–18"),
        ("BG 16 — Discourse 7", "Conclusion · Scriptural Authority · Verses 19–24"),
    ]
    for title, desc in bg16_discourses:
        st.markdown(f"""
        <div class="discourse-row">
            <div class="discourse-icon">🎙️</div>
            <div class="discourse-name">{title} <span style="color:#B8956B;font-weight:400;">— {desc}</span></div>
            <div class="discourse-badge">PDF</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Published Books ───────────────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">📖 Published Works by Swāmī Aparājitānandajī</div>',
                unsafe_allow_html=True)

    books = [
        ("Indispensable Values", "Central Chinmaya Mission Trust, 2022",
         "Detailed commentary on 37 values from Bhagavad Gītā Chapters 13 & 16"),
        ("Gurudev's Quotes — Volume I", "Compilation",
         "Selected quotes from Pūjya Swāmī Chinmayānandajī"),
        ("Gurudev's Quotes — Volume II", "Compilation",
         "Selected quotes from Pūjya Swāmī Chinmayānandajī"),
        ("Gurudev's Quotes — Volume III", "Compilation",
         "Selected quotes from Pūjya Swāmī Chinmayānandajī"),
        ("Read Daily, Live Fully", "Daily Companion",
         "A daily spiritual companion for seekers"),
    ]
    for title, meta, desc in books:
        st.markdown(f"""
        <div class="book-card">
            <div class="book-title">📚 {title}</div>
            <div class="book-meta">{meta} · {desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — INDEXED SOURCES (live from registry)
# ══════════════════════════════════════════════════════════════════════════════
with tab_indexed:
    if not indexed_records:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">⏳ No Sources Indexed Yet</div>
            <p style="color:#3A5C68;line-height:1.7;">
                Once the admin uploads sources and builds the knowledge base,
                they will appear here with their full metadata, including chunk counts
                and processing status.
            </p>
            <p style="color:#3A5C68;line-height:1.7;font-size:.9rem;">
                <strong>Admins:</strong> Go to the Admin Panel → Upload Sources →
                Build Knowledge Base.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.caption(f"Showing {len(indexed_records)} indexed source(s)")

        for rec in indexed_records:
            processed  = rec.get("processed", False)
            src_name   = rec.get("file_name", "Unknown")
            speaker    = rec.get("speaker", "—")
            topic      = rec.get("topic", "—")
            scripture  = rec.get("scripture", "—")
            chapter    = rec.get("chapter", "—")
            verse      = rec.get("verse_range", "—")
            language   = rec.get("language", "—")
            chunk_cnt  = rec.get("chunk_count", 0)
            created    = (rec.get("created_at", "") or "")[:10]

            status_icon = "✅" if processed else "⏳"
            with st.expander(
                f"{status_icon}  {src_name}  ·  {speaker}  ·  {chunk_cnt} chunks",
                expanded=False,
            ):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Speaker:** {speaker}")
                    st.markdown(f"**Topic:** {topic}")
                    st.markdown(f"**Language:** {language}")
                with col2:
                    st.markdown(f"**Scripture:** {scripture}")
                    st.markdown(f"**Chapter:** {chapter}")
                    st.markdown(f"**Verses:** {verse}")
                with col3:
                    st.markdown(f"**Chunks:** {chunk_cnt}")
                    st.markdown(f"**Added:** {created}")
                    st.markdown(f"**Status:** {'✅ Processed' if processed else '⏳ Pending'}")
