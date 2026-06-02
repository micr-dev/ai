---
name: grill-with-facts
description: Stress-tests a plan through one-question-at-a-time design grilling and records resolved decisions, risks, vocabulary, and requirements in .facts files. Use when the user says grill-with-facts, wants a plan grilled while preserving decisions, or needs requirements captured in facts instead of chat.
---

# Grill With Facts

Interview the user relentlessly about every aspect of a plan until there is shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one by one, and use `.facts` as the durable ledger so decisions do not vanish into chat history.

1. Identify the plan, proposal, or design being grilled.
2. Load the existing fact sheet:

```sh
facts ll
facts check
facts ll --tags "draft or spec"
```

3. Ask one high-leverage question at a time.
4. After each answer, immediately record durable outcomes in facts.

If no fact sheet exists, ask before running `facts init`. Do not create a separate notes document as a substitute for facts.

### 1. Orient

- Read the current `.facts` files before asking questions.
- Read relevant docs and code when they can answer a question directly.
- If the proposal conflicts with existing facts or code, surface the contradiction before continuing.
- Use the `## domain` section as the vocabulary source. Add a domain fact only when a concept will recur across multiple facts.

### 2. Grill One Branch At A Time

- Ask one focused question at a time.
- Walk down the highest-dependency branch first, then move to the next branch after it is resolved or explicitly deferred.
- For each question, provide your recommended answer and the concrete tradeoff.
- Prefer dependency-resolving questions over style or low-risk details.
- Challenge vague terms, hidden assumptions, irreversible decisions, and missing edge cases.
- If the user answers with a weak or risky default, say so directly and propose a better default.

### 3. Log Facts Immediately

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

### 4. Handle Open Risks

When a risk or unknown matters but is not resolved, log it as a draft fact instead of leaving it in chat:

```sh
facts add "decision needed: webhook retries must define max attempts and dead-letter behavior" --section risks/payments --tags "draft"
```

When the user later resolves it, edit or replace the draft with precise `@spec` facts.

### 5. Add Commands Sparingly

Add `command:` only when the command genuinely tests the claim and would fail if the claim became false. Prefer honest manual facts over keyword-grep checks that create false confidence.

Good commands are fast, read-only, idempotent, and specific:

```sh
facts add "CLI exposes the check subcommand" --section cli --command "facts check --help >/dev/null"
```

### 6. Verify And Close

After each coherent batch of captured facts:

```sh
facts check
facts lint
```

Close with:

- the facts added or changed
- the decisions now captured as `@spec`
- the unresolved risks still captured as `@draft`
- any contradictions between the plan, facts, docs, or code

## Stop Condition

Stop only when the major decision branches are resolved or intentionally deferred, every durable outcome has been captured in `.facts`, and remaining unknowns are represented as `@draft` facts with clear wording.
