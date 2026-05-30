# Repository Test Design Reference

## Source-Backed Principles

- Google Testing Blog: tests should focus on the public API and user-facing behavior; implementation details should usually stay out of tests. Tests independent of implementation are easier to maintain and understand.
- Google Testing Blog: a useful first approximation is 70 percent unit, 20 percent integration, 10 percent E2E, while preserving the pyramid shape rather than treating the ratio as law.
- Martin Fowler's Practical Test Pyramid: build tests at different granularities, keep higher-level tests fewer, push tests down when lower-level tests provide the same confidence, and avoid duplication across layers.
- Playwright best practices: browser tests should verify user-visible behavior, isolate each test, avoid third-party dependencies, use resilient locators, and use web-first assertions instead of manual racy checks.
- Empirical LLM unit-test research: LLM-generated unit tests can suffer from syntactic invalidity, weak defect detection, poor specific input generation, and prompt sensitivity. Validity and defect-detection value matter more than raw coverage.
- Empirical coding-agent mocking research: agent-authored tests are more likely to add mocks than non-agent tests; this can make tests easier to generate but less effective at validating real interactions.

## Layer Selection

Choose the cheapest layer that catches the bug class:

| Behavior | Default Test |
| --- | --- |
| Pure function, parser, formatter, policy, reducer | Unit test with table cases |
| Error handling, boundary values, validation | Unit test plus named regression case |
| Database query, repository method, migration behavior | Narrow integration test against local DB or in-memory equivalent |
| HTTP route, CLI command, SDK method | Contract or API-level test |
| UI state from component props/state | Component test or DOM test |
| Full checkout/login/import/export journey | One E2E smoke/regression test |
| Third-party provider behavior | Local fake, recorded fixture, or contract test against documented response |

## What Makes A Test Efficient

Efficient tests are not just fast. They provide specific failure information with the smallest stable setup.

- Fast feedback: run targeted tests first, then the repo's broader command.
- Locality: a failing test points near the defect.
- Determinism: no real network, uncontrolled clock, shared account, global storage, or random order dependency.
- Minimal duplication: do not retest every lower-level branch through E2E.
- Maintainability: small fixtures, clear data builders, and assertions that read like behavior documentation.
- Refactor tolerance: changing internals should not require test rewrites when behavior is unchanged.

## AI-Generated Test Review Rubric

Score each generated test before accepting it:

| Question | Pass Criteria |
| --- | --- |
| What claim does this test make? | A reviewer can state the invariant in one sentence. |
| Would it fail on the bug? | It fails before the fix or after an intentional mutation. |
| Is the assertion meaningful? | It checks exact behavior, error, state, persistence, or visible output. |
| Is the setup real? | It uses existing helpers, fixtures, public APIs, and deterministic local dependencies. |
| Are mocks justified? | Only external, slow, nondeterministic, paid, or failure-hard dependencies are mocked. |
| Is the layer appropriate? | No full-stack test for behavior a unit/integration test can prove. |
| Does it fit the repo? | File location, naming, runner APIs, and style match nearby tests. |

Reject or rewrite when any answer is weak.

## Prompt Pattern For Agents

When asking an AI model to write tests, do not ask for coverage first. Use this shape:

```text
Read the existing test conventions and the public contract first.
Write tests for these behaviors: [specific invariants].
Use the smallest test layer that proves each invariant.
Prefer real collaborators or existing fakes; mock only external nondeterministic boundaries.
Each test must have a meaningful assertion and must be able to fail for the intended bug.
Run the targeted test command and report the exact command and result.
```

## Anti-Patterns And Fixes

| Bad Default | Why It Is Bad | Fix |
| --- | --- | --- |
| `expect(result).toBeDefined()` | Executes code but proves almost nothing. | Assert exact value, state, output, or error. |
| Mocking the subject under test | Tests the mock, not production behavior. | Instantiate the real subject. |
| Mocking every dependency | Breaks real collaboration confidence. | Use real cheap collaborators and mock only hard boundaries. |
| Testing private helpers | Couples tests to refactors. | Test through public behavior. |
| Snapshotting broad output | Hides meaning and causes brittle diffs. | Assert salient fields or use small inline snapshots. |
| Sleeping in UI tests | Produces flakes and slow suites. | Wait on observable state or framework auto-wait assertions. |
| One giant E2E test | Slow, hard to debug, broad blast radius. | Split lower-layer cases and keep E2E as smoke coverage. |
| Updating snapshots blindly | Locks in accidental output. | Inspect diff and explain the behavior change. |
| Accepting generated green tests | May encode the current bug. | Run against pre-fix code or mutate the implementation. |

## Final Verification Order

1. Targeted test command for the new or changed tests.
2. Existing related suite for the module.
3. Repo's normal typecheck/build/lint command when relevant.
4. For browser tests, inspect trace/screenshot only when the failure or behavior is visual.
5. Report commands run, pass/fail status, and any unrelated failures separately.
