-- UC07: Similarity Search with Relevance Scores
-- Run these statements in IBM Db2 Developer Extension.

-- 1. Total documents in the existing knowledge base.
SELECT COUNT(*) AS TOTAL_DOCS
FROM AI_DEMO.KNOWLEDGE_BASE;

-- 2. Sample documents and stored embedding sizes.
SELECT
    DOCUMENT_ID,
    TITLE,
    DOCUMENT_TYPE,
    LENGTH(EMBEDDING) AS EMBEDDING_BYTES
FROM AI_DEMO.KNOWLEDGE_BASE
FETCH FIRST 5 ROWS ONLY;

-- 3. Documents expected to be relevant for travel-policy queries.
SELECT
    DOCUMENT_ID,
    TITLE,
    REGION,
    DEPARTMENT
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE LOWER(DOCUMENT_TYPE) = 'policy'
  AND LOWER(CONTENT) LIKE '%travel%'
ORDER BY DOCUMENT_ID;

-- 4. Confirm that no embeddings are NULL.
SELECT COUNT(*) AS NULL_EMBEDDINGS
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE EMBEDDING IS NULL;

-- 5. Confirm the sample enterprise documents used by the score-routing demo.
SELECT
    DOCUMENT_ID,
    TITLE,
    DOCUMENT_TYPE,
    REGION
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_ID IN (
    'POL-001',
    'POL-002'
)
ORDER BY DOCUMENT_ID;
