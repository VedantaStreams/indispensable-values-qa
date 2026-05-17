"""
src/embeddings.py — OpenAI embedding model setup with caching.
Uses text-embedding-3-small for cost efficiency.
"""

import streamlit as st
from functools import lru_cache


@st.cache_resource(show_spinner=False)
def get_embeddings(model: str = "text-embedding-3-small"):
    """
    Return a cached OpenAI embeddings instance.
    Uses Streamlit secrets for API key.
    Model: text-embedding-3-small (~$0.02 / 1M tokens — very cost-effective)
    """
    try:
        from langchain_openai import OpenAIEmbeddings
        api_key = st.secrets.get("OPENAI_API_KEY", "")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in Streamlit secrets.")
        return OpenAIEmbeddings(model=model, openai_api_key=api_key)
    except ImportError:
        raise ImportError("Install langchain-openai: pip install langchain-openai")


def get_embedding_dimension(model: str = "text-embedding-3-small") -> int:
    """Return embedding dimension for a given model."""
    dimensions = {
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "text-embedding-ada-002": 1536,
    }
    return dimensions.get(model, 1536)


def estimate_embedding_cost(
    num_chunks: int,
    avg_chunk_tokens: int = 250,
    model: str = "text-embedding-3-small",
) -> float:
    """
    Estimate cost (USD) of embedding a set of chunks.
    text-embedding-3-small: $0.020 per 1M tokens
    """
    cost_per_million = {
        "text-embedding-3-small": 0.020,
        "text-embedding-3-large": 0.130,
        "text-embedding-ada-002": 0.100,
    }
    rate = cost_per_million.get(model, 0.020)
    total_tokens = num_chunks * avg_chunk_tokens
    return (total_tokens / 1_000_000) * rate
