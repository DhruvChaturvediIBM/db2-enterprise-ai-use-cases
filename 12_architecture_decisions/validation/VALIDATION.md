# UC12 Validation Guide

## Purpose

This guide explains how to validate the Architecture Decision Assistant data in IBM Db2 before running semantic searches.

The SQL file is:

```text
validation/validation.sql
```

Run it with the Db2 client or your normal Db2 SQL execution workflow.

## 1. Confirm ADR population

```sql
SELECT COUNT(*) AS TOTAL_ADRS
FROM AI_DEMO.ARCHITECTURE_DECISIONS;
```

Expected:

- The count should be greater than zero.
- The count should match the ADR corpus loaded for the demonstration.

## 2. Review ADR lifecycle state

```sql
SELECT DOCUMENT_ID,
       TITLE,
       STATUS,
       EFFECTIVE_DATE
FROM AI_DEMO.ARCHITECTURE_DECISIONS
ORDER BY DOCUMENT_ID;
```

Review that the records contain meaningful lifecycle states such as:

```text
PROPOSED
ACCEPTED
ACTIVE
SUPERSEDED
DEPRECATED
```

## 3. Review status distribution

```sql
SELECT STATUS,
       COUNT(*) AS COUNT
FROM AI_DEMO.ARCHITECTURE_DECISIONS
GROUP BY STATUS;
```

This confirms that the corpus contains lifecycle information needed for current versus historical searches.

## 4. Verify embeddings

```sql
SELECT DOCUMENT_ID,
       LENGTH(EMBEDDING) AS EMBEDDING_BYTES
FROM AI_DEMO.ARCHITECTURE_DECISIONS
WHERE EMBEDDING IS NOT NULL
ORDER BY DOCUMENT_ID;
```

Expected:

- ADRs intended for semantic search should have non-null embeddings.
- The embedding payload should have a non-zero length.

## 5. Verify current search candidates

```sql
SELECT DOCUMENT_ID,
       TITLE
FROM AI_DEMO.ARCHITECTURE_DECISIONS
WHERE STATUS IN ('ACTIVE', 'ACCEPTED')
ORDER BY DOCUMENT_ID;
```

These are the records appropriate for a current-decision search.

Superseded and deprecated ADRs remain useful for historical questions and should not be deleted solely because they are no longer current.

## Application validation

After SQL validation succeeds:

```bash
python main.py
```

Then try:

```bash
python main.py --query "authentication mechanism for services"
```

and:

```bash
python main.py --query "vector store selection"
```

Finally:

```bash
python -m evaluation.eval
```

## Important runtime note

The Python project can be syntax-checked without Db2, but semantic retrieval requires:

- a reachable IBM Db2 instance
- the configured `AI_DEMO.ARCHITECTURE_DECISIONS` table
- populated embeddings
- the configured embedding model
- installed Python dependencies

The evaluation metrics are meaningful only when the live vector store is available.
