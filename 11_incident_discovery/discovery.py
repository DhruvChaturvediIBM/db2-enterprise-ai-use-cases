from __future__ import annotations

from dataclasses import dataclass

from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_db2 import DB2VS

from config import table_name
from db import create_connection
from embeddings import create_embeddings


@dataclass
class IncidentResult:
    incident_id: str
    title: str
    severity: str
    service: str
    product: str
    root_cause: str
    resolution: str
    score: float | None


def create_vector_store() -> DB2VS:
    return DB2VS(
        embedding_function=create_embeddings(),
        table_name=table_name(),
        client=create_connection(),
        distance_strategy=DistanceStrategy.COSINE,
    )


def discover_similar_incidents(
    description: str,
    k: int = 3,
    service: str | None = None,
    severity: str | None = None,
) -> list[IncidentResult]:
    if not description.strip():
        raise ValueError("Incident description cannot be empty.")
    if k < 1:
        raise ValueError("k must be >= 1.")

    vector_store = create_vector_store()

    filters: dict[str, list[str]] = {}
    if service:
        filters["service"] = [service]
    if severity:
        filters["severity"] = [severity]

    kwargs = {"filter": filters} if filters else {}

    results = vector_store.similarity_search_with_score(
        description,
        k=k,
        **kwargs,
    )

    return [
        IncidentResult(
            incident_id=str(doc.metadata.get("incident_id", "UNKNOWN")),
            title=str(doc.metadata.get("title", "Untitled")),
            severity=str(doc.metadata.get("severity", "UNKNOWN")),
            service=str(doc.metadata.get("service", "UNKNOWN")),
            product=str(doc.metadata.get("product", "UNKNOWN")),
            root_cause=str(doc.metadata.get("root_cause", "")),
            resolution=str(doc.metadata.get("resolution", "")),
            score=float(score) if score is not None else None,
        )
        for doc, score in results
    ]
