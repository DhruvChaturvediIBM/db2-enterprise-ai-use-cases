from sample_data import SAMPLE_ADRS, adr_embedding_text
from db2_store import get_vector_store


def build_documents():
    try:
        from langchain_core.documents import Document
    except ImportError as exc:
        raise RuntimeError(
            "langchain-core is required. Install requirements.txt first."
        ) from exc

    documents = []
    for adr in SAMPLE_ADRS:
        documents.append(
            Document(
                page_content=adr_embedding_text(adr),
                metadata={
                    "document_id": adr["document_id"],
                    "title": adr["title"],
                    "status": adr["status"],
                    "effective_date": adr["effective_date"],
                    "affected_system": adr["affected_system"],
                    "decision": adr["decision"],
                    "context": adr["context"],
                    "reason": adr["reason"],
                    "rejected_alternatives": adr["rejected_alternatives"],
                },
            )
        )
    return documents


def ingest_sample_adrs():
    store = get_vector_store()
    documents = build_documents()
    store.add_documents(documents)
    return len(documents)


if __name__ == "__main__":
    count = ingest_sample_adrs()
    print(f"Ingested {count} ADR documents.")
