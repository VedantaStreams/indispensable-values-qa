# Indispensable Values Q&A — Project Context for Claude

**Please read this entire file before responding to any request.**

---

## App Details
- **Live URL:** https://wisdom-companion.streamlit.app
- **GitHub:** https://github.com/Vedantastreams/indispensable-values-qa (public repo)
- **Local path:** `/Users/sumarajashankar/Documents/Documents - Suma's MacBook Pro/Suma/Chinmaya Mission Activities/apps/Indispensable_Values/indispensable-values-qa`
- **Framework:** Streamlit (Python 3.11 locally, Python 3.14 on Streamlit Cloud)
- **LLM:** OpenAI gpt-4o-mini
- **Embeddings:** OpenAI text-embedding-3-small
- **Vector store:** ChromaDB (local, resets on Cloud restart — future: Pinecone)

---

## App Purpose
RAG-based AI study companion for Bhagavad Gītā Chapters 13 (20 indispensable values / jñāna sādhana) and 16 (daivī sampat & āsurī sampat), exclusively using Swāmī Aparājitānanda's discourses, transcripts, and published books.

---

## Page Structure (sidebar order)
```
Home.py
pages/0_Gratitude_and_Reverence.py
pages/1_About_Pujya_Swamiji.py
pages/2_Indispensable_Values_QA.py   ← main RAG chatbot
pages/3_Reflection_Journal.py
pages/4_Value_of_the_Day.py
pages/5_Source_Library.py
pages/6_About_the_App.py
pages/7_FAQ.py
pages/8_Get_the_App.py
pages/9_Admin_Panel.py               ← consolidated admin (3 tabs, 1 password)
```
---

## Source Folder
```
src/
rag_chain.py
embeddings.py
vector_store.py
chunking.py
ingestion.py
prompts.py
page_header.py
visitor_counter.py
admin_guard.py
ui_components.py
export_utils.py
```
---

## Key Functions
- `render_om_symbol()` — Om image in a styled box, top of each page
- `render_page_quote(html_text)` — centered italic quote
- `require_admin()` — checks ADMIN_PASSWORD from st.secrets, returns bool
- `get_rag_answer(query, filters)` — returns answer + sources
- `get_today_value()` — returns (value_dict, value_idx, prompt_idx) using `date.today().toordinal()`
- `inject_global_css()` — injects shared CSS from ui_components
- `render_chunk_card(chunk, i)` — renders a retrieved source chunk card
- `export_to_txt / export_to_pdf / export_to_docx` — download chat history

---

## Assets
- `assets/images/om_symbol.jpeg` — 4.4K, safe for base64 embedding
- `assets/images/swamiji_chinmayananda.jpg` — 20K, safe for base64
- `assets/images/swamiji_aparajitananda.jpg` — 150K, must use `st.image()`

---

## Theme (config.toml)
Do NOT hardcode background, text, or sidebar colours in individual page CSS — let the theme file control them. Only component-specific styles (cards, bubbles, pills, etc.) should be hardcoded in page CSS.

**Ocean Teal & Orange:**
```toml
[theme]
base = "light"
primaryColor = "#1A7A8C"
backgroundColor = "#E8F4F6"
secondaryBackgroundColor = "#D0EDF1"
textColor = "#1A3A45"
font = "serif"
```

**Warm Saffron:**
```toml
[theme]
base = "light"
primaryColor = "#D4621A"
backgroundColor = "#FFF8F0"
secondaryBackgroundColor = "#FFEDD9"
textColor = "#2C1810"
font = "serif"
```

---

## Current Page States (as of latest session)

### Home.py
- Hero block with Om + title
- Two quote blocks
- **Two labelled pill rows:** Ch.13 (20 values, BG 13.7–11) + Ch.16 (26 values, BG 16.01–16.03), each with a badge header
- Nav cards (3×3 grid)
- Knowledge base stats
- Visitor counter
- Gurudev photo + footer

### pages/1_About_Pujya_Swamiji.py
- Global CSS overrides REMOVED — page follows config.toml theme
- Swamiji photo: **200px**, border `4px solid #1A7A8C`, `border-radius:16px`
- Bio card, journey milestones, quotes
- **Section heading:** "The 20 Indispensable Values — Bhagavad Gītā 13.7–11"
- Ch.13 values displayed in a **bio-card box** with 2-column HTML grid (not st.columns)
- **Section heading:** "The 26 Indispensable Values — Bhagavad Gītā 16 (Daivī Sampat)"
- Ch.16 values displayed in a bio-card box with 3-column HTML grid
- YouTube channels
- Published works

