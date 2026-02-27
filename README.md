# ZenIgnite — Git Collaboration Training

> **Learn Git by building something real.**

ZenIgnite is a hands-on training repository where teams collaborate to build a **Todo CLI application backed by SQLite** using Python. The goal is NOT just to build the app — the goal is to **master Git workflows** along the way.

---

## What You Will Build

A command-line Todo application that lets users:

- **Add** todos with a title, description, priority, and due date
- **List** todos with optional filters (by status or priority)
- **Update** todo status (`pending` → `in-progress` → `done`) and priority
- **Delete** todos
- **Persist** all data in a local SQLite database

---

## Repository Structure

```
ZenIgnite/
├── README.md                        ← You are here
├── .gitignore
├── git-commands-cheatsheet.md       ← Full Git reference (study this first)
├── todo-app/
│   ├── README.md                    ← App requirements & setup
│   ├── requirements.txt
│   └── src/
│       ├── database.py              ← DB connection layer
│       ├── models.py                ← Todo data model
│       ├── operations.py            ← CRUD business logic
│       └── cli.py                   ← Command-line interface
│   └── tests/
│       └── test_todos.py            ← Unit test stubs
├── solution/
│   ├── README.md                    ← How to use the solutions
│   ├── three-person/
│   │   ├── person-a/                ← database.py + models.py
│   │   ├── person-b/                ← operations.py
│   │   └── person-c/                ← cli.py + test_todos.py
│   └── four-person/
│       ├── person-a/                ← database.py + models.py
│       ├── person-b/                ← operations.py
│       ├── person-c/                ← cli.py
│       └── person-d/                ← test_todos.py
├── workflows/
│   ├── three-person/                ← 3-person collaboration guide
│   └── four-person/                 ← 4-person collaboration guide
└── exercises/
    ├── git-exercises.md             ← Step-by-step Git exercises
    └── conflict-resolution.md      ← Merge conflict practice lab
```

---

## Using the Solutions

The `solution/` folder contains complete, working implementations for every module. Use them as a **last resort** — only after genuinely attempting the implementation yourself.

> **Rule:** Read a solution, understand it, close it, then write your own version from scratch. Do not copy-paste.

See [solution/README.md](solution/README.md) for the full guide.

---

## Choose Your Workflow

| Team Size | Guide |
|-----------|-------|
| 3 people  | [Three-Person Workflow](workflows/three-person/README.md) |
| 4 people  | [Four-Person Workflow](workflows/four-person/README.md) |

---

## Before You Start

### Prerequisites

- Git installed and configured
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "you@example.com"
  ```
- Python 3.8+ installed
- A GitHub account
- Read [git-commands-cheatsheet.md](git-commands-cheatsheet.md)

### Setup

```bash
# Clone the training repo (replace URL with your team's forked repo)
git clone <your-team-repo-url>
cd ZenIgnite

# Install dependencies
pip install -r todo-app/requirements.txt

# Run the app (once your team has implemented it)
python todo-app/src/cli.py
```

---

## Git Philosophy for This Training

> "Every meaningful action deserves a commit. Every feature deserves a branch."

You are expected to use **at least 25 different Git commands** across this training. Study [git-commands-cheatsheet.md](git-commands-cheatsheet.md) and work through [exercises/git-exercises.md](exercises/git-exercises.md).

---

## Completion Checklist

- [ ] Forked and cloned the repo
- [ ] Each person created their own feature branch
- [ ] Feature branches merged into `main` via Pull Requests (with at least one review)
- [ ] All CRUD operations implemented and working
- [ ] At least one merge conflict intentionally created and resolved
- [ ] Commit history shows meaningful, atomic commit messages
- [ ] A release tagged as `v1.0`
- [ ] Ran `git log --oneline --graph --all` and can read the history