"""
rag_chain.py — RAG pipeline for Indispensable Values Q&A.

Retrieves up to DEFAULT_K chunks from ChromaDB with a similarity score
threshold, builds a context string, and calls GPT-4o-mini to generate
a source-cited, reverent answer.
"""

from __future__ import annotations

from typing import Dict, List, Optional

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from src.prompts import SYSTEM_PROMPT, RAG_PROMPT_TEMPLATE, NO_RESULTS_RESPONSE
from src.vector_store import get_vector_store
from src.guardrails import is_on_topic

DEFAULT_K = 8
SIMILARITY_THRESHOLD = 0.15


def _build_context(docs_and_scores: List) -> str:
    """Format retrieved documents into a numbered context block."""
    lines = []
    for i, (doc, score) in enumerate(docs_and_scores, 1):
        source = doc.metadata.get("source", "Unknown source")
        lines.append(f"[{i}] Source: {source}\n{doc.page_content.strip()}")
    return "\n\n".join(lines)


def answer_question(
    question: str,
    k: int = DEFAULT_K,
    threshold: float = SIMILARITY_THRESHOLD,
) -> Dict:
    """Answer a question using the RAG pipeline.

    Returns a dict with keys:
        answer (str): The generated answer.
        sources (List[str]): Source filenames that were retrieved.
        num_chunks (int): Number of chunks retrieved.
        on_topic (bool): Whether the question passed the topic guardrail.
    """
    # Topic guardrail
    if not is_on_topic(question):
        return {
            "answer": (
                "🙏 This question appears to be outside the scope of the 20 Indispensable Values "
                "as taught by Pūjya Swāmī Aparājitānandajī. "
                "This study companion is grounded exclusively in His teachings on the jñāna sādhana "
                "from Bhagavad Gītā Chapter 13, verses 7–11."
            ),
            "sources": [],
            "num_chunks": 0,
            "on_topic": False,
        }

    api_key = st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        return {
            "answer": "⚠️ OpenAI API key is not configured. Please contact the administrator.",
            "sources": [],
            "num_chunks": 0,
            "on_topic": True,
        }

    # Retrieve relevant chunks with scores
    store = get_vector_store()
    try:
        docs_and_scores = store.similarity_search_with_relevance_scores(question, k=k)
    except Exception as e:
        return {
            "answer": f"⚠️ Knowledge base error: {e}. Please build the knowledge base first.",
            "sources": [],
            "num_chunks": 0,
            "on_topic": True,
        }

    # Apply similarity threshold filter
    filtered = [(doc, score) for doc, score in docs_and_scores if score >= threshold]

    if not filtered:
        return {
            "answer": NO_RESULTS_RESPONSE,
            "sources": [],
            "num_chunks": 0,
            "on_topic": True,
        }

    context = _build_context(filtered)
    sources = list({doc.metadata.get("source", "Unknown") for doc, _ in filtered})

    # Build prompt and call LLM
    prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=question)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        openai_api_key=api_key,
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ]

    response = llm.invoke(messages)
    answer = response.content

    return {
        "answer": answer,
        "sources": sources,
        "num_chunks": len(filtered),
        "on_topic": True,
    }
