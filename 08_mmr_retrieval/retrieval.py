from __future__ import annotations

from dataclasses import dataclass
from langchain_core.documents import Document

from config import Settings
from db2_store import create_db2_vector_store

@dataclass(frozen=True)
class RetrievalComparison:
    similarity: list[Document]
    mmr: list[Document]
    lambda_mult: float
    fetch_k: int

def run_similarity_search(vector_store, query: str, k: int) -> list[Document]:
    return vector_store.similarity_search(query, k=k)

def run_mmr_search(
    vector_store,
    query: str,
    k: int,
    fetch_k: int,
    lambda_mult: float,
) -> list[Document]:
    return vector_store.max_marginal_relevance_search(
        query,
        k=k,
        fetch_k=fetch_k,
        lambda_mult=lambda_mult,
    )

def compare_retrieval(
    settings: Settings,
    query: str,
    k: int | None = None,
    fetch_k: int | None = None,
    lambda_mult: float | None = None,
) -> RetrievalComparison:
    vector_store = create_db2_vector_store(settings)
    final_k = k if k is not None else settings.top_k
    final_fetch_k = fetch_k if fetch_k is not None else settings.fetch_k
    final_lambda = lambda_mult if lambda_mult is not None else settings.lambda_mult

    if final_k <= 0:
        raise ValueError("k must be greater than zero.")
    if final_fetch_k < final_k:
        raise ValueError("fetch_k must be greater than or equal to k.")
    if not 0.0 <= final_lambda <= 1.0:
        raise ValueError("lambda_mult must be between 0.0 and 1.0.")

    similarity = run_similarity_search(vector_store, query, final_k)
    mmr = run_mmr_search(
        vector_store, query, final_k, final_fetch_k, final_lambda
    )

    return RetrievalComparison(
        similarity=similarity,
        mmr=mmr,
        lambda_mult=final_lambda,
        fetch_k=final_fetch_k,
    )
