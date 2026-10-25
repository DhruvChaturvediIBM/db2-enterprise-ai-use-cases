from db2_store import create_db2_vector_store
from config import get_settings
from score_router import classify_distance
from evaluation.questions import EVALUATION_CASES


def main() -> None:
    settings = get_settings()
    vector_store = create_db2_vector_store(settings)

    for index, case in enumerate(EVALUATION_CASES, start=1):
        results = vector_store.similarity_search_with_score(
            case["query"],
            k=settings.top_k,
        )

        top_distance = results[0][1] if results else None
        decision = classify_distance(
            distance=top_distance,
            high_max_distance=settings.high_max_distance,
            medium_max_distance=settings.medium_max_distance,
        )

        print("=" * 80)
        print(f"Case {index}")
        print(f"Query: {case['query']}")
        print(f"Expected tier: {case['expected_tier']}")
        print(f"Actual tier: {decision.tier.value}")
        print(
            f"Top distance: {top_distance:.4f}"
            if top_distance is not None
            else "Top distance: none"
        )
        print(
            f"Routing match: "
            f"{decision.tier.value == case['expected_tier']}"
        )


if __name__ == "__main__":
    main()
