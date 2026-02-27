# Phase 1 — Project Setup & Database Layer

**Owner:** Person A (Lead / DB Architect)
**Depends on:** Nothing — this is the first phase.
**Output:** A merged PR that gives Person B a working database and data model.

---

## Step-by-Step Instructions

### 1. Fork & Configure the Remote

Only Person A does this. The rest of the team clones Person A's fork.

```bash
# (On GitHub) Fork the ZenIgnite repository to your team's account
# Then clone the fork locally:
git clone https://github.com/<your-team>/ZenIgnite.git
cd ZenIgnite

# Verify the remote
git remote -v

# Add the original repo as "upstream" (optional but good practice)
git remote add upstream https://github.com/saranmahadevt/ZenIgnite.git
git remote -v
```

### 2. Protect the Main Branch

In GitHub → Settings → Branches → Add rule for `main`:
- ✅ Require pull request reviews before merging (1 reviewer)
- ✅ Require linear history (optional but good practice)

### 3. Create Your Feature Branch

```bash
git switch -c feature/db-setup
git branch         # confirm you're on the new branch
git status         # should show clean working tree
```

### 4. Implement `database.py`

Open `todo-app/src/database.py` and implement:
- `DB_PATH` — path to `todos.db` file
- `get_connection(db_path)` — returns sqlite3.Connection with row_factory
- `init_db(db_path)` — creates the todos table
- `db_connection(db_path)` — context manager

**Commit after each function:**
```bash
git diff                          # see what changed
git add -p                        # stage interactively
git commit -m "feat: add DB_PATH and get_connection function"

# implement init_db(), then:
git diff --staged                 # review before commit
git commit -m "feat: add init_db to create todos table"

# implement context manager, then:
git commit -m "feat: add db_connection context manager"
```

### 5. Implement `models.py`

Open `todo-app/src/models.py` and implement all TODOs.

```bash
git add -p
git commit -m "feat: add Todo dataclass with from_row and validators"
```

### 6. Review Your History

```bash
git log --oneline
# Should show 4 clean commits:
# abc1234 feat: add Todo dataclass with from_row and validators
# def5678 feat: add db_connection context manager
# ghi9012 feat: add init_db to create todos table
# jkl3456 feat: add DB_PATH and get_connection function
```

If you have messy WIP commits, clean them up:
```bash
git rebase -i HEAD~<number-of-commits>
# Use 'squash' or 'fixup' to combine them
```

### 7. Push & Open a Pull Request

```bash
git push -u origin feature/db-setup
```

Then on GitHub:
- Open a Pull Request: `feature/db-setup` → `main`
- Title: `feat: add database connection and Todo model`
- Description: List what you implemented and what Person B needs to know about the DB contract

### 8. Person B Reviews the PR

Person B should:
```bash
git fetch origin
git checkout feature/db-setup
# Read the code, leave comments on GitHub, then approve
```

### 9. Merge

Once approved, Person A merges the PR using **"Squash and merge"** or **"Rebase and merge"** (not "Create a merge commit" unless you want the graph to show the merge node).

```bash
# Person A, after merging on GitHub:
git switch main
git pull origin main
git log --oneline   # verify your commits are visible on main
```

---

## Checkpoint

Notify Person B: _"Phase 1 merged. You can now start Phase 2."_

```bash
# Person B runs:
git fetch origin
git log origin/main --oneline   # should see Person A's commits
```
