from __future__ import annotations

import os

from langchain_db2 import DB2VS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}\n"
            "Copy .env.example to .env and fill in your Db2 credentials."
        )
    return value


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = DB2VS(
    embedding_function=embeddings,
    table_name=f"{_required('DB2_SCHEMA')}.DB2VS_SMOKE_TEST",
    connection_args={
        "database": _required("DB2_DATABASE"),
        "host": _required("DB2_HOST"),
        "port": os.getenv("DB2_PORT", "50000"),
        "username": _required("DB2_USER"),
        "password": _required("DB2_PASSWORD"),
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
