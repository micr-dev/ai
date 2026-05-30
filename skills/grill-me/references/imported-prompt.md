---
type: command
description: Interview the user relentlessly about a plan or design until reaching shared understanding.
---

<objective>
Interview me relentlessly about every aspect of this plan or design until we reach a shared understanding.
</objective>

<process>

Walk down each branch of the design tree, resolving dependencies between decisions one by one.

If a question can be answered by exploring the codebase, explore the codebase instead of asking.

For each question:
- Ask one focused question at a time
- Provide your recommended answer
- Explain the tradeoff briefly when the choice is non-obvious
- Use the answer to decide the next highest-leverage question

Stop only when:
- The major branches are resolved
- The key assumptions are explicit
- The remaining unknowns are either low-risk or intentionally deferred

Then provide a short summary covering:
- the agreed plan
- the open risks
- the unresolved decisions
</process>
