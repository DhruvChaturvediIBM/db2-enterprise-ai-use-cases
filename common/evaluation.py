"""
common/evaluation.py
────────────────────
Lightweight evaluation helpers for all use cases.

No external benchmark framework required.
Each use case calls these functions to produce a small eval report.

Retrieval metrics: hit_rate, mrr, precision_at_k
Generation metrics: faithfulness (keyword-based, no LLM call required)
"""

from __future__ import annotations
from dataclasses import dataclass


# ─────────────────────────────────────────────────────────────────────────────
# Retrieval evaluation
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class RetrievalResult:
    query: str
    expected_doc_ids: list[str]
    retrieved_doc_ids: list[str]

    @property
    def hit(self) -> bool:
        """True if at least one expected doc is in retrieved results."""
        return bool(set(self.expected_doc_ids) & set(self.retrieved_doc_ids))

    @property
    def precision(self) -> float:
        if not self.retrieved_doc_ids:
            return 0.0
        hits = len(set(self.expected_doc_ids) & set(self.retrieved_doc_ids))
        return hits / len(self.retrieved_doc_ids)

    @property
    def reciprocal_rank(self) -> float:
        for i, doc_id in enumerate(self.retrieved_doc_ids, start=1):
            if doc_id in self.expected_doc_ids:
                return 1.0 / i
        return 0.0


def hit_rate(results: list[RetrievalResult]) -> float:
    """Fraction of queries where at least one relevant doc was retrieved."""
    if not results:
        return 0.0
    return sum(1 for r in results if r.hit) / len(results)


def mean_reciprocal_rank(results: list[RetrievalResult]) -> float:
    """Average reciprocal rank across all queries."""
    if not results:
        return 0.0
    return sum(r.reciprocal_rank for r in results) / len(results)


def precision_at_k(results: list[RetrievalResult], k: int = 5) -> float:
    """Average precision@k across all queries."""
    if not results:
        return 0.0
    truncated = [
        RetrievalResult(r.query, r.expected_doc_ids, r.retrieved_doc_ids[:k])
        for r in results
    ]
    return sum(r.precision for r in truncated) / len(truncated)


# ─────────────────────────────────────────────────────────────────────────────
# Generation evaluation (no LLM call — keyword-based faithfulness check)
# ─────────────────────────────────────────────────────────────────────────────

def faithfulness_score(answer: str, context_docs: list[str]) -> float:
    """
    Rough keyword-overlap faithfulness.
    Returns fraction of answer words that appear in any context document.
    Not a substitute for LLM-graded faithfulness, but useful for quick checks.
    """
    context = " ".join(context_docs).lower()
    words = [w.strip(".,;:!?\"'") for w in answer.lower().split()]
    if not words:
        return 0.0
    overlap = sum(1 for w in words if len(w) > 4 and w in context)
    return overlap / len(words)


# ─────────────────────────────────────────────────────────────────────────────
# Report printer
# ─────────────────────────────────────────────────────────────────────────────

def print_retrieval_report(results: list[RetrievalResult], name: str = "Eval") -> None:
    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(title=f"[bold]{name} — Retrieval Evaluation[/bold]")
    table.add_column("Query", style="cyan", max_width=50)
    table.add_column("Hit", justify="center")
    table.add_column("RR", justify="right")
    table.add_column("Precision", justify="right")

    for r in results:
        table.add_row(
            r.query[:48] + "…" if len(r.query) > 48 else r.query,
            "✓" if r.hit else "✗",
            f"{r.reciprocal_rank:.2f}",
            f"{r.precision:.2f}",
        )

    console.print(table)
    console.print(f"[bold]Hit Rate:[/bold]  {hit_rate(results):.2%}")
    console.print(f"[bold]MRR:[/bold]       {mean_reciprocal_rank(results):.3f}")
    console.print(f"[bold]P@5:[/bold]       {precision_at_k(results, k=5):.2%}")
