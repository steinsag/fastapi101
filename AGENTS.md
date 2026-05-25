# Project Guidelines
Last updated: 2026-05-25

## Project purpose
- Demonstrate a practical TDD workflow for a small FastAPI backend.
- Use tests as the primary driver for behavior, design, and regression safety.
- Show a component-test-oriented strategy instead of relying only on isolated unit tests.
- Demonstrate a layered backend where REST endpoints call domain services, domain code stays framework-agnostic, and adapters own external integrations.
- Store item data in MongoDB and include Kafka adapter support for publishing item events.
- Show modern Python project hygiene with `uv`, Ruff, Black, `ty`, Pyrefly, pytest, and coverage.

## Current stack
- Python: `>=3.14,<4.0`, with type hints expected in production code.
- Web API: FastAPI.
- Persistence: MongoDB via PyMongo.
- Messaging: Kafka via `confluent-kafka`.
- Tests: pytest, FastAPI `TestClient`, pytest-cov, Testcontainers for MongoDB and Kafka.
- Tooling: `uv`, Ruff, Black, `ty`, Pyrefly.

## Architecture
- `app/rest`: FastAPI routers and API DTOs.
- `app/domain`: business services, protocols, and domain models.
- `app/adapter`: infrastructure integrations such as MongoDB and Kafka.
- `tests/rest`: route-level behavior tests using fakes and dependency overrides.
- `tests/domain`: domain service tests.
- `tests/adapter`: integration-style adapter tests against Testcontainers where appropriate.
- `tests/componenttests`: component tests that exercise the FastAPI app through `TestClient` with real containerized dependencies.
- `tests/test`: shared test fixtures, test data, and test-container helpers.

## Design rules
- Keep domain code independent of FastAPI, PyMongo, Kafka, Testcontainers, and other infrastructure details.
- REST code may depend on domain protocols and services, but should not contain persistence or messaging logic.
- Adapter code may depend on external clients and environment variables, but must return or accept domain models at the boundary.
- Use protocols for substitutable service boundaries, especially where REST tests need fakes.
- Keep DTOs in `app/rest/dto` and domain models in `app/domain/model`.
- Map explicitly between DTOs and domain models; do not let API schemas leak into domain code.
- Do not add production-only hooks or alternate code paths just to make tests easier.

## API behavior
- Endpoints return JSON by default.
- Successful and error responses should have `application/json` content type where tests assert it.
- `GET /items/{item_id}` returns the item DTO when found.
- Missing items return `404` with an empty JSON body `{}`.
- Unsupported `Accept` headers return `406` with `{"detail": "Not Acceptable"}`.
- Internal errors are hidden behind `500` with `{"detail": "Internal Server Error"}`.
- Let FastAPI/Pydantic handle standard validation failures such as malformed path, query, or body values.

## TDD and testing
- Start behavior changes with a failing test whenever practical.
- Follow the detailed testing rules in [TEST_STRATEGY.md](TEST_STRATEGY.md).

## Local development
- Install dependencies with `uv sync --python 3.14`.
- Run the API locally with `uv run fastapi dev app/main.py`.
- For local MongoDB, use `docker compose -f scripts/docker/docker-compose.yml up -d`.
- `MONGODB_URL` must include a database name, for example `mongodb://test:test@localhost:27017/test?authSource=test`.
- Kafka adapter code reads `KAFKA_ENDPOINT`, `KAFKA_USERNAME`, `KAFKA_PASSWORD`, and `KAFKA_SECURITY_PROTOCOL`.
- Keep `uv.lock` updated whenever dependencies change.

## Code style
- Use Black-compatible formatting with line length 88.
- Keep imports sorted in standard library, third-party, then local groups where possible.
- Use snake_case for functions and variables, PascalCase for classes, and UPPER_CASE for constants.
- Public production functions and methods should be typed.
- Do not add docstrings by default.
- Avoid comments unless they clarify non-obvious code.
- Use standard logging instead of `print` in production code, and log only when it adds operational value.

## Verification
- Preferred full verification command: `uv run scripts/verify.py`.
- The verification script runs, in order:
  - `ruff check --fix .`
  - `black .`
  - `ty check`
  - `pyrefly check`
  - `pytest`
- For targeted work, it is acceptable to run the narrow pytest file first, then run full verification before handing off substantial code changes.

## Review checklist
- [ ] Behavior was driven or protected by tests.
- [ ] Component coverage was considered for REST/domain/adapter workflows.
- [ ] REST, domain, and adapter boundaries remain clean.
- [ ] DTOs and domain models are mapped explicitly.
- [ ] MongoDB and Kafka details stay in adapters.
- [ ] Test coverage remains close to 100% where practical.
- [ ] Error handling and content negotiation still match tests.
- [ ] `uv.lock` is updated if dependencies changed.
- [ ] `README.md` is updated when setup, commands, or behavior changed.
- [ ] `uv run scripts/verify.py` passes before final handoff for substantial changes.
