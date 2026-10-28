from __future__ import annotations

import sys
from dataclasses import dataclass

from discovery import discover_similar_incidents

# Minimum fraction of queries whose Top-1 result must be correct for the
# overall evaluation to pass.  Adjust this threshold as the corpus grows.
TOP1_PASS_THRESHOLD = 1.0


@dataclass(frozen=True)
class Case:
    query: str
    relevant: set[str]


CASES = [
    Case(
        "Database connection errors are causing payment requests to fail.",
        {"INC-001", "INC-004"},
    ),
    Case(
        "Users cannot log in after a certificate update.",
        {"INC-002", "INC-005"},
    ),
    Case(
        "Application pods are repeatedly being terminated because of memory exhaustion.",
        {"INC-003"},
    ),
]


def main() -> None:
    top1_hits = 0
    relevant_retrieved = 0
    total_relevant = sum(len(case.relevant) for case in CASES)

    for number, case in enumerate(CASES, 1):
        results = discover_similar_incidents(case.query, k=3)
        ids = [result.incident_id for result in results]

        top1_correct = bool(ids) and ids[0] in case.relevant
        top3_hit = bool(set(ids) & case.relevant)

        if top1_correct:
            top1_hits += 1

        relevant_retrieved += len(set(ids) & case.relevant)

        print(f"\nQuery {number}: {case.query}")
        print(f"Retrieved:    {', '.join(ids) or 'none'}")
        print(f"Expected:     {', '.join(sorted(case.relevant))}")
        # Top-1: was the first result a relevant incident?
        print(f"Top-1 result: {'PASS' if top1_correct else 'FAIL'}")
        # Top-3: was any relevant incident retrieved in the top-3?
        print(f"Top-3 recall: {'PASS' if top3_hit else 'FAIL'}")

    top1_accuracy = top1_hits / len(CASES)
    top3_recall = relevant_retrieved / total_relevant

    print("\n" + "=" * 50)
    print(f"Top-1 Accuracy: {top1_accuracy:.2%}  (threshold: {TOP1_PASS_THRESHOLD:.2%})")
    print(f"Top-3 Recall:   {top3_recall:.2%}")
    print("=" * 50)

    # Note: relevance labels are manually curated for this small sample corpus.
    if top1_accuracy < TOP1_PASS_THRESHOLD:
        print(f"\nEVAL FAILED: Top-1 accuracy {top1_accuracy:.2%} is below the required {TOP1_PASS_THRESHOLD:.2%}.")
        sys.exit(1)

    print("\nEVAL PASSED.")


if __name__ == "__main__":
    main()
