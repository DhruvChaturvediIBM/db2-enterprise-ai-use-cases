"""Evaluation cases for the single-agent research assistant."""

CASES = [
    {
        "name": "authentication_research",
        "query": (
            "What are our authentication architecture decisions and "
            "how do they relate to recent incidents?"
        ),
        "expected_types": {"adr", "incident"},
    },
    {
        "name": "payment_reliability",
        "query": "Summarise what we know about payment service reliability issues.",
        "expected_types": {"incident", "runbook", "technical"},
    },
    {
        "name": "ai_vendor_research",
        "query": (
            "What do I need to know before proposing a new vendor "
            "for our AI platform?"
        ),
        "expected_types": {"policy", "technical", "adr"},
    },
]
