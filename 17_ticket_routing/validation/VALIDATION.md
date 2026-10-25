# UC17 Validation Guide

## Purpose

Validate the historical ticket corpus and its vector embeddings in IBM Db2 before running semantic routing.

SQL file:

```text
validation/validation.sql
```

## 1. Confirm ticket history

```sql
SELECT COUNT(*) AS TOTAL_TICKETS
FROM AI_DEMO.TICKETS;
```

Expected:

- Count greater than zero.
- Count should match the corpus intended for semantic routing.

## 2. Review routing teams

```sql
SELECT DEPARTMENT AS TEAM,
       COUNT(*) AS TICKET_COUNT
FROM AI_DEMO.TICKETS
GROUP BY DEPARTMENT
ORDER BY TICKET_COUNT DESC;
```

This verifies that historical tickets contain routing targets.

## 3. Review categories

```sql
SELECT DOCUMENT_TYPE AS CATEGORY,
       COUNT(*) AS COUNT
FROM AI_DEMO.TICKETS
GROUP BY DOCUMENT_TYPE
ORDER BY COUNT DESC;
```

This verifies category labels are populated.

## 4. Inspect sample ticket metadata

```sql
SELECT DOCUMENT_ID,
       TITLE,
       DEPARTMENT AS TEAM,
       SUBSTR(CONTENT, 1, 100) AS SYMPTOM_PREVIEW
FROM AI_DEMO.TICKETS
FETCH FIRST 10 ROWS ONLY;
```

Review that the ticket text and routing metadata are meaningful.

## 5. Verify embeddings

```sql
SELECT COUNT(*) AS TICKETS_WITH_EMBEDDING
FROM AI_DEMO.TICKETS
WHERE EMBEDDING IS NOT NULL;
```

For a fully prepared corpus, this should match the number of tickets intended for semantic routing.

## Application validation

After the SQL checks succeed:

```bash
python main.py
```

Try a custom ticket:

```bash
python main.py \
  --ticket "login failure after certificate update"
```

Then run the evaluation:

```bash
python -m evaluation.eval
```

## Runtime requirements

Live semantic routing requires:

- reachable IBM Db2
- populated `AI_DEMO.TICKETS`
- ticket embeddings
- configured embedding model
- installed Python dependencies

The Python source can be syntax-checked without a live Db2 connection, but retrieval and evaluation require the configured runtime services.
