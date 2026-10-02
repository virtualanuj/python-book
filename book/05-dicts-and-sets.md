# Chapter 5: Dictionaries and sets

> ThreatDesk gains: indicator records as dictionaries, fast de-duplication with sets, counts by type, and `ingest()`, a mini pipeline from raw STIX patterns to clean, unique indicators.

## 5.1 Dictionaries

A dictionary maps **keys** to **values**:

```python
indicator = {
    "type": "ipv4-addr",
    "property": "value",
    "value": "198.51.100.7",
    "key": "ipv4-addr|198.51.100.7",
}
```

| Operation | Example | Notes |
|---|---|---|
| read | `indicator["type"]` | `KeyError` if the key is missing |
| read safely | `indicator.get("confidence", 0)` | returns the fallback (or `None`) if missing |
| add or change | `indicator["source"] = "demo-feed"` | creates the key if it's new |
| remove | `del indicator["source"]` | `KeyError` if missing |
| does key exist? | `"type" in indicator` | checks **keys**, not values |
| how many pairs? | `len(indicator)` | |

Keys are usually strings, but any unchangeable value works (numbers, tuples). Values can be anything, including lists and other dicts.

Dictionaries **remember insertion order**: when you loop over one or print it, the keys come out in the order they were added.

### Tuple or dict?

Lesson 4's `parse_pattern()` returned a tuple: `("ipv4-addr", "value", "198.51.100.7")`. That works, but every reader has to remember what position 2 means. A dict names each field, so `indicator["value"]` explains itself. Use tuples for small, fixed groups that are unpacked straight away; use dicts (and later, dataclasses) for records that travel around a program.

## 5.2 Looping over dictionaries

```python
for key in indicator:                  # keys
    print(key)

for key, value in indicator.items():   # key and value together
    print(f"{key} = {value}")

indicator.keys()      # all keys
indicator.values()    # all values
```

## 5.3 Counting with get()

```python
counts = {}
for ind in indicators:
    counts[ind["type"]] = counts.get(ind["type"], 0) + 1
```

`counts.get(t, 0)` gives the current count, or 0 the first time a type appears. This pattern is so common that the standard library has a ready-made tool for it, `collections.Counter`, which you'll meet once we cover imports:

```python
from collections import Counter
Counter(ind["type"] for ind in indicators)
```

## 5.4 Sets

A set is an unordered collection of **unique** items:

```python
seen = set()            # empty set ({} would be an empty dict)
seen.add("evil.example")
seen.add("evil.example")   # no effect: already there
"evil.example" in seen     # True
tlp = {"red", "amber", "green", "clear"}   # a set literal
```

| Operation | Example |
|---|---|
| add one item | `s.add(x)` |
| remove one item | `s.discard(x)` (no error if missing) |
| membership | `x in s` |
| from a list | `set(values)` (duplicates vanish, order is lost) |
| in both | `a & b` (intersection) |
| in either | `a \| b` (union) |
| in a but not b | `a - b` (difference) |

The set operations are handy for questions like "which indicators appear in **both** feeds?" (`feed_a & feed_b`), which Chapter 39 uses to measure feed overlap.

### Why sets are fast

`x in some_list` checks items one by one, so the time grows with the list's length. A set stores items using a **hash**, a number computed from the value that tells Python exactly where to look. So `x in some_set` takes about the same time for ten items or ten million. Dict key lookups work the same way, which is why `key in some_dict` is fast too.

The catch: only **hashable** (unchangeable) values can go in a set or be dict keys. Strings, numbers and tuples are fine. Lists and dicts are not, and trying gives `TypeError: unhashable type`.

## 5.5 Ordered de-duplication

```python
def unique_values(values):
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
```

The set answers "seen it?" quickly; the list keeps the original order. A neat one-line alternative relies on dicts keeping insertion order: `list(dict.fromkeys(values))`.

## 5.6 continue

`continue` skips the rest of the current loop round and moves to the next item. It's the loop version of an early return:

```python
for pattern in patterns:
    parsed = parse_pattern(pattern)
    if parsed is None:
        continue          # broken: move on to the next pattern
    ...
```

Its sibling `break` stops the whole loop immediately.

## 5.7 ThreatDesk code after Chapter 5

```python
def to_indicator(parsed):
    object_type, prop, value = parsed
    return {
        "type": object_type,
        "property": prop,
        "value": value,
        "key": f"{object_type}|{value}",
    }


def count_by_type(indicators):
    counts = {}
    for ind in indicators:
        counts[ind["type"]] = counts.get(ind["type"], 0) + 1
    return counts


def ingest(patterns):
    seen = set()
    result = []
    for pattern in patterns:
        parsed = parse_pattern(pattern)
        if parsed is None:
            continue
        indicator = to_indicator(parsed)
        if indicator["key"] in seen:
            continue
        seen.add(indicator["key"])
        result.append(indicator)
    return result


def remove_allowed(indicators, allow_list):
    allowed = set(allow_list)
    return [ind for ind in indicators if ind["value"] not in allowed]
```

```python
>>> feed = ["[ipv4-addr:value = '198.51.100.7']", "broken",
...         "[ipv4-addr:value = '198.51.100.7']"]
>>> ingest(feed)
[{'type': 'ipv4-addr', 'property': 'value', 'value': '198.51.100.7', 'key': 'ipv4-addr|198.51.100.7'}]
```

### Design decisions recorded

- An indicator is identified by its **key**, `type|value`. Two feeds reporting the same IP produce the same key, so ThreatDesk stores it once.
- Broken patterns are skipped silently for now. That's not good enough for a real product (you'd want to know which feed sent garbage); Chapter 6 adds errors and Chapter 22 adds logging.
- Allow-lists are converted to a set once, before the loop, not on every check.

## Key takeaways

- Dicts store named fields: `d["key"]` to read, `d.get("key", default)` to read safely.
- `counts[k] = counts.get(k, 0) + 1` is the classic counting pattern.
- Sets hold unique items and answer `in` almost instantly; `set()` makes an empty one.
- Combine a set (fast check) with a list (order) for ordered de-duplication.
- `continue` skips to the next loop round; `break` leaves the loop.
- Only unchangeable values can be set items or dict keys.
