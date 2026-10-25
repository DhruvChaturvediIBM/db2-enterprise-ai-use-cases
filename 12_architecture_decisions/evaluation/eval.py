from adr_search import search_adrs
from evaluation.cases import EVALUATION_CASES, is_hit


def evaluate():
    total = len(EVALUATION_CASES)
    top1_correct = 0
    topk_correct = 0

    print("UC12 Architecture Decision Assistant Evaluation")
    print("=" * 52)

    for case in EVALUATION_CASES:
        results = search_adrs(case["question"], k=3)

        top1 = bool(
            results
            and results[0].get("document_id") == case["expected"]
        )
        topk = is_hit(results, case["expected"])

        top1_correct += int(top1)
        topk_correct += int(topk)

        retrieved = [
            result.get("document_id")
            for result in results
        ]

        print(f"\nQuestion: {case['question']}")
        print(f"Expected: {case['expected']}")
        print(f"Retrieved: {retrieved}")
        print(f"Top-1 hit: {top1}")
        print(f"Top-k hit: {topk}")

    top1_accuracy = top1_correct / total if total else 0.0
    topk_hit_rate = topk_correct / total if total else 0.0

    print("\nSummary")
    print("-------")
    print(f"Cases: {total}")
    print(f"Top-1 accuracy: {top1_accuracy:.2%}")
    print(f"Top-k hit rate: {topk_hit_rate:.2%}")


if __name__ == "__main__":
    evaluate()
