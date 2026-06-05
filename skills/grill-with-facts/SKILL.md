---
name: grill-with-facts
description: Stress-tests a plan through one-question-at-a-time design grilling and records resolved decisions, risks, vocabulary, and requirements in .facts files. Use when the user says grill-with-facts, wants a plan grilled while preserving decisions, or needs requirements captured in facts instead of chat.
---

# Grill With Facts

Stress-test a plan until the important decisions are explicit, then write the durable outcomes into `.facts`. The goal is not to produce a chat transcript. The goal is to leave the project with crisp `@spec` facts, honest `@draft` risks, and domain vocabulary a future agent can use.

## Start

1. Identify the plan, proposal, or design being grilled.
2. Load the facts workflow and current fact sheet:

```sh
facts skills show facts
facts ll
facts check
facts ll --tags "draft or spec"
```

3. Ask one high-leverage question at a time.
4. After each settled answer, immediately record the outcome with `facts add` or `facts edit`.

If no fact sheet exists, ask before running `facts init`. Do not create a separate notes document as a substitute for facts.

## Orient

- Read current `.facts` files before asking questions.
- Use section filters when the sheet is large, such as `facts ll --section feature/area` and `facts check --section feature/area`.
- Read relevant docs and code when they can answer a question directly.
- If the proposal conflicts with existing facts, docs, or code, surface the contradiction before continuing.
- Use the `## domain` section as the vocabulary source. Add a domain fact only when a concept will recur across multiple facts.
- For relevant manual facts shown by `facts check`, inspect the code and report each as `PASS` or `FAIL` with a one-line reason.

## Grill One Branch At A Time

- Ask one focused question at a time.
- Walk down the highest-dependency branch first, then move to the next branch after it is resolved or explicitly deferred.
- For each question, provide a recommended answer and the concrete tradeoff.
- Prefer dependency-resolving questions over style or low-risk details.
- Challenge vague terms, hidden assumptions, irreversible decisions, missing edge cases, and weak defaults.

## Log Facts Immediately

Convert each settled answer into atomic, declarative facts as soon as it is resolved:

```sh
facts add "the precise requirement or decision" --section feature/area --tags "spec"
facts add "the rough open idea that still needs refinement" --section feature/area --tags "draft"
facts add "a Term is a precise domain definition" --section domain
```

Use lifecycle tags deliberately:

- `@draft` for rough ideas, unresolved questions, and risks that still need refinement.
- `@spec` for precise intended behavior, accepted constraints, and decisions ready to implement.
- `@implemented` only after code inspection or validation proves the fact already holds.
- Untagged facts only for current ground truth verified against the codebase.

Do not use facts for chat transcript fragments. Facts must be behavioral, atomic, stable, falsifiable, and useful to a future agent implementing the project.

## Companion Skills

This skill captures and pressure-tests requirements. It does not replace the facts lifecycle skills:

- Use `facts-refine` when the session is mainly about turning existing `@draft` facts into precise `@spec` facts.
- Hand off to `facts-implement` after grilling when the resulting `@spec` facts are ready to build.
- Use `facts-discover` only when the user explicitly asks to audit, bootstrap, discover, or sync the fact sheet against existing code.

During a grilling session, stay focused on requirement capture. Do not start implementation unless the user redirects.

## Add Commands Sparingly

Add `command:` only when the command genuinely tests the claim and would fail if the claim became false. Prefer honest manual facts over keyword-grep checks that create false confidence.

Good commands are fast, read-only, idempotent, and specific:

```sh
facts add "CLI exposes the check subcommand" --section cli --command "facts check --help >/dev/null"
```

## Verify And Close

After each coherent batch of captured facts:

```sh
facts check
facts lint
```

Close with:

- facts added or changed
- decisions captured as `@spec` and unresolved risks captured as `@draft`
- relevant manual facts verified as `PASS` or `FAIL`
- contradictions between the plan, facts, docs, or code
- the next lifecycle step, usually `facts-refine` for remaining drafts or `facts-implement` for ready specs

Stop only when the major decision branches are resolved or intentionally deferred, every durable outcome has been captured in `.facts`, and remaining unknowns are represented as `@draft` facts with clear wording.
