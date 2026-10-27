# Scripting Boat

Everything the CLI prints for a human has a machine-readable twin. Reach for the CLI with
`--json` when a shell wrapper is the fastest path, and for the typed SDKs
(`@boatdev/sdk`, `boat-sdk`, base URL `https://boat.dev/api/v1`) when the
call site is a real service.

## Authenticate once per process

```bash
boat login "$BOAT_API_KEY" --json >/dev/null    # {"event":"login_complete",...}
```

Put it in the container entrypoint or start command, before the first Boat call. The key
comes from `boat api-key create <name> --json | jq -r .secret`, run from a **browser**
session; an API-key session can use Boat normally but cannot mint, rotate or revoke keys.
Store it as `BOAT_API_KEY` in the platform secret manager, never in an image or a Dockerfile.

## The output contract

`--json` enables itself whenever stdout is piped or redirected, so a script gets JSON
even without the flag. Two shapes:

**One object.** `config`, `list`, `info`, `limits`, `stop`, `resume`, `fork`,
`interrupt`, `host`, `desktop`, `api-key create|rotate|list|revoke`.

**JSON Lines, one object per line.** Each carries an `event` field.

| Command | Lines |
| --- | --- |
| `boat new --json` | `created`, zero or more `state`, then `ready` or `error` |
| `boat prompt ... --json` | `queued`, then `chat` lines until the prompt finishes |
| `boat events <id> --json` | `chat` lines, then exit |
| `boat events <id> --follow --json` | `chat` lines until interrupted |

`boat new` ready line:

```json
{"event":"ready","id":"bx_8pqt6dup","state":"ready","url":"https://example-boat.on.ascii.dev",
 "ip":"203.0.113.10","desktopUrl":"...","archiveAfter":"2026-05-28T17:00:33.162Z",
 "commands":{"ssh":"boat ssh bx_8pqt6dup","forward":"boat forward bx_8pqt6dup --remote 3000 --local 3000"}}
```

A `chat` line carries `final` (false for streaming partials) and
`data.type` of `prompt`, `response`, `usage_limit` or `git_checkpoint`. Tool traces live
under `data.data.tools`; keep the whole object if you need them. `boat events` returns only
the persisted subset, which is fewer lines than `boat prompt` streamed live.

## Errors

A failed command emits one final line on **stdout** and exits non-zero:

```ts
type CliErrorLine = {
  event: "error";
  error: string;    // human-readable, may have a dashboard URL with a token appended
  code?: string;    // backend code, present only for Boat API failures
  status?: number;  // HTTP status, same condition
}
```

Local failures (bad provider, unreachable host, SSH exit) carry no `code`/`status`.
Argument-parsing failures come from the CLI parser on **stderr** and may not be JSON at
all, so a wrapper that only reads stdout must still surface stderr on a non-zero exit.

Treat the error string as sensitive: for `billing_required`, `provider_not_configured`
and friends the CLI appends a dashboard URL carrying `boat_token`.

### Retry verdicts

| Code | Status | Verdict |
| --- | --- | --- |
| `boat_starting` | 409 | **Retry.** Boat still provisioning; poll `boat info` for `ready`. |
| `boat_restoring` | 409 | **Retry.** SSH/desktop asked for in the first seconds of a resume. |
| `boat_securing` | 409 | **Retry.** A `--no-env` conversion is scrubbing owner secrets. |
| `rate_limited` | 429 | **Back off.** `window` names which of minute/hour/day you hit; `starts` has remaining counts for all three. |
| `limit_reached` | 429 | **Back off.** Concurrent-boat cap; stop something first. |
| `5xx` | 5xx | **Retry idempotent calls with jitter.** Log `requestId`. |
| `unauthorized` | 401 | Fix the token. |
| `billing_required`, `boat_access_inactive` | 402 | Send the user to the returned `billingUrl`. |
| `team_member_cap_reached` | 402 | Owner raises the cap, or wait for the window to renew. |
| `trial_auto_stop_required` | 400 | Trial account: TTL <= 2h and auto-stop stays on. |
| `trial_machine_class_not_allowed` | 403 | Trial account: `large` needs a payment method. |
| `not_found` | 404 | Refresh local state; the boat or key is gone. |
| `provider_not_configured` | 409 | Configure the agent provider at the returned `setupUrl`. |
| `invalid_timeout` | 400 | `timeoutSeconds` must be an integer 1-600. |
| `invalid_path` | 400 | File paths must resolve under `<boat-home>` or `/tmp`. |
| `type_too_small` | 409 | Shrinking a boat that holds more data than the target size. Boat untouched. |

**Commands are never retried for you.** Running a command is not idempotent, so a
timeout or a dropped connection mid-call leaves the decision to you: the command may well
still be running on the boat.

## Idempotent create and fork

`POST /sandboxes` and `.../fork` provision a billable machine, so a lost response is
ambiguous. Send your own account-unique `Idempotency-Key` header (a UUID) and a retry
with the same account, key and body returns the original boat instead of a second one.

