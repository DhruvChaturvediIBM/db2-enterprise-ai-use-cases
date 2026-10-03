from langchain_db2 import DB2VS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

HOST = "khushityagi463-5zh1k-x86.dev.fyre.ibm.com"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = DB2VS(
    embedding_function=embeddings,
    table_name="KHUSHIID.DB2VS_SMOKE_TEST",
    connection_args={
        "database": "AIDEMO",
        "host": HOST,
        "port": "50000",
        "username": "KHUSHIID",
        "password": "Vmlogin@123",
    },
)

documents = [
    Document(
        page_content="Payment service is returning HTTP 503 because the database connection pool is exhausted.",
        metadata={
            "service": "payment",
            "severity": "SEV-1",
        },
    )
]

vector_store.add_documents(documents)

results = vector_store.similarity_search_with_score(
    "Payment API is failing because Db2 connections are exhausted",
    k=1,
)

for document, score in results:
    print("RESULT:")
    print(document.page_content)
    print("SCORE:", score)
    print("METADATA:", document.metadata)
