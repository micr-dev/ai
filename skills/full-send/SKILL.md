---
name: full-send
description: Carry an explicitly authorized coding task through implementation, verification, and delivery. Use when the user asks for full end-to-end execution; this skill does not add permissions beyond the user's request and active policies.
version: 1.0.0
metadata:
  hermes:
    tags: [coding, implementation, verification, pull-requests]
---

# Full Send

Take the assigned work to a verified endpoint instead of stopping after diagnosis or a partial patch. Follow the active session rules, the user's scope, and repository instructions. Full-send language means persistence to completion, not blanket authority.

## Workflow

1. Establish the requested outcome, constraints, protected work, and what will prove completion. Ask only when a missing decision materially changes behavior or risk.
2. Read the applicable repository instructions and inspect its current state before editing. Preserve unrelated changes and avoid adjacent cleanup.
3. Identify which actions the user authorized. Implement the smallest complete change, then run the relevant checks. If a check fails, diagnose and fix the cause; never weaken the check to claim success.
4. Review the final diff and check that the implementation matches the request. For pull requests, inspect relevant review findings and required checks; fix findings that apply and verify the result again.
5. Stop at the user's authorization boundary. A request to finish the task does not by itself authorize a commit, push, merge, release, deployment, production change, paid service, or contact with another person. Do those only when explicitly in scope and allowed by higher-priority policy. Without merge authorization, leave the change verified and review-ready.
6. If blocked, finish any independent authorized work, state what evidence is missing, and name the smallest action needed to proceed. Do not repeat a failed route without new evidence.

## Completion report

Lead with the result. List the change, the checks and their actual outcomes, and any remaining blocker or action outside the authorized scope. Do not claim a merge, deployment, or other external result unless it happened and was verified.

## Source

Adapted from the Full Send workflow described in [Theo's short](https://x.com/NerdSnipePod/status/2110347739644969044) and the PR example in [the related episode transcript](https://moderncreator.app/2026-10-09-theo-t3-gg-finally-a-good-small-model). The source describes an agent taking a PR through review and merge; this version preserves the end-to-end intent while keeping authorization specific to each task.
