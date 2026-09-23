# UC06 — Local Ollama Reranking for Sensitive Enterprise Data

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

Some enterprise environments cannot send retrieved document content to external APIs for any purpose — including reranking. This use case shows how to use a locally-running Ollama Granite model as the reranking intelligence, keeping all document content on local infrastructure while still improving retrieval quality.

**College project framing:** Implement a fully local (offline-capable) RAG pipeline with local reranking.  
**Enterprise framing:** A data-sovereign retrieval system where documents never leave the enterprise perimeter — Db2 stores them, Ollama ranks them, Granite answers the question.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | Haystack + local Ollama |
| Db2 capability | Vector retrieval (candidate set) |
| Reranker | Ollama `granite3.1-dense:8b` as a local scoring model |
| LLM | Ollama `granite3.1-dense:8b` (same model, dual use) |
| Key difference from UC05 | Cross-encoder reranker → local LLM-based relevance scoring |

### Flow

```
Question
  │
  ▼
Db2  →  top-15 candidates
  │
  ▼
Ollama Granite (local) scores each candidate:
  "On a scale 1-10, how relevant is this document to the question?"
  │
  ▼
Sorted by Granite relevance score  →  top-5
  │
  ▼
Prompt + Granite  →  answer
```

---

## Scope

- Retrieve top-15 from Db2
- For each candidate, call Ollama Granite with a scoring prompt:
  `"Rate the relevance of this document to the question on a scale of 1-10. Return only the integer."`
- Sort candidates by score, keep top-5
- Feed top-5 to generation prompt
- Show scored candidate list in output

**Ollama dependency note:** This example REQUIRES Ollama running locally (`ollama serve`). The `install.sh` pulls the model. If Ollama is unavailable, the example falls back to UC05 cross-encoder reranking with a clear warning.

---

## How to try it (once code is written)

```bash
# Ensure Ollama is running
ollama serve &

source .venv/bin/activate
cd 06_ollama_local_reranking
python main.py
```

Sample queries:
- `"What are the Kubernetes resource limits for healthcare services?"`
- `"What is the process for recovering from a P1 payment service outage?"`

---

## How to test it

```bash
python main.py --query "payment service P1 recovery"
# Expected output:
#   Candidate 1: RUN-001 (runbook) — Granite score: 9
#   Candidate 2: INC-001 (incident) — Granite score: 7
#   ...
#   Answer: grounded in runbook content
```

**SQL validation** (`validation.sql`):
```sql
-- Validate documents available for retrieval
SELECT DOCUMENT_ID, TITLE, DOCUMENT_TYPE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE IN ('runbook', 'incident', 'support')
ORDER BY DOCUMENT_TYPE, DOCUMENT_ID;
```

---

## Files (to be created)

```
06_ollama_local_reranking/
├── README.md
├── main.py           ← full local pipeline
├── local_reranker.py ← Ollama-based scoring function
├── validation.sql
└── eval.py
```

---

## Enterprise impact

Demonstrates a fully enterprise-private retrieval-augmented generation pipeline. No data leaves the network perimeter. IBM Db2 stores and retrieves; Ollama Granite scores and answers. This pattern directly addresses data sovereignty requirements in regulated industries.
