"""Sample test scenarios and expected candidate artifacts."""

SCENARIOS = [
    {
        "name": "authentication_migration",
        "change": "Replacing authentication from API keys to OAuth 2.0 PKCE",
        "expected_documents": ["ADR-003", "INC-002", "POL-004", "TECH-002"],
    },
    {
        "name": "payment_event_migration",
        "change": "Migrating payment event processing to Apache Kafka",
        "expected_documents": ["ADR-002", "INC-001", "RUN-001"],
    },
    {
        "name": "db2_connection_pool",
        "change": "Increasing Db2 connection pool size for all services",
        "expected_documents": ["INC-001", "TECH-001", "SUP-002"],
    },
]
