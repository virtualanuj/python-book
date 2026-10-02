"""Lesson 4 exercise: read a STIX pattern.

Run from the repo root:
    uv run --python 3.14 lessons/04-slicing-and-splitting/exercise.py
"""


# Step 1: return True if the pattern (after removing outside spaces) starts
# with "[" and ends with "]".
# Example: has_brackets("  [ipv4-addr:value = '198.51.100.7'] ") should give True
def has_brackets(pattern):
    return pattern.strip().startswith("[") and pattern.strip().endswith("]")


# Step 2: return the text between the brackets (remove outside spaces first).
# Example: strip_brackets(" [abc] ") should give "abc"
def strip_brackets(pattern):
    return pattern.strip()[1:-1]


# Step 3: split text at the FIRST sep, and return a tuple (before, after),
# each with outside spaces removed. If sep isn't there, after is "".
# Example: split_once("ipv4-addr:value = 'x'", "=") should give ("ipv4-addr:value", "'x'")
def split_once(text, sep):
    before, _, after = text.partition(sep)
    return (before.strip(), after.strip())


# Step 4: return True if text is at least 2 characters long and starts AND
# ends with a single quote '.
# Example: is_quoted("'198.51.100.7'") should give True, is_quoted("198.51.100.7") False
def is_quoted(text):
    return len(text) >= 2 and text.startswith("'") and text.endswith("'")


# Step 5: return a tuple (object_type, prop, value), or None if the pattern is
# broken. Follow the 7-line plan in the lesson README. Use steps 1 to 4!
# Example: parse_pattern("[ipv4-addr:value = '198.51.100.7']")
#          should give ("ipv4-addr", "value", "198.51.100.7")
def parse_pattern(pattern):
    if not has_brackets(pattern):
        return None

    value = strip_brackets(pattern)
    left, right = split_once(value, "=")

    if not is_quoted(right) or right == "''":
        return None
    
    kind, prop = split_once(left, ":")

    if not prop or not kind:
        return None

    return (kind, prop, right[1:-1])

# ---------------------------------------------------------------------------
# The checker. You don't need to read or change anything below this line.
# ---------------------------------------------------------------------------
STEPS = [
    (
        has_brackets,
        [(("[ipv4-addr:value = '198.51.100.7']",), True),
         (("  [domain-name:value = 'a.example']  ",), True),
         (("ipv4-addr:value = '198.51.100.7'",), False),
         (("[missing-end",), False)],
        'Strip first, then check both ends:  p = pattern.strip()  then  '
        'return p.startswith("[") and p.endswith("]")',
    ),
    (
        strip_brackets,
        [(("[abc]",), "abc"), ((" [ipv4-addr:value = 'x'] ",), "ipv4-addr:value = 'x'")],
        "Strip the spaces, then slice off the first and last character:  "
        "return pattern.strip()[1:-1]",
    ),
    (
        split_once,
        [(("ipv4-addr:value = 'x'", "="), ("ipv4-addr:value", "'x'")),
         (("ipv4-addr:value", ":"), ("ipv4-addr", "value")),
         (("a=b=c", "="), ("a", "b=c")),
         (("no-equals", "="), ("no-equals", ""))],
        "before, found, after = text.partition(sep)   then   "
        "return before.strip(), after.strip()",
    ),
    (
        is_quoted,
        [(("'198.51.100.7'",), True), (("198.51.100.7",), False),
         (("'",), False), (("''",), True), (("'half",), False)],
        "Three checks joined with and:  len(text) >= 2  and  "
        "text.startswith(\"'\")  and  text.endswith(\"'\")",
    ),
    (
        parse_pattern,
        [(("[ipv4-addr:value = '198.51.100.7']",), ("ipv4-addr", "value", "198.51.100.7")),
         (("[domain-name:value='update.malware.example']",),
          ("domain-name", "value", "update.malware.example")),
         (("  [url:value = 'http://bad.example/a=b']  ",), ("url", "value", "http://bad.example/a=b")),
         (("ipv4-addr:value = '198.51.100.7'",), None),
         (("[ipv4-addr:value = 198.51.100.7]",), None),
         (("[ipv4-addr = '198.51.100.7']",), None),
         (("[ipv4-addr:value = '']",), None)],
        "Follow the 7-line plan in the README. Start with:  "
        "if not has_brackets(pattern):  then (indented)  return None",
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
    print(f"\nAll {len(STEPS)} steps done. 🎉 ThreatDesk can read STIX patterns!")


if __name__ == "__main__":
    main()
