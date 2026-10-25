import argparse

from config import settings
from router import RoutingSuggestion, route_ticket


BUILT_IN_TICKETS = [
    "OOMKilled pods in production namespace, services crashing",
    "User locked out, cannot set up new authenticator app",
    "Payment failing for European customers, error code 503",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="UC17 Semantic Ticket Routing"
    )
    parser.add_argument(
        "--ticket",
        help="Ticket text to route.",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=settings.top_k,
        help="Number of historical tickets to retrieve.",
    )
    return parser.parse_args()


def print_suggestion(ticket: str, suggestion: RoutingSuggestion):
    print(f"\nTicket: {ticket}")
    print("\nRouting suggestion")
    print("------------------")
    print(f"Suggested Team: {suggestion.team}")
    print(f"Suggested Category: {suggestion.category}")
    print(f"Suggested Priority: {suggestion.priority}")
    print(f"Routing Confidence: {suggestion.confidence:.2f}")

    if suggestion.confidence < settings.routing_confidence_threshold:
        print(
            "Confidence Gate: REVIEW "
            f"(threshold={settings.routing_confidence_threshold:.2f})"
        )
    else:
        print("Confidence Gate: ELIGIBLE FOR ROUTING")

    print("\nSupporting historical tickets")
    print("-----------------------------")

    for index, candidate in enumerate(
        suggestion.candidates,
        start=1,
    ):
        print(f"\n{index}. {candidate['document_id']}")
        print(f"   Title: {candidate['title']}")
        print(f"   Similarity: {candidate['similarity']:.2f}")
        print(f"   Raw score: {candidate['raw_score']:.4f}")
        print(f"   Team: {candidate['team']}")
        print(f"   Category: {candidate['category']}")
        print(f"   Priority: {candidate['priority']}")
        print(f"   Product: {candidate['product']}")
        print(
            "   Resolution: "
            f"{candidate['resolution_summary']}"
        )


def main():
    args = parse_args()

    tickets = [args.ticket] if args.ticket else BUILT_IN_TICKETS

    for ticket in tickets:
        suggestion = route_ticket(ticket, k=args.k)
        print_suggestion(ticket, suggestion)


if __name__ == "__main__":
    main()
