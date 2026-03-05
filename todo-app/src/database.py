"""
database.py — SQLite Database Connection Layer
===============================================
PERSON A (Lead / DB Architect) implements this module.
If you are stuck, see the complete solution at:
    solution/three-person/person-a/database.py  (three-person workflow)
    solution/four-person/person-a/database.py   (four-person workflow)
Your tasks:
1. Define DB_PATH — path to the SQLite file
2. Implement get_connection() — returns a sqlite3.Connection
3. Implement init_db() — creates the todos table if it doesn't exist
4. Implement the DatabaseConnection context manager

Git tasks for this file:
- Create branch: git switch -c feature/db-setup
- Commit after each logical step with a meaningful message
- Push and open a Pull Request when done
"""

import sqlite3
import os
from contextlib import contextmanager

# ---------------------------------------------------------------------------
# TODO (Person A): Set the path where the SQLite database file will be stored.
# Hint: use os.path to build an absolute path relative to this file's location.
# ---------------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "--", "team08__database.db")  # replace with actual path, e.g. os.path.join(os.path.dirname(__file__), "..", "todos.db")


def get_connection(db_path: str = None) -> sqlite3.Connection:
    """
    Open and return a sqlite3 connection.
    - Use db_path if provided, otherwise fall back to DB_PATH.
    - Set row_factory to sqlite3.Row so columns are accessible by name.

    TODO (Person A): Implement this function.
    """
    if db_path is None:
        db_path = DB_PATH
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = None) -> None:
    """
    Create the todos table if it does not already exist.

    Schema:
        id          INTEGER PRIMARY KEY AUTOINCREMENT
        title       TEXT NOT NULL
        description TEXT
        priority    TEXT NOT NULL DEFAULT 'medium'
        status      TEXT NOT NULL DEFAULT 'pending'
        due_date    TEXT
        created_at  TEXT NOT NULL
        updated_at  TEXT NOT NULL

    TODO (Person A): Implement this function using get_connection().
    Hint: Use CREATE TABLE IF NOT EXISTS.
    """
     # We use our get_connection function to talk to the DB
    conn = get_connection(db_path)

    # The SQL command to create our table with the required columns
    schema = """
    CREATE TABLE IF NOT EXISTS todos (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        title       TEXT NOT NULL,
        description TEXT,
        priority    TEXT NOT NULL DEFAULT 'medium',
        status      TEXT NOT NULL DEFAULT 'pending',
        due_date    TEXT,
        created_at  TEXT NOT NULL,
        updated_at  TEXT NOT NULL
    );
    """
    # Execute the command to create the table
    conn.execute(schema)
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


@contextmanager
def db_connection(db_path: str = None):
    """
    Context manager that yields an open sqlite3 connection and
    commits on success or rolls back on exception.

    Usage:
        with db_connection() as conn:
            conn.execute("INSERT INTO todos ...")

    TODO (Person A): Implement this context manager.
    Hint: use try/except/finally with conn.commit() and conn.rollback().
    """
    raise NotImplementedError("Person A: implement db_connection context manager")
    yield  # noqa: unreachable — keep for syntax; remove after implementing
