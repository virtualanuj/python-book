# Lesson 1: Strings, functions and f-strings

**Product step:** ThreatDesk's first real feature. Threat feeds describe indicators with **STIX patterns**, for example:

```
[ipv4-addr:value = '198.51.100.7']
[file:hashes.'SHA-256' = '2cf24dba...9824']
```

Before ThreatDesk can store, search or de-duplicate an indicator, it has to understand that string. You'll turn it into:

```python
{"type": "ipv4-addr", "property": "value", "value": "198.51.100.7",
 "key": "ipv4-addr|198.51.100.7"}
```

The `key` is what ThreatDesk will use later to spot the same indicator arriving from different feeds.

## Setup (once)

Install uv and Python 3.14 and clone this repo (see the top-level README). Then, from the repo root:

```bash
uv run --python 3.14 lessons/01-parse-pattern/exercise.py
```

## The ideas you need

**1. Strings are immutable sequences with handy methods.** Every method returns a new string.

```python
p = "  [ipv4-addr:value = '198.51.100.7']  "
p = p.strip()                       # remove surrounding whitespace
p.startswith("["), p.endswith("]")  # (True, True)
inner = p[1:-1]                     # slice: drop first and last character
"Update.EXAMPLE".lower()            # "update.example"
```

**2. `partition` splits once and never fails.** It always returns a 3-tuple, so you can unpack it safely:

```python
left, sep, right = "ipv4-addr:value = '1.2.3.4'".partition("=")
# left = "ipv4-addr:value ", sep = "=", right = " '1.2.3.4'"
"no equals here".partition("=")     # ("no equals here", "", "")  sep is "" when not found
```

Compare `split("=", 1)`, which returns a list of one or two items and makes you check its length.

**3. Functions with type hints and docstrings.** `dict | None` says "returns a dict, or None". Small helpers keep the main function readable:

```python
def is_quoted(text: str) -> bool:
    """True for "'abc'": wrapped in single quotes."""
    return len(text) >= 2 and text.startswith("'") and text.endswith("'")
```

**4. f-strings** build values inline: `f"{object_type}|{value}"`. Use `f"{pattern!r}"` in debug output so stray spaces are visible.

**5. Early returns.** Check each requirement and `return None` as soon as one fails. The happy path then reads top to bottom without deep nesting.

## Exercise

Open `exercise.py` and implement `parse_pattern(pattern)`:

1. Ignore surrounding whitespace. The pattern must start with `[` and end with `]`.
2. Inside the brackets, a compound pattern containing ` AND ` or ` OR ` returns `None` for now (lesson 3 handles them).
3. Split on the first `=`. The left side is `type:property` (split on the first `:`); the right side must be a value in single quotes. Spaces around `=` are optional.
4. Return `None` if anything is missing: no `=`, no `:`, unquoted value, empty type, property or value.
5. Normalise: lowercase the value for `domain-name` and `email-addr`, and for any property starting with `hashes.`. Leave IPs and URLs as they are (URL paths can be case-sensitive).
6. Add `"key": f"{type}|{value}"`.

Run the exercise until all 10 checks pass. Then compare with [`solutions/01-parse-pattern/solution.py`](../../solutions/01-parse-pattern/solution.py).

## Stretch goals

- Write `describe(indicator)` returning `"ipv4-addr 198.51.100.7"` for display, using an f-string.
- The STIX spec allows `\'` inside a quoted value. Find an input that breaks your parser, and write it down for lesson 14 (property-based testing).

## Product thinking

Threat feeds are **untrusted input**: they come from third parties and may be malformed or even hostile. Rejecting anything you don't fully understand (returning `None`, and later raising a clear error) is safer than guessing. Normalising case is what makes de-duplication work: `Update.Malware.EXAMPLE` and `update.malware.example` are the same domain, and treating them as two indicators would double-count alerts.
