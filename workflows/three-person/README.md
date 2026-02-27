# Three-Person Workflow

## Overview

Three people collaborate to build the complete Todo CLI application. Work is divided into sequential phases with clear handoffs, pull requests, and code reviews — just like a real engineering team.

---

## Team Roles

| Person | Role | Module(s) |
|--------|------|-----------|
| **Person A** | Lead / DB Architect | `database.py`, `models.py` |
| **Person B** | Backend Developer | `operations.py` |
| **Person C** | Interface Builder & QA | `cli.py`, `tests/test_todos.py` |

Read the full role descriptions in [roles.md](roles.md).

---

## Workflow at a Glance

```
Phase 1 ──► Phase 2 ──► Phase 3
Person A     Person B     Person C
DB Setup  ►  CRUD Logic ► CLI + Tests
   │            │             │
   ▼            ▼             ▼
 PR #1  ──►  PR #2   ──►   PR #3
               (depends       (depends
                on PR #1)      on PR #2)
```

---

## Phases

| Phase | Owner | Depends On | Guide |
|-------|-------|------------|-------|
| Phase 1: Setup & DB | Person A | — | [phase-1-setup-db.md](phase-1-setup-db.md) |
| Phase 2: CRUD | Person B | Phase 1 merged | [phase-2-crud.md](phase-2-crud.md) |
| Phase 3: Interface & Testing | Person C | Phase 2 merged | [phase-3-interface-testing.md](phase-3-interface-testing.md) |

---

## Ground Rules

1. **Never commit directly to `main`**. All work happens on feature branches.
2. Every Pull Request requires **at least one reviewer** before merging.
3. Commit messages follow [Conventional Commits](../../git-commands-cheatsheet.md#commit-message-convention).
4. Before opening a PR, run `git log --oneline` and make sure the history is clean.
5. Use `git rebase main` (not merge) to keep your branch up to date.

---

## Branch Strategy

```
main
 ├── feature/db-setup        (Person A)
 ├── feature/crud-operations (Person B)
 └── feature/cli-interface   (Person C)
     feature/tests           (Person C — can be parallel)
```

---

## Final Integration

After all three PRs are merged:

```bash
git switch main
git pull origin main
git log --oneline --graph --all
python todo-app/src/cli.py add --title "ZenIgnite complete!" --priority high
python -m pytest todo-app/tests/ -v
git tag -a v1.0 -m "Release v1.0 — three-person workflow complete"
git push origin v1.0
```
