"""Lesson 1 solution. Have a go at the exercise first!"""


def welcome() -> str:
    return "Welcome to ThreatDesk"


def label(value: str) -> str:
    return f"Indicator: {value}"


def make_key(kind: str, value: str) -> str:
    return f"{kind}|{value}"


def clean(value: str) -> str:
    return value.strip().lower()


if __name__ == "__main__":
    print(welcome())
    print(label("198.51.100.7"))
    print(make_key("ipv4-addr", "198.51.100.7"))
    print(clean("  EVIL.Example "))
