# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack test automation framework targeting [JSONPlaceholder](https://jsonplaceholder.typicode.com) — a fake REST API. Tests are written with `pytest` and cover API endpoints via `requests`. Playwright is available for future UI tests.

## Commands

### Setup
```bash
pip install -r requirements.txt
playwright install --with-deps chromium
```

### Run all tests
```bash
pytest
```

### Run by marker
```bash
pytest -m api       # all API tests
pytest -m smoke     # quick sanity checks only
pytest -m ui        # UI/Playwright tests
```

### Run a single test file
```bash
pytest tests/test_posts.py
```

### Run a single test by name
```bash
pytest tests/test_posts.py::test_get_post_returns_200
```

HTML reports are always written to `reports/report.html` (configured in `pytest.ini`).

## Architecture

```
config/settings.py          # BASE_URL (from .env or default) and TIMEOUT
api/base_client.py          # BaseClient: shared requests.Session with headers/timeout
api/<resource>_api.py       # Resource-specific clients that extend BaseClient
tests/conftest.py           # pytest fixtures — one per API client (posts_api, users_api, …)
tests/test_<resource>.py    # Test modules grouped by resource
```

### Key design decisions

- **`BaseClient`** owns the `requests.Session` and base URL; all HTTP verbs delegate here. Resource clients inherit from it and add endpoint-specific methods.
- **`BASE_URL`** can be overridden via a `.env` file (`python-dotenv`) — useful for pointing at different environments without changing code.
- **Fixtures** in `conftest.py` instantiate API clients; tests receive them as arguments. There is no shared mutable state across tests.
- **Markers** (`@pytest.mark.api`, `@pytest.mark.smoke`) let CI run subsets of the suite efficiently.
- **Schema validation** uses `jsonschema.validate` against inline dict schemas defined at the top of test files.
- **`faker`** is used to generate random payloads in write-operation tests.

### Adding a new resource

1. Create `api/<resource>_api.py` extending `BaseClient`.
2. Add a fixture in `tests/conftest.py`.
3. Create `tests/test_<resource>.py` — follow the existing section structure: smoke → happy path → filtering → CRUD → negative → performance.
