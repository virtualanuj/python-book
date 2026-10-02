"""Lesson 3 exercise: lists and loops.

Run from the repo root:
    uv run --python 3.14 lessons/03-lists-and-loops/exercise.py
"""


# --- Helpers from earlier lessons (ready to use, no need to change) ---------
def clean(value):
    return value.strip().lower()


def guess_kind(value):
    if value.startswith("http://") or value.startswith("https://"):
        return "url"
    elif "@" in value:
        return "email-addr"
    elif value.count(".") == 3 and value.replace(".", "").isdigit():
        return "ipv4-addr"
    else:
        return "domain-name"
# ---------------------------------------------------------------------------


# Step 1: return the first item in the list.
# Example: first_item(["a", "b", "c"]) should give "a"
def first_item(values):
    return None


# Step 2: return how many items are in the list.
# Example: how_many(["a", "b", "c"]) should give 3
def how_many(values):
    return None


# Step 3: return a NEW list with clean() applied to every item.
# Example: clean_all(["  A.Example", "B.EXAMPLE "]) should give ["a.example", "b.example"]
def clean_all(values):
    result = []
    # your loop goes here
    return result


# Step 4: return a new list with only the items whose guess_kind() equals kind.
# Example: only_kind(["198.51.100.7", "evil.example"], "ipv4-addr") should give ["198.51.100.7"]
def only_kind(values, kind):
    result = []
    # your loop goes here
    return result


# Step 5: return a new list with the same items in the same order, but each
# value only once.
# Example: without_duplicates(["a", "b", "a", "c", "b"]) should give ["a", "b", "c"]
def without_duplicates(values):
    result = []
    # your loop goes here
    return result


# ---------------------------------------------------------------------------
# The checker. You don't need to read or change anything below this line.
# ---------------------------------------------------------------------------
FEED = ["198.51.100.7", "evil.example", "https://login.bad.example",
        "payroll@phish.example", "203.0.113.9"]

STEPS = [
    (
        first_item,
        [((FEED,), "198.51.100.7"), ((["only-one.example"],), "only-one.example")],
        "Positions start at 0, so the first item is  values[0]",
    ),
    (
        how_many,
        [((FEED,), 5), (([],), 0)],
        "len() counts the items in a list:  return len(values)",
    ),
    (
        clean_all,
        [((["  A.Example", "B.EXAMPLE "],), ["a.example", "b.example"]), (([],), [])],
        "Inside the loop:  for value in values:  then (indented)  result.append(clean(value))",
    ),
    (
        only_kind,
        [((FEED, "ipv4-addr"), ["198.51.100.7", "203.0.113.9"]),
         ((FEED, "url"), ["https://login.bad.example"]),
         ((FEED, "ipv6-addr"), [])],
        "Loop over values, and inside the loop add  if guess_kind(value) == kind:  "
        "with  result.append(value)  indented below it",
    ),
    (
        without_duplicates,
        [((["a", "b", "a", "c", "b"],), ["a", "b", "c"]),
         ((["198.51.100.7", "198.51.100.7"],), ["198.51.100.7"]),
         (([],), [])],
        "Inside the loop:  if value not in result:  then (indented)  result.append(value)",
    ),
]


def show_call(func, args):
    return f"{func.__name__}({', '.join(repr(a) for a in args)})"


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
    print(f"\nAll {len(STEPS)} steps done. 🎉 ThreatDesk can now process a whole feed!")


if __name__ == "__main__":
    main()
