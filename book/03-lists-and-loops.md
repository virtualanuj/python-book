# Chapter 3: Lists and loops

> ThreatDesk gains: `clean_all()`, `only_kind()` and `without_duplicates()`, the first stage of an ingest pipeline that turns a messy batch of values into a tidy one.

## 3.1 Lists

A **list** is an ordered collection of values, written in square brackets:

```python
feed = ["198.51.100.7", "evil.example", "https://login.bad.example"]
empty = []
```

- Lists keep their **order**: items stay where you put them.
- Lists can hold **duplicates**: `["a", "a"]` is fine.
- Lists can hold any type, even a mix: `["evil.example", 443, True]`. In practice, keep each list to one kind of thing.
- `len(feed)` gives the number of items.

## 3.2 Indexes

Each item has a position, its **index**, starting at **0**:

```
feed = ["198.51.100.7", "evil.example", "https://login.bad.example"]
index:        0               1                    2
negative:    -3              -2                   -1
```

```python
feed[0]     # '198.51.100.7'
feed[-1]    # 'https://login.bad.example'  (last item)
feed[3]     # IndexError: list index out of range
```

Why start at 0? The index measures "how many steps from the start". The first item is zero steps away. Almost every programming language works this way, so it's worth getting used to.

You can also replace an item by assigning to its index: `feed[1] = "other.example"`.

## 3.3 Asking about lists

| Expression | Result |
|---|---|
| `"evil.example" in feed` | `True` if the value is in the list |
| `"x" not in feed` | `True` if it isn't |
| `len(feed)` | number of items |
| `feed.count("evil.example")` | how many times a value appears |

`in` on a list checks each item in turn until it finds a match. For a few hundred items that's instant. For millions it gets slow, and Chapter 5 introduces **sets**, which answer `in` almost instantly no matter how big they are.

## 3.4 Changing lists

| Method | What it does |
|---|---|
| `items.append(x)` | adds `x` to the end |
| `items.insert(0, x)` | adds `x` at position 0 (the front) |
| `items.remove(x)` | removes the first `x` it finds |
| `items.pop()` | removes and returns the last item |
| `items.sort()` | sorts the list in place |

**Important difference from strings:** strings can never change, so string methods return a new string. Lists **can** change, so most list methods change the list itself and return `None`:

```python
found = []
found = found.append("x")    # wrong: found is now None
found.append("x")            # right
```

## 3.5 for loops

```python
for value in feed:
    print(value)
```

- `for NAME in LIST:` runs the indented block once per item, with `NAME` set to the current item.
- When the list runs out, the loop ends and Python carries on with the next unindented line.
- Looping over an empty list runs the block zero times. That's not an error.

Loops also work on strings (one character at a time) and many other things you'll meet later. Anything you can loop over is called an **iterable**.

## 3.6 The build-a-new-list pattern

```python
def clean_all(values):
    result = []
    for value in values:
        result.append(clean(value))
    return result
```

Four parts: start empty, loop, append, return after the loop. Add an `if` inside the loop to **filter**:

```python
def only_kind(values, kind):
    result = []
    for value in values:
        if guess_kind(value) == kind:
            result.append(value)
    return result
```

### Indentation decides what's inside

```python
for value in values:
    result.append(value)
    return result        # wrong: inside the loop, returns after the FIRST item
```

```python
for value in values:
    result.append(value)
return result            # right: after the loop has finished
```

This is the most common loop bug. If a function gives back only one item, check the indentation of `return`.

## 3.7 Removing duplicates while keeping order

```python
def without_duplicates(values):
    result = []
    for value in values:
        if value not in result:
            result.append(value)
    return result
```

The first time a value appears, it's not in `result` yet, so it's added. Every later copy is already there and is skipped. The original order is kept, which matters for ThreatDesk: the first time an indicator was seen is useful information.

Notice the order of operations in the pipeline: **clean first, then de-duplicate**. `"Evil.Example"` and `"evil.example "` only become duplicates after cleaning.

## 3.8 A preview: list comprehensions

Python has a compact way to write the build-a-new-list pattern on one line:

```python
cleaned = [clean(value) for value in values]
ips = [value for value in values if guess_kind(value) == "ipv4-addr"]
```

Read it as "a list of `clean(value)` for each value in values". It does exactly what the four-line loop does. Use whichever you find clearer for now; Chapter 5 practises comprehensions properly.

## 3.9 ThreatDesk code after Chapter 3

```python
def clean_all(values):
    result = []
    for value in values:
        result.append(clean(value))
    return result


def only_kind(values, kind):
    result = []
    for value in values:
        if guess_kind(value) == kind:
            result.append(value)
    return result


def without_duplicates(values):
    result = []
    for value in values:
        if value not in result:
            result.append(value)
    return result
```

The pipeline so far:

```python
>>> raw = ["  198.51.100.7", "Evil.Example", "evil.example ", "https://login.bad.example"]
>>> values = without_duplicates(clean_all(raw))
>>> values
['198.51.100.7', 'evil.example', 'https://login.bad.example']
>>> only_kind(values, "domain-name")
['evil.example']
```

## Key takeaways

- A list holds values in order; indexes start at 0, and `-1` is the last item.
- `.append()` changes the list itself; don't assign its result.
- `for item in items:` runs the block once per item.
- Build new lists with: empty list, loop, (optional `if`), append, return after the loop.
- Clean before you de-duplicate.
