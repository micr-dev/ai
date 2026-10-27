# Daily update contract

The host runs `scripts/daily-update.py` once daily through a persistent systemd timer. MicroClaw performs editorial edits in a task-specific host session; Python owns input capture, validation, Git publication and deployment verification. The site uses one deployment path: the existing Vercel Git integration.

## MicroClaw handoff

When the MCP inventory changes, the runner first creates a one-shot MicroClaw research task and requires a sourced description for every configured server. It redacts and scans the resulting evidence before passing it to a separate one-shot editorial task. Each task's preflight configures its model-request header and disables configured MCP startup for that session only. Agents may research public documentation or query configured MCP tool listings using existing credentials.

The owner chose MicroClaw's host runtime. It has the user's normal filesystem and network access; untrusted research material can therefore influence an agent with access to private files and credentials. Prompt restrictions, source hashes and publication checks do not create a filesystem sandbox.

Task completion alone is not proof of editorial success. The runner requires a report, checks the frozen input snapshot for changes, validates the candidate independently, and stops the task's own host session. An incomplete or timed-out run cannot publish. Each task uses a unique directory so abandoned work cannot affect a later run.

## Sources

OMP is the primary harness. Codex remains secondary. Read OMP's model roles and configured MCP names from its local configuration and the enabled Codex discovery source. OMP overrides take precedence, and disabled servers remain excluded. Configuration establishes names, not server capabilities or availability. Never export credentials, provider URLs, command arguments or environment values. OMP currently shares its skills directory and AGENTS.md with Codex; resolve those links rather than treating the directory name as the active harness. Capture all Markdown skill sources and the manual into a private run directory before editing. For skills already selected on the public site, also capture their supporting text scripts. Installed skills are candidates, not permission to publish private prompts. Preserve gated skills and intentional public selections.

Supported script extensions are `.py`, `.sh`, `.js`, `.mjs`, `.cjs`, `.ts` and `.ps1`; other supporting file types require operator review.

The `how` critique rubric was reviewed and approved for publication. Other private rubrics remain excluded unless separately approved.

Capture the curated `lsops --json` catalogue as names, descriptions, and optional why/when guidance only. Do not retain executable paths or help commands. The editor reconciles all CLI entries to those names and descriptions; validation independently rejects missing, extra, duplicate or stale entries, even if the report says the source was ignored.

Rank model usage from `https://tokens.micr.dev/api/v1/usage.json` using seven days of per-model total tokens across providers. Keep two models in each primary and secondary column. Normalize aliases before summing and exclude unattributed usage. A challenger moves above an incumbent only after leading it by at least 15% in two consecutive daily snapshots. Persist the snapshot only after deployment verification; reruns on the same day cannot advance the rule. If usage is unavailable, stale or incomplete, keep the existing model order and continue other updates. Usage ranking does not change OMP's configured default model.

On the first run only, when the API covers enough history and includes today, reconstruct yesterday's seven-day window from the current response. This initializes the stability check; it is not a previously recorded snapshot. If that history is unavailable, wait for a second verified daily observation.

For configured MCPs, collect nearby local package descriptions and README prose when available. For stdio servers, also request their tool descriptions without calling tools in a bounded, offline sandbox with no configured credentials or general access to the operator's home. JavaScript entrypoints may read their own installed package and runtime. A failed or unavailable probe provides no evidence; it does not establish that a server has no capabilities or that its configured runtime works. For user hooks and installed extensions, capture events, hashes and redacted code excerpts. The collector excludes paths, URLs, code fences and credential-labelled lines, and scans the extracted MCP and hook evidence for secrets before invoking the editor. The snapshot is private and the editor must treat it as untrusted data, not instructions. Redaction and secret scanning cannot guarantee that every secret or identifying detail is detected. Evidence can be incomplete or unavailable for remote servers. Names and hashes do not establish capabilities or availability. Do not publish source excerpts or configuration; retain only supported descriptions, and stop for operator review where evidence is insufficient. The collector does not inspect project-local hooks.

