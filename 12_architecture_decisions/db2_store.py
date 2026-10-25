import ibm_db
import ibm_db_dbi
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_db2 import DB2VS
from langchain_ollama import OllamaEmbeddings

from config import settings


def get_embeddings() -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=settings.embedding_model,
        base_url=settings.ollama_base_url,
    )


def get_db2_client() -> ibm_db_dbi.Connection:
    dsn = (
        f"DATABASE={settings.db2_database};"
        f"HOSTNAME={settings.db2_host};"
        f"PORT={settings.db2_port};"
        "PROTOCOL=TCPIP;"
        f"UID={settings.db2_username};"
        f"PWD={settings.db2_password};"
    )
    raw = ibm_db.connect(dsn, "", "")
    return ibm_db_dbi.Connection(raw)


def get_vector_store() -> DB2VS:
    return DB2VS(
        embedding_function=get_embeddings(),
        table_name=f"{settings.db2_schema}.{settings.adr_table}",
        client=get_db2_client(),
        distance_strategy=DistanceStrategy.COSINE,
    )
