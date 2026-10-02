"""Lesson 3 solution. Have a go at the exercise first!"""


def clean(value):
    return value.strip().lower()


def guess_kind(value):
    if value.startswith("http://") or value.startswith("https://"):
        return "url"
    elif "@" in value:
        return "email-addr"
    elif value.count(".") == 3 and value.replace(".", "").isdigit():
        return "ipv4-addr"
    else:
        return "domain-name"


def first_item(values):
    return values[0]


def how_many(values):
    return len(values)


def clean_all(values):
    result = []
    for value in values:
        result.append(clean(value))
    return result


def only_kind(values, kind):
    result = []
    for value in values:
        if guess_kind(value) == kind:
            result.append(value)
    return result


def without_duplicates(values):
    result = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


if __name__ == "__main__":
    raw = ["  198.51.100.7", "Evil.Example", "evil.example ", "https://login.bad.example"]
    values = without_duplicates(clean_all(raw))
    print(values)
    print(only_kind(values, "domain-name"))
