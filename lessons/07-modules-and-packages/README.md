# Lesson 7: Modules, packages and files

This is the last lesson of Module 1, and it's a milestone. 🎉

So far each lesson's code has lived in its own `exercise.py`, and every new lesson started by copying your earlier functions in at the top. Real products don't work like that. Today you'll move ThreatDesk's code into a proper **package**: a folder of well-named files that import from each other, which any later lesson (and later, a CLI, an API and a dashboard) can use.

You'll also read a threat feed from a **file** for the first time.

**What you'll learn:** modules and `import`, the standard library, packages, creating a project with uv, and reading a text file.

**What's different today:** there's no `exercise.py`. You'll create real files in a new `threatdesk/` folder, and a checker tests the package you built.

---

## Part 1: Modules and import (10 minutes)

Every `.py` file is a **module**. Code in one module can use code from another with `import`.

Try it with modules from Python's **standard library**, the large toolbox that comes with every Python install:

```python
>>> import ipaddress
>>> ipaddress.ip_address("198.51.100.7")
IPv4Address('198.51.100.7')
>>> ipaddress.ip_address("198.51.100.7").version
4
>>> ipaddress.ip_address("2001:db8::1").version
6
>>> ipaddress.ip_address("999.1.1.1")
ValueError: '999.1.1.1' does not appear to be an IPv4 or IPv6 address
```

That `ValueError` is exactly what lesson 6 taught you to catch. This module fixes the `is_ipv4("999.1.1.1")` weakness from lesson 2, and handles IPv6 for free.

There are two ways to import:

```python
import ipaddress                  # then write ipaddress.ip_address(...)
from collections import Counter   # then write Counter(...) directly
```

`Counter` is the ready-made version of your `count_by_type` loop:

```python
>>> from collections import Counter
>>> Counter(["ipv4-addr", "url", "ipv4-addr"])
Counter({'ipv4-addr': 2, 'url': 1})
```

Imports always go at the **top** of a file.

## Part 2: Packages (5 minutes)

A **package** is a folder of modules that belong together. ThreatDesk will look like this:

```
threatdesk/                     the project folder
├── pyproject.toml              the project's settings (name, Python version, ...)
└── src/
    └── threatdesk/             the package itself
        ├── __init__.py         marks this folder as a package
        ├── normalize.py        clean, make_key, guess_kind
        ├── patterns.py         PatternError, parse_pattern, safe_parse
        └── ingest.py           to_indicator, ingest, count_by_type, reading files
```

Each module has **one job**, and its name says what that job is. Modules import from each other using the package name:

```python
# in ingest.py
from threatdesk.patterns import PatternError, parse_pattern
```

(The extra `src/` folder is a common convention called the **src layout**. It stops you from accidentally importing the code without installing it properly, which avoids a whole family of confusing bugs.)

## Part 3: Reading a file (5 minutes)

```python
from pathlib import Path

text = Path("lessons/07-modules-and-packages/sample-feed.txt").read_text()
lines = text.splitlines()      # a list, one item per line
```

`Path` comes from the standard library too. Lesson 17 covers files in depth; this is all you need today.

---

## Exercise: build the threatdesk package

Run every command from the **repo root** (the `python-book` folder). The checker runs like this:

```bash
uv run --project threatdesk lessons/07-modules-and-packages/check.py
```

`--project threatdesk` tells uv to use your new project, so `import threatdesk` works. As before, the checker goes step by step and gives hints.

### Step 1: create the project

```bash
uv init --lib --vcs none --python 3.14 threatdesk
```

- `--lib` makes a library-style project with the `src/threatdesk/` layout.
- `--vcs none` stops uv from creating a second git repository inside yours.

Look at what it made. You can delete the example `hello()` function in `src/threatdesk/__init__.py`. Leave the file there (it can even be empty), because it's what makes the folder a package.

### Step 2: `normalize.py`

Create `threatdesk/src/threatdesk/normalize.py` with `clean`, `make_key` and `guess_kind`, copied from your earlier lessons. Then make `guess_kind` smarter with `ipaddress`:

- a valid IPv4 address gives `"ipv4-addr"`,
- a valid IPv6 address gives `"ipv6-addr"`,
- `"999.1.1.1"` is no longer an IP, so it falls through to `"domain-name"`.

A helper keeps it tidy:

```python
def ip_version(value: str) -> int | None:
    """Return 4 or 6 if value is a valid IP address, otherwise None."""
    ...  # try ipaddress.ip_address(value).version, except ValueError return None
```

### Step 3: `patterns.py`

Create `patterns.py` with `PatternError`, `require_brackets`, `is_quoted`, `parse_pattern` and `safe_parse` from lesson 6.

### Step 4: `ingest.py`

Create `ingest.py` with `to_indicator`, `ingest` and `count_by_type`. It needs to **import** what it uses from your other modules:

```python
from threatdesk.normalize import make_key
from threatdesk.patterns import PatternError, parse_pattern
```

Bonus: let `to_indicator` use `make_key()` for the `"key"` field, and try `Counter` in `count_by_type`.

### Step 5: read a feed file

Add two functions to `ingest.py`:

- `load_patterns(path: str) -> list[str]` reads the file and returns one pattern per line, **skipping blank lines and lines that start with `#`** (comments). Strip each line first.
- `ingest_file(path: str) -> tuple[list[dict[str, str]], list[str]]` is one line: `return ingest(load_patterns(path))`.

Open [`sample-feed.txt`](sample-feed.txt) to see what the checker feeds in. It has comments, blank lines, a duplicate, two broken patterns and an IPv6 address.

When everything passes, compare with the reference package in [`solutions/07-modules-and-packages/threatdesk/`](../../solutions/07-modules-and-packages/threatdesk/).

## Try it yourself

Once the checker passes, ThreatDesk is importable from anywhere in the project. Try:

```bash
uv run --project threatdesk python
```

```python
>>> from threatdesk.ingest import ingest_file
>>> indicators, errors = ingest_file("lessons/07-modules-and-packages/sample-feed.txt")
>>> for error in errors:
...     print(error)
```

## If you get stuck

- `ModuleNotFoundError: No module named 'threatdesk'`: check you ran `uv init` from the repo root, and that you passed `--project threatdesk` to `uv run`.
- `ModuleNotFoundError: No module named 'threatdesk.normalize'`: the file is in the wrong place or misspelled. It must be `threatdesk/src/threatdesk/normalize.py`, next to `__init__.py`.
- `ImportError: cannot import name 'parse_pattern'`: the function's name in `patterns.py` doesn't match the import, or it's missing.
- `FileNotFoundError`: paths are relative to the folder you ran the command from, so run it from the repo root.

## Why this matters for ThreatDesk

From now on, every lesson adds to **this** package instead of starting over. Tests (Module 3), the database (Module 4), the CLI (Module 5) and the API (Module 9) will all `import threatdesk`. You've just laid the foundation the whole product stands on.
