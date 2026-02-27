"""
models.py — SOLUTION (Person A — Four-Person Workflow)
========================================================
This is the complete working implementation. Study it to understand the approach,
then implement your own version in todo-app/src/models.py.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

VALID_PRIORITIES = ["low", "medium", "high"]
VALID_STATUSES = ["pending", "in-progress", "done"]


@dataclass
class Todo:
    """Represents a single Todo record from the database."""
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
        """Create a Todo from a sqlite3.Row object."""
        d = dict(row)
        return cls(**d)

    def __str__(self) -> str:
        return (
            f"Todo #{self.id}\n"
            f"  Title:       {self.title}\n"
            f"  Description: {self.description or '—'}\n"
            f"  Priority:    {self.priority}\n"
            f"  Status:      {self.status}\n"
            f"  Due Date:    {self.due_date or '—'}\n"
            f"  Created:     {self.created_at}\n"
            f"  Updated:     {self.updated_at}"
        )


def validate_priority(priority: str) -> str:
    """Validate and normalise a priority value. Raises ValueError if invalid."""
    p = priority.strip().lower()
    if p not in VALID_PRIORITIES:
        raise ValueError(
            f"Invalid priority '{priority}'. Must be one of: {', '.join(VALID_PRIORITIES)}"
        )
    return p


def validate_status(status: str) -> str:
    """Validate and normalise a status value. Raises ValueError if invalid."""
    s = status.strip().lower()
    if s not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status '{status}'. Must be one of: {', '.join(VALID_STATUSES)}"
        )
    return s


def validate_due_date(due_date: Optional[str]) -> Optional[str]:
    """Validate YYYY-MM-DD format, or accept None. Raises ValueError if malformed."""
    if due_date is None:
        return None
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
        return due_date
    except ValueError:
        raise ValueError(
            f"Invalid due_date '{due_date}'. Expected format: YYYY-MM-DD"
        )
