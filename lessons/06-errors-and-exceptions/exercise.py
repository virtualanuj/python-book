"""Lesson 6 exercise: errors and exceptions.

Run from the repo root:
    uv run --python 3.14 lessons/06-errors-and-exceptions/exercise.py
"""


class PatternError(ValueError):
    """A STIX pattern could not be parsed."""


# --- From lesson 5 (ready to use, no need to change) -------------------------
def to_indicator(parsed: tuple[str, str, str]) -> dict[str, str]:
    object_type, prop, value = parsed
    return {"type": object_type, "property": prop, "value": value,
            "key": f"{object_type}|{value}"}
# ---------------------------------------------------------------------------


# Step 1: return int(text), or None if text isn't a whole number.
# Use try / except ValueError.
# Example: to_number("443") should give 443, to_number("https") should give None
def to_number(text: str) -> int | None:
    return None


# Step 2: if the pattern (after removing outside spaces) starts with "[" and
# ends with "]", return the text between them. Otherwise:
#     raise PatternError("missing [ ] brackets")
# Example: require_brackets(" [abc] ") should give "abc"
def require_brackets(pattern: str) -> str:
    return ""


# Step 3: parse a STIX pattern into (object_type, prop, value), raising
# PatternError with one of these exact messages when something is wrong:
#     "missing [ ] brackets"            (use require_brackets for this)
#     "value must be in single quotes"  (right of = isn't 'quoted')
#     "expected type:property before =" (no ":" on the left, or either side empty)
#     "value is empty"                  (the quotes are empty: '')
# Example: parse_pattern("[ipv4-addr:value = '198.51.100.7']")
#          should give ("ipv4-addr", "value", "198.51.100.7")
def parse_pattern(pattern: str) -> tuple[str, str, str]:
    return ("", "", "")


# Step 4: return parse_pattern(pattern), or None if it raises PatternError.
def safe_parse(pattern: str) -> tuple[str, str, str] | None:
    return None


# Step 5: return a tuple (indicators, errors).
#   indicators: one to_indicator() dict per good pattern, skipping repeated keys
#               (use a seen set, as in lesson 5)
#   errors:     one text per bad pattern, made with  f"{pattern!r}: {err}"
def ingest(patterns: list[str]) -> tuple[list[dict[str, str]], list[str]]:
    return [], []


# ---------------------------------------------------------------------------
# The checker. You don't need to read or change anything below this line.
# ---------------------------------------------------------------------------
class Raises:
    def __init__(self, message: str) -> None:
        self.message = message

    def __repr__(self) -> str:
        return f"raise PatternError({self.message!r})"


def outcome(func, args):
    try:
        return func(*args)
    except PatternError as err:
        return Raises(str(err))


def same(got, expected) -> bool:
    if isinstance(expected, Raises):
        return isinstance(got, Raises) and got.message == expected.message
    return not isinstance(got, Raises) and got == expected


IP = {"type": "ipv4-addr", "property": "value", "value": "198.51.100.7",
      "key": "ipv4-addr|198.51.100.7"}
DOM = {"type": "domain-name", "property": "value", "value": "evil.example",
       "key": "domain-name|evil.example"}
FEED = [
    "[ipv4-addr:value = '198.51.100.7']",
    "not a pattern",
    "[domain-name:value = 'evil.example']",
    "[ipv4-addr:value = 198.51.100.7]",
    "[ipv4-addr:value = '198.51.100.7']",
]

STEPS = [
    (
        to_number,
        [(("443",), 443), (("https",), None), (("",), None)],
        "try:  return int(text)   then   except ValueError:  return None",
    ),
    (
        require_brackets,
        [((" [abc] ",), "abc"),
         (("abc",), Raises("missing [ ] brackets")),
         (("[abc",), Raises("missing [ ] brackets"))],
        'p = pattern.strip()  then  if not (p.startswith("[") and p.endswith("]")):  '
        'raise PatternError("missing [ ] brackets")   and finally  return p[1:-1]',
    ),
    (
        parse_pattern,
        [(("[ipv4-addr:value = '198.51.100.7']",), ("ipv4-addr", "value", "198.51.100.7")),
         (("  [url:value='http://bad.example/a=b'] ",), ("url", "value", "http://bad.example/a=b")),
         (("ipv4-addr:value = '198.51.100.7'",), Raises("missing [ ] brackets")),
         (("[ipv4-addr:value = 198.51.100.7]",), Raises("value must be in single quotes")),
         (("[ipv4-addr = '198.51.100.7']",), Raises("expected type:property before =")),
         (("[:value = '198.51.100.7']",), Raises("expected type:property before =")),
         (("[ipv4-addr:value = '']",), Raises("value is empty"))],
        "Start with  inner = require_brackets(pattern)  then  left, _, right = inner.partition(\"=\")  "
        "and strip both. Then check each problem in turn and raise the matching PatternError.",
    ),
    (
        safe_parse,
        [(("[ipv4-addr:value = '198.51.100.7']",), ("ipv4-addr", "value", "198.51.100.7")),
         (("broken",), None)],
        "try:  return parse_pattern(pattern)   then   except PatternError:  return None",
    ),
    (
        ingest,
        [((FEED,), ([IP, DOM], ["'not a pattern': missing [ ] brackets",
                                "'[ipv4-addr:value = 198.51.100.7]': value must be in single quotes"])),
         (([],), ([], []))],
        "Like lesson 5's ingest, plus an errors list. Inside the loop:  try:  parsed = parse_pattern(pattern)  "
        'except PatternError as err:  errors.append(f"{pattern!r}: {err}")  then  continue',
    ),
]


def show_call(func, args) -> str:
    text = f"{func.__name__}({', '.join(repr(a) for a in args)})"
    return text if len(text) < 120 else text[:117] + "..."


def main() -> None:
    for number, (func, cases, hint) in enumerate(STEPS, start=1):
        for args, expected in cases:
            got = outcome(func, args)
            if not same(got, expected):
                print(f"Step {number} is next.")
                print(f"  {show_call(func, args)}")
                print(f"  should give {expected!r}")
                print(f"  right now it gives {got!r}")
                print(f"  Hint: {hint}")
                print(f"\n{number - 1} of {len(STEPS)} steps done. Keep going!")
                return
        print(f"Step {number} passed ✓")
    print(f"\nAll {len(STEPS)} steps done. 🎉 ThreatDesk now explains exactly what's wrong with bad patterns!")


if __name__ == "__main__":
    main()
