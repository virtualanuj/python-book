"""Lesson 1 solution. Have a go at the exercise first!"""


def welcome():
    return "Welcome to ThreatDesk"


def label(value):
    return f"Indicator: {value}"


def make_key(kind, value):
    return f"{kind}|{value}"


def clean(value):
    return value.strip().lower()


if __name__ == "__main__":
    print(welcome())
    print(label("198.51.100.7"))
    print(make_key("ipv4-addr", "198.51.100.7"))
    print(clean("  EVIL.Example "))
