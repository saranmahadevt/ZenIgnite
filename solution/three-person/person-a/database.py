"""
database.py — SOLUTION (Person A)
===================================
This is the complete working implementation. Study it to understand the approach,
then implement your own version in todo-app/src/database.py.
"""

import sqlite3
import os
from contextlib import contextmanager

# Absolute path to the database file, stored one level above src/
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "todos.db")


def get_connection(db_path: str = None) -> sqlite3.Connection:
    """Open and return a sqlite3.Connection with row_factory set to sqlite3.Row."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = None) -> None:
    """Create the todos table if it does not already exist."""
    with db_connection(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT NOT NULL,
                description TEXT,
                priority    TEXT NOT NULL DEFAULT 'medium',
                status      TEXT NOT NULL DEFAULT 'pending',
                due_date    TEXT,
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL
            )
        """)


@contextmanager
def db_connection(db_path: str = None):
    """
    Context manager: opens a connection, commits on success, rolls back on error.

    Usage:
        with db_connection() as conn:
            conn.execute("INSERT INTO todos ...")
    """
    conn = get_connection(db_path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
