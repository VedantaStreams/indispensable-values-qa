"""
pages/7_Admin_Upload_Sources.py — Admin only. Password protected.
Includes file deletion and KB status indicator.
"""
import sys, json, shutil
from pathlib import Path
from datetime import datetime
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

st.set_page_config(page_title="Admin: Upload Sources",
                   page_icon="🔐", layout="wide")

render_om_symbol()

DATA_DIR    = Path(__file__).parent.parent / "data"
RAW_DIR     = DATA_DIR / "raw"
STATUS_FILE = DATA_DIR / "kb_status.json"
RAW_DIR.mkdir(parents=True, exist_ok=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Lato:wght@300;400;700&family=Cormorant+Garamond:ital@1&display=swap');

[data-testid="stImage"] {
    margin-bottom:-1.5rem!important;
    padding-bottom:0!important;
    line-height:0!important;
}
[data-testid="stImage"] img {
    display:block!important;
}

html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:#F8F9F5;color:#1A3A28;}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#2A5C3A!important;}
div[data-testid="stSidebar"]{background:linear-gradient(180deg,#EDF3EC,#E0EBE2)!important;border-right:2px solid #B8D4BC;}
div[data-testid="stSidebar"] *{color:#2A4A38!important;font-weight:600!important;}
.stButton>button{background:linear-gradient(135deg,#4A7C59,#6A9E78);color:white!important;
    border:none;border-radius:8px;font-weight:700;padding:.5rem 1.2rem;transition:all .3s;}
.stButton>button:hover{background:linear-gradient(135deg,#2A5C3A,#4A7C59);}
.page-header{background:linear-gradient(135deg,#EDF3EC,#E4EDE4);border:2px solid #B8D4BC;
    border-radius:18px;padding:2rem;text-align:center;margin-bottom:1.5rem;}
.page-header-title{font-family:'Playfair Display',serif;font-size:2rem;font-weight:800;color:#2A5C3A;}
.page-header-sub{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.1rem;color:#4A7C59;}
.kb-ready{background:#E8F5E9;border:2px solid #4CAF50;border-radius:12px;padding:1rem 1.5rem;margin-bottom:1.5rem;}
.kb-stale{background:#EAF3E4;border:2px solid #FF9800;border-radius:12px;padding:1rem 1.5rem;margin-bottom:1.5rem;}
.kb-empty{background:#EDF3EC;border:2px solid #B8D4BC;border-radius:12px;padding:1rem 1.5rem;margin-bottom:1.5rem;}
.kb-title{font-weight:700;font-size:1rem;margin-bottom:.2rem;}
.kb-detail{font-size:.85rem;color:#3A5040;}
.section-card{background:white;border:2px solid #B8D4BC;border-radius:14px;
    padding:1.8rem;margin-bottom:1.5rem;box-shadow:0 2px 10px rgba(74,124,89,.06);}
.section-title{font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:700;
    color:#2A5C3A;margin-bottom:1rem;padding-bottom:.4rem;border-bottom:2px solid #B8D4BC;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <div style="font-size:2rem;margin-bottom:.3rem;">📤</div>
    <div class="page-header-title">Admin · Upload Sources</div>
    <div class="page-header-sub">Manage knowledge base sources — upload, review, and delete</div>
</div>
""", unsafe_allow_html=True)


render_page_quote(
    "A heart filled with <strong>noble emotions</strong> — kindness, compassion, mercy, truthfulness, honesty — such a heart is called a <strong>pure heart</strong>."
)
# ── KB Status Indicator ────────────────────────────────────────────────────────
def get_kb_status():
    if STATUS_FILE.exists():
        try:
            return json.loads(STATUS_FILE.read_text())
        except Exception:
            pass
    return None

raw_files = sorted(RAW_DIR.glob("*.*")) if RAW_DIR.exists() else []
kb = get_kb_status()

if kb and kb.get("chunks", 0) > 0:
    built_at = kb.get("built_at", "Unknown")
    st.markdown(f"""
    <div class="kb-ready">
        <div class="kb-title">✅ Knowledge Base is UP TO DATE</div>
        <div class="kb-detail">Last built: {built_at} &nbsp;·&nbsp;
        {kb.get('chunks',0):,} chunks &nbsp;·&nbsp; {kb.get('sources',0)} sources</div>
    </div>
    """, unsafe_allow_html=True)
elif raw_files:
    st.markdown(f"""
    <div class="kb-stale">
        <div class="kb-title">⚠️ Knowledge Base needs rebuilding</div>
        <div class="kb-detail">{len(raw_files)} file(s) uploaded but not yet indexed.
        Go to Admin → Build Knowledge Base.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="kb-empty">
        <div class="kb-title">📭 No sources uploaded yet</div>
        <div class="kb-detail">Upload PDFs or DOCX files below to get started.</div>
    </div>
    """, unsafe_allow_html=True)

# ── Existing Files + Delete ────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">📁 Uploaded Files</div>',
            unsafe_allow_html=True)

if not raw_files:
    st.info("No files yet.")
else:
    st.caption(f"{len(raw_files)} file(s) uploaded")

    col_a, col_b = st.columns([3,1])
    with col_b:
        if st.button("🗑️ Delete ALL", help="Remove all source files"):
            st.session_state["confirm_delete_all"] = True

    if st.session_state.get("confirm_delete_all"):
        st.warning("⚠️ Delete ALL source files? This cannot be undone.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Yes, delete all"):
                for f in raw_files:
                    f.unlink(missing_ok=True)
                st.session_state["confirm_delete_all"] = False
                st.success("All files deleted. Rebuild the knowledge base.")
                st.rerun()
        with c2:
            if st.button("❌ Cancel"):
                st.session_state["confirm_delete_all"] = False
                st.rerun()

    st.divider()

    for i, fpath in enumerate(raw_files):
        size_kb = fpath.stat().st_size / 1024
        ext = fpath.suffix.upper().lstrip(".")
        icon = {"PDF":"📄","DOCX":"📝","TXT":"📃","MP3":"🎵","MP4":"🎬"}.get(ext,"📎")

        col_icon, col_name, col_size, col_del = st.columns([0.3, 3, 1, 0.8])
        with col_icon:
            st.write(icon)
        with col_name:
            st.write(f"**{fpath.name}**")
        with col_size:
            st.write(f"{size_kb:.1f} KB")
        with col_del:
            if st.button("🗑️ Delete", key=f"del_{i}"):
                st.session_state[f"confirm_del_{i}"] = True

        if st.session_state.get(f"confirm_del_{i}"):
            st.warning(f"Delete **{fpath.name}**?")
            cy, cn = st.columns(2)
            with cy:
                if st.button("Yes, delete", key=f"yes_del_{i}"):
                    fpath.unlink(missing_ok=True)
                    st.session_state[f"confirm_del_{i}"] = False
                    st.success(f"Deleted {fpath.name}")
                    st.rerun()
            with cn:
                if st.button("No, keep", key=f"no_del_{i}"):
                    st.session_state[f"confirm_del_{i}"] = False
                    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ── Upload New Files ───────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">📤 Upload New Sources</div>',
            unsafe_allow_html=True)

try:
    from src.ingestion import ingest_file
    from src.transcription import fetch_youtube_transcript

    tab_file, tab_yt = st.tabs(["📄 Upload Files", "📹 YouTube URL"])

    with tab_file:
        col1, col2 = st.columns(2)
        with col1:
            speaker   = st.text_input("Speaker", value="Swami Aparajitananda", key="f_spk")
            topic     = st.text_input("Topic", placeholder="e.g. Indispensable Values", key="f_topic")
            scripture = st.text_input("Scripture", value="Bhagavad Gītā", key="f_script")
        with col2:
            chapter    = st.text_input("Chapter", value="13", key="f_ch")
            verse_range= st.text_input("Verse Range", value="7-11", key="f_vr")
            language   = st.selectbox("Language",
                ["English","Hindi","Kannada","Telugu","Tamil","Marathi"], key="f_lang")
        src_type = st.selectbox("Source Type",
            ["discourse_transcript","book_chapter","story_transcript","lecture_notes","other"],
            key="f_type")

        uploaded = st.file_uploader("Choose PDF / DOCX / TXT files",
            type=["pdf","docx","txt"], accept_multiple_files=True, key="f_up")

        if uploaded and st.button("⬆️ Upload & Process Files"):
            meta = dict(speaker=speaker, topic=topic, scripture=scripture,
                        chapter=chapter, verse_range=verse_range,
                        language=language, source_type=src_type)
            for uf in uploaded:
                dest = RAW_DIR / uf.name
                dest.write_bytes(uf.read())
                try:
                    ingest_file(str(dest), meta)
                    st.success(f"✅ {uf.name} uploaded")
                except Exception as e:
                    st.error(f"❌ {uf.name}: {e}")
            st.info("🔨 Go to Admin → Build Knowledge Base to index these files.")
            st.rerun()

    with tab_yt:
        yt_url = st.text_input("YouTube URL", key="yt_url")
        yt_spk = st.text_input("Speaker", value="Swami Aparajitananda", key="yt_spk")
        yt_topic = st.text_input("Topic", key="yt_topic")
        yt_lang  = st.selectbox("Transcript Language",["en","hi","kn","te","ta"], key="yt_lang")

        if yt_url and st.button("📥 Fetch YouTube Transcript"):
            with st.spinner("Fetching..."):
                try:
                    result = fetch_youtube_transcript(yt_url, language=yt_lang)
                    meta = dict(speaker=yt_spk, topic=yt_topic,
                                source_type="youtube_transcript", language=yt_lang)
                    from src.ingestion import ingest_youtube_transcript
                    ingest_youtube_transcript(result, meta, RAW_DIR)
                    st.success("✅ Transcript fetched")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ {e}")

except ImportError as e:
    st.warning(f"Ingestion pipeline not available: {e}")

st.markdown('</div>', unsafe_allow_html=True)
