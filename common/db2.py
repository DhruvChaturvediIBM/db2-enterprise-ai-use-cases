"""
common/db2.py
─────────────
IBM Db2 connection helpers shared across all use cases.

Usage
-----
from common.db2 import get_connection, get_connection_string

conn = get_connection()          # ibm_db native connection
cs   = get_connection_string()   # SQLAlchemy-compatible DSN string
"""

import ibm_db
import ibm_db_dbi
from common.config import (
    DB2_HOST, DB2_PORT, DB2_DATABASE,
    DB2_USERNAME, DB2_PASSWORD,
    DB2_SSL, DB2_SSL_CERT, DB2_SCHEMA,
)


def _build_dsn() -> str:
    """Build the ibm_db DSN string from environment config."""
    dsn = (
        f"DATABASE={DB2_DATABASE};"
        f"HOSTNAME={DB2_HOST};"
        f"PORT={DB2_PORT};"
        f"PROTOCOL=TCPIP;"
        f"UID={DB2_USERNAME};"
        f"PWD={DB2_PASSWORD};"
    )
    if DB2_SSL:
        dsn += "Security=SSL;"
        if DB2_SSL_CERT:
            dsn += f"SSLServerCertificate={DB2_SSL_CERT};"
    return dsn


def get_connection() -> ibm_db_dbi.Connection:
    """
    Return a DB-API 2.0-compatible ibm_db connection.
    Raises a clear error if the connection fails.
    """
    dsn = _build_dsn()
    try:
        conn = ibm_db.connect(dsn, "", "")
        return ibm_db_dbi.Connection(conn)
    except Exception as e:
        raise ConnectionError(
            f"Cannot connect to IBM Db2 at {DB2_HOST}:{DB2_PORT}/{DB2_DATABASE}.\n"
            f"Check your .env credentials and VPN connection.\n"
            f"Error: {e}"
        ) from e


def get_connection_string() -> str:
    """
    Return a SQLAlchemy-compatible Db2 connection string.
    Used by LangChain DB2VS and ibm_db_sa.
    """
    proto = "db2+ibm_db"
    ssl_suffix = "?Security=SSL" if DB2_SSL else ""
    return (
        f"{proto}://{DB2_USERNAME}:{DB2_PASSWORD}"
        f"@{DB2_HOST}:{DB2_PORT}/{DB2_DATABASE}{ssl_suffix}"
    )


def ensure_schema(conn) -> None:
    """Create the working schema if it does not already exist."""
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE SCHEMA {DB2_SCHEMA}")
    except Exception:
        pass  # schema already exists — safe to ignore
    finally:
        cursor.close()


def run_sql(conn, sql: str, params: tuple = ()) -> list[dict]:
    """Execute a SQL statement and return rows as list-of-dicts."""
    cursor = conn.cursor()
    cursor.execute(sql, params)
    if cursor.description:
        cols = [d[0] for d in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]
    return []
