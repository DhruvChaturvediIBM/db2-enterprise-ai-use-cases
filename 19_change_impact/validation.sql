-- UC19: Semantic Change Impact Discovery — SQL Validation

-- 1. Cross-type knowledge available for impact discovery
SELECT DOCUMENT_TYPE, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY DOCUMENT_TYPE
ORDER BY DOCUMENT_TYPE;
-- Good impact discovery requires: adr, incident, technical, policy, runbook all present

-- 2. Key documents for authentication change impact test
SELECT DOCUMENT_ID, TITLE, DOCUMENT_TYPE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE IN ('adr', 'incident', 'policy', 'technical')
  AND (LOWER(CONTENT) LIKE '%auth%'
    OR LOWER(CONTENT) LIKE '%certificate%'
    OR LOWER(CONTENT) LIKE '%oauth%'
    OR LOWER(CONTENT) LIKE '%credential%')
ORDER BY DOCUMENT_TYPE, DOCUMENT_ID;
-- Expected: ADR-003, INC-002, POL-004 should all appear

-- 3. Key documents for payment change impact test
SELECT DOCUMENT_ID, TITLE, DOCUMENT_TYPE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE LOWER(CONTENT) LIKE '%payment%'
   OR LOWER(CONTENT) LIKE '%connection pool%'
ORDER BY DOCUMENT_TYPE, DOCUMENT_ID;
-- Expected: INC-001, RUN-001, ADR-002 should appear
