# Chapter 1: First steps

> ThreatDesk gains: `clean()`, which tidies up an indicator value, and `make_key()`, which gives each indicator a simple ID.

This chapter is for complete beginners. It explains the ideas from lesson 1 in a bit more depth, so you can come back to it whenever something feels fuzzy.

## 1.1 Running Python

There are two ways to run Python code.

**The interactive prompt (the REPL).** Start it with `uv run --python 3.14 python`. You type one line, press Enter, and see the result straight away. It's perfect for experimenting. Leave with `exit()` or Ctrl+D.

```python
>>> 10 * 3
30
```

**A script file.** Code saved in a `.py` file runs from top to bottom with `uv run --python 3.14 path/to/file.py`. This is how real programs run, and it's how you run the exercises.

One difference to remember: the prompt shows the result of every line automatically, but a script only shows what you `print()`.

## 1.2 Values and types

Every piece of data in Python is a **value**, and every value has a **type**. The three you'll meet first:

| Type | Name in Python | Examples |
|---|---|---|
| Text | `str` (string) | `"198.51.100.7"`, `'hello'` |
| Whole number | `int` (integer) | `42`, `-1`, `0` |
| Decimal number | `float` | `3.14`, `0.5` |

You can ask Python for a value's type:

```python
>>> type("hello")
<class 'str'>
>>> type(42)
<class 'int'>
```

Strings can use single or double quotes; they mean the same thing. This course uses double quotes.

**Watch out:** `"42"` (with quotes) is a string, not a number. `"4" + "2"` gives `"42"`, while `4 + 2` gives `6`.

## 1.3 Variables

A variable is a name that refers to a value:

```python
ip = "198.51.100.7"
port = 443
```

- `=` means **assign** ("store this under this name"), not "is equal to".
- Names can contain letters, digits and underscores, but can't start with a digit. Python style is `lower_case_with_underscores`.
- Names are case-sensitive: `ip` and `IP` are different variables.
- You can reassign a variable at any time: `ip = "203.0.113.9"`.

Using a name you haven't assigned yet gives a `NameError`. It's almost always a typo.

## 1.4 f-strings

An f-string is a string with an `f` before the opening quote. Anything in `{curly braces}` is replaced with its value:

```python
kind = "ipv4-addr"
value = "198.51.100.7"
f"{kind}|{value}"          # 'ipv4-addr|198.51.100.7'
f"Found {2 + 3} matches"   # 'Found 5 matches'  (any expression works)
```

Forgetting the `f` is a classic mistake: `"{kind}"` is literally the text `{kind}`.

## 1.5 String methods

A **method** is a function that belongs to a value. You call it with a dot. Strings have dozens; these are the first ones worth knowing:

| Method | What it does | Example | Result |
|---|---|---|---|
| `.strip()` | removes spaces (and tabs and newlines) at both ends | `"  hi  ".strip()` | `"hi"` |
| `.lower()` | makes letters lowercase | `"EVIL.Example".lower()` | `"evil.example"` |
| `.upper()` | makes letters uppercase | `"tlp:red".upper()` | `"TLP:RED"` |
| `.replace(a, b)` | swaps every `a` for `b` | `"a-b".replace("-", ".")` | `"a.b"` |
| `.startswith(x)` | is `x` at the start? | `"https://x".startswith("https")` | `True` |

Methods never change the original string. They give you back a **new** one. So this does nothing useful:

```python
value = "  EVIL.Example "
value.strip()      # makes a new string... and throws it away
value              # still '  EVIL.Example '
```

and this does what you meant:

```python
value = value.strip()
```

You can **chain** methods because each one returns a string: `value.strip().lower()`.

## 1.6 Functions

A function packages a few lines of code under a name, so you can reuse them:

```python
def make_key(kind, value):
    return f"{kind}|{value}"
```

- `def` starts the definition, followed by the name, the **parameters** in brackets, and a colon.
- The **body** is indented by 4 spaces. Python uses indentation, not brackets, to know what belongs inside.
- `return` hands a result back to whoever called the function and ends the function.
- Calling it: `make_key("domain-name", "evil.example")` gives `"domain-name|evil.example"`. The values you pass in are called **arguments**.

A function without `return` gives back the special value `None`, meaning "nothing". If your function seems to return `None`, check you didn't forget `return`.

**Why bother with functions?** Once `clean()` exists, every part of ThreatDesk can use it, and if you ever improve it, the whole product improves at once.

## 1.7 Reading error messages

Errors are Python telling you exactly what confused it. Read from the **bottom up**:

```
  File "exercise.py", line 12
    return f"Indicator: {value}
           ^
SyntaxError: unterminated f-string literal (detected at line 12)
```

The last line names the problem (a string with no closing quote), and the lines above show where. The most common beginner errors:

| Error | Usual cause |
|---|---|
| `SyntaxError` | a missing quote, bracket or colon |
| `IndentationError` | the body of a function isn't indented by 4 spaces |
| `NameError` | a misspelled name, or using a variable before assigning it |
| `TypeError` | mixing types, such as `"Port " + 443` (use an f-string instead) |

## 1.8 ThreatDesk code after Chapter 1

```python
def clean(value):
    return value.strip().lower()


def make_key(kind, value):
    return f"{kind}|{value}"
```

```python
>>> make_key("domain-name", clean("  EVIL.Example "))
'domain-name|evil.example'
```

Two lines of code, and ThreatDesk can already treat `"  EVIL.Example "` and `"evil.example"` as the same indicator. That idea, **normalising** messy input before comparing it, runs through the whole product.

## Key takeaways

- The REPL is for experiments; `.py` files are for programs.
- Strings are text in quotes; `=` stores a value under a name.
- f-strings put values into text: `f"{kind}|{value}"`.
- String methods return new strings; assign the result if you want to keep it.
- A function is `def name(parameters):` plus an indented body that `return`s a result.
- Error messages are helpful. Read the last line first.
