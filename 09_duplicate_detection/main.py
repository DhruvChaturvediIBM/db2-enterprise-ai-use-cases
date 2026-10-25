from __future__ import annotations

import argparse

from config import get_settings
from decision import Classification
from detector import DuplicateCandidate, DuplicateCheckResult, check_duplicate

TEST_CASES = {
    "duplicate": (
        "All business travel in Europe requires prior approval. "
        "Hotel expenses must remain within the approved European accommodation limit."
    ),
    "related": (
        "Employees travelling internationally should submit receipts within ten "
        "business days and use the corporate reimbursement process for eligible expenses."
    ),
    "new": (
        "To make a sourdough starter, mix equal parts flour and water and leave "
        "at room temperature for 24 hours until bubbles form."
    ),
}


def candidate_label(candidate: DuplicateCandidate) -> str:
    metadata = candidate.metadata
    document_id = metadata.get("document_id") or metadata.get("id") or getattr(
        candidate.document, "id", None
    ) or "unknown"
    title = metadata.get("title") or metadata.get("TITLE") or "Untitled"
    document_type = metadata.get("document_type") or metadata.get("DOCUMENT_TYPE") or "unknown"
    department = metadata.get("department") or metadata.get("DEPARTMENT") or "unknown"
    region = metadata.get("region") or metadata.get("REGION") or "unknown"
    return (
        f"{document_id} | {title} | type={document_type} | "
        f"department={department} | region={region}"
    )


def print_result(text: str, result: DuplicateCheckResult) -> None:
    print("\n" + "=" * 78)
    print("UC09 - SEMANTIC DUPLICATE KNOWLEDGE DETECTION")
    print("=" * 78)
    print(f"Input: {text}")
    print(f"Classification: {result.classification.value}")
    print(f"Recommended action: {result.action.value}")
    print(f"Duplicate threshold: {result.duplicate_threshold:.2f}")
    print(f"Related threshold:   {result.related_threshold:.2f}")

    if not result.top_candidate:
        print("\nNo existing candidates were returned. Treating input as NEW.")
        return

    top = result.top_candidate
    print("\nTop candidate")
    print("-------------")
    print(candidate_label(top))
    print(f"Raw cosine distance: {top.distance:.6f}")
    print(f"Derived similarity:  {top.similarity:.6f}")

    print("\nTop candidates")
    print("--------------")
    for index, candidate in enumerate(result.candidates, start=1):
        print(f"{index}. {candidate_label(candidate)}")
        print(
            f"   distance={candidate.distance:.6f} | "
            f"similarity={candidate.similarity:.6f}"
        )

    if result.classification is Classification.DUPLICATE:
        print("\nDecision rationale: the closest existing document crossed the duplicate threshold.")
    elif result.classification is Classification.RELATED:
        print("\nDecision rationale: the closest existing document crossed the related threshold but not the duplicate threshold.")
    else:
        print("\nDecision rationale: the closest existing document did not cross the related threshold.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="UC09: Detect semantic duplicates in enterprise knowledge"
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="New document text to classify")
    source.add_argument(
        "--case",
        choices=["duplicate", "related", "new", "all"],
        help="Run a built-in demonstration case",
    )
    parser.add_argument("--top-k", type=int, default=None)
    parser.add_argument("--duplicate-threshold", type=float, default=None)
    parser.add_argument("--related-threshold", type=float, default=None)
    args = parser.parse_args()

    settings = get_settings()
    texts = (
        [args.text]
        if args.text is not None
        else [TEST_CASES[name] for name in (TEST_CASES if args.case == "all" else [args.case])]
    )

    for text in texts:
        result = check_duplicate(
            text,
            settings=settings,
            top_k=args.top_k,
            duplicate_threshold=args.duplicate_threshold,
            related_threshold=args.related_threshold,
        )
        print_result(text, result)


if __name__ == "__main__":
    main()
