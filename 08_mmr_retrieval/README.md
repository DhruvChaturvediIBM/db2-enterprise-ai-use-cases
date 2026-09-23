# UC08 — Diverse Enterprise Retrieval with MMR

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

For broad questions, pure similarity search tends to return multiple documents that say almost the same thing. Maximal Marginal Relevance (MMR) balances relevance with diversity — ensuring the retrieved context covers multiple facets of a broad question rather than repeating the same information from slightly different documents.

**College project framing:** Implement MMR to get diverse search results instead of near-duplicate top-k.  
**Enterprise framing:** A modernisation or architectural review assistant that retrieves context covering architecture, security, deployment, and operations — not five nearly-identical architecture documents.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | LangChain |
| Db2 capability | `DB2VS` VectorStore |
| Core API | `max_marginal_relevance_search(query, k=5, fetch_k=20, lambda_mult=0.5)` |
| Key parameter | `lambda_mult`: 0.0 = maximum diversity, 1.0 = maximum similarity |

### MMR vs Similarity comparison

```
Query: "What should we consider when modernising our payment platform?"

Pure similarity top-5:        MMR top-5:
  ADR-002 (event-driven)        ADR-002 (event-driven)       ← relevant
  ADR-003 (authentication)      ADR-003 (authentication)     ← diverse
  ADR-001 (vector store)        INC-001 (payment incident)   ← diverse
  ADR-001 variant               RUN-001 (recovery runbook)   ← actionable
  ADR-002 variant               PROC-001 (vendor policy)     ← procurement angle
```

---

## Scope

- Use `DB2VS.max_marginal_relevance_search(query, k=5, fetch_k=20, lambda_mult=0.5)`
- Run same query with `similarity_search` vs `max_marginal_relevance_search`
- Print both result sets side by side, highlighting the diversity difference
- Allow `lambda_mult` to be passed as CLI argument to show the diversity/relevance tradeoff

---

## How to try it (once code is written)

```bash
source .venv/bin/activate
cd 08_mmr_retrieval
python main.py
```

Broad questions that benefit from MMR:
- `"What are the main considerations for modernising our application platform?"`
- `"What enterprise knowledge do I need before onboarding a new vendor?"`

---

## How to test it

```bash
python main.py --query "payment platform modernisation" --compare
# Shows: similarity top-5 vs MMR top-5
# Expected: MMR results cover more diverse document types

python main.py --query "payment platform modernisation" --lambda 0.1
# Expected: very diverse results (low similarity bias)

python main.py --query "payment platform modernisation" --lambda 0.9
# Expected: near-duplicate similar results (high similarity bias)
```

**SQL validation** (`validation.sql`):
```sql
-- Inspect document type distribution (should be diverse for MMR to show value)
SELECT DOCUMENT_TYPE, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY DOCUMENT_TYPE
ORDER BY COUNT DESC;
```

---

## Files (to be created)

```
08_mmr_retrieval/
├── README.md
├── main.py         ← side-by-side comparison: similarity vs MMR
├── validation.sql
└── eval.py         ← diversity metric: unique doc types in top-k
```

---

## Enterprise impact

Demonstrates diversity-aware retrieval for broad enterprise questions. When a decision-maker asks "what do we need to consider?", they need multiple perspectives — not five variations of the same perspective. MMR makes Db2 vector search qualitatively better for strategic queries.
