from __future__ import annotations

import argparse

from discovery import discover_similar_incidents
from sample_data import scenario


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Discover similar historical incidents using IBM Db2."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--incident")
    group.add_argument(
        "--scenario",
        choices=["database", "authentication", "memory"],
    )
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--service")
    parser.add_argument("--severity")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    description = args.incident or scenario(args.scenario)

    results = discover_similar_incidents(
        description=description,
        k=args.k,
        service=args.service,
        severity=args.severity,
    )

    print("=" * 64)
    print("AI-POWERED INCIDENT DISCOVERY")
    print("=" * 64)
    print("\nNew incident:")
    print(description)

    if not results:
        print("\nNo similar incidents found.")
        return

    for index, result in enumerate(results, 1):
        print("\n" + "-" * 64)
        print(f"Match #{index}")
        print("-" * 64)
        print(f"Incident ID : {result.incident_id}")
        print(f"Title       : {result.title}")
        print(f"Severity    : {result.severity}")
        print(f"Service     : {result.service}")
        print(f"Product     : {result.product}")
        if result.score is not None:
            print(f"Score       : {result.score:.4f}")
        print(f"\nRoot Cause : {result.root_cause}")
        print(f"Resolution : {result.resolution}")


if __name__ == "__main__":
    main()
