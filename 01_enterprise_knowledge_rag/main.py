"""
UC01 - Enterprise Knowledge Assistant (Haystack + IBM Db2)

Usage
-----
    python main.py --query "What is the travel policy for Europe?"
    python main.py                         # runs the 3 sample questions
    python main.py --ingest                # (re)load the corpus, then answer
    python main.py --recreate --ingest     # drop + recreate the Db2 table first
"""

from __future__ import annotations

import argparse

from rich.console import Console
from rich.table import Table

from config import TABLE_NAME, create_document_store
from ingest import ingest
from pipeline import ask, build_rag_pipeline

SAMPLE_QUESTIONS = [
    "What is the travel reimbursement policy for Europe?",
    "How do I troubleshoot a slow Db2 query?",
    "What is the data retention requirement for customer transactions?",
]

console = Console()


def print_result(question: str, result: dict) -> None:
    console.rule(f"[bold]{question}")
    table = Table(title="Retrieved from Db2 (top-k)")
    table.add_column("#", justify="right")
    table.add_column("Document", style="cyan")
    table.add_column("Title", max_width=60)
    table.add_column("Distance", justify="right")
    table.add_column("Similarity", justify="right")
    for i, doc in enumerate(result["documents"], start=1):
        distance = float(doc.score)  # IBMDb2DocumentStore returns raw Db2 cosine distance
        table.add_row(str(i), doc.id, str(doc.meta.get("title", "")), f"{distance:.4f}", f"{1 - distance:.4f}")
    console.print(table)
    console.print(f"\n[bold green]Answer[/bold green]\n{result['answer']}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="UC01: Enterprise Knowledge Assistant")
    parser.add_argument("--query", help="Question to ask. Omit to run the 3 sample questions.")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--ingest", action="store_true", help="Embed and load the corpus into Db2 before querying")
    parser.add_argument("--recreate", action="store_true", help="Drop and recreate the Db2 table (implies --ingest)")
    args = parser.parse_args()

    store = create_document_store(recreate_table=args.recreate)
    try:
        if args.ingest or args.recreate or store.count_documents() == 0:
            console.print(f"Ingesting corpus into [bold]{TABLE_NAME}[/bold] ...")
            console.print(f"Wrote {ingest(store)} documents.")
        console.print(f"{TABLE_NAME}: {store.count_documents()} documents\n")

        pipe = build_rag_pipeline(store, top_k=args.top_k)
        for question in [args.query] if args.query else SAMPLE_QUESTIONS:
            print_result(question, ask(pipe, question))
    finally:
        store.close()


if __name__ == "__main__":
    main()
