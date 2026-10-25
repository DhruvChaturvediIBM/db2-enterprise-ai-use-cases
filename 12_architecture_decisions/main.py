import argparse

from adr_search import format_adr, search_adrs
from config import settings


BUILT_IN_QUERIES = [
    "Have we evaluated event-driven architecture?",
    "What did we decide about authentication mechanisms?",
    "Why did we choose IBM Db2 for vector storage?",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="UC12 Architecture Decision Assistant"
    )
    parser.add_argument(
        "--query",
        help="Architecture question to search for.",
    )
    parser.add_argument(
        "--status",
        help="Optional ADR status filter.",
    )
    parser.add_argument(
        "--system",
        dest="affected_system",
        help="Optional affected-system filter.",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=settings.top_k,
        help="Number of ADRs to return.",
    )
    return parser.parse_args()


def run_query(
    query: str,
    k: int,
    status: str | None = None,
    affected_system: str | None = None,
):
    print(f"\nQuery: {query}\n")
    results = search_adrs(
        query,
        k=k,
        status=status,
        affected_system=affected_system,
    )

    if not results:
        print("No matching ADRs found.")
        return

    for index, result in enumerate(results, start=1):
        print(format_adr(result, index))
        print()


def main():
    args = parse_args()

    if args.query:
        run_query(
            args.query,
            args.k,
            status=args.status,
            affected_system=args.affected_system,
        )
        return

    for query in BUILT_IN_QUERIES:
        run_query(
            query,
            args.k,
            status=args.status,
            affected_system=args.affected_system,
        )


if __name__ == "__main__":
    main()
