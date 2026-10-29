"""
UC01 configuration.

Reuses the repo-wide settings in common/config.py (.env at the repo root) and adds
the one UC01-specific value: the Db2 table used by the Haystack document store.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Make `common/` importable when running `python main.py` from this folder.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from haystack.utils import Secret  # noqa: E402
from haystack_integrations.document_stores.ibm_db import IBMDb2DocumentStore  # noqa: E402

from common.config import (  # noqa: E402
    DB2_DATABASE,
    DB2_HOST,
    DB2_PORT,
    DB2_SSL,
    DB2_SSL_CERT,
    EMBEDDING_DIM,
    EMBEDDING_MODEL,
    OLLAMA_BASE,
    OLLAMA_MODEL,
)

# The Haystack store owns its table layout (id, content, meta, embedding), so it
# must not share a table with the LangChain DB2VS use cases (e.g. UC09).
TABLE_NAME = os.getenv("HAYSTACK_DB2_TABLE", "AI_DEMO.HAYSTACK_KNOWLEDGE_BASE")
SCHEMA_NAME = TABLE_NAME.split(".")[0] if "." in TABLE_NAME else None

__all__ = [
    "EMBEDDING_DIM",
    "EMBEDDING_MODEL",
    "OLLAMA_BASE",
    "OLLAMA_MODEL",
    "TABLE_NAME",
    "create_document_store",
]


def create_document_store(recreate_table: bool = False) -> IBMDb2DocumentStore:
    """Build the official Haystack IBM Db2 document store (COSINE, FLOAT32 vectors)."""
    return IBMDb2DocumentStore(
        database=DB2_DATABASE,
        hostname=DB2_HOST,
        port=DB2_PORT,
        username=Secret.from_env_var("DB2_USERNAME"),
        password=Secret.from_env_var("DB2_PASSWORD"),
        use_ssl=DB2_SSL,
        ssl_certificate=DB2_SSL_CERT or None,
        table_name=TABLE_NAME,
        embedding_dim=EMBEDDING_DIM,
        distance_metric="COSINE",
        recreate_table=recreate_table,
    )
