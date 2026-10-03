# Lessons

Every lesson in the course, with one line on what it covers. ✅ = you've completed it, 👉 = up next, and the rest are still to come. The full plan, with what ThreatDesk gains in each lesson, is in [OUTLINE.md](OUTLINE.md).

## Module 1: Python from zero

| # | Lesson | What it covers |
|---|---|---|
| 1 ✅ | [First steps](lessons/01-first-steps/README.md) | Running Python, values, variables, f-strings and writing your first functions. |
| 2 ✅ | [Making decisions](lessons/02-making-decisions/README.md) | `True`/`False`, comparisons, `and`/`or`/`not`, and `if`/`elif`/`else` to tell IPs, URLs, emails and domains apart. |
| 3 ✅ | [Lists and loops](lessons/03-lists-and-loops/README.md) | Lists, indexes, `for` loops and building new lists to clean and filter a whole feed. |
| 4 ✅ | [Slicing and splitting](lessons/04-slicing-and-splitting/README.md) | Slicing, `split()`/`partition()`, tuples and `None` to read a STIX pattern. |
| 5 ✅ | [Dictionaries and sets](lessons/05-dicts-and-sets/README.md) | Dicts for named records, counting, and sets for fast de-duplication in a mini ingest pipeline. |
| 6 ✅ | [Errors and exceptions](lessons/06-errors-and-exceptions/README.md) | Reading type hints, `try`/`except`, `raise`, and a custom `PatternError` that explains what went wrong. |
| 7 👉 | [Modules, packages and files](lessons/07-modules-and-packages/README.md) | Imports and the standard library, turning ThreatDesk into a real `threatdesk` package with uv, and reading a feed file. |

## Module 2: Modelling threat data

| # | Lesson | What it covers |
|---|---|---|
| 8 | Dataclasses | Defining your own types (`Indicator`, `Feed`, `Sighting`) instead of passing dicts around. |
| 9 | Enums and dates | Fixed choices like TLP markings with `Enum`, and timestamps and expiry with `datetime`. |
| 10 | Checking type hints | Running mypy or pyright so mistakes are caught before the code runs. |
| 11 | Protocols and composition | Describing what a feed source must do, so TAXII, CSV and blocklist feeds plug in the same way. |
| 12 | Iterators and generators | Processing huge STIX bundles one item at a time without filling memory. |

## Module 3: Testing and quality

| # | Lesson | What it covers |
|---|---|---|
| 13 | pytest basics | Writing real automated tests for the pattern parser. |
| 14 | Fixtures and parametrize | Reusable test data (sample bundles, fake TAXII replies) and table-driven tests. |
| 15 | Ruff and pre-commit | Automatic linting and formatting on every commit. |
| 16 | Property-based testing | Hypothesis throws thousands of odd inputs at the parser to prove it never crashes. |

## Module 4: Persistence

| # | Lesson | What it covers |
|---|---|---|
| 17 | Files, pathlib and JSON | Reading and writing STIX bundles on disk. |
| 18 | SQLite | Storing indicators with first-seen/last-seen dates and their sources in a database. |
| 19 | SQLAlchemy and Alembic | A proper data layer and schema migrations, ready for PostgreSQL. |

## Module 5: The CLI

| # | Lesson | What it covers |
|---|---|---|
| 20 | argparse to Typer | A real command-line tool: `threatdesk feeds pull`, `threatdesk search`. |
| 21 | Configuration and secrets | Settings files and environment variables, keeping feed credentials out of code. |
| 22 | Logging | Structured logs that record what each ingest pulled, added and expired. |
| 23 | Rich output | Coloured tables and progress bars in the terminal. |

## Module 6: Talking TAXII

| # | Lesson | What it covers |
|---|---|---|
| 24 | HTTP with httpx | Calling the TAXII 2.1 API: discovery, API roots and collections. |
| 25 | Pagination and incremental pulls | Fetching only new objects each time with `added_after` and paging. |
| 26 | Auth, retries and libraries | Authentication, timeouts and retries, and when to use `stix2`/`taxii2-client`. |

## Module 7: Concurrency and async

| # | Lesson | What it covers |
|---|---|---|
| 27 | Threads, processes and the GIL | How Python runs things in parallel, including free-threaded Python. |
| 28 | asyncio | Pulling many feeds at the same time with `async`/`await`. |
| 29 | Rate limiting and backoff | Enrichment lookups that stay fast without getting blocked. |

## Module 8: Packaging and shipping

| # | Lesson | What it covers |
|---|---|---|
| 30 | pyproject.toml and entry points | Installing ThreatDesk as a proper `threatdesk` command. |
| 31 | Versioning and publishing | Building wheels and publishing to TestPyPI. |
| 32 | GitHub Actions CI | Tests, linting and type checks running on every push. |

## Module 9: API and dashboard

| # | Lesson | What it covers |
|---|---|---|
| 33 | FastAPI basics | A web API to list and look up indicators. |
| 34 | Pydantic | Validating API input and output with models. |
| 35 | Auth and dependency injection | API keys with read-only and admin roles. |
| 36 | Background jobs | Pulling each feed automatically on its own schedule. |
| 37 | The dashboard | Web pages with search, feed health and recent indicators (Jinja2 + HTMX). |
| 38 | Docker and deployment | Running ThreatDesk and PostgreSQL in containers on a cloud host. |

## Module 10: Analytics and expert topics

| # | Lesson | What it covers |
|---|---|---|
| 39 | Polars and charts | Dashboard charts: indicators per day, by type, feed overlap and ageing. |
| 40 | Decorators and context managers | Reusable `@retry` and `@timed` helpers and safe database transactions. |
| 41 | Profiling and performance | Making a million-indicator ingest fast, and upgrading to Python 3.15. |
| 42 | Capstone | Match your own logs against ThreatDesk, or serve ThreatDesk as a TAXII server. |
