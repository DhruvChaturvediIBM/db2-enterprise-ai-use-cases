-- UC13: Single-Agent Enterprise Research Assistant — SQL Validation

-- 1. Knowledge base available to the agent
SELECT DOCUMENT_TYPE, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY DOCUMENT_TYPE
ORDER BY DOCUMENT_TYPE;

-- 2. Confirm sufficient content for meaningful agent research
SELECT COUNT(*) AS TOTAL_DOCS
FROM AI_DEMO.KNOWLEDGE_BASE;
-- Expected: >= 15 documents for meaningful cross-type research

-- 3. Sample of document titles the agent can discover
SELECT DOCUMENT_ID, DOCUMENT_TYPE, TITLE
FROM AI_DEMO.KNOWLEDGE_BASE
ORDER BY DOCUMENT_TYPE, DOCUMENT_ID
FETCH FIRST 20 ROWS ONLY;
