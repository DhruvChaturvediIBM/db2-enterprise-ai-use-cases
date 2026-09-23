# UC12 — Architecture Decision Assistant

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

Engineering organizations make hundreds of architecture decisions and systematically lose track of them. When a team revisits a technology choice, they often can't find whether it was already evaluated — leading to duplicated work and inconsistent decisions. This use case stores Architecture Decision Records (ADRs) in IBM Db2 and provides instant semantic retrieval of past decisions, context, and the alternatives that were rejected.

**College project framing:** Build a semantic search engine over a structured decision log.  
**Enterprise framing:** An architecture assistant that answers "Have we already decided this?" and surfaces the full rationale — context, decision, rejected alternatives — from the organisation's ADR history stored in Db2.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | LangChain |
| Db2 capability | `DB2VS`, `similarity_search()` |
| Data | ADRs: decision, context, alternatives_rejected, reason, status, affected_system |
| Output | Structured ADR display: decision + rationale + rejected alternatives |

### Example interaction

```
Query: "Have we already evaluated event-driven processing for payment systems?"
  │
  ▼
Db2 similarity search
  │
  ▼
ADR-002: Adopt event-driven architecture for payment processing
  Decision: Apache Kafka for asynchronous payment event streaming
  Reason: Decouples producers, enables horizontal scaling, durable replay
  Rejected: RabbitMQ (insufficient retention), direct REST (tight coupling)
  Status: ACCEPTED
```

---

## Scope

- Populate `AI_DEMO.ARCHITECTURE_DECISIONS` with ADR corpus
- Implement `search_adrs(question: str, k: int = 3)`
- Format output to display each ADR clearly: title, decision, reason, rejected_alternatives, status
- Support filtering by: status (ACCEPTED / PROPOSED / SUPERSEDED / DEPRECATED), affected_system
- Demonstrate: finding superseded decisions (to understand historical context)

---

## How to try it (once code is written)

```bash
source .venv/bin/activate
cd 12_architecture_decisions
python main.py
```

Built-in queries:
- `"Have we evaluated event-driven architecture?"`
- `"What did we decide about authentication mechanisms?"`
- `"Why did we choose IBM Db2 for vector storage?"`

---

## How to test it

```bash
python main.py --query "authentication mechanism for services"
# Expected: ADR-003 (OAuth 2.0 with PKCE) in top-2
# Expected output includes: rejected alternatives (SAML, mTLS)

python main.py --query "vector store selection"
# Expected: ADR-001 (IBM Db2 over Pinecone/Weaviate) in top-1
```

**SQL validation** (`validation.sql`):
```sql
-- Confirm ADRs loaded
SELECT COUNT(*) FROM AI_DEMO.ARCHITECTURE_DECISIONS;

-- List all ADR statuses
SELECT DOCUMENT_ID, TITLE, STATUS
FROM AI_DEMO.ARCHITECTURE_DECISIONS
ORDER BY DOCUMENT_ID;
```

---

## Files (to be created)

```
12_architecture_decisions/
├── README.md
├── main.py           ← interactive ADR search
├── adr_search.py     ← search_adrs() with formatted output
├── validation.sql
└── eval.py
```

---

## Enterprise impact

Connects semantic retrieval with durable organisational knowledge. Architecture teams stop re-evaluating already-decided questions. New engineers can onboard faster. And when an ADR needs to be revisited, the full historical context is available instantly from Db2.
