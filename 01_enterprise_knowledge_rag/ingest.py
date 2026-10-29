"""
UC01 ingestion: shared enterprise corpus -> embeddings -> IBMDb2DocumentStore.

Each EnterpriseDocument becomes one Haystack Document. The business `document_id`
is used as the Haystack document id, so retrieval results can cite it directly.
"""

from __future__ import annotations

from dataclasses import asdict

from haystack import Document
from haystack.document_stores.types import DuplicatePolicy
from haystack_integrations.components.embedders.ollama import OllamaDocumentEmbedder
from haystack_integrations.document_stores.ibm_db import IBMDb2DocumentStore

from common.db2 import ensure_schema, get_connection
from common.sample_data import ALL_DOCUMENTS
from config import EMBEDDING_DIM, EMBEDDING_MODEL, OLLAMA_BASE, SCHEMA_NAME

_META_FIELDS = (
    "title", "document_type", "department", "business_unit", "region", "product",
    "classification", "status", "effective_date", "owner", "source", "tags",
)


def build_documents() -> list[Document]:
    docs = []
    for d in ALL_DOCUMENTS:
        data = asdict(d)
        docs.append(
            Document(
                id=d.document_id,
                content=d.content,
                meta={k: data[k] for k in _META_FIELDS},
            )
        )
    return docs


def ingest(store: IBMDb2DocumentStore) -> int:
    """Embed the corpus with Ollama and upsert it into Db2. Returns the row count written."""
    if SCHEMA_NAME:
        conn = get_connection()
        try:
            ensure_schema(conn)  # no-op if AI_DEMO already exists
        finally:
            conn.close()

    embedder = OllamaDocumentEmbedder(
        model=EMBEDDING_MODEL,
        url=OLLAMA_BASE,
        meta_fields_to_embed=["title"],  # titles carry strong signal (e.g. "Europe", "Db2")
        progress_bar=False,
    )
    embedded = embedder.run(documents=build_documents())["documents"]

    dim = len(embedded[0].embedding)
    if dim != EMBEDDING_DIM:
        raise ValueError(
            f"Embedding model '{EMBEDDING_MODEL}' returned {dim} dimensions but "
            f"EMBEDDING_DIM={EMBEDDING_DIM}. Fix EMBEDDING_DIM in .env and re-run with --recreate."
        )

    return store.write_documents(embedded, policy=DuplicatePolicy.OVERWRITE)
