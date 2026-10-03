"""Lesson 7 checker: tests the threatdesk package you built.

Run from the repo root:
    uv run --project threatdesk lessons/07-modules-and-packages/check.py
"""

import importlib
from pathlib import Path

SAMPLE_FEED = str(Path(__file__).parent / "sample-feed.txt")


def get(module_name, *names):
    """Import threatdesk.<module_name> and return the requested functions."""
    module = importlib.import_module(f"threatdesk.{module_name}")
    return [getattr(module, name) for name in names]


def step_1():
    importlib.import_module("threatdesk")


def step_2():
    clean, make_key, guess_kind = get("normalize", "clean", "make_key", "guess_kind")
    yield "clean('  EVIL.Example ')", clean("  EVIL.Example "), "evil.example"
    yield "make_key('ipv4-addr', '198.51.100.7')", make_key("ipv4-addr", "198.51.100.7"), "ipv4-addr|198.51.100.7"
    yield "guess_kind('198.51.100.7')", guess_kind("198.51.100.7"), "ipv4-addr"
    yield "guess_kind('https://login.bad.example')", guess_kind("https://login.bad.example"), "url"
    yield "guess_kind('payroll@phish.example')", guess_kind("payroll@phish.example"), "email-addr"
    yield "guess_kind('2001:db8::1')", guess_kind("2001:db8::1"), "ipv6-addr"
    yield "guess_kind('999.1.1.1')", guess_kind("999.1.1.1"), "domain-name"


def step_3():
    PatternError, parse_pattern, safe_parse = get("patterns", "PatternError", "parse_pattern", "safe_parse")
    yield "PatternError is a kind of ValueError", issubclass(PatternError, ValueError), True
    yield ("parse_pattern(\"[ipv4-addr:value = '198.51.100.7']\")",
           parse_pattern("[ipv4-addr:value = '198.51.100.7']"), ("ipv4-addr", "value", "198.51.100.7"))
    try:
        parse_pattern("broken")
        raised = "nothing was raised"
    except PatternError as err:
        raised = str(err)
    yield "parse_pattern('broken') raises PatternError", raised, "missing [ ] brackets"
    yield "safe_parse('broken')", safe_parse("broken"), None


def step_4():
    to_indicator, ingest, count_by_type = get("ingest", "to_indicator", "ingest", "count_by_type")
    ip = {"type": "ipv4-addr", "property": "value", "value": "198.51.100.7", "key": "ipv4-addr|198.51.100.7"}
    yield "to_indicator(('ipv4-addr', 'value', '198.51.100.7'))", to_indicator(("ipv4-addr", "value", "198.51.100.7")), ip
    indicators, errors = ingest(["[ipv4-addr:value = '198.51.100.7']", "broken", "[ipv4-addr:value = '198.51.100.7']"])
    yield "ingest([...]) indicators", indicators, [ip]
    yield "ingest([...]) errors", errors, ["'broken': missing [ ] brackets"]
    yield "count_by_type([ip, ip])", dict(count_by_type([ip, ip])), {"ipv4-addr": 2}


def step_5():
    load_patterns, ingest_file = get("ingest", "load_patterns", "ingest_file")
    patterns = load_patterns(SAMPLE_FEED)
    yield "len(load_patterns(sample-feed.txt))", len(patterns), 8
    yield "load_patterns(...)[0]", patterns[0], "[ipv4-addr:value = '198.51.100.7']"
    indicators, errors = ingest_file(SAMPLE_FEED)
    yield "number of indicators from ingest_file(sample-feed.txt)", len(indicators), 5
    yield "number of errors from ingest_file(sample-feed.txt)", len(errors), 2


STEPS = [
    (step_1, "Create the project",
     "From the repo root run:  uv init --lib --vcs none --python 3.14 threatdesk   "
     "then run this checker again with  --project threatdesk"),
    (step_2, "threatdesk/src/threatdesk/normalize.py",
     "Create normalize.py next to __init__.py with clean, make_key and guess_kind. "
     "For IPs, use  import ipaddress  and  ipaddress.ip_address(value).version  inside try/except ValueError."),
    (step_3, "threatdesk/src/threatdesk/patterns.py",
     "Create patterns.py and copy PatternError, require_brackets, parse_pattern and safe_parse "
     "from your lesson 6 exercise."),
    (step_4, "threatdesk/src/threatdesk/ingest.py",
     "Create ingest.py with to_indicator, ingest and count_by_type. At the top:  "
     "from threatdesk.patterns import PatternError, parse_pattern"),
    (step_5, "Reading a feed file",
     "Add load_patterns(path) to ingest.py: Path(path).read_text().splitlines(), strip each line, "
     "skip blank lines and lines starting with #. Then ingest_file(path) returns ingest(load_patterns(path))."),
]


def main():
    for number, (step, title, hint) in enumerate(STEPS, start=1):
        try:
            results = step()
            for description, got, expected in results or []:
                if got != expected:
                    print(f"Step {number} ({title}) is next.")
                    print(f"  {description}")
                    print(f"  should give {expected!r}")
                    print(f"  right now it gives {got!r}")
                    print(f"  Hint: {hint}")
                    print(f"\n{number - 1} of {len(STEPS)} steps done. Keep going!")
                    return
        except (ImportError, AttributeError) as err:
            print(f"Step {number} ({title}) is next.")
            print(f"  Python says: {type(err).__name__}: {err}")
            print(f"  Hint: {hint}")
            print(f"\n{number - 1} of {len(STEPS)} steps done. Keep going!")
            return
        print(f"Step {number} passed ✓  {title}")
    print(f"\nAll {len(STEPS)} steps done. 🎉 ThreatDesk is a real Python package now!")


if __name__ == "__main__":
    main()
