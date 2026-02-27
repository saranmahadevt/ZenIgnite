# Merge Conflict Resolution Lab

> Merge conflicts are not errors — they are Git asking you to make a decision. This lab teaches you to create and resolve them confidently.

---

## Understanding a Conflict

When two branches modify the **same lines** of the same file, Git cannot automatically decide which version to keep. It marks the conflict in the file:

```
<<<<<<< HEAD
    Your version of the line
=======
    Their version of the line
>>>>>>> feature/other-branch
```

- `<<<<<<< HEAD` — everything below is YOUR current branch's version
- `=======` — separator
- `>>>>>>> feature/other-branch` — everything above is the INCOMING branch's version

Your job: edit the file to keep the **correct** version (or combine both), remove the conflict markers, stage the file, and complete the merge/rebase.

---

## Lab 1 — Basic Merge Conflict

**Goal:** Create a conflict, recognize it, resolve it, and complete the merge.

### Setup

```bash
git switch main
git switch -c conflict/lab1-branch-a

# Edit the VALID_PRIORITIES line in models.py
# Change:  VALID_PRIORITIES = []
# To:      VALID_PRIORITIES = ["low", "medium", "high"]
git add todo-app/src/models.py
git commit -m "feat: fill in VALID_PRIORITIES on branch-a"

# Now simulate another person doing the same thing differently
git switch main
git switch -c conflict/lab1-branch-b

# Edit the SAME line differently:
# Change:  VALID_PRIORITIES = []
# To:      VALID_PRIORITIES = ["low", "normal", "high", "critical"]
git add todo-app/src/models.py
git commit -m "feat: fill in VALID_PRIORITIES on branch-b (different values)"
```

### Trigger the Conflict

```bash
# Merge branch-a into main first
git switch main
git merge conflict/lab1-branch-a

# Now try to merge branch-b — this will conflict
git merge conflict/lab1-branch-b
```

### Resolve the Conflict

```bash
# See which files conflict
git status
# You'll see: both modified: todo-app/src/models.py

# Open the file and find the conflict markers
# The file will look like:
# <<<<<<< HEAD
# VALID_PRIORITIES = ["low", "medium", "high"]
# =======
# VALID_PRIORITIES = ["low", "normal", "high", "critical"]
# >>>>>>> conflict/lab1-branch-b

# Decide: keep branch-a's version (correct values for this project)
# Edit the file to:
# VALID_PRIORITIES = ["low", "medium", "high"]
# (remove all conflict markers)

# Stage the resolved file
git add todo-app/src/models.py

# Check status — should say "All conflicts fixed but you are still merging"
git status

# Complete the merge
git commit -m "merge: resolve VALID_PRIORITIES conflict, keep low/medium/high"
```

### Verify

```bash
git log --oneline --graph
git show HEAD    # verify the merge commit and final content
```

### Cleanup

```bash
git branch -d conflict/lab1-branch-a conflict/lab1-branch-b
```

---

## Lab 2 — Rebase Conflict

**Goal:** Experience a conflict during rebase and resolve it.

Rebase conflicts work the same way as merge conflicts, but you resolve them commit-by-commit instead of all at once.

### Setup

```bash
git switch main

# Commit a change to main
# Edit todo-app/src/models.py: change VALID_STATUSES = [] to:
# VALID_STATUSES = ["pending", "in-progress", "done"]
git commit -am "feat: fill in VALID_STATUSES on main"

# Now create a branch from 1 commit BEFORE that change
git switch -c conflict/lab2-rebase HEAD~1

# Make a different change to the same line
# Change VALID_STATUSES = [] to:
# VALID_STATUSES = ["todo", "doing", "done"]
git commit -am "feat: fill in VALID_STATUSES with different names"
```

### Trigger the Conflict

```bash
# Rebase our branch on top of main
git rebase main
# Conflict! Git stops at the conflicting commit
```

### Resolve During Rebase

```bash
# See the conflict
git status
# "both modified: todo-app/src/models.py"

# Open the file — same conflict markers as before
# <<<<<<< HEAD (this is main's version during rebase)
# VALID_STATUSES = ["pending", "in-progress", "done"]
# =======
# VALID_STATUSES = ["todo", "doing", "done"]
# >>>>>>> <commit-sha> (feat: fill in VALID_STATUSES with different names)

# Resolve: choose the canonical values
# VALID_STATUSES = ["pending", "in-progress", "done"]

# Stage the resolved file
git add todo-app/src/models.py

# Continue the rebase (do NOT git commit — just continue)
git rebase --continue

# Git may ask you to confirm/edit the commit message — save and close

# Check the result
git log --oneline --graph --all
```

