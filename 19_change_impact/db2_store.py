"""IBM Db2 vector-store integration.

This module intentionally uses the public DB2VS integration directly rather than
wrapping or replacing the vector-store implementation.
"""

import ibm_db
import ibm_db_dbi
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_db2 import DB2VS
from langchain_ollama import OllamaEmbeddings

from config import settings


def build_db2_vector_store() -> DB2VS:
    """Create a DB2VS instance over the enterprise knowledge table."""
    embeddings = OllamaEmbeddings(
        model=settings.embedding_model,
        base_url=settings.ollama_base_url,
    )

    dsn = (
        f"DATABASE={settings.db2_database};"
        f"HOSTNAME={settings.db2_host};"
        f"PORT={settings.db2_port};"
        "PROTOCOL=TCPIP;"
        f"UID={settings.db2_username};"
        f"PWD={settings.db2_password};"
    )
    raw = ibm_db.connect(dsn, "", "")
    client = ibm_db_dbi.Connection(raw)

    return DB2VS(
        embedding_function=embeddings,
        table_name=f"{settings.db2_schema}.{settings.knowledge_table}",
        client=client,
        distance_strategy=DistanceStrategy.COSINE,
    )
