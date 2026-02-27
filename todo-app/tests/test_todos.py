"""
test_todos.py — Unit Tests for the Todo App
=============================================
PERSON C (3-person) / PERSON D (4-person) implements this module.

If you are stuck, see the complete solution at:
    solution/three-person/person-c/test_todos.py  (three-person: Person C)
    solution/four-person/person-d/test_todos.py   (four-person: Person D)

Your tasks:
1. Implement each test method (they currently just call self.skipTest)
2. Use an in-memory SQLite database for all tests (no file created)
3. Ensure all tests pass before the final merge to main

Git tasks for this file:
- Create your branch: git switch -c feature/tests origin/main
- After writing a failing test, commit it: git commit -m "test: add failing test for add_todo"
- After making it pass, amend or commit: git commit -m "test: add_todo test passing"
- Try using `git cherry-pick` to bring a specific fix commit from another branch
- Push and open a Pull Request

Run tests:
    python -m pytest todo-app/tests/ -v
    python -m pytest todo-app/tests/ -v --tb=short
"""

import unittest
import sqlite3
import sys
import os

# ---------------------------------------------------------------------------
# TODO: Adjust these imports once the modules are implemented.
# ---------------------------------------------------------------------------
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
# from database import init_db, db_connection
# from operations import add_todo, get_todo, list_todos, update_todo, delete_todo
# from models import Todo, VALID_PRIORITIES, VALID_STATUSES


class TestAddTodo(unittest.TestCase):
    """Tests for the add_todo() function."""

    def setUp(self):
        """Set up an in-memory database before each test."""
        # TODO: Override DB_PATH with ":memory:" and call init_db()
        self.skipTest("Person C/D: implement setUp to use in-memory DB")

    def tearDown(self):
        """Clean up after each test."""
        pass  # TODO: close in-memory connection if needed

    def test_add_valid_todo(self):
        """add_todo() should return a positive integer id."""
        self.skipTest("TODO: implement — call add_todo and assert id > 0")

    def test_add_todo_with_all_fields(self):
        """add_todo() with all optional fields should persist them correctly."""
        self.skipTest("TODO: implement — verify description, due_date stored")

    def test_add_todo_empty_title_raises(self):
        """add_todo() should raise ValueError when title is empty."""
        self.skipTest("TODO: implement — assert ValueError raised for empty title")

    def test_add_todo_invalid_priority_raises(self):
        """add_todo() should raise ValueError for an invalid priority."""
        self.skipTest("TODO: implement — assert ValueError for priority='urgent'")

    def test_add_todo_invalid_due_date_raises(self):
        """add_todo() should raise ValueError for a malformed due_date."""
        self.skipTest("TODO: implement — assert ValueError for due_date='31-12-2026'")


class TestGetTodo(unittest.TestCase):
    """Tests for the get_todo() function."""

    def setUp(self):
        self.skipTest("Person C/D: implement setUp to use in-memory DB")

    def test_get_existing_todo(self):
        """get_todo() should return a Todo for a known id."""
        self.skipTest("TODO: implement — add a todo, then get it by id")

    def test_get_nonexistent_todo_returns_none(self):
        """get_todo() should return None for an id that doesn't exist."""
        self.skipTest("TODO: implement — assert get_todo(9999) is None")


class TestListTodos(unittest.TestCase):
    """Tests for the list_todos() function."""

    def setUp(self):
        self.skipTest("Person C/D: implement setUp to use in-memory DB")

    def test_list_all_returns_all(self):
        """list_todos() without filters should return all inserted todos."""
        self.skipTest("TODO: implement — insert 3 todos, assert len(list) == 3")

    def test_list_filter_by_status(self):
        """list_todos(status='done') should only return done todos."""
        self.skipTest("TODO: implement — insert mixed, filter by status")

    def test_list_filter_by_priority(self):
        """list_todos(priority='high') should only return high-priority todos."""
        self.skipTest("TODO: implement — insert mixed, filter by priority")

    def test_list_empty_db_returns_empty_list(self):
        """list_todos() on an empty database should return an empty list."""
        self.skipTest("TODO: implement — assert list_todos() == []")

    def test_list_invalid_status_raises(self):
        """list_todos(status='invalid') should raise ValueError."""
        self.skipTest("TODO: implement — assert ValueError for bad status filter")


class TestUpdateTodo(unittest.TestCase):
    """Tests for the update_todo() function."""

    def setUp(self):
        self.skipTest("Person C/D: implement setUp to use in-memory DB")

    def test_update_status(self):
        """update_todo() should change status correctly."""
        self.skipTest("TODO: implement — add, update status, get and assert new status")

    def test_update_priority(self):
        """update_todo() should change priority correctly."""
        self.skipTest("TODO: implement")

    def test_update_nonexistent_returns_false(self):
        """update_todo() should return False for a non-existent id."""
        self.skipTest("TODO: implement — assert update_todo(9999, status='done') is False")

    def test_update_invalid_status_raises(self):
        """update_todo() should raise ValueError for an invalid new status."""
        self.skipTest("TODO: implement — assert ValueError for status='archived'")

    def test_update_sets_updated_at(self):
        """update_todo() should always update the updated_at timestamp."""
        self.skipTest("TODO: implement — compare updated_at before and after")


class TestDeleteTodo(unittest.TestCase):
    """Tests for the delete_todo() function."""

    def setUp(self):
        self.skipTest("Person C/D: implement setUp to use in-memory DB")

    def test_delete_existing_todo(self):
        """delete_todo() should remove the record and return True."""
        self.skipTest("TODO: implement — add, delete, assert get returns None")

    def test_delete_nonexistent_returns_false(self):
        """delete_todo() should return False for a non-existent id."""
        self.skipTest("TODO: implement — assert delete_todo(9999) is False")


class TestValidation(unittest.TestCase):
    """Tests for validation functions in models.py."""

    def test_validate_priority_valid(self):
        """validate_priority() should accept low, medium, high (case-insensitive)."""
        self.skipTest("TODO: implement using validate_priority()")

    def test_validate_priority_invalid(self):
        """validate_priority() should raise ValueError for 'urgent'."""
        self.skipTest("TODO: implement")

    def test_validate_status_valid(self):
        """validate_status() should accept pending, in-progress, done."""
        self.skipTest("TODO: implement using validate_status()")

    def test_validate_status_invalid(self):
        """validate_status() should raise ValueError for 'archived'."""
        self.skipTest("TODO: implement")

    def test_validate_due_date_valid(self):
        """validate_due_date() should accept a correctly formatted date."""
        self.skipTest("TODO: implement — assert '2026-12-31' is accepted")

    def test_validate_due_date_invalid_format(self):
        """validate_due_date() should raise ValueError for wrong format."""
        self.skipTest("TODO: implement — assert ValueError for '31/12/2026'")

    def test_validate_due_date_none_accepted(self):
        """validate_due_date(None) should return None without error."""
        self.skipTest("TODO: implement")


if __name__ == "__main__":
    unittest.main()
