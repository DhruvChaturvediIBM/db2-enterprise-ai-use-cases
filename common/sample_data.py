"""
common/sample_data.py
─────────────────────
Shared enterprise knowledge corpus for all 20 use cases.

All use cases draw from this single dataset so metadata relationships
are realistic and consistent.

Domains: Finance, Banking, Insurance, Healthcare, Retail, Technology,
         Customer Support, Procurement, Compliance, Engineering

Document classes:
  - policies
  - technical_documents
  - architecture_decisions
  - support_articles
  - incidents
  - runbooks
  - requirements
  - release_notes
  - procurement_documents
  - compliance_documents
"""

from __future__ import annotations
from datetime import date
from dataclasses import dataclass, field


@dataclass
class EnterpriseDocument:
    document_id: str
    title: str
    content: str
    document_type: str          # policy | technical | adr | support | incident | runbook | requirement | release_note | procurement | compliance
    department: str
    business_unit: str
    region: str                 # GLOBAL | NORTH_AMERICA | EUROPE | ASIA_PACIFIC
    product: str
    classification: str         # PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED
    status: str                 # ACTIVE | ARCHIVED | DRAFT | UNDER_REVIEW
    effective_date: str         # ISO 8601
    owner: str
    source: str
    created_at: str
    updated_at: str
    tags: list[str] = field(default_factory=list)


# ─────────────────────────────────────────────────────────────────────────────
# Policies (10 samples — expand in production)
# ─────────────────────────────────────────────────────────────────────────────
POLICIES: list[EnterpriseDocument] = [
    EnterpriseDocument(
        document_id="POL-001", title="Travel and Expense Reimbursement Policy — Europe Finance",
        content="All business travel within Europe must be pre-approved by the finance manager. Economy class is required for flights under 6 hours. Hotel bookings must not exceed €250 per night in tier-1 cities. Meal allowances are €75 per day. Receipts are required for all expenses above €25. Reimbursement requests must be submitted within 30 days of travel.",
        document_type="policy", department="Finance", business_unit="Corporate Services",
        region="EUROPE", product="N/A", classification="INTERNAL", status="ACTIVE",
        effective_date="2024-01-01", owner="CFO Office", source="HR Portal", created_at="2024-01-01", updated_at="2024-06-15",
        tags=["travel", "expense", "reimbursement", "europe", "finance"],
    ),
    EnterpriseDocument(
        document_id="POL-002", title="Travel and Expense Reimbursement Policy — North America",
        content="All domestic US travel requires manager approval above $500 total cost. Business class is permitted for transcontinental flights over 5 hours. Hotel cap is $275/night in tier-1 cities (New York, San Francisco, Chicago). Meal per diem is $85/day. Receipts required for all expenses above $25. Expense reports due within 45 days.",
        document_type="policy", department="Finance", business_unit="Corporate Services",
        region="NORTH_AMERICA", product="N/A", classification="INTERNAL", status="ACTIVE",
        effective_date="2024-01-01", owner="CFO Office", source="HR Portal", created_at="2024-01-01", updated_at="2024-06-15",
        tags=["travel", "expense", "reimbursement", "north_america", "finance"],
    ),
    EnterpriseDocument(
        document_id="POL-003", title="Data Retention Policy — Customer Transaction Records",
        content="Customer transaction records must be retained for a minimum of 7 years from transaction date per financial regulation FR-2024-11. Records in Db2 must be archived after 2 years and stored in compressed format. Access after archival requires compliance team approval. Deletion after 7 years requires documented sign-off. Applicable to: Banking, Insurance, and Retail divisions.",
        document_type="policy", department="Compliance", business_unit="Legal & Compliance",
        region="GLOBAL", product="N/A", classification="CONFIDENTIAL", status="ACTIVE",
        effective_date="2024-03-01", owner="Chief Compliance Officer", source="Compliance Portal", created_at="2024-03-01", updated_at="2024-03-01",
        tags=["data_retention", "compliance", "transaction", "banking", "7_year"],
    ),
    EnterpriseDocument(
        document_id="POL-004", title="Information Security Policy — Access Control",
        content="All systems containing customer PII must enforce role-based access control (RBAC). Privileged access must be reviewed quarterly. MFA is mandatory for all admin accounts. Access must be revoked within 24 hours of employee offboarding. Shared credentials are prohibited. Annual security training is required for all employees with system access.",
        document_type="policy", department="IT Security", business_unit="Technology",
        region="GLOBAL", product="N/A", classification="CONFIDENTIAL", status="ACTIVE",
        effective_date="2023-07-01", owner="CISO", source="Security Portal", created_at="2023-07-01", updated_at="2024-01-15",
        tags=["security", "access_control", "rbac", "mfa", "pii"],
    ),
    EnterpriseDocument(
        document_id="POL-005", title="Procurement Policy — Vendor Approval Process",
        content="New vendors must complete a due diligence review before contract execution. Contracts above $50,000 require CFO approval. Contracts above $250,000 require board approval. Vendors handling PII must provide SOC 2 Type II certification. Preferred vendor list must be consulted before onboarding new suppliers. Standard payment terms are Net-30.",
        document_type="policy", department="Procurement", business_unit="Corporate Services",
        region="GLOBAL", product="N/A", classification="INTERNAL", status="ACTIVE",
        effective_date="2023-01-01", owner="CPO", source="Procurement Portal", created_at="2023-01-01", updated_at="2024-02-01",
        tags=["procurement", "vendor", "approval", "soc2", "contract"],
    ),
]

