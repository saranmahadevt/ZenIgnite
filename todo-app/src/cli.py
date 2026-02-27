"""
cli.py — Command-Line Interface
================================
PERSON C (Interface Builder) implements this module.
If you are stuck, see the complete solution at:
    solution/three-person/person-c/cli.py  (three-person workflow)
    solution/four-person/person-c/cli.py  (four-person workflow)
Your tasks:
1. Set up argparse with subcommands: add, list, update, delete, show
2. Call the appropriate function from operations.py for each subcommand
3. Display results in a formatted table using prettytable
4. Handle errors (ValueError, missing records) with friendly messages

Git tasks for this file:
- Create your branch AFTER Person B merges feature/crud-operations:
    git fetch origin
    git switch -c feature/cli-interface origin/main
- Use `git stash` when switching branches mid-work
- Use `git diff --staged` before every commit to review what you're committing
- After finishing, use `git rebase -i HEAD~<n>` to squash WIP commits
- Push and open a Pull Request when done

Usage (once implemented):
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

# ---------------------------------------------------------------------------
# TODO (Person C): Import from operations once Person B's code is merged.
# ---------------------------------------------------------------------------
# from operations import add_todo, get_todo, list_todos, update_todo, delete_todo
# from database import init_db

# ---------------------------------------------------------------------------
# TODO (Person C): Import prettytable for formatted output.
# from prettytable import PrettyTable
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """
    Build and return the top-level argument parser with subcommands.

    Subcommands to define:
        add     --title (required) --description --priority --due
        list    --status --priority
        show    --id (required)
        update  --id (required) --title --description --priority --status --due
        delete  --id (required)

    TODO (Person C): Implement this function.
    """
    raise NotImplementedError("Person C: implement build_parser()")


def cmd_add(args: argparse.Namespace) -> None:
    """
    Handle the `add` subcommand.
    Call add_todo(), then print a success message with the new id.

    TODO (Person C): Implement this function.
    """
    raise NotImplementedError("Person C: implement cmd_add()")


def cmd_list(args: argparse.Namespace) -> None:
    """
    Handle the `list` subcommand.
    Call list_todos() with optional filters.
    Print results in a PrettyTable with columns:
        ID | Title | Priority | Status | Due Date | Created At

    TODO (Person C): Implement this function.
    """
    raise NotImplementedError("Person C: implement cmd_list()")


def cmd_show(args: argparse.Namespace) -> None:
    """
    Handle the `show` subcommand.
    Call get_todo() and print all fields of the todo.
    If not found, print an error message.

    TODO (Person C): Implement this function.
    """
    raise NotImplementedError("Person C: implement cmd_show()")


def cmd_update(args: argparse.Namespace) -> None:
    """
    Handle the `update` subcommand.
    Collect changed fields from args, call update_todo().
    Print success or "Todo #<id> not found".

    TODO (Person C): Implement this function.
    """
    raise NotImplementedError("Person C: implement cmd_update()")


def cmd_delete(args: argparse.Namespace) -> None:
    """
    Handle the `delete` subcommand.
    Call delete_todo() and print success or "Todo #<id> not found".

    TODO (Person C): Implement this function.
    """
    raise NotImplementedError("Person C: implement cmd_delete()")


def main() -> None:
    """
    Entry point: parse args, initialize the DB, dispatch to the right command.

    TODO (Person C): Implement this function.
    Steps:
    1. Build the parser
    2. Parse sys.argv[1:]
    3. Call init_db() to ensure the table exists
    4. Dispatch to cmd_add / cmd_list / cmd_show / cmd_update / cmd_delete
    5. Catch ValueError and print a user-friendly error, then exit with code 1
    """
    raise NotImplementedError("Person C: implement main()")


if __name__ == "__main__":
    main()
