from __future__ import annotations

import ibm_db
import ibm_db_dbi

from config import database_config


def create_connection():
    cfg = database_config()

    dsn = (
        f"DATABASE={cfg['database']};"
        f"HOSTNAME={cfg['host']};"
        f"PORT={cfg['port']};"
        f"PROTOCOL=TCPIP;"
        f"UID={cfg['username']};"
        f"PWD={cfg['password']};"
    )

    raw_connection = ibm_db.connect(dsn, "", "")
    return ibm_db_dbi.Connection(raw_connection)
