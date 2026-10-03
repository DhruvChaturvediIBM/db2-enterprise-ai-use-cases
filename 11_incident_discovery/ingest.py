from __future__ import annotations

from langchain_core.documents import Document
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_db2 import DB2VS

from config import table_name
from db import create_connection
from embeddings import create_embeddings
from sample_data import INCIDENTS, incident_to_text


def build_documents() -> list[Document]:
    return [
        Document(
            page_content=incident_to_text(incident),
            metadata={
                "incident_id": incident["incident_id"],
                "title": incident["title"],
                "severity": incident["severity"],
                "service": incident["service"],
                "department": incident["department"],
                "product": incident["product"],
                "root_cause": incident["root_cause"],
                "resolution": incident["resolution"],
                "effective_date": incident["effective_date"].isoformat(),
            },
        )
        for incident in INCIDENTS
    ]


def ingest() -> None:
    connection = create_connection()
    embeddings = create_embeddings()
    documents = build_documents()

    print(f"Ingesting {len(documents)} incidents into {table_name()}...")

    DB2VS.from_documents(
        documents,
        embeddings,
        client=connection,
        table_name=table_name(),
        distance_strategy=DistanceStrategy.COSINE,
    )

    print("Incident ingestion complete.")


if __name__ == "__main__":
    ingest()
