"""Configuration for UC19 Semantic Change Impact Discovery."""

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
    knowledge_table: str = os.getenv("KNOWLEDGE_TABLE", "KNOWLEDGE_BASE")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    llm_model: str = os.getenv("LLM_MODEL", "granite3.1-dense:8b")
    top_k: int = int(os.getenv("TOP_K", "10"))
    direct_impact_threshold: float = float(
        os.getenv("DIRECT_IMPACT_THRESHOLD", "0.75")
    )
    indirect_impact_threshold: float = float(
        os.getenv("INDIRECT_IMPACT_THRESHOLD", "0.55")
    )


settings = Settings()
