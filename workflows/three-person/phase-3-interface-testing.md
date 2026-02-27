# Phase 3 — CLI Interface & Testing

**Owner:** Person C (Interface Builder & QA)
**Depends on:** Phase 2 merged to `main`
**Output:** A working CLI app and a green test suite, both merged to `main`.

---

## Step-by-Step Instructions

### 1. Get the Latest Code

```bash
git fetch origin
git log origin/main --oneline   # confirm Phase 1 and 2 commits are there
```

### 2. Start Two Branches

You can work on the CLI and tests in parallel (or sequentially — your choice):

```bash
# CLI branch
git switch -c feature/cli-interface origin/main

# Test branch (optional: start now or after CLI is done)
git switch -c feature/tests origin/main
git switch feature/cli-interface   # go back to CLI work first
```

### 3. Understand the Operations Contract

Before writing the CLI, understand what Person B built:

```bash
git log --author="Person B" --oneline
git diff main~5..main -- todo-app/src/operations.py
cat todo-app/src/operations.py
```

### 4. Implement `cli.py`

Work through each handler and commit per command:

```bash
# Implement build_parser()
git commit -m "feat: add argparse setup with all subcommands"

# Implement cmd_add() and cmd_list()
git commit -m "feat: implement add and list commands with prettytable output"

# Implement cmd_show(), cmd_update(), cmd_delete()
git commit -m "feat: implement show, update, and delete commands"

# Implement main() with error handling
git commit -m "feat: add main entry point with ValueError handling"
```

### 5. Manual Smoke Test

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
python todo-app/src/cli.py update --id 2 --priority medium
python todo-app/src/cli.py delete --id 2
python todo-app/src/cli.py list
```

### 6. Stash Practice — Switch to the Tests Branch

```bash
# Save your uncommitted work on CLI branch if any
git stash push -m "WIP: cli error messages"

# Switch to tests branch
git switch feature/tests

# Restore when you return to CLI branch later
# git switch feature/cli-interface
# git stash pop
```

### 7. Implement Tests in `test_todos.py`

Replace every `self.skipTest(...)` with a real implementation.

```bash
# After implementing setUp:
git commit -m "test: set up in-memory database for all test classes"

# After implementing TestAddTodo:
git commit -m "test: add unit tests for add_todo"

# After fixing a bug found by tests — use cherry-pick to bring a fix:
# Imagine you fixed something in operations.py on feature/cli-interface
git log feature/cli-interface --oneline
git cherry-pick <sha-of-the-fix>
git commit -m "fix: cherry-pick input validation fix from cli-interface branch"

# Continue test implementation...
git commit -m "test: add unit tests for list_todos with filters"
git commit -m "test: add unit tests for update_todo and delete_todo"
git commit -m "test: add unit tests for validation functions"
```

### 8. Run the Full Test Suite

```bash
python -m pytest todo-app/tests/ -v
python -m pytest todo-app/tests/ -v --tb=short   # compact traceback
```

All tests must be green before the PR.

### 9. Clean Up History (Interactive Rebase)

```bash
# On feature/cli-interface:
git log --oneline
git rebase -i origin/main
# Squash any "fix typo" or "WIP" commits into their parent

# On feature/tests:
git log --oneline
git rebase -i origin/main
```

### 10. Push Both Branches & Open PRs

```bash
git push -u origin feature/cli-interface
git push -u origin feature/tests
```

Open two PRs:
1. `feature/cli-interface` → `main` (tag Person A and B as reviewers)
2. `feature/tests` → `main` (can piggyback on the same PR or separate)

### 11. Final Integration — After Both PRs Merge

```bash
git switch main
git pull origin main
git log --oneline --graph --all

# Run the full app
python todo-app/src/cli.py add --title "ZenIgnite done!" --priority high
python todo-app/src/cli.py list

# Run ALL tests one final time
python -m pytest todo-app/tests/ -v

# Tag the release
git tag -a v1.0 -m "Release v1.0 — three-person workflow complete"
git push origin v1.0
git tag   # verify the tag exists
```

---

## You're Done!

Run `git log --oneline --graph --all` and take a screenshot of the beautiful branch history for your team. You've just built a real app using real Git collaboration.
