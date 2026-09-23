-- UC06: Local Ollama Reranking — SQL Validation

-- 1. Documents available to local reranking pipeline
SELECT DOCUMENT_TYPE, COUNT(*) AS COUNT
FROM AI_DEMO.KNOWLEDGE_BASE
GROUP BY DOCUMENT_TYPE
ORDER BY COUNT DESC;

-- 2. Runbooks and incidents (primary test documents for this UC)
SELECT DOCUMENT_ID, TITLE, DOCUMENT_TYPE, CLASSIFICATION
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE IN ('runbook', 'incident', 'support')
ORDER BY DOCUMENT_TYPE, DOCUMENT_ID;

-- 3. Verify embeddings exist (Db2 retrieval prerequisite)
SELECT COUNT(*) AS TOTAL,
       COUNT(CASE WHEN EMBEDDING IS NOT NULL THEN 1 END) AS WITH_EMBEDDING
FROM AI_DEMO.KNOWLEDGE_BASE;
