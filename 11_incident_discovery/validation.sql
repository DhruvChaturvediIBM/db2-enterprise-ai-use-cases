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

-- ─────────────────────────────────────────────────────────────────────────────
-- Filter validation for discovery.py
--
-- discovery.py passes metadata filters in the form:
--   {"service": ["payment"], "severity": ["SEV-1"]}
--
-- The queries below verify that:
--   a) the metadata JSON column stores the expected keys and values, and
--   b) the DB2VS integration correctly restricts results to the requested filter.
--
-- Run these after ingestion (ingest.py) to confirm filter correctness before
-- running eval.py.
-- ─────────────────────────────────────────────────────────────────────────────

-- 7. Confirm that at least one row per distinct service value was ingested.
--    If this returns empty the metadata column name or JSON path is wrong.
SELECT JSON_VALUE(METADATA, '$.service') AS SERVICE,
       COUNT(*)                          AS ROW_COUNT
FROM AI_DEMO.INCIDENTS
GROUP BY JSON_VALUE(METADATA, '$.service')
ORDER BY SERVICE;

-- 8. Confirm that at least one row per distinct severity value was ingested.
SELECT JSON_VALUE(METADATA, '$.severity') AS SEVERITY,
       COUNT(*)                            AS ROW_COUNT
FROM AI_DEMO.INCIDENTS
GROUP BY JSON_VALUE(METADATA, '$.severity')
ORDER BY SEVERITY;

-- 9. Spot-check: retrieve rows for a specific service filter.
--    Expected: only rows where service = 'payment' are returned.
SELECT JSON_VALUE(METADATA, '$.incident_id') AS INCIDENT_ID,
       JSON_VALUE(METADATA, '$.service')      AS SERVICE,
       JSON_VALUE(METADATA, '$.severity')     AS SEVERITY
FROM AI_DEMO.INCIDENTS
WHERE JSON_VALUE(METADATA, '$.service') = 'payment';

-- 10. Spot-check: retrieve rows for a specific severity filter.
--     Expected: only rows where severity = 'SEV-1' are returned.
SELECT JSON_VALUE(METADATA, '$.incident_id') AS INCIDENT_ID,
       JSON_VALUE(METADATA, '$.service')      AS SERVICE,
       JSON_VALUE(METADATA, '$.severity')     AS SEVERITY
FROM AI_DEMO.INCIDENTS
WHERE JSON_VALUE(METADATA, '$.severity') = 'SEV-1';

-- 11. Combined filter — service AND severity.
SELECT JSON_VALUE(METADATA, '$.incident_id') AS INCIDENT_ID,
       JSON_VALUE(METADATA, '$.service')      AS SERVICE,
       JSON_VALUE(METADATA, '$.severity')     AS SEVERITY
FROM AI_DEMO.INCIDENTS
WHERE JSON_VALUE(METADATA, '$.service')  = 'payment'
  AND JSON_VALUE(METADATA, '$.severity') = 'SEV-1';

