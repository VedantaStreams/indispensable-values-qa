"""
pages/7_Admin_Upload_Sources.py — Admin only. Password protected.
Two upload options: Discourse Transcripts and Books/Articles (PDF).
"""
import sys
import json
from pathlib import Path
from datetime import datetime

_ROOT = Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.admin_guard import require_admin
if not require_admin():
    import streamlit as st
    st.stop()

import streamlit as st
from src.page_header import render_om_symbol, render_page_quote

st.set_page_config(
    page_title="Admin: Upload Sources",
    page_icon="🔐",
    layout="wide"
)

DATA_DIR    = Path(__file__).parent.parent / "data"
RAW_DIR     = DATA_DIR / "raw"
STATUS_FILE = DATA_DIR / "kb_status.json"
RAW_DIR.mkdir(parents=True, exist_ok=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Lato:wght@300;400;700&family=Cormorant+Garamond:ital@1&display=swap');
html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#F8F9F5;color:#1A3A28;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#2A5C3A!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#EDF3EC,#E0EBE2)!important;border-right:2px solid #B8D4BC;}
div[data-testid="stSidebar"] *{color:#2A4A38!important;font-weight:600!important;}
.stButton>button{background:linear-gradient(135deg,#4A7C59,#6A9E78);color:white!important;
    border:none;border-radius:8px;font-weight:700;padding:.6rem 1.4rem;
    font-size:1rem;transition:all .3s;}
.stButton>button:hover{background:linear-gradient(135deg,#2A5C3A,#4A7C59);transform:translateY(-2px);}
.page-header{background:linear-gradient(135deg,#EDF3EC,#E4EDE4);border:2px solid #B8D4BC;
    border-radius:18px;padding:2rem;text-align:center;margin-bottom:1.5rem;}
.page-header-title{font-family:'Playfair Display',serif;font-size:2rem;font-weight:800;color:#2A5C3A;}
.page-header-sub{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.1rem;color:#4A7C59;}
.kb-ready{background:#E8F5E9;border:2px solid #4CAF50;border-radius:12px;padding:1rem 1.5rem;margin-bottom:1.5rem;}
.kb-stale{background:#FFF8E7;border:2px solid #FFA000;border-radius:12px;padding:1rem 1.5rem;margin-bottom:1.5rem;}
.kb-empty{background:#EDF3EC;border:2px solid #B8D4BC;border-radius:12px;padding:1rem 1.5rem;margin-bottom:1.5rem;}
.kb-title{font-weight:700;font-size:1rem;margin-bottom:.2rem;color:#1A3A28;}
.kb-detail{font-size:.85rem;color:#3A5040;}
.section-card{background:white;border:2px solid #B8D4BC;border-radius:14px;
    padding:1.8rem;margin-bottom:1.5rem;box-shadow:0 2px 10px rgba(74,124,89,.06);}
.section-title{font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:700;
    color:#2A5C3A;margin-bottom:1rem;padding-bottom:.4rem;border-bottom:2px solid #B8D4BC;}
.upload-hint{background:#EDF3EC;border-radius:10px;padding:1rem 1.2rem;
    font-size:.9rem;color:#3A5040;margin-bottom:1rem;border-left:4px solid #4A7C59;line-height:1.7;}
.workflow-step{display:flex;align-items:flex-start;gap:.8rem;margin-bottom:.6rem;
    font-size:.9rem;color:#3A5040;}
.workflow-num{background:#4A7C59;color:white;border-radius:50%;width:22px;height:22px;
    display:flex;align-items:center;justify-content:center;
    font-size:.75rem;font-weight:700;flex-shrink:0;margin-top:.1rem;}
</style>
""", unsafe_allow_html=True)

render_om_symbol()

st.markdown("""
<div class="page-header">
    <div style="font-size:2rem;margin-bottom:.3rem;">📤</div>
    <div class="page-header-title">Admin · Upload Sources</div>
    <div class="page-header-sub">Upload transcripts and books to the knowledge base</div>
</div>
""", unsafe_allow_html=True)

render_page_quote(
    "A heart filled with <strong>noble emotions</strong> like kindness, "
    "compassion, mercy, truthfulness, honesty — such a heart is called "
    "a <strong>pure heart</strong>."
)

# ── KB Status ──────────────────────────────────────────────────────────────────
raw_files = sorted(RAW_DIR.glob("*.*"))
kb_data = {}
if STATUS_FILE.exists():
    try:
        kb_data = json.loads(STATUS_FILE.read_text())
    except Exception:
        pass

if kb_data.get("chunks", 0) > 0:
    st.markdown(f"""
    <div class="kb-ready">
        <div class="kb-title">✅ Knowledge Base is UP TO DATE</div>
        <div class="kb-detail">Last built: {kb_data.get('built_at','Unknown')} &nbsp;·&nbsp;
        {kb_data.get('chunks',0):,} chunks &nbsp;·&nbsp; {kb_data.get('sources',0)} sources</div>
    </div>""", unsafe_allow_html=True)
elif raw_files:
    st.markdown(f"""
    <div class="kb-stale">
        <div class="kb-title">⚠️ Knowledge Base needs rebuilding</div>
        <div class="kb-detail">{len(raw_files)} file(s) uploaded but not yet indexed.
        Go to Admin → Build Knowledge Base.</div>
    </div>""", unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="kb-empty">
        <div class="kb-title">📭 No sources uploaded yet</div>
        <div class="kb-detail">Upload discourse transcripts or book PDFs below.</div>
    </div>""", unsafe_allow_html=True)

# ── Two Tabs ───────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🎙️ Discourse Transcripts", "📖 Books & Articles (PDF)"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DISCOURSE TRANSCRIPTS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class="upload-hint">
        <strong>Recommended workflow:</strong><br>
        <div class="workflow-step">
            <div class="workflow-num">1</div>
            <div>Go to <strong>Wisdom Distiller</strong>
            (wisdomdistiller.vedantadhara.com) and upload Swamiji's audio or video</div>
        </div>
        <div class="workflow-step">
            <div class="workflow-num">2</div>
            <div>Download the transcript as <strong>TXT or DOCX</strong></div>
        </div>
        <div class="workflow-step">
            <div class="workflow-num">3</div>
            <div>Upload that file here and fill in the metadata below</div>
        </div>
        <div class="workflow-step">
            <div class="workflow-num">4</div>
            <div>Go to <strong>Admin → Build Knowledge Base</strong> to index</div>
        </div>
        <br>✅ &nbsp;<strong>Accepted formats:</strong> TXT, DOCX, PDF
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-title">Transcript Details</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        t_speaker   = st.text_input("Speaker",
                          value="Swami Aparajitananda", key="t_spk")
        t_topic     = st.text_input("Talk / Series Title",
                          placeholder="e.g. Value of Values — Discourse 1",
                          key="t_topic")
        t_scripture = st.text_input("Scripture",
                          value="Bhagavad Gītā", key="t_script")
    with col2:
        t_chapter   = st.text_input("Chapter", value="13", key="t_ch")
        t_verse     = st.text_input("Verse Range", value="7-11", key="t_vr")
        t_lang      = st.selectbox("Language",
                          ["English","Hindi","Kannada","Telugu","Tamil","Marathi"],
                          key="t_lang")

    t_type = st.selectbox("Transcript Type",
                 ["discourse_transcript","story_transcript",
                  "satsang_transcript","lecture_notes","other"],
                 key="t_type")

    st.markdown("---")

    t_files = st.file_uploader(
        "📂 Select transcript files (TXT, DOCX or PDF)",
        type=["txt","docx","pdf"],
        accept_multiple_files=True,
        key="t_up"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⬆️ Upload Transcripts to Knowledge Base",
                 use_container_width=True, key="t_btn"):
        if not t_files:
            st.warning("⚠️ Please select at least one file first.")
        else:
            meta = dict(
                speaker=t_speaker, topic=t_topic,
                scripture=t_scripture, chapter=t_chapter,
                verse_range=t_verse, language=t_lang,
                source_type=t_type,
                uploaded_at=datetime.now().isoformat()
            )
            count = 0
            for uf in t_files:
                dest = RAW_DIR / uf.name
                dest.write_bytes(uf.read())
                count += 1
                try:
                    from src.ingestion import ingest_file
                    ingest_file(str(dest), meta)
                    st.success(f"✅ {uf.name} — uploaded and processed")
                except Exception:
                    st.success(f"✅ {uf.name} — saved ({uf.size/1024:.1f} KB)")
            if count:
                st.info(f"🔨 {count} transcript(s) ready. "
                        f"Go to **Admin → Build Knowledge Base** to index them.")

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — BOOKS & ARTICLES
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="upload-hint">
        Upload Swamiji's published books or spiritual articles in
        <strong>PDF format</strong>. Examples:
        <ul style="margin:.5rem 0 0 1rem;line-height:2.2;">
            <li>Indispensable Values (2022)</li>
            <li>Gurudev's Quotes I, II, III</li>
            <li>Read Daily, Live Fully</li>
            <li>Any published book or article by Swamiji</li>
        </ul>
        <br>✅ &nbsp;<strong>Accepted formats:</strong> PDF only
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-title">Book / Article Details</div>',
                unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        b_author    = st.text_input("Author",
                          value="Swami Aparajitananda", key="b_author")
        b_title     = st.text_input("Book / Article Title",
                          placeholder="e.g. Indispensable Values",
                          key="b_title")
        b_publisher = st.text_input("Publisher",
                          value="Central Chinmaya Mission Trust",
                          key="b_pub")
    with col4:
        b_year      = st.text_input("Year Published",
                          placeholder="e.g. 2022", key="b_year")
        b_scripture = st.text_input("Scripture Reference",
                          placeholder="e.g. Bhagavad Gītā Ch.13",
                          key="b_script")
        b_lang      = st.selectbox("Language",
                          ["English","Hindi","Kannada","Telugu","Tamil","Marathi"],
                          key="b_lang")

    b_type = st.selectbox("Content Type",
                 ["book_chapter","full_book","article","commentary","other"],
                 key="b_type")

    st.markdown("---")

    b_files = st.file_uploader(
        "📂 Select PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        key="b_up"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⬆️ Upload Books / Articles to Knowledge Base",
                 use_container_width=True, key="b_btn"):
        if not b_files:
            st.warning("⚠️ Please select at least one PDF file first.")
        else:
            meta = dict(
                speaker=b_author, topic=b_title,
                scripture=b_scripture, publisher=b_publisher,
                year=b_year, language=b_lang,
                source_type=b_type,
                uploaded_at=datetime.now().isoformat()
            )
            count = 0
            for uf in b_files:
                dest = RAW_DIR / uf.name
                dest.write_bytes(uf.read())
                count += 1
                try:
                    from src.ingestion import ingest_file
                    ingest_file(str(dest), meta)
                    st.success(f"✅ {uf.name} — uploaded and processed")
                except Exception:
                    st.success(f"✅ {uf.name} — saved ({uf.size/1024:.1f} KB)")
            if count:
                st.info(f"📚 {count} book/article(s) ready. "
                        f"Go to **Admin → Build Knowledge Base** to index them.")

    st.markdown('</div>', unsafe_allow_html=True)

# ── Uploaded Files List ────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">📁 Uploaded Files</div>',
            unsafe_allow_html=True)

raw_files = sorted(RAW_DIR.glob("*.*"))

if not raw_files:
    st.info("No files uploaded yet.")
else:
    st.caption(f"{len(raw_files)} file(s) in knowledge base source folder")

    _, col_del_all = st.columns([4, 1])
    with col_del_all:
        if st.button("🗑️ Delete ALL", key="del_all"):
            st.session_state["confirm_delete_all"] = True

    if st.session_state.get("confirm_delete_all"):
        st.warning("⚠️ Delete ALL source files?")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Yes, delete all", key="yes_all"):
                for f in raw_files:
                    f.unlink(missing_ok=True)
                st.session_state["confirm_delete_all"] = False
                st.success("All files deleted.")
                st.rerun()
        with c2:
            if st.button("❌ Cancel", key="no_all"):
                st.session_state["confirm_delete_all"] = False
                st.rerun()

    st.divider()

    for i, fpath in enumerate(raw_files):
        size_kb = fpath.stat().st_size / 1024
        ext  = fpath.suffix.upper().lstrip(".")
        icon = {"PDF":"📄","DOCX":"📝","TXT":"📃"}.get(ext, "📎")
        c1, c2, c3, c4 = st.columns([0.3, 3, 1, 0.8])
        with c1: st.write(icon)
        with c2: st.write(f"**{fpath.name}**")
        with c3: st.write(f"{size_kb:.1f} KB")
        with c4:
            if st.button("🗑️", key=f"del_{i}", help=f"Delete {fpath.name}"):
                st.session_state[f"confirm_del_{i}"] = True

        if st.session_state.get(f"confirm_del_{i}"):
            st.warning(f"Delete **{fpath.name}**?")
            cy, cn = st.columns(2)
            with cy:
                if st.button("Yes", key=f"yes_{i}"):
                    fpath.unlink(missing_ok=True)
                    st.session_state[f"confirm_del_{i}"] = False
                    st.success(f"Deleted {fpath.name}")
                    st.rerun()
            with cn:
                if st.button("No", key=f"no_{i}"):
                    st.session_state[f"confirm_del_{i}"] = False
                    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
