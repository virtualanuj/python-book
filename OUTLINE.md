# Course outline: building ThreatDesk

ThreatDesk is a threat intelligence service. It pulls indicators of compromise (malicious IPs, domains, URLs, file hashes) from **TAXII 2.1** feeds, normalises the **STIX 2.1** objects, stores and de-duplicates them, enriches them, and shows everything on a dashboard and through an API.

Each line is one micro lesson. **Product step** is what ThreatDesk gains.

## Module 1: Language core (the indicator parser)
1. Strings, functions and f-strings. Product step: `parse_pattern()` turns the STIX pattern `[ipv4-addr:value = '198.51.100.7']` into a dict.
2. Lists, dicts, sets and comprehensions. Product step: de-duplicate indicators, count them by type, apply an allow-list.
3. Control flow and `match` statements. Product step: compound patterns (`AND`/`OR`) and classifying raw IOCs (is this an IP, domain, URL or hash?).
4. Errors and exceptions. Product step: `PatternError` with helpful messages instead of returning `None`.
5. Modules and project layout with uv. Product step: move code into a `threatdesk` package (`src/` layout).

## Module 2: Modelling threat data
6. Dataclasses. Product step: `Indicator`, `Feed` and `Sighting` classes replace dicts.
7. Enums and `datetime`. Product step: TLP markings as an enum, `valid_from`/`valid_until` and indicator expiry.
8. Type hints and mypy/pyright. Product step: fully typed core.
9. Protocols and composition. Product step: a `FeedSource` interface (TAXII, CSV, plain-text blocklists).
10. Iterators and generators. Product step: stream large STIX bundles without loading them into memory.

## Module 3: Testing and quality
11. pytest basics. Product step: tests for the pattern parser.
12. Fixtures and parametrize. Product step: sample STIX bundles and fake TAXII responses as fixtures.
13. Ruff (lint and format) and pre-commit.
14. Property-based testing with Hypothesis. Product step: the parser never crashes on hostile input (threat feeds are untrusted data).

## Module 4: Persistence
15. Files, `pathlib` and JSON. Product step: load and save STIX bundles.
16. SQLite with the standard library. Product step: indicators table with first-seen/last-seen and source tracking.
17. SQLAlchemy 2.0 and Alembic migrations. Product step: schema ready for PostgreSQL.

## Module 5: The CLI
18. `argparse` to Typer. Product step: `threatdesk feeds add/pull`, `threatdesk search 198.51.100.7`.
19. Configuration, environment variables and secrets. Product step: feed credentials kept out of code.
20. Logging. Product step: structured ingest logs (what was pulled, added, expired).
21. Rich output. Product step: coloured tables and progress bars for ingest.

## Module 6: Talking TAXII
22. HTTP with `httpx`. Product step: TAXII 2.1 discovery, API roots and collections.
23. Pagination and incremental pulls. Product step: `added_after` and `next` so each pull only fetches new objects.
24. Auth, retries and timeouts; the `stix2` and `taxii2-client` libraries vs. hand-rolled code.

## Module 7: Concurrency and async
25. Threads, processes and the GIL (plus free-threaded Python).
26. `asyncio` fundamentals. Product step: pull many collections concurrently.
27. Rate limiting and backoff. Product step: enrichment lookups (ASN, geolocation, reputation) without getting blocked.

## Module 8: Packaging and shipping
28. `pyproject.toml` and entry points. Product step: `uv tool install .` gives a real `threatdesk` command.
29. Versioning, wheels, publishing to TestPyPI.
30. GitHub Actions CI. Product step: tests, lint and type checks on every push.

## Module 9: API and dashboard
31. FastAPI basics. Product step: `GET /indicators`, `GET /indicators/lookup?value=...`.
32. Pydantic models and validation.
33. Auth and dependency injection. Product step: API keys with read-only and admin roles.
34. Background jobs and scheduling. Product step: each feed pulled on its own schedule.
35. The dashboard. Product step: server-rendered pages (Jinja2 + HTMX) with search, feed health and recent indicators.
36. Docker and deployment. Product step: ThreatDesk running with PostgreSQL on a cloud host.

## Module 10: Analytics and expert topics
37. Polars and charts. Product step: dashboard charts for indicators per day, by type, feed overlap and ageing.
38. Decorators and context managers. Product step: `@retry`, `@timed` and a DB transaction helper.
39. Profiling and performance. Product step: bulk-ingest a million indicators fast; upgrading to Python 3.15.
40. Capstone: match your own logs against ThreatDesk indicators, or serve ThreatDesk as a TAXII server.