Codex hooks come from its `hooks/list` API, queried with a temporary writable Codex-home overlay, read-only host files and no network. Only enabled, trusted or managed hooks are inventoried; disabled and untrusted hooks are not treated as active. The collector retains redacted labels, event names, source excerpts and hashes, never commands or paths.

The collector also reads OMP's unexpired tool cache without starting servers. It accepts only entries whose normalized configuration hash matches and whose OMP version is supported by the collector (currently 18.12.0). Cache entries may be up to 30 days old and cannot prove the server's current availability or version. Unsupported OMP versions skip the cache until their normalization is verified; the offline probe remains available.

The pipeline reads the live host configuration directly. The independent CLI backup service remains unchanged. Each immutable private snapshot has a content digest. Compare against the last verified snapshot, not the newest visible changelog date. On first run, reconcile OMP, CLI, MCPs, hooks, the manual and differing published skill copies. Newly introduced source keys are also reconciled against an existing checkpoint. Record other installed skills as the initial baseline without changing the existing public selection. Record changes as first observed on the run date; never fabricate adoption dates or rewrite historical entries.

The snapshot is private and checked for mutation after editing. Pending publication resumes verification without creating another MicroClaw task.

## Transaction

1. Acquire a process lock. Resume verification of an already-pushed run before starting another.
2. Fetch the verified site origin and create a fresh isolated Jujutsu workspace. Never modify the operator's checkout.
3. Capture source files and write a private structured input manifest. MicroClaw may edit only `index.html`, `main.js`, `agents/AGENTS.md`, Markdown under `skills/`, and supporting scripts under `scripts/` within selected public skills. It must return a structured report covering each changed source.
4. Validate the report, changed paths, historical entries, skill links and public content. Run a secret scan. Reject incomplete reports, unplanned edits, symlinks, missing skill files and unexpected source-catalog loss.
5. Generate llms.txt and the OG image from the final site. Publish only after validation. Refuse a changed remote base rather than overwriting concurrent work.
6. Save the pending commit and expected public file hashes before pushing. A failed or interrupted deployment is retried by verifying that same commit, without repeating the editorial step.
7. Require a Ready Production deployment for the pushed commit in the configured Vercel project, the correct domain alias, and matching live bytes for every changed public artifact. Verify `index.html` at its canonical public URL `/`, because clean URLs redirect the file path. Only then advance the source checkpoint.

Deployment verification uses the existing Vercel CLI login. When its OAuth access token expires, the updater refreshes that login through Vercel's published OAuth endpoint and atomically updates the protected auth file. A failed refresh must leave the previous file intact. Avoid simultaneous Vercel login or refresh operations: the CLI does not share a lock with the updater. The updater checks for changes before replacing the file and retains the new credentials privately for recovery if it detects a conflict.

A successful unchanged-source check still verifies the deployed site and regenerates dated OG assets without calling the model. Failures exit nonzero and preserve the run directory. A separate hourly watchdog reports an unsuccessful latest run or more than 30 hours without a verified check. Notifications are deduplicated; notification failure must remain visible in the service log.

## Operations

Set `microclaw_group` in the private updater configuration to the group that performs the editorial task. Its host runner must support task-session provider headers and MCP opt-out.

Set `AI_SITE_USER_AGENT` in the private runtime environment; startup fails if it is missing. Do not publish its value.

Private settings, run evidence and checkpoints live outside the public repository. Keep credentials and run evidence out of the public repository. The runner requires Python 3.11+ with PyYAML and python-dotenv, bubblewrap, OMP, MicroClaw and its `ncl` CLI, lsops with a nonempty version 2 curated catalogue, Jujutsu, GitHub authentication, Node 24, ImageMagick 6, gitleaks and Vercel API authentication. Run `python3 scripts/test-daily-update.py` before installing changes. Use `daily-update.py prepare` to create and validate a candidate without publishing; `validate RUN_DIRECTORY` rechecks a repaired candidate; `publish RUN_DIRECTORY` publishes that reviewed candidate. `run` performs both, and `watchdog` checks freshness.

The superseded NanoClaw detection/apply/OG tasks remain paused for history. The old GitHub OG workflow, host redeploy script and placeholder sync script have been removed. See [the troubleshooting guide](daily-update-guide.md) for status checks and recovery.
