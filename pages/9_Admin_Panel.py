"""
pages/7_Admin_Panel.py — Consolidated admin panel.
ONE password entry → access to Upload, Build KB, and Settings in tabs.

Replaces (and supersedes) the previous three separate admin pages:
  - 7_Admin_Upload_Sources.py
  - 8_Admin_Build_Knowledge_Base.py
  - 9_Admin_Settings.py
"""
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

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
    page_title="Admin Panel | Indispensable Values",
    page_icon="🔐",
    layout="wide",
)

# ── Paths ──────────────────────────────────────────────────────────────────────
DATA_DIR      = _ROOT / "data"
RAW_DIR       = DATA_DIR / "raw"
REGISTRY_PATH = DATA_DIR / "processed" / "source_registry.json"
STATUS_FILE   = DATA_DIR / "kb_status.json"
RAW_DIR.mkdir(parents=True, exist_ok=True)
REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Lato:wght@300;400;700&family=Cormorant+Garamond:ital@1&display=swap');
html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#E8F4F6;color:#0A1E28;font-weight:500;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#062E3A!important;font-weight:800!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#FFFFFF,#A8D8E0)!important;border-right:2px solid #88C5D0;}
div[data-testid="stSidebar"] *{color:#0A1E28!important;font-weight:600!important;}
.stButton>button{background:linear-gradient(135deg,#0D5C6B,#2C95A8);color:white!important;border:none;border-radius:8px;font-weight:700;padding:.6rem 1.4rem;transition:all .3s;}
.stButton>button:hover{background:linear-gradient(135deg,#062E3A,#0D5C6B);transform:translateY(-2px);}

.page-header{background:linear-gradient(135deg,#FFFFFF,#D0EDF1);border:2px solid #88C5D0;
    border-radius:18px;padding:2rem;text-align:center;margin-bottom:1.5rem;
    box-shadow:0 4px 20px rgba(0,0,0,.08);}
.page-header-title{font-family:'Playfair Display',serif;font-size:2.2rem;font-weight:800;color:#062E3A;}
.page-header-sub{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.1rem;color:#0D5C6B;}

.kb-ready{background:#E8F5E9;border:2px solid #4CAF50;border-radius:12px;padding:1rem 1.5rem;margin-bottom:1.5rem;}
.kb-stale{background:#FFF8E7;border:2px solid #FFA000;border-radius:12px;padding:1rem 1.5rem;margin-bottom:1.5rem;}
.kb-empty{background:#FFFFFF;border:2px solid #88C5D0;border-radius:12px;padding:1rem 1.5rem;margin-bottom:1.5rem;}
.kb-title{font-weight:700;font-size:1rem;margin-bottom:.2rem;color:#0A1E28;}
.kb-detail{font-size:.85rem;color:#1A3A45;}

.section-card{background:#FFFFFF;border:2px solid #88C5D0;border-radius:14px;padding:1.8rem;margin-bottom:1.5rem;box-shadow:0 2px 10px rgba(0,0,0,.06);}
.section-title{font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:700;color:#062E3A;margin-bottom:1rem;padding-bottom:.4rem;border-bottom:2px solid #88C5D0;}

.stat-card{background:#FFFFFF;border:1.5px solid #88C5D0;border-radius:12px;padding:1.1rem;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.06);}
.stat-number{font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:800;color:#0D5C6B;}
.stat-label{color:#1A3A45;font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-top:.2rem;}

.upload-hint{background:#FFFFFF;border-radius:10px;padding:1rem 1.2rem;font-size:.9rem;
    color:#1A3A45;margin-bottom:1rem;border-left:4px solid #0D5C6B;line-height:1.7;}
.workflow-step{display:flex;align-items:flex-start;gap:.8rem;margin-bottom:.6rem;font-size:.9rem;color:#1A3A45;}
.workflow-num{background:#0D5C6B;color:white;border-radius:50%;width:22px;height:22px;
    display:flex;align-items:center;justify-content:center;
    font-size:.75rem;font-weight:700;flex-shrink:0;margin-top:.1rem;}

.file-row{display:flex;align-items:center;gap:.8rem;background:#FFFFFF;
    border:1px solid #88C5D0;border-radius:8px;padding:.6rem 1rem;
    margin-bottom:.4rem;font-size:.9rem;}

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
    <div class="page-header-title">Admin Panel</div>
    <div class="page-header-sub">Manage sources, build knowledge base, and configure settings</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="swamiji-quote-pg">
    &ldquo;Whatever you may offer — it doesn&rsquo;t matter. What Bhagavān sees is the <strong>devotion</strong> with which you offer.&rdquo;
    <span class="swamiji-quote-pg-attr">— Swāmī Aparājitānanda</span>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# THREE TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_upload, tab_build, tab_settings = st.tabs([
    "📤 Upload Sources",
    "🔨 Build Knowledge Base",
    "⚙️ Settings"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — UPLOAD SOURCES
# ══════════════════════════════════════════════════════════════════════════════
with tab_upload:
    # ── KB Status ──────────────────────────────────────────────────────────────
    raw_files = sorted(RAW_DIR.glob("*.*"))
    kb_data = {}
    if STATUS_FILE.exists():
        try:
            kb_data = json.loads(STATUS_FILE.read_text())
        except Exception:
            pass

    if kb_data.get("chunks", 0) > 0:
        st.markdown(f"""<div class="kb-ready">
            <div class="kb-title">✅ Knowledge Base is UP TO DATE</div>
            <div class="kb-detail">Last built: {kb_data.get('built_at','Unknown')} &nbsp;·&nbsp;
            {kb_data.get('chunks',0):,} chunks &nbsp;·&nbsp; {kb_data.get('sources',0)} sources</div>
        </div>""", unsafe_allow_html=True)
    elif raw_files:
        st.markdown(f"""<div class="kb-stale">
            <div class="kb-title">⚠️ Knowledge Base needs rebuilding</div>
            <div class="kb-detail">{len(raw_files)} file(s) uploaded but not yet indexed.
            Switch to the <strong>Build Knowledge Base</strong> tab.</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="kb-empty">
            <div class="kb-title">📭 No sources uploaded yet</div>
            <div class="kb-detail">Upload discourse transcripts or book PDFs below.</div>
        </div>""", unsafe_allow_html=True)

    # ── Two Upload Sub-tabs ────────────────────────────────────────────────────
    sub1, sub2 = st.tabs(["🎙️ Discourse Transcripts", "📖 Books & Articles (PDF)"])

    with sub1:
        st.markdown("""<div class="upload-hint">
            <strong>Recommended workflow:</strong><br>
            <div class="workflow-step"><div class="workflow-num">1</div>
            <div>Go to <strong>Wisdom Distiller</strong> and upload Swamiji's audio or video</div></div>
            <div class="workflow-step"><div class="workflow-num">2</div>
            <div>Download the transcript as <strong>TXT or DOCX</strong></div></div>
            <div class="workflow-step"><div class="workflow-num">3</div>
            <div>Upload that file here and fill in the metadata below</div></div>
            <div class="workflow-step"><div class="workflow-num">4</div>
            <div>Switch to <strong>Build Knowledge Base</strong> tab to index</div></div>
            <br>✅ &nbsp;<strong>Accepted formats:</strong> TXT, DOCX, PDF
        </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            t_speaker   = st.text_input("Speaker", value="Swami Aparajitananda", key="t_spk")
            t_topic     = st.text_input("Talk / Series Title",
                            placeholder="e.g. Value of Values — Discourse 1", key="t_topic")
            t_scripture = st.text_input("Scripture", value="Bhagavad Gītā", key="t_script")
        with col2:
            t_chapter   = st.text_input("Chapter", value="13", key="t_ch")
            t_verse     = st.text_input("Verse Range", value="7-11", key="t_vr")
            t_lang      = st.selectbox("Language",
                            ["English","Hindi","Kannada","Telugu","Tamil","Marathi"],
                            key="t_lang")
        t_type = st.selectbox("Transcript Type",
                     ["discourse_transcript","story_transcript",
                      "satsang_transcript","lecture_notes","other"], key="t_type")

        t_files = st.file_uploader("📂 Select transcript files",
            type=["txt","docx","pdf"], accept_multiple_files=True, key="t_up")

        if st.button("⬆️ Upload Transcripts", use_container_width=True, key="t_btn"):
            if not t_files:
                st.warning("⚠️ Please select at least one file first.")
            else:
                meta = dict(speaker=t_speaker, topic=t_topic, scripture=t_scripture,
                            chapter=t_chapter, verse_range=t_verse, language=t_lang,
                            source_type=t_type, uploaded_at=datetime.now().isoformat())
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
                            f"Go to **Build Knowledge Base** tab to index them.")

    with sub2:
        st.markdown("""<div class="upload-hint">
            Upload Swamiji's books or articles in <strong>PDF format</strong>:
            <ul style="margin:.5rem 0 0 1rem;line-height:2.2;">
                <li>Indispensable Values (2022)</li>
                <li>Gurudev's Quotes I, II, III</li>
                <li>Read Daily, Live Fully</li>
                <li>Any published work or article</li>
            </ul>
            <br>✅ &nbsp;<strong>Accepted formats:</strong> PDF only
        </div>""", unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            b_author    = st.text_input("Author", value="Swami Aparajitananda", key="b_auth")
            b_title     = st.text_input("Book / Article Title",
                            placeholder="e.g. Indispensable Values", key="b_title")
            b_publisher = st.text_input("Publisher",
                            value="Central Chinmaya Mission Trust", key="b_pub")
        with col4:
            b_year      = st.text_input("Year Published", placeholder="e.g. 2022", key="b_year")
            b_scripture = st.text_input("Scripture Reference",
                            placeholder="e.g. Bhagavad Gītā Ch.13", key="b_scr")
            b_lang      = st.selectbox("Language",
                            ["English","Hindi","Kannada","Telugu","Tamil","Marathi"],
                            key="b_lang")
        b_type = st.selectbox("Content Type",
                     ["book_chapter","full_book","article","commentary","other"],
                     key="b_type")

        b_files = st.file_uploader("📂 Select PDF files",
            type=["pdf"], accept_multiple_files=True, key="b_up")

        if st.button("⬆️ Upload Books / Articles", use_container_width=True, key="b_btn"):
            if not b_files:
                st.warning("⚠️ Please select at least one PDF first.")
            else:
                meta = dict(speaker=b_author, topic=b_title, scripture=b_scripture,
                            publisher=b_publisher, year=b_year, language=b_lang,
                            source_type=b_type, uploaded_at=datetime.now().isoformat())
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
                    st.info(f"📚 {count} book(s) ready. "
                            f"Go to **Build Knowledge Base** tab to index them.")

    # ── Uploaded Files List ────────────────────────────────────────────────────
    st.markdown('<div class="section-card"><div class="section-title">📁 Uploaded Files</div>',
                unsafe_allow_html=True)
    raw_files = sorted(RAW_DIR.glob("*.*"))
    if not raw_files:
        st.info("No files uploaded yet.")
    else:
        st.caption(f"{len(raw_files)} file(s)")
        _, col_del_all = st.columns([4, 1])
        with col_del_all:
            if st.button("🗑️ Delete ALL", key="del_all_up"):
                st.session_state["confirm_del_all_up"] = True
        if st.session_state.get("confirm_del_all_up"):
            st.warning("⚠️ Delete ALL source files?")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Yes", key="yes_all_up"):
                    for f in raw_files:
                        f.unlink(missing_ok=True)
                    st.session_state["confirm_del_all_up"] = False
                    st.success("All files deleted.")
                    st.rerun()
            with c2:
                if st.button("❌ Cancel", key="no_all_up"):
                    st.session_state["confirm_del_all_up"] = False
                    st.rerun()
        st.divider()
        for i, fpath in enumerate(raw_files):
            size_kb = fpath.stat().st_size / 1024
            ext = fpath.suffix.upper().lstrip(".")
            icon = {"PDF":"📄","DOCX":"📝","TXT":"📃"}.get(ext,"📎")
            c1, c2, c3, c4 = st.columns([0.3, 3, 1, 0.8])
            with c1: st.write(icon)
            with c2: st.write(f"**{fpath.name}**")
            with c3: st.write(f"{size_kb:.1f} KB")
            with c4:
                if st.button("🗑️", key=f"del_up_{i}"):
                    fpath.unlink(missing_ok=True)
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — BUILD KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════════════════════
with tab_build:
    try:
        from src.ingestion import (
            extract_text, build_source_record, compute_file_hash,
            clean_discourse_transcript, clean_story_transcript,
            detect_story_format, extract_discourse_metadata,
            load_source_registry, save_source_registry, mark_source_processed,
        )
        from src.chunking import build_chunk_documents
        from src.embeddings import get_embeddings
        from src.vector_store import (
            add_chunks_to_store, get_collection_stats,
            delete_chunks_by_source, clear_collection,
        )
        PIPELINE_OK = True
    except ImportError as e:
        PIPELINE_OK = False
        PIPELINE_ERR = str(e)

    raw_files = sorted(RAW_DIR.glob("*.*"))
    try:
        stats = get_collection_stats() if PIPELINE_OK else {}
    except Exception:
        stats = {}

    # Stats
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(f"""<div class="stat-card">
            <div class="stat-number">{len(raw_files)}</div>
            <div class="stat-label">Files Ready</div>
        </div>""", unsafe_allow_html=True)
    with s2:
        st.markdown(f"""<div class="stat-card">
            <div class="stat-number">{stats.get('total_chunks',0):,}</div>
            <div class="stat-label">Chunks in DB</div>
        </div>""", unsafe_allow_html=True)
    with s3:
        ready_txt = "✅ Ready" if stats.get('total_chunks',0) > 0 else "⏳ Not Built"
        st.markdown(f"""<div class="stat-card">
            <div class="stat-number" style="font-size:1.2rem;">{ready_txt}</div>
            <div class="stat-label">Query Status</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if not PIPELINE_OK:
        st.error(f"⚠️ Pipeline error: {PIPELINE_ERR}")
        st.stop()

    if not raw_files:
        st.info("📭 No source files. Upload files in the **Upload Sources** tab first.")
    else:
        # Build settings
        st.markdown('<div class="section-card"><div class="section-title">⚙️ Build Settings</div>',
                    unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            chunk_size = st.slider("Chunk Size (chars)", 600, 1800, 1000, 100)
            chunk_overlap = st.slider("Chunk Overlap (chars)", 100, 400, 200, 50)
        with col_b:
            embedding_model = st.selectbox("Embedding Model",
                ["text-embedding-3-small","text-embedding-3-large"])
            reprocess = st.checkbox("Re-process indexed files", value=False)
            clean_txt = st.checkbox("Clean transcripts", value=True)

        est = len(raw_files) * 30
        st.caption(f"💡 Estimated cost: ~${est * 250 * 0.00002 / 1000:.4f} USD")
        st.markdown('</div>', unsafe_allow_html=True)

        # Build button
        if st.button("🚀 Build Knowledge Base", use_container_width=True, type="primary"):
            progress = st.progress(0)
            status   = st.empty()
            log      = st.container()
            embeddings = get_embeddings(embedding_model)
            total_chunks = 0
            errors = 0

            for idx, fpath in enumerate(raw_files):
                progress.progress(idx / len(raw_files))
                status.markdown(f"**Processing ({idx+1}/{len(raw_files)}):** `{fpath.name}`")
                try:
                    text, meta = extract_text(fpath)
                    if detect_story_format(text):
                        text = clean_story_transcript(text)
                    elif "Discourse" in text or "DISCOURSE" in text:
                        em = extract_discourse_metadata(text)
                        meta.update({k:v for k,v in em.items() if v})
                        text = clean_discourse_transcript(text)
                    record = build_source_record(
                        file_path=fpath,
                        metadata={**meta, "file_path": str(fpath),
                                  "source_type": meta.get("source_type","document")},
                        source_type=meta.get("source_type","document"),
                    )
                    source_id = record["source_id"]
                    if reprocess:
                        try: delete_chunks_by_source(source_id)
                        except: pass
                    chunks = build_chunk_documents(text, record,
                        chunk_size=chunk_size, overlap=chunk_overlap)
                    if not chunks:
                        log.warning(f"⚠️ No chunks: {fpath.name}")
                        continue
                    n_added = add_chunks_to_store(chunks, embeddings, batch_size=50)
                    total_chunks += n_added
                    reg = load_source_registry(REGISTRY_PATH)
                    reg = [r for r in reg if r.get("source_id") != source_id]
                    reg.append(record)
                    save_source_registry(reg, REGISTRY_PATH)
                    mark_source_processed(source_id, n_added, REGISTRY_PATH)
                    log.success(f"✅ {fpath.name} — {n_added} chunks")
                except Exception as e:
                    log.error(f"❌ {fpath.name}: {e}")
                    errors += 1

            progress.progress(1.0)
            status.empty()

            new_stats = get_collection_stats()
            STATUS_FILE.write_text(json.dumps({
                "built_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "chunks":   new_stats.get("total_chunks", 0),
                "sources":  len(raw_files) - errors,
                "errors":   errors,
            }, indent=2))

            if total_chunks > 0:
                st.success(f"🎉 **{total_chunks:,}** chunks indexed from "
                           f"**{len(raw_files)-errors}** file(s).")
                st.balloons()
            else:
                st.error("❌ No chunks indexed.")

        # Danger zone
        st.divider()
        with st.expander("⚠️ Danger Zone — Clear Vector Database"):
            st.warning("This deletes ALL chunks. Source files are kept.")
            if st.button("🗑️ Clear Vector Database"):
                try:
                    clear_collection()
                    STATUS_FILE.write_text(json.dumps({"chunks":0,"sources":0}))
                    st.success("✅ Cleared.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ {e}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — SETTINGS
# ══════════════════════════════════════════════════════════════════════════════
with tab_settings:
    # API Key Status
    st.markdown('<div class="section-card"><div class="section-title">🔑 API Key Status</div>',
                unsafe_allow_html=True)
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    if api_key:
        st.success(f"✅ OpenAI API key configured (`{api_key[:8]}...{api_key[-4:]}`)")
    else:
        st.error("❌ OPENAI_API_KEY not found in Streamlit secrets.")
        st.code('OPENAI_API_KEY = "sk-..."', language="toml")
    st.markdown('</div>', unsafe_allow_html=True)

    # Model Info
    st.markdown('<div class="section-card"><div class="section-title">🤖 Model Configuration</div>',
                unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Chat Model**")
        st.info("Currently using: **gpt-4o-mini**\n\n"
                "- Excellent quality answers\n"
                "- ~$0.0005 per Q&A query\n"
                "- Fast response time")
    with c2:
        st.markdown("**Embedding Model**")
        st.info("Currently using: **text-embedding-3-small**\n\n"
                "- 1536 dimensions\n"
                "- $0.02 per 1M tokens\n"
                "- Excellent quality for similarity search")
    st.markdown('</div>', unsafe_allow_html=True)

    # Knowledge Base Stats
    st.markdown('<div class="section-card"><div class="section-title">📊 Knowledge Base Stats</div>',
                unsafe_allow_html=True)
    try:
        from src.vector_store import get_collection_stats
        stats = get_collection_stats()
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Total Chunks", f"{stats.get('total_chunks',0):,}")
        with c2: st.metric("Total Sources", stats.get('total_sources', 0))
        with c3: st.metric("Speakers", len(stats.get('speakers', [])))
        with c4: st.metric("Scriptures", len(stats.get('scriptures', [])))
    except Exception as e:
        st.info("Knowledge base not yet built.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Cost Calculator
    st.markdown('<div class="section-card"><div class="section-title">💰 Cost Calculator</div>',
                unsafe_allow_html=True)
    st.caption("Estimate costs before processing documents")
    cc1, cc2 = st.columns(2)
    with cc1:
        num_docs   = st.number_input("Number of documents", 1, 500, 10, key="cc_docs")
        avg_pages  = st.number_input("Average length (pages)", 1, 300, 40, key="cc_pages")
    with cc2:
        words_per  = st.number_input("Words per page", 100, 400, 150, key="cc_wpp")
        queries    = st.number_input("Expected Q&A queries/month", 0, 10000, 500, key="cc_q")

    total_words = num_docs * avg_pages * words_per
    total_tokens = total_words * 1.33
    embed_cost = total_tokens * 0.02 / 1_000_000
    query_cost = queries * 0.0005

    st.markdown(f"""
    **One-time embedding cost:** ${embed_cost:.4f} USD
    **Monthly Q&A queries:** ${query_cost:.4f} USD
    **First month total:** **${embed_cost + query_cost:.4f} USD**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # App info
    st.markdown('<div class="section-card"><div class="section-title">🪷 About This Instance</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
    - **App:** Indispensable Values Q&A
    - **Knowledge Base:** Bhagavad Gītā Chapters 13 & 16
    - **Sources:** Swamiji's discourses, books, and articles
    - **Data Directory:** `{DATA_DIR}`
    """)
    st.markdown('</div>', unsafe_allow_html=True)