# ─────────────────────────────────────────────────────────────────────────────
# Technical documents (5 samples)
# ─────────────────────────────────────────────────────────────────────────────
TECHNICAL_DOCS: list[EnterpriseDocument] = [
    EnterpriseDocument(
        document_id="TECH-001", title="IBM Db2 Vector Storage — Developer Guide",
        content="IBM Db2 supports native VECTOR data type for storing fixed-dimension float arrays. Create a vector column: VECTOR_COL VECTOR(768). Insert a vector: INSERT INTO TABLE VALUES (1, VECTOR('[0.1, 0.2, ...]')). Query by cosine similarity: ORDER BY VECTOR_DISTANCE(QUERY_VECTOR, VECTOR_COL, 'COSINE') FETCH FIRST 5 ROWS ONLY. Indexes on vector columns improve performance at scale.",
        document_type="technical", department="Engineering", business_unit="Technology",
        region="GLOBAL", product="IBM Db2", classification="INTERNAL", status="ACTIVE",
        effective_date="2024-01-01", owner="Db2 Platform Team", source="Engineering Wiki", created_at="2024-01-01", updated_at="2024-09-01",
        tags=["db2", "vector", "embedding", "sql", "developer"],
    ),
    EnterpriseDocument(
        document_id="TECH-002", title="API Gateway Configuration Guide — Rate Limiting",
        content="The enterprise API gateway enforces rate limiting per client ID. Default limits: 1000 requests/min for standard tier, 10,000/min for premium tier. Configure custom limits in gateway-config.yaml. Burst allowance is 20% above tier limit for up to 10 seconds. Exceeding limits returns HTTP 429. Alert thresholds: 80% of limit triggers warning; 95% triggers PagerDuty alert.",
        document_type="technical", department="Engineering", business_unit="Technology",
        region="GLOBAL", product="API Platform", classification="INTERNAL", status="ACTIVE",
        effective_date="2023-09-01", owner="Platform Engineering", source="Engineering Wiki", created_at="2023-09-01", updated_at="2024-04-01",
        tags=["api", "gateway", "rate_limiting", "configuration", "platform"],
    ),
    EnterpriseDocument(
        document_id="TECH-003", title="Kubernetes Deployment Guide — Healthcare Data Services",
        content="Healthcare data services must be deployed in the dedicated compliance namespace 'healthcare-prod'. Resource limits: 4 CPU, 8Gi memory per pod. Persistent volumes must use encrypted storage class 'encrypted-ssd'. Network policies must restrict ingress to authorized internal CIDRs only. Health check endpoint: /health/live. Liveness probe timeout: 10s. Readiness probe: 5s.",
        document_type="technical", department="Engineering", business_unit="Healthcare",
        region="NORTH_AMERICA", product="Healthcare Platform", classification="CONFIDENTIAL", status="ACTIVE",
        effective_date="2024-02-01", owner="Healthcare Platform Team", source="Engineering Wiki", created_at="2024-02-01", updated_at="2024-08-01",
        tags=["kubernetes", "healthcare", "deployment", "compliance", "security"],
    ),
]

