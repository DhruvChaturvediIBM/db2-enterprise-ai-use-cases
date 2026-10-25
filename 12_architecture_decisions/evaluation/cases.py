EVALUATION_CASES = [
    {
        "question": "authentication mechanism for services",
        "expected": "ADR-003",
    },
    {
        "question": "vector store selection",
        "expected": "ADR-001",
    },
    {
        "question": "event-driven processing for payment systems",
        "expected": "ADR-002",
    },
    {
        "question": "why did we move away from the previous payment communication architecture?",
        "expected": "ADR-004",
    },
]


def is_hit(results, expected: str) -> bool:
    return any(
        result.get("document_id") == expected
        for result in results
    )
