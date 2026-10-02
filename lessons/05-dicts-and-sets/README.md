# Lesson 5: Dictionaries and sets

Halfway through Module 1, and ThreatDesk can already read STIX patterns. Today it gets two new containers that real products use constantly:

- a **dictionary** to describe one indicator with **named** fields, instead of remembering that position 0 is the type and position 2 is the value;
- a **set** to answer "have I seen this before?" instantly, even with millions of items. (This is the fix for slow de-duplication I mentioned after lesson 3.)

**What you'll build today:** a mini ingest pipeline. It takes a list of raw STIX patterns, skips the broken ones, drops duplicates and produces clean indicator records.

---

## Part 1: Dictionaries (10 minutes)

A **dictionary** (`dict`) stores **key: value** pairs inside curly braces:

```python
>>> indicator = {"type": "ipv4-addr", "value": "198.51.100.7"}
>>> indicator["type"]
'ipv4-addr'
>>> indicator["value"]
'198.51.100.7'
```

You look things up by **name** (the key) instead of by position. Compare:

```python
parsed[2]               # tuple: what was position 2 again?
indicator["value"]      # dict: obvious
```

Adding or changing a field uses the same square brackets:

```python
>>> indicator["source"] = "demo-feed"
>>> indicator
{'type': 'ipv4-addr', 'value': '198.51.100.7', 'source': 'demo-feed'}
```

Asking for a key that doesn't exist gives a `KeyError`. When a key might be missing, `.get()` lets you supply a fallback instead:

```python
>>> indicator.get("confidence", 0)
0
```

And `in` checks whether a **key** exists: `"type" in indicator` is `True`.

## Part 2: Using dict values in f-strings (2 minutes)

```python
>>> f"{indicator['type']} {indicator['value']}"
'ipv4-addr 198.51.100.7'
```

Use single quotes for the key inside a double-quoted f-string, so the quotes don't get mixed up.

## Part 3: Counting with a dict (5 minutes)

A very common pattern: keep a running count for each thing you see.

```python
counts = {}
for colour in ["red", "blue", "red"]:
    counts[colour] = counts.get(colour, 0) + 1
```

```python
>>> counts
{'red': 2, 'blue': 1}
```

Read the middle line as: "this colour's count is its old count (or 0 if it's new) plus 1".

## Part 4: Sets (10 minutes)

A **set** is a collection with **no duplicates** and no order. Create an empty one with `set()` (not `{}`, which makes an empty dict):

```python
>>> seen = set()
>>> seen.add("evil.example")
>>> seen.add("evil.example")      # adding it again does nothing
>>> seen
{'evil.example'}
>>> "evil.example" in seen
True
```

Why not just use a list? Checking `x in some_list` looks at every item one by one, so it gets slower as the list grows. Checking `x in some_set` takes the same tiny amount of time whether the set holds 10 items or 10 million. That's why real systems use sets for "have I seen this?" questions.

Sets don't keep order, so to remove duplicates **and** keep the original order, combine a set (for the fast check) with a list (for the order):

```python
def unique_words(words):
    seen = set()
    result = []
    for word in words:
        if word not in seen:
            seen.add(word)
            result.append(word)
    return result
```

## Part 5: A list of dictionaries (3 minutes)

Real data usually looks like a **list of dicts**, one dict per record:

```python
indicators = [
    {"type": "ipv4-addr", "value": "198.51.100.7"},
    {"type": "domain-name", "value": "evil.example"},
]
for ind in indicators:
    print(ind["value"])
```

This is exactly the shape of the JSON that threat feeds send, which ThreatDesk will read in a later lesson.

---

## Exercise: a mini ingest pipeline

Open `lessons/05-dicts-and-sets/exercise.py`. Your `parse_pattern()` from lesson 4 is at the top, ready to use.

```bash
uv run --python 3.14 lessons/05-dicts-and-sets/exercise.py
```

| Step | Function | Returns |
|---|---|---|
| 1 | `to_indicator(parsed)` | a dict with `type`, `property`, `value` and `key` (type and value joined by a pipe) |
| 2 | `describe(indicator)` | text like `"ipv4-addr 198.51.100.7"` |
| 3 | `unique_values(values)` | values in order, no repeats, using a set |
| 4 | `count_by_type(indicators)` | a dict like `{"ipv4-addr": 2, "domain-name": 1}` |
| 5 | `ingest(patterns)` | a list of indicator dicts: broken patterns skipped, duplicates (same `key`) dropped |

Step 5 brings everything together. A plan:

1. Start with `seen = set()` and `result = []`.
2. Loop over the patterns. Parse each one with `parse_pattern()`.
3. If the result `is None`, skip it with `continue` (it jumps straight to the next round of the loop).
4. Turn it into an indicator with `to_indicator()`.
5. If its `"key"` is already in `seen`, skip it. Otherwise add the key to `seen` and the indicator to `result`.
6. After the loop, return `result`.

When everything passes, compare with [`solutions/05-dicts-and-sets/solution.py`](../../solutions/05-dicts-and-sets/solution.py).

## Stretch goal

Write `remove_allowed(indicators, allow_list)`, which drops any indicator whose value is in an allow-list (for example, your own company's domains, which should never be flagged). Turn `allow_list` into a set first with `set(allow_list)`.

## If you get stuck

- `KeyError: 'value'`: the key you asked for isn't in the dict. Print the dict to see what keys it really has (and check the spelling).
- `TypeError: unhashable type: 'dict'`: you tried to put a dict into a set. Sets can only hold unchangeable things like strings, numbers and tuples. Add the indicator's `key` string instead.
- Made `{}` and wondered why `.add()` fails? `{}` is an empty **dict**. Use `set()`.

## Why this matters for ThreatDesk

Many threat feeds overlap: the same malicious IP can arrive from five sources in one hour. Without de-duplication, ThreatDesk would raise five alerts for one threat. Normalising, building a `key`, and checking it against a set is how real threat intelligence platforms keep their data clean.
