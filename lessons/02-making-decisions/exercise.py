"""Lesson 2 exercise: making decisions.

Run from the repo root:
    uv run --python 3.14 lessons/02-making-decisions/exercise.py

Fill in each function. Replace the line   return False   (or   return ""  ).
"""


# Step 1: return True if value starts with "http://" or "https://", otherwise False.
# Example: is_url("https://login.bad.example") should give True
def is_url(value):
    return value.startswith("http://") or value.startswith("https://")


# Step 2: return True if value contains an "@" character.
# Example: is_email("payroll@phish.example") should give True
def is_email(value):
    return "@" in value


# Step 3: return True if value has exactly 3 dots AND is only digits once
# the dots are removed.
# Example: is_ipv4("198.51.100.7") should give True, is_ipv4("evil.example") False
def is_ipv4(value):
    return value.count(".") == 3 and value.replace(".", "").isdigit()


# Step 4: return the kind of indicator as text, using if / elif / else:
#   a URL               -> "url"
#   an email address    -> "email-addr"
#   an IPv4 address     -> "ipv4-addr"
#   anything else       -> "domain-name"
# Use your functions from steps 1 to 3. Check for a URL first!
def guess_kind(value):
    if value is None or not isinstance(value, str):
        raise ValueError("value must be a non-empty string")
    if is_url(value):
        return "url"
    elif is_email(value):
        return "email-addr"
    elif is_ipv4(value):
        return "ipv4-addr"
    else:
        return "domain-name"    


# ---------------------------------------------------------------------------
# The checker. You don't need to read or change anything below this line.
# ---------------------------------------------------------------------------
STEPS = [
    (
        is_url,
        [("https://login.bad.example", True), ("http://old.bad.example/x", True),
         ("bad.example", False), ("ftp://files.example", False)],
        'Use "or" to combine two startswith checks:  '
        'return value.startswith("http://") or value.startswith("https://")',
    ),
    (
        is_email,
        [("payroll@phish.example", True), ("bad.example", False)],
        'The "in" operator checks if text is inside other text:  return "@" in value',
    ),
    (
        is_ipv4,
        [("198.51.100.7", True), ("203.0.113.250", True), ("evil.example", False),
         ("1.2.3", False), ("1.2.3.x", False), ("a.b.c.d", False)],
        'Combine two checks with "and":  '
        'return value.count(".") == 3 and value.replace(".", "").isdigit()',
    ),
    (
        guess_kind,
        [("https://login.bad.example", "url"), ("payroll@phish.example", "email-addr"),
         ("198.51.100.7", "ipv4-addr"), ("update.malware.example", "domain-name"),
         ("https://user@bad.example/login", "url")],
        "Start with:  if is_url(value):  then on the next line (indented)  return \"url\"  "
        "then add  elif is_email(value):  and so on, ending with  else:",
    ),
]


def main():
    for number, (func, cases, hint) in enumerate(STEPS, start=1):
        for value, expected in cases:
            got = func(value)
            if got != expected:
                print(f"Step {number} is next.")
                print(f"  {func.__name__}({value!r}) should give {expected!r}")
                print(f"  right now it gives {got!r}")
                print(f"  Hint: {hint}")
                print(f"\n{number - 1} of {len(STEPS)} steps done. Keep going!")
                return
        print(f"Step {number} passed ✓")
    print(f"\nAll {len(STEPS)} steps done. 🎉 ThreatDesk can now recognise four kinds of indicator!")


if __name__ == "__main__":
    main()
