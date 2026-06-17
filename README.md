# -my-api-automation
Full-stack test automation framework | Python · Pytest · Playwright · Requests · API &amp; UI testing | Learning project
# my-api-automation

Full-stack test automation framework built with Python, Pytest, Playwright, and Requests — covering both REST API testing and UI end-to-end testing.

## What this project tests

**API testing** (JSONPlaceholder + ReqRes)
- CRUD operations on posts, users, albums, comments, todos
- Authentication flows: login, register, token handling
- Schema validation with jsonschema
- Negative cases: 404s, invalid payloads, edge cases
- Response time assertions

**UI testing** (SauceDemo, via Playwright)
- Login flow — valid and invalid credentials
- Shopping flow — browse, add to cart, checkout
- Full end-to-end order completion

## Tech stack

- Python 3.14
- Pytest
- Playwright
- Requests
- Faker (dynamic test data)
- jsonschema (response validation)
- GitHub Actions (CI/CD)

## Project structure

api/        — API client classes (one per resource)
config/     — environment and settings configuration
pages/      — Page Object Model classes for UI tests
tests/      — all test files (API + UI)
utils/      — shared assertions, schemas, data factories

## Running the tests

Install dependencies:

    pip install -r requirements.txt
    playwright install chromium

Run everything:

    pytest -v

Run only API tests:

    pytest -m api -v

Run only UI tests:

    pytest -m ui -v

Run only smoke tests:

    pytest -m smoke -v

Generate an HTML report:

    pytest --html=reports/report.html

## CI/CD

Every push and pull request automatically triggers the test suite on GitHub Actions — see `.github/workflows/ci.yml`. Both API and UI test reports are uploaded as downloadable artifacts.

## Author

Roxana Ojog — QA Engineer transitioning into test automation and AI quality engineering.
