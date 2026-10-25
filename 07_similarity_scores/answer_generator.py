from __future__ import annotations

from langchain_ollama import ChatOllama
from langchain_core.documents import Document

from config import Settings
from score_router import EvidenceTier


def _context(documents: list[Document]) -> str:
    sections = []

    for document in documents:
        meta = document.metadata
        sections.append(
            "\n".join(
                [
                    f"Document ID: {meta.get('document_id', meta.get('id', 'unknown'))}",
                    f"Title: {meta.get('title', 'unknown')}",
                    f"Type: {meta.get('document_type', 'unknown')}",
                    f"Department: {meta.get('department', 'unknown')}",
                    f"Region: {meta.get('region', 'unknown')}",
                    f"Content: {document.page_content}",
                ]
            )
        )

    return "\n\n---\n\n".join(sections)


def generate_answer(
    settings: Settings,
    query: str,
    documents: list[Document],
    tier: EvidenceTier,
) -> str:
    model = ChatOllama(
        model=settings.chat_model,
        base_url=settings.ollama_base_url,
        temperature=0,
    )

    if tier is EvidenceTier.MEDIUM:
        instruction = (
            "Evidence is medium strength. Answer only from the supplied "
            "documents and explicitly state that the answer is based on "
            "moderate retrieval evidence. Do not invent missing facts."
        )
    else:
        instruction = (
            "Evidence is strong. Answer only from the supplied documents. "
            "Do not invent missing facts."
        )

    prompt = f"""You are an enterprise knowledge assistant.

{instruction}

User question:
{query}

Retrieved enterprise documents:
{_context(documents)}

Provide a concise answer. At the end, list the source document IDs and titles.
"""

    response = model.invoke(prompt)
    return response.content
