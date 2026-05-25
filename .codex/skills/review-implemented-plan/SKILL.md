---
name: review-implemented-plan
description: Review completed code changes after a plan, checklist, or implementation has been carried out. Use when Codex has just implemented a plan, finished a multi-step change, is preparing a final handoff, or the user asks for a post-implementation review focused on avoiding over-engineering, preserving clean code principles such as SOLID, DRY, and SRP, and confirming tests fully cover the changed behavior.
---

# Review Implemented Plan

## Review Workflow

Perform a focused engineering review of the implemented changes before handoff.

1. Reconstruct the implemented scope from the conversation, plan, and local diff.
2. Inspect `git status --short`, `git diff --stat`, and the relevant `git diff`.
3. Separate files changed for the task from unrelated pre-existing work. Do not revert or judge unrelated changes unless they affect the implemented behavior.
4. Review production code, tests, configuration, and docs that changed.
5. Run the narrowest meaningful tests first when practical, then broader verification for substantial changes.
6. Fix clear issues directly when acting as the implementer. If the user asked for review only, report findings without editing.
7. Re-run affected tests after fixes and include the verification result in the handoff.

## Review Priorities

Prioritize concrete defects over style preferences.

- Correctness: Verify the implementation satisfies the plan and does not introduce regressions, edge-case failures, hidden behavior changes, or broken public contracts.
- Simplicity: Flag abstractions, indirection, generalized helpers, configuration, or alternate paths that are not justified by current requirements.
- SOLID and SRP: Check that each class, function, module, route, service, and adapter has a focused responsibility and that dependencies point in the expected direction.
- DRY: Remove meaningful duplication when it obscures behavior or increases maintenance cost. Do not force premature abstraction for small, clearer repetition.
- Test coverage: Confirm the behavior is protected at the right level: component tests for cross-boundary workflows, route tests for API behavior, domain tests for business rules, and adapter tests for infrastructure mapping or integration.
- Maintainability: Prefer explicit mappings, clear names, local patterns, typed public production APIs, and small changes with limited blast radius.

## Test Coverage Checks

Treat tests as part of the implementation, not as a final checkbox.

- Identify every new or changed behavior and find the test that would fail if that behavior regressed.
- Check success paths, relevant error paths, validation behavior, side effects, and boundary mappings.
- Confirm tests assert observable behavior rather than implementation details.
- Watch for tests that pass only because fakes duplicate production bugs or because assertions are too broad.
- If coverage is incomplete, add focused tests before changing production code unless the review is explicitly read-only.
- For this project, prefer the repository verification command `uv run scripts/verify.py` for substantial changes, and use targeted `uv run pytest ...` runs during iteration.

## Output Format

When reporting a review, lead with findings ordered by severity. Use file and line references for each finding.

Use this structure:

```markdown
**Findings**
- [P1] Brief issue title - `path/to/file.py:42`
  Explain the behavioral risk and why it matters.

**Tests**
- `command` passed.
- `command` was not run: reason.

**Summary**
One or two sentences describing the reviewed scope and residual risk.
```

If there are no findings, state that clearly and still mention test coverage and any verification that was or was not run.
