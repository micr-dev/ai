---
name: compact-handoff
description: Use before manual or automatic context compaction, when the user asks for precompact/pre-compact handling, or immediately after compaction/resume to preserve and reload durable session context. Creates and reads compact handoff markdown files under ~/.codex/compact-handoffs so a post-compact agent can continue without relying only on the model-generated compact summary.
---

# Compact Handoff

Use this skill for context compaction handoffs.

## Create Before Compacting

1. Create a durable handoff file under `~/.codex/compact-handoffs/` with a kebab-case timestamped name:

   ```bash
   mkdir -p ~/.codex/compact-handoffs
   handoff="$(mktemp ~/.codex/compact-handoffs/$(date -u +%Y-%m-%dT%H-%M-%SZ)-handoff-XXXXXX.md)"
   sed -n '1,20p' "$handoff"
   ```

2. Fill the file with concise resume context. Do not duplicate large artifacts that already exist elsewhere. Reference paths, issue URLs, PR URLs, commits, and docs instead.

3. Include these sections:
   - `# Compact Handoff: <task>`
   - `## Current State`
   - `## Decisions and Assumptions`
   - `## Files and Artifacts`
   - `## Verification`
   - `## Immediate Resume Instructions`
   - `## Open Risks`

4. Run a quick readback:

   ```bash
   sed -n '1,220p' "$handoff"
   ls -t ~/.codex/compact-handoffs/*.md | head -1
   ```

5. Tell the user the handoff path. After that, compaction can proceed. The `PreCompact` hook expects a recent markdown file in `~/.codex/compact-handoffs/`.

## Read After Compacting

1. Find the latest handoff:

   ```bash
   latest="$(ls -t ~/.codex/compact-handoffs/*.md 2>/dev/null | head -1)"
   printf '%s\n' "$latest"
   ```

2. Read it completely before any implementation or destructive command:

   ```bash
   sed -n '1,260p' "$latest"
   ```

3. Verify the live workspace state against the handoff:
   - `pwd`
   - `git status -s -u` when inside a git repo
   - any running dev server or workflow named in the handoff

4. Start from `Immediate Resume Instructions`. If the handoff conflicts with live files, trust live files and report the mismatch before editing.

## Content Rules

- Keep secrets out of handoffs. Mention env var names only, never values.
- Prefer exact file paths and command outcomes over broad prose.
- Keep the handoff short enough to read after compaction, usually 80-180 lines.
- If the task has an existing PRD, ADR, issue, PR, or docs artifact, link to it instead of copying it.
