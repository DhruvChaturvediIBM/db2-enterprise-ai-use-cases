"""Optional Haystack ingestion path.

This module is intentionally separate from runtime CrewAI retrieval.

The exact IBMDb2DocumentStore constructor can vary with the installed
ibm-db-haystack release. Keep the ingestion adapter isolated here so the
CrewAI agent never depends on Haystack.
"""

from haystack import Document, Pipeline
from haystack.components.writers import DocumentWriter
from haystack_integrations.document_stores.ibm_db2 import IBMDb2DocumentStore
from haystack_integrations.components.embedders.sentence_transformers import (
    SentenceTransformersDocumentEmbedder,
)

from config import settings


def build_ingestion_pipeline() -> Pipeline:
    """Build a Haystack write pipeline for compatible Db2 vector storage."""
    document_store = IBMDb2DocumentStore(
        connection_string=settings.db2_dsn,
        table_name=f"{settings.db2_schema}.{settings.knowledge_table}",
        embedding_dimension=settings.embedding_dim,
    )

    embedder = SentenceTransformersDocumentEmbedder(
        model=settings.embedding_model,
    )
    writer = DocumentWriter(document_store=document_store)

    pipeline = Pipeline()
    pipeline.add_component("embedder", embedder)
    pipeline.add_component("writer", writer)
    pipeline.connect("embedder.documents", "writer.documents")
    return pipeline


def ingest_documents(documents: list[Document]) -> dict:
    """Embed and write documents to Db2 using Haystack."""
    pipeline = build_ingestion_pipeline()
    return pipeline.run({"embedder": {"documents": documents}})
