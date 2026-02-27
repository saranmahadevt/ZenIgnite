# Phase 1 — Project Setup & Database Layer

**Owner:** Person A (Lead / DB Architect)
**Depends on:** Nothing — this is the very first phase.
**Notify when done:** Person B AND Person D (both can begin work after this merges).

---

## Overview

Person A sets up the repository, designs the SQLite schema, and implements the database connection layer and Todo data model. Everything the rest of the team builds depends on this phase.

---

## Step 1: Fork & Configure the Remote

Only Person A does this. The rest of the team clones Person A's fork.

```bash
# (On GitHub) Fork the ZenIgnite repository to your team's account
# Then clone the fork locally:
git clone https://github.com/<your-team>/ZenIgnite.git
cd ZenIgnite

# Verify the remote
git remote -v

# Add the original repo as "upstream" (good practice)
git remote add upstream https://github.com/saranmahadevt/ZenIgnite.git
git remote -v
```

## Step 2: Configure GitHub Settings

1. In GitHub → Settings → Collaborators: invite Person B, C, and D
2. In GitHub → Settings → Branches → Add a branch protection rule for `main`:
   - ✅ Require pull request reviews before merging (1 approving review)
   - ✅ Dismiss stale pull request approvals when new commits are pushed

## Step 3: Create Your Feature Branch

```bash
git switch -c feature/db-setup
git branch         # confirm you are on the new branch
git status         # should show a clean working tree
```

## Step 4: Implement `database.py`

Open `todo-app/src/database.py` and implement all four TODOs:

- `DB_PATH` — path to the `todos.db` file relative to this file
- `get_connection(db_path)` — returns a `sqlite3.Connection` with `row_factory = sqlite3.Row`
- `init_db(db_path)` — creates the `todos` table using `CREATE TABLE IF NOT EXISTS`
- `db_connection(db_path)` — context manager: yield the connection, commit on success, rollback on exception

**Commit after each function:**
```bash
git diff                          # review what changed
git add -p                        # stage interactively, hunk by hunk
git commit -m "feat: add DB_PATH and get_connection function"

# implement init_db(), then:
git diff --staged                 # review staged changes before committing
git commit -m "feat: add init_db to create todos table"

# implement context manager, then:
git commit -m "feat: add db_connection context manager"
```

## Step 5: Implement `models.py`

Open `todo-app/src/models.py` and implement all TODOs:

- `VALID_PRIORITIES = ["low", "medium", "high"]`
- `VALID_STATUSES = ["pending", "in-progress", "done"]`
- `Todo.from_row(row)` — maps a `sqlite3.Row` to a `Todo` dataclass
- `Todo.__str__()` — human-readable multi-line string
- `validate_priority(priority)` — lowercases and validates; raises `ValueError` if invalid
- `validate_status(status)` — lowercases and validates; raises `ValueError` if invalid
- `validate_due_date(due_date)` — validates `YYYY-MM-DD` format or `None`

```bash
git add -p
git commit -m "feat: add Todo dataclass with from_row and validators"
```

## Step 6: Review Your History

```bash
git log --oneline
# Should show 4 clean commits, for example:
# abc1234 feat: add Todo dataclass with from_row and validators
# def5678 feat: add db_connection context manager
# ghi9012 feat: add init_db to create todos table
# jkl3456 feat: add DB_PATH and get_connection function
```

If you have messy WIP commits, clean them up before opening the PR:
```bash
git rebase -i HEAD~<number-of-commits>
# Use 'squash' or 'fixup' to combine related commits
```

## Step 7: Amend Practice

Fix a typo or improve the wording of your last commit message:
```bash
git commit --amend -m "feat: add Todo dataclass with from_row, __str__, and validators"
git log --oneline   # verify the updated message
```

## Step 8: Push & Open a Pull Request

```bash
git push -u origin feature/db-setup
```

On GitHub:
- Open a PR: `feature/db-setup` → `main`
- Title: `feat: add database connection layer and Todo model`
- Description: explain the DB schema columns and what Person B and D need to know

## Step 9: Review

Person B should review the PR:
```bash
git fetch origin
git checkout feature/db-setup
# Read all code, leave comments on GitHub if needed, then approve
```

## Step 10: Merge

Once approved, Person A merges using **Squash and merge** or **Rebase and merge**.

```bash
# After merging on GitHub:
git switch main
git pull origin main
git log --oneline   # verify your commits are on main
```

## Step 11: Tag the Schema Milestone

```bash
git tag -a v0.1 -m "DB schema and data model ready — team can now build on top of this"
git push origin v0.1
git tag             # verify the tag exists
```

---

## Git Commands Used in This Phase

| Command | Purpose |
|---------|---------|
| `git clone` | Copy the remote repository |
| `git remote add` | Add upstream remote |
| `git remote -v` | Verify remotes |
| `git switch -c` | Create and switch to feature branch |
| `git add -p` | Stage changes hunk by hunk |
| `git diff` | Review unstaged changes |
| `git diff --staged` | Review staged changes before committing |
| `git commit -m` | Create an atomic commit |
| `git commit --amend` | Fix the last commit message |
| `git rebase -i` | Clean up commit history before PR |
| `git log --oneline` | Review branch history |
| `git push -u` | Publish branch with tracking |
| `git tag -a` | Create annotated tag |
| `git push origin v0.1` | Push tag to remote |

---

## Checkpoint

Notify the team in your group chat:
- ✅ Person B: _"Phase 1 merged. You can now start `feature/crud-operations`."_
- ✅ Person D: _"Phase 1 merged. You can now create `feature/tests` and start with `TestValidation`."_
- Paste the output of `git log --oneline --graph --all` so everyone can see the current state.
