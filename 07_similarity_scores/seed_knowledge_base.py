"""
seed_knowledge_base.py
──────────────────────
One-shot script: create AI_DEMO.KNOWLEDGE_BASE and populate it with the
shared enterprise corpus from common/sample_data.py.

Run this once before main.py.  Safe to re-run — it skips rows that
already exist (DB2VS inserts are idempotent via SHA-256 primary key).

Usage
-----
    cd 07_similarity_scores/07_similarity_scores
    python seed_knowledge_base.py
"""

from __future__ import annotations

import sys
import os

# Allow imports from the repo root common/ package when running from this dir.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import ibm_db
import ibm_db_dbi
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from langchain_db2 import DB2VS
from dotenv import load_dotenv
from common.sample_data import ALL_DOCUMENTS, EnterpriseDocument

load_dotenv()


# ── Connection ────────────────────────────────────────────────────────────────

def _connect() -> ibm_db_dbi.Connection:
    dsn = (
        f"DATABASE={os.environ['DB2_DATABASE']};"
        f"HOSTNAME={os.environ['DB2_HOST']};"
        f"PORT={os.environ['DB2_PORT']};"
        "PROTOCOL=TCPIP;"
        f"UID={os.environ['DB2_USERNAME']};"
        f"PWD={os.environ['DB2_PASSWORD']};"
    )
    if os.getenv("DB2_SECURITY", "false").lower() == "true":
        dsn += "SECURITY=SSL;"
    raw = ibm_db.connect(dsn, "", "")
    return ibm_db_dbi.Connection(raw)


# ── Seed ─────────────────────────────────────────────────────────────────────

def seed() -> None:
    table = os.getenv("DB2_TABLE", "AI_DEMO.KNOWLEDGE_BASE")
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    embed_model = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")

    print(f"Connecting to Db2 ...")
    conn = _connect()
    print("  ✓ Connected")

    embeddings = OllamaEmbeddings(model=embed_model, base_url=ollama_url)

    print(f"Initialising DB2VS on {table} ...")
    store = DB2VS(
        embedding_function=embeddings,
        table_name=table,
        client=conn,
        distance_strategy=DistanceStrategy.COSINE,
    )
    print("  ✓ Table ready")

    docs: list[Document] = []
    metadatas: list[dict] = []

    for doc in ALL_DOCUMENTS:
        docs.append(Document(page_content=doc.content))
        metadatas.append({
            "id":            doc.document_id,
            "document_id":   doc.document_id,
            "title":         doc.title,
            "document_type": doc.document_type,
            "department":    doc.department,
            "region":        doc.region,
            "status":        doc.status,
            "tags":          ",".join(doc.tags),
        })

    print(f"Embedding and inserting {len(docs)} documents ...")
    texts = [d.page_content for d in docs]
    store.add_texts(texts=texts, metadatas=metadatas)
    print(f"  ✓ {len(docs)} documents seeded into {table}")
    print("\nDone. You can now run:  python main.py --query \"<your question>\"")


if __name__ == "__main__":
    seed()
