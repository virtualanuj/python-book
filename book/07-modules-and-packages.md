# Chapter 7: Modules, packages and files

> ThreatDesk gains: a real `threatdesk` package (`normalize`, `patterns` and `ingest` modules) created with uv, proper IPv4/IPv6 detection using the standard library, and `ingest_file()`, which reads a feed from disk.

## 7.1 Modules

A **module** is a `.py` file. Its functions, classes and variables can be used from other modules by importing it.

```python
import ipaddress                       # import the module, use ipaddress.ip_address()
from collections import Counter        # import one name from a module
from threatdesk.patterns import PatternError, parse_pattern   # several names
import threatdesk.normalize as norm    # import under a shorter name
```

| Style | Use when |
|---|---|
| `import module` | you use several things from it, and want it obvious where they come from (`ipaddress.ip_address`) |
| `from module import name` | you use one or two names a lot (`Counter`, `Path`) |

Avoid `from module import *`. It pulls in every name, so readers can't tell where anything came from.

### Order and placement

Imports go at the top of the file, in three groups separated by blank lines: the standard library, then third-party packages (from Module 5 on), then your own package. Tools like Ruff (Chapter 15) can sort them for you.

```python
from collections import Counter
from pathlib import Path

from threatdesk.normalize import make_key
from threatdesk.patterns import PatternError, parse_pattern
```

### What happens on import

The first time a module is imported, Python runs its file from top to bottom, which defines its functions and classes, and caches the result. Later imports reuse that cache. This is why module files should only *define* things. Code that *does* things (printing, reading files) belongs inside functions, or under the guard below.

```python
if __name__ == "__main__":
    main()
```

`__name__` is `"__main__"` only when the file is run directly (`python file.py`), not when it's imported. Every exercise checker in this course uses this guard.

## 7.2 The standard library

Python ships with hundreds of modules: "batteries included". A few ThreatDesk will use:

| Module | For |
|---|---|
| `ipaddress` | parsing and validating IPv4/IPv6 addresses and networks |
| `collections` | `Counter`, `defaultdict` and other specialised containers |
| `pathlib` | file paths and reading/writing files |
| `json` | reading and writing JSON (STIX is JSON) |
| `datetime` | dates, times and time zones |
| `logging` | structured log output |
| `sqlite3` | a built-in database |

Before writing something general-purpose yourself, check the standard library first. Its code is tested by millions of users.

### ipaddress

```python
>>> import ipaddress
>>> ipaddress.ip_address("198.51.100.7").version
4
>>> ipaddress.ip_address("2001:db8::1").version
6
>>> ipaddress.ip_address("198.51.100.7") in ipaddress.ip_network("198.51.100.0/24")
True
```

Invalid input raises `ValueError`, which makes it a natural fit for the try/except pattern from Chapter 6.

### Counter

```python
>>> from collections import Counter
>>> Counter(ind["type"] for ind in indicators)
Counter({'ipv4-addr': 2, 'domain-name': 1})
```

A `Counter` is a dict subclass, so everything you know about dicts still works. `.most_common(3)` gives the top three.

## 7.3 Packages and the src layout

A **package** is a folder of modules with an `__init__.py` file:

```
threatdesk/                 project folder (what uv manages)
├── pyproject.toml          project metadata and settings
├── README.md
└── src/
    └── threatdesk/         the importable package
        ├── __init__.py
        ├── py.typed        tells type checkers this package has type hints
        ├── normalize.py
        ├── patterns.py
        └── ingest.py
```

- `__init__.py` runs when the package is imported. It can be empty, or hold a docstring describing the package.
- Modules inside a package import each other with **absolute imports**: `from threatdesk.patterns import parse_pattern`.
- The **src layout** puts the package under `src/`, so the only way to import it is to install it (which `uv run` does for you). Without it, Python might import the local folder by accident and hide packaging mistakes until a user installs your code.

### How to split code into modules

Group code by **responsibility**, and name the module after it. A reader looking for "where are patterns parsed?" should be able to guess `patterns.py`. Dependencies should flow one way: `ingest` imports from `patterns` and `normalize`, and they never import from `ingest`. Two modules importing each other (a **circular import**) is a sign the split is wrong.

