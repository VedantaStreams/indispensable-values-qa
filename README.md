# 🪷 Indispensable Values Q&A

> *"Amānitvam adambhitvam ahiṃsā kṣāntir ārjavam…"*  
> — Bhagavad Gītā 13.7

A reverential, RAG-based Streamlit chatbot for studying Swamiji's teachings on the **Indispensable Values** (*jñāna sādhana*) of Bhagavad Gītā Chapter 13.

---

## ✨ What This App Does

Seekers can ask questions like:

- *"What is amānitvam and how does Swamiji explain it?"*
- *"How does ahiṃsā apply in daily life?"*
- *"Why are these values prerequisites for self-knowledge?"*

…and receive **grounded, source-cited answers** drawn only from Swamiji's uploaded talks, transcripts, and writings — never from AI hallucination.

---

## 🏗️ Architecture

```
User Question
     │
     ▼
[OpenAI Embedding]
     │
     ▼
[ChromaDB Vector Search] ──── top-k chunks ────▶
     │
     ▼
[GPT-4o-mini + System Prompt + Retrieved Context]
     │
     ▼
Structured Answer (with citations, reflection, sources)
```

**Stack:**
- **Frontend:** Streamlit (multipage)
- **Embeddings:** OpenAI `text-embedding-3-small`
- **Vector DB:** ChromaDB (local persistent)
- **LLM:** OpenAI `gpt-4o-mini` (or `gpt-4o`)
- **YouTube:** `youtube-transcript-api` + `yt-dlp`
- **PDF:** `pdfplumber`

---

## 📁 Folder Structure

```
indispensable-values-chatbot/
├── app.py                          ← Home page
├── pages/
│   ├── 1_Upload_Sources.py         ← Add YouTube URLs, PDFs, transcripts
│   ├── 2_Build_Knowledge_Base.py   ← Process + embed + index
│   ├── 3_Indispensable_Values_QA.py ← Main chatbot Q&A page
│   ├── 4_Source_Library.py         ← Browse indexed sources
│   └── 5_Settings.py               ← Config, models, cost info
├── src/
│   ├── ingestion.py                ← PDF/DOCX/TXT text extraction
│   ├── transcription.py            ← YouTube transcript fetching
│   ├── chunking.py                 ← Semantic chunking with verse-awareness
│   ├── embeddings.py               ← OpenAI embeddings setup
│   ├── vector_store.py             ← ChromaDB operations
│   ├── rag_chain.py                ← RAG pipeline + LLM call
│   ├── guardrails.py               ← Input/output safety checks
│   ├── prompts.py                  ← System prompts + templates
│   ├── export_utils.py             ← TXT/PDF/DOCX chat export
│   └── ui_components.py            ← Reusable Streamlit components
├── data/
│   ├── raw/                        ← Uploaded files saved here
│   ├── processed/                  ← Extracted text cache
│   ├── transcripts/                ← YouTube transcript cache
│   ├── vector_db/                  ← ChromaDB persistent storage
│   └── source_registry.json        ← Source metadata index
├── .streamlit/
│   ├── config.toml                 ← Theme + server config
│   └── secrets.toml                ← API keys (DO NOT COMMIT)
├── requirements.txt
└── README.md
```

---

## 🚀 Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/indispensable-values-chatbot.git
cd indispensable-values-chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
# venv\Scripts\activate       # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your OpenAI API Key

Create `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "sk-your-key-here"
```

> ⚠️ **Never commit this file.** It is already in `.gitignore`.

### 5. Run the App

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## 📖 Usage Guide

### Step 1 — Upload Sources

Go to **Upload Sources** and add:
- YouTube playlist URL (all videos processed automatically)
- Individual YouTube video URLs
- PDF files (book on Indispensable Values, talk notes)
- TXT or DOCX transcripts

Fill in the metadata (speaker, scripture, chapter, verse range).

### Step 2 — Build Knowledge Base

Go to **Build Knowledge Base** and click **🚀 Build Knowledge Base**.

The app will:
1. Fetch YouTube transcripts
2. Extract PDF/DOCX text
3. Chunk documents semantically
4. Embed chunks with OpenAI
5. Store in ChromaDB

This is a one-time operation. New sources can be added incrementally.

### Step 3 — Ask Questions

Go to **Indispensable Values Q&A** and start asking.

Each answer includes:
- **Answer** — clear response from retrieved teachings
- **Relevant Teaching** — excerpt from the source
- **Scriptural Connection** — Gītā reference if available
- **Reflection** — gentle practical note for seekers
- **Sources** — speaker, talk, page/timestamp/URL

---

## ☁️ Deployment on Streamlit Community Cloud

Streamlit Community Cloud hosts public apps for **free** with a GitHub account.

### Steps:

1. **Push to GitHub** (make sure `.streamlit/secrets.toml` is in `.gitignore`)

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**

3. Select:
   - **Repository:** your-username/indispensable-values-chatbot
   - **Branch:** main
   - **Main file path:** `app.py`

4. Under **Advanced settings → Secrets**, paste:

```toml
OPENAI_API_KEY = "sk-your-key-here"
```

5. Click **Deploy!** 🎉

> **Note on persistence:** Streamlit Community Cloud does not provide persistent disk storage. The `data/vector_db/` ChromaDB folder will be lost on each restart. For production use, switch to **Pinecone** or **Supabase Vector** (cloud-hosted vector databases). The source files in `data/raw/` and `data/transcripts/` will also be lost — consider keeping them in the GitHub repo (if not private) or using cloud storage.

---

## 💰 Cost Estimates

| Operation | Model | Est. Cost |
|---|---|---|
| Embed 500 chunks | text-embedding-3-small | ~$0.003 |
| Embed 5,000 chunks | text-embedding-3-small | ~$0.025 |
| 100 Q&A queries | gpt-4o-mini | ~$0.005 |
| 100 Q&A queries | gpt-4o | ~$0.15 |

For a typical knowledge base of 10–20 talks + 1 PDF book (~3,000 chunks):
- **One-time embedding cost:** ~$0.015
- **Monthly queries (100/day):** ~$0.15–$4.50 depending on model

Use `gpt-4o-mini` for all standard study queries. Switch to `gpt-4o` only when synthesis of multiple sources is needed.

---

## 🛡️ Guardrails

The app enforces:
- ✅ Answers only from retrieved context (no hallucination)
- ✅ No invented quotes, page numbers, or scripture references  
- ✅ Sanskrit terms preserved exactly
- ✅ Harmful or off-topic requests rejected gently
- ✅ Daily query limits to control costs
- ✅ Input/output sanitization

---

## 🌿 Values Covered

The knowledge base is designed to cover all 20 values from BG 13.7–11:

amānitvam · adambhitvam · ahiṃsā · kṣāntiḥ · ārjavam · ācāryopāsanam · śaucam · sthairyam · ātmavinigrahaḥ · vairāgyam · anahaṅkāra · viveka · asaktir · sama-cittatvam · bhakti · viviktadeśasevitṛtvam · jñāna · tattva-jñānārtha-darśanam

---

## 🙏 Acknowledgements

Built with reverence for **Swami Dayananda Saraswati** and the Vedantic tradition.  
*May this tool serve sincere seekers on the path of knowledge.*

---

*"This knowledge base is a lamp. The teaching is the oil. Your sincerity is the flame."*
