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
    adr_table: str = os.getenv("ADR_TABLE", "ARCHITECTURE_DECISIONS")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    ollama_base_url: str = os.getenv(
        "OLLAMA_BASE_URL", "http://localhost:11434"
    )
    top_k: int = int(os.getenv("TOP_K", "3"))


settings = Settings()
