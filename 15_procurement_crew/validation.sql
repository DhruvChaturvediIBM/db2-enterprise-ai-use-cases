-- UC15: Procurement / RFP Analysis Crew — SQL Validation

-- 1. Procurement and policy knowledge for agents
SELECT DOCUMENT_TYPE, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE IN ('procurement', 'compliance', 'policy')
GROUP BY DOCUMENT_TYPE;

-- 2. Specific procurement documents
SELECT DOCUMENT_ID, TITLE, DEPARTMENT, STATUS
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'procurement'
ORDER BY DOCUMENT_ID;

-- 3. Compliance rules available to Compliance Analyst agent
SELECT DOCUMENT_ID, TITLE, REGION
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'compliance'
ORDER BY DOCUMENT_ID;

-- 4. Verify all knowledge types agents need are present
SELECT DOCUMENT_TYPE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE IN ('procurement', 'compliance', 'policy')
GROUP BY DOCUMENT_TYPE;
-- Expected: all 3 types present
