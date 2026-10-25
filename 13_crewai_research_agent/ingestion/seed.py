"""
seed.py — UC13 knowledge base seeder.

Creates AI_DEMO.RESEARCH_KNOWLEDGE with a plain VARCHAR document_id
column so DB2VectorSearchTool can return it directly without having
to decode the metadata BLOB.

Schema:
    id           CHAR(16)        — SHA-256 primary key (DB2VS standard)
    text         CLOB            — document content
    metadata     BLOB            — full metadata JSON (DB2VS standard)
    embedding    VECTOR(768)     — nomic-embed-text vector
    document_id  VARCHAR(32)     — plain document ID for easy retrieval
    title        VARCHAR(256)    — plain title for easy retrieval

Run once before main.py:
    cd 13_crewai_research_agent/13_crewai_research_agent
    python -m ingestion.seed
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

import ibm_db
import ibm_db_dbi
import ollama
from dotenv import load_dotenv

from common.sample_data import ALL_DOCUMENTS

load_dotenv()

TABLE = os.getenv("KNOWLEDGE_TABLE", "RESEARCH_KNOWLEDGE")
SCHEMA = os.getenv("DB2_SCHEMA", "AI_DEMO")
FULL_TABLE = f"{SCHEMA}.{TABLE}"
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "768"))


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


def _table_exists(conn: ibm_db_dbi.Connection) -> bool:
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT COUNT(*) FROM {FULL_TABLE}")
        return True
    except Exception as e:
        if "SQL0204N" in str(e):
            return False
        raise
    finally:
        cur.close()


def _create_table(conn: ibm_db_dbi.Connection) -> None:
    ddl = f"""
        CREATE TABLE {FULL_TABLE} (
            id          CHAR(16)        NOT NULL PRIMARY KEY,
            text        CLOB,
            metadata    BLOB,
            embedding   VECTOR({EMBEDDING_DIM}, FLOAT32),
            document_id VARCHAR(32),
            title       VARCHAR(256)
        )
    """
    cur = conn.cursor()
    try:
        cur.execute(ddl)
        cur.execute("COMMIT")
        print(f"  ✓ Table {FULL_TABLE} created")
    finally:
        cur.close()


def _embed(text: str) -> list[float]:
    client = ollama.Client(host=OLLAMA_BASE_URL)
    resp = client.embeddings(model=EMBEDDING_MODEL, prompt=text)
    return resp["embedding"]


def _make_id(document_id: str) -> str:
    return hashlib.sha256(document_id.encode()).hexdigest()[:16].upper()


def _insert_documents(conn: ibm_db_dbi.Connection) -> int:
    sql = f"""
        INSERT INTO {FULL_TABLE}
            (id, text, metadata, embedding, document_id, title)
        VALUES
            (?, ?, SYSTOOLS.JSON2BSON(?),
             VECTOR(cast(? as CLOB(100000)), {EMBEDDING_DIM}, FLOAT32),
             ?, ?)
    """
    cur = conn.cursor()
    count = 0
    try:
        for doc in ALL_DOCUMENTS:
            row_id = _make_id(doc.document_id)
            meta = json.dumps({
                "document_id":   doc.document_id,
                "title":         doc.title,
                "document_type": doc.document_type,
                "department":    doc.department,
                "region":        doc.region,
                "status":        doc.status,
            })
            vec = str(_embed(doc.content))
            cur.execute(sql, (
                row_id,
                doc.content,
                meta,
                vec,
                doc.document_id,
                doc.title,
            ))
            count += 1
            print(f"  {doc.document_id} — {doc.title[:50]}")
        cur.execute("COMMIT")
    finally:
        cur.close()
    return count


def seed() -> None:
    print(f"Connecting to Db2 ...")
    conn = _connect()
    print("  ✓ Connected")

    if _table_exists(conn):
        print(f"  Table {FULL_TABLE} already exists — skipping DDL")
    else:
        _create_table(conn)

    print(f"\nEmbedding and inserting {len(ALL_DOCUMENTS)} documents ...")
    count = _insert_documents(conn)
    print(f"\n  ✓ {count} documents seeded into {FULL_TABLE}")
    print(f"\nDone. Run:  python main.py --query \"<your question>\"")


if __name__ == "__main__":
    seed()
