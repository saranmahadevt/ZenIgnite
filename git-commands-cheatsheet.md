# Git Commands Cheatsheet

> Reference guide for the ZenIgnite training. Every command listed here should appear at least once in your team's git history by the end of the project.

---

## 1. Setup & Configuration

```bash
# Set your identity (do this before your first commit)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Set preferred editor
git config --global core.editor "code --wait"

# View all configuration
git config --list

# View a specific setting
git config user.name
```

---

## 2. Starting a Repository

```bash
# Initialize a new repository
git init

# Clone an existing repository
git clone <url>

# Clone into a specific folder
git clone <url> my-folder

# Clone only the most recent snapshot (shallow clone)
git clone --depth 1 <url>
```

---

## 3. Remotes

```bash
# View remotes
git remote -v

# Add a remote
git remote add origin <url>

# Rename a remote
git remote rename origin upstream

# Remove a remote
git remote remove upstream

# Fetch all info from a remote without merging
git fetch origin

# Fetch a specific branch
git fetch origin feature/crud-operations
```

---

## 4. Staging & Committing

```bash
# Check status of working tree
git status

# Stage a specific file
git add src/database.py

# Stage all changes
git add .

# Stage changes interactively (hunk by hunk)
git add -p

# Unstage a file
git restore --staged src/database.py

# Discard changes in working directory
git restore src/database.py

# Commit staged changes
git commit -m "feat: add SQLite database connection module"

# Commit with a multi-line message
git commit

# Amend the last commit message (before pushing)
git commit --amend -m "feat: add SQLite database connection with init schema"

# Amend without changing the message
git commit --amend --no-edit

# Stage tracked files and commit in one step
git commit -am "fix: correct null check in delete operation"
```

---

## 5. Branching

```bash
# List local branches
git branch

# List all branches (including remote-tracking)
git branch -a

# Create a new branch
git branch feature/crud-operations

# Switch to an existing branch
git checkout feature/crud-operations
# Modern syntax:
git switch feature/crud-operations

# Create and switch in one step
git checkout -b feature/cli-interface
# Modern syntax:
git switch -c feature/cli-interface

# Rename the current branch
git branch -m feature/cli-ui feature/cli-interface

# Delete a branch (safe — only if merged)
git branch -d feature/crud-operations

# Force-delete a branch
git branch -D feature/abandoned-idea

# Push a local branch to remote and track it
git push -u origin feature/crud-operations

# Delete a remote branch
git push origin --delete feature/old-branch
```

---

## 6. Merging

```bash
# Merge a branch into the current branch
git merge feature/crud-operations

# Merge with a commit message (no fast-forward)
git merge --no-ff feature/crud-operations -m "merge: integrate CRUD operations"

# Abort a merge in progress
git merge --abort

# After fixing conflicts, complete the merge
git add .
git commit
```

---

## 7. Rebasing

```bash
# Rebase current branch on top of main
git rebase main

# Interactive rebase — rewrite last 3 commits
git rebase -i HEAD~3

# Interactive rebase options (in the editor):
#   pick   → keep the commit as-is
#   reword → keep but edit message
#   edit   → pause and amend the commit
#   squash → combine with the previous commit
#   fixup  → like squash but discard the message
#   drop   → remove the commit entirely

# Abort an in-progress rebase
git rebase --abort

# Continue after resolving conflicts during rebase
git rebase --continue
```

---

## 8. Viewing History

```bash
# Full log
git log

# Compact one-line log
git log --oneline

# Visual graph of all branches
git log --oneline --graph --all

# Log with author and date
git log --pretty=format:"%h %an %ar %s"

# Filter by author
git log --author="Alice"

# Filter by date
git log --after="2026-01-01" --before="2026-03-01"

# Search commits whose diff contains a string
git log -S "create_table"

# Show changes introduced by a specific commit
git show abc1234

# Show the most recent commit on current branch
git show HEAD
```

---

## 9. Diffing

```bash
# Diff working directory vs staging area
git diff

# Diff staging area vs last commit
git diff --staged

# Diff between two branches
git diff main..feature/crud-operations

# Diff a specific file between two branches
git diff main..feature/crud-operations -- src/operations.py

# Diff two commits
git diff abc1234 def5678
```

---

## 10. Stashing

```bash
# Stash uncommitted changes (saves them temporarily)
git stash

# Stash with a descriptive message
git stash push -m "WIP: half-done delete operation"

# List all stashes
git stash list

# Apply the most recent stash (keeps it in the stash list)
git stash apply

# Apply the most recent stash and remove it from the list
git stash pop

# Apply a specific stash
git stash apply stash@{2}

# View what's in a stash
git stash show -p stash@{0}

# Drop a specific stash
git stash drop stash@{1}

# Clear all stashes
git stash clear
```

---

## 11. Undoing Changes

```bash
# Undo the last commit, keep changes staged
git reset --soft HEAD~1

# Undo the last commit, keep changes unstaged
git reset HEAD~1

# Undo the last commit, discard ALL changes (destructive!)
git reset --hard HEAD~1

# Create a new commit that undoes a previous commit (safe for shared history)
git revert abc1234

# Revert without auto-committing
git revert --no-commit abc1234
```

---

## 12. Cherry-Picking

```bash
# Apply a specific commit from another branch to current branch
git cherry-pick abc1234

# Cherry-pick without auto-committing
git cherry-pick --no-commit abc1234

# Cherry-pick a range of commits
git cherry-pick abc1234..def5678
```

---

## 13. Tagging

```bash
# List all tags
git tag

# Create a lightweight tag
git tag v1.0

# Create an annotated tag (recommended for releases)
git tag -a v1.0 -m "Release version 1.0 — all CRUD operations complete"

# Tag a specific past commit
git tag -a v0.9 abc1234 -m "Beta release"

# Push a tag to remote
git push origin v1.0

# Push all tags
git push origin --tags

# Delete a local tag
git tag -d v0.9

# Delete a remote tag
git push origin --delete v0.9
```

---

## 14. Blame & Bisect

```bash
# See who last changed each line of a file
git blame src/operations.py

# Blame a specific line range
git blame -L 10,25 src/operations.py

# Find which commit introduced a bug (binary search)
git bisect start
git bisect bad                  # current commit is broken
git bisect good abc1234         # this commit was working
# Git checks out commits in between; test each one then run:
git bisect good   # or: git bisect bad
# When found:
git bisect reset                # return to original HEAD
```

---

## 15. Reflog (Your Safety Net)

```bash
# View the reflog — every HEAD movement ever
git reflog

# Recover a deleted branch or lost commit
git checkout -b recovered-branch abc1234

# Undo a bad rebase or reset using reflog
git reset --hard HEAD@{5}
```

---

## Commit Message Convention

Use **Conventional Commits** format throughout this training:

```
<type>: <short description>

[optional body]

[optional footer]
```

| Type | When to use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Formatting, no logic change |
| `refactor` | Code restructuring, no feature/fix |
| `test` | Adding or updating tests |
| `chore` | Build process, dependency updates |

**Examples:**
```
feat: add SQLite schema for todos table
fix: handle empty title in add_todo validation
test: add unit tests for delete operation
docs: add setup instructions to README
refactor: extract db connection into context manager
```

---

## Branch Naming Convention

```
feature/<short-description>       # New feature work
fix/<short-description>           # Bug fixes
docs/<short-description>          # Documentation
refactor/<short-description>      # Refactoring
release/<version>                 # Release preparation
```
