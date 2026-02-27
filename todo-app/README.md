# Todo App — Requirements & Setup

## Overview

A command-line Todo application built in Python using SQLite for persistence. This is the application your team will build together during the ZenIgnite Git training.

---

## Functional Requirements

### Todo Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | INTEGER | auto | Primary key, auto-incremented |
| `title` | TEXT | Yes | Max 100 characters |
| `description` | TEXT | No | Max 500 characters |
| `priority` | TEXT | Yes | `low`, `medium`, `high` |
| `status` | TEXT | Yes | `pending`, `in-progress`, `done` |
| `due_date` | TEXT | No | Format: `YYYY-MM-DD` |
| `created_at` | TEXT | auto | ISO timestamp, set on insert |
| `updated_at` | TEXT | auto | ISO timestamp, updated on change |

### Commands to Implement

```
python cli.py add      --title "Buy groceries" --priority high --due 2026-03-01
python cli.py list
python cli.py list     --status pending
python cli.py list     --priority high
python cli.py update   --id 1 --status in-progress
python cli.py update   --id 1 --priority low
python cli.py delete   --id 1
python cli.py show     --id 1
```

---

## Module Responsibilities

### `src/database.py` — Person A (Lead/DB Architect)

Responsibilities:
- Open and close the SQLite connection
- Create the `todos` table if it does not exist
- Provide a context manager or helper for database access

### `src/models.py` — Person A (Lead/DB Architect)

Responsibilities:
- Define a `Todo` dataclass or named tuple representing a todo row
- Define constants for valid priority and status values
- Input validation logic (raise `ValueError` for invalid data)

### `src/operations.py` — Person B (Backend Developer)

Responsibilities:
- `add_todo(title, description, priority, due_date)` → returns new todo id
- `get_todo(todo_id)` → returns a `Todo` or `None`
- `list_todos(status=None, priority=None)` → returns list of `Todo`
- `update_todo(todo_id, **kwargs)` → returns `True` if updated
- `delete_todo(todo_id)` → returns `True` if deleted

### `src/cli.py` — Person C (Interface Builder)

Responsibilities:
- Parse command-line arguments using `argparse`
- Call functions from `operations.py`
- Display output in a readable table format using `prettytable`
- Handle errors gracefully (invalid id, missing title, etc.)

### `tests/test_todos.py` — Person C (QA) / Person D (4-person workflow)

Responsibilities:
- Test each CRUD operation with `unittest`
- Use an in-memory SQLite database (`:memory:`) for isolation
- At minimum: test add, list, update status, delete, invalid input

---

## File Structure

```
todo-app/
├── README.md            ← This file
├── requirements.txt     ← Python dependencies
└── src/
    ├── database.py      ← DB layer (skeleton provided)
    ├── models.py        ← Data model (skeleton provided)
    ├── operations.py    ← CRUD logic (skeleton provided)
    └── cli.py           ← CLI interface (skeleton provided)
└── tests/
    └── test_todos.py    ← Unit tests (stubs provided)
```

---

## Setup

```bash
# From the ZenIgnite root:
pip install -r todo-app/requirements.txt

# Run the CLI
python todo-app/src/cli.py --help

# Run tests
python -m pytest todo-app/tests/ -v
```

---

## Acceptance Criteria

Your implementation is complete when:

1. `python cli.py add --title "Test" --priority medium` creates a record in `todos.db`
2. `python cli.py list` shows all todos in a formatted table
3. `python cli.py list --status pending` filters correctly
4. `python cli.py update --id 1 --status done` changes status and updates `updated_at`
5. `python cli.py delete --id 1` removes the record
6. All tests in `tests/test_todos.py` pass
7. Invalid inputs (missing title, bad priority, non-existent id) show clear error messages
