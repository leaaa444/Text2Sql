#connect to localdatabase with read-only user and run query

import psycopg

from agent.config import settings


def _readonly_kwargs():
    return dict(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_readonly_user,
        password=settings.db_readonly_password,
        autocommit=True,
        options="-c default_transaction_read_only=on",
    )


def run_query(sql, limit=None):
    with psycopg.connect(**_readonly_kwargs()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            columns = [d.name for d in cur.description] if cur.description else []
            rows = cur.fetchmany(limit) if limit is not None else cur.fetchall()
    return columns, rows
