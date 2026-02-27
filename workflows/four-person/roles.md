# Four-Person Workflow — Roles

---

## Person A — Lead / DB Architect

### Responsibilities

- Fork the repository and invite Person B, C, and D as collaborators
- Set up branch protection rules on GitHub for the team of 4
- Design the SQLite schema for the `todos` table
- Implement `todo-app/src/database.py` (connection, `init_db`, context manager)
- Implement `todo-app/src/models.py` (the `Todo` dataclass, all validators)
- Communicate the database schema and `Todo` model to **both Person B and Person D** so they can start planning
- Create a `v0.1` tag after merging so Person D can begin test stubs early

### Git Commands You Must Use

| Command | When |
|---------|------|
| `git switch -c feature/db-setup` | Start your branch |
| `git add -p` | Stage changes hunk by hunk |
| `git commit -m "feat: ..."` | Atomic commits |
| `git push -u origin feature/db-setup` | Publish branch |
| `git log --oneline --graph --all` | Visualize history |
| `git commit --amend --no-edit` | Fix last commit without changing message |
| `git tag -a v0.1 -m "DB schema ready"` | Mark the schema milestone |

### Definition of Done

- [ ] `get_connection()` returns a working `sqlite3.Connection`
- [ ] `init_db()` creates the `todos` table
- [ ] `db_connection` context manager works
- [ ] `Todo.from_row()` works
- [ ] All validators raise `ValueError` for invalid input
- [ ] PR merged into `main`

---

## Person B — Backend Developer

### Responsibilities

- Wait for Person A's PR to be merged before starting work
- Implement all five CRUD operations in `todo-app/src/operations.py`
- Commit each function separately for a clean, reviewable history
- Share function signatures clearly with **Person C** (they call your code from the CLI)
- Share return types and error behaviour with **Person D** (they write tests against your code)
- Push your branch early so Person D can monitor progress with `git fetch`

### Git Commands You Must Use

| Command | When |
|---------|------|
| `git fetch origin && git switch -c feature/crud-operations origin/main` | Start from up-to-date main |
| `git rebase main` | Stay current |
| `git stash` / `git stash pop` | Context switching |
| `git log --oneline --format="%h %s" -- todo-app/src/operations.py` | Log for one file |
| `git diff origin/main..HEAD` | See all your changes |
| `git bisect` | Practice locating a introduced bug |

### Definition of Done

- [ ] All 5 CRUD functions implemented and manually tested
- [ ] PR merged into `main`

---

## Person C — Interface Builder

### Responsibilities

- Build the full CLI using `argparse` and `prettytable`
- Coordinate with Person D to agree on expected output format for tests
- Use `git cherry-pick` to bring any shared helpers from Person B's branch if needed

### Git Commands You Must Use

| Command | When |
|---------|------|
| `git switch -c feature/cli-interface origin/main` | Start after Phase 2 merges |
| `git rebase -i HEAD~<n>` | Squash WIP commits before PR |
| `git stash push -m "WIP: ..."` | Pause mid-feature |
| `git cherry-pick <sha>` | Bring a specific fix |
| `git log --oneline --graph` | Review history |
| `git blame todo-app/src/operations.py` | Understand Person B's code |
| `git diff --word-diff` | Per-word diff for small changes |

### Definition of Done

- [ ] All CLI subcommands implemented
- [ ] `prettytable` output looks clean for `list` and `show`
- [ ] Errors handled with clear messages
- [ ] PR merged into `main`

---

## Person D — QA & Release Engineer

### Responsibilities

This is the most Git-intensive role:
- Can start writing test stubs **after Phase 1** (the model is known)
- Writes the full test suite in `tests/test_todos.py`
- After all features merge: performs final QA, updates docs, creates the release tag
- Acts as the **primary reviewer** on all PRs (4+ reviews across the project)

### Git Commands You Must Use

| Command | When |
|---------|------|
| `git switch -c feature/tests origin/main` | Start after Phase 1 |
| `git fetch origin && git rebase origin/main` | Keep up with team merges |
| `git log --all --oneline --graph` | Monitor team progress |
| `git cherry-pick <sha>` | Pull a bug fix into tests branch |
| `git revert <sha>` | Undo a bad commit |
| `git log -S "validate_priority"` | Find where a function was introduced |
| `git blame todo-app/src/operations.py` | Find who owns which line |
| `git bisect` | Find the commit that broke a test |
| `git reflog` | Recover a lost commit |
| `git tag -a v1.0 -m "..."` | Create the release tag |
| `git push origin --tags` | Publish the release tag |
| `git switch -c release/v1.0` | Create release branch for final prep |

### Definition of Done

- [ ] All test stubs replaced with working tests
- [ ] `python -m pytest todo-app/tests/ -v` is all green
- [ ] All 4 team members' PRs reviewed (at least 1 review each)
- [ ] `CHANGELOG.md` updated (or release notes written in the PR)
- [ ] `v1.0` tag created and pushed
- [ ] Final `git log --oneline --graph --all` screenshot taken
