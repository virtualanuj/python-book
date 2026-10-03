# Chapter 6: Errors and exceptions

> ThreatDesk gains: `PatternError`, a `parse_pattern()` that says exactly what is wrong with a bad pattern, and an `ingest()` that returns error reports alongside the good indicators. From this chapter on, all ThreatDesk code carries **type hints**.

## 6.1 Type hints

Type hints document what a function accepts and returns:

```python
def to_indicator(parsed: tuple[str, str, str]) -> dict[str, str]:
    ...
```

| Hint | Meaning |
|---|---|
| `str`, `int`, `float`, `bool` | basic types |
| `list[str]` | list whose items are strings |
| `dict[str, int]` | dict with `str` keys and `int` values |
| `set[str]` | set of strings |
| `tuple[str, str, str]` | tuple of exactly three strings |
| `tuple[str, ...]` | tuple of any length, all strings |
| `X \| None` | an `X`, or `None` |
| `-> None` | the function returns nothing useful |

Variables can be hinted too. This is mostly useful for empty containers, where a tool can't guess what will go inside:

```python
seen: set[str] = set()
counts: dict[str, int] = {}
```

### What hints do (and don't do)

- Python **does not enforce** hints at runtime. `make_key(1, 2)` still runs.
- **Editors** use them for autocomplete and to underline mistakes as you type.
- **Type checkers** such as mypy and pyright read the whole program and report mismatches before you run anything. Chapter 10 sets one up for ThreatDesk.
- **People** read them: a hinted signature is documentation that can't go out of date without a tool noticing.

The `X | None` syntax and lowercase `list[str]` / `dict[str, int]` work in Python 3.10 and later. Older code uses `Optional[X]` and `List[str]` from the `typing` module; you'll see both in the wild.

## 6.2 Exceptions

An exception is Python's way of saying "I can't continue from here". It has a **type** and a **message**:

```
ValueError: invalid literal for int() with base 10: 'forty-two'
```

When an exception is raised, Python leaves the current function, then the function that called it, and so on up the chain, until something **handles** it. If nothing does, the program stops and prints the traceback.

### Common built-in exceptions

| Exception | Typical cause |
|---|---|
| `ValueError` | right type, unacceptable value: `int("abc")` |
| `TypeError` | wrong type: `"port " + 443`, or calling a function with the wrong number of arguments |
| `KeyError` | missing dict key |
| `IndexError` | list position out of range |
| `AttributeError` | the value has no such method: `None.strip()` |
| `FileNotFoundError` | opening a file that doesn't exist (Chapter 17) |

They're organised in a family tree. For example, `KeyError` and `IndexError` are both kinds of `LookupError`, and almost everything is a kind of `Exception`. Catching a parent catches all of its children.

## 6.3 try / except / else / finally

```python
try:
    port = int(text)
except ValueError as err:
    print(f"bad port {text!r}: {err}")
    port = None
else:
    print("parsed fine")       # runs only if no exception happened
finally:
    print("always runs")       # runs no matter what, e.g. to close a connection
```

- Put **only** the code that might fail inside `try`. A large `try` block makes it unclear which line you're protecting.
- Catch **specific** exceptions. A bare `except:` or `except Exception:` also swallows bugs (typos, wrong names) you'd want to see.
- `as err` names the exception so you can read its message with `str(err)` or in an f-string.
- You can catch several types: `except (ValueError, KeyError):`.

## 6.4 raise

```python
if value == "":
    raise PatternError("value is empty")
```

`raise` stops the function immediately and sends the exception to the caller. Write messages for the person who'll read them: say what was wrong, not just that something was.

### None or an exception?

| Use `None` when... | Raise when... |
|---|---|
| "nothing found" is a normal outcome (a lookup with no match) | the input is invalid or something went wrong |
| the caller can carry on without knowing why | the caller (or an operator) needs to know **what** went wrong |

A common pattern is to offer both: a strict function that raises (`parse_pattern`) and a convenience wrapper that returns `None` (`safe_parse`).

## 6.5 Custom exception types

```python
class PatternError(ValueError):
    """A STIX pattern could not be parsed."""
```

This defines a new exception type that **inherits** from `ValueError`. Benefits:

- Callers can catch ThreatDesk parsing problems specifically (`except PatternError:`) without accidentally catching unrelated `ValueError`s from elsewhere.
- Code that already catches `ValueError` still works, because a `PatternError` *is* a `ValueError`.
- The name documents intent in tracebacks and logs.

Chapter 8 explains classes in full. For exceptions, this two-line form is all you usually need.

## 6.6 ThreatDesk code after Chapter 6

```python
class PatternError(ValueError):
    """A STIX pattern could not be parsed."""


def require_brackets(pattern: str) -> str:
    p = pattern.strip()
    if not (p.startswith("[") and p.endswith("]")):
        raise PatternError("missing [ ] brackets")
    return p[1:-1]


def is_quoted(text: str) -> bool:
    return len(text) >= 2 and text.startswith("'") and text.endswith("'")


def parse_pattern(pattern: str) -> tuple[str, str, str]:
    inner = require_brackets(pattern)

    left, _, right = inner.partition("=")
    left, right = left.strip(), right.strip()
    if not is_quoted(right):
        raise PatternError("value must be in single quotes")

    object_type, colon, prop = left.partition(":")
    object_type, prop = object_type.strip(), prop.strip()
    if not colon or object_type == "" or prop == "":
        raise PatternError("expected type:property before =")

    value = right[1:-1]
    if value == "":
        raise PatternError("value is empty")

    return object_type, prop, value


def safe_parse(pattern: str) -> tuple[str, str, str] | None:
    try:
        return parse_pattern(pattern)
    except PatternError:
        return None


def ingest(patterns: list[str]) -> tuple[list[dict[str, str]], list[str]]:
    seen: set[str] = set()
    indicators: list[dict[str, str]] = []
    errors: list[str] = []
    for pattern in patterns:
        try:
            parsed = parse_pattern(pattern)
        except PatternError as err:
            errors.append(f"{pattern!r}: {err}")
            continue
        indicator = to_indicator(parsed)
        if indicator["key"] in seen:
            continue
        seen.add(indicator["key"])
        indicators.append(indicator)
    return indicators, errors
```

```python
>>> indicators, errors = ingest(["[ipv4-addr:value = '198.51.100.7']", "not a pattern"])
>>> errors
["'not a pattern': missing [ ] brackets"]
```

### Design decisions recorded

- `parse_pattern()` is now **strict**: it raises with a specific message. `safe_parse()` keeps the old "return `None`" behaviour for callers who don't care why.
- `PatternError` subclasses `ValueError`, because a bad pattern is a bad value.
- `ingest()` never stops because of one bad pattern; it reports it and moves on. One broken line in a feed of 10,000 shouldn't lose the other 9,999.
- Error reports use `!r` so the exact offending text, including stray spaces, is visible.

## Key takeaways

- Type hints (`name: str`, `-> list[str]`, `X | None`) document intent for people and tools; Python doesn't enforce them at runtime.
- An exception has a type and a message, and travels up the call chain until handled.
- Keep `try` blocks small and catch specific exception types.
- `raise` with a clear message when input is invalid; return `None` when "nothing" is a normal answer.
- A custom exception is two lines and makes errors easy to catch precisely.
