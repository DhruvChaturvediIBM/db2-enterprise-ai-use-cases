# UC10 — Semantic Recommendation Engine

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

Enterprise platforms need to surface related artifacts without relying on manually created links or exact keyword tags. A new incident report should surface similar past incidents. An open requirement should suggest related architectural decisions. This use case demonstrates IBM Db2 vector search as a universal recommendation primitive — reusable across any entity type.

**College project framing:** Build a "you may also like" recommendation system for enterprise documents using vector similarity.  
**Enterprise framing:** A semantic recommendation layer that works across any enterprise artifact type — incidents surface similar incidents, requirements surface related requirements, support tickets surface related knowledge articles — all powered by a single Db2 vector search.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | LangChain |
| Db2 capability | `DB2VS` `similarity_search()`, `similarity_search_by_vector()` |
| Key pattern | "Find similar to THIS document" (not a text query — a vector query) |
| Input | An existing document ID → fetch its embedding → search by vector |

### Recommendation modes

```
By document ID:   recommend_similar(doc_id="INC-001", k=3)
By text:          recommend_similar(text="payment service crash", k=3)
By vector:        similarity_search_by_vector(embedding, k=3)
```

---

## Scope

- Implement `recommend_similar(doc_id, k=5)`:
  1. Fetch existing document embedding from Db2 by ID
  2. Call `similarity_search_by_vector(embedding, k=5)` — no text encoding needed
  3. Exclude the source document from results
  4. Return top-k similar documents with scores
- Demonstrate across multiple entity types:
  - Incident → similar incidents
  - ADR → related ADRs
  - Support article → similar support articles
- Optionally filter by document_type for type-consistent recommendations

---

## How to try it (once code is written)

```bash
source .venv/bin/activate
cd 10_semantic_recommendation
python main.py
```

Built-in demo scenarios:
- `recommend_similar("INC-001")` → surfaces INC-002, INC-003 (all P1/P2 production incidents)
- `recommend_similar("ADR-001")` → surfaces ADR-002, ADR-003 (architectural decisions)
- `recommend_similar("POL-001")` → surfaces POL-002 (similar travel policy, different region)

---

## How to test it

```bash
python main.py --doc_id INC-001
# Expected: INC-002 and/or INC-003 appear in top-3 (both are production incidents)
# Expected: POL-001 does NOT appear (different semantic space)

python main.py --text "authentication failure after certificate change"
# Expected: INC-002 appears (certificate rotation auth failure)
```

**SQL validation** (`validation.sql`):
```sql
-- Confirm all document IDs are in Db2 for recommendation input
SELECT DOCUMENT_ID, DOCUMENT_TYPE, TITLE
FROM AI_DEMO.KNOWLEDGE_BASE
ORDER BY DOCUMENT_TYPE, DOCUMENT_ID;
```

---

## Files (to be created)

```
10_semantic_recommendation/
├── README.md
├── main.py           ← demo: shows recommendations for several document IDs
├── recommender.py    ← recommend_similar() function
├── validation.sql
└── eval.py
```

---

## Enterprise impact

Demonstrates vector search as a universal application primitive — not only useful for answering questions, but for building recommendation features across any enterprise artifact type. One Db2 vector table; unlimited recommendation use cases layered on top.
