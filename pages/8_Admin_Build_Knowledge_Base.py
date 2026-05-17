"""
pages/2_Build_Knowledge_Base.py — Process sources, chunk, embed, and index.
"""
import sys
from pathlib import Path
import sys
from pathlib import Path as _Path
_ROOT = _Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from src.page_header import render_om_symbol, render_page_quote

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.admin_guard import require_admin

if not require_admin():
    import streamlit as st
    st.stop()



import streamlit as st
import time
from pathlib import Path

st.set_page_config(
    page_title="Build Knowledge Base | Indispensable Values",
    page_icon="🔨",
    layout="wide",
)

render_om_symbol()

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ui_components import inject_global_css, render_page_header, render_status_banner
from src.ingestion import (
    load_source_registry, save_source_registry, mark_source_processed,
    extract_text, save_raw_text, load_raw_text,
    clean_discourse_transcript, extract_discourse_metadata,
    clean_story_transcript, detect_story_format,
)
from src.transcription import (
    get_youtube_transcript, get_playlist_video_ids, clean_transcript,
    get_video_metadata, save_transcript_cache, load_transcript_cache,
    extract_video_id,
)
from src.chunking import build_chunk_documents, chunk_transcript_with_timestamps
from src.embeddings import get_embeddings, estimate_embedding_cost
from src.vector_store import add_chunks_to_store, get_collection_stats, delete_chunks_by_source

inject_global_css()

REGISTRY_PATH  = Path("data/source_registry.json")
RAW_DIR        = Path("data/raw")
TRANSCRIPT_DIR = Path("data/transcripts")

render_page_header(
    "Build Knowledge Base",
    "Process, chunk, embed, and index uploaded sources",
    "🔨",
)

# ── Status Overview ────────────────────────────────────────────────────────────
records = load_source_registry(REGISTRY_PATH)
pending = [r for r in records if not r.get("processed")]
done    = [r for r in records if r.get("processed")]
stats   = get_collection_stats()

col1, col2, col3, col4 = st.columns(4)
col1.metric("📁 Total Sources", len(records))
col2.metric("⏳ Pending", len(pending))
col3.metric("✅ Processed", len(done))
col4.metric("🔍 Chunks in DB", stats.get("total_chunks", 0))

st.divider()

if not records:
    st.info("No sources found. Please upload sources first on the **Upload Sources** page.")
    st.stop()

# ── Settings ──────────────────────────────────────────────────────────────────
with st.expander("⚙️ Processing Settings", expanded=False):
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        chunk_size = st.slider("Chunk Size (chars)", 600, 1800, 1000, 100)
        chunk_overlap = st.slider("Chunk Overlap (chars)", 100, 400, 200, 50)
    with col_s2:
        embedding_model = st.selectbox(
            "Embedding Model",
            ["text-embedding-3-small", "text-embedding-3-large"],
            index=0,
            help="3-small is cost-effective and excellent for most use cases.",
        )
        reprocess_existing = st.checkbox("Re-process already processed sources", value=False)
    with col_s3:
        enable_transcription = st.checkbox("Fetch YouTube transcripts", value=True)
        clean_transcripts = st.checkbox("Clean transcripts (remove fillers)", value=True)
        st.caption(f"Est. cost per 100 chunks: ~${estimate_embedding_cost(100, 250, embedding_model):.4f}")

# ── Source Selection ──────────────────────────────────────────────────────────
st.markdown("### Select Sources to Process")

to_process = pending if not reprocess_existing else records
if not to_process:
    st.success("All sources have been processed. Enable 'Re-process' above to rebuild.")
    st.stop()

selected_ids = []
select_all = st.checkbox("Select All Pending", value=True)

for rec in to_process:
    label = f"[{rec.get('source_type','').upper()}] {rec.get('file_name','Unknown')} — {rec.get('speaker','')}"
    checked = select_all or st.checkbox(label, key=f"sel_{rec['source_id']}", value=False)
    if checked:
        selected_ids.append(rec["source_id"])

if not selected_ids:
    st.info("Select at least one source to process.")
    st.stop()

