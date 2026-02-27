# Solutions

> If you are stuck or want to verify your implementation, the complete working solutions are organised here by workflow and person.

## Structure

```
solution/
├── three-person/
│   ├── person-a/
│   │   ├── database.py    ← Complete database.py solution
│   │   └── models.py      ← Complete models.py solution
│   ├── person-b/
│   │   └── operations.py  ← Complete operations.py solution
│   └── person-c/
│       ├── cli.py          ← Complete cli.py solution
│       └── test_todos.py  ← Complete test suite solution
└── four-person/
    ├── person-a/
    │   ├── database.py
    │   └── models.py
    ├── person-b/
    │   └── operations.py
    ├── person-c/
    │   └── cli.py
    └── person-d/
        └── test_todos.py
```

## How to Use

1. Try implementing your module yourself first.
2. If you are stuck for more than 30 minutes, look at the solution.
3. Do NOT copy-paste blindly — read the solution, understand it, close it, then write your own version.
4. The Git workflow (branches, commits, PRs) is your main learning goal. The Python code is secondary.

## Note on Differences Between Workflows

The Python implementation is identical between the three-person and four-person workflows. The only difference is the person responsible for each file:

| File | 3-person Owner | 4-person Owner |
|------|---------------|----------------|
| `database.py` | Person A | Person A |
| `models.py` | Person A | Person A |
| `operations.py` | Person B | Person B |
| `cli.py` | Person C | Person C |
| `test_todos.py` | Person C | Person D |
