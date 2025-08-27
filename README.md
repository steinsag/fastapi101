
## Initial setup

This project uses package manager [uv](https://github.com/astral-sh/uv) to manage dependencies.
Run the following to install all dependencies:

    uv sync

## Running the service locally

Start MongoDB via Docker Compose (one-time seed included):

    docker compose -f scripts/docker/docker-compose.yml up -d

This starts MongoDB on localhost:27017 and creates an application user on DB "test":
- username: test
- password: test
- database: test

On first startup, it also seeds the "items" collection with a sample document:

    { "id": 1, "name": "Sample Item", "price": 107.99 }

Set environment variable for the app to connect to MongoDB (note the database name is part of the URL path):

    export MONGODB_URL="mongodb://test:test@localhost:27017/test?authSource=test"

Install dependencies and run the API locally (use FastAPI CLI for better dev experience: auto-reload, live reload for static files, improved error pages):

    uv sync
    uv run fastapi dev app/main.py

The app listens on http://localhost:8000. Try fetching the seeded item:

    curl http://localhost:8000/items/1

Expected response:

    {"id": 1, "name": "Sample Item", "price": 107.99}

To stop MongoDB when finished:

    docker compose -f scripts/docker/docker-compose.yml down

## Creating and running a Docker container

Build the container:

    docker build -t fastapi101 .

Run the container (provide MongoDB connection via env var):

    docker run -p 8000:8000 \
      -e MONGODB_URL="mongodb://test:test@host.docker.internal:27017/test?authSource=test" \
      fastapi101

The app is listening on port 8000 locally. Try: http://localhost:8000/items/1

## Verify (format, lint, type-check, tests)

One command to auto-fix formatting/lints, run type checks, and tests:

      uv run scripts/verify.py

This runs, in order: `black .`, `ruff check --fix .`, `ty check`, `pytest`.

## Code formatting (Black)

[Black](https://black.readthedocs.io/) is used for code formatting.

Check formatting:

      uv run black --check .

Auto-format the code locally:

      uv run black .

## Linting (Ruff)

[Ruff](https://docs.astral.sh/ruff/) enforces common Python lint rules and import sorting.

Run Ruff for the whole project:

    uv run ruff check .

Optionally, to auto-fix what Ruff can fix:

    uv run ruff check . --fix

## Static type checking (ty)

[ty](https://docs.astral.sh/ty/) is used for static type checking.

Run ty for the whole project:

    uv run ty check

## Running tests (with coverage)

Pytest is configured to generate coverage reports automatically via pytest-cov.

Run tests:

    uv run pytest

After the run you'll get:

- Terminal coverage summary (missing lines shown, skip-covered enabled)
- HTML report in htmlcov/index.html
- XML report in coverage.xml

## Git pre-commit hooks

Enable the repository-managed pre-commit hook so that linters and formatters run before each commit:

    git config core.hooksPath .githooks

What it does:
- Runs ty: `uv run ty check`
- Runs Ruff lint: `uv run ruff check .`
- Runs Black in check mode: `uv run black --check .`
- Blocks the commit if linting, formatting, or typing issues are found

To bypass the hook: `git commit --no-verify`
