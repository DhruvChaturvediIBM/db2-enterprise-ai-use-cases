# UC03 — Technical Documentation Semantic Search

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

Developers don't always need a generated answer — they need to find the right document. This use case demonstrates IBM Db2 as a **semantic enterprise search layer**, returning a ranked list of relevant documentation rather than generating text. The result is a developer search tool where queries like "kubernetes memory limits healthcare" return the most relevant technical documents with similarity scores.

**College project framing:** Build a semantic document search engine backed by a database.  
**Enterprise framing:** Replace keyword-based developer portals or Confluence search with vector-powered semantic search that understands meaning, not just exact words.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | Haystack |
| Db2 capability | `Db2DocumentStore`, `Db2EmbeddingRetriever`, `top_k` |
| Output | Ranked document list with title, source, similarity score, snippet |
| LLM | None — this is a pure retrieval example (no generation) |
| Key insight | Db2 as semantic search layer, not only as RAG backend |

### Flow

```
Developer query (e.g. "how to set Kubernetes memory limits")
  │
  ▼
Embed query (Ollama nomic-embed-text)
  │
  ▼
Db2EmbeddingRetriever  →  top_k=10
  │
  ▼
Return ranked documents:
  [1] TECH-003 — Kubernetes Deployment Guide — Healthcare  (score: 0.91)
  [2] TECH-002 — API Gateway Configuration Guide           (score: 0.74)
  ...
```

---

## Scope

- Reuse `AI_DEMO.KNOWLEDGE_BASE` with technical documents
- Pure retrieval — **no LLM generation**
- Return top-k with: document_id, title, source, department, similarity_score, content_snippet (first 200 chars)
- Support filtering by document_type=technical
- Demonstrate top_k parameter: compare k=3, k=5, k=10 results
- Show COSINE vs EUCLIDEAN distance comparison on same query

**Out of scope:** generation, agents, reranking (covered in UC05)

---

## How to try it (once code is written)

```bash
source .venv/bin/activate
cd 03_technical_document_search
python main.py
```

Sample queries:
- `"Kubernetes pod memory OOM crash"`
- `"IBM Db2 vector column creation"`
- `"API rate limiting configuration"`

---

## How to test it

```bash
python main.py --query "kubernetes memory OOM" --top_k 5
# Expected: TECH-003 appears in top 2 results
```

**SQL validation** (`validation.sql`):
```sql
-- Count technical documents in the store
SELECT COUNT(*)
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'technical';

-- Inspect technical document metadata
SELECT DOCUMENT_ID, TITLE, DEPARTMENT, PRODUCT, STATUS
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'technical'
ORDER BY CREATED_AT DESC;
```

---

## Files (to be created)

```
03_technical_document_search/
├── README.md
├── main.py         ← semantic search entry point, prints ranked results
├── search.py       ← search function with score formatting
├── validation.sql
└── eval.py
```

---

## Enterprise impact

Demonstrates that IBM Db2 with native VECTOR is a complete semantic enterprise search engine — not just a RAG backend. Teams can build internal developer portals, knowledge search, or documentation discovery on top of Db2 without adding a search-specific system.
