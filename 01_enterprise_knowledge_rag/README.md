# UC01 — Enterprise Knowledge Assistant

## Status
> 🔲 Scope defined. Code not yet written. Review this README, suggest changes, then we implement.

---

## Why this use case exists

Employees across large organisations constantly search for answers buried in internal policies, runbooks, technical documents, and FAQs. Keyword search fails because the same concept is expressed differently across documents. This use case shows how IBM Db2 with native VECTOR storage becomes the foundation of a grounded enterprise assistant — without adding a separate vector database.

**College project framing:** Build a Q&A system over a document corpus where answers cite the source documents.  
**Enterprise framing:** Replace SharePoint full-text search with a semantically-grounded assistant that answers from your own Db2-hosted knowledge base.

---

## What it demonstrates

| Capability | Detail |
|---|---|
| Framework | Haystack |
| Db2 capability | `Db2DocumentStore`, `Db2EmbeddingRetriever`, native VECTOR column |
| LLM | Ollama `granite3.1-dense:8b` (local, no API key) |
| Embedding | Ollama `nomic-embed-text` |
| Pattern | RAG (Retrieval-Augmented Generation) |

### Flow

```
Question
  │
  ▼
Embed question (nomic-embed-text via Ollama)
  │
  ▼
Db2EmbeddingRetriever  ←  Db2DocumentStore
  │                         (VECTOR column, cosine distance)
  ▼
Top-5 relevant documents
  │
  ▼
Prompt + LLM (Granite via Ollama)
  │
  ▼
Grounded answer with source citations
```

---

## Scope

- Load shared enterprise corpus from `common/sample_data.py` into Db2
- Embed all documents using `common/embeddings.py` (Ollama nomic-embed-text)
- Store in `AI_DEMO.KNOWLEDGE_BASE` table with VECTOR column
- Build a Haystack RAG pipeline: retriever → prompt → LLM
- Accept a natural-language question and return a grounded answer
- Print top-k retrieved documents with similarity scores
- Run evaluation on 3 sample queries

**Out of scope for UC01:** metadata filtering (that is UC02), reranking (UC05), agents (UC13+)

---

## How to try it (once code is written)

```bash
# From repo root
source .venv/bin/activate
cd 01_enterprise_knowledge_rag
python main.py
```

Sample questions to ask:
- `"What is the travel reimbursement policy for Europe?"`
- `"How do I troubleshoot a slow Db2 query?"`
- `"What is the data retention requirement for customer transactions?"`

---

## How to test it

**Functional test:**
```bash
python main.py --query "What is the travel policy for Europe?"
# Expected: answer mentioning POL-001, €250 hotel cap, €75 meal allowance
```

**SQL validation** (`validation.sql`):
```sql
-- Confirm documents were loaded
SELECT COUNT(*) FROM AI_DEMO.KNOWLEDGE_BASE;

-- Inspect first 5 rows
SELECT DOCUMENT_ID, TITLE, DOCUMENT_TYPE
FROM AI_DEMO.KNOWLEDGE_BASE
FETCH FIRST 5 ROWS ONLY;

-- Confirm vector column exists and is populated
SELECT DOCUMENT_ID, LENGTH(EMBEDDING) AS VECTOR_BYTES
FROM AI_DEMO.KNOWLEDGE_BASE
FETCH FIRST 3 ROWS ONLY;
```

---

## Files (to be created)

```
01_enterprise_knowledge_rag/
├── README.md         ← this file
├── main.py           ← entry point, runs the full pipeline
├── pipeline.py       ← Haystack RAG pipeline definition
├── ingest.py         ← loads sample_data into Db2DocumentStore
├── validation.sql    ← SQL queries to inspect Db2 state
└── eval.py           ← evaluation on 3 sample queries
```

---

## Enterprise impact

Demonstrates the complete path from enterprise knowledge stored in IBM Db2 to a grounded AI assistant, with zero dependency on an external vector database. All data stays inside Db2.
