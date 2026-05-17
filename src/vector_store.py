"""
vector_store.py — ChromaDB collection management for Indispensable Values Q&A.

Provides helpers to get or create the persistent ChromaDB collection,
add documents, and retrieve the LangChain Chroma wrapper for similarity search.
"""

from __future__ import annotations

import os
from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.embeddings import get_embeddings

# Persistent directory for ChromaDB data
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
COLLECTION_NAME = "indispensable_values"


def get_vector_store() -> Chroma:
    """Return a LangChain Chroma vector store backed by the persistent collection."""
    embeddings = get_embeddings()
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )


def add_documents(documents: List[Document]) -> int:
    """Add a list of LangChain Documents to the vector store.

    Returns the number of documents added.
    """
    if not documents:
        return 0
    store = get_vector_store()
    store.add_documents(documents)
    return len(documents)


def get_collection_count() -> int:
    """Return the number of documents currently in the collection."""
    try:
        store = get_vector_store()
        return store._collection.count()
    except Exception:
        return 0


def reset_collection() -> None:
    """Delete and recreate the ChromaDB collection (used by admin KB builder)."""
    import chromadb

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
