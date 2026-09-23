-- UC08: MMR Diverse Retrieval — SQL Validation

-- 1. Document type distribution (diversity of corpus is key for MMR value)
SELECT DOCUMENT_TYPE, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY DOCUMENT_TYPE
ORDER BY COUNT DESC;
-- For MMR to show value, we need at least 4 different document types

-- 2. Department distribution (confirms cross-domain coverage)
SELECT DEPARTMENT, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY DEPARTMENT
ORDER BY COUNT DESC;

-- 3. Confirm sufficient corpus size for meaningful MMR (fetch_k=20 requires >=20 docs)
SELECT COUNT(*) AS TOTAL
FROM AI_DEMO.KNOWLEDGE_BASE;
-- Expected: >= 20

-- 4. Sample of diverse document titles (manual review that types differ)
SELECT DOCUMENT_ID, DOCUMENT_TYPE, TITLE
FROM AI_DEMO.KNOWLEDGE_BASE
ORDER BY DOCUMENT_TYPE, DOCUMENT_ID
FETCH FIRST 20 ROWS ONLY;
