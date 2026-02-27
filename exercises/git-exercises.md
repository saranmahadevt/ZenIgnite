# Git Exercises

Work through these exercises in order. Each builds on the previous and covers the commands listed in the [git-commands-cheatsheet.md](../git-commands-cheatsheet.md).

> **Rule:** Do each exercise in your actual project repository. Don't use a throwaway repo — use the ZenIgnite repo during or before your team phase.

---

## Exercise 1 — Identity & Config

**Git commands:** `git config`, `git config --list`

```bash
# Check your current identity
git config user.name
git config user.email

# Set them if needed
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Set VS Code as your default editor
git config --global core.editor "code --wait"

# View all global config
git config --global --list

# Set a useful alias
git config --global alias.lg "log --oneline --graph --all"
# Now you can run: git lg
```

**Verify:** `git config --list` shows your name, email, and the `lg` alias.

---

## Exercise 2 — Clone & Explore

**Git commands:** `git clone`, `git remote -v`, `git log`, `git show`, `git status`

```bash
# Clone the team repo (already done? just explore)
git clone <your-team-repo> zen-explore
cd zen-explore

# See the remotes
git remote -v

# Explore the history
git log
git log --oneline
git log --oneline --graph --all     # or: git lg

# Show what changed in the very first commit
git log --oneline | tail -1         # get the first commit SHA
git show <first-commit-sha>

# Check for any unstaged changes
git status
git diff
```

**Verify:** You can name the first commit author, message, and what files it changed.

---

## Exercise 3 — Branching & Switching

**Git commands:** `git branch`, `git checkout -b`, `git switch -c`, `git switch`, `git branch -d`

```bash
# List all local branches
git branch

# List all branches including remote-tracking
git branch -a

# Create a new branch (without switching)
git branch exercise/branching-practice

# Switch to it
git switch exercise/branching-practice

# Create and switch in one command
git switch -c exercise/another-branch

# List branches again — see which one is active
git branch

# Go back to your original branch
git switch exercise/branching-practice

# Delete the unused branch
git branch -d exercise/another-branch

# Try to delete a branch with unmerged changes (it should refuse)
git switch -c exercise/unmerged
echo "test" > test.txt
git add test.txt
git commit -m "test: add test file"
git switch exercise/branching-practice
git branch -d exercise/unmerged    # should fail
git branch -D exercise/unmerged    # force delete
```

**Verify:** `git branch -a` shows only the branches you intended to keep.

---

## Exercise 4 — Staging & Committing

**Git commands:** `git add`, `git add -p`, `git diff`, `git diff --staged`, `git commit`, `git commit --amend`, `git restore --staged`

```bash
git switch -c exercise/staging-practice

# Make two unrelated changes in the same file
# Open todo-app/src/models.py and change VALID_PRIORITIES (line 1 of TODO)
# Also add a comment somewhere else in the same file

# Stage only one hunk interactively
git add -p todo-app/src/models.py
# Press 'y' for the hunk you want, 's' to split, 'n' to skip

# See what's staged vs unstaged
git diff            # unstaged changes
git diff --staged   # staged changes

# Commit the staged hunk
git commit -m "docs: add comment to models.py"

# Oops — typo in message. Amend it:
git commit --amend -m "docs: add clarifying comment to models.py"

# Stage the rest and commit
git add todo-app/src/models.py
git commit -m "chore: update VALID_PRIORITIES placeholder comment"

# Practice unstaging:
echo "temp" > temp.txt
git add temp.txt
git status                          # shows as staged
git restore --staged temp.txt       # unstage
git status                          # shows as untracked
rm temp.txt
```

**Verify:** `git log --oneline` shows exactly 2 clean commits on this branch.

---

## Exercise 5 — Stashing

**Git commands:** `git stash`, `git stash push -m`, `git stash list`, `git stash pop`, `git stash apply`, `git stash show`, `git stash drop`

