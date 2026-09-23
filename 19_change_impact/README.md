# UC19 — Semantic Change Impact Discovery

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

A proposed change to an enterprise system — replacing an authentication mechanism, migrating a database, changing an API contract — can affect many documents and decisions that are not explicitly linked. This use case demonstrates semantic discovery: given a change description, find everything in the enterprise knowledge base that is semantically related and therefore potentially impacted.

**College project framing:** Build a "what else does this touch?" discovery tool using semantic search.  
**Enterprise framing:** A change impact assistant that helps architects and engineers discover the full blast radius of a proposed change — surfacing affected ADRs, runbooks, requirements, incidents, and release notes — before the change is made.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | LangChain (or Haystack) |
| Db2 capability | `DB2VS` `similarity_search()` across ALL document types |
| Key pattern | Cross-type semantic impact discovery |
| LLM | Ollama `granite3.1-dense:8b` — summarises discovered impact |

### Flow

```
Change description: 
"We are replacing the authentication mechanism from API keys to OAuth 2.0 PKCE"
  │
  ▼
Embed change description
  │
  ▼
Db2 similarity search across ALL document types (k=10, broad net)
  │
  ▼
Potentially affected artifacts:
  - ADR-003 (authentication architecture decision)
  - INC-002 (auth failure incident — relevant warning)
  - POL-004 (access control policy)
  - TECH-002 (API gateway configuration)
  │
  ▼
Granite LLM → impact summary with risk assessment
```

---

## Scope

- Accept a change description as input
- Search ALL document types with a broad k (k=10 or k=15)
- Group results by document_type for structured output
- Generate an impact summary via Ollama Granite:
  - What is directly affected (score > 0.75)
  - What may be indirectly affected (score 0.55–0.75)
  - Potential risks surfaced from historical incidents
- Show all Db2 document IDs in the output so each can be manually reviewed

**Important scope:** This is discovery, not impact analysis. The AI surfaces candidates. Engineers confirm actual impact.

---

## How to try it (once code is written)

```bash
source .venv/bin/activate
cd 19_change_impact
python main.py
```

Built-in test changes:
1. `"Replacing authentication from API keys to OAuth 2.0 PKCE"` → ADR-003, INC-002, POL-004, TECH-002
2. `"Migrating payment event processing to Apache Kafka"` → ADR-002, INC-001, RUN-001
3. `"Increasing Db2 connection pool size for all services"` → INC-001, TECH-001, SUP-002

---

## How to test it

```bash
python main.py --change "replacing authentication mechanism"
# Expected: ADR-003, INC-002, POL-004 appear in results
# Expected: LLM summary mentions token rotation, certificate management

python main.py --change "payment service database connection pool"
# Expected: INC-001, RUN-001, TECH-001 appear in results
```

**SQL validation** (`validation.sql`):
```sql
-- Confirm cross-type knowledge is available for impact discovery
SELECT DOCUMENT_TYPE, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY DOCUMENT_TYPE
ORDER BY DOCUMENT_TYPE;

-- Verify ADRs and incidents are indexed (key for change impact)
SELECT DOCUMENT_ID, TITLE, DOCUMENT_TYPE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE IN ('adr', 'incident', 'technical', 'policy')
ORDER BY DOCUMENT_TYPE, DOCUMENT_ID;
```

---

## Files (to be created)

```
19_change_impact/
├── README.md
├── main.py           ← runs change impact discovery
├── impact.py         ← discover_impact() function with group-by-type output
├── validation.sql
└── eval.py
```

---

## Enterprise impact

Demonstrates semantic discovery beyond question answering. Every enterprise change carries risk from things we don't know are connected. This example shows how Db2 vector search surfaces those hidden connections — reducing the risk of unexpected side effects from architectural and operational changes.
