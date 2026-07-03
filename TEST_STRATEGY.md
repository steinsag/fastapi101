# Test Strategy

This project uses tests to drive behavior and preserve the REST, domain, and adapter boundaries.

## TDD Workflow

- Start behavior changes with a failing test whenever practical.
- Prefer tests that assert observable behavior over implementation details.
- Keep test coverage close to 100% where practical, especially for production code and behavior at architectural boundaries.
- Keep test data builders and fixtures in `tests/test`.
- Use Testcontainers for MongoDB and Kafka integration; do not require a developer's local services for tests.
- Do not add production-only hooks or alternate code paths just to make tests easier.

## Test Structure

- Put local fixtures at the top of the test file.
- Put sunny test cases as first test cases in a test file.
- Put error and edge-case tests after the sunny cases.
- Structure each test as given, when, then by separating those phases with empty lines.
- Do not add comments just to label given, when, or then.

## Test Layers

### Component tests
- Location: `tests/componenttests`.
- Exercise the FastAPI app through `TestClient` with real containerized dependencies.
- Prove that REST, domain services, MongoDB, and Kafka work together.
- For each workflow, keep coverage to one sunny case and one representative error case.
- Do not repeat the full HTTP status-code matrix here.

### REST route tests
- Location: `tests/rest`.
- Exercise HTTP behavior through `TestClient` with fake services and dependency overrides.
- Own the HTTP contract: status codes, response bodies, content type, content negotiation, and hidden internal errors.
- Map domain/service outcomes and exceptions to the correct HTTP responses.
- Restore app dependency overrides after each test.

### Domain service tests
- Location: `tests/domain`.
- Exercise framework-agnostic domain behavior with fake providers and publishers.
- Own service orchestration rules, such as persistence before publishing and logging publish failures.
- Assert that provider and publisher boundaries are called with the expected values.
- Ensure relevant domain exceptions propagate so the REST layer can map them.
- Do not import FastAPI, PyMongo, Kafka, or Testcontainers.

### Adapter tests
- Location: `tests/adapter`.
- Exercise infrastructure mapping and integration details against Testcontainers where appropriate.
- Own MongoDB and Kafka-specific behavior, such as ObjectId conversion, persisted document shape, Kafka key, topic, and payload.
- Cover adapter error contracts, especially whether infrastructure errors are propagated unchanged or translated into domain errors.
- Keep external technology types inside adapter code and adapter/component tests.

## Error Coverage

- REST tests cover all expected HTTP status codes for a route.
- Domain tests cover all domain/service exceptions that REST must handle.
- Adapter tests cover infrastructure-specific failures or mappings, including persistence and publish failures.
- Component tests include only one representative error case per workflow to prove real-stack error handling remains connected.

## Verification

- Run a narrow pytest target first while developing a behavior.
- Run `uv run scripts/verify.py` before handing off substantial changes.
