"""
src/vector_store.py — Pinecone vector store management.
Replaces ChromaDB with permanent cloud storage.
Vectors survive app restarts, redeployments and Streamlit Cloud wipes.
"""

import streamlit as st
from typing import Optional

# ── Constants ──────────────────────────────────────────────────────────────────
INDEX_NAME     = "indispensable-values"
NAMESPACE      = "indispensable-values"
EMBEDDING_DIM  = 1536          # text-embedding-3-small
CLOUD          = "aws"
REGION         = "us-east-1"   # Pinecone free tier region

CHUNK_METADATA_FIELDS = [
    "chunk_id", "chunk_type", "chunk_index",
    "source_id", "source_title", "speaker", "topic",
    "scripture", "chapter", "verse_range",
    "source_url", "page_number", "timestamp",
    "language", "source_type",
]


# ── Pinecone Connection ────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def _get_pinecone_index():
    """
    Return a cached Pinecone index connection.
    Creates the index automatically if it does not yet exist.
    Requires PINECONE_API_KEY in .streamlit/secrets.toml.
    """
    try:
        from pinecone import Pinecone, ServerlessSpec
    except ImportError:
        raise ImportError(
            "Pinecone not installed. Run: pip install pinecone"
        )

    api_key = st.secrets.get("PINECONE_API_KEY", "")
    if not api_key:
        raise ValueError(
            "PINECONE_API_KEY not found in Streamlit secrets. "
            "Add it to .streamlit/secrets.toml."
        )

    pc = Pinecone(api_key=api_key)

    # Create index if it does not exist yet
    existing = [idx.name for idx in pc.list_indexes()]
    if INDEX_NAME not in existing:
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIM,
            metric="cosine",
            spec=ServerlessSpec(cloud=CLOUD, region=REGION),
        )

    return pc.Index(INDEX_NAME)


# ── Write ──────────────────────────────────────────────────────────────────────
def add_chunks_to_store(
    chunk_docs: list[dict],
    embeddings_model,
    batch_size: int = 50,
) -> int:
    """
    Embed and upsert a list of chunk dicts into Pinecone.
    Returns number of chunks added.

    chunk_docs: list of dicts from chunking.py
                (must include 'text', 'chunk_id', and metadata fields)
    embeddings_model: LangChain OpenAIEmbeddings instance
    """
    if not chunk_docs:
        return 0

    index  = _get_pinecone_index()
    added  = 0

    for i in range(0, len(chunk_docs), batch_size):
        batch   = chunk_docs[i : i + batch_size]
        texts   = [doc["text"] for doc in batch]
        vectors = embeddings_model.embed_documents(texts)

        upsert_data = []
        for doc, vec in zip(batch, vectors):
            # Store all metadata fields as strings
            meta = {k: str(doc.get(k, "")) for k in CHUNK_METADATA_FIELDS}
            # Also store the text itself — needed for retrieval
            meta["text"] = doc["text"][:38_000]  # Pinecone metadata limit ~40KB
            upsert_data.append({
                "id":       doc["chunk_id"],
                "values":   vec,
                "metadata": meta,
            })

        index.upsert(vectors=upsert_data, namespace=NAMESPACE)
        added += len(batch)

    return added


# ── Delete ─────────────────────────────────────────────────────────────────────
def delete_chunks_by_source(source_id: str):
    """Remove all chunks belonging to a given source_id from Pinecone."""
    index = _get_pinecone_index()
    try:
        index.delete(
            filter={"source_id": {"$eq": source_id}},
            namespace=NAMESPACE,
        )
    except Exception:
        # Some index tiers require fetching IDs first; graceful fallback
        pass


# ── Query ──────────────────────────────────────────────────────────────────────
def query_collection(
    query_text: str,
    embeddings_model,
    n_results: int = 8,
    filters: Optional[dict] = None,
) -> list[dict]:
    """
    Embed query and retrieve top-n relevant chunks from Pinecone.

    filters: dict of metadata field -> value
             e.g. {"chapter": "13"} or {"speaker": "Swamiji"}
    Returns list of dicts: {text, score, metadata}
    """
    index = _get_pinecone_index()

    # Return early if index is empty
    stats = index.describe_index_stats()
    ns    = getattr(stats, "namespaces", {}) or {}
    total = (
        ns.get(NAMESPACE, {}).get("vector_count", 0)
        if ns
        else getattr(stats, "total_vector_count", 0)
    )
    if total == 0:
        return []

    query_vector = embeddings_model.embed_query(query_text)

    # Build Pinecone filter
    pinecone_filter = None
    if filters:
        valid = {k: v for k, v in filters.items() if v}
        if valid:
            conditions = [{k: {"$eq": str(v)}} for k, v in valid.items()]
            pinecone_filter = (
                {"$and": conditions} if len(conditions) > 1 else conditions[0]
            )

    try:
        results = index.query(
            vector=query_vector,
            top_k=n_results,
            namespace=NAMESPACE,
            filter=pinecone_filter,
            include_metadata=True,
        )
    except Exception:
        # Fallback: retry without filters if filter causes an error
        results = index.query(
            vector=query_vector,
            top_k=n_results,
            namespace=NAMESPACE,
            include_metadata=True,
        )

    chunks = []
    for match in results.get("matches", []):
        meta = dict(match.get("metadata", {}))
        text = meta.pop("text", "")   # Pull text back out of metadata
        chunks.append({
            "text":     text,
            "score":    round(float(match.get("score", 0)), 4),
            "metadata": meta,
        })

    # Sort by relevance descending (Pinecone already does this, but be safe)
    chunks.sort(key=lambda x: x["score"], reverse=True)
    return chunks


# ── Stats ──────────────────────────────────────────────────────────────────────
def get_collection_stats() -> dict:
    """
    Return statistics about the current Pinecone index.
    Used by the Admin Panel KB status display.
    """
    try:
        index = _get_pinecone_index()
        stats = index.describe_index_stats()
        ns    = getattr(stats, "namespaces", {}) or {}
        total = (
            ns.get(NAMESPACE, {}).get("vector_count", 0)
            if ns
            else getattr(stats, "total_vector_count", 0)
        )
        return {
            "total_chunks":  total,
            "total_sources": "—",   # Not directly available from Pinecone stats
            "speakers":      [],
            "chunk_types":   {},
        }
    except Exception:
        return {
            "total_chunks":  0,
            "total_sources": 0,
            "speakers":      [],
            "chunk_types":   {},
        }


# ── Reset ──────────────────────────────────────────────────────────────────────
def clear_collection():
    """
    Delete all vectors from the Pinecone namespace — full KB reset.
    Does NOT delete the index itself, only its contents.
    """
    try:
        index = _get_pinecone_index()
        index.delete(delete_all=True, namespace=NAMESPACE)
    except Exception:
        pass
