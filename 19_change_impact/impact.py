"""Semantic change impact discovery over IBM Db2."""

from collections import defaultdict
from typing import Any

from config import settings


def classify_similarity(similarity: float) -> str:
    """Apply the configurable demonstration relevance bands."""
    if similarity > settings.direct_impact_threshold:
        return "direct"
    if similarity >= settings.indirect_impact_threshold:
        return "indirect"
    return "lower_relevance"


def cosine_distance_to_similarity(distance: float) -> float:
    """Convert cosine distance to a normalized similarity for the demo."""
    return 1.0 - distance


def discover_impact(vector_store: Any, change_description: str) -> list[dict]:
    """Retrieve a broad candidate set across the indexed knowledge base."""
    documents = vector_store.similarity_search_with_score(
        change_description,
        k=settings.top_k,
    )

    results = []
    for document, raw_score in documents:
        metadata = document.metadata or {}

        # IBM Db2 vector-store score semantics depend on the configured distance
        # strategy. This demo assumes cosine distance when deriving similarity.
        similarity = cosine_distance_to_similarity(float(raw_score))

        results.append(
            {
                "document_id": metadata.get("DOCUMENT_ID")
                or metadata.get("document_id")
                or "unknown",
                "title": metadata.get("TITLE")
                or metadata.get("title")
                or "Untitled",
                "document_type": (
                    metadata.get("DOCUMENT_TYPE")
                    or metadata.get("document_type")
                    or "unknown"
                ),
                "raw_score": float(raw_score),
                "similarity": similarity,
                "relevance_band": classify_similarity(similarity),
                "content_preview": document.page_content[:500],
                "metadata": metadata,
            }
        )

    return results


def group_by_document_type(results: list[dict]) -> dict[str, list[dict]]:
    grouped = defaultdict(list)
    for result in results:
        grouped[result["document_type"]].append(result)
    return dict(sorted(grouped.items()))