## 7.4 Projects with uv

```bash
uv init --lib --vcs none --python 3.14 threatdesk
```

| Option | Meaning |
|---|---|
| `--lib` | a library project with the `src/` layout and a build system, so it can be installed |
| `--vcs none` | don't create a git repository (we're already inside one) |
| `--python 3.14` | the minimum Python version for the project |

`pyproject.toml` is the standard file describing a Python project:

```toml
[project]
name = "threatdesk"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = []

[build-system]
requires = ["uv_build>=0.8.17,<0.9.0"]
build-backend = "uv_build"
```

`dependencies` lists third-party packages ThreatDesk needs. It's empty for now; `uv add httpx` will add to it in Module 6.

`uv run --project threatdesk <command>` creates a virtual environment (`threatdesk/.venv/`) if needed, installs the project into it, and runs the command there. The `.venv` folder is local to your machine and is never committed. `uv.lock` records exact versions and **is** committed.

## 7.5 Reading a text file

```python
from pathlib import Path

def load_patterns(path: str) -> list[str]:
    patterns = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue
        patterns.append(line)
    return patterns
```

- `Path(path).read_text()` reads the whole file into one string.
- `.splitlines()` splits it into a list of lines, without the newline characters.
- Relative paths are resolved from the **current working directory**, the folder you ran the command from, not the folder the `.py` file is in.

Reading the whole file at once is fine for small feeds. Chapter 12 streams large files line by line with generators.

## 7.6 ThreatDesk code after Chapter 7

`src/threatdesk/normalize.py`:

```python
import ipaddress


def clean(value: str) -> str:
    return value.strip().lower()


def make_key(kind: str, value: str) -> str:
    return f"{kind}|{value}"


def is_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def is_email(value: str) -> bool:
    return "@" in value


def ip_version(value: str) -> int | None:
    """Return 4 or 6 if value is a valid IP address, otherwise None."""
    try:
        return ipaddress.ip_address(value).version
    except ValueError:
        return None


def guess_kind(value: str) -> str:
    if is_url(value):
        return "url"
    elif is_email(value):
        return "email-addr"
    elif ip_version(value) == 4:
        return "ipv4-addr"
    elif ip_version(value) == 6:
        return "ipv6-addr"
    else:
        return "domain-name"
```

`src/threatdesk/patterns.py` holds `PatternError`, `require_brackets`, `is_quoted`, `parse_pattern` and `safe_parse`, unchanged from Chapter 6.

`src/threatdesk/ingest.py`:

```python
from collections import Counter
from pathlib import Path

from threatdesk.normalize import make_key
from threatdesk.patterns import PatternError, parse_pattern


def to_indicator(parsed: tuple[str, str, str]) -> dict[str, str]:
    object_type, prop, value = parsed
    return {
        "type": object_type,
        "property": prop,
        "value": value,
        "key": make_key(object_type, value),
    }


def ingest(patterns: list[str]) -> tuple[list[dict[str, str]], list[str]]:
    ...  # unchanged from Chapter 6


def count_by_type(indicators: list[dict[str, str]]) -> dict[str, int]:
    return dict(Counter(ind["type"] for ind in indicators))


def load_patterns(path: str) -> list[str]:
    ...  # as in 7.5


def ingest_file(path: str) -> tuple[list[dict[str, str]], list[str]]:
    return ingest(load_patterns(path))
```

### Design decisions recorded

- Three modules by responsibility: **normalize** (values), **patterns** (STIX syntax), **ingest** (turning feeds into records).
- `to_indicator` now uses `make_key`, so the key format is defined in exactly one place.
- IP detection uses `ipaddress`, which rejects `999.1.1.1` and understands IPv6.
- Feed files support `#` comments and blank lines, so people can annotate test feeds.

## Key takeaways

- A module is a `.py` file; a package is a folder of modules with `__init__.py`.
- Check the standard library before writing general-purpose code yourself.
- Put imports at the top, grouped standard library, third-party, then your own.
- Split code into modules by responsibility, with dependencies flowing one way.
- `uv init --lib` creates a project with the src layout; `uv run --project` runs code inside it.
- `Path(path).read_text().splitlines()` reads a small text file as a list of lines.
