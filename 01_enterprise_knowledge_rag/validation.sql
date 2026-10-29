-- UC01: Enterprise Knowledge Assistant — SQL Validation
-- Table is created by the official ibm-db-haystack IBMDb2DocumentStore:
--   ID VARCHAR(512) PK | CONTENT CLOB(2M) | META BLOB (BSON) | EMBEDDING VECTOR(768, FLOAT32)
-- Metadata lives in BSON, so read it with SYSTOOLS.BSON2JSON(META).
-- Run in IBM Db2 Developer Extension or any Db2 client.

-- 1. Confirm documents were loaded
-- Expected: 19 (the shared corpus in common/sample_data.py)
SELECT COUNT(*) AS TOTAL_DOCUMENTS
FROM AI_DEMO.HAYSTACK_KNOWLEDGE_BASE;


-- 2. Inspect the first 10 rows with their metadata
SELECT ID,
       JSON_VALUE(SYSTOOLS.BSON2JSON(META), '$.title'         RETURNING VARCHAR(200)) AS TITLE,
       JSON_VALUE(SYSTOOLS.BSON2JSON(META), '$.document_type' RETURNING VARCHAR(50))  AS DOCUMENT_TYPE,
       JSON_VALUE(SYSTOOLS.BSON2JSON(META), '$.department'    RETURNING VARCHAR(100)) AS DEPARTMENT,
       JSON_VALUE(SYSTOOLS.BSON2JSON(META), '$.region'        RETURNING VARCHAR(50))  AS REGION,
       JSON_VALUE(SYSTOOLS.BSON2JSON(META), '$.status'        RETURNING VARCHAR(50))  AS STATUS
FROM AI_DEMO.HAYSTACK_KNOWLEDGE_BASE
ORDER BY ID
FETCH FIRST 10 ROWS ONLY;


-- 3. Confirm the VECTOR column is populated and has the right dimension
-- Expected: DIMENSION = 768 and no NULL embeddings
SELECT ID,
       VECTOR_DIMENSION_COUNT(EMBEDDING) AS DIMENSION
FROM AI_DEMO.HAYSTACK_KNOWLEDGE_BASE
WHERE EMBEDDING IS NOT NULL
ORDER BY ID
FETCH FIRST 5 ROWS ONLY;

SELECT COUNT(*) AS ROWS_WITHOUT_EMBEDDING
FROM AI_DEMO.HAYSTACK_KNOWLEDGE_BASE
WHERE EMBEDDING IS NULL;
-- Expected: 0


-- 4. Count documents by type
SELECT JSON_VALUE(SYSTOOLS.BSON2JSON(META), '$.document_type' RETURNING VARCHAR(50)) AS DOCUMENT_TYPE,
       COUNT(*) AS DOC_COUNT
FROM AI_DEMO.HAYSTACK_KNOWLEDGE_BASE
GROUP BY JSON_VALUE(SYSTOOLS.BSON2JSON(META), '$.document_type' RETURNING VARCHAR(50))
ORDER BY DOC_COUNT DESC;


-- 5. Reproduce the retriever in pure SQL
-- Nearest neighbours of POL-001 (Europe travel policy) by cosine distance.
-- This is the same VECTOR_DISTANCE ... ORDER BY ... FETCH FIRST k pattern that
-- IBMDb2EmbeddingRetriever issues. Lower distance = closer; POL-001 itself is 0.
-- Expected: POL-001 first, then POL-002 (North America travel policy) near the top.
SELECT B.ID,
       VECTOR_DISTANCE(A.EMBEDDING, B.EMBEDDING, COSINE) AS COSINE_DISTANCE
FROM AI_DEMO.HAYSTACK_KNOWLEDGE_BASE A,
     AI_DEMO.HAYSTACK_KNOWLEDGE_BASE B
WHERE A.ID = 'POL-001'
ORDER BY COSINE_DISTANCE ASC
FETCH FIRST 5 ROWS ONLY;
