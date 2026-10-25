"""Evaluation harness.

This is intentionally lightweight because CrewAI tool-call traces and final
answers are runtime-dependent. The cases define what evidence coverage should
be inspected during evaluation.
"""

from cases import CASES


def summarize_cases() -> None:
    for case in CASES:
        print(f"\n[{case['name']}]")
        print(f"Query: {case['query']}")
        print("Expected document types:", ", ".join(sorted(case["expected_types"])))


if __name__ == "__main__":
    summarize_cases()
