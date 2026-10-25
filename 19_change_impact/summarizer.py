"""Evidence-grounded change impact summarization with Ollama."""

from langchain_ollama import OllamaLLM

from config import settings


def build_llm() -> OllamaLLM:
    return OllamaLLM(
        model=settings.llm_model,
        base_url=settings.ollama_base_url,
    )


def summarize_impact(
    change_description: str,
    results: list[dict],
) -> str:
    evidence = "\n\n".join(
        (
            f"Document ID: {item['document_id']}\n"
            f"Title: {item['title']}\n"
            f"Type: {item['document_type']}\n"
            f"Similarity: {item['similarity']:.3f}\n"
            f"Relevance band: {item['relevance_band']}\n"
            f"Excerpt: {item['content_preview']}"
        )
        for item in results
    )

    prompt = f"""
You are an enterprise change discovery assistant.

Proposed change:
{change_description}

Retrieved evidence:
{evidence}

Write a concise discovery summary.

Rules:
1. Use only the supplied evidence.
2. Cite document IDs when referring to evidence.
3. Separate strong/direct evidence from possible indirect relationships.
4. Highlight relevant historical incidents when present.
5. Do not invent dependencies, owners, systems, or risks.
6. If evidence is insufficient, say so.
7. Do not make a final approval, rejection, or implementation decision.
8. End by reminding the reader that engineers and architects must confirm actual impact.
"""

    return build_llm().invoke(prompt)