### pages/2_Indispensable_Values_QA.py
- Sidebar: filters (speaker, scripture, chapter, source type, language, value/topic), retrieval settings, KB status
- Header block with Om
- Toolbar: Clear Chat + download buttons (TXT / PDF / DOCX — visible once chat has messages)
- **Two tabs** for starter questions: `📖 BG Ch.13 — 20 Jñāna Values` and `📖 BG Ch.16 — 26 Daivī Values`
  - Each tab has its own quick-reference box + themed sample question buttons
- Chat history (user bubble / bot bubble)
- RAG processing on last pending user message
- Chat input
- Retrieved chunks (expandable)
- Usage/cost footer

---

## Critical Bugs Already Fixed
1. **Docstring as visible text** — never use `"""..."""` as first statement in page files. Start with `import os`.
2. **VALUE_PROMPTS.index(today_value) ValueError** — use `date.today().toordinal() % len(VALUE_PROMPTS)` instead.
3. **protobuf error** — add `os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"` at top of every file using ChromaDB.
4. **YouTube 403** — yt-dlp blocked on Streamlit Cloud. Use Wisdom Distiller to transcribe offline.
5. **Sidebar ordering** — Streamlit sorts by filename string. Use `0_` through `9_` prefix.
6. **Photo centering** — put photo AND name caption inside same column `with col_c:`.
7. **Hardcoded CSS override bug** — About Swamiji page previously hardcoded `background-color`, sidebar gradient, and button colours in page CSS, overriding config.toml. This has been removed. Do not re-add global colour overrides to any page CSS.

---

## Knowledge Base Sources
- BG Chapter 13 — 7 discourses (Swāmī Aparājitānanda)
- BG Chapter 16 — 7 discourses (Swāmī Aparājitānanda)
- Value of Values — 8 discourses
- Value Based Stories — 6 discourses
- 5 books: Read Daily Live Fully (2016), Gurudev's Quotes I/II/III (2019/2021/2021), Indispensable Values (2022)

---

## Push Workflow
```bash
git add .
git commit -m "description"
git push
```
If rejected: `git pull` first, then `git push`.

---

## Secrets (in .streamlit/secrets.toml — gitignored)
```toml
OPENAI_API_KEY = "sk-..."
ADMIN_PASSWORD = "vedanta2025"
```

---

## Names Convention
- "Pūjya Swāmī Chinmayānanda" (no "ji" at end)
- "Pūjya Swāmī Aparājitānanda" (no "ji" at end)
- Attribution under quotes: `— Swāmī Aparājitānanda` (Playfair Display, not uppercase)

---

## Delivery Convention
- Deliver single `.py` files to `/mnt/user-data/outputs/` for download and push
- For multi-file changes, deliver all files in one session
- Always validate syntax with `python3 -c "import ast; ast.parse(open('file.py').read())"` before delivering
- Use targeted `str_replace` edits on existing files — do not rewrite the whole file unless explicitly asked

---

## Working Guidelines

### 1. Provide CLAUDE.md Files for Context
- Read this file fully before writing any code.
- If context is missing or ambiguous, ask for clarification before proceeding.
- When bugs are fixed or features added, note them in the relevant section above so knowledge is retained across sessions.

### 2. Be Specific and Unambiguous
- Use exact file paths, function names, and variable names — never guess.
- Reproduce Sanskrit terms and diacritics exactly as written in this file.
- If a request could be interpreted more than one way, state your interpretation explicitly before acting.

### 3. Think Step-by-Step
- For any multi-part task, outline the plan before writing code.
- Validate syntax before delivering any `.py` file.
- For changes to existing files, use targeted edits rather than full rewrites.

### 4. Iterate and Improve Continuously
- Deliver working code first, then refine on feedback.
- Document any new bugs fixed or design decisions made so they are not undone in future sessions.
- If something was done a particular way for a reason, note it here.

---

## What We're Working On Now
[Describe your current task here when starting a new session]