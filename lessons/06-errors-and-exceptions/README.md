# Lesson 6: Errors and exceptions

You've been adding `raise ValueError(...)` to your exercises since lesson 1 without being asked, so this lesson makes it official. 🙂

Right now, when `parse_pattern()` meets a broken pattern, it returns `None`. That keeps the program running, but it throws away **why** the pattern was broken. Was it missing brackets? Was the value unquoted? Whoever runs ThreatDesk will want to know, so they can tell the feed provider. Today the parser learns to explain itself.

**What you'll learn:** reading type hints, what exceptions are, `try`/`except`, `raise`, and making your own error type.

**New in the exercises from today:** every function has **type hints**. Part 1 explains how to read them.

---

## Part 1: Reading type hints (5 minutes)

Type hints are short notes that say what kind of value goes **in** to a function and what comes **out**:

```python
def make_key(kind: str, value: str) -> str:
    return f"{kind}|{value}"
```

- `kind: str` means "`kind` should be a string".
- `-> str` means "this function gives back a string".

Some hints you'll see:

| Hint | Means |
|---|---|
| `str`, `int`, `bool` | a string, a whole number, True/False |
| `list[str]` | a list of strings |
| `dict[str, int]` | a dict with string keys and int values |
| `tuple[str, str, str]` | a tuple of exactly three strings |
| `set[str]` | a set of strings |
| `str \| None` | a string, **or** `None` |

Python itself doesn't check hints when your code runs. They're there for **people** (you can read a function's first line and know how to use it) and for **tools**: your editor uses them for autocomplete and warnings, and lesson 10 adds a checker that catches mistakes before you run anything. Professional Python code almost always has them.

The solutions for lessons 1 to 5 now include type hints too, so you can see your earlier work written this way.

## Part 2: What an exception is (5 minutes)

When Python hits something it can't do, it **raises an exception**: it stops what it's doing and reports the problem.

```python
>>> int("42")
42
>>> int("forty-two")
ValueError: invalid literal for int() with base 10: 'forty-two'
```

`ValueError` is the exception's **type**, and the text after it is the **message**. Types you've probably met already:

| Exception | Raised when |
|---|---|
| `ValueError` | the type is right but the value is wrong (`int("abc")`) |
| `TypeError` | the type is wrong (`"port " + 443`) |
| `KeyError` | a dict key doesn't exist |
| `IndexError` | a list position doesn't exist |

If nothing **handles** an exception, the whole program stops and prints the traceback you've learned to read.

## Part 3: Handling exceptions with try and except (10 minutes)

```python
def to_number(text: str) -> int | None:
    try:
        return int(text)
    except ValueError:
        return None
```

How it reads:

1. **try** to run the indented code.
2. If a `ValueError` happens anywhere in that block, jump to `except ValueError:` and run its code instead.
3. If no error happens, the `except` block is skipped.

```python
>>> to_number("443")
443
>>> to_number("https") is None
True
```

To use the error's message, give it a name with `as`:

```python
try:
    int("forty-two")
except ValueError as err:
    print(f"Could not convert: {err}")
```

**Only catch what you expect.** `except ValueError:` handles bad numbers. It doesn't hide a typo elsewhere in your code that causes a `NameError`, which is good: you *want* to see those. Avoid a bare `except:` that catches everything.

## Part 4: Raising your own exceptions (5 minutes)

You've done this already:

```python
if value == "":
    raise ValueError("value must not be empty")
```

`raise` stops the function immediately (like `return`) and hands the error to whoever called it. The caller can handle it with `try`/`except`, or let it stop the program.

**Return `None` or raise?** A good rule: if "no answer" is a normal, expected outcome, return `None`. If it means something is wrong and the caller should know what, raise an exception with a clear message.

## Part 5: Your own exception type (5 minutes)

You can create a new kind of exception with two lines:

```python
class PatternError(ValueError):
    """A STIX pattern could not be parsed."""
```

`class` creates a new type (lesson 8 covers classes properly). `(ValueError)` means "a `PatternError` is a special kind of `ValueError`", so code that catches `ValueError` catches it too. The docstring is the only body it needs.

Now ThreatDesk can raise errors that clearly belong to it:

```python
raise PatternError("value must be in single quotes")
```

and callers can catch exactly that:

```python
try:
    parsed = parse_pattern(text)
except PatternError as err:
    print(f"Skipping bad pattern: {err}")
```

---

## Exercise: a parser that explains itself

Open `lessons/06-errors-and-exceptions/exercise.py`. `PatternError` is already defined at the top for you.

```bash
uv run --python 3.14 lessons/06-errors-and-exceptions/exercise.py
```

| Step | Function | What it does |
|---|---|---|
| 1 | `to_number(text: str) -> int \| None` | `int(text)`, or `None` if it's not a number |
| 2 | `require_brackets(pattern: str) -> str` | returns the text inside `[ ]`, or raises `PatternError("missing [ ] brackets")` |
| 3 | `parse_pattern(pattern: str) -> tuple[str, str, str]` | like lesson 4, but **raises** `PatternError` with a specific message instead of returning `None` |
| 4 | `safe_parse(pattern: str) -> tuple[str, str, str] \| None` | calls `parse_pattern`, and returns `None` if it raises `PatternError` |
| 5 | `ingest(patterns: list[str]) -> tuple[list[dict[str, str]], list[str]]` | returns the good indicators **and** a list of error reports for the bad ones |

The exact messages for step 3 are in the comments in the exercise file. The checker tells you if a message doesn't match.

For step 5, each error report should look like this (the `!r` adds quotes around the pattern):

```python
f"{pattern!r}: {err}"
# "'not a pattern': missing [ ] brackets"
```

When all five pass, compare with [`solutions/06-errors-and-exceptions/solution.py`](../../solutions/06-errors-and-exceptions/solution.py).

## If you get stuck

- The checker says your function returned something when it should have raised: make sure you used `raise`, not `return`.
- Your `except` never runs: check you're catching the right type (`PatternError`), and that the call which might fail is **inside** the `try` block.
- `NameError: name 'err' is not defined`: you need `except PatternError as err:` to give the error a name.

## Why this matters for ThreatDesk

When a feed sends garbage, an operator needs to see something like `'[ipv4-addr:value = 198.51.100.7]': value must be in single quotes`, not just "1 pattern skipped". Clear, specific errors turn a mystery into a five-minute fix, and that's a big part of what makes a product feel trustworthy.
