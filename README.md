## Initial setup

This project uses package manager [uv](https://github.com/astral-sh/uv) to manage dependencies.

    uv sync

## Running tests (with coverage)

Pytest is configured to generate coverage reports automatically via pytest-cov.

Run tests:

    uv run pytest

After the run you'll get:

- Terminal coverage summary (missing lines shown, skip-covered enabled)
- HTML report in htmlcov/index.html
- XML report in coverage.xml

## Static type checking (ty)

[ty](https://docs.astral.sh/ty/) is configured in `pyproject.toml` and installed via the dev dependency group.

Run ty for the whole project:

    uv run ty check

If you haven't installed dev dependencies yet, run the initial setup above (`uv sync`).

## Creating and running a Docker container

Build the container:

docker build -t fastapi101

Run the container:

docker run -p 8000:8000 fastapi101

The app is listening on port 8000 locally. Try: http://localhost:8000/items/5?q=somequery
