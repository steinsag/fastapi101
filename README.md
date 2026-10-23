
## Initial setup

This project uses package manager [uv](https://github.com/astral-sh/uv) to manage dependencies.
Run the following to install all dependencies:

    uv sync --python 3.14

## Running the service locally

Start MongoDB and Kafka via Docker Compose (one-time seed included):

    docker compose -f scripts/docker/docker-compose.yml up -d

This starts MongoDB on localhost:27017 and creates an application user on DB "test":
- username: test
- password: test
- database: test

On the first startup, it also seeds the "items" collection with a sample item available through this API id:

    507f1f77bcf86cd799439011

Kafka is available on localhost:9092.

Set environment variables for the app to connect to MongoDB and Kafka (note the database name is part of the MongoDB URL path):

    export MONGODB_URL="mongodb://test:test@localhost:27017/test?authSource=test"
    export KAFKA_ENDPOINT="localhost:9092"
    export KAFKA_USERNAME="testuser"
    export KAFKA_PASSWORD="testpass"
    export KAFKA_SECURITY_PROTOCOL="PLAINTEXT"

Install dependencies and run the API locally (use FastAPI CLI for better dev experience: auto-reload, live reload for static files, improved error pages):

    uv sync --python 3.14
    uv run fastapi dev app/main.py

The app listens on http://localhost:8000. Try fetching the seeded item:

    curl http://localhost:8000/items/507f1f77bcf86cd799439011

Expected response:

    {"id": "507f1f77bcf86cd799439011", "name": "Sample Item", "price": 107.99}

Create a new item:

    curl -i -X POST http://localhost:8000/items \
      -H "Content-Type: application/json" \
      -H "Accept: application/json" \
      -d '{"name":"New Item","price":12.99}'

Expected response status is `201 Created` with this body shape:

    {"id":"...","name":"New Item","price":12.99}

To stop MongoDB and Kafka when finished:

    docker compose -f scripts/docker/docker-compose.yml down

## Creating and running a Docker container

Build the container:

    docker build -t fastapi101 .

Run the container (provide MongoDB and Kafka connection via env vars):

    docker run -p 8000:8000 \
      -e MONGODB_URL="mongodb://test:test@host.docker.internal:27017/test?authSource=test" \
      -e KAFKA_ENDPOINT="host.docker.internal:9092" \
      -e KAFKA_USERNAME="testuser" \
      -e KAFKA_PASSWORD="testpass" \
      -e KAFKA_SECURITY_PROTOCOL="PLAINTEXT" \
      fastapi101

The app is listening on port 8000 locally. Try: http://localhost:8000/items/507f1f77bcf86cd799439011

## Verify (format, lint, type-check, tests)

One command to auto-fix formatting/lints, run type checks, and tests:

      uv run scripts/verify.py

This runs, in order: `ruff check --fix .`, `black .`, `ty check`, `pyrefly check`, `pytest`.

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

## Static type checking (pyrefly)

[pyrefly](https://pyrefly.org/) is used as an additional static type checker.

Run pyrefly for the whole project:

    uv run pyrefly check

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
- Runs pyrefly: `uv run pyrefly check`
- Runs Ruff lint: `uv run ruff check .`
- Runs Black in check mode: `uv run black --check .`
- Blocks the commit if linting, formatting, or typing issues are found

To bypass the hook: `git commit --no-verify`
