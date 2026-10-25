-- UC09: Semantic Duplicate Detection - SQL Validation

-- 1. Confirm policy documents are loaded (primary duplicate detection target)
SELECT DOCUMENT_ID, TITLE, DOCUMENT_TYPE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'policy'
ORDER BY DOCUMENT_ID;

-- Expected:
-- One or more policy documents should be returned, including the policy used
-- as the primary duplicate-detection target when that seed data is present.


-- 2. Check for obvious title duplicates (manual baseline for comparison)
SELECT TITLE, COUNT(*) AS TITLE_COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY TITLE
HAVING COUNT(*) > 1;

-- Expected:
-- 0 rows unless intentional test duplicates were seeded.


-- 3. After seeding a test duplicate - confirm it was added
-- Run this after the test duplicate has been inserted by an ingestion workflow.
SELECT DOCUMENT_ID, TITLE, DOCUMENT_TYPE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE TITLE LIKE '%TEST_DUPLICATE%'
   OR DOCUMENT_ID LIKE '%TEST%';

-- Expected:
-- The intentionally seeded test document should be visible.


-- 4. After deletion - confirm the test duplicate was removed
-- Run only after an explicit cleanup operation.
SELECT COUNT(*) AS REMAINING_DOCS
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE TITLE LIKE '%TEST_DUPLICATE%';

-- Expected:
-- 0
