# UC11 — SQL Validation Guide

This validation file is specifically for the table managed by the **official `langchain_db2.DB2VS` integration**.

It does not assume the schema used by a separate Langflow component.

## 1. Confirm the table exists

```sql
SELECT TABSCHEMA, TABNAME, TYPE
FROM SYSCAT.TABLES
WHERE TABSCHEMA = UPPER('AI_DEMO')
  AND TABNAME = UPPER('INCIDENTS');
```

Expected: one table entry for `AI_DEMO.INCIDENTS`.

## 2. Confirm rows exist

```sql
SELECT COUNT(*) AS TOTAL_INCIDENTS
FROM AI_DEMO.INCIDENTS;
```

After the supplied sample data is ingested, the count should be at least 5.

## 3. Inspect the DB2VS-generated columns

```sql
SELECT COLNO, COLNAME, TYPENAME, LENGTH, SCALE, NULLS
FROM SYSCAT.COLUMNS
WHERE TABSCHEMA = UPPER('AI_DEMO')
  AND TABNAME = UPPER('INCIDENTS')
ORDER BY COLNO;
```

This is intentionally important: the example uses the real `DB2VS` storage implementation, so validation should inspect the table produced by that implementation rather than inventing a separate application schema.

## 4. Confirm a vector column exists

```sql
SELECT COLNAME, TYPENAME, LENGTH
FROM SYSCAT.COLUMNS
WHERE TABSCHEMA = UPPER('AI_DEMO')
  AND TABNAME = UPPER('INCIDENTS')
  AND UPPER(TYPENAME) = 'VECTOR';
```

Expected: at least one row.

The exact vector column name and dimensionality are discovered from the Db2 catalog.

## 5. Inspect table statistics

```sql
SELECT TABSCHEMA, TABNAME, CARD
FROM SYSCAT.TABLES
WHERE TABSCHEMA = UPPER('AI_DEMO')
  AND TABNAME = UPPER('INCIDENTS');
```

This provides a Db2 catalog view of the table cardinality.

## 6. Check current schema

```sql
VALUES CURRENT SCHEMA;
```

This is useful when troubleshooting unqualified table names or connection configuration.

## What this SQL does not do

It does not reproduce the vector-search operation in SQL.

The semantic search is intentionally executed through:

```python
from langchain_db2 import DB2VS

vector_store.similarity_search_with_score(...)
```

The SQL script validates the database-side state; the Python application validates the LangChain integration path.

## Expected validation checklist

```text
[ ] AI_DEMO.INCIDENTS exists
[ ] Incident rows exist
[ ] DB2VS-generated columns are present
[ ] A VECTOR column exists
[ ] Table statistics are populated
[ ] Python semantic search returns incidents
```
