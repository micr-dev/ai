# GitHub research

Use repository discovery to find projects, exact code search to find implementations, and direct inspection for a known repository. Do not treat README marketing or stars as proof that an API behaves correctly.

```bash
gitquarry --host github.com search 'topic' --format json --progress off
gitquarry --host github.com search 'topic' --language rust --topic cli --limit 10 --format json --progress off
gitquarry --host github.com inspect OWNER/REPO --readme --format json --progress off
gh search code 'exact API symbol' --limit 20
```

Search both the specific API and its surrounding usage shape. Inspect credible matching files and their repository/version context before recommending a pattern. Cite repository URLs and file paths.

## Deliberate broader discovery

```bash
gitquarry --host github.com search 'topic' --mode discover \
  --depth balanced --rank quality --explain --format json --progress off
```

Use discover mode when native results leave a coverage gap or ranking/explanation is needed. Non-native ranks require `--mode discover`. Without an explicit rank, discover uses `blended`. `--readme` adds an evidence/enrichment pass; it is not free retrieval and should stay explicit. Activity ranking is useful when recency is the question, not proof of quality. Do not copy old benchmark latency claims into current recommendations.

Use structured filters for languages, topics, ownership, dates and repository properties. Avoid contradictory raw query qualifiers and structured flags. `--plan` prints the compiled search plan without contacting GitHub; use it to check complex filters.

For a known repository:

```bash
gitquarry tree OWNER/REPO
gitquarry code OWNER/REPO 'literal pattern'
```

Inspect each command's help before adding path/depth/reference/file-size options. Bound remote scans; do not fetch every file when a path or symbol identifies the needed source. Use raw source readers for exact bytes.

## Authentication and failures

Credentials are host-scoped. Confirm the host first, then `gitquarry auth status`, then command shape and option compatibility. Reuse saved authentication; do not print tokens or start login unless needed and authorized. Do not enable insecure credential storage as a convenience fix.

For the selected normalized host, credential precedence is `GITQUARRY_TOKEN_<NORMALIZED_HOST>` (for example `GITQUARRY_TOKEN_GITHUB_COM`), then global `GITQUARRY_TOKEN`, then saved secure credentials, then the explicitly enabled insecure-file fallback. A saved login does not override an environment token. When access fails, check which variable names are set without printing their values before replacing saved credentials. The insecure fallback requires `GITQUARRY_ALLOW_INSECURE_STORAGE=1`; leave it disabled rather than enabling it to bypass a storage failure.

`gitquarry config path` locates the active config; `gitquarry config show` reports effective non-secret configuration such as host and output defaults, not credential values. Treat private host names as sensitive. For tests or multi-host scripts, set `GITQUARRY_CONFIG_DIR` to a fresh temporary directory and use an explicit `--host`, so those runs do not change the normal config. This isolates config files, not environment tokens or the OS credential store; avoid login/logout against real accounts during isolated checks.

Use structured JSON/compact output for scripts and `--progress off` to keep progress out of parsed output. README inspection, broad candidate enrichment and code probing add requests; increase scope only when the question needs it.

Evidence: installed search/inspect help and live inspection of `Octen-Team/octen-mcp` on 2026-10-28. This reference incorporates the prior operator playbook's native/discover, host, filters, output and troubleshooting rules; the original is retained in the consolidation backup.
