---
name: create-cli
description: "Design or implement a CLI: command surface, args, prompts, help, output, errors, config, packaging, and releases."
---

# Create CLI

Design CLI surface area (syntax + behavior), human-first, script-friendly.

## Do This First

- Read `references/cli-guidelines.md` and apply it as the default rubric.
- Upstream/full guidelines: https://clig.dev/ (propose changes: https://github.com/cli-guidelines/cli-guidelines)
- Ask only the minimum clarifying questions needed to lock the interface.

## Clarify (fast)

Ask, then proceed with best-guess defaults if user is unsure:

- Command name + one-sentence purpose.
- Primary user: humans, scripts, or both.
- Input sources: args vs stdin; files vs URLs; secrets (never via flags).
- Output contract: human text, `--json`, `--plain`, exit codes.
- Interactivity: prompts allowed? need `--no-input`? confirmations for destructive ops?
- Config model: flags/env/config-file; precedence; XDG vs repo-local.
- Platform/runtime constraints: macOS/Linux/Windows; single binary vs runtime.

## Suggested Implementation Stack

Use this stack only when the user asks for a recommendation or explicitly selects it. Otherwise follow the repository's established language, runtime, tools, package manager, and test runner.

1. Write the command contract and tests before implementation. Cover parsing, exit codes, stdout/stderr, non-interactive behavior, and destructive-operation safety. This step is complete when the tests express every observable behavior being added.
2. Implement command parsing, subcommands, validation, help, and version output with `gunshi`. Keep command handlers thin enough that behavior can be tested without spawning a process; add process-level tests for the executable contract.
3. Use `@clack/prompts` only for the interactive path. Gate prompts on TTY availability, make `--no-input` fail with an actionable error when required input is missing, and keep prompts/progress off machine-readable stdout. This step is complete when every prompt has a flag, argument, config, or safe default for automation.
4. Build with `tsdown`. Point `package.json#bin` at the built executable, preserve the Node shebang and executable contract, and keep source maps enabled for debug output. This step is complete when the packed package contains only the intended runtime files and its binary runs outside the source tree.
5. Configure `lefthook` to run the repository's fast formatting, linting, typecheck, and test commands at the appropriate Git hooks. Reuse package scripts rather than duplicating shell pipelines in hook config.
6. Use `@varlock/bumpy` for bump files, changelogs, versioning, and publishing. Initialize with `bumpy init`, add release intent with `bumpy add`, inspect it with `bumpy status`, and use `bumpy ci setup` when GitHub release automation is requested. This step is complete when release intent is reviewable in the repository and CI owns the canonical publish path.
7. For a new npm package, offer `fledgling` as a one-time bootstrap before the first real release. Run its dry-run first, then use it to claim the package name and configure npm trusted publishing for the exact CI workflow and optional protected environment. Do not keep an npm publish token in CI once OIDC works. This step is complete when the package exists on npm and its trusted-publisher settings match the release workflow.

Do not add Fledgling to the routine release path. Re-run `fledgling sync` only when packages or trusted-publisher settings change; Bumpy owns normal releases.

## Deliverables (what to output)

When designing a CLI, produce a compact spec the user can implement:

- Command tree + USAGE synopsis.
- Args/flags table (types, defaults, required/optional, examples).
- Subcommand semantics (what each does; idempotence; state changes).
- Output rules: stdout vs stderr; TTY detection; `--json`/`--plain`; `--quiet`/`--verbose`.
- Error + exit code map (top failure modes).
- Safety rules: `--dry-run`, confirmations, `--force`, `--no-input`.
- Config/env rules + precedence (flags > env > project config > user config > system).
- Shell completion story (if relevant): install/discoverability; generation command or bundled scripts.
- 5–10 example invocations (common flows; include piped/stdin examples).

## Default Conventions (unless user says otherwise)

- `-h/--help` always shows help and ignores other args.
- `--version` prints version to stdout.
- Primary data to stdout; diagnostics/errors to stderr.
- Add `--json` for machine output; consider `--plain` for stable line-based text.
- Prompts only when stdin is a TTY; `--no-input` disables prompts.
- Destructive operations: interactive confirmation + non-interactive requires `--force` or explicit `--confirm=...`.
- Respect `NO_COLOR`, `TERM=dumb`; provide `--no-color`.
- Handle Ctrl-C: exit fast; bounded cleanup; be crash-only when possible.

## Templates (copy into your answer)

### CLI spec skeleton

Fill these sections, drop anything irrelevant:

1. **Name**: `mycmd`
2. **One-liner**: `...`
3. **USAGE**:
   - `mycmd [global flags] <subcommand> [args]`
4. **Subcommands**:
   - `mycmd init ...`
   - `mycmd run ...`
5. **Global flags**:
   - `-h, --help`
   - `--version`
   - `-q, --quiet` / `-v, --verbose` (define exactly)
   - `--json` / `--plain` (if applicable)
6. **I/O contract**:
   - stdout:
   - stderr:
7. **Exit codes**:
   - `0` success
   - `1` generic failure
   - `2` invalid usage (parse/validation)
   - (add command-specific codes only when actually useful)
8. **Env/config**:
   - env vars:
   - config file path + precedence:
9. **Examples**:
   - …

## Notes

- Keep design and implementation requests language-agnostic unless the user selects a stack or the repository already establishes one.
- If the request is “design parameters”, do not drift into implementation.