```bash
git switch -c exercise/stash-practice

# Make some changes but don't commit them
echo "# WIP notes" >> todo-app/README.md

# Stash them with a message
git stash push -m "WIP: README notes"

# Verify working tree is clean
git status
cat todo-app/README.md   # your changes are gone

# Make another stash
echo "second wip" >> todo-app/README.md
git stash push -m "WIP: second notes"

# List all stashes
git stash list

# View what's in a specific stash
git stash show -p stash@{0}

# Apply the older stash without removing it
git stash apply stash@{1}

# Pop the most recent stash
git stash pop

# Drop a stash manually
git stash list
git stash drop stash@{0}

# Clear all remaining stashes
git stash clear
git stash list   # should be empty
```

**Verify:** `git stash list` is empty and `git status` shows a clean tree.

---

## Exercise 6 — Remote Operations

**Git commands:** `git fetch`, `git pull`, `git push`, `git push -u`, `git remote add`, `git remote -v`

```bash
# Add a second remote (the original ZenIgnite repo as upstream)
git remote add upstream https://github.com/saranmahadevt/ZenIgnite.git
git remote -v    # should show both origin and upstream

# Fetch updates from upstream without merging
git fetch upstream
git log upstream/main --oneline

# Fetch from origin
git fetch origin
git log origin/main --oneline

# Push a branch with tracking set up
git switch -c exercise/remote-practice
git commit --allow-empty -m "chore: empty commit to practice remote push"
git push -u origin exercise/remote-practice

# Verify tracking
git branch -vv    # shows tracking info

# Pull latest main
git switch main
git pull origin main

# Remove the upstream remote when done
git remote remove upstream
```

**Verify:** `git remote -v` shows only `origin`. The exercise branch was pushed successfully.

---

## Exercise 7 — Merging

**Git commands:** `git merge`, `git merge --no-ff`, `git merge --abort`

```bash
git switch main

# Create a feature branch with a small change
git switch -c exercise/merge-practice
echo "# Merge exercise" > merged-note.md
git add merged-note.md
git commit -m "docs: add merge exercise note"

# Merge back into main
git switch main
git merge exercise/merge-practice          # fast-forward merge

# Now try a --no-ff merge to force a merge commit
git switch -c exercise/merge-no-ff
echo "# No-FF merge" >> merged-note.md
git commit -am "docs: update merge note"

git switch main
git merge --no-ff exercise/merge-no-ff -m "merge: exercise/merge-no-ff into main"

# View the graph
git log --oneline --graph --all

# Clean up
git branch -d exercise/merge-practice exercise/merge-no-ff
rm merged-note.md
git commit -am "chore: remove merge exercise file"
```

**Verify:** `git log --oneline --graph` shows a merge commit node from `--no-ff`.

---

## Exercise 8 — Rebasing

**Git commands:** `git rebase`, `git rebase -i`, `git rebase --abort`, `git rebase --continue`

```bash
# Create a branch with 4 commits
git switch -c exercise/rebase-practice
echo "line 1" > rebase-test.txt && git add . && git commit -m "feat: line 1"
echo "line 2" >> rebase-test.txt && git commit -am "WIP: line 2"
echo "line 3" >> rebase-test.txt && git commit -am "fixup: fix typo line 2"
echo "line 4" >> rebase-test.txt && git commit -am "feat: line 4"

git log --oneline    # 4 commits, 2 are WIP/fixup

# Interactive rebase to squash the WIP into the previous commit
git rebase -i HEAD~4
# In the editor:
#   pick  abc  feat: line 1
#   pick  def  WIP: line 2        ← change "pick" to "squash"
#   pick  ghi  fixup: fix typo    ← change "pick" to "fixup"
#   pick  jkl  feat: line 4

git log --oneline    # should now show 2 clean commits

# Add main changes and rebase on top
git switch main
echo "main update" > rebase-main.txt && git add . && git commit -m "chore: main update"

git switch exercise/rebase-practice
git rebase main      # replay your commits on top of new main

git log --oneline --graph --all

# Clean up
git switch main
git branch -D exercise/rebase-practice
rm rebase-main.txt
git commit -am "chore: remove rebase exercise file"
```

