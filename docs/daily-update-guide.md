# Daily updater guide

## How it works

`ai-site-sync.timer` runs at 09:30 Europe/Madrid and catches up after host downtime. It snapshots OMP settings, the curated lsops catalogue, redacted MCP, hook and extension evidence, and shared skills/manual. It asks MicroClaw to edit changed content, validates the candidate, then pushes through Vercel's Git integration. Unchanged sources skip the editor. Success requires the production commit and public file hashes to match. See [the contract](daily-update.md) for validation rules and inventory limits.

The service retries failures after 30 minutes, with at most three starts per day. The hourly watchdog reports failures or a checkpoint older than 30 hours to the configured Discord system channel. This host must be online; its watchdog cannot alert while the host is down.

The systemd timer remains the only publisher. Each changed run creates a one-shot MicroClaw editor task, and a separate MCP review task when the MCP inventory changes. Do not enable the old MicroClaw publishing tasks. `ncl tasks run` queues a real occurrence, including for paused tasks; it is not a dry run.

## Check status

Run these as the host account that owns the timers:

```sh
systemctl --user list-timers 'ai-site-sync*' --no-pager
systemctl --user show ai-site-sync.service -p ActiveState -p Result -p ExecMainStatus
journalctl --user -u ai-site-sync.service -u ai-site-sync-watchdog.service -n 100 --no-pager
cat ~/.local/state/ai-site-sync/status.json
```

An inactive oneshot service is normal after completion. Check `status.json` for `verified` and `checkpoint.json` for `verified_at`, `commit` and expected hashes. An empty journal alone does not prove success. Private evidence lives in `~/.local/state/ai-site-sync/runs/`: `input.json`, `microclaw-task.json`, `editorial/report.json` and `candidate.json`. Successful runs remove their temporary site. Never publish these snapshots or task details.

The private `source/cli.json`, `source/mcps.json` and `source/hooks.json` files record the next candidate's inventory and redacted evidence. CLI names and descriptions must exactly match the catalogue. MCP README or package evidence may be missing or describe an installation rather than a running server. An offline stdio probe can supply tool descriptions, but it does not use credentials or establish live availability. Hook and extension excerpts omit string literals and other potentially sensitive lines, so they can miss important conditions. Secret scanning and redaction are not guarantees. If evidence is insufficient, inspect its source privately and review the candidate and report. Never publish private paths, credentials or source excerpts. The collector does not inspect project-local hooks.

`source/models.json` records the selected order when the usage API is usable. `checkpoint.json` stores the two daily observations only after publication is verified. A log message saying model usage is unavailable means the model list stayed unchanged; inspect the API response and its freshness before the next run.

The private snapshot also includes supported scripts for skills already linked on the public site. Review each script for private content before publication. The candidate secret scan covers scripts, but it cannot guarantee that they contain no sensitive information.

## Fix a failed run

| Symptom | Action |
| --- | --- |
| MicroClaw task failure | Inspect `microclaw-task.json`, the task's session history and the runner log. Confirm the configured group and host runner are available. A completed task without a valid report is a failure. |
| Missing command, Python import or image font error | Check `~/.config/ai-site-sync/runtime.env`. Use the dedicated Python environment, Node 24 and system ImageMagick 6. |
| Missing report, invalid edit, secret scan or history check failure | Inspect the run's log, report and candidate diff. Fix the cause or review the candidate manually; do not weaken validation. |
| `STALE_TARGET` before publication | A newer commit reached main. Start a fresh run against that revision. |
| Deployment timeout or API error | Check the configured Vercel project, authentication, Git deployment and domain alias. Expired CLI OAuth logins refresh automatically; if refresh fails, sign in again. If the login changed during refresh, inspect the protected recovery file named in the error before changing either login. Retry the pending commit; do not deploy from the CLI. |
| Pending publication conflicts with newer main | Compare `pending.json` with remote history before acting. Preserve the pending evidence and last verified checkpoint. Reconcile the commits, then explicitly archive the obsolete pending record before preparing a new run. Never force-push or blindly delete it. |
| Watchdog delivery failure | Check its service log and the Discord credential/channel referenced by private `config.json`. |

After fixing the cause, retry through systemd so it supplies the updater environment:

```sh
systemctl --user reset-failed ai-site-sync.service
systemctl --user start --no-block ai-site-sync.service
```

This can publish. A `pending.json` resumes that same commit; otherwise the runner prepares a fresh candidate. Confirm a new verified checkpoint afterward. Do not edit the checkpoint to make a failure look successful.

For manual candidate repair, wait until the service is inactive and stop the daily timer. Load the installed environment with `set -a; . ~/.config/ai-site-sync/runtime.env; set +a`. Use `~/.local/lib/ai-site-sync/venv/bin/python ~/.local/lib/ai-site-sync/daily-update.py validate RUN_DIRECTORY`, inspect the result, then use `publish RUN_DIRECTORY`. These commands resume pending state if present, so resolve that first. Re-enable the timer with `systemctl --user enable --now ai-site-sync.timer` after recovery.

## Maintain the installation

The timer executes `~/.local/lib/ai-site-sync/daily-update.py`, not the repository copy. Private settings are in `~/.config/ai-site-sync/config.json`; dependencies are pinned in `scripts/daily-update-requirements.txt`. After testing a runner change with the dedicated Python environment and `scripts/test-daily-update.py`, install the reviewed script to that runtime path. For unit changes, copy `docs/ai-site-sync*.service` and `docs/ai-site-sync*.timer` to `~/.config/systemd/user/`, run `systemctl --user daemon-reload`, and restart changed timers. Verify their next run times.

The old NanoClaw tasks stay paused for history. Their scripts and the old GitHub OG workflow are retired; do not reactivate them. Keep the independent CLI backup service and the operator's dirty site checkout untouched.
