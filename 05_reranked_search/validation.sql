-- UC05: Retrieval + Reranking — SQL Validation
-- Reranking happens in Python (Haystack). SQL validates the Db2 retrieval layer.

-- 1. Confirm documents available for retrieval (support + technical + runbooks)
SELECT DOCUMENT_TYPE, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE IN ('support', 'technical', 'runbook', 'incident')
GROUP BY DOCUMENT_TYPE;

-- 2. List support + technical documents (primary reranking candidates)
SELECT DOCUMENT_ID, TITLE, DOCUMENT_TYPE
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE IN ('support', 'technical', 'runbook')
ORDER BY DOCUMENT_TYPE, TITLE;

-- 3. Verify all have embeddings (required for initial Db2 retrieval)
SELECT COUNT(*) AS DOCS_WITHOUT_EMBEDDING
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE EMBEDDING IS NULL;
-- Expected: 0