**Verify:** The `exercise/rebase-practice` commits appeared on top of the main commit (no merge commit).

---

## Exercise 9 — Undoing Changes

**Git commands:** `git reset --soft`, `git reset --hard`, `git revert`, `git restore`

```bash
git switch -c exercise/undo-practice

# Make 3 commits
echo "A" > undo-test.txt && git add . && git commit -m "feat: A"
echo "B" >> undo-test.txt && git commit -am "feat: B"
echo "C" >> undo-test.txt && git commit -am "feat: C"

git log --oneline   # 3 commits

# Soft reset — undo last commit, keep changes staged
git reset --soft HEAD~1
git status          # C change is staged
git log --oneline   # only 2 commits now

# Re-commit with a better message
git commit -m "feat: add C with better message"

# Hard reset — undo last 2 commits and discard changes
git reset --hard HEAD~2
git log --oneline   # only the A commit
cat undo-test.txt   # only "A"

# Safe undo with revert (creates a new commit — safe for shared history)
git revert HEAD --no-edit
git log --oneline   # shows both the original and the revert commit

# Discard working directory changes
echo "unwanted change" >> undo-test.txt
git restore undo-test.txt
cat undo-test.txt   # change is gone

# Clean up
git switch main
git branch -D exercise/undo-practice
```

**Verify:** You understand the difference between `reset` (rewrites history) and `revert` (adds a new commit).

---

## Exercise 10 — Cherry-Picking, Blame, Bisect & Reflog

**Git commands:** `git cherry-pick`, `git blame`, `git bisect`, `git reflog`

```bash
# Cherry-pick
git switch -c exercise/cherry-source
echo "cherry feature" > cherry.txt && git add . && git commit -m "feat: cherry feature"
SOURCE_SHA=$(git log --oneline -1 | awk '{print $1}')

git switch main
git switch -c exercise/cherry-target
git cherry-pick $SOURCE_SHA       # bring the commit over
git log --oneline                  # cherry feature should be here

# Blame
git blame todo-app/src/database.py
git blame -L 1,20 todo-app/src/database.py   # blame specific lines

# Bisect practice (simulated)
# Make commits where a "bug" is introduced at commit 3
git switch -c exercise/bisect-practice
echo "v1" > bisect.txt && git add . && git commit -m "test: v1 (good)"
echo "v2" >> bisect.txt && git commit -am "test: v2 (good)"
echo "BUG" >> bisect.txt && git commit -am "test: v3 (this is the bad one)"
echo "v4" >> bisect.txt && git commit -am "test: v4 (good but bug inherited)"

git bisect start
git bisect bad                          # current commit has bug
git bisect good HEAD~3                  # v1 was good
# Git checks out a middle commit — check if bisect.txt contains "BUG":
# cat bisect.txt
# If it does: git bisect bad
# If not:     git bisect good
# Repeat until Git identifies the offending commit
git bisect reset

# Reflog
git reflog                              # see every HEAD movement
git switch main
git branch -D exercise/bisect-practice exercise/cherry-source exercise/cherry-target
git reflog                              # even deleted branch commits are here
# You could recover a deleted branch:
# git switch -c recovered-branch <sha-from-reflog>
```

**Verify:** You can navigate `git reflog` and understand how to recover a "lost" commit.

---

## Exercise Completion Checklist

- [ ] Exercise 1 — Config: alias `lg` created and working
- [ ] Exercise 2 — Clone & Explore: described the first commit
- [ ] Exercise 3 — Branching: created and deleted branches confidently
- [ ] Exercise 4 — Staging: used `git add -p` and `--amend`
- [ ] Exercise 5 — Stashing: used all stash subcommands
- [ ] Exercise 6 — Remotes: pushed a tracking branch
- [ ] Exercise 7 — Merging: observed fast-forward vs `--no-ff`
- [ ] Exercise 8 — Rebasing: squashed commits with `rebase -i`
- [ ] Exercise 9 — Undoing: understood `reset` vs `revert`
- [ ] Exercise 10 — Advanced: used `cherry-pick`, `blame`, `bisect`, `reflog`
