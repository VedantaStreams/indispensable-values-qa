"""
pages/8_Admin_Build_Knowledge_Base.py — Admin only. Password protected.
Processes uploaded files → chunks → embeddings → ChromaDB vector store.
"""
import sys
import json
import time
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
    page_title="Admin: Build Knowledge Base",
    page_icon="🔨",
    layout="wide"
)

# ── Paths ──────────────────────────────────────────────────────────────────────
DATA_DIR      = _ROOT / "data"
RAW_DIR       = DATA_DIR / "raw"
REGISTRY_PATH = DATA_DIR / "processed" / "source_registry.json"
STATUS_FILE   = DATA_DIR / "kb_status.json"
RAW_DIR.mkdir(parents=True, exist_ok=True)
REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Lato:wght@300;400;700&family=Cormorant+Garamond:ital@1&display=swap');
html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#F8F9F5;color:#1A3A28;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#2A5C3A!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#EDF3EC,#E0EBE2)!important;border-right:2px solid #B8D4BC;}
div[data-testid="stSidebar"] *{color:#2A4A38!important;font-weight:600!important;}
.stButton>button{background:linear-gradient(135deg,#4A7C59,#6A9E78);color:white!important;
    border:none;border-radius:8px;font-weight:700;padding:.6rem 1.4rem;font-size:1rem;transition:all .3s;}
.stButton>button:hover{background:linear-gradient(135deg,#2A5C3A,#4A7C59);transform:translateY(-2px);}
.page-header{background:linear-gradient(135deg,#EDF3EC,#E4EDE4);border:2px solid #B8D4BC;
    border-radius:18px;padding:2rem;text-align:center;margin-bottom:1.5rem;}
.page-header-title{font-family:'Playfair Display',serif;font-size:2rem;font-weight:800;color:#2A5C3A;}
.page-header-sub{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.1rem;color:#4A7C59;}
.stat-card{background:white;border:1.5px solid #B8D4BC;border-radius:12px;
    padding:1.1rem;text-align:center;box-shadow:0 2px 8px rgba(74,124,89,.06);}
.stat-number{font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:800;color:#4A7C59;}
.stat-label{color:#3A5040;font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-top:.2rem;}
.section-card{background:white;border:2px solid #B8D4BC;border-radius:14px;
    padding:1.8rem;margin-bottom:1.5rem;box-shadow:0 2px 10px rgba(74,124,89,.06);}
.section-title{font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:700;
    color:#2A5C3A;margin-bottom:1rem;padding-bottom:.4rem;border-bottom:2px solid #B8D4BC;}
.file-row{display:flex;align-items:center;gap:.8rem;background:#EDF3EC;
    border:1px solid #B8D4BC;border-radius:8px;padding:.6rem 1rem;margin-bottom:.4rem;font-size:.9rem;}
</style>
""", unsafe_allow_html=True)

render_om_symbol()

st.markdown("""
<div class="page-header">
    <div style="font-size:2rem;margin-bottom:.3rem;">🔨</div>
    <div class="page-header-title">Admin · Build Knowledge Base</div>
    <div class="page-header-sub">Process, chunk, embed and index uploaded sources</div>
</div>
""", unsafe_allow_html=True)

render_page_quote(
    "Reforming oneself is like <strong>chiselling a stone</strong> to perfection!"
)

# ── Import pipeline modules ────────────────────────────────────────────────────
try:
    from src.ingestion import (
        extract_text, save_raw_text, load_raw_text,
        clean_discourse_transcript, extract_discourse_metadata,
        clean_story_transcript, detect_story_format,
        load_source_registry, save_source_registry,
        mark_source_processed, build_source_record, compute_file_hash,
    )
    from src.chunking import build_chunk_documents
    from src.embeddings import get_embeddings
    from src.vector_store import (
        add_chunks_to_store, get_collection_stats,
        delete_chunks_by_source, clear_collection,
    )
    PIPELINE_AVAILABLE = True
except ImportError as e:
    PIPELINE_AVAILABLE = False
    PIPELINE_ERROR = str(e)

# ── Stats ──────────────────────────────────────────────────────────────────────
raw_files = sorted(RAW_DIR.glob("*.*"))
n_files   = len(raw_files)

try:
    stats = get_collection_stats() if PIPELINE_AVAILABLE else {}
except Exception:
    stats = {}

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-number">{n_files}</div>
        <div class="stat-label">Files Uploaded</div>
    </div>""", unsafe_allow_html=True)
with s2:
    st.markdown(f"""<div class="stat-card">
        <div class="stat-number">{stats.get('total_chunks', 0):,}</div>
        <div class="stat-label">Chunks in DB</div>
    </div>""", unsafe_allow_html=True)
with s3:
    ready = "✅ Ready" if stats.get('total_chunks', 0) > 0 else "⏳ Not Built"
    st.markdown(f"""<div class="stat-card">
        <div class="stat-number" style="font-size:1.2rem;">{ready}</div>
        <div class="stat-label">Query Status</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Pipeline error notice ──────────────────────────────────────────────────────
if not PIPELINE_AVAILABLE:
    st.error(f"⚠️ Pipeline not available: {PIPELINE_ERROR}")
    st.info("The core pipeline modules (chunking, embeddings, vector store) "
            "need to be properly set up before building the knowledge base.")
    st.stop()

# ── No files notice ────────────────────────────────────────────────────────────
if not raw_files:
    st.info("📭 No source files found. "
            "Go to **Admin → Upload Sources** to upload transcripts and books first.")
    st.stop()

# ── File list ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">📁 Files Ready to Process</div>',
            unsafe_allow_html=True)

for fpath in raw_files:
    size_kb = fpath.stat().st_size / 1024
    ext  = fpath.suffix.upper().lstrip(".")
    icon = {"PDF":"📄","DOCX":"📝","TXT":"📃"}.get(ext,"📎")
    st.markdown(f"""<div class="file-row">
        <span>{icon}</span>
        <span><strong>{fpath.name}</strong></span>
        <span style="color:#4A7C59;font-size:.82rem;">{size_kb:.1f} KB · {ext}</span>
    </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Settings ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">⚙️ Build Settings</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    chunk_size    = st.slider("Chunk Size (characters)", 600, 1800, 1000, 100,
                        help="Size of each text chunk. 1000 works well for discourses.")
    chunk_overlap = st.slider("Chunk Overlap (characters)", 100, 400, 200, 50,
                        help="Overlap between chunks for context continuity.")
with col2:
    embedding_model = st.selectbox("Embedding Model",
        ["text-embedding-3-small", "text-embedding-3-large"],
        help="3-small is cost-effective and excellent quality.")
    reprocess = st.checkbox("Re-process already indexed files",
        value=False,
        help="Enable to rebuild from scratch. Deletes existing chunks first.")
    clean_text = st.checkbox("Clean transcripts (remove fillers)",
        value=True,
        help="Remove 'um', 'uh', repeated words from Wisdom Distiller transcripts.")

# Cost estimate
est_chunks = n_files * 30
st.caption(
    f"💡 Estimated cost: ~${est_chunks * 250 * 0.00002 / 1000:.4f} USD "
    f"({est_chunks} estimated chunks × {embedding_model})"
)
st.markdown('</div>', unsafe_allow_html=True)

# ── Build Button ───────────────────────────────────────────────────────────────
if st.button("🚀 Build Knowledge Base", use_container_width=True, type="primary"):

    progress_bar = st.progress(0)
    status_box   = st.empty()
    log          = st.container()

    try:
        import streamlit as st2
        api_key = st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        api_key = ""

    embeddings = get_embeddings(embedding_model)
    total = len(raw_files)
    total_chunks = 0
    errors = 0

    for idx, fpath in enumerate(raw_files):
        progress_bar.progress(idx / total)
        status_box.markdown(f"**Processing ({idx+1}/{total}):** `{fpath.name}`")

        try:
            # Extract text
            text, meta = extract_text(fpath)

            # Clean based on format
            if detect_story_format(text):
                text = clean_story_transcript(text)
                log.info(f"  🪷 Story format detected — cleaned")
            elif "Discourse Summary" in text or "DISCOURSE DETAILS" in text:
                embedded_meta = extract_discourse_metadata(text)
                meta.update({k:v for k,v in embedded_meta.items() if v})
                text = clean_discourse_transcript(text)
                log.info(f"  🧹 Discourse format detected — cleaned")
            elif clean_text:
                from src.transcription import clean_transcript
                text = clean_transcript(text)

            # Build source record using actual function signature
            record = build_source_record(
                file_path=fpath,
                metadata={**meta, "file_path": str(fpath),
                          "source_type": meta.get("source_type","document")},
                source_type=meta.get("source_type","document"),
            )
            source_id = record["source_id"]

            # Delete existing chunks if reprocessing
            if reprocess:
                try:
                    delete_chunks_by_source(source_id)
                except Exception:
                    pass

            # Chunk — correct param name is source_metadata
            chunks = build_chunk_documents(
                text, record,  # positional: text, source_metadata
                chunk_size=chunk_size,
                overlap=chunk_overlap,
            )

            if not chunks:
                log.warning(f"⚠️ No chunks generated for {fpath.name}")
                continue

            # Embed and store
            n_added = add_chunks_to_store(chunks, embeddings, batch_size=50)
            total_chunks += n_added

            # Update registry
            registry = load_source_registry(REGISTRY_PATH)
            registry = [r for r in registry if r.get("source_id") != source_id]
            registry.append(record)
            save_source_registry(registry, REGISTRY_PATH)
            mark_source_processed(source_id, n_added, REGISTRY_PATH)

            log.success(f"✅ {fpath.name} — {n_added} chunks indexed")

        except Exception as e:
            log.error(f"❌ {fpath.name}: {e}")
            errors += 1
            continue

    progress_bar.progress(1.0)
    status_box.empty()

    # Save KB status
    kb_status = {
        "built_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "chunks":   stats.get("total_chunks", 0) + total_chunks,
        "sources":  total - errors,
        "errors":   errors,
    }
    STATUS_FILE.write_text(json.dumps(kb_status, indent=2))

    if total_chunks > 0:
        st.success(
            f"🎉 Knowledge base built! **{total_chunks:,}** chunks indexed "
            f"from **{total - errors}** file(s). "
            f"{'⚠️ ' + str(errors) + ' error(s).' if errors else ''}"
        )
        st.balloons()
    else:
        st.error("❌ No chunks were indexed. Check the error messages above.")

# ── Danger Zone ────────────────────────────────────────────────────────────────
st.divider()
with st.expander("⚠️ Danger Zone — Reset Knowledge Base"):
    st.warning("This deletes ALL chunks from the vector database. "
               "Source files are kept. You will need to rebuild after this.")
    if st.button("🗑️ Clear Vector Database", type="secondary"):
        try:
            clear_collection()
            # Reset registry
            if REGISTRY_PATH.exists():
                registry = load_source_registry(REGISTRY_PATH)
                for r in registry:
                    r["processed"] = False
                    r["chunk_count"] = 0
                save_source_registry(registry, REGISTRY_PATH)
            # Reset status
            STATUS_FILE.write_text(json.dumps({"chunks": 0, "sources": 0}))
            st.success("✅ Vector database cleared. Upload and rebuild to restore.")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error clearing database: {e}")
