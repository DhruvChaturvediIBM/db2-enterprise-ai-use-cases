from __future__ import annotations

import argparse

from answer_generator import generate_answer
from config import get_settings
from db2_store import create_db2_vector_store
from score_router import EvidenceTier, classify_distance


def print_results(results) -> None:
    print("\nRetrieved documents:\n")

    for index, (document, distance) in enumerate(results, start=1):
        meta = document.metadata
        document_id = meta.get("document_id", meta.get("id", "unknown"))
        title = meta.get("title", "unknown")

        print(
            f"{index}. [{distance:.4f}] {document_id} — {title}"
        )
        print(
            f"   type={meta.get('document_type', 'unknown')} "
            f"region={meta.get('region', 'unknown')} "
            f"department={meta.get('department', 'unknown')}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="UC07: Db2 similarity search with score-based routing"
    )
    parser.add_argument("--query", required=True)
    parser.add_argument("--k", type=int, default=None)
    args = parser.parse_args()

    settings = get_settings()
    vector_store = create_db2_vector_store(settings)

    k = args.k or settings.top_k
    results = vector_store.similarity_search_with_score(
        args.query,
        k=k,
    )

    print_results(results)

    top_distance = results[0][1] if results else None
    decision = classify_distance(
        distance=top_distance,
        high_max_distance=settings.high_max_distance,
        medium_max_distance=settings.medium_max_distance,
    )

    print("\nEvidence decision:")
    print(f"Tier: {decision.tier.value}")
    print(
        f"Top distance: "
        f"{decision.top_distance:.4f}"
        if decision.top_distance is not None
        else "Top distance: none"
    )
    print(f"Reason: {decision.reason}")

    if decision.tier is EvidenceTier.LOW:
        print(
            "\nAnswer:\n"
            "Insufficient evidence in the knowledge base. "
            "The closest retrieved documents did not meet the "
            "configured evidence threshold."
        )
        return

    documents = [document for document, _ in results]

    answer = generate_answer(
        settings=settings,
        query=args.query,
        documents=documents,
        tier=decision.tier,
    )

    print("\nAnswer:\n")
    print(answer)


if __name__ == "__main__":
    main()
