# Lesson 3: Lists and loops

Two lessons down! So far your functions have handled **one** value at a time. Real threat feeds send hundreds or thousands. Today you'll learn how to hold many values together and work through them one by one.

**What you'll build today:** ThreatDesk learns to clean a whole batch of indicators, pick out the ones of a certain kind, and drop duplicates.

**What you'll learn:** lists, indexes, `len()`, `for` loops, and building a new list with `.append()`.

---

## Part 1: Lists (5 minutes)

A **list** holds several values in order. You write it with square brackets and commas:

```python
>>> feed = ["198.51.100.7", "evil.example", "https://login.bad.example"]
>>> feed
['198.51.100.7', 'evil.example', 'https://login.bad.example']
>>> len(feed)          # how many items?
3
```

A list can be empty, too: `[]`.

## Part 2: Getting items out (5 minutes)

Each item has a position number called an **index**. Python starts counting at **0**, not 1:

```python
>>> feed[0]            # the first item
'198.51.100.7'
>>> feed[1]            # the second item
'evil.example'
>>> feed[-1]           # negative counts from the end: the last item
'https://login.bad.example'
```

Asking for a position that doesn't exist, like `feed[10]`, gives an `IndexError`.

You can ask whether something is in a list with `in`, just like with strings:

```python
>>> "evil.example" in feed
True
```

## Part 3: Adding items (5 minutes)

`.append()` adds an item to the end of a list:

```python
>>> found = []
>>> found.append("198.51.100.7")
>>> found.append("evil.example")
>>> found
['198.51.100.7', 'evil.example']
```

Unlike string methods, `.append()` **changes the list itself**. You don't need to write `found = found.append(...)` (in fact, that would break it, because `.append()` returns `None`).

## Part 4: Loops (10 minutes)

A `for` loop runs the same code once for **each item** in a list:

```python
>>> for value in feed:
...     print(f"Checking {value}")
...
Checking 198.51.100.7
Checking evil.example
Checking https://login.bad.example
```

(In the prompt you'll see `...` on the indented line. Press Enter on an empty line to run the loop.)

Reading it: "for each `value` in `feed`, do the indented lines". On the first round `value` is `"198.51.100.7"`, on the second it's `"evil.example"`, and so on. The name `value` is your choice; pick something that describes one item.

## Part 5: The build-a-new-list pattern (10 minutes)

This pattern is used everywhere in Python, so it's worth learning by heart:

```python
def shout_all(words):
    result = []                    # 1. start with an empty list
    for word in words:             # 2. go through each item
        result.append(word.upper())   # 3. add the changed item
    return result                  # 4. hand back the new list
```

```python
>>> shout_all(["hi", "there"])
['HI', 'THERE']
```

And you can combine it with `if` from lesson 2 to **keep only some** items:

```python
def only_long(words):
    result = []
    for word in words:
        if len(word) > 5:
            result.append(word)
    return result
```

Watch the indentation: `result.append(word)` is inside the `if`, which is inside the `for`. And `return result` sits at the same level as `for`, so it runs once, **after** the loop finishes.

---

## Exercise: handle a whole feed

Open `lessons/03-lists-and-loops/exercise.py`. At the top you'll find `clean()` and `guess_kind()` from your earlier lessons, ready to use. Below them are five functions to fill in.

```bash
uv run --python 3.14 lessons/03-lists-and-loops/exercise.py
```

| Step | Function | Returns |
|---|---|---|
| 1 | `first_item(values)` | the first item in the list |
| 2 | `how_many(values)` | how many items are in the list |
| 3 | `clean_all(values)` | a new list with `clean()` applied to every item |
| 4 | `only_kind(values, kind)` | only the items whose `guess_kind()` matches `kind` |
| 5 | `without_duplicates(values)` | the items in the same order, with repeats removed |

Steps 3 to 5 all use the build-a-new-list pattern from Part 5. For step 5, think about this: before adding a value to `result`, how could you check whether it's **already in** `result`?

When everything passes, compare with [`solutions/03-lists-and-loops/solution.py`](../../solutions/03-lists-and-loops/solution.py).

## If you get stuck

- Your function returns only one item: `return result` is probably indented inside the loop, so it returns on the first round. Move it back to line up with `for`.
- `AttributeError: 'NoneType' object has no attribute 'append'`: you wrote `result = result.append(...)`. Just write `result.append(...)`.
- `IndexError: list index out of range`: you asked for a position that doesn't exist.

## Why this matters for ThreatDesk

A feed pull gives ThreatDesk a big list of raw values. Cleaning them, sorting them by kind and dropping duplicates is exactly the first stage of the real ingest pipeline. You're building it now, one loop at a time.