# ─────────────────────────────────────────────────────────────────────────────
# Architecture Decision Records (5 samples)
# ─────────────────────────────────────────────────────────────────────────────
ARCHITECTURE_DECISIONS: list[EnterpriseDocument] = [
    EnterpriseDocument(
        document_id="ADR-001", title="ADR-001: Use IBM Db2 as the enterprise vector store",
        content="Context: We evaluated Pinecone, Weaviate, pgvector, and IBM Db2 native VECTOR. Decision: IBM Db2 native VECTOR. Reason: Db2 is already the enterprise data platform. Adding a separate vector DB introduces operational overhead, a new security boundary, and additional licensing. Db2 VECTOR achieves acceptable similarity search performance at our scale (<10M vectors). Alternatives rejected: Pinecone (external SaaS, data sovereignty concerns), pgvector (not our database platform), Weaviate (additional operational overhead). Status: Accepted. Affected systems: All AI retrieval services.",
        document_type="adr", department="Engineering", business_unit="Technology",
        region="GLOBAL", product="AI Platform", classification="INTERNAL", status="ACTIVE",
        effective_date="2024-03-01", owner="Chief Architect", source="Architecture Board", created_at="2024-03-01", updated_at="2024-03-01",
        tags=["adr", "vector_store", "db2", "architecture", "decision"],
    ),
    EnterpriseDocument(
        document_id="ADR-002", title="ADR-002: Adopt event-driven architecture for payment processing",
        content="Context: Current synchronous payment processing creates bottlenecks during peak periods. Decision: Adopt Apache Kafka for asynchronous payment event streaming. Reason: Decouples producers from consumers, enables horizontal scaling, provides durable message replay, and supports audit trail requirements. Alternatives rejected: RabbitMQ (insufficient retention guarantees for financial audit), direct REST calls (tight coupling, no replay). Status: Accepted. Affected systems: Payment Gateway, Reconciliation Service, Fraud Detection.",
        document_type="adr", department="Engineering", business_unit="Banking",
        region="GLOBAL", product="Payment Platform", classification="INTERNAL", status="ACTIVE",
        effective_date="2023-11-01", owner="Banking Architecture Team", source="Architecture Board", created_at="2023-11-01", updated_at="2023-11-01",
        tags=["adr", "event_driven", "kafka", "payment", "architecture"],
    ),
    EnterpriseDocument(
        document_id="ADR-003", title="ADR-003: Authentication mechanism — OAuth 2.0 with PKCE",
        content="Context: Legacy authentication used shared API keys per service. Decision: Migrate all service authentication to OAuth 2.0 with PKCE flow. Reason: API keys are single-factor and difficult to rotate. OAuth 2.0 PKCE supports short-lived tokens, refresh rotation, and fine-grained scopes. Compatible with our identity provider (IBM Security Verify). Alternatives rejected: SAML (too complex for service-to-service), mTLS only (certificate management overhead). Status: Accepted. Affected systems: All internal APIs, Developer Portal.",
        document_type="adr", department="IT Security", business_unit="Technology",
        region="GLOBAL", product="Identity Platform", classification="CONFIDENTIAL", status="ACTIVE",
        effective_date="2024-01-15", owner="Security Architecture", source="Architecture Board", created_at="2024-01-15", updated_at="2024-01-15",
        tags=["adr", "authentication", "oauth2", "pkce", "security"],
    ),
]

