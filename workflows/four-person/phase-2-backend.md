# Phase 2 — CRUD Operations (Backend)

**Owner:** Person B (Backend Developer)
**Depends on:** Phase 1 merged to `main`
**Notify when done:** Person C AND Person D.

---

## Overview

Person B implements all five CRUD functions in `operations.py`. This is the core business logic layer that both the CLI (Person C) and the test suite (Person D) depend on. Push your branch early and often so Person D can track your progress in parallel.

---

## Step 1: Get the Latest Code

```bash
git fetch origin
git log origin/main --oneline   # confirm Person A's commits are visible
git switch -c feature/crud-operations origin/main
git branch   # confirm you are on the new branch
```

## Step 2: Study Person A's Work

Before writing any code, understand what was built:

```bash
cat todo-app/src/database.py     # understand get_connection, init_db, db_connection
cat todo-app/src/models.py       # understand Todo, VALID_PRIORITIES, validators

# Use git blame to see which commit introduced each piece
git blame todo-app/src/database.py
git blame todo-app/src/models.py

# See all changes Person A made
git diff main~4..main -- todo-app/src/
```

## Step 3: Coordinate with Person D

Person D will write tests in parallel. Communicate your function signatures before you implement them so they can start `TestAddTodo` while you work on `list_todos`:

```bash
# Push early, even before functions are complete
git push -u origin feature/crud-operations

# Person D can then watch your progress:
# git fetch origin && git log origin/feature/crud-operations --oneline
```

## Step 4: Implement `operations.py` — One Function Per Commit

### 4a. `add_todo()`

Validates title (not empty, max 100 chars), priority, and due_date. Inserts the record with `created_at` and `updated_at` set to the current UTC time. Returns the new row's `id`.

```bash
git add todo-app/src/operations.py
git diff --staged     # review before committing
git commit -m "feat: implement add_todo with input validation"
git push              # notify Person D — they can now write TestAddTodo
```

### 4b. `get_todo(todo_id)`

Returns a `Todo` object for the given id, or `None` if not found.

```bash
git commit -am "feat: implement get_todo returning Todo or None"
```

### 4c. `list_todos(status, priority)`

Returns all todos matching the optional filters, ordered by priority (high → medium → low) then `created_at` descending.

```bash
git commit -am "feat: implement list_todos with optional status and priority filters"
git push   # Person D can now write TestListTodos
```

### 4d. `update_todo(todo_id, **kwargs)`

Dynamically updates only the provided fields. Always updates `updated_at`. Returns `True` if updated, `False` if id not found. Raises `ValueError` for unknown fields or invalid values.

```bash
git commit -am "feat: implement update_todo with dynamic SET and validation"
```

### 4e. `delete_todo(todo_id)`

Removes the record. Returns `True` if deleted, `False` if not found.

```bash
git commit -am "feat: implement delete_todo returning True/False"
git push   # Person D can now complete the full test suite
```

## Step 5: Simulate a Bug and Practice `git bisect`

Intentionally introduce a bug in one commit to practice finding it later:

```bash
# Step 1: You already have a working add_todo commit
# Step 2: Make the next commit introduce a bug (e.g., return None instead of lastrowid)
echo "# bad change" >> todo-app/src/operations.py
git commit -am "bug: simulate bad commit"

# Step 3: Make one more normal commit on top
echo "# normal" >> todo-app/src/operations.py
git commit -am "chore: normal commit after bug"

# Step 4: Use bisect to find the bad commit
git bisect start
git bisect bad                   # current HEAD is broken
git bisect good feature/crud-operations~3   # three commits ago was fine
# Git checks out the midpoint — test it manually, then:
git bisect bad    # or git bisect good
git bisect reset  # done — returns to HEAD

# Step 5: Fix the bug using revert or reset
git revert <bad-commit-sha>
# or:
git reset --soft HEAD~2   # undo the last 2 commits, keep changes staged
# fix it properly, then:
git commit -m "feat: implement add_todo corrected"
```

## Step 6: Simulate a Context Switch with Stash

```bash
# You're in the middle of update_todo but need to check something on main
git stash push -m "WIP: half-done update_todo dynamic SET"
git stash list

git switch main
git log --oneline    # check what Person A tagged

git switch feature/crud-operations
git stash pop
git stash list       # confirm stash is consumed
```

