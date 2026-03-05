"""
operations.py — CRUD Business Logic
=====================================
PERSON B (Backend Developer) implements this module.
If you are stuck, see the complete solution at:
    solution/three-person/person-b/operations.py  (three-person workflow)
    solution/four-person/person-b/operations.py   (four-person workflow)
Your tasks:
1. Implement add_todo()
2. Implement get_todo()
3. Implement list_todos()
4. Implement update_todo()
5. Implement delete_todo()

Git tasks for this file:
- Create your branch AFTER Person A merges feature/db-setup:
    git fetch origin
    git switch -c feature/crud-operations origin/main
- Implement and commit each function separately for clean history
- Rebase on main if it has changed: git rebase main
- Use `git log --oneline --graph` to see where your branch diverges
- Push and open a Pull Request when done
"""

from datetime import datetime, timezone
from typing import Optional, List

from database import db_connection
from models import Todo, validate_priority, validate_status, validate_due_date


def _now() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def add_todo(
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    due_date: Optional[str] = None,
) -> int:
    """
    Insert a new todo into the database.

    Steps:
    1. Validate title (not empty, max 100 chars)
    2. Validate priority using validate_priority()
    3. Validate due_date using validate_due_date()
    4. Insert the record with created_at and updated_at set to now
    5. Return the new row's id

    TODO (Person B): Implement this function.

    Raises:
        ValueError: if title is empty or validation fails
    Returns:
        int: the id of the newly created todo
    """
    # Step 1: Validate title
    if not title or not title.strip():
        raise ValueError("Title cannot be empty.")
    if len(title) > 100:
        raise ValueError("Title must be 100 characters or fewer.")

    # Step 2 & 3: Validate priority and due_date
    priority = validate_priority(priority)
    due_date = validate_due_date(due_date)

    # Step 4: Insert into DB and return new id
    now = _now()
    with db_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO todos (title, description, priority, due_date, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (title.strip(), description, priority, due_date, now, now),
        )
        return cursor.lastrowid


def get_todo(todo_id: int) -> Optional[object]:
    """
    Retrieve a single todo by its id.

    TODO (Person B): Implement this function.

    Returns:
        Todo if found, None if not found
    """
    raise NotImplementedError("Person B: implement get_todo()")


def list_todos(
    status: Optional[str] = None,
    priority: Optional[str] = None,
) -> List[object]:
    """
    Retrieve all todos, with optional filters.

    - If status is provided, filter by status (validate first)
    - If priority is provided, filter by priority (validate first)
    - Order results by: priority (high → medium → low), then created_at DESC

    TODO (Person B): Implement this function.

    Returns:
        List of Todo objects (may be empty)
    """
    raise NotImplementedError("Person B: implement list_todos()")


def update_todo(todo_id: int, **kwargs) -> bool:
    """
    Update fields of an existing todo.

    Accepted keyword arguments: title, description, priority, status, due_date
    Always update updated_at to the current timestamp.

    Steps:
    1. Verify the todo exists (use get_todo)
    2. Validate any provided priority or status values
    3. Build a dynamic UPDATE query from the provided kwargs
    4. Execute the update

    TODO (Person B): Implement this function.

    Returns:
        True if the todo was found and updated, False if not found
    Raises:
        ValueError: if an unknown field is provided or validation fails
    """
    raise NotImplementedError("Person B: implement update_todo()")


def delete_todo(todo_id: int) -> bool:
    """
    Delete a todo by its id.

    TODO (Person B): Implement this function.

    Returns:
        True if the todo was found and deleted, False if not found
    """
    raise NotImplementedError("Person B: implement delete_todo()")
