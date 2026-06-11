"""
RAG Service — builds and manages FAISS vector indexes for paper Q&A.

Flow:
  1. Chunk the report text into overlapping segments.
  2. Embed chunks using SentenceTransformer (all-MiniLM-L6-v2).
  3. Store the FAISS index + raw chunks on disk keyed by paper_id.
  4. At query time, embed the question and retrieve the top-k chunks.
"""
import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

INDEX_DIR = os.path.join(os.path.dirname(__file__), '..', 'indexes')
os.makedirs(INDEX_DIR, exist_ok=True)

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def chunk_text(text: str, chunk_size: int = 600, overlap: int = 120) -> list[str]:
    """Split text into overlapping chunks for retrieval."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def _index_path(paper_id: str) -> str:
    return os.path.join(INDEX_DIR, f'{paper_id}.index')


def _chunks_path(paper_id: str) -> str:
    return os.path.join(INDEX_DIR, f'{paper_id}_chunks.json')


def build_index(paper_id: str, text: str) -> list[str]:
    """Embed text chunks and write FAISS index + chunks JSON to disk."""
    model = get_model()
    chunks = chunk_text(text)
    if not chunks:
        return []

    embeddings = model.encode(chunks, normalize_embeddings=True).astype(np.float32)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatIP(dim)  # cosine similarity (vectors are normalised)
    index.add(embeddings)

    faiss.write_index(index, _index_path(paper_id))
    with open(_chunks_path(paper_id), 'w', encoding='utf-8') as f:
        json.dump(chunks, f)

    return chunks


def load_index(paper_id: str):
    """Load existing FAISS index from disk. Returns (chunks, index) or (None, None)."""
    ip = _index_path(paper_id)
    cp = _chunks_path(paper_id)
    if not os.path.exists(ip) or not os.path.exists(cp):
        return None, None
    index = faiss.read_index(ip)
    with open(cp, encoding='utf-8') as f:
        chunks = json.load(f)
    return chunks, index


def get_or_build_index(paper_id: str, text: str):
    """Return cached index or build a new one."""
    chunks, index = load_index(paper_id)
    if index is None:
        chunks = build_index(paper_id, text)
        chunks, index = load_index(paper_id)
    return chunks, index


def invalidate_index(paper_id: str) -> None:
    """Remove cached index files so the next chat rebuilds the index."""
    for path in [_index_path(paper_id), _chunks_path(paper_id)]:
        if os.path.exists(path):
            os.remove(path)


def retrieve_chunks(paper_id: str, text: str, query: str, k: int = 4) -> list[str]:
    """Return the k most relevant chunks for the query."""
    chunks, index = get_or_build_index(paper_id, text)
    if not chunks or index is None:
        return []

    model = get_model()
    query_emb = model.encode([query], normalize_embeddings=True).astype(np.float32)
    k = min(k, index.ntotal)
    _, indices = index.search(query_emb, k)
    return [chunks[i] for i in indices[0] if 0 <= i < len(chunks)]
