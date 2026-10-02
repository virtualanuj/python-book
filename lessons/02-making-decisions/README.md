# Lesson 2: Making decisions

Nice work finishing lesson 1! Today your code learns to **make choices**: do one thing in one situation and something else in another. Same as before, take it at your own pace and ask in the chat whenever something doesn't click.

**What you'll build today:** ThreatDesk learns to look at a value like `"198.51.100.7"` or `"https://login.bad.example"` and work out what kind of indicator it is.

**What you'll learn:** `True` and `False`, comparing values, `and` / `or` / `not`, and `if` / `elif` / `else`.

---

## Part 1: True and False (5 minutes)

Python has two special values for yes and no: `True` and `False` (with capital letters). They're called **booleans**.

Start the prompt (`uv run --python 3.14 python`) and try some questions:

```python
>>> 5 > 3
True
>>> 2 == 7
False
```

Note the **double** equals `==`. It means "is this equal to?". A single `=` stores a value in a variable (from lesson 1), so Python needs a different symbol for comparing.

| You write | It asks |
|---|---|
| `a == b` | is a equal to b? |
| `a != b` | is a different from b? |
| `a > b`, `a < b` | greater than, less than |
| `a >= b`, `a <= b` | greater or equal, less or equal |

These work on strings too:

```python
>>> "evil.example" == "evil.example"
True
>>> "evil.example" == "EVIL.example"
False
```

That second one is exactly why we wrote `clean()` in lesson 1!

## Part 2: Questions you can ask a string (5 minutes)

```python
>>> url = "https://login.bad.example"
>>> url.startswith("https://")
True
>>> "@" in "payroll@phish.example"     # is "@" somewhere inside?
True
>>> "198.51.100.7".count(".")          # how many dots?
3
>>> "42".isdigit()                     # only digits 0-9?
True
>>> "4a".isdigit()
False
```

## Part 3: Combining questions with and, or, not (5 minutes)

```python
>>> value = "198.51.100.7"
>>> value.count(".") == 3 and value.replace(".", "").isdigit()
True
```

- `A and B` is `True` only if **both** are true.
- `A or B` is `True` if **at least one** is true.
- `not A` flips `True` to `False` and back.

```python
>>> url = "http://old.bad.example"
>>> url.startswith("http://") or url.startswith("https://")
True
```

## Part 4: Functions that answer yes or no (5 minutes)

A function can return a boolean. By convention, their names start with `is_`:

```python
def is_long(value):
    return len(value) > 20
```

`len(value)` gives the number of characters. `len(value) > 20` is already `True` or `False`, so we can return it directly.

## Part 5: if, elif, else (10 minutes)

Now the main event. `if` runs some code **only when** a condition is true:

```python
def describe_size(value):
    if len(value) > 20:
        return "long"
    elif len(value) > 5:
        return "medium"
    else:
        return "short"
```

How Python reads it:

1. Is the value longer than 20 characters? If yes, return `"long"` and stop.
2. **Otherwise** (`elif` means "else if"), is it longer than 5? If yes, return `"medium"` and stop.
3. If none of the above matched, `else` catches everything left: return `"short"`.

Python checks from the top and takes the **first** match, so order matters. Each condition ends with a colon `:`, and the code that belongs to it is indented, just like a function body.

```python
>>> describe_size("evil.example")
'medium'
```

---

## Exercise: teach ThreatDesk to recognise indicators

Open `lessons/02-making-decisions/exercise.py`. There are four functions to fill in, and each one has a comment explaining what it should do. Run the checker as often as you like:

```bash
uv run --python 3.14 lessons/02-making-decisions/exercise.py
```

| Step | Function | Returns |
|---|---|---|
| 1 | `is_url(value)` | `True` if it starts with `http://` or `https://` |
| 2 | `is_email(value)` | `True` if it contains `@` |
| 3 | `is_ipv4(value)` | `True` if it has exactly 3 dots and only digits otherwise |
| 4 | `guess_kind(value)` | `"url"`, `"email-addr"`, `"ipv4-addr"` or `"domain-name"` |

For step 4, use `if` / `elif` / `else` and **call your three functions from steps 1 to 3**. Functions using other functions is how real programs are built. Hint: check for a URL first, because a URL can contain an `@` too.

When everything passes, compare with [`solutions/02-making-decisions/solution.py`](../../solutions/02-making-decisions/solution.py).

## If you get stuck

- `SyntaxError` near an `if`: check for the colon `:` at the end of the line.
- Your function returns `None`: one of the branches is missing a `return`.
- `=` vs `==`: inside a condition you almost always want `==`.

## Why this matters for ThreatDesk

Threat feeds don't always label their data. Sometimes you just get a list of values, and ThreatDesk has to work out what each one is before it can store or search it properly. `guess_kind()` is the first version of that. (Our `is_ipv4` is deliberately simple: it would accept `999.1.1.1`. A later lesson uses Python's built-in `ipaddress` module to do it properly.)
