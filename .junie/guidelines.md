# Project Guidelines
Last updated: 2025-08-27 10:51 (local)

## Project Purpose
- Provide a concise, practical reference for future FastAPI projects.
- Demonstrate integration of external systems (e.g. Kafka, MongoDB)
- Demonstrate use of test-driven development (TDD) and clean architecture.
- Demonstrate best practices for Python development.
- Demonstrate Python typing.
- Demonstrate dependency management.
- Demonstrate use of formatters, linters, type checkers, etc.

## Tech stack
- Language: Python (type-hinted, latest stable Python version)
- Web: FastAPI
- Testing: pytest + FastAPI TestClient
- Architecture: Simple layered approach
  - REST layer (app/rest): routers, request/response DTOs
  - Domain layer (app/domain): services, protocols, models
  - Adapter layer (app/adapter): integrations (e.g., Kafka, MongoDB)

## Repository conventions
- Layer boundaries
  - REST layer depends on Domain via protocols and services.
  - Domain layer should be tech-agnostic (no FastAPI imports).
  - Adapters implement external integrations and should not leak into Domain.
- DTOs vs Domain models
  - DTOs (app/rest/dto) represent API I/O shapes.
  - Domain models (app/domain/model) represent core business entities.
  - REST layer maps between DTOs and Domain models.
- Dependency injection
  - Use FastAPI dependency_overrides in tests.
  - Prefer protocols (e.g., ItemServiceProtocol) for substitutability.
- Error handling
  - 404: return empty JSON body {} where tests expect it.
  - 406: respect Accept header; return {"detail": "Not Acceptable"} when content is unsupported.
  - 422: rely on FastAPI validation for path/query/body type errors.
- Content negotiation
  - Endpoints default to JSON; ensure application/json Content-Type for success and error responses (as tests expect).

## Code style
- Type hints: required for public functions and methods.
- Formatting: use Black-compatible style (default line length 88).
- Imports: standard library, third-party, local; keep sorted where possible.
- Naming: follow Python conventions, e.g. snake_case for functions/variables, PascalCase for classes, UPPER_CASE for constants.
- Docstrings: Don't add doc strings.
- Comments: Don't add comments unless they are part of the code. Ensure code is readable like a book without comments.

## Testing and TDD
- Framework: pytest.
- Location: tests/ mirrors app/ structure
- Prefer unit tests for domain/services and route tests for REST.
- Do not rely on external dependencies but use testccontainers to mock them.
- Patterns for REST route tests:
  - Use TestClient(app) for REST.
  - Override dependencies via app.dependency_overrides.
  - Provide fakes implementing Protocols for service boundaries.
- Implement component tests (tests/componenttests) integrating all parts of the system using TestClient and TestContainers.

## Dependency management
- Use uv as package manager.
- Ensure uv.lock is up-to-date when changing dependencies.

## FastAPI patterns
- Routers live in app/rest/; expose path operations with clear tags and response_model pointing to DTOs.
- Validate inputs via Pydantic models where applicable.
- Map domain entities to DTOs explicitly to avoid leaking internal representation.

## Adapters
- Keep external system specifics (e.g., Kafka producer/consumer) in app/adapter/.
- Abstract behind protocols if domain needs to call them; inject via constructor or FastAPI dependency.

## Observability & logging
- Use standard logging; avoid printing in production code.
- Keep logging to a minimum; only log when something is wrong.

## Security basics
- Never commit secrets; use environment variables or Docker secrets.
- Validate inputs; avoid exposing internal errors in responses.
- Keep dependencies updated; prefer pinned versions where necessary.

## Review checklist
- [ ] Code compiles and tests pass locally.
- [ ] Code is formatted consistently using `uv run black .`.
- [ ] Code is linted using `uv run ruff check --fix .`.
- [ ] Code is type checked using `uv run ty check`.
- [ ] REST/Domain/Adapter boundaries respected.
- [ ] DTOs and models mapped correctly; response schemas match tests.
- [ ] Errors and content negotiation behave as expected by tests.
- [ ] No dead code or unused imports.
- [ ] README.md is up-to-date.

## Pre-submit requirements (Junie)
- Before calling the `submit` tool, Junie must execute and pass all items from the Review checklist and report their outcomes in the `<UPDATE>` section:
  - Run tests: `uv run pytest -q`.
  - Format code: `uv run black .`.
  - Lint and auto-fix: `uv run ruff check --fix .`.
  - Type check: `uv run ty check`.
- If any step fails, do not submit. Fix the issues or ask the User for help via `<ask_user>` according to the workflow.
- Ensure REST/Domain/Adapter boundaries and content negotiation/error handling behaviors continue to comply with these guidelines before submission.
