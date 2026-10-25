from __future__ import annotations

from collections import defaultdict

from config import get_settings
from detector import check_duplicate
from evaluation.cases import CASES


def safe_divide(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def main() -> None:
    settings = get_settings()
    rows = []

    print("UC09 evaluation")
    print("=" * 78)

    for case in CASES:
        result = check_duplicate(case["text"], settings=settings)
        actual = result.classification.value
        correct = actual == case["expected"]
        top = result.top_candidate
        rows.append(
            {
                "expected": case["expected"],
                "actual": actual,
                "correct": correct,
            }
        )
        print(f"\nCase: {case['name']}")
        print(f"Expected: {case['expected']}")
        print(f"Actual:   {actual}")
        if top:
            print(f"Top candidate: {top.metadata.get('document_id', top.metadata.get('id', getattr(top.document, 'id', 'unknown')))}")
            print(f"Raw distance: {top.distance:.6f}")
            print(f"Similarity:   {top.similarity:.6f}")
        print(f"Correct:    {'YES' if correct else 'NO'}")

    accuracy = safe_divide(sum(row["correct"] for row in rows), len(rows))
    print("\nOverall")
    print("-------")
    print(f"Correct classifications: {sum(row['correct'] for row in rows)}/{len(rows)}")
    print(f"Accuracy: {accuracy:.2%}")

    labels = sorted({row["expected"] for row in rows} | {row["actual"] for row in rows})
    print("\nPer-class metrics")
    print("-----------------")
    for label in labels:
        true_positive = sum(
            row["expected"] == label and row["actual"] == label for row in rows
        )
        false_positive = sum(
            row["expected"] != label and row["actual"] == label for row in rows
        )
        false_negative = sum(
            row["expected"] == label and row["actual"] != label for row in rows
        )
        precision = safe_divide(true_positive, true_positive + false_positive)
        recall = safe_divide(true_positive, true_positive + false_negative)
        print(f"{label}: precision={precision:.2%}, recall={recall:.2%}")

    print("\nThis is a small demonstration evaluation. Calibrate thresholds with a representative labelled enterprise dataset before production use.")


if __name__ == "__main__":
    main()
