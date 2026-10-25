from __future__ import annotations

from dataclasses import dataclass
from langchain_core.documents import Document

@dataclass(frozen=True)
class DiversityStats:
    document_count: int
    unique_document_types: int
    unique_departments: int
    diversity_ratio_by_type: float
    diversity_ratio_by_department: float
    document_ids: tuple[str, ...]

def _values(documents: list[Document], field: str) -> set[str]:
    return {
        str(document.metadata[field])
        for document in documents
        if document.metadata.get(field)
    }

def calculate_diversity(documents: list[Document]) -> DiversityStats:
    count = len(documents)
    types = _values(documents, "document_type")
    departments = _values(documents, "department")
    ids = tuple(
        str(document.metadata.get("document_id", document.id))
        for document in documents
    )

    return DiversityStats(
        document_count=count,
        unique_document_types=len(types),
        unique_departments=len(departments),
        diversity_ratio_by_type=len(types) / count if count else 0.0,
        diversity_ratio_by_department=len(departments) / count if count else 0.0,
        document_ids=ids,
    )

def document_overlap(first: list[Document], second: list[Document]) -> int:
    first_ids = set(calculate_diversity(first).document_ids)
    second_ids = set(calculate_diversity(second).document_ids)
    return len(first_ids.intersection(second_ids))
