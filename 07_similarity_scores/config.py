from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    db2_database: str
    db2_host: str
    db2_port: str
    db2_username: str
    db2_password: str
    db2_security: bool
    db2_table: str
    ollama_base_url: str
    embedding_model: str
    chat_model: str
    top_k: int
    high_max_distance: float
    medium_max_distance: float


def get_settings() -> Settings:
    return Settings(
        db2_database=os.environ["DB2_DATABASE"],
        db2_host=os.environ["DB2_HOST"],
        db2_port=os.environ["DB2_PORT"],
        db2_username=os.environ["DB2_USERNAME"],
        db2_password=os.environ["DB2_PASSWORD"],
        db2_security=os.getenv("DB2_SECURITY", "false").lower() == "true",
        db2_table=os.getenv("DB2_TABLE", "AI_DEMO.KNOWLEDGE_BASE"),
        ollama_base_url=os.getenv(
            "OLLAMA_BASE_URL", "http://localhost:11434"
        ),
        embedding_model=os.getenv(
            "OLLAMA_EMBEDDING_MODEL", "nomic-embed-text"
        ),
        chat_model=os.getenv(
            "OLLAMA_CHAT_MODEL", "granite3.1-dense:8b"
        ),
        top_k=int(os.getenv("TOP_K", "5")),
        high_max_distance=float(os.getenv("HIGH_MAX_DISTANCE", "0.35")),
        medium_max_distance=float(os.getenv("MEDIUM_MAX_DISTANCE", "0.52")),
    )
