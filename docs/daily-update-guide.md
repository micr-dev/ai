# Daily updater guide

## How it works

`ai-site-sync.timer` runs at 09:30 Europe/Madrid and catches up after host downtime. It snapshots OMP settings and shared skills/manual, asks sandboxed OMP to edit changed content, validates the candidate, then pushes through Vercel's Git integration. Unchanged sources skip OMP. Success requires the production commit and public file hashes to match. See [the contract](daily-update.md) for validation rules.

The service retries failures after 30 minutes, with at most three starts per day. The hourly watchdog reports failures or a checkpoint older than 30 hours to the configured Discord system channel. This host must be online; its watchdog cannot alert while the host is down.

## Check status

Run these as the host account that owns the timers:

```sh
systemctl --user list-timers 'ai-site-sync*' --no-pager
systemctl --user show ai-site-sync.service -p ActiveState -p Result -p ExecMainStatus
journalctl --user -u ai-site-sync.service -u ai-site-sync-auth.service -u ai-site-sync-watchdog.service -n 100 --no-pager
cat ~/.local/state/ai-site-sync/status.json
```

An inactive oneshot service is normal after completion. Check `status.json` for `verified` and `checkpoint.json` for `verified_at`, `commit` and expected hashes. An empty journal alone does not prove success. Private evidence lives in `~/.local/state/ai-site-sync/runs/`: `input.json`, `omp.log` when OMP ran, `editorial/report.json` and `candidate.json`. Successful runs remove their temporary site and OMP runtime. Never publish these snapshots or logs.

## Fix a failed run

| Symptom | Action |
| --- | --- |
| OMP authentication failure | Check the auth service log and repair the existing OMP account login. The broker shares that account store; do not copy credential databases into runs. |
| Missing command, Python import or image font error | Check `~/.config/ai-site-sync/runtime.env`. Use the dedicated Python environment, Node 24 and system ImageMagick 6. |
| Missing report, invalid edit, secret scan or history check failure | Inspect the run's log, report and candidate diff. Fix the cause or review the candidate manually; do not weaken validation. |
| `STALE_TARGET` before publication | A newer commit reached main. Start a fresh run against that revision. |
| Deployment timeout or API error | Check the configured Vercel project, authentication, Git deployment and domain alias. Retry the pending commit; do not deploy from the CLI. |
| Pending publication conflicts with newer main | Compare `pending.json` with remote history before acting. Preserve the pending evidence and last verified checkpoint. Reconcile the commits, then explicitly archive the obsolete pending record before preparing a new run. Never force-push or blindly delete it. |
| Watchdog delivery failure | Check its service log and the Discord credential/channel referenced by private `config.json`. |

After fixing the cause, retry through systemd so it supplies the environment and credential broker:

```sh
systemctl --user reset-failed ai-site-sync.service
systemctl --user start --no-block ai-site-sync.service
```

This can publish. A `pending.json` resumes that same commit; otherwise the runner prepares a fresh candidate. Confirm a new verified checkpoint afterward. Do not edit the checkpoint to make a failure look successful.

For manual candidate repair, wait until the service is inactive and stop the daily timer. Load the installed environment with `set -a; . ~/.config/ai-site-sync/runtime.env; set +a`. Use `~/.local/lib/ai-site-sync/venv/bin/python ~/.local/lib/ai-site-sync/daily-update.py validate RUN_DIRECTORY`, inspect the result, then use `publish RUN_DIRECTORY`. These commands resume pending state if present, so resolve that first. Re-enable the timer with `systemctl --user enable --now ai-site-sync.timer` after recovery.

## Maintain the installation

The timer executes `~/.local/lib/ai-site-sync/daily-update.py`, not the repository copy. Private settings are in `~/.config/ai-site-sync/config.json`; dependencies are pinned in `scripts/daily-update-requirements.txt`. After testing a runner change with the dedicated Python environment and `scripts/test-daily-update.py`, install the reviewed script to that runtime path. For unit changes, copy `docs/ai-site-sync*.service` and `docs/ai-site-sync*.timer` to `~/.config/systemd/user/`, run `systemctl --user daemon-reload`, and restart changed timers. Verify their next run times.

The old NanoClaw tasks stay paused for history. Their scripts and the old GitHub OG workflow are retired; do not reactivate them. Keep the independent CLI backup service and the operator's dirty site checkout untouched.