# ─────────────────────────────────────────────────────────────────────────────
# Incidents (5 samples)
# ─────────────────────────────────────────────────────────────────────────────
INCIDENTS: list[EnterpriseDocument] = [
    EnterpriseDocument(
        document_id="INC-001", title="INC-001: Payment service database connection pool exhaustion",
        content="Symptoms: Payment service returning HTTP 503. High latency observed. DB2 connection wait times spiking. Root cause: Connection pool size set to 10 during deployment; traffic spike caused pool exhaustion. Resolution: Increased pool size to 50. Added connection pool monitoring. Deployed circuit breaker. Service: Payment Gateway. Severity: P1. Duration: 47 minutes. Environment: Production. Affected customers: ~12,000.",
        document_type="incident", department="Engineering", business_unit="Banking",
        region="NORTH_AMERICA", product="Payment Platform", classification="CONFIDENTIAL", status="ARCHIVED",
        effective_date="2024-05-12", owner="SRE Team", source="Incident Management System", created_at="2024-05-12", updated_at="2024-05-13",
        tags=["incident", "database", "connection_pool", "payment", "p1"],
    ),
    EnterpriseDocument(
        document_id="INC-002", title="INC-002: Authentication service token validation failure after certificate rotation",
        content="Symptoms: Users unable to log in. API calls returning 401. OAuth tokens rejected across all services. Root cause: Certificate rotation completed but token validation service cache not cleared. Old certificate fingerprint still in memory cache for 4 hours. Resolution: Restarted token validation service. Implemented cache invalidation on certificate rotation events. Service: Identity Platform. Severity: P1. Duration: 2 hours 15 minutes. Environment: Production.",
        document_type="incident", department="IT Security", business_unit="Technology",
        region="GLOBAL", product="Identity Platform", classification="CONFIDENTIAL", status="ARCHIVED",
        effective_date="2024-02-28", owner="Identity Platform Team", source="Incident Management System", created_at="2024-02-28", updated_at="2024-03-01",
        tags=["incident", "authentication", "certificate", "cache", "p1"],
    ),
    EnterpriseDocument(
        document_id="INC-003", title="INC-003: Kubernetes pod OOMKilled — Healthcare data processing",
        content="Symptoms: Healthcare data processing pods restarting repeatedly. OOMKilled events in pod logs. Processing queue growing. Root cause: New document batch contained unusually large PDF files (avg 180MB vs normal 2MB). Memory limit of 4Gi insufficient for processing. Resolution: Increased memory limit to 8Gi. Added document size validation at ingestion. Added streaming processor for large files. Service: Healthcare Platform. Severity: P2. Duration: 3 hours.",
        document_type="incident", department="Engineering", business_unit="Healthcare",
        region="NORTH_AMERICA", product="Healthcare Platform", classification="CONFIDENTIAL", status="ARCHIVED",
        effective_date="2024-07-03", owner="Healthcare Platform Team", source="Incident Management System", created_at="2024-07-03", updated_at="2024-07-04",
        tags=["incident", "kubernetes", "oom", "healthcare", "memory", "p2"],
    ),
]

# ─────────────────────────────────────────────────────────────────────────────
# Support articles (3 samples)
# ─────────────────────────────────────────────────────────────────────────────
SUPPORT_ARTICLES: list[EnterpriseDocument] = [
    EnterpriseDocument(
        document_id="SUP-001", title="How to reset two-factor authentication for locked accounts",
        content="If a user is locked out due to 2FA device loss: 1. User submits help desk ticket with employee ID and manager approval. 2. IT Security verifies identity via video call. 3. IT Security temporarily disables 2FA for account (max 4 hours). 4. User sets up new 2FA device. 5. IT Security re-enables 2FA enforcement. All steps are logged for compliance audit. SLA: 4 hours during business hours.",
        document_type="support", department="IT Support", business_unit="Technology",
        region="GLOBAL", product="Identity Platform", classification="INTERNAL", status="ACTIVE",
        effective_date="2023-06-01", owner="IT Help Desk", source="Knowledge Base", created_at="2023-06-01", updated_at="2024-01-01",
        tags=["2fa", "account_lockout", "support", "identity", "security"],
    ),
    EnterpriseDocument(
        document_id="SUP-002", title="Db2 slow query troubleshooting guide",
        content="Common causes of slow Db2 queries: 1. Missing indexes — run EXPLAIN and check index usage. 2. Table statistics out of date — run RUNSTATS ON TABLE. 3. Lock contention — query MON_GET_LOCKS. 4. Insufficient buffer pool — check BUFFERPOOL hit ratio. 5. Full table scans on large tables — add column statistics. Quick diagnostic: SELECT * FROM SYSIBMADM.SNAPSTMT ORDER BY TOTAL_EXEC_TIME DESC FETCH FIRST 10 ROWS ONLY.",
        document_type="support", department="IT Operations", business_unit="Technology",
        region="GLOBAL", product="IBM Db2", classification="INTERNAL", status="ACTIVE",
        effective_date="2023-04-01", owner="Database Operations", source="Knowledge Base", created_at="2023-04-01", updated_at="2024-03-01",
        tags=["db2", "performance", "slow_query", "troubleshooting", "index"],
    ),
]

