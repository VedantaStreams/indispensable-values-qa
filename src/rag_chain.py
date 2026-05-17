"""
src/rag_chain.py — RAG answer generation using retrieved context and OpenAI LLM.
Enforces guardrails and formats structured answers.
"""

import json
import time
import datetime
import streamlit as st
from typing import Optional

from src.prompts import SYSTEM_PROMPT, ANSWER_NOT_FOUND
from src.guardrails import check_input_guardrails, check_output_guardrails
from src.vector_store import query_collection
from src.embeddings import get_embeddings


# ── Usage Tracking ─────────────────────────────────────────────────────────────
def _get_usage_state() -> dict:
    if "usage_stats" not in st.session_state:
        st.session_state["usage_stats"] = {
            "queries_today": 0,
            "tokens_today": 0,
            "last_reset": datetime.date.today().isoformat(),
        }
    # Reset daily counters
    today = datetime.date.today().isoformat()
    if st.session_state["usage_stats"]["last_reset"] != today:
        st.session_state["usage_stats"]["queries_today"] = 0
        st.session_state["usage_stats"]["tokens_today"] = 0
        st.session_state["usage_stats"]["last_reset"] = today
    return st.session_state["usage_stats"]


def _increment_usage(tokens: int):
    state = _get_usage_state()
    state["queries_today"] += 1
    state["tokens_today"] += tokens


# ── Context Formatting ─────────────────────────────────────────────────────────
def format_context_for_prompt(chunks: list[dict]) -> str:
    """Format retrieved chunks into a readable context block for the LLM."""
    if not chunks:
        return "No relevant context found in the knowledge base."

    parts = []
    for i, chunk in enumerate(chunks, 1):
        meta = chunk.get("metadata", {})
        source_label = meta.get("source_title", "Unknown Source")
        speaker = meta.get("speaker", "")
        chapter = meta.get("chapter", "")
        verse = meta.get("verse_range", "")
        page = meta.get("page_number", "")
        ts = meta.get("timestamp", "")
        url = meta.get("source_url", "")

        ref_parts = []
        if speaker:
            ref_parts.append(f"Speaker: {speaker}")
        if source_label:
            ref_parts.append(f"Source: {source_label}")
        if chapter:
            ref_parts.append(f"Chapter: {chapter}")
        if verse:
            ref_parts.append(f"Verse: {verse}")
        if page:
            ref_parts.append(f"Page: {page}")
        if ts:
            ref_parts.append(f"Timestamp: {ts}")
        if url:
            ref_parts.append(f"URL: {url}")

        header = " | ".join(ref_parts) if ref_parts else f"Source {i}"
        parts.append(f"[CHUNK {i} — {header}]\n{chunk['text']}\n")

    return "\n---\n".join(parts)


# ── Main RAG Function ──────────────────────────────────────────────────────────
def get_rag_answer(
    question: str,
    filters: Optional[dict] = None,
    n_chunks: int = 8,
    model: str = "gpt-4o-mini",
    max_daily_queries: int = 100,
) -> dict:
    """
    Full RAG pipeline: retrieve → format context → generate answer.

    Returns:
    {
        "answer": str,
        "chunks": list[dict],
        "context": str,
        "usage": dict,
        "error": str | None,
        "guardrail_warning": str,
    }
    """
    # ── Daily limit check ──
    usage = _get_usage_state()
    if usage["queries_today"] >= max_daily_queries:
        return {
            "answer": f"🙏 The daily query limit ({max_daily_queries}) has been reached. "
                       "Please try again tomorrow or ask the administrator to increase the limit.",
            "chunks": [],
            "context": "",
            "usage": usage,
            "error": "daily_limit",
            "guardrail_warning": "",
        }

    # ── Input guardrails ──
    is_safe, reason = check_input_guardrails(question)
    if not is_safe:
        from src.prompts import HARMFUL_REQUEST_RESPONSE, OFF_TOPIC_RESPONSE
        if reason == "harmful":
            return {"answer": HARMFUL_REQUEST_RESPONSE, "chunks": [], "context": "",
                    "usage": usage, "error": "guardrail_input", "guardrail_warning": ""}
        elif reason == "off_topic":
            return {"answer": OFF_TOPIC_RESPONSE, "chunks": [], "context": "",
                    "usage": usage, "error": "guardrail_input", "guardrail_warning": ""}
        else:
            return {"answer": reason, "chunks": [], "context": "",
                    "usage": usage, "error": "guardrail_input", "guardrail_warning": ""}

    # ── Retrieval ──
    try:
        embeddings = get_embeddings()
        chunks = query_collection(question, embeddings, n_results=n_chunks, filters=filters)
    except Exception as e:
        return {
            "answer": f"⚠️ Could not retrieve from knowledge base: {e}\n\nPlease ensure the knowledge base has been built.",
            "chunks": [],
            "context": "",
            "usage": usage,
            "error": "retrieval_error",
            "guardrail_warning": "",
        }

    # No results
    if not chunks or all(c["score"] < 0.15 for c in chunks):
        return {
            "answer": ANSWER_NOT_FOUND,
            "chunks": [],
            "context": "",
            "usage": usage,
            "error": None,
            "guardrail_warning": "",
        }

    # Filter to meaningful chunks
    chunks = [c for c in chunks if c["score"] >= 0.15]

    # ── Format context ──
    context = format_context_for_prompt(chunks)

    # ── Build prompt ──
    filled_prompt = SYSTEM_PROMPT.format(context=context, question=question)

    # ── Call LLM ──
    try:
        from openai import OpenAI
        api_key = st.secrets.get("OPENAI_API_KEY", "")
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": filled_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.2,   # Low temperature for grounded factual answers
            max_tokens=1200,
        )

        answer = response.choices[0].message.content or ANSWER_NOT_FOUND
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens

        _increment_usage(total_tokens)

        # ── Output guardrails ──
        _, gw = check_output_guardrails(answer, context)

        return {
            "answer": answer,
            "chunks": chunks,
            "context": context,
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "queries_today": usage["queries_today"],
            },
            "error": None,
            "guardrail_warning": gw,
        }

    except Exception as e:
        err_msg = str(e)
        if "api_key" in err_msg.lower() or "authentication" in err_msg.lower():
            err_msg = "Invalid or missing OpenAI API key. Please check Settings."
        return {
            "answer": f"⚠️ Error generating answer: {err_msg}",
            "chunks": [],
            "context": context,
            "usage": usage,
            "error": "llm_error",
            "guardrail_warning": "",
        }


# ── Cost Estimation ────────────────────────────────────────────────────────────
def estimate_query_cost(
    prompt_tokens: int,
    completion_tokens: int,
    model: str = "gpt-4o-mini",
) -> float:
    """Estimate USD cost of a query."""
    # Prices per 1M tokens (input / output)
    pricing = {
        "gpt-4o-mini": (0.15, 0.60),
        "gpt-4o": (5.00, 15.00),
        "gpt-4-turbo": (10.00, 30.00),
    }
    in_rate, out_rate = pricing.get(model, (0.15, 0.60))
    cost = (prompt_tokens / 1_000_000) * in_rate + (completion_tokens / 1_000_000) * out_rate
    return cost
