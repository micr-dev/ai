# Research jobs: retrieval and task-based deep research

Checking or retrieving an existing run is read-only with respect to the provider job and is not a reason to create another one. For new investigations, the agent may choose deep research under the selection criteria below without an explicit request or another confirmation. A bounded index command named `research search-papers` is ordinary retrieval, not a deep-research job.

## Existing runs

For a supplied Parallel research run ID, check status or retrieve the existing result:

```bash
parallel-cli research status RUN_ID --json
parallel-cli research poll RUN_ID -o /tmp/topic-report --timeout 540
```

Use the same run ID after interruptions; never create a replacement job merely because a local wait timed out. A polling timeout does not cancel server-side work. Follow the current harness's background-job waiting policy; do not create manual sleep/poll loops.

Polling saves `.json` and, for a text-schema run, `.md`. Existing files require `--force` to overwrite; choose another path unless replacement is intended. Read the result and inspect important citations before delivering it. A completed provider job is not evidence that its claims are correct. For FindAll IDs, use [Entity discovery](entities.md), not the research commands above.

## Recover before replacing

Before switching providers, changing research depth, or substituting manual searches after an error:

1. Inspect the original response, request ID, elapsed time and provider logs. Distinguish input rejection, client timeout, server research deadline, authentication, quota and rate limits. Check automatic retries: total command duration is not necessarily one request's duration.
2. Check current help and primary documentation for a supported correction. Fix invalid input before resubmitting. For timeouts, retrieve existing work first; extend a client deadline only if the server can still finish. A longer client wait cannot extend a fixed server budget.
3. Attempt a bounded, evidence-backed recovery within the authorized scope and budget. Preserve the research questions when splitting an oversized task. Resume the same job when supported. Before a new billable request, establish the previous request's status and cost; if either is unknown, seek authorization rather than risk duplicate work. Do not repeat an unchanged failure just to confirm it.
4. Replace the provider or method only after the supported recovery fails, or record why recovery cannot proceed within access, budget, safety or deadline constraints. Report the error, correction attempted or blocker, replacement and remaining evidence gaps. A smaller probe succeeding does not prove the original task is complete.

Respect provider-specific stop rules, including CAPTCHA and YouTube rate-limit handling. Recovery does not authorize bypassing controls, changing billing or buying credits.

## Starting deep research

Choose depth by the evidence work required:

