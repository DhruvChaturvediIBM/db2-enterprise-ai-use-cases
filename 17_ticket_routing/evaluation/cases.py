EVALUATION_CASES = [
    {
        "ticket": "OOMKilled pods in production namespace, services crashing",
        "team": "Engineering",
        "category": "Kubernetes",
        "priority": "P1",
    },
    {
        "ticket": "User locked out, cannot set up new authenticator app",
        "team": "Identity Platform",
        "category": "Authentication",
        "priority": "P2",
    },
    {
        "ticket": "Payment failing for European customers, error code 503",
        "team": "Banking",
        "category": "Payment Platform",
        "priority": "P1",
    },
    {
        "ticket": "Users cannot authenticate after certificate renewal",
        "team": "Identity Platform",
        "category": "Authentication",
        "priority": "P1",
    },
]


def label_accuracy(actual: str, expected: str) -> bool:
    return actual == expected
