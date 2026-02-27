# Three-Person Workflow — Roles

---

## Person A — Lead / DB Architect

### Responsibilities

- Set up the repository after forking (add `.gitignore`, protect `main` branch in GitHub settings)
- Design the SQLite schema for the `todos` table
- Implement `todo-app/src/database.py` (connection, `init_db`, context manager)
- Implement `todo-app/src/models.py` (the `Todo` dataclass, validators)
- Write a clear PR description so Person B can understand the database contract

### Git Commands You Must Use

| Command | When |
|---------|------|
| `git switch -c feature/db-setup` | Start your branch |
| `git add -p` | Stage changes hunk by hunk |
| `git commit -m "feat: ..."` | Atomic commits per function |
| `git push -u origin feature/db-setup` | Publish branch |
| `git log --oneline` | Review your history before PR |
| `git commit --amend` | Fix a typo in the last commit message |
| `git diff --staged` | Double-check before committing |

### Definition of Done

- [ ] `get_connection()` returns a working `sqlite3.Connection`
- [ ] `init_db()` creates the `todos` table with all required columns
- [ ] `db_connection` context manager commits on success and rolls back on error
- [ ] `Todo.from_row()` correctly maps a database row to a `Todo` object
- [ ] All validators raise `ValueError` with clear messages for invalid input
- [ ] PR created, reviewed, and merged into `main`

---

## Person B — Backend Developer

### Responsibilities

- Wait for Person A's PR to be merged before starting
- Implement all CRUD operations in `todo-app/src/operations.py`
- Each function should be committed separately
- Handle edge cases: empty results, non-existent IDs, invalid filter values

### Git Commands You Must Use

| Command | When |
|---------|------|
| `git fetch origin && git switch -c feature/crud-operations origin/main` | Start your branch from up-to-date main |
| `git rebase main` | If main gets updated while you work |
| `git stash push -m "WIP: update logic"` | When you need to switch context |
| `git stash pop` | Resume work after context switch |
| `git log --author="Person A"` | Review Person A's commits |
| `git diff main..feature/crud-operations` | See all your changes vs main |
| `git log --oneline --graph` | Visualize branch history |

### Definition of Done

- [ ] `add_todo()` validates input and inserts a record, returns new id
- [ ] `get_todo()` returns a `Todo` or `None`
- [ ] `list_todos()` returns all todos, with correct filtering and ordering
- [ ] `update_todo()` updates specified fields and always updates `updated_at`
- [ ] `delete_todo()` removes the record, returns `True`/`False`
- [ ] PR created, reviewed, and merged into `main`

---

## Person C — Interface Builder & QA

### Responsibilities

- Wait for Person B's PR to be merged before starting CLI work
- Implement `todo-app/src/cli.py` with all subcommands
- Implement all unit tests in `todo-app/tests/test_todos.py`
- Ensure all tests pass before the final merge

### Git Commands You Must Use

| Command | When |
|---------|------|
| `git switch -c feature/cli-interface origin/main` | Start CLI branch |
| `git switch -c feature/tests origin/main` | Start test branch (can be parallel) |
| `git rebase -i HEAD~3` | Squash WIP commits before the PR |
| `git cherry-pick <sha>` | Bring a specific fix from another branch |
| `git blame src/operations.py` | Understand what Person B wrote |
| `git revert <sha>` | Undo a commit that broke tests |
| `git tag -a v1.0 -m "..."` | After final merge, create release tag |

### Definition of Done

- [ ] All 8 CLI subcommand handlers are implemented and working
- [ ] `prettytable` used for list/show output
- [ ] All test stubs in `test_todos.py` are replaced with working tests
- [ ] `python -m pytest todo-app/tests/ -v` shows all tests green
- [ ] PR created, reviewed, and merged into `main`
- [ ] `v1.0` tag created and pushed
