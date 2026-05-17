# Indispensable Values Q&A

**A Reverential AI-Powered Study Companion**

Grounded in the teachings of Pūjya Swāmī Aparājitānandajī of Chinmaya Mission, this
Streamlit-based RAG (Retrieval-Augmented Generation) application answers questions about
the **20 Indispensable Values (jñāna sādhana)** from Bhagavad Gītā Chapter 13, verses 7–11.

Answers are drawn exclusively from Swamiji's authentic video talks, transcripts, stories,
and published books -- never fabricated.

---

## Features

- **Q&A Interface** -- Ask questions; receive source-cited answers from Swamiji's teachings
- **Source Library** -- Browse all indexed discourse transcripts and books
- **Admin Pages** -- Password-protected upload, knowledge-base builder, and settings
- **Visitor Counter** -- Session-based persistent visitor tracking
- **Reverential Design** -- Sandalwood & Sage theme, Sanskrit preserved with diacritics

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit (multi-page, 10 pages) |
| LLM | OpenAI GPT-4o-mini (temperature 0.2) |
| Embeddings | OpenAI text-embedding-3-small |
| Vector DB | ChromaDB (local persistent) |
| Language | Python 3.11+ |

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/VedantaStreams/indispensable-values-qa.git
cd indispensable-values-qa
pip install -r requirements.txt
```

### 2. Configure secrets

Create `.streamlit/secrets.toml` (this file is gitignored):

```toml
OPENAI_API_KEY = "sk-..."
ADMIN_PASSWORD = "your-admin-password"
```

### 3. Run

```bash
streamlit run Home.py
```

### 4. Build the knowledge base

1. Navigate to **Admin Upload Sources** (password required)
2. Upload PDF/DOCX/TXT files or fetch YouTube transcripts
3. Navigate to **Admin Build Knowledge Base** and click **Mark as Built**

## Project Structure

```
.
├── Home.py                               # Hero page with visitor counter
├── pages/
│   ├── 0_Gratitude_and_Reverence.py
│   ├── 1_About_Pujya_Swamiji.py
│   ├── 2_Indispensable_Values_QA.py      # Main RAG Q&A interface
│   ├── 3_Source_Library.py
│   ├── 4_About_the_App.py
│   ├── 5_FAQ.py
│   ├── 6_Get_the_App.py
│   ├── 7_Admin_Upload_Sources.py         # Password-protected
│   ├── 8_Admin_Build_Knowledge_Base.py   # Password-protected
│   └── 9_Admin_Settings.py              # Password-protected
├── src/
│   ├── rag_chain.py        # RAG pipeline (threshold 0.15, 8 chunks)
│   ├── vector_store.py     # ChromaDB collection management
│   ├── embeddings.py       # OpenAI embedding generation
│   ├── ingestion.py        # PDF/DOCX/TXT ingestion with cleaners
│   ├── chunking.py         # Verse-aware and story-aware chunking
│   ├── transcription.py    # YouTube transcript fetching
│   ├── guardrails.py       # Content guardrails for reverence & accuracy
│   ├── prompts.py          # System and RAG prompts
│   ├── page_header.py      # Shared Om symbol and rotating Swamiji quote
│   ├── visitor_counter.py  # Session-based visitor tracking
│   └── admin_guard.py      # Password-protected admin pages
├── data/
│   ├── visitors.json       # Visitor count (persistent)
│   └── kb_status.json      # Knowledge base status
├── tests/
│   └── test_core.py        # Unit tests (pytest)
├── .streamlit/
│   └── config.toml         # Streamlit theme (Sandalwood & Sage)
└── requirements.txt
```

## Running Tests

```bash
pip install pytest
pytest tests/
```

## Knowledge Base Sources

| Collection | Type | Items |
|-----------|------|-------|
| Value of Values | Discourse Transcripts | 8 discourses |
| Bhagavad Gītā Chapter 13 | Discourse Transcripts | 2 discourses |
| Value Based Stories for All | Story Transcripts | 6 discourses |
| Indispensable Values (2022) | Published Book | 320 pages |

## Key Conventions

- **Never fabricate** Swamiji's words -- only answer from retrieved chunks
- **Preserve Sanskrit** with diacritical marks (amānitvam, kṣāntiḥ, etc.)
- Admin pages require password from `st.secrets["ADMIN_PASSWORD"]`
- OpenAI key stored in `.streamlit/secrets.toml` (gitignored)
- Similarity threshold: **0.15**, default chunks: **8**

---

*Built with reverence -- Chinmaya Mission — Bhagavad Gītā Chapter 13*
