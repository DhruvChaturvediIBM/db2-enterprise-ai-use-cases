from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from db2_store import get_vector_store
from config import settings


@dataclass(frozen=True)
class RoutingSuggestion:
    team: str
    category: str
    priority: str
    confidence: float
    candidates: list[dict[str, Any]]


def _normalize_score(raw_score: float) -> float:
    """
    Convert cosine distance into normalized similarity.

    Db2VS score semantics depend on the configured distance strategy.
    This demonstration assumes cosine distance, where lower is better.
    """
    similarity = 1.0 - float(raw_score)
    return max(0.0, min(1.0, similarity))


def _weighted_vote(
    candidates: list[dict[str, Any]],
    field: str,
) -> tuple[str, float, float]:
    totals: dict[str, float] = defaultdict(float)

    for candidate in candidates:
        label = candidate.get(field)
        if not label:
            continue
        totals[str(label)] += candidate["similarity"]

    if not totals:
        return "UNKNOWN", 0.0, 0.0

    ranked = sorted(
        totals.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    winner, winning_weight = ranked[0]
    second_weight = ranked[1][1] if len(ranked) > 1 else 0.0

    confidence = (
        (winning_weight - second_weight) / winning_weight
        if winning_weight > 0
        else 0.0
    )

    return winner, winning_weight, confidence


def route_ticket(
    text: str,
    k: int | None = None,
) -> RoutingSuggestion:
    if not text or not text.strip():
        raise ValueError("ticket text must not be empty")

    top_k = k or settings.top_k
    store = get_vector_store()

    raw_results = store.similarity_search_with_score(
        text,
        k=top_k,
    )

    candidates = []

    for document, raw_score in raw_results:
        metadata = document.metadata or {}

        candidates.append(
            {
                "document_id": metadata.get("document_id"),
                "title": metadata.get("title"),
                "team": metadata.get("team"),
                "category": metadata.get("category"),
                "priority": metadata.get("priority"),
                "product": metadata.get("product"),
                "resolution_summary": metadata.get(
                    "resolution_summary"
                ),
                "raw_score": float(raw_score),
                "similarity": _normalize_score(float(raw_score)),
            }
        )

    team, _, team_confidence = _weighted_vote(candidates, "team")
    category, _, category_confidence = _weighted_vote(
        candidates, "category"
    )
    priority, _, priority_confidence = _weighted_vote(
        candidates, "priority"
    )

    confidence = min(
        team_confidence,
        category_confidence,
        priority_confidence,
    )

    return RoutingSuggestion(
        team=team,
        category=category,
        priority=priority,
        confidence=confidence,
        candidates=candidates,
    )