1. Use deep research when the user requests it. Otherwise, use it when the task requires sustained investigation across interdependent questions or many primary sources, or when ordinary search leaves material contradictions or evidence gaps that deeper investigation can resolve. A complex technical decision, literature review or market analysis can justify starting directly with deep research; a token preliminary search is not required.
2. Keep ordinary search and extraction for a focused fact, a known page, or a comparison that a few primary sources can resolve. Words such as "research" or "comprehensive" are signals to assess scope, not automatic escalation. A broken provider or missing credit alone does not justify deeper work.
3. Respect explicit limits such as "quick answer", "no deep research", a deadline or a spending cap. State the reason for choosing deep research and its scope briefly, then proceed without asking for permission again when it fits those limits.
4. Define the question, date range, evidence requirements, deliverable and stopping condition before starting. Choose the least costly adequate processor and a provider with working access. This permission covers bounded research using existing configured access and available allowance; it does not authorize credit top-ups, new subscriptions, exceeding a budget or disclosure of private data.
5. If the selected provider fails, follow [Recover before replacing](#recover-before-replacing). Any replacement must preserve the requested evidence scope and spending limits; report a blocker when none can.

### Optional multi-agent deep research

This procedure applies only after choosing deep research. Use one agent or one hosted research job when it can cover the scope. Delegate only when there are at least two independent, substantial questions with checkable results; add agents around a hosted job only to address named gaps.

1. **Prepare a shared brief.** Carry forward the scope, date range, evidence requirements and stopping condition defined above. Give each worker its question, shared comparison criteria, allowed tools or files, and share of the overall spending limit. Keep search queries flexible so workers can find different evidence without changing what counts as an answer.
2. **Check the method before repeating it.** For repeated assignments, complete one representative assignment first. Inspect its source passages and unresolved checks before launching the rest. Correct a method that loses evidence or confuses failed retrieval with a negative finding before scaling it.
3. **Return comparable evidence.** Each worker returns findings in this format: claim; source URL and supporting passage or location; applicable date/version; documented, observed or inferred; contradictions and unresolved checks. Workers return evidence for the coordinator's synthesis rather than separate final reports. Mark inaccessible or unverified evidence explicitly, not as proof of absence.
4. **Keep criteria consistent.** Workers report flaws in the shared criteria to the coordinator rather than redefining them. If a criterion changes, reassess every affected finding before comparing results; otherwise differences may reflect the method rather than the subject.
5. **Synthesize centrally.** The coordinator checks conclusion-driving findings against their sources, reconciles contradictions and delivers one answer under the existing delivery rules. Count independent underlying sources, not agreeing agents. Finish when each assigned question has supported findings or an explicit evidence gap.

### Parallel

Inspect `parallel-cli research processors` and `research run --help` for current tiers. The installed default is `pro-fast`; stronger tiers cost more. Research query input has a 15,000-character limit, and the inspected implementation truncates longer input. Shorten deliberately rather than losing constraints silently.

Choose freshness as well as depth. The installed processor list labels non-fast tiers as providing fresher data. For news from the last day or two or another explicitly current investigation, choose the corresponding non-fast tier (for example `pro` rather than `pro-fast`) and allow its longer latency. A faster tier is not proof that its sources cover recent events; verify source dates in the returned report.

```bash
parallel-cli research run 'Research question, evidence gaps, scope and stopping condition' \
  --processor pro-fast --text --text-description 'Requested report format and scope' \
  --no-wait --json
```

Record `run_id` and `interaction_id` as soon as creation succeeds, then follow [Existing runs](#existing-runs) for status and results.

For a continuation needed to answer the current task, select a lighter processor (`lite-fast` or `base-fast`) when the prior run already did the substantial research. Use the corresponding non-fast tier when the follow-up requires fresher sources. Continue only to resolve a named gap within the original scope and limits, not to expand the investigation indefinitely. Escalate depth only for a materially harder question; omitting the processor silently selects `pro-fast`.

```bash
parallel-cli research run 'Follow-up resolving a remaining evidence gap' \
  --processor lite-fast --text --no-wait --json --previous-interaction-id INTERACTION_ID
```

Keep persistent memory/account management under `parallel-memory`; do not modify it as an incidental research step.

### Context.dev

`context-dev web answers --help` exposes `fast` and `ultra`; **ultra is the default**. When deeper investigation is warranted under the selection criteria above, specify the mode deliberately:

```bash
context-dev web answers --task 'Deep research question with source constraints' \
  --mode ultra --format json
```

Preflight task length against the current Answers contract; the observed validation limit is 2,000 characters. Shorten deliberately while retaining the questions and constraints. `--json-format` takes an example answer object, not JSON Schema.

For timeout recovery, inspect `context-dev logs list --help` and `context-dev logs retrieve --help`. Filter by endpoint and time, then retrieve the matching request to check its input, response, latency and credits used without rerunning it. Keep credentials and unrelated retained inputs out of output.

The [Answers contract](https://docs.context.dev/answers/overview) gives `ultra` a research budget of up to 50 seconds, not an unbounded deep-research run. [Timeout options](https://docs.context.dev/optimization/timeouts) can shorten but cannot extend that budget. Inspect `--timeout-opts` and the endpoint schema before use; supported partial results must remain labeled partial. For a broad task that exhausts the research budget, try a bounded focused subquestion on the same provider after checking prior status and cost, then cover and reconcile the remaining questions. Increasing the shell timeout alone is not a fix.

### Kagi Assistant

When selecting Kagi's research assistant under the same criteria, load the preserved `kagi-assistant` and `kagi-ai` skills for account-backed conversation mechanics and model/assistant selection. Verify current available assistants instead of assuming an assistant ID. Ordinary Quick Answer is not a substitute when the task requires sustained investigation.

## Deliver

Report the result location or run ID, evidence, limitations and unresolved contradictions. Do not present a provider-generated report unread or call it comprehensive without checking its coverage. No deep-research job was started during consolidation. Parallel live access was blocked by insufficient credit on 2026-10-28.
