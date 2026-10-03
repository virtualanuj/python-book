"""Parsing STIX 2.1 patterns such as [ipv4-addr:value = '198.51.100.7']."""


class PatternError(ValueError):
    """A STIX pattern could not be parsed."""


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
