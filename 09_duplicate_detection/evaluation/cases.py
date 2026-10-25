from __future__ import annotations

CASES = [
    # ── Core cases ────────────────────────────────────────────────────────────
    {
        "name": "near_duplicate_travel_policy",
        "text": (
            "All business travel in Europe requires prior approval. "
            "Hotel expenses must remain within the approved European accommodation limit."
        ),
        "expected": "DUPLICATE",
    },
    {
        "name": "related_travel_reimbursement",
        "text": (
            "Employees travelling internationally should submit receipts within ten "
            "business days and use the corporate reimbursement process for eligible expenses."
        ),
        # Similarity ~0.728 — sits 0.02 below the DUPLICATE boundary (0.75).
        "expected": "RELATED",
    },
    {
        "name": "new_software_licensing",
        "text": (
            "Software license procurement requires legal review for open-source "
            "dependencies and renewal terms."
        ),
        # Similarity ~0.634 — genuinely RELATED to POL-005 (procurement/legal overlap).
        "expected": "RELATED",
    },
    {
        "name": "new_culinary_content",
        "text": (
            "To make a sourdough starter, mix equal parts flour and water and leave "
            "at room temperature for 24 hours until bubbles form."
        ),
        # Similarity ~0.480 — no domain overlap with enterprise corpus.
        "expected": "NEW",
    },

    # ── Boundary stress cases ─────────────────────────────────────────────────
    # These probe the thresholds directly. A robust system should still route
    # correctly even when the input lands close to a boundary.
    {
        "name": "stress_near_duplicate_boundary",
        "text": (
            "European business trips must be pre-approved and hotel costs must stay "
            "within the per-night accommodation cap set for tier-1 cities."
        ),
        # Near-paraphrase of POL-001 phrased differently. Should still be DUPLICATE.
        "expected": "DUPLICATE",
    },
    {
        "name": "stress_related_upper_boundary",
        "text": (
            "Expense claims for client entertainment and team offsites require "
            "manager sign-off and original receipts before reimbursement is processed."
        ),
        # Same expense/reimbursement domain as POL-001/POL-002 but different focus.
        # Should be RELATED, not DUPLICATE.
        "expected": "RELATED",
    },
    {
        "name": "stress_related_lower_boundary",
        "text": (
            "Vendor invoices must be matched to approved purchase orders and "
            "validated by accounts payable before payment is released."
        ),
        # Procurement-adjacent but narrower than POL-005. Should be RELATED, not NEW.
        "expected": "RELATED",
    },
    {
        "name": "stress_new_same_industry",
        "text": (
            "The central bank raised its benchmark interest rate by 25 basis points "
            "in response to persistent inflationary pressure."
        ),
        # Financial industry but zero overlap with this enterprise corpus content.
        # Should be NEW.
        "expected": "NEW",
    },
]