st.caption(f"{len(selected_ids)} source(s) selected.")
st.divider()

# ── Cost Estimate ──────────────────────────────────────────────────────────────
estimated_chunks = len(selected_ids) * 25  # rough average
est_cost = estimate_embedding_cost(estimated_chunks, 250, embedding_model)
st.info(
    f"💡 **Estimated embedding cost:** ~${est_cost:.4f} USD "
    f"(~{estimated_chunks} chunks × {embedding_model}). "
    "Actual cost depends on document length."
)

# ── Build Button ───────────────────────────────────────────────────────────────
if st.button("🚀 Build Knowledge Base", type="primary", use_container_width=True):
    records = load_source_registry(REGISTRY_PATH)
    selected_records = [r for r in records if r["source_id"] in selected_ids]

    progress_bar = st.progress(0)
    status_box   = st.empty()
    log_box      = st.container()

    embeddings = get_embeddings(embedding_model)
    total = len(selected_records)
    total_chunks_added = 0

    for idx, rec in enumerate(selected_records):
        src_id   = rec["source_id"]
        src_type = rec.get("source_type", "document")
        src_name = rec.get("file_name", "Unknown")

        status_box.markdown(f"**Processing ({idx+1}/{total}):** `{src_name}`")
        progress_bar.progress((idx) / total)

        try:
            chunk_docs = []

            # ── YouTube Video ──────────────────────────────────────────────
            if src_type in ("youtube_video",):
                if not enable_transcription:
                    log_box.warning(f"⏭ Skipped (transcription disabled): {src_name}")
                    continue

                video_id = rec.get("video_id") or extract_video_id(rec.get("source_url", ""))
                if not video_id:
                    log_box.error(f"❌ Invalid video ID for: {src_name}")
                    continue

                # Check cache
                cached = load_transcript_cache(video_id, TRANSCRIPT_DIR)
                if cached:
                    log_box.info(f"📦 Using cached transcript: {video_id}")
                    transcript_data = cached
                else:
                    log_box.info(f"🔄 Fetching transcript: {video_id}")
                    transcript_data = get_youtube_transcript(video_id)
                    if transcript_data:
                        if clean_transcripts:
                            transcript_data["text"] = clean_transcript(transcript_data["text"])
                        save_transcript_cache(video_id, transcript_data, TRANSCRIPT_DIR)

                if not transcript_data:
                    log_box.warning(f"⚠️ No transcript available for {video_id}. Skipping.")
                    continue

                video_meta = get_video_metadata(video_id)
                source_meta = {**rec, "title": video_meta.get("title", src_name)}

                if transcript_data.get("segments"):
                    chunk_docs = chunk_transcript_with_timestamps(
                        transcript_data["segments"], source_meta, words_per_chunk=280
                    )
                else:
                    chunk_docs = build_chunk_documents(
                        transcript_data["text"], source_meta,
                        chunk_size=chunk_size, overlap=chunk_overlap,
                    )

            # ── YouTube Playlist ───────────────────────────────────────────
            elif src_type == "youtube_playlist":
                if not enable_transcription:
                    log_box.warning(f"⏭ Skipped (transcription disabled): {src_name}")
                    continue

                playlist_url = rec.get("source_url", "")
                log_box.info(f"📋 Fetching playlist: {playlist_url}")

                try:
                    videos = get_playlist_video_ids(playlist_url)
                    log_box.info(f"  Found {len(videos)} video(s) in playlist.")
                except Exception as e:
                    log_box.error(f"❌ Playlist fetch error: {e}")
                    continue

                for vid in videos:
                    vid_id = vid.get("video_id")
                    vid_title = vid.get("title", vid_id)
                    if not vid_id:
                        continue

                    cached = load_transcript_cache(vid_id, TRANSCRIPT_DIR)
                    if cached:
                        td = cached
                    else:
                        td = get_youtube_transcript(vid_id)
                        if td:
                            if clean_transcripts:
                                td["text"] = clean_transcript(td["text"])
                            save_transcript_cache(vid_id, td, TRANSCRIPT_DIR)
                        else:
                            log_box.warning(f"  ⚠️ No transcript: {vid_title}")
                            continue

                    vid_meta = {**rec, "title": vid_title, "source_url": vid.get("url", ""), "video_id": vid_id}
                    if td.get("segments"):
                        vchunks = chunk_transcript_with_timestamps(td["segments"], vid_meta, words_per_chunk=280)
                    else:
                        vchunks = build_chunk_documents(td["text"], vid_meta, chunk_size=chunk_size, overlap=chunk_overlap)

                    chunk_docs.extend(vchunks)
                    log_box.info(f"  ✅ {vid_title}: {len(vchunks)} chunks")
                    time.sleep(0.5)  # Be gentle with YouTube API

            # ── Document / PDF / DOCX / TXT ───────────────────────────────
            else:
                file_path = Path(rec.get("file_path", ""))
                raw_text = load_raw_text(src_id, RAW_DIR)

                if not raw_text:
                    if not file_path.exists():
                        log_box.error(f"❌ File not found: {file_path}")
                        continue
                    text, extra = extract_text(file_path)
                    save_raw_text(src_id, text, RAW_DIR)
                    page_texts = extra.get("page_texts", None)
                else:
                    text = raw_text
                    page_texts = None

                # Auto-detect transcript format and clean accordingly
                if detect_story_format(text):
                    # Value Based Stories for All — summer camp format
                    text = clean_story_transcript(text)
                    log_box.info(f"  🪷 Story transcript format detected — cleaned (classroom prompts removed, stories preserved).")
                    page_texts = None
                elif "Discourse Summary" in text or "DISCOURSE DETAILS" in text:
                    # Standard Value of Values / BG Chapter 13 discourse format
                    embedded_meta = extract_discourse_metadata(text)
                    if embedded_meta.get("speaker") and not rec.get("speaker"):
                        rec["speaker"] = embedded_meta["speaker"]
                    if embedded_meta.get("topic") and not rec.get("topic"):
                        rec["topic"] = embedded_meta["topic"]
                    text = clean_discourse_transcript(text)
                    log_box.info(f"  🧹 Discourse transcript format detected — cleaned.")
                    page_texts = None

                chunk_docs = build_chunk_documents(
                    text, rec,
                    page_texts=page_texts,
                    chunk_size=chunk_size,
                    overlap=chunk_overlap,
                )

            # ── Embed and Store ────────────────────────────────────────────
            if chunk_docs:
                if reprocess_existing:
                    delete_chunks_by_source(src_id)

                n_added = add_chunks_to_store(chunk_docs, embeddings, batch_size=50)
                total_chunks_added += n_added
                mark_source_processed(src_id, n_added, REGISTRY_PATH)
                log_box.success(f"✅ {src_name}: {n_added} chunks indexed.")
            else:
                log_box.warning(f"⚠️ No chunks generated for: {src_name}")

        except Exception as e:
            log_box.error(f"❌ Error processing {src_name}: {e}")
            continue

    progress_bar.progress(1.0)
    status_box.empty()

    final_stats = get_collection_stats()
    render_status_banner(
        f"🎉 Knowledge base built! "
        f"**{total_chunks_added}** new chunks indexed across **{len(selected_records)}** source(s). "
        f"Total chunks in DB: **{final_stats['total_chunks']}**.",
        "success",
    )

# ── Reset / Clear ──────────────────────────────────────────────────────────────
st.divider()
with st.expander("⚠️ Danger Zone — Reset Knowledge Base"):
    st.warning("This will delete ALL chunks from the vector database. Source files will be kept.")
    if st.button("🗑 Clear Vector Database", type="secondary"):
        from src.vector_store import clear_collection
        clear_collection()
        # Reset processed flags
        records = load_source_registry(REGISTRY_PATH)
        for r in records:
            r["processed"] = False
            r["chunk_count"] = 0
        save_source_registry(records, REGISTRY_PATH)
        render_status_banner("Vector database cleared. Sources marked as unprocessed.", "warning")
        st.rerun()
