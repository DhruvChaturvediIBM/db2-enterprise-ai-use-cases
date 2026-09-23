# UC05 — Retrieval + Reranking for High-Precision Knowledge Search

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

Vector similarity scores are a good first ranking — but not always the best final ranking. A cross-encoder reranker can evaluate each (query, document) pair more precisely than a single embedding comparison. This use case shows a two-stage retrieval architecture: Db2 provides a broad candidate set, then a Haystack reranker selects the most useful passages.

**College project framing:** Implement a two-stage retrieval pipeline (approximate → precise).  
**Enterprise framing:** Improve the answer quality of a knowledge assistant without changing the underlying Db2 storage layer — the reranking happens at the application level after Db2 retrieves candidates.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | Haystack |
| Db2 capability | Vector retrieval, broad candidate set (top_k=15) |
| Reranker | Haystack `SentenceTransformersSimilarityRanker` (local model) |
| LLM | Ollama `granite3.1-dense:8b` |
| Key distinction | Db2 retrieves; Haystack pipeline reranks |

### Flow

```
Question
  │
  ▼
Db2EmbeddingRetriever  →  top-15 candidates (broad net)
  │
  ▼
SentenceTransformersSimilarityRanker  →  top-5 (precise)
  │
  ▼
Prompt + Granite LLM  →  answer from highest-quality context
```

---

## Scope

- Set `Db2EmbeddingRetriever(top_k=15)` — wider candidate set than UC01
- Add `SentenceTransformersSimilarityRanker` as next Haystack pipeline component
- Final context: top-5 after reranking
- **Show comparison:** same query, top-5 from Db2 alone vs top-5 after reranking
- Document which reranker model is used: `cross-encoder/ms-marco-MiniLM-L-6-v2` (small, fast)

**Note:** This uses `sentence-transformers` for the reranker, not Ollama. The reranker is a cross-encoder that requires both query and document as input — it cannot be replaced by a simple embedding call.

---

## How to try it (once code is written)

```bash
source .venv/bin/activate
cd 05_reranked_search
python main.py
```

Sample queries:
- `"What is the process for resetting two-factor authentication?"`
- `"Kubernetes OOM issue in healthcare pods"`

---

## How to test it

```bash
python main.py --query "2FA reset process" --compare
# Prints: Db2-only top-5 ranking
# Prints: Reranked top-5 ranking
# Difference shows reranker benefit
```

**SQL validation** (`validation.sql`):
```sql
-- Same as UC01 — documents are already in Db2
-- This example validates retrieval only; reranking happens in Python

SELECT DOCUMENT_ID, TITLE, DOCUMENT_TYPE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE IN ('support', 'technical', 'runbook')
ORDER BY TITLE;
```

---

## Files (to be created)

```
05_reranked_search/
├── README.md
├── main.py           ← runs pipeline with/without reranking for comparison
├── pipeline.py       ← Haystack pipeline: retriever → reranker → prompt → LLM
├── validation.sql
└── eval.py
```

---

## Enterprise impact

Demonstrates a practical retrieval-quality architecture where the database tier (Db2) and the application tier (Haystack) each do what they are best at. No Db2 changes are required to improve answer quality — the reranking is transparent to the storage layer.
