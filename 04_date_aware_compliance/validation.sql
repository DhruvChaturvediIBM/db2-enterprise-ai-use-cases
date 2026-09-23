-- UC04: Date-Aware Compliance Knowledge Search — SQL Validation

-- 1. Active vs archived document distribution
SELECT STATUS, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY STATUS;

-- 2. Currently effective compliance documents (safe to surface)
SELECT DOCUMENT_ID, TITLE, EFFECTIVE_DATE, STATUS, CLASSIFICATION
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'compliance'
  AND STATUS = 'ACTIVE'
  AND EFFECTIVE_DATE <= CURRENT DATE
ORDER BY EFFECTIVE_DATE DESC;

-- 3. Policies that would be excluded by date filter (future or archived)
SELECT DOCUMENT_ID, TITLE, EFFECTIVE_DATE, STATUS
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE (STATUS = 'ARCHIVED' OR EFFECTIVE_DATE > CURRENT DATE)
  AND DOCUMENT_TYPE IN ('policy', 'compliance')
ORDER BY EFFECTIVE_DATE DESC;

-- 4. Compliance documents by region (for regional filtering)
SELECT REGION, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE IN ('compliance', 'policy')
  AND STATUS = 'ACTIVE'
GROUP BY REGION
ORDER BY COUNT DESC;
