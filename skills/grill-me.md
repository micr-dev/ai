---
name: prompts-grill-me
description: Interview the user relentlessly about a plan, design, implementation approach, or architecture proposal until the key assumptions, dependencies, decisions, and risks are explicit. Use when the user says grill-me, asks to be challenged on a plan, wants rigorous design questioning, or needs an idea stress-tested before implementation.
---

# Prompts Grill Me

Run a focused design interview instead of jumping straight into implementation.

## Workflow

1. Start by identifying the plan, design, or proposal being examined.
2. Walk down the highest-leverage branch of the decision tree first.
3. Ask one focused question at a time.
4. Give a recommended answer with a brief tradeoff when the choice is non-obvious.
5. Use each answer to decide the next question rather than dumping a questionnaire.

## Operating Rules

- If a question can be answered by exploring the codebase, inspect the codebase instead of asking.
- Prefer dependency-resolving questions over stylistic or low-risk questions.
- Surface assumptions explicitly when they materially affect the design.
- Challenge weak reasoning directly and propose a better default when one exists.
- Keep going until the major branches are resolved or intentionally deferred.

## Stop Condition

Stop only when:

- the major branches are resolved
- the key assumptions are explicit
- the remaining unknowns are low-risk or intentionally deferred

## Closeout

End with a short summary covering:

- the agreed plan
- the open risks
- the unresolved decisions
