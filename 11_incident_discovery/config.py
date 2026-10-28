from __future__ import annotations

import os


def required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def database_config() -> dict[str, str]:
    return {
        "database": required("DB2_DATABASE"),
        "host": required("DB2_HOST"),
        "port": required("DB2_PORT"),
        "username": required("DB2_USER"),
        "password": required("DB2_PASSWORD"),
    }


def table_name() -> str:
    schema = os.getenv("DB2_SCHEMA", "AI_DEMO").strip()
    table = os.getenv("DB2_TABLE", "INCIDENTS").strip()
    if not schema or not table:
        raise RuntimeError("DB2_SCHEMA and DB2_TABLE must not be empty.")
    return f"{schema}.{table}"
