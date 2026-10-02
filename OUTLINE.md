# Course outline: building ThreatDesk

ThreatDesk is a threat intelligence service. It pulls indicators of compromise (malicious IPs, domains, URLs, file hashes) from **TAXII 2.1** feeds, normalises the **STIX 2.1** objects, stores and de-duplicates them, enriches them, and shows everything on a dashboard and through an API.

Each line is one micro lesson. Module 1 assumes no Python experience at all; later modules build on it step by step. **Product step** is what ThreatDesk gains.

## Module 1: Python from zero (no experience needed)
1. First steps. Running Python, values, variables, f-strings and your first functions. Product step: `clean()` and `make_key()` for indicator values.
2. Making decisions. `if`/`else`, `True`/`False`, comparisons. Product step: tell an IP address from a domain or a URL.
3. Lists and loops. Product step: clean a whole list of indicators at once.
4. Slicing and splitting text. Product step: `parse_pattern()` reads a STIX pattern like `[ipv4-addr:value = '198.51.100.7']`.
5. Dictionaries and sets. Product step: de-duplicate indicators, count them by type, apply an allow-list.
6. Errors and exceptions. Product step: `PatternError` with a helpful message instead of a silent failure.
7. Files, modules and project layout with uv. Product step: a real `threatdesk` package (`src/` layout) and type hints from here on.

## Module 2: Modelling threat data
8. Dataclasses. Product step: `Indicator`, `Feed` and `Sighting` classes replace dicts.
9. Enums and `datetime`. Product step: TLP markings as an enum, `valid_from`/`valid_until` and indicator expiry.
10. Type hints and mypy/pyright. Product step: fully typed core.
11. Protocols and composition. Product step: a `FeedSource` interface (TAXII, CSV, plain-text blocklists).
12. Iterators and generators. Product step: stream large STIX bundles without loading them into memory.

## Module 3: Testing and quality
13. pytest basics. Product step: tests for the pattern parser.
14. Fixtures and parametrize. Product step: sample STIX bundles and fake TAXII responses as fixtures.
15. Ruff (lint and format) and pre-commit.
16. Property-based testing with Hypothesis. Product step: the parser never crashes on hostile input (threat feeds are untrusted data).

## Module 4: Persistence
17. Files, `pathlib` and JSON. Product step: load and save STIX bundles.
18. SQLite with the standard library. Product step: indicators table with first-seen/last-seen and source tracking.
19. SQLAlchemy 2.0 and Alembic migrations. Product step: schema ready for PostgreSQL.

## Module 5: The CLI
20. `argparse` to Typer. Product step: `threatdesk feeds add/pull`, `threatdesk search 198.51.100.7`.
21. Configuration, environment variables and secrets. Product step: feed credentials kept out of code.
22. Logging. Product step: structured ingest logs (what was pulled, added, expired).
23. Rich output. Product step: coloured tables and progress bars for ingest.

## Module 6: Talking TAXII
24. HTTP with `httpx`. Product step: TAXII 2.1 discovery, API roots and collections.
25. Pagination and incremental pulls. Product step: `added_after` and `next` so each pull only fetches new objects.
26. Auth, retries and timeouts; the `stix2` and `taxii2-client` libraries vs. hand-rolled code.

## Module 7: Concurrency and async
27. Threads, processes and the GIL (plus free-threaded Python).
28. `asyncio` fundamentals. Product step: pull many collections concurrently.
29. Rate limiting and backoff. Product step: enrichment lookups (ASN, geolocation, reputation) without getting blocked.

## Module 8: Packaging and shipping
30. `pyproject.toml` and entry points. Product step: `uv tool install .` gives a real `threatdesk` command.
31. Versioning, wheels, publishing to TestPyPI.
32. GitHub Actions CI. Product step: tests, lint and type checks on every push.

## Module 9: API and dashboard
33. FastAPI basics. Product step: `GET /indicators`, `GET /indicators/lookup?value=...`.
34. Pydantic models and validation.
35. Auth and dependency injection. Product step: API keys with read-only and admin roles.
36. Background jobs and scheduling. Product step: each feed pulled on its own schedule.
37. The dashboard. Product step: server-rendered pages (Jinja2 + HTMX) with search, feed health and recent indicators.
38. Docker and deployment. Product step: ThreatDesk running with PostgreSQL on a cloud host.

## Module 10: Analytics and expert topics
39. Polars and charts. Product step: dashboard charts for indicators per day, by type, feed overlap and ageing.
40. Decorators and context managers. Product step: `@retry`, `@timed` and a DB transaction helper.
41. Profiling and performance. Product step: bulk-ingest a million indicators fast; upgrading to Python 3.15.
42. Capstone: match your own logs against ThreatDesk indicators, or serve ThreatDesk as a TAXII server.
