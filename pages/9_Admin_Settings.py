"""
pages/5_Settings.py — App configuration, usage limits, model selection, API key verification.
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
from pathlib import Path

st.set_page_config(
    page_title="Settings | Indispensable Values",
    page_icon="⚙️",
    layout="wide",
)

render_om_symbol()

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ui_components import inject_global_css, render_page_header, render_status_banner
from src.vector_store import get_collection_stats
from src.embeddings import estimate_embedding_cost

inject_global_css()

render_page_header("Settings", "Configure models, limits, and API credentials", "⚙️")

# ── API Key Status ─────────────────────────────────────────────────────────────
st.markdown("### 🔑 API Key Status")
api_key = st.secrets.get("OPENAI_API_KEY", "")

if not api_key:
    render_status_banner(
        "⚠️ OPENAI_API_KEY not found in <code>.streamlit/secrets.toml</code>. "
        "The app will not function without it. See README for setup instructions.",
        "error",
    )
else:
    masked = api_key[:6] + "…" + api_key[-4:] if len(api_key) > 12 else "****"
    render_status_banner(f"✅ OpenAI API key detected: <code>{masked}</code>", "success")

    if st.button("🔍 Verify API Key"):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            client.models.list()
            render_status_banner("✅ API key is valid and working.", "success")
        except Exception as e:
            render_status_banner(f"❌ API key error: {e}", "error")

st.divider()

# ── Model Configuration ────────────────────────────────────────────────────────
st.markdown("### 🤖 Model Configuration")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Chat Model** (for Q&A answers)")
    st.info("""
    - **gpt-4o-mini** — Recommended. Fast, cost-effective, very capable.  
      Cost: ~$0.15 / 1M input tokens, $0.60 / 1M output tokens.
    - **gpt-4o** — Higher capability for complex multi-step reasoning.  
      Cost: ~$5.00 / 1M input tokens, $15.00 / 1M output tokens.
    """)
with col2:
    st.markdown("**Embedding Model** (for indexing & retrieval)")
    st.info("""
    - **text-embedding-3-small** — Recommended. Excellent quality, lowest cost.  
      Cost: ~$0.020 / 1M tokens.
    - **text-embedding-3-large** — Higher precision, 6x more expensive.  
      Cost: ~$0.130 / 1M tokens.
    """)

st.divider()

# ── Usage Statistics ───────────────────────────────────────────────────────────
st.markdown("### 📊 Usage Statistics")

usage = st.session_state.get("usage_stats", {})
stats = get_collection_stats()

col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("🔍 Chunks in DB", stats.get("total_chunks", 0))
col_b.metric("📁 Sources", stats.get("total_sources", 0))
col_c.metric("💬 Queries Today", usage.get("queries_today", 0))
col_d.metric("🔢 Tokens Today", f"{usage.get('tokens_today', 0):,}")

st.divider()

# ── Cost Calculator ────────────────────────────────────────────────────────────
st.markdown("### 💰 Cost Calculator")
st.caption("Estimate costs before processing documents")

col_c1, col_c2 = st.columns(2)
with col_c1:
    num_docs   = st.number_input("Number of documents / videos", 1, 500, 10)
    avg_pages  = st.number_input("Average length (pages or minutes)", 1, 300, 40)
    words_per  = st.number_input("Words per page/minute", 100, 400, 150)

with col_c2:
    total_words  = num_docs * avg_pages * words_per
    total_tokens = int(total_words * 1.33)  # rough word-to-token ratio
    num_chunks   = max(1, total_tokens // 250)

    embed_cost_s = estimate_embedding_cost(num_chunks, 250, "text-embedding-3-small")
    embed_cost_l = estimate_embedding_cost(num_chunks, 250, "text-embedding-3-large")
    query_cost   = 0.00005 * 100  # ~100 queries at gpt-4o-mini rates

    st.markdown(f"""
    **Estimated totals:**
    - Words: ~{total_words:,}
    - Tokens: ~{total_tokens:,}
    - Chunks: ~{num_chunks:,}
    
    **One-time embedding cost:**
    - text-embedding-3-small: **${embed_cost_s:.4f}**
    - text-embedding-3-large: **${embed_cost_l:.4f}**
    
    **Per 100 queries (gpt-4o-mini):** ~**$0.005**
    """)

st.divider()

# ── Cost Controls ─────────────────────────────────────────────────────────────
st.markdown("### 🛡️ Cost Controls")

col_d1, col_d2 = st.columns(2)
with col_d1:
    st.markdown("""
    **Active controls in this app:**
    - ✅ Daily query limit (configurable in rag_chain.py)
    - ✅ Transcript caching (no re-fetch of YouTube transcripts)
    - ✅ Embedding caching (no re-embedding of unchanged sources)
    - ✅ Persistent ChromaDB (no re-indexing on restart)
    - ✅ Deduplication by file hash
    - ✅ Token usage logging per session
    """)
with col_d2:
    st.markdown("""
    **Recommendations:**
    - Use `gpt-4o-mini` for all standard Q&A
    - Use `text-embedding-3-small` for embeddings
    - Process documents offline / in batch
    - Set Streamlit secrets to limit access
    - Monitor OpenAI usage dashboard monthly
    - Enable admin-only ingestion in production
    """)

st.divider()

# ── Deployment Info ────────────────────────────────────────────────────────────
st.markdown("### 🚀 Deployment")
st.markdown("""
**Streamlit Community Cloud** — Free for public apps with a GitHub account.  
[streamlit.io/cloud](https://streamlit.io/cloud)

**Steps to deploy:**
1. Push this repo to GitHub (private or public)
2. Go to share.streamlit.io → New app → Select repo
3. Set **Main file path:** `app.py`
4. Under **Advanced settings → Secrets**, add:
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```
5. Click **Deploy!**

**Important:** Add `.streamlit/secrets.toml` to `.gitignore` before pushing.  
The `data/vector_db/` folder will not persist across Streamlit Cloud restarts  
(no persistent disk). For production, use **Pinecone**, **Supabase Vector**,  
or a VPS with persistent storage.
""")

st.divider()

# ── .gitignore Reminder ────────────────────────────────────────────────────────
st.markdown("### 📁 .gitignore Reminder")
st.code("""
# Secrets
.streamlit/secrets.toml

# Vector DB (large binary files)
data/vector_db/

# Raw uploaded files (optional — add if private)
data/raw/
data/transcripts/

# Python
__pycache__/
*.pyc
.env
""", language="gitignore")
