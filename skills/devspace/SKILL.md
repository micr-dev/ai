---
name: devspace
description: Operate the Waishnav DevSpace local MCP server on this machine.
---

# DevSpace

## Local Setup

This machine has DevSpace installed and configured. Do not run `devspace init` or overwrite the configuration unless the user explicitly asks to reconfigure.

Expected configuration:
- CLI: global `devspace` command from `@waishnav/devspace`
- Config dir: `~/.devspace`
- Local MCP URL: `http://127.0.0.1:7676/mcp`

Do not treat DevSpace as an outbound consultation path from a local agent. A Codex session on this machine cannot use DevSpace to ask ChatGPT or GPT-5.5 Pro a question unless a separate outbound bridge is installed and verified.

## Verify The Install

```bash
command -v devspace
devspace doctor
devspace config get
```

## Start And Connect

```bash
devspace serve
```

When the client connects, DevSpace shows an Owner password approval page. The password is stored in `~/.devspace/auth.json`; do not print or paste it.

## Client Workflow

The MCP host should call `open_workspace` once for a project under an allowed root and reuse the returned `workspaceId` for later calls.

## Tool Surface

Default tool names: `open_workspace`, `read`, `write`, `edit`, `bash`. Default `DEVSPACE_TOOL_MODE=minimal` hides dedicated search/list tools.

## Security Rules

- Keep `DEVSPACE_ALLOWED_ROOTS` narrow
- Treat a connected MCP client as trusted local code execution
- Do not expose auth tokens, tunnel credentials, or secrets in chat, logs, or commits
