from db2_store import get_vector_store
from sample_data import SAMPLE_TICKETS, ticket_embedding_text


def build_documents():
    from langchain_core.documents import Document

    documents = []

    for ticket in SAMPLE_TICKETS:
        documents.append(
            Document(
                page_content=ticket_embedding_text(ticket),
                metadata={
                    "document_id": ticket["document_id"],
                    "title": ticket["title"],
                    "team": ticket["team"],
                    "category": ticket["category"],
                    "priority": ticket["priority"],
                    "product": ticket["product"],
                    "resolution_summary": ticket["resolution_summary"],
                },
            )
        )

    return documents


def ingest_sample_tickets():
    store = get_vector_store()
    documents = build_documents()
    store.add_documents(documents)
    return len(documents)


if __name__ == "__main__":
    count = ingest_sample_tickets()
    print(f"Ingested {count} ticket documents.")
