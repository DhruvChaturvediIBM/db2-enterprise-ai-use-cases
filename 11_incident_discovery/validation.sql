-- UC11: Db2VS SQL Validation
--
-- DB2VS creates/manages the vector-store table.
-- This validation intentionally inspects the Db2 catalog instead of
-- assuming the internal DB2VS column names beyond the table itself.

-- 1. Confirm the table exists.
SELECT TABSCHEMA,
       TABNAME,
       TYPE
FROM SYSCAT.TABLES
WHERE TABSCHEMA = UPPER('AI_DEMO')
  AND TABNAME = UPPER('INCIDENTS');

-- 2. Confirm the table contains rows.
SELECT COUNT(*) AS TOTAL_INCIDENTS
FROM AI_DEMO.INCIDENTS;

-- 3. Inspect the actual columns created for the DB2VS vector store.
SELECT COLNO,
       COLNAME,
       TYPENAME,
       LENGTH,
       SCALE,
       NULLS
FROM SYSCAT.COLUMNS
WHERE TABSCHEMA = UPPER('AI_DEMO')
  AND TABNAME = UPPER('INCIDENTS')
ORDER BY COLNO;

-- 4. Confirm the table has a vector column.
-- The exact column name is intentionally discovered from the catalog.
SELECT COLNAME,
       TYPENAME,
       LENGTH
FROM SYSCAT.COLUMNS
WHERE TABSCHEMA = UPPER('AI_DEMO')
  AND TABNAME = UPPER('INCIDENTS')
  AND UPPER(TYPENAME) = 'VECTOR';

-- 5. Inspect Db2 table statistics.
SELECT TABSCHEMA,
       TABNAME,
       CARD
FROM SYSCAT.TABLES
WHERE TABSCHEMA = UPPER('AI_DEMO')
  AND TABNAME = UPPER('INCIDENTS');

-- 6. Verify that the table is owned by the expected schema.
VALUES CURRENT SCHEMA;
