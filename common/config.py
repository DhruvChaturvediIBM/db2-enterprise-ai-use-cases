"""
common/config.py
────────────────
Load all environment variables for IBM Db2 AI Use Cases.
Every use case imports this module — never read env vars directly.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Walk up from this file to find .env (handles running from any sub-folder)
_root = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=_root / ".env", override=False)


def _require(key: str) -> str:
    v = os.getenv(key)
    if not v:
        raise EnvironmentError(
            f"Required environment variable '{key}' is not set.\n"
            f"Copy .env.example to .env and fill in your credentials."
        )
    return v


# ── IBM Db2 ───────────────────────────────────────────────────────────────────
DB2_HOST     = _require("DB2_HOST")
DB2_PORT     = int(os.getenv("DB2_PORT", "50000"))
DB2_DATABASE = os.getenv("DB2_DATABASE", "BLUDB")
DB2_USERNAME = _require("DB2_USERNAME")
DB2_PASSWORD = _require("DB2_PASSWORD")
DB2_SSL      = os.getenv("DB2_SSL", "false").lower() == "true"
DB2_SSL_CERT = os.getenv("DB2_SSL_CERT_PATH", "")
DB2_SCHEMA   = os.getenv("DB2_SCHEMA", "AI_DEMO")

# ── LLM ───────────────────────────────────────────────────────────────────────
LLM_PROVIDER  = os.getenv("LLM_PROVIDER", "ollama").lower()
OLLAMA_BASE   = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL  = os.getenv("OLLAMA_MODEL", "granite3.1-dense:8b")
OPENAI_KEY    = os.getenv("OPENAI_API_KEY", "")
WATSONX_KEY   = os.getenv("WATSONX_API_KEY", "")
WATSONX_PID   = os.getenv("WATSONX_PROJECT_ID", "")
WATSONX_URL   = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

# ── Embeddings ────────────────────────────────────────────────────────────────
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "ollama").lower()
EMBEDDING_MODEL    = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
EMBEDDING_DIM      = int(os.getenv("EMBEDDING_DIM", "768"))

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
