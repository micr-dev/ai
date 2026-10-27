---
disable-model-invocation: true
name: ios-reflect
description: Mine an iOS app project's agent sessions and route durable lessons into the iOS app framework (AGENTS.md, development-docs/, checklists/). Use after a milestone, a release, an App Review outcome, or when the user says ios-reflect.
---

# ios-reflect

Turn one app's sessions into framework edits so the next app starts smarter. The framework repo is the single source of truth; the app repo only holds a copy.

Leading word: **lesson**. A lesson is a rule that changes what a future agent does on a *different* app. An incident ("the export screen broke after sign-out") is evidence; the lesson is the generalized guardrail ("sign-out invalidates in-flight work").

## 1. Locate inputs

- **Framework repo**: the directory holding `AGENTS.md`, `development-docs/`, `checklists/`. Ask once if it is not the current repo or a sibling; every edit lands there.
- **Transcripts**: the agent harness session directory for the app's working directory (omp: `~/.omp/agent/sessions/-<cwd-with-dashes>/`; Cursor: the `agent-transcripts/` dir named in the system prompt). Include subagent transcripts. Stay inside this app's directory; other projects' sessions are private.
- **Since-marker**: read `development-docs/framework-log.md`. Mine only sessions newer than the last entry for this app, unless the user asks for a full pass.
- **App artifacts**: the app repo's `docs/`, `research/`, store metadata, ADRs, and App Review correspondence. These hold conclusions the transcripts only reach slowly.

Done when you can list every transcript file and artifact directory in scope.

## 2. Build digests

```bash
python3 <skill-dir>/scripts/build-digests.py <session-dir>... --out /tmp/ios-reflect-digests
```

Raw transcripts are mostly tool output. The digests keep user turns, assistant text, tool-call heads, tool errors, and compaction summaries, split into ~450 KB slices. Done when every slice file exists and the total count is known.

## 3. Mine in parallel

Spawn one read-only miner per slice plus one for app artifacts, all in one batch, using [`references/miner.md`](references/miner.md) verbatim with the slice path substituted. Each miner writes `findings-<slice>.md`. Done when every slice has a findings file; re-dispatch any slice that returned empty or partial.

## 4. Synthesize

Spawn one synthesizer with [`references/synthesizer.md`](references/synthesizer.md), passing the findings directory and framework root. It reads the current framework files and returns Accepted / Rejected / Backlog tables. Done when every finding is accounted for in one of the three.

## 5. Approve, then apply

Show the user the full tables and wait for approval; framework edits affect every future app. The user may pick a subset or reroute rows. Then apply each approved row to its routed file:

- New mistake: append to `development-docs/mistakes-ledger.md` with the next stable `M-NNN` ID.
- New or corrected rule: edit the owning topic doc in place; replace stale lines instead of layering exceptions.
- New owner prerequisite or release step: add a checkbox to the matching checklist with its proof.
- New topic with no home: add `development-docs/<kebab-name>.md` and a pointer line in `AGENTS.md`.
- Owner preference: `development-docs/agent-operating-manual.md`, or `AGENTS.md` if every task needs it.

Write per [`references/writing-rules.md`](references/writing-rules.md): positive guardrails, leading words, no app names, volatile facts marked "verify at use" with a primary-source URL.

## 6. Log and hand off

Append to `development-docs/framework-log.md`: date, app, sessions covered, rows applied, rows backlogged. Report changed files and dropped findings (one line each, with reason). Commit only when the user asks.
