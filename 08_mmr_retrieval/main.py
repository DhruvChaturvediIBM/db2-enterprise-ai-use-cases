from __future__ import annotations

import argparse

from config import get_settings
from diversity import calculate_diversity, document_overlap
from retrieval import compare_retrieval

def print_documents(title: str, documents) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    for index, document in enumerate(documents, start=1):
        meta = document.metadata
        document_id = meta.get("document_id", document.id)
        print(f"{index}. {document_id} - {meta.get('title', 'Untitled')}")
        print(
            f"   type={meta.get('document_type', 'unknown')} | "
            f"department={meta.get('department', 'unknown')} | "
            f"region={meta.get('region', 'unknown')}"
        )

def print_stats(label: str, documents) -> None:
    stats = calculate_diversity(documents)
    print(f"\n{label}")
    print(f"  Documents: {stats.document_count}")
    print(f"  Unique document types: {stats.unique_document_types}")
    print(f"  Unique departments: {stats.unique_departments}")
    print(f"  Type diversity ratio: {stats.diversity_ratio_by_type:.2f}")
    print(
        f"  Department diversity ratio: "
        f"{stats.diversity_ratio_by_department:.2f}"
    )

def main() -> None:
    parser = argparse.ArgumentParser(
        description="UC08: Compare Db2 similarity search with MMR"
    )
    parser.add_argument("--query", required=True)
    parser.add_argument("--k", type=int, default=None)
    parser.add_argument("--fetch-k", type=int, default=None)
    parser.add_argument("--lambda", dest="lambda_mult", type=float, default=None)
    parser.add_argument("--compare", action="store_true")
    args = parser.parse_args()

    settings = get_settings()
    comparison = compare_retrieval(
        settings=settings,
        query=args.query,
        k=args.k,
        fetch_k=args.fetch_k,
        lambda_mult=args.lambda_mult,
    )

    print(f"Query: {args.query}")
    print(f"MMR lambda_mult: {comparison.lambda_mult}")
    print(f"MMR fetch_k: {comparison.fetch_k}")

    print_documents("NORMAL SIMILARITY SEARCH", comparison.similarity)
    print_documents("MMR SEARCH", comparison.mmr)
    print_stats("SIMILARITY DIVERSITY", comparison.similarity)
    print_stats("MMR DIVERSITY", comparison.mmr)

    overlap = document_overlap(comparison.similarity, comparison.mmr)
    print("\nRESULT OVERLAP")
    print("--------------")
    print(f"Shared document IDs: {overlap}")

if __name__ == "__main__":
    main()
