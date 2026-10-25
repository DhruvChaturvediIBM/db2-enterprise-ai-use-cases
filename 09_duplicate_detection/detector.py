from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from config import Settings
from db2_store import create_db2_vector_store
from decision import Classification, RecommendedAction, action_for, classify_similarity


@dataclass(frozen=True)
class DuplicateCandidate:
    document: Any
    distance: float
    similarity: float

    @property
    def metadata(self) -> dict[str, Any]:
        return dict(getattr(self.document, "metadata", {}) or {})


@dataclass(frozen=True)
class DuplicateCheckResult:
    classification: Classification
    action: RecommendedAction
    top_candidate: DuplicateCandidate | None
    candidates: list[DuplicateCandidate]
    duplicate_threshold: float
    related_threshold: float


def cosine_distance_to_similarity(distance: float) -> float:
    """Convert Db2 cosine distance to the demonstration similarity scale."""
    return max(0.0, min(1.0, 1.0 - float(distance)))


def _candidate(document: Any, distance: float) -> DuplicateCandidate:
    return DuplicateCandidate(
        document=document,
        distance=float(distance),
        similarity=cosine_distance_to_similarity(float(distance)),
    )


def check_duplicate(
    new_doc: str,
    *,
    settings: Settings | None = None,
    top_k: int | None = None,
    duplicate_threshold: float | None = None,
    related_threshold: float | None = None,
) -> DuplicateCheckResult:
    if not new_doc.strip():
        raise ValueError("new_doc must not be empty.")

    active = settings or __import__("config").get_settings()
    final_k = top_k if top_k is not None else active.top_k
    final_duplicate = (
        duplicate_threshold
        if duplicate_threshold is not None
        else active.duplicate_threshold
    )
    final_related = (
        related_threshold
        if related_threshold is not None
        else active.related_threshold
    )

    if final_k <= 0:
        raise ValueError("top_k must be greater than zero.")
    if not 0.0 <= final_related < final_duplicate <= 1.0:
        raise ValueError(
            "Thresholds must satisfy 0 <= related_threshold "
            "< duplicate_threshold <= 1."
        )

    vector_store = create_db2_vector_store(active)
    raw_results = vector_store.similarity_search_with_score(new_doc, k=final_k)
    candidates = [_candidate(document, score) for document, score in raw_results]

    top = candidates[0] if candidates else None
    classification = (
        classify_similarity(top.similarity, final_duplicate, final_related)
        if top
        else Classification.NEW
    )

    return DuplicateCheckResult(
        classification=classification,
        action=action_for(classification),
        top_candidate=top,
        candidates=candidates,
        duplicate_threshold=final_duplicate,
        related_threshold=final_related,
    )
