# UC04 — Date-Aware Compliance Knowledge Search

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

A policy can be semantically very relevant but dangerously outdated. In compliance, regulatory, and audit contexts, surfacing an expired policy as an authoritative answer is worse than returning no result. This use case demonstrates how Db2 metadata (effective_date, expiry_date, status) adds temporal safety to vector retrieval — only currently-valid documents are ever surfaced.

**College project framing:** Build a search system that only returns documents valid on a given date.  
**Enterprise framing:** A compliance knowledge assistant that automatically filters out superseded regulations and expired policies, grounding every answer in currently enforceable documents only.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | Haystack |
| Db2 capability | Metadata filtering on date columns, `effective_date`, `status` |
| Key pattern | Temporal safety: `effective_date <= TODAY AND status = 'ACTIVE'` |
| LLM | Ollama `granite3.1-dense:8b` |

### Flow

```
Compliance question
  │
  ▼
Build date filter: effective_date <= TODAY, status = ACTIVE
(optionally: expiry_date >= TODAY for documents with expiry)
  │
  ▼
Db2EmbeddingRetriever with temporal filter
  │
  ▼
Only currently-valid, semantically-relevant documents
  │
  ▼
Prompt + Granite → Answer grounded in current regulations only
```

---

## Scope

- Load corpus including intentionally ARCHIVED / superseded policies (created_at in past, status=ARCHIVED)
- Build a retrieval pipeline that adds `status=ACTIVE` AND `effective_date <= today` filter
- Demonstrate the risk: same query WITHOUT filter returns archived content
- Demonstrate the safety: query WITH filter returns only current content
- Show date arithmetic in Db2: `EFFECTIVE_DATE <= CURRENT DATE`

**Contrast to UC02:** UC02 filters by department/region. UC04 filters by time. Together they compose.

---

## How to try it (once code is written)

```bash
source .venv/bin/activate
cd 04_date_aware_compliance
python main.py
```

Sample queries:
- `"What is the current data retention requirement for customer transaction records?"`
- `"What are the active GDPR obligations for EU customer data?"`

Expected behaviour: archived versions of these policies do NOT appear in results.

---

## How to test it

```bash
python main.py --query "data retention for customer records" --show-both
# Shows: results WITHOUT date filter (may include ARCHIVED docs)
# Shows: results WITH date filter (only ACTIVE, currently effective)
```

**SQL validation** (`validation.sql`):
```sql
-- Verify active vs archived distribution
SELECT STATUS, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY STATUS;

-- Only currently-effective compliance documents
SELECT DOCUMENT_ID, TITLE, EFFECTIVE_DATE, STATUS
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'compliance'
  AND STATUS = 'ACTIVE'
  AND EFFECTIVE_DATE <= CURRENT DATE
ORDER BY EFFECTIVE_DATE DESC;
```

---

## Files (to be created)

```
04_date_aware_compliance/
├── README.md
├── main.py         ← runs safe (filtered) vs unsafe (unfiltered) comparison
├── filters.py      ← builds temporal + metadata filters
├── validation.sql
└── eval.py
```

---

## Enterprise impact

In regulated industries (banking, insurance, healthcare, government), temporal grounding is non-negotiable. This example demonstrates that enterprise RAG must compose semantic similarity with structured time constraints — a pattern that distinguishes production-ready from demo-quality AI systems.
