"""Lesson 1 exercise: first steps.

Run from the repo root:
    uv run --python 3.14 lessons/01-first-steps/exercise.py

In each function, replace the line   return ""   with your own code.
"""


# Step 1: return the text "Welcome to ThreatDesk"
def welcome():
    return "Welcome to ThreatDesk"


# Step 2: return "Indicator: " followed by the value.
# Example: label("198.51.100.7") should give "Indicator: 198.51.100.7"
def label(value):
    return f"Indicator: {value}"


# Step 3: return the kind, then a | character, then the value.
# Example: make_key("ipv4-addr", "198.51.100.7") should give "ipv4-addr|198.51.100.7"
def make_key(kind, value):
    if not kind or not value:
        raise ValueError("kind and value must be non-empty strings")
    return f"{kind}|{value}"


# Step 4: return the value with spaces removed from both ends, in lowercase.
# Example: clean("  EVIL.Example ") should give "evil.example"
def clean(value):
    return value.strip().lower()


# ---------------------------------------------------------------------------
# The checker. You don't need to read or change anything below this line.
# ---------------------------------------------------------------------------
STEPS = [
    (
        "welcome()",
        lambda: welcome(),
        "Welcome to ThreatDesk",
        'Write the text in quotes after return:  return "Welcome to ThreatDesk"',
    ),
    (
        'label("198.51.100.7")',
        lambda: label("198.51.100.7"),
        "Indicator: 198.51.100.7",
        'Use an f-string with the value inside curly braces:  return f"Indicator: {value}"',
    ),
    (
        'make_key("ipv4-addr", "198.51.100.7")',
        lambda: make_key("ipv4-addr", "198.51.100.7"),
        "ipv4-addr|198.51.100.7",
        "An f-string can hold two values: put {kind}, then |, then {value} inside the quotes.",
    ),
    (
        'clean("  EVIL.Example ")',
        lambda: clean("  EVIL.Example "),
        "evil.example",
        "Chain two string methods:  return value.strip().lower()",
    ),
]


def main():
    for number, (call, run, expected, hint) in enumerate(STEPS, start=1):
        got = run()
        if got != expected:
            print(f"Step {number} is next.")
            print(f"  {call} should give {expected!r}")
            print(f"  right now it gives {got!r}")
            print(f"  Hint: {hint}")
            print(f"\n{number - 1} of {len(STEPS)} steps done. You've got this!")
            return
        print(f"Step {number} passed ✓")
    print(f"\nAll {len(STEPS)} steps done. 🎉 You just wrote your first Python functions!")


if __name__ == "__main__":
    main()
