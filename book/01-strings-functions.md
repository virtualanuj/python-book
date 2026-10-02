# Chapter 1: Strings, functions and f-strings

> ThreatDesk gains: `parse_pattern()`, which turns the STIX pattern `[ipv4-addr:value = '198.51.100.7']` into `{"type": "ipv4-addr", "property": "value", "value": "198.51.100.7", "key": "ipv4-addr|198.51.100.7"}`.

## 1.0 Background: STIX patterns

Threat intelligence is shared as **STIX 2.1** JSON objects, usually delivered over **TAXII 2.1**, an HTTP API for threat feeds. An `indicator` object carries a `pattern` field describing what to look for:

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "pattern": "[domain-name:value = 'update.malware.example']",
  "pattern_type": "stix",
  "valid_from": "2026-10-01T00:00:00Z"
}
```

The simplest patterns are one comparison inside brackets: `[<object-type>:<property> = '<value>']`. Common object types are `ipv4-addr`, `ipv6-addr`, `domain-name`, `url`, `email-addr` and `file` (matched by `hashes.'SHA-256'`, `hashes.MD5` and so on). Chapter 3 handles compound patterns joined with `AND` and `OR`.

## 1.1 Strings are immutable sequences

A `str` is an ordered, immutable sequence of Unicode characters. Every string method returns a **new** string; the original never changes.

```python
p = "  [url:value='http://bad.example']  "
p.strip()      # "[url:value='http://bad.example']"
p              # unchanged
```

Because strings are sequences, you can index, slice, iterate and test membership:

```python
p = "[ipv4-addr:value = '198.51.100.7']"
p[0]           # "["
p[-1]          # "]"     negative indexes count from the end
p[1:-1]        # "ipv4-addr:value = '198.51.100.7'"  everything except first and last
" OR " in p    # False
len(p)         # 34
```

Slicing never raises for out-of-range bounds (`"x"[1:]` is `""`); indexing does (`""[0]` raises `IndexError`). Checking `len(text) >= 2` before trusting `text[0]` and `text[-1]` avoids surprises with very short input.

### Methods you will use constantly

| Method | Example | Result |
|---|---|---|
| `strip()` / `lstrip()` / `rstrip()` | `" x ".strip()` | `"x"` |
| `startswith()` / `endswith()` | `"[a]".startswith("[")` | `True` (also accepts a tuple of prefixes) |
| `partition(sep)` | `"a:b:c".partition(":")` | `("a", ":", "b:c")` splits once, always 3 parts |
| `split()` | `"a  b\tc".split()` | `["a", "b", "c"]` any whitespace, no empty items |
| `split(sep, maxsplit)` | `"a=b=c".split("=", 1)` | `["a", "b=c"]` |
| `join(iterable)` | `"-".join(["url", "x"])` | `"url-x"` |
| `lower()` / `casefold()` | `"EXAMPLE".lower()` | `"example"` |
| `removeprefix()` / `removesuffix()` | `"[x]".removeprefix("[")` | `"x]"` |

### `partition` vs `split`

```python
left, sep, right = "file:hashes.'SHA-256'".partition(":")
# ("file", ":", "hashes.'SHA-256'")
"no-colon".partition(":")
# ("no-colon", "", "")  -> sep == "" means "not found"
```

`partition` always returns exactly three strings, so unpacking it can never fail, and it splits on the **first** separator only. That matters here: in `file:hashes.'SHA-256' = 'ab:cd'` only the first `:` and the first `=` are structural.

**Pitfall:** `lower()` is fine for ASCII protocol values like domains and hashes. For comparing arbitrary international text case-insensitively, use `casefold()`. Internationalised domain names have their own rules (IDNA/punycode); Chapter 3 touches on them.

## 1.2 Functions

```python
def parse_pattern(pattern: str) -> dict | None:
    """Parse a simple STIX pattern like "[ipv4-addr:value = '198.51.100.7']"."""
    ...
```

- `def` creates a function object and binds it to a name.
- **Type hints** are not checked at runtime. `dict | None` documents that callers must handle `None`, and type checkers (Chapter 8) will enforce it.
- The **docstring** is the first string in the body. `help(parse_pattern)` shows it, and so does your editor on hover.
- A function without a `return` returns `None`.

### Small helpers and module-level constants

```python
CASE_INSENSITIVE_TYPES = ("domain-name", "email-addr")


def is_quoted(text: str) -> bool:
    """True for "'abc'": at least two characters, wrapped in single quotes."""
    return len(text) >= 2 and text.startswith("'") and text.endswith("'")
