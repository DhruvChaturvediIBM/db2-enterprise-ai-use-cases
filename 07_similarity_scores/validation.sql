-- UC07: Similarity Search with Relevance Scores — SQL Validation

-- 1. Total documents in DB2VS table
SELECT COUNT(*) AS TOTAL_DOCS
FROM AI_DEMO.KNOWLEDGE_BASE;

-- 2. Sample documents with embedding sizes (confirms vectors stored)
SELECT DOCUMENT_ID, TITLE, DOCUMENT_TYPE,
       LENGTH(EMBEDDING) AS EMBEDDING_BYTES
FROM AI_DEMO.KNOWLEDGE_BASE
FETCH FIRST 5 ROWS ONLY;

-- 3. Documents that should score HIGH for travel policy queries
SELECT DOCUMENT_ID, TITLE, REGION, DEPARTMENT
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE DOCUMENT_TYPE = 'policy'
  AND LOWER(CONTENT) LIKE '%travel%'
ORDER BY DOCUMENT_ID;
-- Expected: POL-001 (Europe), POL-002 (North America)

-- 4. Confirm no embeddings are NULL (would break similarity search)
SELECT COUNT(*) AS NULL_EMBEDDINGS
FROM AI_DEMO.KNOWLEDGE_BASE
WHERE EMBEDDING IS NULL;
-- Expected: 0
