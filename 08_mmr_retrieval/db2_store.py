from __future__ import annotations

import ibm_db
import ibm_db_dbi
from langchain_db2 import DB2VS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_ollama import OllamaEmbeddings

from config import Settings

def create_db2_vector_store(settings: Settings) -> DB2VS:
    dsn = (
        f"DATABASE={settings.db2_database};"
        f"HOSTNAME={settings.db2_host};"
        f"PORT={settings.db2_port};"
        "PROTOCOL=TCPIP;"
        f"UID={settings.db2_username};"
        f"PWD={settings.db2_password};"
    )
    if settings.db2_security:
        dsn += "SECURITY=SSL;"

    raw_connection = ibm_db.connect(dsn, "", "")
    connection = ibm_db_dbi.Connection(raw_connection)

    embeddings = OllamaEmbeddings(
        model=settings.embedding_model,
        base_url=settings.ollama_base_url,
    )

    return DB2VS(
        embedding_function=embeddings,
        table_name=settings.db2_table,
        client=connection,
        distance_strategy=DistanceStrategy.COSINE,
    )
