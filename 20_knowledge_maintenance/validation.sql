-- UC20: Enterprise Knowledge Maintenance Assistant — SQL Validation

-- 1. Knowledge base health overview
SELECT COUNT(*) AS TOTAL,
       STATUS,
       COUNT(CASE WHEN UPDATED_AT < (CURRENT DATE - 365 DAYS) THEN 1 END) AS NOT_UPDATED_IN_1_YEAR
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY STATUS;

-- 2. Oldest documents (stale detection candidates)
SELECT DOCUMENT_ID, TITLE, DOCUMENT_TYPE, EFFECTIVE_DATE, UPDATED_AT, STATUS
FROM AI_DEMO.KNOWLEDGE_BASE
ORDER BY EFFECTIVE_DATE ASC
FETCH FIRST 10 ROWS ONLY;

-- 3. Check for obvious title duplicates (baseline before semantic duplicate search)
SELECT TITLE, COUNT(*) AS TITLE_COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY TITLE
HAVING COUNT(*) > 1;

-- 4. After running audit and deletions — confirm state
SELECT COUNT(*) AS REMAINING_DOCS, STATUS
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY STATUS;

-- 5. Verify a specific deletion was applied (replace DOCUMENT_ID with actual)
-- SELECT COUNT(*) FROM AI_DEMO.KNOWLEDGE_BASE WHERE DOCUMENT_ID = 'TEST-DUPLICATE-001';
-- Expected: 0

-- 6. Test clear_table safety check — count before any clear operation
SELECT COUNT(*) AS COUNT_BEFORE_CLEAR
FROM AI_DEMO.KNOWLEDGE_BASE;
-- Manually confirm this number before running any clear_table() call
