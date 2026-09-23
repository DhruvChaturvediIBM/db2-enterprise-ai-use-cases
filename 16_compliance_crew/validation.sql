-- UC16: Enterprise Compliance Investigation Crew — SQL Validation

-- 1. All compliance-relevant knowledge
SELECT DOCUMENT_TYPE, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE IN ('compliance', 'policy', 'incident', 'adr')
GROUP BY DOCUMENT_TYPE;

-- 2. GDPR and compliance documents (primary evidence source)
SELECT DOCUMENT_ID, TITLE, REGION, CLASSIFICATION
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'compliance'
ORDER BY DOCUMENT_ID;

-- 3. Policies for the Policy Analyst agent
SELECT DOCUMENT_ID, TITLE, DEPARTMENT, STATUS, EFFECTIVE_DATE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'policy'
  AND STATUS = 'ACTIVE'
ORDER BY DEPARTMENT, DOCUMENT_ID;

-- 4. Historical cases (for Evidence Researcher) — incidents as proxy
SELECT DOCUMENT_ID, TITLE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'incident'
ORDER BY EFFECTIVE_DATE DESC;