# ─────────────────────────────────────────────────────────────────────────────
# Runbooks (3 samples)
# ─────────────────────────────────────────────────────────────────────────────
RUNBOOKS: list[EnterpriseDocument] = [
    EnterpriseDocument(
        document_id="RUN-001", title="Runbook: Payment service P1 recovery",
        content="Trigger: Payment service health check failing or error rate > 5% for 2 minutes. Step 1: Check pod status — kubectl get pods -n payments. Step 2: Check DB2 connections — run HEALTH_CHECK_PAYMENTS.sql. Step 3: If connection pool exhausted — kubectl rollout restart deployment/payment-service. Step 4: If DB2 unreachable — escalate to DBA on-call. Step 5: Notify stakeholders via PagerDuty. Step 6: Open incident ticket. Recovery time objective: 15 minutes.",
        document_type="runbook", department="Engineering", business_unit="Banking",
        region="GLOBAL", product="Payment Platform", classification="CONFIDENTIAL", status="ACTIVE",
        effective_date="2024-01-01", owner="SRE Team", source="Operations Wiki", created_at="2024-01-01", updated_at="2024-06-01",
        tags=["runbook", "payment", "p1", "recovery", "sre"],
    ),
]

# ─────────────────────────────────────────────────────────────────────────────
# Procurement documents (3 samples)
# ─────────────────────────────────────────────────────────────────────────────
PROCUREMENT_DOCS: list[EnterpriseDocument] = [
    EnterpriseDocument(
        document_id="PROC-001", title="RFP Requirements — Cloud AI Platform 2024",
        content="Required capabilities: (1) Vector search with >1M document scale. (2) Support for IBM Db2 as primary data source. (3) On-premises deployment option for data sovereignty. (4) SOC 2 Type II certification. (5) SLA: 99.9% uptime. (6) Pricing: per-token or per-query model accepted. (7) Support for Granite/Llama model families. Evaluation criteria: 40% capability, 30% security, 20% price, 10% support.",
        document_type="procurement", department="Procurement", business_unit="Technology",
        region="GLOBAL", product="AI Platform", classification="CONFIDENTIAL", status="ACTIVE",
        effective_date="2024-06-01", owner="Technology Procurement", source="Procurement System", created_at="2024-06-01", updated_at="2024-06-01",
        tags=["procurement", "rfp", "ai_platform", "requirements", "vendor"],
    ),
]

# ─────────────────────────────────────────────────────────────────────────────
# Compliance documents (3 samples)
# ─────────────────────────────────────────────────────────────────────────────
COMPLIANCE_DOCS: list[EnterpriseDocument] = [
    EnterpriseDocument(
        document_id="COMP-001", title="GDPR Compliance Checklist — Customer Data Processing",
        content="Article 13/14 obligations: Privacy notice must be provided at point of data collection. Lawful basis must be documented for each processing activity. Data subject rights: Access (30-day SLA), Erasure (30-day SLA), Portability (30-day SLA). Data Protection Officer contact must be published. Cross-border transfers require Standard Contractual Clauses or adequacy decision. Annual GDPR audit required. Applicable to: All EU customer data. Non-compliance risk: Up to €20M or 4% of global turnover.",
        document_type="compliance", department="Compliance", business_unit="Legal & Compliance",
        region="EUROPE", product="N/A", classification="CONFIDENTIAL", status="ACTIVE",
        effective_date="2024-01-01", owner="Data Protection Officer", source="Compliance Portal", created_at="2024-01-01", updated_at="2024-01-01",
        tags=["gdpr", "compliance", "data_protection", "eu", "privacy"],
    ),
]

# ─────────────────────────────────────────────────────────────────────────────
# Master corpus — all documents combined
# ─────────────────────────────────────────────────────────────────────────────
ALL_DOCUMENTS: list[EnterpriseDocument] = (
    POLICIES
    + TECHNICAL_DOCS
    + ARCHITECTURE_DECISIONS
    + INCIDENTS
    + SUPPORT_ARTICLES
    + RUNBOOKS
    + PROCUREMENT_DOCS
    + COMPLIANCE_DOCS
)


def get_documents(
    document_type: str | None = None,
    department: str | None = None,
    region: str | None = None,
    status: str = "ACTIVE",
) -> list[EnterpriseDocument]:
    """
    Filter the shared corpus by type, department, region, or status.
    Pass status=None to include all statuses.
    """
    docs = ALL_DOCUMENTS
    if document_type:
        docs = [d for d in docs if d.document_type == document_type]
    if department:
        docs = [d for d in docs if d.department == department]
    if region:
        docs = [d for d in docs if d.region == region]
    if status:
        docs = [d for d in docs if d.status == status]
    return docs
