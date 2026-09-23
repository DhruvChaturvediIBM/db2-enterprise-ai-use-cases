-- UC10: Semantic Recommendation Engine — SQL Validation

-- 1. Confirm all document IDs available for recommendation input
SELECT DOCUMENT_ID, DOCUMENT_TYPE, TITLE
FROM AI_DEMO.KNOWLEDGE_BASE
ORDER BY DOCUMENT_TYPE, DOCUMENT_ID;

-- 2. Verify incidents are in the corpus (key for incident→incident recommendations)
SELECT DOCUMENT_ID, TITLE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'incident'
ORDER BY DOCUMENT_ID;
-- Expected: INC-001, INC-002, INC-003

-- 3. Verify ADRs are in the corpus (key for ADR→ADR recommendations)
SELECT DOCUMENT_ID, TITLE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'adr'
ORDER BY DOCUMENT_ID;
-- Expected: ADR-001, ADR-002, ADR-003

-- 4. Count per type for recommendation diversity check
SELECT DOCUMENT_TYPE, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY DOCUMENT_TYPE
ORDER BY DOCUMENT_TYPE;
