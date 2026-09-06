---
name: box-cli
description: Cloud Linux sandboxes via Box CLI (`box`). Run remote tests, builds, compiles, or untrusted code in disposable or persistent VMs, manage sandbox lifecycle, and inspect quota.
---

# Box CLI

A box is a persistent Ubuntu VM rented by the second while running. Stopped boxes are free.

The primary personal use is testing, compiling, and running isolated builds. Because Box has **no idle timer**, unstopped boxes burn quota continuously until their TTL expires. Every run must treat stopping the machine as a mandatory completion step.

Read `box <command> --help` for flag syntax.

## Pre-flight: Check Quota

Before starting work, check that machine time and starts remain:

```bash
box limits          # compute seconds remaining, starts budget, and active boxes
box status          # API health and signed-in account
```

If compute time is 0s or status is depleted, stop immediately and report to the user. Do not attempt `box new` or `box resume`.

If `box: command not found`, install via `curl -fsSL https://box.ascii.dev/install | sh`. If signed out, stop and ask the user to authenticate; non-interactive `box login` without a key hangs waiting for a browser. Headless sessions use `box login "$BOX_API_KEY"`.

## The Test & Compile Loop

Follow this four-step sequence for every remote execution:

```bash
# 1. Allocate a small box with a tight deadman TTL (e.g. 5-10 minutes)
box new --type small --ttl 300

# 2. Run the test or compile command over the API
box exec current --timeout 240 "npm test"

# 3. Pull output artifacts if needed (skip if stdout is sufficient)
box scp current:/home/user/dist ./dist

# 4. Mandatory completion: STOP immediately to halt billing
box stop current
```

**Completion criterion**: Remote execution is not done until `box stop` (or `box delete`) succeeds. If the remote command fails or errors out, still stop the box immediately.

## Quota & Sizing Rules

1. **Default to `small` for tests and compiles**
   - `--type small` (2 vCPU, 4 GB): **0.5x burn rate** ($0.018/h, ~1,110 hours per $20 plan). This handles standard test suites, linters, typechecks, and package builds.
   - `--type default` (4 vCPU, 8 GB): **1x burn rate** ($0.036/h, ~555 hours per $20 plan). Use only when memory or thread limits exceed 4 GB (e.g. large Docker-in-Docker or heavier services).
   - `--type large` (8 vCPU, 16 GB): **2x burn rate** ($0.072/h). Use only for heavily parallel C++/Rust workspace compilations.
   - Omitting `--type` defaults to `default`, burning quota twice as fast as `small`.

2. **TTL is a deadman switch, not an idle timer**
   - The meter runs every second a box is in `ready`, `cloning`, `running`, or `idle`.
   - Never run `box new` without `--ttl`. Default TTL is 3600 (1 hour); leaving it burns 50+ idle minutes if a stop is missed.
   - Set `--ttl` to estimated runtime plus a small buffer (e.g. `--ttl 300` for 5m, `--ttl 600` for 10m).
   - Never use `--no-auto-stop` for routine tests or builds.

3. **Always pass `--ttl` when resuming**
   - `box resume <id>` without `--ttl` preserves the box's previous TTL setting or disabled auto-stop. Always supply an explicit timer: `box resume <id> --ttl 300`.

4. **Budget machine starts**
   - `new`, `resume`, and `fork` each consume 1 start against rolling account caps (10/min, 50/hour, 150/day).
   - Group multiple test commands into a single box session rather than creating a new box for every command.

5. **Choose Stop vs Delete**
   - `box stop <id>`: Pauses billing and saves the filesystem snapshot for free. Use this for reusable test runners where installed dependencies should be preserved.
   - `box delete <id> --yes`: Permanently tears down the VM and its snapshot chain. Use this for one-off throwaway runs to avoid cluttered inventories.

## Leverage: The Warmed Test Runner

Cold builds spend billable box seconds cloning repos and installing dependencies. Build a reusable warm box once and resume it for subsequent runs:

```bash
# Setup phase (run once)
box new --type small --ttl 600
box exec current "git clone <repo> && cd <repo> && npm install"
box stop current                         # disk snapshotted for free

# Recurring test phase (sub-second launch, cached node_modules/cargo)
box resume <id> --ttl 300
box exec <id> "cd <repo> && git pull && npm test"
box stop <id>                            # billing halts immediately
```

To deploy identical runners concurrently, snapshot the setup:
```bash
box snapshot <id> test-runner            # freeze template (up to 10 kept)
box new --from test-runner --type small --ttl 300
```

## Running Long Builds (>600s)

Synchronous `box exec` caps at 600 seconds. For longer compilations, detach and poll:

```bash
pid="$(box exec current --detach "cargo build --release" | jq -r .processId)"
box exec current --status "$pid"         # poll until exitCode appears
box stop current                         # stop once done
```

Detached logs stay at `~/.ascii/processes/<pid>.log` on the box.

## Common Traps

| Trap | Root Cause | Solution |
| --- | --- | --- |
| Quota drained with no work running | Box was left in `idle` or auto-stop was omitted. | Always pass tight `--ttl` (300-600s) and stop immediately after work. |
| Resumed box stayed up indefinitely | `box resume` without `--ttl` inherits old lifetime. | Always pass `box resume <id> --ttl <secs>`. |
| Tests burned quota at 1x or 2x rate | Default size is `default` (4 vCPU / 8 GB). | Explicitly pass `--type small` (0.5x burn rate). |
| Start limit 429 `rate_limited` | Exceeded 10 starts/min or 50/hour. | Run multiple test steps in one session instead of spinning up a box per step. |
| Test server unreachable on hosted URL | Service bound only to `127.0.0.1`. | App must bind `0.0.0.0` when exposing ports via `box host <id> <port>`. |
| Interactive command hangs indefinitely | `box login` with no key waits for browser. | Check `box status` first; use `box login "$BOX_API_KEY"` headlessly. |
| Stop refused and box left running | Disk snapshot in progress or failing. | The billing meter pauses on failed stop. Poll `box info` for `stopped`, or use `--force` if unsaved scratch data can be discarded. |

## Automation & Scripting

For shell automation, CI scripts, and error code reference, see [`references/automation.md`](references/automation.md).
