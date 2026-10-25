"""Actual IBM Db2 search tool used by the CrewAI agent.

Uses DB2VectorSearchTool from crewai-tools against AI_DEMO.RESEARCH_KNOWLEDGE,
which has plain VARCHAR document_id and title columns alongside the standard
DB2VS columns. This avoids the metadata BLOB serialisation issue.
"""

import ollama as _ollama
from crewai_tools import DB2VectorSearchTool

from config import settings


def embed_query(text: str) -> list[float]:
    """Embed using the same nomic-embed-text model used to seed RESEARCH_KNOWLEDGE."""
    client = _ollama.Client(host=settings.ollama_base_url)
    resp = client.embeddings(model=settings.embedding_model, prompt=text)
    return resp["embedding"]


db2_search_tool = DB2VectorSearchTool(
    name="ibm_db2_enterprise_knowledge_search",
    description=(
        "Search the IBM Db2 enterprise knowledge base. "
        "Input: a plain-text search query string only. "
        "Returns matching documents with their document_id, title, and content. "
        "Use the document_id values (e.g. ADR-001, POL-001, INC-001) as "
        "citations in your answer. "
        "Do not pass any parameters other than the query string."
    ),
    connection_string=settings.db2_dsn,
    table_name=f"{settings.db2_schema}.{settings.knowledge_table}",
    vector_column="embedding",
    return_columns=["document_id", "title", "text"],
    limit=settings.retrieval_top_k,
    distance_metric=settings.distance_metric,
    custom_embedding_fn=embed_query,
)
