---
name: write-better-error-messages
description: Use when reviewing, designing, or rewriting user-facing error messages, validation copy, failure states, toasts, dialogs, and support paths. Helps agents make errors specific, calm, accountable, actionable, and clear about what happened and what the user can do next.
---

# Write Better Error Messages

Use this skill to turn vague or stressful failure copy into useful product guidance.

## Core Questions

Before approving an error message, answer:

1. What user-visible action failed?
2. What is the clearest honest reason the product can provide?
3. Was any user work saved, preserved, or left unchanged?
4. What should the user do next?
5. What escape path exists if the next step does not work?

If the product cannot answer these questions, flag the product or engineering gap instead of only rewriting the sentence.

## Avoid

- Do not lead with jokes, cute phrasing, or casual interjections in serious flows.
- Do not blame the user, a browser, an integration, or a third-party service.
- Do not expose implementation details unless they help the user act.
- Do not use "Something went wrong" when the system has a more specific cause.
- Do not offer "try again later" as the only path when a support, retry, save, cancel, or recovery option exists.
- Do not imply data was lost or changed unless the system knows that happened.

## Prefer

- Start with the outcome: "We couldn't upload the file" or "Your changes were saved, but the invite was not sent."
- Add the useful cause: "because the file is larger than 25 MB" or "because your session expired."
- Reassure only when true: "Your draft is still saved" or "No payment was collected."
- Give one concrete primary action: "Choose a smaller file", "Sign in again", "Reconnect the account."
- Provide a fallback for blocked users: support, help docs, export, download, save draft, or contact path.

## Rewrite Workflow

1. Identify the context: user goal, screen, action, stakes, data at risk, and whether the user is blocked.
2. Identify the cause: validation rule, permission issue, service failure, timeout, unavailable feature, or unknown fallback.
3. Classify the current copy: generic, unclear, jargon-heavy, blaming, tone mismatch, missing reassurance, or missing next step.
4. Draft the replacement:
   - Title: the failed or partial outcome.
   - Body: cause and preserved state, if known.
   - Primary action: the best next step.
   - Fallback: support or escape route.
5. Remove words that do not help the user understand, recover, or trust the product.
6. Recheck the Core Questions.

## Inventory Format

For batches of errors, keep a compact inventory:

| Field | Use |
| --- | --- |
| Surface | Page, component, toast, dialog, email, or API response. |
| Current copy | Exact text users see today. |
| Trigger | Condition that shows the error. |
| Cause known? | Whether the system can explain the failure. |
| Blocking? | Whether the user can continue. |
| Affected state | What changed, failed, or stayed preserved. |
| Proposed copy | Title, body, action, and fallback. |
| Follow-up | Engineering, design, instrumentation, or support work needed. |

Prioritize errors that block important tasks, appear frequently, or create trust risk.

## Output Format

When rewriting, use:

```markdown
Current: "..."
Issue: Generic / unclear / jargon / blame / tone mismatch / missing reassurance / missing next step
Rewrite:
Title: ...
Body: ...
Primary action: ...
Fallback: ...
Reasoning: ...
```

Keep reasoning brief and tied to the user's recovery path.
