from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EvidenceTier(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass(frozen=True)
class ScoreDecision:
    tier: EvidenceTier
    top_distance: float | None
    reason: str


def classify_distance(
    distance: float | None,
    high_max_distance: float,
    medium_max_distance: float,
) -> ScoreDecision:
    if distance is None:
        return ScoreDecision(
            tier=EvidenceTier.LOW,
            top_distance=None,
            reason="No search result was returned.",
        )

    if distance <= high_max_distance:
        return ScoreDecision(
            tier=EvidenceTier.HIGH,
            top_distance=distance,
            reason="The closest result is within the strong-evidence distance range.",
        )

    if distance <= medium_max_distance:
        return ScoreDecision(
            tier=EvidenceTier.MEDIUM,
            top_distance=distance,
            reason="The closest result is usable but outside the strong-evidence range.",
        )

    return ScoreDecision(
        tier=EvidenceTier.LOW,
        top_distance=distance,
        reason="The closest result is outside the configured evidence range.",
    )
