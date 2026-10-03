"""Lesson 5 solution. Have a go at the exercise first!"""


def parse_pattern(pattern: str) -> tuple[str, str, str] | None:
    """Return (object_type, prop, value) for a simple STIX pattern, or None."""
    p = pattern.strip()
    if not (p.startswith("[") and p.endswith("]")):
        return None
    left, _, right = p[1:-1].partition("=")
    left, right = left.strip(), right.strip()
    if not (len(right) >= 2 and right.startswith("'") and right.endswith("'")):
        return None
    object_type, _, prop = left.partition(":")
    object_type, prop, value = object_type.strip(), prop.strip(), right[1:-1]
    if object_type == "" or prop == "" or value == "":
        return None
    return object_type, prop, value


def to_indicator(parsed: tuple[str, str, str]) -> dict[str, str]:
    object_type, prop, value = parsed
    return {
        "type": object_type,
        "property": prop,
        "value": value,
        "key": f"{object_type}|{value}",
    }


def describe(indicator: dict[str, str]) -> str:
    return f"{indicator['type']} {indicator['value']}"


def unique_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def count_by_type(indicators: list[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for ind in indicators:
        counts[ind["type"]] = counts.get(ind["type"], 0) + 1
    return counts


def ingest(patterns: list[str]) -> list[dict[str, str]]:
    seen: set[str] = set()
    result = []
    for pattern in patterns:
        parsed = parse_pattern(pattern)
        if parsed is None:
            continue
        indicator = to_indicator(parsed)
        if indicator["key"] in seen:
            continue
        seen.add(indicator["key"])
        result.append(indicator)
    return result


def remove_allowed(
    indicators: list[dict[str, str]], allow_list: list[str]
) -> list[dict[str, str]]:
    """Stretch goal: drop indicators whose value is on the allow-list."""
    allowed = set(allow_list)
    return [ind for ind in indicators if ind["value"] not in allowed]


if __name__ == "__main__":
    feed = [
        "[ipv4-addr:value = '198.51.100.7']",
        "[domain-name:value = 'evil.example']",
        "[domain-name:value = 'mycompany.example']",
        "[ipv4-addr:value = '198.51.100.7']",
        "broken",
    ]
    indicators = remove_allowed(ingest(feed), ["mycompany.example"])
    for ind in indicators:
        print(describe(ind))
    print(count_by_type(indicators))
