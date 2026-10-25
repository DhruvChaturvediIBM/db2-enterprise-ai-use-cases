"""UC19: Semantic Change Impact Discovery."""

import argparse

from db2_store import build_db2_vector_store
from impact import discover_impact, group_by_document_type
from summarizer import summarize_impact


DEFAULT_CHANGE = "Replacing authentication from API keys to OAuth 2.0 PKCE"


def print_results(change: str, results: list[dict]) -> None:
    print("\n=== Semantic Change Impact Discovery ===")
    print(f"Change: {change}")
    print(f"Candidates: {len(results)}\n")

    grouped = group_by_document_type(results)

    for document_type, items in grouped.items():
        print(f"[{document_type}]")
        for item in items:
            print(
                f"  {item['document_id']} | {item['title']} | "
                f"similarity={item['similarity']:.3f} | "
                f"raw_score={item['raw_score']:.3f} | "
                f"band={item['relevance_band']}"
            )
            print(f"    {item['content_preview']}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--change", default=DEFAULT_CHANGE)
    args = parser.parse_args()

    store = build_db2_vector_store()
    results = discover_impact(store, args.change)

    print_results(args.change, results)

    print("=== LLM Discovery Summary ===")
    print(summarize_impact(args.change, results))
    print(
        "\nHuman review required: retrieved candidates are discovery evidence, "
        "not a final impact determination."
    )


if __name__ == "__main__":
    main()
