# Practical Python: building a product step by step

Micro lessons (15 to 30 minutes each) that take you from core Python to expert product development. Every lesson adds one real piece to the same product, **ThreatDesk**, and every lesson has a matching book chapter.

## Repository layout

```
python-book/
├── README.md            this file: setup and how to use the repo
├── OUTLINE.md           the full course plan (40 lessons, 10 modules)
├── book/                the book, one chapter per lesson
│   ├── README.md        table of contents
│   └── 01-strings-functions.md
├── lessons/             hands-on lessons; you edit the exercise files
│   └── 01-parse-pattern/
│       ├── README.md    the micro lesson
│       └── exercise.py  starter code with built-in checks
└── solutions/           reference solutions, kept apart so you don't peek
    └── 01-parse-pattern/
        └── solution.py
```

From lesson 5 onwards, the product code also lives in `threatdesk/` as a real package that grows lesson by lesson.

## Python version: 3.14

Use **CPython 3.14** (latest patch release). The whole ecosystem (FastAPI, Pydantic, SQLAlchemy, pytest, mypy) fully supports it. Python 3.15.0 came out on 1 October 2026; a later lesson covers upgrading, which is itself a useful product skill.

## Setup with uv

[uv](https://docs.astral.sh/uv/) installs Python, creates virtual environments and manages dependencies.

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

uv python install 3.14
git clone https://github.com/virtualanuj/python-book.git
cd python-book
```

## How to work through a lesson

1. Read `lessons/NN-name/README.md`.
2. Edit `lessons/NN-name/exercise.py` and run it: `uv run --python 3.14 lessons/01-parse-pattern/exercise.py`.
3. When every check passes, compare with `solutions/NN-name/solution.py`.
4. Read `book/NN-*.md` to consolidate what you learned.

## The product: ThreatDesk

A threat intelligence service. It ingests indicators of compromise from **TAXII 2.1** feeds (as **STIX 2.1** objects), normalises and de-duplicates them, enriches them, and serves them through a CLI (`threatdesk search 198.51.100.7`), a FastAPI web API and a dashboard.

All examples use documentation-only IP ranges (198.51.100.0/24, 203.0.113.0/24) and `.example` domains, so nothing in this repo points at real infrastructure.
