"""
UC01 evaluation: 3 labelled questions.

Checks, per question:
  - retrieval : is the expected document in the Db2 top-k? (hit / reciprocal rank / precision)
  - grounding : does the answer cite the expected document id, e.g. [POL-001]?
  - faithful  : rough keyword-overlap faithfulness (common.evaluation, no LLM call)
"""

from __future__ import annotations

import sys

from rich.console import Console
from rich.table import Table

from config import create_document_store  # must come first: puts the repo root on sys.path
from common.evaluation import RetrievalResult, faithfulness_score, print_retrieval_report
from pipeline import ask, build_rag_pipeline

CASES = [
    {
        "query": "What is the travel reimbursement policy for Europe?",
        "expected": ["POL-001"],
        "must_mention": ["250", "75"],
    },
    {
        "query": "How do I troubleshoot a slow Db2 query?",
        "expected": ["SUP-002"],
        "must_mention": ["RUNSTATS", "index"],
    },
    {
        "query": "What is the data retention requirement for customer transactions?",
        "expected": ["POL-003"],
        "must_mention": ["7 years"],
    },
]

console = Console()


def main() -> int:
    store = create_document_store()
    try:
        if store.count_documents() == 0:
            console.print("[red]Table is empty. Run `python main.py --ingest` first.[/red]")
            return 1

        pipe = build_rag_pipeline(store, top_k=5)
        retrieval, rows = [], []
        for case in CASES:
            out = ask(pipe, case["query"])
            docs = out["documents"]
            retrieval.append(RetrievalResult(case["query"], case["expected"], [d.id for d in docs]))
            answer = out["answer"]
            rows.append(
                (
                    case["query"],
                    all(f"[{e}]" in answer or e in answer for e in case["expected"]),
                    all(m.lower() in answer.lower() for m in case["must_mention"]),
                    faithfulness_score(answer, [d.content for d in docs]),
                )
            )

        print_retrieval_report(retrieval, name="UC01")

        table = Table(title="UC01 - Generation checks")
        table.add_column("Query", style="cyan", max_width=50)
        table.add_column("Cites source", justify="center")
        table.add_column("Key facts", justify="center")
        table.add_column("Faithfulness", justify="right")
        for query, cited, facts, faith in rows:
            table.add_row(query, "✓" if cited else "✗", "✓" if facts else "✗", f"{faith:.2f}")
        console.print(table)

        passed = all(r.hit for r in retrieval)
        console.print(f"\nRetrieval gate: {'[green]PASS' if passed else '[red]FAIL'}[/]")
        return 0 if passed else 1
    finally:
        store.close()


if __name__ == "__main__":
    sys.exit(main())
