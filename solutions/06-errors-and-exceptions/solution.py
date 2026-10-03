"""Lesson 6 solution. Have a go at the exercise first!"""


class PatternError(ValueError):
    """A STIX pattern could not be parsed."""


def to_number(text: str) -> int | None:
    try:
        return int(text)
    except ValueError:
        return None


def require_brackets(pattern: str) -> str:
    p = pattern.strip()
    if not (p.startswith("[") and p.endswith("]")):
        raise PatternError("missing [ ] brackets")
    return p[1:-1]


def is_quoted(text: str) -> bool:
    return len(text) >= 2 and text.startswith("'") and text.endswith("'")


def parse_pattern(pattern: str) -> tuple[str, str, str]:
    inner = require_brackets(pattern)

    left, _, right = inner.partition("=")
    left, right = left.strip(), right.strip()
    if not is_quoted(right):
        raise PatternError("value must be in single quotes")

    object_type, colon, prop = left.partition(":")
    object_type, prop = object_type.strip(), prop.strip()
    if not colon or object_type == "" or prop == "":
        raise PatternError("expected type:property before =")

    value = right[1:-1]
    if value == "":
        raise PatternError("value is empty")

    return object_type, prop, value


def safe_parse(pattern: str) -> tuple[str, str, str] | None:
    try:
        return parse_pattern(pattern)
    except PatternError:
        return None


def to_indicator(parsed: tuple[str, str, str]) -> dict[str, str]:
    object_type, prop, value = parsed
    return {
        "type": object_type,
        "property": prop,
        "value": value,
        "key": f"{object_type}|{value}",
    }


def ingest(patterns: list[str]) -> tuple[list[dict[str, str]], list[str]]:
    seen = set()
    indicators = []
    errors = []
    for pattern in patterns:
        try:
            parsed = parse_pattern(pattern)
        except PatternError as err:
            errors.append(f"{pattern!r}: {err}")
            continue
        indicator = to_indicator(parsed)
        if indicator["key"] in seen:
            continue
        seen.add(indicator["key"])
        indicators.append(indicator)
    return indicators, errors


if __name__ == "__main__":
    feed = [
        "[ipv4-addr:value = '198.51.100.7']",
        "not a pattern",
        "[ipv4-addr:value = 198.51.100.7]",
        "[domain-name = 'evil.example']",
    ]
    indicators, errors = ingest(feed)
    print(f"{len(indicators)} indicator(s) ingested")
    for error in errors:
        print(f"skipped {error}")
