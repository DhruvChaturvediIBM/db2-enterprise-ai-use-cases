from __future__ import annotations

from enum import Enum


class Classification(str, Enum):
    DUPLICATE = "DUPLICATE"
    RELATED = "RELATED"
    NEW = "NEW"


class RecommendedAction(str, Enum):
    HOLD = "HOLD"
    REVIEW = "REVIEW"
    INGEST = "INGEST"


def classify_similarity(
    similarity: float,
    duplicate_threshold: float,
    related_threshold: float,
) -> Classification:
    if similarity >= duplicate_threshold:
        return Classification.DUPLICATE
    if similarity >= related_threshold:
        return Classification.RELATED
    return Classification.NEW


def action_for(classification: Classification) -> RecommendedAction:
    return {
        Classification.DUPLICATE: RecommendedAction.HOLD,
        Classification.RELATED: RecommendedAction.REVIEW,
        Classification.NEW: RecommendedAction.INGEST,
    }[classification]
