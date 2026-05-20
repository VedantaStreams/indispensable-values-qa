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
html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#E8F4F6;color:#0A1E28;font-weight:500;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#062E3A!important;font-weight:800!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#FFFFFF,#A8D8E0)!important;border-right:2px solid #88C5D0;}
div[data-testid="stSidebar"] *{color:#0A1E28!important;font-weight:600!important;}

.page-header{background:linear-gradient(135deg,#FFFFFF,#D0EDF1);border:2px solid #88C5D0;
    border-radius:18px;padding:2rem;text-align:center;margin-bottom:1.5rem;
    box-shadow:0 4px 20px rgba(0,0,0,.08);}
.page-header-title{font-family:'Playfair Display',serif;font-size:2.2rem;font-weight:800;color:#062E3A;}
.page-header-sub{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.1rem;color:#0D5C6B;}

.section-card{background:#FFFFFF;border:2px solid #88C5D0;border-radius:14px;
    padding:1.8rem;margin-bottom:1.5rem;box-shadow:0 2px 10px rgba(0,0,0,.06);}
.section-title{font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:700;
    color:#062E3A;margin-bottom:1rem;padding-bottom:.4rem;border-bottom:2px solid #88C5D0;}

.chapter-card{background:linear-gradient(135deg,#FFFFFF,#E8F4F6);
    border:1.5px solid #88C5D0;border-left:5px solid #0D5C6B;
    border-radius:0 12px 12px 0;padding:1.2rem 1.5rem;margin-bottom:1rem;}
.chapter-title{font-family:'Playfair Display',serif;font-weight:800;color:#062E3A;
    font-size:1.2rem;margin-bottom:.3rem;}
.chapter-skt{font-family:'Cormorant Garamond',serif;font-style:italic;
    color:#062E3A;font-size:1rem;margin-bottom:.6rem;}
.chapter-desc{color:#0A1E28;font-size:.93rem;line-height:1.7;font-weight:500;}

.discourse-row{background:#FFFFFF;border:1px solid #88C5D0;border-radius:8px;
    padding:.6rem 1rem;margin-bottom:.4rem;display:flex;align-items:center;gap:.7rem;}
.discourse-icon{font-size:1.1rem;}
.discourse-name{font-weight:700;color:#0A1E28;font-size:.92rem;flex:1;}
.discourse-badge{background:#FFFFFF;color:#0D5C6B;font-size:.72rem;font-weight:700;
    padding:.2rem .6rem;border-radius:10px;letter-spacing:.3px;}

.book-card{background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:10px;
    padding:1rem 1.2rem;margin-bottom:.6rem;}
.book-title{font-family:'Playfair Display',serif;font-weight:700;color:#062E3A;font-size:1rem;}
.book-meta{color:#B8956B;font-size:.82rem;margin-top:.2rem;font-style:italic;}

.stat-row{display:flex;align-items:center;justify-content:center;gap:2rem;
    background:linear-gradient(135deg,#FFFFFF,#E8F4F6);border:1.5px solid #88C5D0;
    border-radius:12px;padding:1rem 1.5rem;margin:1rem 0;flex-wrap:wrap;}
.stat-num{font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:800;color:#0D5C6B;}
.stat-lbl{font-size:.72rem;font-weight:700;color:#1A3A45;
    text-transform:uppercase;letter-spacing:.5px;}

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
<div class="page-header">
    <div class="om-box-pg"><img src="data:image/jpeg;base64,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" alt="Om"/></div>
    <div class="page-header-title">Source Library</div>
    <div class="page-header-sub">All teaching sources indexed in this knowledge base</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="swamiji-quote-pg">
    &ldquo;God resides in the hearts of all. But only those <strong>blessed ones</strong> who have kept their <strong>heart pure</strong> can experience it.&rdquo;
    <span class="swamiji-quote-pg-attr">— Swāmī Aparājitānanda</span>
</div>
""", unsafe_allow_html=True)

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

    st.markdown("**🎙️ 7 Discourses by Swāmī Aparājitānanda**")
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

    st.markdown("**🎙️ 7 Discourses by Swāmī Aparājitānanda**")
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
    st.markdown('<div class="section-card"><div class="section-title">📖 Published Works by Swāmī Aparājitānanda</div>',
                unsafe_allow_html=True)

    books = [
        ("Indispensable Values", "Central Chinmaya Mission Trust, 2022",
         "Detailed commentary on 37 values from Bhagavad Gītā Chapters 13 & 16"),
        ("Gurudev's Quotes — Volume I", "Compilation",
         "Selected quotes from Pūjya Swāmī Chinmayānanda"),
        ("Gurudev's Quotes — Volume II", "Compilation",
         "Selected quotes from Pūjya Swāmī Chinmayānanda"),
        ("Gurudev's Quotes — Volume III", "Compilation",
         "Selected quotes from Pūjya Swāmī Chinmayānanda"),
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
            <p style="color:#1A3A45;line-height:1.7;">
                Once the admin uploads sources and builds the knowledge base,
                they will appear here with their full metadata, including chunk counts
                and processing status.
            </p>
            <p style="color:#1A3A45;line-height:1.7;font-size:.9rem;">
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
