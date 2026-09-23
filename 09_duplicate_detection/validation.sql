-- UC09: Semantic Duplicate Detection — SQL Validation

-- 1. Confirm policy documents are loaded (primary duplicate detection target)
SELECT DOCUMENT_ID, TITLE, DOCUMENT_TYPE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'policy'
ORDER BY DOCUMENT_ID;

-- 2. Check for obvious title duplicates (manual baseline for comparison)
SELECT TITLE, COUNT(*) AS TITLE_COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY TITLE
HAVING COUNT(*) > 1;
-- Expected: 0 unless test duplicates were seeded

-- 3. After seeding a test duplicate — confirm it was added
-- (Run this after main.py --seed-duplicate)
SELECT DOCUMENT_ID, TITLE, DOCUMENT_TYPE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE TITLE LIKE '%TEST_DUPLICATE%'
   OR DOCUMENT_ID LIKE '%TEST%';

-- 4. After deletion — confirm duplicate was removed
-- (Run after interactive approval)
SELECT COUNT(*) AS REMAINING_DOCS
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE TITLE LIKE '%TEST_DUPLICATE%';
-- Expected: 0
