# Phase 3 — CLI Interface & Tests (Parallel Work)

This phase runs in **parallel**. Person C builds the CLI interface while Person D writes the full test suite at the same time. Both work on separate branches and merge independently via PRs.

---

## Person C — CLI Interface

**Branch:** `feature/cli-interface`
**Depends on:** Phase 2 merged to `main`

---

### Step 1: Start Your Branch

```bash
git fetch origin
git log origin/main --oneline    # confirm Phase 1 and 2 commits are visible
git switch -c feature/cli-interface origin/main
```

### Step 2: Study Person B's Work Before Writing Anything

```bash
cat todo-app/src/operations.py
git blame todo-app/src/operations.py        # understand the author of each line
git log --author="Person B" --oneline       # review their commits
git diff origin/main~5..origin/main -- todo-app/src/operations.py
```

### Step 3: Implement `cli.py` — Commit Per Subcommand Group

**3a. Parser setup:**
- Use `argparse` with a top-level `ArgumentParser` and `add_subparsers`
- Subcommands: `add`, `list`, `show`, `update`, `delete`
- Argument specs: see `todo-app/README.md` for full field list

```bash
git commit -m "feat: add argparse setup with all CLI subcommands"
```

**3b. `cmd_add()` and `cmd_list()`:**
- `cmd_add`: calls `add_todo()`, prints `✓ Todo #<id> created: '<title>'`
- `cmd_list`: calls `list_todos()`, renders a `PrettyTable` with columns: ID, Title, Priority, Status, Due Date, Created

```bash
git commit -m "feat: implement add and list commands with prettytable output"
```

**3c. `cmd_show()`, `cmd_update()`, `cmd_delete()`:**
- `cmd_show`: calls `get_todo()`, prints all fields; exits with error if not found
- `cmd_update`: collects only the provided kwargs, calls `update_todo()`
- `cmd_delete`: calls `delete_todo()`, prints success or not-found message

```bash
git commit -m "feat: implement show, update, and delete commands"
```

**3d. `main()` entry point:**
- Build parser, parse args, call `init_db()`, dispatch to the right handler
- Wrap the dispatch in `try/except ValueError` and print a clean error + `sys.exit(1)`

```bash
git commit -m "feat: add main entry point with init_db and error handling"
```

### Step 4: Manual Smoke Test

```bash
cd ZenIgnite
python todo-app/src/cli.py --help
python todo-app/src/cli.py add --title "Buy milk" --priority high --due 2026-03-15
python todo-app/src/cli.py add --title "Read a book" --priority low
python todo-app/src/cli.py list
python todo-app/src/cli.py list --status pending
python todo-app/src/cli.py list --priority high
python todo-app/src/cli.py show --id 1
python todo-app/src/cli.py update --id 1 --status in-progress
python todo-app/src/cli.py delete --id 2
python todo-app/src/cli.py list
```

### Step 5: Practice Stash (Context Switch)

```bash
# Mid-work — need to check something on main
git stash push -m "WIP: error message formatting in cmd_update"
git switch main
git log --oneline       # review the state of main
git switch feature/cli-interface
git stash pop
```

### Step 6: Stay Current with Main

If Person D's tests exposed a bug in Phase 2 that got fixed and merged:
```bash
git fetch origin
git rebase origin/main      # pick up the fix
# resolve conflicts if any, then: git rebase --continue
```

Bring a specific fix commit directly without a full rebase:
```bash
git log origin/main --oneline    # find the fix SHA
git cherry-pick <fix-sha>
```

### Step 7: Review Line-by-Line Before the PR

```bash
git diff --word-diff HEAD~1     # per-word diff of last commit
git diff origin/main..HEAD      # everything your branch adds
git diff --staged               # before each commit
```

### Step 8: Clean Up History and Open PR

```bash
git log --oneline
git rebase -i origin/main       # squash WIP/fixup commits
git push -u origin feature/cli-interface   # or --force-with-lease after rebase
```

On GitHub:
- PR: `feature/cli-interface` → `main`
- Tag Person A and Person B as reviewers
- Add Person D as reviewer — they will verify the CLI matches what the tests expect

---

---

## Person D — Test Suite

**Branch:** `feature/tests`
**Stage 1:** Can start after Phase 1 merges (validation tests).
**Stage 2:** Full CRUD tests after Phase 2 merges.

---

### Stage 1: After Phase 1 — Start Immediately with Validation Tests

```bash
git fetch origin
git switch -c feature/tests origin/main
git push -u origin feature/tests      # publish early so the team sees your progress
```

Open `todo-app/tests/test_todos.py` and implement `TestValidation`:
- `setUp()`: override `database.DB_PATH` with the path to a temp file, call `init_db()`
- `tearDown()`: delete the temp file
- Implement all 7 validation test methods

```bash
git commit -m "test: configure temp-file DB for isolated tests (setUp/tearDown)"
git commit -m "test: implement TestValidation — priority, status, due_date"
git push
```

### Stage 2: After Phase 2 — Complete CRUD Tests

```bash
git fetch origin
git rebase origin/main    # pull in Person B's CRUD code
```

Implement test classes in order:
```bash
git commit -m "test: implement TestAddTodo — valid, all-fields, invalid inputs"
git push    # Person B can see your tests pass against their code

git commit -m "test: implement TestGetTodo and TestListTodos with filters"
git commit -m "test: implement TestUpdateTodo — field updates, updated_at, invalid"
git commit -m "test: implement TestDeleteTodo — delete, not-found"
git push
```

### Finding Bugs During Testing

If a test reveals a bug in `operations.py`:

