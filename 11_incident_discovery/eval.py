from __future__ import annotations

from dataclasses import dataclass

from discovery import discover_similar_incidents


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

        if ids and ids[0] in case.relevant:
            top1_hits += 1

        relevant_retrieved += len(set(ids) & case.relevant)

        print(f"\nQuery {number}: {case.query}")
        print(f"Retrieved: {', '.join(ids) or 'none'}")
        print(f"Expected:  {', '.join(sorted(case.relevant))}")
        print(f"Result:    {'PASS' if set(ids) & case.relevant else 'FAIL'}")

    print("\n" + "=" * 50)
    print(f"Top-1 Accuracy: {top1_hits / len(CASES):.2%}")
    print(f"Top-3 Recall:   {relevant_retrieved / total_relevant:.2%}")
    print("=" * 50)


if __name__ == "__main__":
    main()
