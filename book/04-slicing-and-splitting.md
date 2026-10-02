# Chapter 4: Slicing and splitting text

> ThreatDesk gains: `parse_pattern()`, which reads the STIX pattern `[ipv4-addr:value = '198.51.100.7']` and returns `("ipv4-addr", "value", "198.51.100.7")`, or `None` if the pattern is broken.

## 4.1 Background: STIX and TAXII in one minute

Organisations share threat intelligence in a standard JSON format called **STIX 2.1**, usually delivered over **TAXII 2.1**, an HTTP API for threat feeds. ThreatDesk will speak both. The most important STIX object is the **indicator**, and its key field is a `pattern`:

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "pattern": "[domain-name:value = 'update.malware.example']",
  "pattern_type": "stix",
  "valid_from": "2026-10-01T00:00:00Z"
}
```

The simplest patterns are a single comparison inside square brackets:

```
[<object-type>:<property> = '<value>']
```

Common object types are `ipv4-addr`, `ipv6-addr`, `domain-name`, `url`, `email-addr` and `file`. Files are usually matched by hash, for example `[file:hashes.'SHA-256' = '2cf2...']`. Patterns can also combine comparisons with `AND` and `OR`; ThreatDesk will handle those later.

## 4.2 Indexing and slicing

Strings and lists share the same indexing rules (Chapter 3):

```python
s = "ThreatDesk"
s[0]      # 'T'
s[-1]     # 'k'
```

A **slice** `s[start:stop]` takes everything from `start` up to, **but not including**, `stop`:

```
 T  h  r  e  a  t  D  e  s  k
 0  1  2  3  4  5  6  7  8  9
-10 -9 -8 -7 -6 -5 -4 -3 -2 -1
```

| Slice | Result | Meaning |
|---|---|---|
| `s[0:6]` | `'Threat'` | positions 0 to 5 |
| `s[6:]` | `'Desk'` | from 6 to the end |
| `s[:6]` | `'Threat'` | from the start to 5 |
| `s[1:-1]` | `'hreatDes'` | drop the first and last characters |
| `s[:]` | `'ThreatDesk'` | a full copy |

Two facts that save a lot of bugs:

- **Slicing never raises an error** for out-of-range positions: `"ab"[5:]` is simply `""`. Indexing does: `"ab"[5]` raises `IndexError`.
- The length of `s[a:b]` is `b - a` (for positive positions). "Stop is excluded" makes this arithmetic work.

## 4.3 split and partition

| Call | Result | Notes |
|---|---|---|
| `"a b  c".split()` | `['a', 'b', 'c']` | no argument: any run of whitespace, no empty items |
| `"a,,b".split(",")` | `['a', '', 'b']` | exact separator: keeps empty items |
| `"a=b=c".split("=", 1)` | `['a', 'b=c']` | split at most once |
| `"a=b=c".partition("=")` | `('a', '=', 'b=c')` | always 3 parts, first match only |
| `"abc".partition("=")` | `('abc', '', '')` | middle is `''` when not found |

**Why `partition` for parsing:** it always returns exactly three strings, so unpacking it never fails, and it only splits at the **first** separator. That matters for patterns like `[url:value = 'http://bad.example/a=b']`, where only the first `=` is part of the pattern's structure. The others belong to the value.

## 4.4 Tuples and unpacking

A **tuple** is an ordered, unchangeable sequence, written with commas (the brackets are optional but usual):

```python
point = (3, 4)
parsed = ("ipv4-addr", "value", "198.51.100.7")
parsed[0]          # 'ipv4-addr'
len(parsed)        # 3
```

Use a tuple for a fixed group of values that belong together, such as the three parts of a pattern. Use a list for a collection that grows or shrinks, such as a feed.

**Unpacking** assigns each item to its own variable:

```python
object_type, prop, value = parsed
before, _, after = "a:b".partition(":")   # _ means "I don't need this one"
```

The number of names must match the number of items, otherwise you get `ValueError: too many values to unpack` (or "not enough").

A function returns several values by returning a tuple: `return before.strip(), after.strip()`.

## 4.5 None and early returns

`None` is Python's "no value". Functions use it to say "I couldn't produce an answer". Check for it with `is None` / `is not None`, not `== None`:

```python
result = parse_pattern(text)
if result is None:
    print("Could not understand that pattern")
```

**Early returns** (also called guard clauses) check each requirement and leave as soon as one fails:

```python
def parse_pattern(pattern):
    if not has_brackets(pattern):
        return None
    ...
```

Everything after a guard can assume that requirement holds. The alternative, nested `if` blocks several levels deep, is much harder to read.

## 4.6 ThreatDesk code after Chapter 4

```python
def has_brackets(pattern):
    p = pattern.strip()
    return p.startswith("[") and p.endswith("]")


def strip_brackets(pattern):
    return pattern.strip()[1:-1]


def split_once(text, sep):
    before, found, after = text.partition(sep)
    return before.strip(), after.strip()


def is_quoted(text):
    return len(text) >= 2 and text.startswith("'") and text.endswith("'")


def parse_pattern(pattern):
    if not has_brackets(pattern):
        return None

    left, right = split_once(strip_brackets(pattern), "=")
    if not is_quoted(right):
        return None

    object_type, prop = split_once(left, ":")
    value = right[1:-1]
    if object_type == "" or prop == "" or value == "":
        return None

    return object_type, prop, value
```

```python
>>> parse_pattern("[ipv4-addr:value = '198.51.100.7']")
('ipv4-addr', 'value', '198.51.100.7')
>>> parse_pattern("[ipv4-addr:value = 198.51.100.7]") is None
True
```

### Design decisions recorded

- **Strict by default.** Threat feeds are untrusted input. Anything the parser doesn't fully understand returns `None` instead of a guess.
- **First separator wins.** Only the first `=` and the first `:` are structural.
- **Known gaps:** compound patterns (`AND`/`OR`) and escaped quotes inside values (`\'`) aren't handled yet. Chapter 6 replaces `None` with errors that explain *what* was wrong.

## Key takeaways

- `s[start:stop]` includes `start` and excludes `stop`; `s[1:-1]` drops both ends.
- `partition()` splits once, always returns three parts, and never fails.
- Tuples group a fixed number of related values; unpack them into separate names.
- `None` means "no answer"; test it with `is None`.
- Guard clauses with early returns keep validation code flat.
- Treat external data as hostile: reject what you don't understand.
