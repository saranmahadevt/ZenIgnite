"""
test_todos.py — SOLUTION (Person C in three-person / Person D in four-person)
===============================================================================
This is the complete working test suite. Study it to understand the approach,
then implement your own version in todo-app/tests/test_todos.py.

Key technique: each test class creates a real temporary SQLite file and patches
database.DB_PATH so all module-level db calls use the isolated file.
The temp file is deleted after each test.

Run with:
    python -m pytest todo-app/tests/ -v
    python -m pytest solution/three-person/person-c/test_todos.py -v
"""

import unittest
import tempfile
import time
import os
import sys

# Allow running from any directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "todo-app", "src"))

import database  # imported first so we can patch DB_PATH


class BaseTestCase(unittest.TestCase):
    """
    Base class for all tests. Creates an isolated temporary SQLite database
    for each test method and tears it down afterwards.
    """

    def setUp(self):
        # Create a temp file for this particular test
        fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        # Patch the module-level DB_PATH used by database.get_connection
        database.DB_PATH = self.db_path
        # Initialise the schema in the temp DB
        database.init_db(self.db_path)

    def tearDown(self):
        # Small retry loop for Windows file-lock issues
        for _ in range(5):
            try:
                os.unlink(self.db_path)
                break
            except PermissionError:
                time.sleep(0.05)


# ---------------------------------------------------------------------------
# Import operations & models AFTER sys.path is set
# ---------------------------------------------------------------------------
from operations import add_todo, get_todo, list_todos, update_todo, delete_todo
from models import (
    Todo,
    VALID_PRIORITIES,
    VALID_STATUSES,
    validate_priority,
    validate_status,
    validate_due_date,
)


# ===========================================================================
class TestAddTodo(BaseTestCase):
    """Tests for add_todo()."""

    def test_add_valid_todo(self):
        new_id = add_todo("Buy groceries")
        self.assertIsInstance(new_id, int)
        self.assertGreater(new_id, 0)

    def test_add_todo_with_all_fields(self):
        new_id = add_todo(
            title="Read a book",
            description="Something good",
            priority="high",
            due_date="2026-12-31",
        )
        todo = get_todo(new_id)
        self.assertEqual(todo.title, "Read a book")
        self.assertEqual(todo.description, "Something good")
        self.assertEqual(todo.priority, "high")
        self.assertEqual(todo.due_date, "2026-12-31")
        self.assertEqual(todo.status, "pending")

    def test_add_todo_default_priority_is_medium(self):
        new_id = add_todo("Default priority task")
        todo = get_todo(new_id)
        self.assertEqual(todo.priority, "medium")

    def test_add_todo_empty_title_raises(self):
        with self.assertRaises(ValueError):
            add_todo("")

    def test_add_todo_whitespace_title_raises(self):
        with self.assertRaises(ValueError):
            add_todo("   ")

    def test_add_todo_title_too_long_raises(self):
        with self.assertRaises(ValueError):
            add_todo("x" * 101)

    def test_add_todo_invalid_priority_raises(self):
        with self.assertRaises(ValueError):
            add_todo("Task", priority="urgent")

    def test_add_todo_invalid_due_date_raises(self):
        with self.assertRaises(ValueError):
            add_todo("Task", due_date="31-12-2026")

    def test_add_multiple_todos_have_different_ids(self):
        id1 = add_todo("Task 1")
        id2 = add_todo("Task 2")
        self.assertNotEqual(id1, id2)


# ===========================================================================
class TestGetTodo(BaseTestCase):
    """Tests for get_todo()."""

    def test_get_existing_todo_returns_todo_object(self):
        new_id = add_todo("Get me")
        todo = get_todo(new_id)
        self.assertIsInstance(todo, Todo)
        self.assertEqual(todo.id, new_id)
        self.assertEqual(todo.title, "Get me")

    def test_get_nonexistent_todo_returns_none(self):
        result = get_todo(9999)
        self.assertIsNone(result)

    def test_get_todo_has_created_at_and_updated_at(self):
        new_id = add_todo("Timestamps check")
        todo = get_todo(new_id)
        self.assertTrue(len(todo.created_at) > 0)
        self.assertTrue(len(todo.updated_at) > 0)


# ===========================================================================
class TestListTodos(BaseTestCase):
    """Tests for list_todos()."""

    def test_list_all_returns_all_todos(self):
        add_todo("Task A")
        add_todo("Task B")
        add_todo("Task C")
        results = list_todos()
        self.assertEqual(len(results), 3)

    def test_list_empty_database_returns_empty_list(self):
        results = list_todos()
        self.assertEqual(results, [])

    def test_list_filter_by_status_pending(self):
        id1 = add_todo("Pending task")
        id2 = add_todo("Done task")
        update_todo(id2, status="done")
        results = list_todos(status="pending")
        ids = [t.id for t in results]
        self.assertIn(id1, ids)
        self.assertNotIn(id2, ids)

    def test_list_filter_by_status_done(self):
        id1 = add_todo("Task A")
        id2 = add_todo("Task B")
        update_todo(id1, status="done")
        results = list_todos(status="done")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, id1)

    def test_list_filter_by_priority(self):
        id_high = add_todo("High task", priority="high")
        id_low = add_todo("Low task", priority="low")
        results = list_todos(priority="high")
        ids = [t.id for t in results]
        self.assertIn(id_high, ids)
        self.assertNotIn(id_low, ids)

    def test_list_combined_filters(self):
        id1 = add_todo("High pending", priority="high")
        id2 = add_todo("High done", priority="high")
        add_todo("Low pending", priority="low")
        update_todo(id2, status="done")
        results = list_todos(status="pending", priority="high")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, id1)

    def test_list_invalid_status_raises(self):
        with self.assertRaises(ValueError):
            list_todos(status="archived")

    def test_list_invalid_priority_raises(self):
        with self.assertRaises(ValueError):
            list_todos(priority="critical")

    def test_list_returns_todo_objects(self):
        add_todo("Type check")
        results = list_todos()
        self.assertIsInstance(results[0], Todo)


