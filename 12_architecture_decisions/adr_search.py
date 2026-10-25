from typing import Any

from db2_store import get_vector_store
from config import settings


def _metadata_matches(
    metadata: dict[str, Any],
    status: str | None,
    affected_system: str | None,
) -> bool:
    if status and metadata.get("status", "").upper() != status.upper():
        return False

    if affected_system:
        actual = str(metadata.get("affected_system", "")).lower()
        if affected_system.lower() not in actual:
            return False

    return True


def search_adrs(
    question: str,
    k: int = 3,
    status: str | None = None,
    affected_system: str | None = None,
) -> list[dict[str, Any]]:
    if not question or not question.strip():
        raise ValueError("question must not be empty")

    store = get_vector_store()

    fetch_k = max(k * 3, k)
    raw_results = store.similarity_search(
        question,
        k=fetch_k,
    )

    results = []
    for document in raw_results:
        metadata = document.metadata or {}

        if not _metadata_matches(metadata, status, affected_system):
            continue

        results.append(
            {
                "document_id": metadata.get("document_id"),
                "title": metadata.get("title"),
                "status": metadata.get("status"),
                "effective_date": metadata.get("effective_date"),
                "affected_system": metadata.get("affected_system"),
                "decision": metadata.get("decision"),
                "context": metadata.get("context"),
                "reason": metadata.get("reason"),
                "rejected_alternatives": metadata.get(
                    "rejected_alternatives"
                ),
                "content": document.page_content,
            }
        )

        if len(results) >= k:
            break

    return results


def format_adr(result: dict[str, Any], rank: int) -> str:
    return "\n".join(
        [
            f"{rank}. {result.get('document_id', 'UNKNOWN')}",
            f"   Title: {result.get('title', '')}",
            f"   Status: {result.get('status', '')}",
            f"   Effective date: {result.get('effective_date', '')}",
            f"   Affected system: {result.get('affected_system', '')}",
            f"   Decision: {result.get('decision', '')}",
            f"   Reason: {result.get('reason', '')}",
            f"   Rejected alternatives: {result.get('rejected_alternatives', '')}",
        ]
    )
