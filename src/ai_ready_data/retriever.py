from pathlib import Path
from typing import Callable

import numpy as np
import structlog
from sentence_transformers import SentenceTransformer

Retriever = Callable[[str], str]

log = structlog.get_logger()

_EMBED_MODEL = "all-MiniLM-L6-v2"
_CHUNK_WORDS = 200
_TOP_K = 4


def null_retriever(query: str) -> str:
    return ""


def make_vector_retriever(parsed_dir: Path) -> Retriever:
    model = SentenceTransformer(_EMBED_MODEL)

    chunks: list[str] = []
    sources: list[str] = []
    for path in sorted(parsed_dir.glob("*")):
        if path.suffix in (".txt", ".csv"):
            file_chunks = _chunk_text(path.read_text())
            chunks.extend(file_chunks)
            sources.extend([path.name] * len(file_chunks))

    if not chunks:
        return null_retriever

    embeddings = model.encode(chunks, convert_to_numpy=True)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / np.where(norms > 0, norms, 1)

    def retrieve(query: str) -> str:
        q = model.encode([query], convert_to_numpy=True)
        q = q / max(float(np.linalg.norm(q)), 1e-9)
        scores = (embeddings @ q.T).squeeze()
        top = np.argsort(scores)[::-1][:_TOP_K]
        log.info(
            "vector retriever selected chunks",
            sources=[f"{sources[i]} (score={scores[i]:.3f})" for i in top],
        )
        return "\n\n".join(chunks[i] for i in top)

    return retrieve


def _chunk_text(text: str) -> list[str]:
    words = text.split()
    return [
        " ".join(words[i:i + _CHUNK_WORDS])
        for i in range(0, len(words), _CHUNK_WORDS)
        if words[i:i + _CHUNK_WORDS]
    ]
