"""
cli.py — SOLUTION (Person C — Four-Person Workflow)
=====================================================
This is the complete working implementation. Study it to understand the approach,
then implement your own version in todo-app/src/cli.py.

Usage:
    python cli.py add    --title "Buy groceries" --priority high --due 2026-03-01
    python cli.py list
    python cli.py list   --status pending
    python cli.py list   --priority high
    python cli.py show   --id 1
    python cli.py update --id 1 --status in-progress
    python cli.py update --id 1 --priority low --title "Buy organic groceries"
    python cli.py delete --id 1
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from prettytable import PrettyTable
from database import init_db
from operations import add_todo, get_todo, list_todos, update_todo, delete_todo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Todo CLI — ZenIgnite Training App",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new todo")
    p_add.add_argument("--title", required=True, help="Todo title (max 100 chars)")
    p_add.add_argument("--description", default=None)
    p_add.add_argument("--priority", default="medium", choices=["low", "medium", "high"])
    p_add.add_argument("--due", default=None, dest="due_date", metavar="YYYY-MM-DD")

    p_list = sub.add_parser("list", help="List todos with optional filters")
    p_list.add_argument("--status", default=None)
    p_list.add_argument("--priority", default=None)

    p_show = sub.add_parser("show", help="Show full details of a single todo")
    p_show.add_argument("--id", type=int, required=True)

    p_update = sub.add_parser("update", help="Update a todo's fields")
    p_update.add_argument("--id", type=int, required=True)
    p_update.add_argument("--title", default=None)
    p_update.add_argument("--description", default=None)
    p_update.add_argument("--priority", default=None)
    p_update.add_argument("--status", default=None)
    p_update.add_argument("--due", default=None, dest="due_date", metavar="YYYY-MM-DD")

    p_delete = sub.add_parser("delete", help="Delete a todo by ID")
    p_delete.add_argument("--id", type=int, required=True)

    return parser


def cmd_add(args: argparse.Namespace) -> None:
    new_id = add_todo(
        title=args.title,
        description=args.description,
        priority=args.priority,
        due_date=args.due_date,
    )
    print(f"Todo #{new_id} created: '{args.title}'")


def cmd_list(args: argparse.Namespace) -> None:
    todos = list_todos(status=args.status, priority=args.priority)
    if not todos:
        print("No todos found.")
        return

    table = PrettyTable(["ID", "Title", "Priority", "Status", "Due Date", "Created"])
    table.align = "l"
    for todo in todos:
        table.add_row([
            todo.id,
            todo.title[:38] + ".." if len(todo.title) > 40 else todo.title,
            todo.priority,
            todo.status,
            todo.due_date or "—",
            todo.created_at[:10],
        ])
    print(table)


def cmd_show(args: argparse.Namespace) -> None:
    todo = get_todo(args.id)
    if not todo:
        print(f"Error: Todo #{args.id} not found.")
        sys.exit(1)
    print(todo)


def cmd_update(args: argparse.Namespace) -> None:
    kwargs = {}
    for field in ("title", "description", "priority", "status", "due_date"):
        val = getattr(args, field, None)
        if val is not None:
            kwargs[field] = val

    if not kwargs:
        print("No fields to update.")
        return

    if update_todo(args.id, **kwargs):
        print(f"Todo #{args.id} updated.")
    else:
        print(f"Error: Todo #{args.id} not found.")
        sys.exit(1)


def cmd_delete(args: argparse.Namespace) -> None:
    if delete_todo(args.id):
        print(f"Todo #{args.id} deleted.")
    else:
        print(f"Error: Todo #{args.id} not found.")
        sys.exit(1)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    init_db()

    dispatch = {
        "add": cmd_add,
        "list": cmd_list,
        "show": cmd_show,
        "update": cmd_update,
        "delete": cmd_delete,
    }

    try:
        dispatch[args.command](args)
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
