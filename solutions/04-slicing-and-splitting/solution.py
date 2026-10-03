"""Lesson 4 solution. Have a go at the exercise first!"""


def has_brackets(pattern: str) -> bool:
    p = pattern.strip()
    return p.startswith("[") and p.endswith("]")


def strip_brackets(pattern: str) -> str:
    return pattern.strip()[1:-1]


def split_once(text: str, sep: str) -> tuple[str, str]:
    before, found, after = text.partition(sep)
    return before.strip(), after.strip()


def is_quoted(text: str) -> bool:
    return len(text) >= 2 and text.startswith("'") and text.endswith("'")


def parse_pattern(pattern: str) -> tuple[str, str, str] | None:
    if not has_brackets(pattern):
        return None

    left, right = split_once(strip_brackets(pattern), "=")
    if not is_quoted(right):
        return None

    object_type, prop = split_once(left, ":")
    value = right[1:-1]
    if object_type == "" or prop == "" or value == "":
        return None

    return object_type, prop, value


if __name__ == "__main__":
    for p in ["[ipv4-addr:value = '198.51.100.7']", "[ipv4-addr = '198.51.100.7']"]:
        print(f"{p!r} -> {parse_pattern(p)!r}")
