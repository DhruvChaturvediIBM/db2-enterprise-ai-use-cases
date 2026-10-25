# UC07 Validation Guide

Run `validation.sql` in IBM Db2 Developer Extension after the knowledge base has been populated.

## 1. Total document count

```sql
SELECT COUNT(*) AS TOTAL_DOCS
FROM AI_DEMO.KNOWLEDGE_BASE;
```

This confirms that the vector store contains documents.

The result should be consistent with the knowledge-base corpus used by the earlier ingestion use case.

## 2. Embedding storage

The second query returns sample documents and the byte length of their stored embeddings.

A populated, non-zero value confirms that vector data exists for the sample rows.

The exact byte count depends on the embedding dimension and Db2 VECTOR representation.

## 3. Travel-policy documents

The third query identifies policy documents containing the word `travel`.

The source validation expected `POL-001` and `POL-002` for the supplied corpus. If the current corpus differs, treat the query as an inspection query rather than assuming those identifiers exist. fileciteturn0file1L13-L18

## 4. NULL embedding check

The fourth query verifies that no stored document has a NULL embedding.

Expected result:

```text
NULL_EMBEDDINGS = 0
```

A non-zero result indicates that similarity search may fail or behave unexpectedly for those rows.

## 5. Sample document check

The final query checks the travel-policy document identifiers used by the original validation.

This is useful when this use case is executed against the same corpus as the earlier examples.

## Important score note

These SQL statements validate the stored data. They do not validate whether a particular query should receive a HIGH, MEDIUM, or LOW routing decision.

Routing is based on the actual value returned by:

```python
DB2VS.similarity_search_with_score()
```

For cosine distance, smaller values indicate closer matches. Threshold calibration therefore belongs to the application/evaluation layer rather than this static SQL validation.