### Abort Option

If things go wrong at any point during a rebase:
```bash
git rebase --abort    # returns to pre-rebase state as if nothing happened
```

### Cleanup

```bash
git switch main
git branch -D conflict/lab2-rebase
```

---

## Lab 3 — Three-Way Conflict (Team Simulation)

**Goal:** Simulate two teammates editing the same lines, resolve it during a team PR review.

This lab requires **two people** (or you can simulate with two terminal sessions).

### Person A's Work

```bash
git switch -c conflict/lab3-person-a

# In todo-app/src/operations.py, find the add_todo docstring and add:
# """Raises: ValueError if title is empty."""
git commit -am "docs: document ValueError in add_todo"
git push -u origin conflict/lab3-person-a
```

### Person B's Work (at the same time)

```bash
git switch main
git switch -c conflict/lab3-person-b

# In todo-app/src/operations.py, same docstring location, add:
# """Raises: ValueError if title is empty or exceeds 100 characters."""
git commit -am "docs: document stricter validation in add_todo"
git push -u origin conflict/lab3-person-b
```

### Merge Process

```bash
# Person A's PR merged first (no conflict yet)
git switch main && git merge conflict/lab3-person-a

# Person B now needs to rebase before their PR can merge
git switch conflict/lab3-person-b
git fetch origin
git rebase origin/main
# Conflict! Resolve as in Lab 1 and Lab 2
# Choose to keep: """Raises: ValueError if title is empty or exceeds 100 characters."""
git add todo-app/src/operations.py
git rebase --continue

git push --force-with-lease origin conflict/lab3-person-b
# --force-with-lease is safer than -f: fails if someone else pushed in the meantime
```

### Cleanup

```bash
git switch main
git branch -d conflict/lab3-person-a conflict/lab3-person-b
```

---

## Lab 4 — Intentional Divergent History

**Goal:** Experience what makes conflicts more (or less) complex, and practice `git log` to understand divergent history.

```bash
git switch -c conflict/lab4-diverge-a
# Make 3 commits to todo-app/src/models.py:
# 1. Change the class name (just the docstring)
# 2. Add a field
# 3. Add a method stub
for i in 1 2 3; do
  echo "# edit $i" >> todo-app/src/models.py
  git commit -am "chore: edit $i on diverge-a"
done

git switch main
git switch -c conflict/lab4-diverge-b
# Make 3 DIFFERENT commits to the same file:
for i in 4 5 6; do
  echo "# edit $i" >> todo-app/src/models.py
  git commit -am "chore: edit $i on diverge-b"
done

# Now visualize the divergence BEFORE merging
git log --oneline --graph --all

# Merge — expect conflicts
git switch main
git merge conflict/lab4-diverge-a
git merge conflict/lab4-diverge-b

# Count conflict markers
grep -c "<<<<<<" todo-app/src/models.py

# Resolve all conflicts, then:
git add todo-app/src/models.py
git commit -m "merge: resolve divergent edits to models.py"

git log --oneline --graph --all   # see the full merge topology
```

---

## Conflict Resolution Checklist

When you hit a conflict, always follow this sequence:

1. `git status` — identify ALL conflicted files
2. Open each conflicted file and search for `<<<<<<<`
3. For each conflict block:
   - Understand what each side changed and WHY
   - Choose the correct version (or combine both thoughtfully)
   - Delete ALL three conflict markers: `<<<<<<<`, `=======`, `>>>>>>>`
4. `git diff` — verify the file looks correct after resolution
5. `git add <resolved-file>` — mark as resolved
6. `git status` — confirm no more conflicts
7. `git commit` (for merge) or `git rebase --continue` (for rebase)
8. `git log --oneline --graph` — verify the history looks right

**Never use `git add .` blindly after a conflict** — check each file first.

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Leaving conflict markers in the file | Code breaks / tests fail | Search for `<<<<<<<` before committing |
| Running `git commit` during a rebase | Creates an unexpected commit | Use `git rebase --continue` instead |
| Pushing after a rebase without `--force-with-lease` | Might clobber a teammate's push | Always use `--force-with-lease`, never `-f` |
| Aborting and giving up | Lose your progress | Use `git rebase --abort` to reset cleanly, then try again |
