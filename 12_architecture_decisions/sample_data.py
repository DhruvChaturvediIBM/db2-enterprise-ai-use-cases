SAMPLE_ADRS = [
    {
        "document_id": "ADR-001",
        "title": "Select IBM Db2 for enterprise vector storage",
        "status": "ACCEPTED",
        "effective_date": "2025-01-15",
        "affected_system": "AI Platform",
        "decision": "Use IBM Db2 as the enterprise vector storage layer.",
        "context": "The organization needs vector search integrated with governed enterprise data.",
        "reason": "Db2 provides enterprise data governance, transactional integration, and vector search in an existing strategic data platform.",
        "rejected_alternatives": "Pinecone; Weaviate",
    },
    {
        "document_id": "ADR-002",
        "title": "Adopt event-driven architecture for payment processing",
        "status": "ACCEPTED",
        "effective_date": "2025-02-10",
        "affected_system": "Payments",
        "decision": "Use Apache Kafka for asynchronous payment event streaming.",
        "context": "Payment workflows require decoupled asynchronous processing and durable event handling.",
        "reason": "Kafka decouples producers and consumers, supports horizontal scaling, and provides durable replay.",
        "rejected_alternatives": "RabbitMQ due to retention requirements; direct REST due to tight coupling",
    },
    {
        "document_id": "ADR-003",
        "title": "Use OAuth 2.0 with PKCE for service authentication",
        "status": "ACTIVE",
        "effective_date": "2025-03-05",
        "affected_system": "Identity Platform",
        "decision": "Use OAuth 2.0 with PKCE for supported service authentication flows.",
        "context": "Services need a standardized authentication mechanism with strong support for modern application flows.",
        "reason": "OAuth 2.0 with PKCE provides a standard authorization model and avoids sharing long-lived client secrets in supported flows.",
        "rejected_alternatives": "SAML for this service-to-service use case; mTLS as the primary application authorization mechanism",
    },
    {
        "document_id": "ADR-004",
        "title": "Use REST for synchronous service communication",
        "status": "SUPERSEDED",
        "effective_date": "2024-06-20",
        "affected_system": "Payments",
        "decision": "Use REST for synchronous service-to-service communication.",
        "context": "The initial service architecture required straightforward request-response communication.",
        "reason": "REST was widely understood and supported by existing service infrastructure.",
        "rejected_alternatives": "Custom RPC protocol; proprietary messaging interface",
    },
]


def adr_embedding_text(adr: dict) -> str:
    return "\n".join(
        [
            f"Title: {adr['title']}",
            f"Context: {adr['context']}",
            f"Decision: {adr['decision']}",
            f"Reason: {adr['reason']}",
            f"Rejected alternatives: {adr['rejected_alternatives']}",
            f"Affected system: {adr['affected_system']}",
            f"Status: {adr['status']}",
        ]
    )
