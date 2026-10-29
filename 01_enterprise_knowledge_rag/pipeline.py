"""
UC01 Haystack RAG pipeline:

    question -> OllamaTextEmbedder -> IBMDb2EmbeddingRetriever -> ChatPromptBuilder -> OllamaChatGenerator
"""

from __future__ import annotations

from haystack import Pipeline
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage
from haystack_integrations.components.embedders.ollama import OllamaTextEmbedder
from haystack_integrations.components.generators.ollama import OllamaChatGenerator
from haystack_integrations.components.retrievers.ibm_db import IBMDb2EmbeddingRetriever
from haystack_integrations.document_stores.ibm_db import IBMDb2DocumentStore

from config import EMBEDDING_MODEL, OLLAMA_BASE, OLLAMA_MODEL

SYSTEM_PROMPT = (
    "You are an enterprise knowledge assistant. Answer ONLY from the provided context.\n"
    "Rules:\n"
    "1. Cite the source document id in square brackets after each fact. "
    "Only cite ids that appear in a <document id=\"...\"> tag in the context; copy them character for character. "
    "Never cite an id that is not in the context.\n"
    "2. Answer only the question asked. Do not write additional questions or answers.\n"
    "3. If the context does not contain the answer, reply with exactly one sentence saying you could "
    "not find it in the knowledge base. Do not cite documents in that case."
)

USER_TEMPLATE = """<context>
{% for doc in documents %}
<document id="{{ doc.id }}" title="{{ doc.meta.title }}">
{{ doc.content }}
</document>
{% endfor %}
</context>

User question: {{ question }}"""


def build_rag_pipeline(store: IBMDb2DocumentStore, top_k: int = 5) -> Pipeline:
    pipe = Pipeline()
    pipe.add_component("embedder", OllamaTextEmbedder(model=EMBEDDING_MODEL, url=OLLAMA_BASE))
    pipe.add_component("retriever", IBMDb2EmbeddingRetriever(document_store=store, top_k=top_k))
    pipe.add_component(
        "prompt_builder",
        ChatPromptBuilder(
            template=[ChatMessage.from_system(SYSTEM_PROMPT), ChatMessage.from_user(USER_TEMPLATE)],
            required_variables=["documents", "question"],
        ),
    )
    pipe.add_component(
        "llm",
        OllamaChatGenerator(
            model=OLLAMA_MODEL,
            url=OLLAMA_BASE,
            # Stop sequences guard against the model inventing follow-up questions.
            generation_kwargs={"temperature": 0, "stop": ["\nQuestion:", "\nUser question:"]},
        ),
    )

    pipe.connect("embedder.embedding", "retriever.query_embedding")
    pipe.connect("retriever.documents", "prompt_builder.documents")
    pipe.connect("prompt_builder.prompt", "llm.messages")
    return pipe


def ask(pipe: Pipeline, question: str, top_k: int | None = None) -> dict:
    """Run the pipeline. Returns {"answer": str, "documents": [Document, ...]} (score = cosine distance)."""
    data: dict = {"embedder": {"text": question}, "prompt_builder": {"question": question}}
    if top_k is not None:
        data["retriever"] = {"top_k": top_k}
    out = pipe.run(data, include_outputs_from={"retriever"})
    return {
        "answer": out["llm"]["replies"][0].text,
        "documents": out["retriever"]["documents"],
    }
