"""Lesson 5 exercise: dictionaries and sets.

Run from the repo root:
    uv run --python 3.14 lessons/05-dicts-and-sets/exercise.py
"""


# --- From lesson 4 (ready to use, no need to change) -------------------------
def parse_pattern(pattern):
    """Return (object_type, prop, value) for a simple STIX pattern, or None."""
    p = pattern.strip()
    if not (p.startswith("[") and p.endswith("]")):
        return None
    left, _, right = p[1:-1].partition("=")
    left, right = left.strip(), right.strip()
    if not (len(right) >= 2 and right.startswith("'") and right.endswith("'")):
        return None
    object_type, _, prop = left.partition(":")
    object_type, prop, value = object_type.strip(), prop.strip(), right[1:-1]
    if object_type == "" or prop == "" or value == "":
        return None
    return object_type, prop, value
# ---------------------------------------------------------------------------


# Step 1: turn a parsed tuple (object_type, prop, value) into a dict with the
# keys "type", "property", "value" and "key". The "key" is "type|value".
# Example: to_indicator(("ipv4-addr", "value", "198.51.100.7")) should give
#   {"type": "ipv4-addr", "property": "value", "value": "198.51.100.7",
#    "key": "ipv4-addr|198.51.100.7"}
def to_indicator(parsed):
    type, prop, value = parsed
    return {"type": type, "property": prop, "value": value, "key": f"{type}|{value}"}


# Step 2: return the indicator's type and value with a space between them.
# Example: describe({"type": "ipv4-addr", "value": "198.51.100.7", ...})
#          should give "ipv4-addr 198.51.100.7"
def describe(indicator):
    return f"{indicator['type']} {indicator['value']}"


# Step 3: return the values in their original order with repeats removed.
# Use a set called seen for the "have I seen this?" check.
# Example: unique_values(["a", "b", "a"]) should give ["a", "b"]
def unique_values(values):
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


# Step 4: count how many indicators there are of each type.
# Example: for two ipv4-addr and one domain-name indicators, should give
#   {"ipv4-addr": 2, "domain-name": 1}
def count_by_type(indicators):
    counts = {}
    for ind in indicators:
        counts[ind["type"]] = counts.get(ind["type"], 0) + 1
    return counts


# Step 5: turn a list of raw STIX patterns into a list of indicator dicts.
# Skip patterns that parse_pattern() can't read, and skip indicators whose
# "key" you've already seen. Follow the 6-line plan in the lesson README.
def ingest(patterns):
    seen_keys = set()
    indicators = []
    for pattern in patterns:
        parsed = parse_pattern(pattern)
        if parsed is None:
            continue
        indicator = to_indicator(parsed)
        if indicator["key"] not in seen_keys:
            seen_keys.add(indicator["key"])
            indicators.append(indicator)
    return indicators


# ---------------------------------------------------------------------------
# The checker. You don't need to read or change anything below this line.
# ---------------------------------------------------------------------------
IP = {"type": "ipv4-addr", "property": "value", "value": "198.51.100.7",
      "key": "ipv4-addr|198.51.100.7"}
IP2 = {"type": "ipv4-addr", "property": "value", "value": "203.0.113.9",
       "key": "ipv4-addr|203.0.113.9"}
DOM = {"type": "domain-name", "property": "value", "value": "evil.example",
       "key": "domain-name|evil.example"}

PATTERNS = [
    "[ipv4-addr:value = '198.51.100.7']",
    "[domain-name:value = 'evil.example']",
    "not a pattern",
    "[ipv4-addr:value = '198.51.100.7']",
    "[ipv4-addr:value = 203.0.113.9]",
    "[ipv4-addr:value = '203.0.113.9']",
]

STEPS = [
    (
        to_indicator,
        [((("ipv4-addr", "value", "198.51.100.7"),), IP),
         ((("domain-name", "value", "evil.example"),), DOM)],
        "Unpack first:  object_type, prop, value = parsed   then return a dict like  "
        '{"type": object_type, "property": prop, ...}  with  "key": f"{object_type}|{value}"',
    ),
    (
        describe,
        [((IP,), "ipv4-addr 198.51.100.7"), ((DOM,), "domain-name evil.example")],
        "return f\"{indicator['type']} {indicator['value']}\"",
    ),
    (
        unique_values,
        [((["a", "b", "a", "c", "b"],), ["a", "b", "c"]), (([],), [])],
        "Same as unique_words() in Part 4: a set called seen, a list called result, "
        "and  if value not in seen:  inside the loop",
    ),
    (
        count_by_type,
        [(([IP, IP2, DOM],), {"ipv4-addr": 2, "domain-name": 1}), (([],), {})],
        "Start with counts = {}, loop, and inside:  "
        "counts[ind[\"type\"]] = counts.get(ind[\"type\"], 0) + 1",
    ),
    (
        ingest,
        [((PATTERNS,), [IP, DOM, IP2]), (([],), [])],
        "Follow the 6-line plan in the README. Inside the loop, start with  "
        "parsed = parse_pattern(pattern)  and  if parsed is None:  continue",
    ),
]


def show_call(func, args):
    text = f"{func.__name__}({', '.join(repr(a) for a in args)})"
    return text if len(text) < 120 else text[:117] + "..."


def main():
    for number, (func, cases, hint) in enumerate(STEPS, start=1):
        for args, expected in cases:
            got = func(*args)
            if got != expected:
                print(f"Step {number} is next.")
                print(f"  {show_call(func, args)}")
                print(f"  should give {expected!r}")
                print(f"  right now it gives {got!r}")
                print(f"  Hint: {hint}")
                print(f"\n{number - 1} of {len(STEPS)} steps done. Keep going!")
                return
        print(f"Step {number} passed ✓")
    print(f"\nAll {len(STEPS)} steps done. 🎉 ThreatDesk has its first ingest pipeline!")


if __name__ == "__main__":
    main()
