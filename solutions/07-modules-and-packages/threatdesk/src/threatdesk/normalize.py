"""Cleaning raw indicator values and working out what kind they are."""

import ipaddress


def clean(value: str) -> str:
    return value.strip().lower()


def make_key(kind: str, value: str) -> str:
    return f"{kind}|{value}"


def is_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def is_email(value: str) -> bool:
    return "@" in value


def ip_version(value: str) -> int | None:
    """Return 4 or 6 if value is a valid IP address, otherwise None."""
    try:
        return ipaddress.ip_address(value).version
    except ValueError:
        return None


def guess_kind(value: str) -> str:
    if is_url(value):
        return "url"
    elif is_email(value):
        return "email-addr"
    elif ip_version(value) == 4:
        return "ipv4-addr"
    elif ip_version(value) == 6:
        return "ipv6-addr"
    else:
        return "domain-name"