| Situation | Result |
| --- | --- |
| Retry after a lost 202 or a 5xx | Same boat, no second charge |
| Retry while the first is still creating | 409 `idempotency_in_progress`, retry shortly |
| Same key, different body | 409 `idempotency_key_reused` |
| Create that failed before the boat existed | Key auto-releases in about 2 minutes |

Keys are kept 24 hours and scoped per account. Both SDKs expose it on create and fork.

## Bash

```bash
set -euo pipefail
boat login "$BOAT_API_KEY" --json >/dev/null

boat_id=""
while IFS= read -r line; do
  case "$(jq -r '.event' <<<"$line")" in
    created) boat_id="$(jq -r '.id' <<<"$line")" ;;
    ready)   echo "ready: $boat_id $(jq -r '.ip // empty' <<<"$line")" ;;
    error)   printf '%s\n' "$line" >&2; exit 1 ;;
  esac
done < <(boat new --ttl 3600 --json)

boat exec "$boat_id" --cwd my-repo --timeout 600 "npm test"
boat stop "$boat_id" --json
```

Long jobs, past the 600s synchronous cap:

```bash
pid="$(boat exec "$boat_id" --detach "npm run build" | jq -r .processId)"
boat exec "$boat_id" --status "$pid"
```

The status payload is the command-status object -- `running`, `exitCode` once finished,
and a tail of stdout/stderr. Print one before writing a poll loop against those keys.

Status degrades to `lost` if the boat's agent restarts across a stop/resume, but the log
files stay on disk at `~/.ascii/processes/<pid>.log`. Detached processes do not survive a
stop, resume or fork; a systemd unit does.

## Node

```js
import { spawnSync, spawn } from "node:child_process";
import { createInterface } from "node:readline";

class BoatCliError extends Error {
  constructor(line, fallback) {
    super(line?.error || fallback);
    this.name = "BoatCliError";
    this.code = line?.code;
    this.status = line?.status;
  }
}

// The error line is always last on stdout, even for single-object commands.
function parseErrorLine(output) {
  const last = output.trim().split(/\r?\n/).filter(Boolean).at(-1);
  try { const p = JSON.parse(last); return p.event === "error" ? p : null; } catch { return null; }
}

function boatJson(args) {
  const r = spawnSync("boat", [...args, "--json"], { encoding: "utf8" });
  if (r.status !== 0) throw new BoatCliError(parseErrorLine(r.stdout), r.stderr);
  return JSON.parse(r.stdout);
}

async function* boatJsonLines(args) {
  const child = spawn("boat", [...args, "--json"]);
  let lastError = null;
  for await (const line of createInterface({ input: child.stdout })) {
    if (!line.trim()) continue;
    const parsed = JSON.parse(line);
    if (parsed.event === "error") lastError = parsed;
    yield parsed;
  }
  const code = await new Promise((res) => child.on("close", res));
  if (code !== 0) throw new BoatCliError(lastError, `boat ${args.join(" ")} exited with ${code}`);
}
```

The Python equivalent is the same two helpers over `subprocess.run` and
`subprocess.Popen`; see https://docs.boat.dev/boat/use-in-code.md.

## Docker

Install the CLI at build time, authenticate at runtime:

```dockerfile
RUN set -eux; \
    case "$(uname -m)" in \
      x86_64|amd64) a="x64" ;; arm64|aarch64) a="arm64" ;; \
      *) echo "unsupported arch" >&2; exit 1 ;; esac; \
    curl -fsSL "https://ascii.dev/api/boat/cli/download?platform=linux-${a}&channel=ascii-prod" \
      -o /usr/local/bin/boat; \
    chmod +x /usr/local/bin/boat; \
    mkdir -p /root/.config/ascii/boat; \
    printf '{"api_url":"https://ascii.dev","channel":"ascii-prod"}\n' \
      > /root/.config/ascii/boat/config.json
```

Needs `ca-certificates`, `curl` and `openssh-client` in the image. Entrypoint runs
`boat login "$BOAT_API_KEY" --json` before anything else.

## Types worth knowing

```ts
type Boat = {
  id: string;                    // bx_...
  name: string;
  state: "init" | "provisioning" | "cloning" | "ready" | "idle" | "running"
       | "stopping" | "stopped" | "error" | string;
  url: string | null;            // public HTTPS URL for services
  ip: string | null;             // direct SSH IPv4
  desktopAvailable: boolean;
  desktopUrl: string | null;     // secret-bearing
  snapshotAvailable: boolean;
  snapshotCompletedAt: string | null;
  createdAt: string | null;
  updatedAt: string | null;
  archiveAfter: string | null;   // null means no automatic stop
  self?: boolean;                // only from `boat list --json`
}
```

The CLI renames three backend states for humans: `provisioned` -> `ready`,
`archiving` -> `stopping`, `archived` -> `stopped`. The API still uses the originals.

`boat list --json` defaults to up/running only, same as `--filter r`. Filter letters:
`r` running, `s` stopped, `p` pending, `t` stopping, `e` error; combine them
(`--filter sr`) or pass `--all`.
