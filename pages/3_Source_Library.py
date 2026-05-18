import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
"""
pages/4_Source_Library.py — Browse all indexed sources and their chunk metadata.
"""

import streamlit as st
from pathlib import Path
import sys
from pathlib import Path as _Path
_ROOT = _Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from src.page_header import render_om_symbol, render_page_quote


st.set_page_config(
    page_title="Source Library | Indispensable Values",
    page_icon="📚",
    layout="wide",
)

render_om_symbol()

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ui_components import inject_global_css, render_page_header, render_source_badge
from src.ingestion import load_source_registry
from src.vector_store import get_collection_stats, get_or_create_collection

inject_global_css()

REGISTRY_PATH = Path("data/source_registry.json")

render_page_header("Source Library", "Browse all indexed knowledge sources", "📚")

records = load_source_registry(REGISTRY_PATH)

if not records:
    st.info("No sources have been uploaded yet. Go to **Upload Sources** to add content.")
    st.stop()

# ── Stats Bar ──────────────────────────────────────────────────────────────────
stats = get_collection_stats()
c1, c2, c3, c4 = st.columns(4)
c1.metric("📁 Total Sources", len(records))
c2.metric("✅ Processed", sum(1 for r in records if r.get("processed")))
c3.metric("🔍 Total Chunks", stats.get("total_chunks", 0))
c4.metric("👤 Speakers", len(stats.get("speakers", [])))

st.divider()

# ── Filters ────────────────────────────────────────────────────────────────────
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    filter_type = st.selectbox(
        "Source Type",
        ["All"] + list({r.get("source_type", "") for r in records}),
    )
with col_f2:
    filter_speaker = st.selectbox(
        "Speaker",
        ["All"] + list({r.get("speaker", "") for r in records if r.get("speaker")}),
    )
with col_f3:
    filter_status = st.selectbox("Status", ["All", "✅ Processed", "⏳ Pending"])

# Apply filters
filtered = records
if filter_type != "All":
    filtered = [r for r in filtered if r.get("source_type") == filter_type]
if filter_speaker != "All":
    filtered = [r for r in filtered if r.get("speaker") == filter_speaker]
if filter_status == "✅ Processed":
    filtered = [r for r in filtered if r.get("processed")]
elif filter_status == "⏳ Pending":
    filtered = [r for r in filtered if not r.get("processed")]

st.caption(f"Showing {len(filtered)} of {len(records)} sources")
st.divider()

# ── Source Cards ───────────────────────────────────────────────────────────────
for rec in filtered:
    processed  = rec.get("processed", False)
    src_type   = rec.get("source_type", "document")
    src_name   = rec.get("file_name", "Unknown")
    speaker    = rec.get("speaker", "—")
    topic      = rec.get("topic", "—")
    scripture  = rec.get("scripture", "—")
    chapter    = rec.get("chapter", "—")
    verse      = rec.get("verse_range", "—")
    language   = rec.get("language", "—")
    chunk_cnt  = rec.get("chunk_count", 0)
    src_url    = rec.get("source_url", "")
    created    = rec.get("created_at", "")[:10]

    badge = render_source_badge(src_type)
    status_icon = "✅" if processed else "⏳"

    with st.expander(
        f"{status_icon}  {src_name}  |  {speaker}  |  {chunk_cnt} chunks",
        expanded=False,
    ):
        st.markdown(badge, unsafe_allow_html=True)
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

        if src_url:
            st.markdown(f"🔗 [Open Source]({src_url})")

        # ── Sample chunks from this source ────────────────────────────────
        if processed and st.checkbox(f"Preview sample chunks", key=f"preview_{rec['source_id']}"):
            try:
                collection = get_or_create_collection()
                results = collection.get(
                    where={"source_id": {"$eq": rec["source_id"]}},
                    limit=3,
                    include=["documents", "metadatas"],
                )
                if results and results.get("documents"):
                    for i, (doc, meta) in enumerate(
                        zip(results["documents"], results["metadatas"]), 1
                    ):
                        st.markdown(f"**Chunk {i}** — Type: `{meta.get('chunk_type','—')}`")
                        st.markdown(f"""
                        <div style="
                            background: rgba(255,255,255,0.03);
                            border-left: 3px solid #d4af5766;
                            padding: 0.7rem 1rem;
                            border-radius: 6px;
                            font-size:0.85rem;
                            color:rgba(245,230,200,0.8);
                            margin-bottom:0.5rem;
                        ">{doc[:600]}{'…' if len(doc) > 600 else ''}</div>
                        """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Could not load chunks: {e}")

# ── Chunk Type Distribution ────────────────────────────────────────────────────
if stats.get("chunk_types"):
    st.divider()
    st.markdown("### 📊 Chunk Type Distribution")
    import pandas as pd
    df = pd.DataFrame(
        list(stats["chunk_types"].items()),
        columns=["Chunk Type", "Count"],
    ).sort_values("Count", ascending=False)
    st.bar_chart(df.set_index("Chunk Type"))
