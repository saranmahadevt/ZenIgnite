"""
operations.py — SOLUTION (Person B)
======================================
This is the complete working implementation. Study it to understand the approach,
then implement your own version in todo-app/src/operations.py.
"""

import sys
import os
from datetime import datetime, timezone
from typing import Optional, List

# Allow running this file directly from any working directory
sys.path.insert(0, os.path.dirname(__file__))
from database import db_connection
from models import Todo, validate_priority, validate_status, validate_due_date


def _now() -> str:
    """Return current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def add_todo(
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    due_date: Optional[str] = None,
) -> int:
    """
    Insert a new todo and return its id.

    Raises:
        ValueError: if title is empty, exceeds 100 chars, or validations fail.
    """
    if not title or not title.strip():
        raise ValueError("Title cannot be empty.")
    if len(title) > 100:
        raise ValueError("Title cannot exceed 100 characters.")

    priority = validate_priority(priority)
    due_date = validate_due_date(due_date)
    now = _now()

    with db_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO todos
                   (title, description, priority, status, due_date, created_at, updated_at)
               VALUES (?, ?, ?, 'pending', ?, ?, ?)""",
            (title.strip(), description, priority, due_date, now, now),
        )
        return cursor.lastrowid


def get_todo(todo_id: int) -> Optional[Todo]:
    """Return a Todo by id, or None if not found."""
    with db_connection() as conn:
        row = conn.execute(
            "SELECT * FROM todos WHERE id = ?", (todo_id,)
        ).fetchone()
        return Todo.from_row(row) if row else None


def list_todos(
    status: Optional[str] = None,
    priority: Optional[str] = None,
) -> List[Todo]:
    """
    Return all todos, with optional status and priority filters.
    Results are ordered: high → medium → low priority, then created_at DESC.
    """
    query = "SELECT * FROM todos WHERE 1=1"
    params: list = []

    if status is not None:
        status = validate_status(status)
        query += " AND status = ?"
        params.append(status)

    if priority is not None:
        priority = validate_priority(priority)
        query += " AND priority = ?"
        params.append(priority)

    query += (
        " ORDER BY CASE priority"
        "  WHEN 'high'   THEN 1"
        "  WHEN 'medium' THEN 2"
        "  WHEN 'low'    THEN 3 END,"
        " created_at DESC"
    )

    with db_connection() as conn:
        rows = conn.execute(query, params).fetchall()
        return [Todo.from_row(r) for r in rows]


def update_todo(todo_id: int, **kwargs) -> bool:
    """
    Update the specified fields of a todo. Always updates updated_at.

    Returns:
        True if the todo was found and updated, False if not found.
    Raises:
        ValueError: for unknown fields or invalid values.
    """
    ALLOWED = {"title", "description", "priority", "status", "due_date"}
    unknown = set(kwargs) - ALLOWED
    if unknown:
        raise ValueError(f"Unknown field(s): {', '.join(sorted(unknown))}")

    if not get_todo(todo_id):
        return False

    if "priority" in kwargs:
        kwargs["priority"] = validate_priority(kwargs["priority"])
    if "status" in kwargs:
        kwargs["status"] = validate_status(kwargs["status"])
    if "due_date" in kwargs:
        kwargs["due_date"] = validate_due_date(kwargs["due_date"])

    kwargs["updated_at"] = _now()

    set_clause = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [todo_id]

    with db_connection() as conn:
        conn.execute(
            f"UPDATE todos SET {set_clause} WHERE id = ?", values
        )
    return True


def delete_todo(todo_id: int) -> bool:
    """
    Delete a todo by id.

    Returns:
        True if deleted, False if not found.
    """
    if not get_todo(todo_id):
        return False

    with db_connection() as conn:
        conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    return True
