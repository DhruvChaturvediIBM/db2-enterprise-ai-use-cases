EVALUATION_CASES = [
    # HIGH — exact topic in corpus (POL-001)
    {
        "query": "What is the travel policy for Europe?",
        "expected_tier": "HIGH",
    },
    # MEDIUM — related domain (policy/region) but no matching document
    {
        "query": "What are the policies for remote work in Asia?",
        "expected_tier": "MEDIUM",
    },
    # LOW — completely outside the corpus domain; no shared vocabulary
    # with business/technology documents.
    # "quantum computing" still scores ~0.47 because "computing/platform"
    # appear in TECH and PROC documents — not a clean out-of-corpus signal.
    # A culinary query has zero overlap with this enterprise corpus.
    {
        "query": "How do I make a sourdough starter from scratch?",
        "expected_tier": "LOW",
    },
]
