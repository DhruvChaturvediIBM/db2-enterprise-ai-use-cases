from evaluation.cases import EVALUATION_CASES, label_accuracy
from router import route_ticket


def evaluate():
    total = len(EVALUATION_CASES)

    team_correct = 0
    category_correct = 0
    priority_correct = 0

    print("UC17 Semantic Ticket Routing Evaluation")
    print("=" * 48)

    for case in EVALUATION_CASES:
        result = route_ticket(case["ticket"])

        team_hit = label_accuracy(result.team, case["team"])
        category_hit = label_accuracy(
            result.category,
            case["category"],
        )
        priority_hit = label_accuracy(
            result.priority,
            case["priority"],
        )

        team_correct += int(team_hit)
        category_correct += int(category_hit)
        priority_correct += int(priority_hit)

        print(f"\nTicket: {case['ticket']}")
        print(
            f"Expected: {case['team']} / "
            f"{case['category']} / {case['priority']}"
        )
        print(
            f"Actual:   {result.team} / "
            f"{result.category} / {result.priority}"
        )
        print(f"Confidence: {result.confidence:.2f}")

    print("\nSummary")
    print("-------")
    print(f"Cases: {total}")
    print(f"Team accuracy: {team_correct / total:.2%}")
    print(f"Category accuracy: {category_correct / total:.2%}")
    print(f"Priority accuracy: {priority_correct / total:.2%}")


if __name__ == "__main__":
    evaluate()
