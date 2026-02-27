# Phase 2 — CRUD Operations

**Owner:** Person B (Backend Developer)
**Depends on:** Phase 1 merged to `main`
**Output:** A merged PR with all five CRUD functions working correctly.

---

## Step-by-Step Instructions

### 1. Get the Latest Code

```bash
git fetch origin
git log origin/main --oneline   # verify Person A's commits are there
git switch -c feature/crud-operations origin/main
git branch   # confirm you're on the new branch
```

### 2. Verify the Database Layer Works

Before writing any code, check what Person A built:

```bash
# Read operations.py to understand the contract
cat todo-app/src/database.py
cat todo-app/src/models.py

# Use git blame to see who wrote what
git blame todo-app/src/database.py

# Compare your branch with main to confirm you have the latest
git diff main..feature/crud-operations
```

### 3. Implement `operations.py` — One Function at a Time

Work through each function and commit after each one:

#### 3a. `add_todo()`

```bash
# Implement add_todo() in operations.py
git add todo-app/src/operations.py
git diff --staged         # review before committing
git commit -m "feat: implement add_todo with validation"
```

#### 3b. `get_todo()`

```bash
# Implement get_todo()
git commit -m "feat: implement get_todo by id"
```

#### 3c. `list_todos()`

```bash
# Implement list_todos() with optional filters
git commit -m "feat: implement list_todos with status and priority filters"
```

#### 3d. `update_todo()`

```bash
# Implement update_todo() with dynamic field updates
git commit -m "feat: implement update_todo with dynamic field update"
```

#### 3e. `delete_todo()`

```bash
# Implement delete_todo()
git commit -m "feat: implement delete_todo"
```

### 4. Quick Manual Test

```python
# Create a quick test script (do NOT commit this — add it to .gitignore or delete after)
# test_manual.py
import sys
sys.path.insert(0, "todo-app/src")
from database import init_db
from operations import add_todo, list_todos, update_todo, delete_todo

init_db()
new_id = add_todo("Test task", priority="high")
print("Added id:", new_id)
todos = list_todos()
print("All todos:", todos)
update_todo(new_id, status="in-progress")
todos = list_todos(status="in-progress")
print("In-progress:", todos)
delete_todo(new_id)
print("Deleted. List now:", list_todos())
```

```bash
python test_manual.py
# Clean up:
del test_manual.py   # Windows
git status           # confirm nothing untracked is present
```

### 5. Handle a Simulated Interruption (Git Stash Practice)

Imagine you receive a request to look at something else mid-work:

```bash
# Simulate: you've made changes but need to switch branches temporarily
git stash push -m "WIP: half-done error handling in update_todo"
git stash list

# Switch to main to check something
git switch main
git log --oneline
git switch feature/crud-operations

# Restore your work
git stash pop
git stash list   # stash should be gone
```

### 6. Sync with Main (if main has changed)

```bash
git fetch origin
git rebase origin/main
# If conflicts:
# 1. Resolve them in your editor
# 2. git add <conflicted-file>
# 3. git rebase --continue
```

### 7. Review Your History Before the PR

```bash
git log --oneline
git log --oneline --graph
git diff main..feature/crud-operations   # see everything you added
```

If you have any fixup commits, clean them up:
```bash
git rebase -i origin/main
```

### 8. Push & Open a Pull Request

```bash
git push -u origin feature/crud-operations
```

On GitHub:
- PR: `feature/crud-operations` → `main`
- Title: `feat: implement all CRUD operations for todos`
- Tag Person A as reviewer

### 9. Merge

After approval, merge the PR.

```bash
# After merging on GitHub:
git switch main
git pull origin main
git log --oneline --graph --all
```

---

## Checkpoint

Notify Person C: _"Phase 2 merged. You can now implement the CLI and tests."_