```

Upper-case names signal "do not reassign" and give magic values a meaning. A **tuple** is used because the set should not change at runtime. A helper with a good name turns a cryptic expression into a readable sentence inside the main function.

### Early returns (guard clauses)

```python
if not (pattern.startswith("[") and pattern.endswith("]")):
    return None
```

Check each requirement and leave as soon as one fails. The remaining code can then assume valid input, and the happy path reads top to bottom without nested `if` blocks.

**Pitfall:** never use a mutable default like `def f(tags=[])`. The list is created once, when the function is defined, and shared across every call. Use `None` and create the list inside.

## 1.3 f-strings

f-strings evaluate expressions inside `{}`:

```python
object_type, value = "ipv4-addr", "198.51.100.7"
f"{object_type}|{value}"            # "ipv4-addr|198.51.100.7"
f"{value!r}"                        # "'198.51.100.7'"  repr, with quotes
f"{object_type:<12}{value}"         # left-align type in 12 characters
f"{0.8734:.0%}"                     # "87%"  confidence scores later on
f"{value=}"                         # "value='198.51.100.7'"  great for debugging
```

Use `!r` when logging untrusted input, so empty strings, stray spaces and control characters are visible.

Python 3.14 adds **t-strings** (`t"..."`, PEP 750). They look like f-strings but produce a `Template` object, so a library can escape each value safely, for example for HTML or SQL. That matters for a security product: ThreatDesk's dashboard will render attacker-controlled strings, and Chapter 35 uses proper escaping for exactly that reason.

## 1.4 Normalisation and identity

Two indicators are the same if they describe the same thing:

- `Update.Malware.EXAMPLE` and `update.malware.example` are the same domain (DNS is case-insensitive).
- `2CF24DBA...` and `2cf24dba...` are the same SHA-256 hash (hex is case-insensitive).
- `http://bad.example/Login` and `http://bad.example/login` may be **different** URLs (paths can be case-sensitive), so URLs are left as they are.

ThreatDesk normalises values first, then builds a **key** with `f"{type}|{value}"`. Chapter 2 uses that key in a dict to de-duplicate indicators arriving from many feeds.

## 1.5 ThreatDesk code after Chapter 1

```python
# Values of these types are case-insensitive, so we store them lowercased.
CASE_INSENSITIVE_TYPES = ("domain-name", "email-addr")


def is_quoted(text: str) -> bool:
    """True for "'abc'": at least two characters, wrapped in single quotes."""
    return len(text) >= 2 and text.startswith("'") and text.endswith("'")


def parse_pattern(pattern: str) -> dict | None:
    """Parse a simple STIX pattern like "[ipv4-addr:value = '198.51.100.7']".

    Returns {"type": str, "property": str, "value": str, "key": str},
    or None if the pattern is not a single, well-formed comparison.
    """
    pattern = pattern.strip()
    if not (pattern.startswith("[") and pattern.endswith("]")):
        return None

    inner = pattern[1:-1]
    if " AND " in inner or " OR " in inner:
        return None  # compound patterns arrive in lesson 3

    left, sep, right = inner.partition("=")
    left, right = left.strip(), right.strip()
    if not sep or ":" not in left or not is_quoted(right):
        return None

    object_type, _, prop = left.partition(":")
    value = right[1:-1]
    if not object_type or not prop or not value:
        return None

    if object_type in CASE_INSENSITIVE_TYPES or prop.startswith("hashes."):
        value = value.lower()

    return {
        "type": object_type,
        "property": prop,
        "value": value,
        "key": f"{object_type}|{value}",
    }
```

### Design decisions recorded

- Anything not fully understood returns `None`; threat feeds are untrusted input. Chapter 4 replaces `None` with a `PatternError` that says what was wrong.
- Domains, email addresses and hashes are lowercased; IPs and URLs are kept as given.
- Compound patterns are deferred to Chapter 3.
- Known gap: escaped quotes (`\'`) inside values are not supported yet. Chapter 14's property-based tests will hunt for inputs like this.

## Key takeaways

- String methods return new strings; strings never change in place.
- `partition` is the safest way to split once: three parts, no exceptions, first separator only.
- Guard clauses with early returns keep validation code flat and readable.
- Type hints and docstrings cost seconds and pay off every time someone reads the code.
- Normalise before comparing: it is the foundation of de-duplication.
- Treat external data as hostile and reject what you do not understand.
