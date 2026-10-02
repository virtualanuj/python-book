"""Lesson 1 exercise: turn a STIX indicator pattern into structured data.

Run from the repo root:  uv run --python 3.14 lessons/01-parse-pattern/exercise.py
"""


def parse_pattern(pattern: str) -> dict | None:
    """Parse a simple STIX pattern like "[ipv4-addr:value = '198.51.100.7']".

    Returns {"type": str, "property": str, "value": str, "key": str},
    or None if the pattern is not a single, well-formed comparison.
    """
    # TODO: replace this with your implementation.
    return None


# ---------------------------------------------------------------------------
# Checks: do not edit below. Each case is (input, expected output).
# ---------------------------------------------------------------------------
SHA256 = "2CF24DBA5FB0A30E26E83B2AC5B9E29E1B161E5C1FA7425E73043362938B9824"

CASES = [
    (
        "[ipv4-addr:value = '198.51.100.7']",
        {"type": "ipv4-addr", "property": "value", "value": "198.51.100.7",
         "key": "ipv4-addr|198.51.100.7"},
    ),
    (
        "  [url:value='http://login.bad.example/verify']  ",
        {"type": "url", "property": "value", "value": "http://login.bad.example/verify",
         "key": "url|http://login.bad.example/verify"},
    ),
    (
        "[domain-name:value = 'Update.Malware.EXAMPLE']",
        {"type": "domain-name", "property": "value", "value": "update.malware.example",
         "key": "domain-name|update.malware.example"},
    ),
    (
        "[email-addr:value = 'Payroll@Phish.Example']",
        {"type": "email-addr", "property": "value", "value": "payroll@phish.example",
         "key": "email-addr|payroll@phish.example"},
    ),
    (
        f"[file:hashes.'SHA-256' = '{SHA256}']",
        {"type": "file", "property": "hashes.'SHA-256'", "value": SHA256.lower(),
         "key": f"file|{SHA256.lower()}"},
    ),
    ("ipv4-addr:value = '198.51.100.7'", None),           # missing [ ]
    ("[ipv4-addr:value = 198.51.100.7]", None),           # value not quoted
    ("[ipv4-addr = '198.51.100.7']", None),               # no property
    ("[ipv4-addr:value = '']", None),                     # empty value
    ("[ipv4-addr:value = '203.0.113.1' OR ipv4-addr:value = '203.0.113.2']", None),  # compound: lesson 3
]


def main() -> None:
    passed = 0
    for text, expected in CASES:
        got = parse_pattern(text)
        if got == expected:
            passed += 1
            print(f"PASS  {text!r}")
        else:
            print(f"FAIL  {text!r}\n      expected {expected}\n      got      {got}")
    print(f"\n{passed}/{len(CASES)} checks passed")


if __name__ == "__main__":
    main()
