# Daily update contract

The host runs `scripts/daily-update.py` once daily through a persistent systemd timer. OMP CLI performs editorial edits; Python owns input capture, validation, Git publication and deployment verification. The site uses one deployment path: the existing Vercel Git integration.

## Sources

OMP is the primary harness. Codex remains secondary. Read OMP's model roles and active MCP names from its local configuration and the enabled Codex discovery source. OMP overrides take precedence, and disabled servers remain excluded. Never export credentials, provider URLs, command arguments or environment values. OMP currently shares its skills directory and AGENTS.md with Codex; resolve those links rather than treating the directory name as the active harness. Capture all Markdown skill sources and the manual into a private run directory before editing. Installed skills are candidates, not permission to publish private prompts. Preserve gated skills and intentional public selections.

The pipeline reads the live host configuration directly. The independent CLI backup service remains unchanged. Each immutable private snapshot has a content digest. Compare against the last verified snapshot, not the newest visible changelog date. On first run, reconcile OMP, the manual and differing published skill copies. Record other installed skills as the initial baseline without changing the existing public selection. Record changes as first observed on the run date; never fabricate adoption dates or rewrite historical entries.

The editorial process runs in a filesystem sandbox with the operator home hidden. It sees only its read-only source snapshot, candidate site, report directory and isolated runtime. OMP’s loopback credential broker uses the existing account store; the updater does not fork OAuth refresh credentials. The broker stops when the update service no longer needs it.

## Transaction

1. Acquire a process lock. Resume verification of an already-pushed run before starting another.
2. Fetch the verified site origin and create a fresh isolated Jujutsu workspace. Never modify the operator's checkout.
3. Capture source files and write a private structured input manifest. OMP may edit only `index.html`, `main.js`, `agents/AGENTS.md` and Markdown under `skills/`. It must return a structured report covering each changed source.
4. Validate the report, changed paths, historical entries, skill links and public content. Run a secret scan. Reject incomplete reports, unplanned edits, symlinks, missing skill files and unexpected source-catalog loss.
5. Generate llms.txt and the OG image from the final site. Publish only after validation. Refuse a changed remote base rather than overwriting concurrent work.
6. Save the pending commit and expected public file hashes before pushing. A failed or interrupted deployment is retried by verifying that same commit, without repeating the editorial step.
7. Require a Ready Production deployment for the pushed commit in the configured Vercel project, the correct domain alias, and matching live bytes for every changed public artifact. Verify `index.html` at its canonical public URL `/`, because clean URLs redirect the file path. Only then advance the source checkpoint.

A successful unchanged-source check still verifies the deployed site and regenerates dated OG assets without calling the model. Failures exit nonzero and preserve the run directory. A separate hourly watchdog reports an unsuccessful latest run or more than 30 hours without a verified check. Notifications are deduplicated; notification failure must remain visible in the service log.

## Operations

Private settings, run evidence and checkpoints live outside the public repository. Keep credentials and run evidence out of the public repository. The runner requires Python 3.11+ with PyYAML and python-dotenv, bubblewrap, OMP, Jujutsu, GitHub authentication, Node 24, ImageMagick 6, gitleaks and Vercel API authentication. Run `python3 scripts/test-daily-update.py` before installing changes. Use `daily-update.py prepare` to create and validate a candidate without publishing; `validate RUN_DIRECTORY` rechecks a repaired candidate; `publish RUN_DIRECTORY` publishes that reviewed candidate. `run` performs both, and `watchdog` checks freshness.

The superseded NanoClaw detection/apply/OG tasks remain paused for history. The old GitHub OG workflow, host redeploy script and placeholder sync script have been removed. See [the troubleshooting guide](daily-update-guide.md) for status checks and recovery.
