"""Lesson 1 solution. Try the exercise first!"""

# Values of these types are case-insensitive, so we store them lowercased.
CASE_INSENSITIVE_TYPES = ("domain-name", "email-addr")


def is_quoted(text: str) -> bool:
    """True for "'abc'": at least two characters, wrapped in single quotes."""
    return len(text) >= 2 and text.startswith("'") and text.endswith("'")


def parse_pattern(pattern: str) -> dict | None:
    """Parse a simple STIX pattern like "[ipv4-addr:value = '198.51.100.7']".

    Returns {"type": str, "property": str, "value": str, "key": str},
    or None if the pattern is not a single, well-formed comparison.
    """
    pattern = pattern.strip()
    if not (pattern.startswith("[") and pattern.endswith("]")):
        return None

    inner = pattern[1:-1]
    if " AND " in inner or " OR " in inner:
        return None  # compound patterns arrive in lesson 3

    left, sep, right = inner.partition("=")
    left, right = left.strip(), right.strip()
    if not sep or ":" not in left or not is_quoted(right):
        return None

    object_type, _, prop = left.partition(":")
    value = right[1:-1]
    if not object_type or not prop or not value:
        return None

    if object_type in CASE_INSENSITIVE_TYPES or prop.startswith("hashes."):
        value = value.lower()

    return {
        "type": object_type,
        "property": prop,
        "value": value,
        "key": f"{object_type}|{value}",
    }


if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Reuse the checks from the matching lesson folder.
    lesson_dir = Path(__file__).resolve().parents[2] / "lessons" / "01-parse-pattern"
    sys.path.insert(0, str(lesson_dir))
    from exercise import CASES

    for text, expected in CASES:
        assert parse_pattern(text) == expected, (text, parse_pattern(text))
    print(f"All {len(CASES)} checks passed")
