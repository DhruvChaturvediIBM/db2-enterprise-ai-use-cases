# UC08 Validation Guide

Run `validation.sql` in IBM Db2 Developer Extension after the knowledge base has been populated.

## 1. Document type distribution

The first query groups documents by `DOCUMENT_TYPE`.

The supplied validation expects at least four different document types to make the MMR demonstration observable.

## 2. Department distribution

The second query groups documents by department and confirms cross-domain coverage.

## 3. Corpus size

The third query returns the total number of documents.

The default configuration uses:

```text
k = 5
fetch_k = 20
```

A corpus of at least 20 documents gives MMR the intended candidate pool.

## 4. Sample diverse documents

The final query displays IDs, types, departments, and titles for manual inspection.

The objective is to confirm that the corpus contains genuinely different enterprise perspectives.

## What the SQL does not validate

The SQL validates prerequisites. It does not determine that MMR is better than similarity search.

The Python application compares:

```python
DB2VS.similarity_search(...)
DB2VS.max_marginal_relevance_search(...)
```

The evaluation script measures the resulting diversity and overlap.

## Expected database state

A healthy UC08 database should contain:

- Multiple document types.
- Multiple departments.
- Enough documents for the configured `fetch_k`.
- Metadata that makes document diversity observable.

Exact counts depend on the corpus.
