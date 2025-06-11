# HUMAN Instructions

This repository contains automated agents that assist with code updates and documentation.
Follow these steps on the human side so the agents can run tests and CI jobs correctly.

## Local environment setup

1. Use **Python 3.11 or newer**. Create a virtualenv and install backend dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt
   ```

2. Install **Playwright** for end‑to‑end tests:
   ```bash
   npm install
   npx playwright install --with-deps
   ```
   The agents cannot run `playwright install` themselves, so ensure it is executed once before running tests.

3. If using PostgreSQL/Redis locally, copy `.env.example` to `.env` and adjust values. See `codex_env_setup.md` for optional service configuration.

## Running tests

Run the Python unit tests from the project root:

```bash
pytest
```

Run the frontend unit and Playwright tests:

```bash
npm test
npm run test:e2e
```

The CI expects all tests to pass before merging.
