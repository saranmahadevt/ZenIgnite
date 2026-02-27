# Four-Person Workflow

## Overview

Four people collaborate to build the complete Todo CLI application. Compared to the three-person workflow, this adds a dedicated **QA & Release Engineer** role, making the workflow more parallel and allowing earlier feedback.

---

## Team Roles

| Person | Role | Module(s) |
|--------|------|-----------|
| **Person A** | Lead / DB Architect | `database.py`, `models.py` |
| **Person B** | Backend Developer | `operations.py` |
| **Person C** | Interface Builder | `cli.py` |
| **Person D** | QA & Release Engineer | `tests/test_todos.py`, release tag, docs |

Read the full role descriptions in [roles.md](roles.md).

---

## Workflow at a Glance

```
Phase 1: Person A                  (DB Setup)
           │
           ▼
Phase 2: Person B ─────────────────(CRUD + B starts testing too)
           │
           ├──► Phase 3: Person C  (CLI Interface)
           │
           └──► Phase 3: Person D  (Test Suite — can start after Phase 1)
                    │
                    ▼
               Phase 4: Person D   (QA sign-off, docs, release)
```

Key difference from 3-person: **Person C and Person D can work in parallel during Phase 3**. Person C builds the interface while Person D writes tests against the already-merged CRUD layer.

---

## Phases

| Phase | Owner | Depends On | Guide |
|-------|-------|------------|-------|
| Phase 1: Setup & DB | Person A | — | [phase-1-setup-db.md](phase-1-setup-db.md) |
| Phase 2: CRUD | Person B | Phase 1 merged | [phase-2-backend.md](phase-2-backend.md) |
| Phase 3a: Interface | Person C | Phase 2 merged | [phase-3-interface.md](phase-3-interface.md) (Person C section) |
| Phase 3b: Tests | Person D | Phase 1 merged — can start early | [phase-3-interface.md](phase-3-interface.md) (Person D section) |
| Phase 4: QA & Release | Person D | Phases 3a + 3b merged | [phase-4-qa-release.md](phase-4-qa-release.md) |

---

## Branch Strategy

```
main
 ├── feature/db-setup          (Person A)
 ├── feature/crud-operations   (Person B)
 ├── feature/cli-interface     (Person C)
 ├── feature/tests             (Person D)
 └── release/v1.0              (Person D)
```

---

## Ground Rules

1. **Never commit directly to `main`**.
2. Every PR requires **at least one review**.
3. Commit messages follow [Conventional Commits](../../git-commands-cheatsheet.md#commit-message-convention).
4. Person D is the **quality gate** — nothing is released without their test sign-off.
5. Use `git fetch` + `git rebase origin/main` (not merge) to stay current.

---

## Final Release

After all PRs are merged, Person D leads the release:

```bash
git switch main && git pull origin main
python -m pytest todo-app/tests/ -v
git tag -a v1.0 -m "Release v1.0 — four-person workflow complete"
git push origin v1.0
git log --oneline --graph --all
```
