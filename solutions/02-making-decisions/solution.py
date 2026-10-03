"""Lesson 2 solution. Have a go at the exercise first!"""


def is_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def is_email(value: str) -> bool:
    return "@" in value


def is_ipv4(value: str) -> bool:
    return value.count(".") == 3 and value.replace(".", "").isdigit()


def guess_kind(value: str) -> str:
    if is_url(value):
        return "url"
    elif is_email(value):
        return "email-addr"
    elif is_ipv4(value):
        return "ipv4-addr"
    else:
        return "domain-name"


if __name__ == "__main__":
    for value in ["https://login.bad.example", "payroll@phish.example",
                  "198.51.100.7", "update.malware.example"]:
        print(f"{value} -> {guess_kind(value)}")
