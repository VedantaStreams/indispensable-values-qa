"""
src/vector_store.py — ChromaDB vector store management.
Handles persistent storage, indexing, and metadata filtering.
"""

import os
import json
from pathlib import Path
from typing import Optional
import streamlit as st


VECTOR_DB_PATH = Path("data/vector_db")
COLLECTION_NAME = "indispensable_values"

# Metadata fields stored alongside each chunk
CHUNK_METADATA_FIELDS = [
    "chunk_id", "chunk_type", "chunk_index",
    "source_id", "source_title", "speaker", "topic",
    "scripture", "chapter", "verse_range",
    "source_url", "page_number", "timestamp",
    "language", "source_type",
]


@st.cache_resource(show_spinner=False)
def _get_chroma_client():
    """Return a persistent ChromaDB client (cached across Streamlit reruns)."""
    try:
        import chromadb
        from chromadb.config import Settings
        VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(
            path=str(VECTOR_DB_PATH),
            settings=Settings(anonymized_telemetry=False),
        )
        return client
    except ImportError:
        raise ImportError("Install chromadb: pip install chromadb")


def get_or_create_collection():
    """Get or create the main ChromaDB collection."""
    client = _get_chroma_client()
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    return collection


def add_chunks_to_store(
    chunk_docs: list[dict],
    embeddings_model,
    batch_size: int = 50,
) -> int:
    """
    Embed and add a list of chunk dicts to ChromaDB.
    Returns number of chunks added.

    chunk_docs: list of dicts from chunking.py (include 'text' and metadata fields)
    embeddings_model: LangChain embeddings instance
    """
    if not chunk_docs:
        return 0

    collection = get_or_create_collection()
    added = 0

    for i in range(0, len(chunk_docs), batch_size):
        batch = chunk_docs[i : i + batch_size]
        texts = [doc["text"] for doc in batch]

        # Get embeddings
        vectors = embeddings_model.embed_documents(texts)

        ids = [doc["chunk_id"] for doc in batch]
        metadatas = []
        for doc in batch:
            meta = {k: str(doc.get(k, "")) for k in CHUNK_METADATA_FIELDS}
            metadatas.append(meta)

        collection.add(
            ids=ids,
            embeddings=vectors,
            documents=texts,
            metadatas=metadatas,
        )
        added += len(batch)

    return added


def delete_chunks_by_source(source_id: str):
    """Remove all chunks belonging to a given source_id."""
    collection = get_or_create_collection()
    collection.delete(where={"source_id": {"$eq": source_id}})


def query_collection(
    query_text: str,
    embeddings_model,
    n_results: int = 8,
    filters: Optional[dict] = None,
) -> list[dict]:
    """
    Embed query and retrieve top-n relevant chunks.

    filters: dict of metadata field -> value (e.g., {"speaker": "Swamiji"})
    Returns list of dicts: {text, score, metadata}
    """
    collection = get_or_create_collection()

    if collection.count() == 0:
        return []

    query_vector = embeddings_model.embed_query(query_text)

    # Build ChromaDB where clause
    where_clause = None
    if filters:
        valid = {k: v for k, v in filters.items() if v}
        if valid:
            conditions = [{"$and": [{k: {"$eq": str(v)}}]} if False else {k: {"$eq": str(v)}}
                         for k, v in valid.items()]
            where_clause = {"$and": conditions} if len(conditions) > 1 else conditions[0]

    try:
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=min(n_results, collection.count()),
            where=where_clause,
            include=["documents", "metadatas", "distances"],
        )
    except Exception:
        # Fallback without filters if filter fails
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=min(n_results, collection.count()),
            include=["documents", "metadatas", "distances"],
        )

    chunks = []
    if results and results["documents"]:
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            score = round(1 - dist, 4)  # Convert distance to similarity score
            chunks.append({
                "text": doc,
                "score": score,
                "metadata": meta,
            })

    # Sort by relevance score descending
    chunks.sort(key=lambda x: x["score"], reverse=True)
    return chunks


def get_collection_stats() -> dict:
    """Get statistics about the current vector store."""
    try:
        collection = get_or_create_collection()
        total = collection.count()

        # Get unique sources
        if total > 0:
            sample = collection.get(limit=min(total, 1000), include=["metadatas"])
            source_ids = set()
            speakers = set()
            chunk_types = {}
            for meta in sample["metadatas"]:
                source_ids.add(meta.get("source_id", ""))
                speakers.add(meta.get("speaker", ""))
                ct = meta.get("chunk_type", "general")
                chunk_types[ct] = chunk_types.get(ct, 0) + 1
        else:
            source_ids = set()
            speakers = set()
            chunk_types = {}

        return {
            "total_chunks": total,
            "total_sources": len(source_ids),
            "speakers": list(speakers - {""}),
            "chunk_types": chunk_types,
        }
    except Exception:
        return {"total_chunks": 0, "total_sources": 0, "speakers": [], "chunk_types": {}}


def clear_collection():
    """Delete and recreate the collection (full reset)."""
    client = _get_chroma_client()
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
