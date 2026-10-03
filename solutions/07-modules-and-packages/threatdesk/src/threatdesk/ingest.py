"""Turning raw STIX patterns into clean, unique indicator records."""

from collections import Counter
from pathlib import Path

from threatdesk.normalize import make_key
from threatdesk.patterns import PatternError, parse_pattern


def to_indicator(parsed: tuple[str, str, str]) -> dict[str, str]:
    object_type, prop, value = parsed
    return {
        "type": object_type,
        "property": prop,
        "value": value,
        "key": make_key(object_type, value),
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


def count_by_type(indicators: list[dict[str, str]]) -> dict[str, int]:
    return dict(Counter(ind["type"] for ind in indicators))


def load_patterns(path: str) -> list[str]:
    """Read one pattern per line, skipping blank lines and # comments."""
    patterns = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue
        patterns.append(line)
    return patterns


def ingest_file(path: str) -> tuple[list[dict[str, str]], list[str]]:
    return ingest(load_patterns(path))
