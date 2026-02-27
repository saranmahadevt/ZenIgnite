# Phase 4 — QA Sign-Off & Release

**Owner:** Person D (QA & Release Engineer)
**Depends on:** All Phase 3 PRs merged to `main`

This is the final phase. Person D takes ownership of quality, documentation, and the version release.

---

## Step 1: Final Sync and Full Test Run

```bash
git switch main
git pull origin main
git log --oneline --graph --all    # take a screenshot — this is the team's work

python -m pytest todo-app/tests/ -v
# Every test must be green. If any fail, create a fix branch:
# git switch -c fix/test-failures origin/main
```

---

## Step 2: End-to-End Smoke Test

```bash
# Clean start — remove any stale DB
del todo-app\todos.db    # Windows

python todo-app/src/cli.py add --title "Buy groceries" --priority high --due 2026-03-10
python todo-app/src/cli.py add --title "Read Clean Code" --priority medium
python todo-app/src/cli.py add --title "Clean desk" --priority low
python todo-app/src/cli.py list
python todo-app/src/cli.py list --status pending
python todo-app/src/cli.py list --priority high
python todo-app/src/cli.py update --id 1 --status in-progress
python todo-app/src/cli.py update --id 2 --status done
python todo-app/src/cli.py show --id 1
python todo-app/src/cli.py delete --id 3
python todo-app/src/cli.py list
```

---

## Step 3: Create a Release Branch

```bash
git switch -c release/v1.0
git log --oneline   # review what's in this release
```

On the release branch, verify and pin the version.

---

## Step 4: Update Documentation

Update the main `README.md` if any setup steps have changed:

```bash
# Make any doc-only fixes:
git add README.md todo-app/README.md
git commit -m "docs: update README with final setup and usage examples"
```

Use `git log` to compile what went into this release:

```bash
git log main --oneline --since="1 week ago"
# Use this to write release notes
```

---

## Step 5: Merge Release Branch to Main

```bash
# Open a PR: release/v1.0 → main
# Review with the full team
# After approval:
git switch main
git pull origin main
git merge --no-ff release/v1.0 -m "release: merge v1.0 release branch"
git push origin main
```

---

## Step 6: Tag the Release

```bash
git tag -a v1.0 -m "Release v1.0

Features:
- Add todos with title, description, priority, due date
- List todos with status and priority filters
- Update todo status and priority
- Delete todos
- Full SQLite persistence
- Complete test suite"

git push origin v1.0
git tag           # verify
git show v1.0     # verify tag details
```

---

## Step 7: Celebrate and Review Git History

```bash
git log --oneline --graph --all

# See contributions by author
git shortlog -sn

# See all tags
git tag -l

# See the full commit count
git rev-list --count main
```

Pull up the history in GitHub → Insights → Contributors. Every team member should appear.

---

## Completion Checklist

- [ ] All tests green: `python -m pytest todo-app/tests/ -v`
- [ ] End-to-end smoke test passed
- [ ] No `NotImplementedError` anywhere in the codebase
- [ ] At least 25 unique Git commands used across the team (check cheatsheet)
- [ ] At least one merge conflict was intentionally created and resolved
- [ ] `v1.0` tag pushed and visible on GitHub
- [ ] `git log --oneline --graph --all` shows a clean, meaningful history
- [ ] Every team member is visible in `git shortlog -sn`
