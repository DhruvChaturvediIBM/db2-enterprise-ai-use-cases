"""Environment configuration for UC13."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    db2_host: str = os.getenv("DB2_HOST", "localhost")
    db2_port: int = int(os.getenv("DB2_PORT", "50000"))
    db2_database: str = os.getenv("DB2_DATABASE", "BLUDB")
    db2_username: str = os.getenv("DB2_USERNAME", "")
    db2_password: str = os.getenv("DB2_PASSWORD", "")
    db2_schema: str = os.getenv("DB2_SCHEMA", "AI_DEMO")
    knowledge_table: str = os.getenv("KNOWLEDGE_TABLE", "RESEARCH_KNOWLEDGE")

    ollama_base_url: str = os.getenv(
        "OLLAMA_BASE_URL", "http://localhost:11434"
    )
    llm_model: str = os.getenv("LLM_MODEL", "llama3.1:8b")

    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL",
        "nomic-embed-text",
    )
    embedding_dim: int = int(os.getenv("EMBEDDING_DIM", "768"))
    retrieval_top_k: int = int(os.getenv("RETRIEVAL_TOP_K", "10"))
    distance_metric: str = os.getenv("DISTANCE_METRIC", "COSINE")

    @property
    def db2_dsn(self) -> str:
        return (
            f"DATABASE={self.db2_database};"
            f"HOSTNAME={self.db2_host};"
            f"PORT={self.db2_port};"
            f"PROTOCOL=TCPIP;"
            f"UID={self.db2_username};"
            f"PWD={self.db2_password};"
        )


settings = Settings()