## Step 7: Stay Current with Main

```bash
git fetch origin
git rebase origin/main
# If conflicts: resolve, then git add, then git rebase --continue
```

## Step 8: Track Changes for Only This File

```bash
git log --oneline -- todo-app/src/operations.py     # commits touching this file
git log --stat                                       # files changed per commit
git diff origin/main..feature/crud-operations       # everything you added
```

## Step 9: Clean Up and Open a Pull Request

```bash
git log --oneline    # review all your commits
git rebase -i origin/main
# Squash any fixup/WIP commits — make sure each commit represents one complete function

git push origin feature/crud-operations   # or --force-with-lease if rebased
```

On GitHub:
- PR: `feature/crud-operations` → `main`
- Title: `feat: implement all five CRUD operations`
- Tag Person A as reviewer; add Person D as observer (they can comment on the `operations.py` interface)

## Step 10: Merge

After approval, merge the PR.

```bash
git switch main
git pull origin main
git log --oneline --graph --all
```

---

## Git Commands Used in This Phase

| Command | Purpose |
|---------|---------|
| `git fetch origin` | Sync all remote branches locally |
| `git switch -c ... origin/main` | Start branch from latest remote main |
| `git blame` | See who wrote each line |
| `git diff --staged` | Review before committing |
| `git push -u` | Publish with tracking |
| `git push` | Push new commits |
| `git stash push -m` | Save WIP with a label |
| `git stash pop` | Restore WIP |
| `git stash list` | List all stashes |
| `git bisect start/bad/good/reset` | Binary search for a bad commit |
| `git revert` | Safely undo a commit |
| `git reset --soft` | Undo commits keeping changes staged |
| `git rebase origin/main` | Keep branch current with main |
| `git rebase -i` | Interactive history cleanup |
| `git log --stat` | Show files changed per commit |
| `git log --oneline -- <file>` | Log limited to one file |

---

## Checkpoint

Notify your team:
- ✅ Person C: _"Phase 2 merged. You can now start `feature/cli-interface`."_
- ✅ Person D: _"Phase 2 merged. Full CRUD is available — you can now complete `TestUpdateTodo` and `TestDeleteTodo`."_

---

## Coordination with Person D (Parallel Testing)

Person D will be writing tests **while you implement operations**. Agree on the function signatures early:

```bash
# Person B: after implementing add_todo, notify Person D
# Person D can then implement TestAddTodo while you work on list_todos

# Good practice: push early even if incomplete
git push -u origin feature/crud-operations
# Person D can follow your progress with:
# git fetch origin && git log origin/feature/crud-operations --oneline
```

---

## Additional Git Commands for This Phase

### Use `git bisect` for Practice

Intentionally introduce a bug in a local commit, then find it with bisect:

```bash
# Step 1: Make one commit that works correctly
git commit -m "feat: implement add_todo"

# Step 2: Introduce a bug in the next commit (simulate a mistake)
# e.g., return None instead of the inserted id

# Step 3: Practice bisect
git bisect start
git bisect bad                  # current HEAD is broken
git bisect good HEAD~2          # 2 commits ago was fine
# Git will checkout commits — test each, then:
git bisect good   # or git bisect bad
# Find the culprit, then:
git bisect reset

# Step 4: Fix the bug with a proper commit
git revert <bad-sha>
# or
git reset --soft HEAD~1
# fix it, then re-commit
```

### Use `git log` to Track Progress

```bash
git log --oneline --graph --all
git log --stat                        # shows which files changed per commit
git log --oneline -- todo-app/src/operations.py   # only commits affecting this file
```

---

## Definition of Done

- [ ] All 5 CRUD functions implemented
- [ ] Person D can run `add_todo`, `list_todos`, `get_todo` manually in their test setUp
- [ ] PR reviewed by Person A (and ideally Person D)
- [ ] PR merged into `main`

---

## Checkpoint

Notify:
- ✅ Person C: _"Phase 2 merged. Start feature/cli-interface."_
- ✅ Person D: _"Phase 2 merged. You now have full CRUD to test against."_
