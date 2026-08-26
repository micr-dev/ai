---
name: box-cli
description: Use for `box` CLI commands and ascii.dev cloud sandboxes: when a task needs a machine that is not this one (untrusted or destructive code, a heavy build, a real browser or GUI session, parallel agents on isolated copies), when something needs a public HTTPS preview URL to share, when creating, snapshotting, forking or resuming a sandbox, or when scripting `box --json`.
---

# Box CLI

A box is a full Linux VM rented by the second: sudo, 2-8 vCPUs, a dedicated IPv4, a
streamed desktop, and a filesystem that survives being switched off. `box` drives it.

Read `box <command> --help` for the live flag surface, and fetch
https://docs.ascii.dev/llms.txt for pages this file does not cover. What follows is the
part `--help` never confesses: the semantics, the clocks, and the traps.

## Check the session first

```bash
box status          # API health, signed-in account, plan, config path
```

`box: command not found` -> `curl -fsSL https://box.ascii.dev/install | sh`
(Windows: `irm https://box.ascii.dev/install.ps1 | iex`).

Signed out -> **report it and stop**. `box login` with no key prints a URL, opens a
browser and blocks for up to six minutes, which strands a non-interactive session. The
user either signs in themselves or puts a key in `BOX_API_KEY`, after which
`box login "$BOX_API_KEY"` works headlessly. Keys are minted only from a browser session
(`box api-key create <name>`, secret shown once), so an API-key session cannot bootstrap
another one, and cannot rotate or revoke keys either.

## The loop

```bash
box new --ttl 3600                            # follows the box to `ready`, prints its id
box exec current "npm test"                   # runs it; exits with the remote exit code
box scp current:/home/user/out.zip ./out.zip  # pull results
box stop current                              # snapshot, then billing stops
```

`current` is the last box created in this shell and `self` is the box you are running
inside. Both work anywhere an id does, including inside a box.

**1. Get a box.** `box new` for a fresh one, `box new --from <name>` to deploy a
template you already built, `box resume <id>` to pick up a stopped one, `box fork <id>`
to branch a running one. `--type small|default|large` is 2/4/8 vCPUs.

**2. Wait for `ready`.** `box new` already follows the box there. `resume` and `fork`
answer asynchronously, so poll `box info <id>` until the state is `ready` or `idle`.
Commands sent earlier are refused with a retryable `box_starting`, and would run before
the box's environment variables were applied anyway.

**3. Run work.** `box exec <id> "cmd"` goes over the API with no SSH key setup and is
the default; add `--cwd <dir>` (relative to `/home/user`) and `--timeout <secs>`.
Reach for `box ssh` when you need an interactive shell or want to stream a local script
in without copying it first: `box ssh <id> -- bash -s < ./setup.sh`.

**4. Get results out.** `box scp` in either direction, `--recursive` for trees. To hand
a running service to a human instead, expose it (see below).

**5. Put it away.** `box stop <id>` snapshots the disk and pauses billing; a stopped box
is free and `box resume` brings it back months later. Reserve `box delete <id>` for data
you want destroyed: it force-stops without a final snapshot and permanently removes every
snapshot chain only that box uses.

## Clocks and money

* Auto-stop counts **from creation, not from last activity**. Default TTL is 1 hour, so a
  box dies mid-work an hour in unless you say otherwise. `box extend <id> --hours 12`,
  `--ttl 2592000` (30 days, the max), or `--no-auto-stop`.
* A fork does not inherit `--no-auto-stop`; it defaults back to 1 hour. Resume keeps the
  box's current setting when you omit `--ttl`.
* $1 buys about 27 hours of a `default` box. `small` burns the balance at 0.5x, `large`
  at 2x. Stopped boxes, snapshots, IPv4 and 2 TB/month egress cost nothing extra.
* Create, fork and resume each count as one **machine start** against per-minute,
  per-hour and per-day caps. `box limits` shows what is left of all three plus the
  balance. Past a cap the API answers 429 `rate_limited` and names the window.
* On the free trial `--no-auto-stop`, any TTL over 2 hours, and `--type large` are all
  refused. Two concurrent boxes, 25 hours of machine time total.

## Traps