```bash
# Option 1: Person B fixes it on their branch and merges to main
git fetch origin && git rebase origin/main   # pull the fix

# Option 2: You fix it yourself and propose it via your PR
# Fix the bug in operations.py on your branch
git commit -m "fix: correct missing-id handling in delete_todo"
# Note it in your PR description so Person B is aware
```

Find where a function was introduced:
```bash
git log -S "delete_todo"                    # find commits mentioning this string
git blame todo-app/src/operations.py        # see who wrote each line
```

### Practice `git bisect` to Find a Regression

```bash
git bisect start
git bisect bad                              # current HEAD has the failing test
git bisect good origin/main                 # main before Phase 2 was fine
# Git checks out commits — run pytest each time
python -m pytest todo-app/tests/ -k "TestDeleteTodo" --tb=short
git bisect bad    # or git bisect good
git bisect reset
```

### Practice `git reflog` Recovery

```bash
# Simulate: accidentally do a hard reset
git reset --hard HEAD~3    # oops — three test commits lost!

# Recover using reflog
git reflog                               # find HEAD@{n} before the reset
git reset --hard HEAD@{3}               # restore to where you were
git log --oneline                        # your commits are back
```

### Run Tests Constantly

```bash
python -m pytest todo-app/tests/ -v
python -m pytest todo-app/tests/ -k "TestAddTodo" -v      # single class
python -m pytest todo-app/tests/ --tb=short               # compact tracebacks
```

### Clean Up and Open PR

```bash
git rebase -i origin/main      # squash WIP commits
git log --oneline
git push origin feature/tests  # or --force-with-lease after rebase
```

On GitHub:
- PR: `feature/tests` → `main`
- Tag Person A and Person B as reviewers
- Person C should also review — confirm that what the tests assert matches CLI output

---

## Git Commands Used in Phase 3

| Person | Command | Purpose |
|--------|---------|---------|
| C | `git cherry-pick` | Bring a specific fix from another branch |
| C | `git diff --word-diff` | Review per-word changes |
| C | `git rebase origin/main` | Stay current |
| C | `git rebase -i` | Squash WIP commits |
| C | `git stash` / `git stash pop` | Context switching |
| D | `git bisect` | Locate the commit that broke a test |
| D | `git reflog` | Recover from a bad reset |
| D | `git log -S` | Search commits by content |
| D | `git blame` | Find who wrote what |
| D | `git revert` | Undo a commit safely |
| D | `git push --force-with-lease` | Push after rebase safely |

---

## Reviews

- Person C reviews Person D's PR (and vice versa)
- Person A reviews both
- At least 1 approval required before each merge

Merge order: Either order is fine — CLI and tests are independent.


### Additional Commands for Person C

```bash
# Stay current with main as Person D's tests might expose bugs that get fixed
git fetch origin
git rebase origin/main

# If Person D finds a bug in operations.py and it gets merged to main,
# use cherry-pick to bring that fix to your branch too if needed:
git cherry-pick <sha-of-fix>

# Use word-diff to review small changes
git diff --word-diff HEAD~1

# Before PR: interactive rebase to produce clean history
git rebase -i origin/main
```

---

## Person D — Test Suite

**Branch:** `feature/tests`
**Can start after:** Phase 1 merged (for validation tests). Full tests after Phase 2 merged.

### Step-by-Step

#### Stage 1: After Phase 1 (write validation tests immediately)

```bash
git fetch origin
git switch -c feature/tests origin/main
```

Implement `TestValidation` in `test_todos.py`:
```bash
git commit -m "test: implement TestValidation for priority, status, due_date"
```

Push early so the team sees your progress:
```bash
git push -u origin feature/tests
```

#### Stage 2: After Phase 2 (write CRUD tests)

```bash
git fetch origin
git rebase origin/main   # pick up Person B's CRUD code
```

Implement `setUp()` using `:memory:`:
```bash
git commit -m "test: configure in-memory DB for all test classes"
```

Implement each test class:
```bash
git commit -m "test: implement TestAddTodo"
git commit -m "test: implement TestGetTodo and TestListTodos"
git commit -m "test: implement TestUpdateTodo and TestDeleteTodo"
```

#### Stage 3: Handle a Bug Found During Testing

If a test reveals a bug in Person B's `operations.py`:

```bash
# Option 1: Person B fixes it on main, then you pull the fix
git fetch origin && git rebase origin/main

# Option 2: You fix it yourself on your branch, then cherry-pick to main
# Fix the bug in operations.py on feature/tests
git commit -m "fix: correct null return in delete_todo for missing id"
# Open a PR or ask Person B to cherry-pick your fix commit

# Practice: identify which commit broke something with bisect
git bisect start
git bisect bad
git bisect good origin/main
# ... test each checkout ...
git bisect reset
```

#### Stage 4: Use `git reflog` to Recover Work

```bash
# Simulate: you accidentally do a hard reset
git reset --hard HEAD~3   # oops!

# Recover using reflog
git reflog
git reset --hard HEAD@{1}  # go back to before the mistake
```

#### Run Tests Constantly

```bash
python -m pytest todo-app/tests/ -v
python -m pytest todo-app/tests/ -k "TestAddTodo" -v   # run only one class
python -m pytest todo-app/tests/ --tb=short            # compact tracebacks
```

#### Clean History and Open PR

```bash
git rebase -i origin/main   # squash WIP commits
git log --oneline
git push origin feature/tests
```

---

## Reviews

- Person C reviews Person D's PR (and vice versa)
- Person A reviews both
- At least 1 approval required before merge

Merge order: Either order is fine — tests and CLI are independent.
