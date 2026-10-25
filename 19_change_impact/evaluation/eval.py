"""Lightweight retrieval evaluation for UC19."""

from impact import discover_impact
from sample_data import SCENARIOS


def evaluate_case(vector_store, case: dict) -> dict:
    results = discover_impact(vector_store, case["change"])
    found = {item["document_id"] for item in results}
    expected = set(case["expected_documents"])
    hits = found.intersection(expected)

    return {
        "name": case["name"],
        "expected": sorted(expected),
        "found": sorted(hits),
        "candidate_recall": len(hits) / len(expected) if expected else 0.0,
        "document_type_coverage": len(
            {item["document_type"] for item in results if item["document_id"] in hits}
        ),
    }


def evaluate_all(vector_store) -> list[dict]:
    return [evaluate_case(vector_store, case) for case in SCENARIOS]
