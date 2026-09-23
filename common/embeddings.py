"""
common/embeddings.py
────────────────────
Embedding helpers shared across all use cases.

Default: Ollama nomic-embed-text (local, no API key needed).
Fallback: sentence-transformers (CPU, offline-capable).

Usage
-----
from common.embeddings import get_embedder, embed_text, embed_batch

embedder = get_embedder()
vector   = embed_text("What is the travel policy?")
vectors  = embed_batch(["doc1", "doc2"])
"""

from __future__ import annotations
import os
from typing import Protocol

from common.config import (
    EMBEDDING_PROVIDER, EMBEDDING_MODEL, EMBEDDING_DIM,
    OLLAMA_BASE,
)


class Embedder(Protocol):
    def embed(self, text: str) -> list[float]: ...
    def embed_batch(self, texts: list[str]) -> list[list[float]]: ...
    @property
    def dimension(self) -> int: ...


# ─────────────────────────────────────────────────────────────────────────────
# Ollama embedder (default — uses granite / nomic-embed-text locally)
# ─────────────────────────────────────────────────────────────────────────────
class OllamaEmbedder:
    def __init__(self, model: str = EMBEDDING_MODEL, base_url: str = OLLAMA_BASE):
        import ollama
        self._client = ollama.Client(host=base_url)
        self._model = model
        self._dim = EMBEDDING_DIM

    def embed(self, text: str) -> list[float]:
        resp = self._client.embeddings(model=self._model, prompt=text)
        return resp["embedding"]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self.embed(t) for t in texts]

    @property
    def dimension(self) -> int:
        return self._dim


# ─────────────────────────────────────────────────────────────────────────────
# SentenceTransformers embedder (fallback — CPU, offline)
# ─────────────────────────────────────────────────────────────────────────────
class SentenceTransformerEmbedder:
    _DEFAULT = "all-MiniLM-L6-v2"

    def __init__(self, model: str = _DEFAULT):
        from sentence_transformers import SentenceTransformer
        self._model = SentenceTransformer(model)
        self._dim = self._model.get_sentence_embedding_dimension()

    def embed(self, text: str) -> list[float]:
        return self._model.encode(text, convert_to_numpy=True).tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return self._model.encode(texts, convert_to_numpy=True).tolist()

    @property
    def dimension(self) -> int:
        return self._dim


# ─────────────────────────────────────────────────────────────────────────────
# Factory
# ─────────────────────────────────────────────────────────────────────────────
_embedder_instance: Embedder | None = None


def get_embedder() -> Embedder:
    global _embedder_instance
    if _embedder_instance is None:
        provider = EMBEDDING_PROVIDER
        if provider == "ollama":
            _embedder_instance = OllamaEmbedder()
        elif provider == "sentence_transformers":
            _embedder_instance = SentenceTransformerEmbedder(EMBEDDING_MODEL)
        else:
            raise ValueError(
                f"Unknown EMBEDDING_PROVIDER '{provider}'. "
                "Use 'ollama' or 'sentence_transformers'."
            )
    return _embedder_instance


def embed_text(text: str) -> list[float]:
    return get_embedder().embed(text)


def embed_batch(texts: list[str]) -> list[list[float]]:
    return get_embedder().embed_batch(texts)
