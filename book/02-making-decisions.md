# Chapter 2: Making decisions

> ThreatDesk gains: `guess_kind()`, which looks at a raw value and decides whether it is a URL, an email address, an IPv4 address or a domain name.

## 2.1 Booleans

A **boolean** (`bool`) has only two possible values: `True` and `False`. They are written with a capital letter and no quotes. `"True"` in quotes is just a string.

Every question you ask Python, such as "is 5 bigger than 3?", produces a boolean:

```python
>>> 5 > 3
True
>>> type(5 > 3)
<class 'bool'>
```

## 2.2 Comparison operators

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `==` | equal to | `"a" == "a"` | `True` |
| `!=` | not equal to | `"a" != "b"` | `True` |
| `>` / `<` | greater / less than | `3 < 2` | `False` |
| `>=` / `<=` | greater or equal / less or equal | `3 >= 3` | `True` |

**`=` vs `==`.** One equals sign assigns (`x = 5` stores 5 in `x`). Two equals signs compare (`x == 5` asks whether `x` is 5). Mixing them up is the most common beginner bug. Luckily, Python gives a `SyntaxError` if you write `if x = 5:`.

String comparison is exact, character by character: `"Evil" == "evil"` is `False`. Normalise first (lesson 1's `clean()`) when case shouldn't matter.

## 2.3 Questions you can ask strings

| Expression | True when | Example |
|---|---|---|
| `x in s` | `x` appears somewhere in `s` | `"@" in "a@b.example"` |
| `x not in s` | it doesn't | `"@" not in "bad.example"` |
| `s.startswith(x)` | `s` begins with `x` | `"https://a".startswith("https")` |
| `s.endswith(x)` | `s` ends with `x` | `"bad.example".endswith(".example")` |
| `s.isdigit()` | `s` is non-empty and only digits | `"2026".isdigit()` |

And two useful tools that return numbers:

- `len(s)`: how many characters. `len("abc")` is `3`.
- `s.count(x)`: how many times `x` appears. `"1.2.3.4".count(".")` is `3`.

## 2.4 and, or, not

```python
value.count(".") == 3 and value.replace(".", "").isdigit()
```

| Expression | True when |
|---|---|
| `A and B` | both A and B are true |
| `A or B` | at least one is true |
| `not A` | A is false |

Python evaluates these left to right and **stops early** once the answer is known. In `A and B`, if `A` is false, `B` is never even looked at. This is called *short-circuiting*, and later you'll use it to avoid errors (for example, checking a value isn't empty before looking at its first character).

**Pitfall:** `value.startswith("http://") or "https://"` does **not** do what it looks like. The right side must be a complete question too: `value.startswith("http://") or value.startswith("https://")`.

## 2.5 if, elif, else

```python
def guess_kind(value):
    if is_url(value):
        return "url"
    elif is_email(value):
        return "email-addr"
    elif is_ipv4(value):
        return "ipv4-addr"
    else:
        return "domain-name"
```

- `if condition:` runs the indented block below it only when the condition is true.
- `elif condition:` ("else if") is checked only if everything above it was false. You can have as many as you need.
- `else:` runs when nothing above matched. It's optional and has no condition.
- Python takes the **first** branch that matches and skips the rest, so put the most specific checks first. Here, a URL like `https://user@bad.example` contains an `@`; checking for URLs before emails makes sure it's classified as a URL.

Every line that starts a block (`if`, `elif`, `else`, `def`) ends with a colon, and the block is indented by 4 spaces.

## 2.6 Functions that return booleans

```python
def is_email(value):
    return "@" in value
```

There's no need to write:

```python
def is_email(value):
    if "@" in value:
        return True
    else:
        return False
```

Both work, but `"@" in value` is already `True` or `False`, so returning it directly is shorter and clearer. Naming boolean functions `is_...` or `has_...` makes code read like English: `if is_email(value):`.

## 2.7 Building on your own functions

`guess_kind()` doesn't repeat the logic for spotting URLs, emails or IPs; it **calls** the small functions that already do it. This is one of the most important habits in programming: build small pieces that each do one job, test them, then combine them. When you later improve `is_ipv4()`, `guess_kind()` improves automatically.

## 2.8 ThreatDesk code after Chapter 2

```python
def clean(value):
    return value.strip().lower()


def make_key(kind, value):
    return f"{kind}|{value}"


def is_url(value):
    return value.startswith("http://") or value.startswith("https://")


def is_email(value):
    return "@" in value


def is_ipv4(value):
    return value.count(".") == 3 and value.replace(".", "").isdigit()


def guess_kind(value):
    if is_url(value):
        return "url"
    elif is_email(value):
        return "email-addr"
    elif is_ipv4(value):
        return "ipv4-addr"
    else:
        return "domain-name"
```

Putting the pieces together:

```python
>>> raw = "  Update.Malware.EXAMPLE "
>>> value = clean(raw)
>>> make_key(guess_kind(value), value)
'domain-name|update.malware.example'
```

### Known limits (on purpose, for now)

- `is_ipv4("999.1.1.1")` returns `True`, but 999 isn't a valid IP part. The standard library's `ipaddress` module handles this properly; we'll switch to it once we've covered errors and imports.
- IPv6 addresses (`2001:db8::1`) are classified as domain names. They'll get their own check later.

Being clear about what your code doesn't handle yet is a good engineering habit, not a weakness.

## Key takeaways

- Comparisons produce `True` or `False`; use `==` to compare and `=` to assign.
- `in`, `startswith`, `isdigit`, `len` and `count` let you ask questions about strings.
- `and`, `or` and `not` combine questions; each side must be a full question.
- `if` / `elif` / `else` picks the first matching branch, so order matters.
- Small functions that each answer one question combine into bigger, readable ones.
