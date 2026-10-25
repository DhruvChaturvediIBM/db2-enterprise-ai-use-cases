# UC13 Validation Guide

## Purpose

Validate that the shared Db2 knowledge base contains enough cross-type enterprise content for the single-agent research demonstration.

## 1. Document-type coverage

Run:

```sql
SELECT DOCUMENT_TYPE, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY DOCUMENT_TYPE
ORDER BY DOCUMENT_TYPE;
```

Review whether the knowledge base contains multiple useful enterprise document categories.

## 2. Document count

Run:

```sql
SELECT COUNT(*) AS TOTAL_DOCS
FROM AI_DEMO.KNOWLEDGE_BASE;
```

The supplied validation expects at least 15 documents for meaningful cross-type research.

## 3. Inspect available evidence

Run:

```sql
SELECT DOCUMENT_ID, DOCUMENT_TYPE, TITLE
FROM AI_DEMO.KNOWLEDGE_BASE
ORDER BY DOCUMENT_TYPE, DOCUMENT_ID
FETCH FIRST 20 ROWS ONLY;
```

Confirm that the agent has architecture, operational, incident, policy, or technical documents it can discover.

## 4. Run the agent

```bash
python main.py --query \
"What are our authentication architecture decisions and how do they relate to recent incidents?"
```

Review:

- whether `DB2VectorSearchTool` was invoked
- search queries selected by the agent
- retrieved document evidence
- whether multiple searches were necessary
- final answer grounding

## 5. Important interpretation

The SQL checks validate data availability, not agent quality.

A successful SQL check does not guarantee a particular retrieval ranking. Retrieval depends on:

- stored embeddings
- query embedding model
- vector dimension
- distance metric
- retrieval limit
- document content

The final answer should remain grounded in the returned Db2 evidence.