# ===========================================================================
class TestUpdateTodo(BaseTestCase):
    """Tests for update_todo()."""

    def test_update_status(self):
        new_id = add_todo("Status update test")
        result = update_todo(new_id, status="in-progress")
        self.assertTrue(result)
        self.assertEqual(get_todo(new_id).status, "in-progress")

    def test_update_priority(self):
        new_id = add_todo("Priority update test")
        update_todo(new_id, priority="low")
        self.assertEqual(get_todo(new_id).priority, "low")

    def test_update_title(self):
        new_id = add_todo("Old title")
        update_todo(new_id, title="New title")
        self.assertEqual(get_todo(new_id).title, "New title")

    def test_update_multiple_fields_at_once(self):
        new_id = add_todo("Multi update")
        update_todo(new_id, status="done", priority="high")
        todo = get_todo(new_id)
        self.assertEqual(todo.status, "done")
        self.assertEqual(todo.priority, "high")

    def test_update_sets_updated_at(self):
        new_id = add_todo("Timestamp update")
        original = get_todo(new_id).updated_at
        time.sleep(0.01)            # ensure time advances
        update_todo(new_id, status="done")
        updated = get_todo(new_id).updated_at
        self.assertGreater(updated, original)

    def test_update_nonexistent_returns_false(self):
        result = update_todo(9999, status="done")
        self.assertFalse(result)

    def test_update_invalid_status_raises(self):
        new_id = add_todo("Invalid status")
        with self.assertRaises(ValueError):
            update_todo(new_id, status="archived")

    def test_update_invalid_priority_raises(self):
        new_id = add_todo("Invalid priority")
        with self.assertRaises(ValueError):
            update_todo(new_id, priority="urgent")

    def test_update_unknown_field_raises(self):
        new_id = add_todo("Unknown field")
        with self.assertRaises(ValueError):
            update_todo(new_id, colour="blue")


# ===========================================================================
class TestDeleteTodo(BaseTestCase):
    """Tests for delete_todo()."""

    def test_delete_existing_todo_returns_true(self):
        new_id = add_todo("To be deleted")
        result = delete_todo(new_id)
        self.assertTrue(result)

    def test_delete_removes_record(self):
        new_id = add_todo("Must disappear")
        delete_todo(new_id)
        self.assertIsNone(get_todo(new_id))

    def test_delete_nonexistent_returns_false(self):
        result = delete_todo(9999)
        self.assertFalse(result)

    def test_delete_does_not_affect_other_todos(self):
        id1 = add_todo("Keep me")
        id2 = add_todo("Delete me")
        delete_todo(id2)
        self.assertIsNotNone(get_todo(id1))
        self.assertEqual(len(list_todos()), 1)


# ===========================================================================
class TestValidation(BaseTestCase):
    """Tests for validation functions in models.py."""

    def test_validate_priority_low(self):
        self.assertEqual(validate_priority("low"), "low")

    def test_validate_priority_medium(self):
        self.assertEqual(validate_priority("medium"), "medium")

    def test_validate_priority_high(self):
        self.assertEqual(validate_priority("high"), "high")

    def test_validate_priority_case_insensitive(self):
        self.assertEqual(validate_priority("HIGH"), "high")
        self.assertEqual(validate_priority("Medium"), "medium")

    def test_validate_priority_invalid_raises(self):
        with self.assertRaises(ValueError):
            validate_priority("urgent")

    def test_validate_status_pending(self):
        self.assertEqual(validate_status("pending"), "pending")

    def test_validate_status_in_progress(self):
        self.assertEqual(validate_status("in-progress"), "in-progress")

    def test_validate_status_done(self):
        self.assertEqual(validate_status("done"), "done")

    def test_validate_status_case_insensitive(self):
        self.assertEqual(validate_status("PENDING"), "pending")

    def test_validate_status_invalid_raises(self):
        with self.assertRaises(ValueError):
            validate_status("archived")

    def test_validate_due_date_valid(self):
        self.assertEqual(validate_due_date("2026-12-31"), "2026-12-31")

    def test_validate_due_date_none_returns_none(self):
        self.assertIsNone(validate_due_date(None))

    def test_validate_due_date_wrong_format_raises(self):
        with self.assertRaises(ValueError):
            validate_due_date("31/12/2026")

    def test_validate_due_date_dmy_format_raises(self):
        with self.assertRaises(ValueError):
            validate_due_date("31-12-2026")


if __name__ == "__main__":
    unittest.main()
