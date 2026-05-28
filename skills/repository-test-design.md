---
name: repository-test-design
description: Designs efficient, maintainable repository test suites and reviews AI-generated tests for real defect-detection value. Use when adding tests, improving test coverage, fixing flaky tests, choosing unit/integration/E2E scope, or preventing shallow AI-written tests.
---

# Repository Test Design

## Quick Start

Before writing tests, identify the contract under test and the cheapest layer that can prove it.

1. Read the existing test runner, nearby tests, public API, and the code path's callers.
2. Write or revise tests around observable behavior, not private structure.
3. Prefer fast unit/component tests for pure logic and narrow integration tests for boundaries.
4. Keep E2E tests for critical user journeys only.
5. Prove each new test can fail for the right reason before trusting it.

## Workflow

### 1. Map The Existing Test Shape

- Detect the package manager from lockfiles and use repo scripts first.
- Read nearby tests before inventing style, fixture names, or helpers.
- Identify the contract source: docs, public types, CLI help, API schema, issue text, existing behavior, or caller expectations.
- Find the smallest runnable target command for the touched area.

### 2. Pick The Test Layer

- Unit test: pure logic, validation, formatting, state transitions, error mapping.
- Component or narrow integration test: multiple local collaborators, database/repository boundary, API handler, file system, parser, queue, cache, auth policy.
- Contract test: public protocol, SDK/API surface, CLI output, persistence format, provider compatibility.
- E2E test: one or two business-critical user journeys where lower layers cannot prove wiring.

Push tests down when they catch the same bug with less runtime, fewer moving parts, and clearer failure output.

### 3. Write High-Signal Tests

- Name the behavior in business or API terms.
- Use Arrange, Act, Assert or Given, When, Then structure.
- Assert specific outcomes: returned values, persisted records, emitted events, HTTP status/body, visible UI state, exit code and stderr.
- Include negative, boundary, and regression cases only when they defend a real invariant.
- Prefer real collaborators, in-memory fakes, or local fixtures when they are cheap and deterministic.
- Mock only uncontrolled, slow, paid, nondeterministic, or failure-hard dependencies.

### 4. Review AI-Generated Tests

Reject tests that only increase count or coverage. A generated test must survive this checklist:

- It fails against the pre-fix bug or against a small intentional mutation.
- It asserts behavior, not that a mock was called unless interaction is the contract.
- It does not mock the subject under test or all meaningful collaborators.
- It uses existing repo helpers and data factories instead of fabricated APIs.
- It has no broad snapshots, non-null assertions, sleep-based waits, or private-method expectations.
- It runs with the normal repo command and does not require hidden state.

## AI Failure Shields

Common model defaults to block:

- Green-bar bias: writing tests that match current buggy behavior.
- Coverage theater: executing lines with weak assertions like truthy, defined, length greater than zero.
- Over-mocking: replacing real cheap collaborators, then testing the mock setup.
- Implementation coupling: asserting call order, private helpers, CSS classes, internal arrays, or exact logs.
- E2E overreach: using browser or full-stack tests for behavior a lower layer can prove.
- Fixture hallucination: inventing factories, routes, env vars, or package APIs that do not exist.
- Flake injection: sleeps, shared mutable data, network calls, real time, random IDs without control.

## References

Use [REFERENCE.md](REFERENCE.md) for source-backed rationale, layer selection guidance, and AI-specific anti-pattern details.
