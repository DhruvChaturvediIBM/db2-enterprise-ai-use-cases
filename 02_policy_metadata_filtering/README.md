# UC02 — Policy Assistant with Metadata Filtering

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

In large enterprises, many documents look similar at the vector level. A travel policy for Europe Finance and a travel policy for North America Finance may return similar semantic scores for the same query. Serving the wrong policy is a real compliance risk. This use case shows how structured Db2 metadata (region, department, status, effective_date) acts as a precision filter on top of semantic retrieval.

**College project framing:** Build a filtered document search where results must match both semantic meaning AND structured metadata conditions.  
**Enterprise framing:** A compliance assistant that only surfaces the policy currently active for the correct department and region, regardless of what other similar policies exist.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | Haystack |
| Db2 capability | `Db2DocumentStore`, `Db2EmbeddingRetriever`, metadata filtering |
| Key pattern | Compound filter: `department=Finance AND region=EUROPE AND status=ACTIVE` |
| LLM | Ollama `granite3.1-dense:8b` |

### Flow

```
Question + metadata context (department, region)
  │
  ▼
Compound filter built from user context
  │
  ▼
Db2EmbeddingRetriever (vector + metadata filter applied in Db2)
  │
  ▼
Only matching + semantically relevant documents
  │
  ▼
Prompt + Granite LLM → precise, scoped answer
```

---

## Scope

- Reuse `AI_DEMO.KNOWLEDGE_BASE` from UC01 (documents already have department/region/status metadata)
- Add Haystack metadata filter to `Db2EmbeddingRetriever`
- Demonstrate compound filters: `{department: Finance, region: EUROPE, status: ACTIVE}`
- Show the difference in results WITH and WITHOUT metadata filtering
- Date-aware filter: `effective_date <= TODAY` — never return future or archived policies

**Out of scope:** reranking, agents, date-range queries (UC04 covers that)

---

## How to try it (once code is written)

```bash
source .venv/bin/activate
cd 02_policy_metadata_filtering
python main.py
```

Sample queries:
- `"What is the travel reimbursement policy?"` — without filter (broader results)
- `"What is the travel reimbursement policy?"` — with filter `department=Finance, region=EUROPE` (precise result)

---

## How to test it

**Key test:** Run the same query with and without filter, compare retrieved document IDs.

```bash
python main.py --query "What is the travel policy?" --department Finance --region EUROPE
# Expected retrieved doc: POL-001 (Europe Finance travel policy)
# NOT retrieved: POL-002 (North America travel policy)
```

**SQL validation** (`validation.sql`):
```sql
-- Count active Europe Finance policies
SELECT COUNT(*)
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DEPARTMENT = 'Finance'
  AND REGION = 'EUROPE'
  AND STATUS = 'ACTIVE';

-- Inspect metadata distribution
SELECT DEPARTMENT, REGION, STATUS, COUNT(*) AS DOC_COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY DEPARTMENT, REGION, STATUS
ORDER BY DOC_COUNT DESC;
```

---

## Files (to be created)

```
02_policy_metadata_filtering/
├── README.md
├── main.py         ← runs filtered vs unfiltered comparison
├── filters.py      ← builds Haystack metadata filter objects
├── validation.sql
└── eval.py
```

---

## Enterprise impact

Demonstrates that semantic retrieval alone is insufficient for enterprise policy management. This is one of the most important patterns in the repository — the combination of relational constraints and vector similarity is what makes AI useful in regulated enterprise environments.
