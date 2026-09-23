-- UC14: Multi-Agent Incident Investigation Crew — SQL Validation

-- 1. All knowledge types available to the crew's agents
SELECT DOCUMENT_TYPE, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY DOCUMENT_TYPE
ORDER BY DOCUMENT_TYPE;
-- Expected: incidents, runbooks, adr, technical, support, policy all present

-- 2. Historical incidents (Historical Analyst agent scope)
SELECT DOCUMENT_ID, TITLE, EFFECTIVE_DATE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'incident'
ORDER BY EFFECTIVE_DATE DESC;

-- 3. Runbooks (Runbook Analyst agent scope)
SELECT DOCUMENT_ID, TITLE, DEPARTMENT
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'runbook'
ORDER BY DOCUMENT_ID;

-- 4. ADRs (Root Cause Analyst agent scope)
SELECT DOCUMENT_ID, TITLE, STATUS
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'adr'
ORDER BY DOCUMENT_ID;
