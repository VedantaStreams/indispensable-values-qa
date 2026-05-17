"""
embeddings.py — OpenAI embedding generation for Indispensable Values Q&A.

Uses text-embedding-3-small via the LangChain OpenAI integration.
"""

from __future__ import annotations

import streamlit as st
from langchain_openai import OpenAIEmbeddings


def get_embeddings() -> OpenAIEmbeddings:
    """Return an OpenAIEmbeddings instance using the app's API key."""
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=api_key,
    )
