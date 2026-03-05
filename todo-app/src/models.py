"""
models.py — Todo Data Model & Validation
=========================================
PERSON A (Lead / DB Architect) implements this module.
If you are stuck, see the complete solution at:
    solution/three-person/person-a/models.py  (three-person workflow)
    solution/four-person/person-a/models.py   (four-person workflow)
Your tasks:
1. Define VALID_PRIORITIES and VALID_STATUSES constants
2. Implement the Todo dataclass
3. Implement validate_priority() and validate_status()
4. Implement Todo.from_row() class method

Git tasks for this file:
- Commit together with database.py on the same branch: feature/db-setup
- Use `git add -p` to stage specific hunks if you made unrelated changes
"""

from dataclasses import dataclass, field
from typing import Optional
import datetime

# ---------------------------------------------------------------------------
# TODO (Person A): Define valid values for priority and status fields.
# ---------------------------------------------------------------------------
VALID_PRIORITIES = ["low", "medium", "high"]
VALID_STATUSES = ["pending", "in-progress", "done"]


@dataclass
class Todo:
    """
    Represents a single Todo record from the database.

    TODO (Person A): Fill in the field types and default values below.
    Use Python's dataclasses module. Mark optional fields with Optional[str] = None.
    """
    id: Optional[int] = None
    title: str = ""
    description: Optional[str] = None
    priority: str = "medium"
    status: str = "pending"
    due_date: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""

    @classmethod
    def from_row(cls, row) -> "Todo":
        """
        Create a Todo instance from a sqlite3.Row object.

        TODO (Person A): Implement this method.
        Hint: sqlite3.Row supports dict(row) or row["column_name"] access.
        """
        raise NotImplementedError("Person A: implement Todo.from_row()")

    def __str__(self) -> str:
        """Human-readable string representation of a Todo."""
        # TODO (Person A): Return a nicely formatted string showing all fields.
        raise NotImplementedError("Person A: implement Todo.__str__()")


def validate_priority(priority: str) -> str:
    """
    Validate that priority is one of VALID_PRIORITIES.
    Return the priority (lowercased) if valid.
    Raise ValueError with a clear message if invalid.

    TODO (Person A): Implement this function.
    """
    raise NotImplementedError("Person A: implement validate_priority()")


def validate_status(status: str) -> str:
    """
    Validate that status is one of VALID_STATUSES.
    Return the status (lowercased) if valid.
    Raise ValueError with a clear message if invalid.

    TODO (Person A): Implement this function.
    """
    raise NotImplementedError("Person A: implement validate_status()")


def validate_due_date(due_date: Optional[str]) -> Optional[str]:
    """
    Validate that due_date is either None or a valid YYYY-MM-DD string.
    Return the string if valid, None if None.
    Raise ValueError if the format is wrong.

    TODO (Person A): Implement this function.
    Hint: use datetime.datetime.strptime(due_date, "%Y-%m-%d")
    """
    raise NotImplementedError("Person A: implement validate_due_date()")
