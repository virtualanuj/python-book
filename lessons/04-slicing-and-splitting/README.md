# Lesson 4: Slicing and splitting text

You're flying through these! Today ThreatDesk reads its first piece of **real threat intelligence format**.

Threat feeds describe what to look for using **STIX patterns**. They look like this:

```
[ipv4-addr:value = '198.51.100.7']
[domain-name:value = 'update.malware.example']
```

Read it as: "look for an `ipv4-addr` whose `value` is `198.51.100.7`". Your job today is to take that string apart into its three useful pieces:

```
[ipv4-addr:value = '198.51.100.7']
 ─────────  ─────   ────────────
   type    property     value
```

**What you'll learn:** slicing strings, `split()` and `partition()`, tuples, and using `None` to mean "this isn't valid".

---

## Part 1: Slicing (10 minutes)

In lesson 3 you used `values[0]` to get one item. Strings work the same way, one character at a time:

```python
>>> p = "[ipv4-addr]"
>>> p[0]
'['
>>> p[-1]
']'
```

A **slice** takes a range of characters with `[start:stop]`. It includes `start` but **stops just before** `stop`:

```python
>>> word = "ThreatDesk"
>>> word[0:6]
'Threat'
>>> word[6:]          # leave out stop: go to the end
'Desk'
>>> word[:6]          # leave out start: begin at 0
'Threat'
>>> word[1:-1]        # from the second character to just before the last
'hreatDes'
```

That last one is the trick for removing brackets or quotes from both ends:

```python
>>> "[ipv4-addr]"[1:-1]
'ipv4-addr'
>>> "'198.51.100.7'"[1:-1]
'198.51.100.7'
```

Slices also work on lists: `feed[:2]` gives the first two items. (You already used `values[:i]` in lesson 3. Nice!)

## Part 2: Splitting (5 minutes)

`split()` cuts a string into a **list** of pieces:

```python
>>> "a b  c".split()               # no argument: split on any spaces
['a', 'b', 'c']
>>> "ipv4-addr:value".split(":")   # split on a specific character
['ipv4-addr', 'value']
```

## Part 3: partition, and tuples (10 minutes)

`partition()` splits **only at the first** match, and always gives back exactly three parts: before, the separator, after.

```python
>>> "ipv4-addr:value".partition(":")
('ipv4-addr', ':', 'value')
>>> "no-colon-here".partition(":")
('no-colon-here', '', '')
```

When the separator isn't found, the middle part is `""`, which makes it easy to check.

Those round brackets `( )` make a **tuple**. A tuple is like a list that can't be changed after it's made. You can **unpack** a tuple straight into variables, one per item:

```python
>>> before, sep, after = "ipv4-addr:value".partition(":")
>>> before
'ipv4-addr'
>>> after
'value'
```

Functions can return tuples too, which is a neat way to give back several things at once:

```python
def first_and_last(text):
    return text[0], text[-1]          # the commas make a tuple
```

```python
>>> first, last = first_and_last("ThreatDesk")
>>> first, last
('T', 'k')
```

## Part 4: None means "nothing" (5 minutes)

Sometimes a function can't give a sensible answer, for example when the input is broken. Python has a special value for this: `None`. It's not `""`, not `0`, not `False`. It just means "no value".

```python
def first_letter(text):
    if text == "":
        return None
    return text[0]
```

To check for it, use `is None`:

```python
>>> first_letter("") is None
True
```

(Notice there's no `else:` above. When the `if` returns, the function stops, so the last line only runs when the text isn't empty. This is called an **early return**, and it keeps code flat and easy to read.)

---

## Exercise: read a STIX pattern

Open `lessons/04-slicing-and-splitting/exercise.py`. Five steps, and each one builds on the ones before.

```bash
uv run --python 3.14 lessons/04-slicing-and-splitting/exercise.py
```

| Step | Function | Returns |
|---|---|---|
| 1 | `has_brackets(pattern)` | `True` if it starts with `[` and ends with `]` (ignore outside spaces) |
| 2 | `strip_brackets(pattern)` | the text between the brackets |
| 3 | `split_once(text, sep)` | a tuple `(before, after)`, each with spaces stripped |
| 4 | `is_quoted(text)` | `True` if it's at least 2 characters, starting and ending with `'` |
| 5 | `parse_pattern(pattern)` | a tuple `(type, property, value)`, or `None` if the pattern is broken |

Step 5 is the big one. Here's a plan you can follow line by line:

1. If the pattern doesn't have brackets, return `None`.
2. Strip the brackets, then `split_once` on `"="` into `left` and `right`.
3. If `right` isn't quoted, return `None`.
4. `split_once` the `left` side on `":"` into `object_type` and `prop`.
5. Remove the quotes from `right` to get `value`.
6. If any of `object_type`, `prop` or `value` is empty (`""`), return `None`.
7. Otherwise return `object_type, prop, value`.

When all five pass, compare with [`solutions/04-slicing-and-splitting/solution.py`](../../solutions/04-slicing-and-splitting/solution.py).

## If you get stuck

- `ValueError: not enough values to unpack`: the number of variables on the left of `=` doesn't match the number of items in the tuple. `partition()` always gives 3.
- Your slice is off by one: remember `[start:stop]` stops **before** `stop`.
- Can't tell what a value looks like? Add `print(repr(value))` inside your function and run it. `repr` shows the quotes, so stray spaces become visible. Remove the print when you're done.

## Why this matters for ThreatDesk

Threat feeds come from outside your organisation, so they are **untrusted input**. They can be badly formatted or even deliberately malicious. A good parser is strict: if it can't fully understand something, it says so (`None`) instead of guessing. You'll see this idea again and again in security products.
