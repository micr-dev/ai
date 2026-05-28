# AI Agent Operating Manual (AGENTS.md)
*Version 4.2-Redacted* — *Authoritative System Instructions for ai.micr.dev*

> [!IMPORTANT]
> This document governs the behaviors, constraints, and execution protocols for all autonomous and semi-autonomous coding agents operating within the `micr` ecosystem. Sensitive environment configurations and internal API signatures have been redacted for public display.

---

## 1. Core Directives

### 1.1 Scope of Autonomy
- Agents are permitted to read and write files within the `/workspace` partition only.
- Direct outbound networking is restricted to approved APIs: `[REDACTED_API_URL]` and designated Model Context Protocol (MCP) bridges.
- All high-privilege system modifications must go through the manual approval hook `[REDACTED_HOOK_TOKEN]`.

### 1.2 Model Selection Hierarchy
1. **Primary Coding Engine**: `Claude 3.5 Sonnet (V2)` (via `[REDACTED]` endpoint)
   - *Use Case*: Complex structural changes, new feature creation, deep debugging.
2. **Secondary Support Engine**: `Gemini 1.5 Pro` (via `[REDACTED]` endpoint)
   - *Use Case*: Long-context analysis, repository-wide indexing, redundant code review.
3. **Image & Asset Generation**: `Flux.1 (Dev)` (hosted at `[REDACTED]`)
   - *Use Case*: High-fidelity asset generation, custom UI mockups.

---

## 2. Development Protocol

### 2.1 Workspace Integrity
- **Do No Harm**: Existing tests must never be bypassed. If code changes invalidate current assertions, the agent must propose a corresponding test update.
- **Dependency Cleanliness**: Avoid adding extraneous dependencies. Prefer vanilla/native browser APIs unless specifically instructed.
- **Linting & Formatting**: All modified JavaScript must comply with the `eslint-config-micr` rule set. CSS must align with the pure-variable architecture.

### 2.2 Styling Constraints
- Never inject inline styling unless doing dynamic, state-based layout calculations (e.g., hover tracking).
- Use global CSS design tokens defined in `index.css`.
- Avoid boxy containers, cards, and artificial panel divisions. The interface should read as clean text floating directly on the dark void.
- **Transitions**: Do not use opacity fades. Any dynamic element rendering or hover transition must be crisp, instant, or coordinate-based.

---

## 3. MCP Integration Protocols

Agents interact with the local operating system via the Model Context Protocol. The following bridges are active:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": ["/usr/local/bin/mcp-fs-bridge.js"],
      "env": {
        "ALLOWED_DIRS": ["/workspace"]
      }
    },
    "memory": {
      "command": "node",
      "args": ["/usr/local/bin/mcp-memory-bridge.js"],
      "env": {
        "DB_PATH": "/workspace/.residue/memory.db"
      }
    },
    "search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "████████████████████████████"
      }
    }
  }
}
```

---

## 4. Git & Changelog Automation

### 4.1 Commit Messages
All automated commits must be prefixed with `[agent]` followed by the primary module affected.
- *Example*: `[agent] workspace: update terminal config for tmux keybindings`

### 4.2 Changelog Updates
When a stack change is deployed, the agent must generate a **Change Entry** inside `CONTEXT.md` (or the corresponding DB schema). The entry must be date-grouped under `DD/MM/YYYY` and contain:
- Brief, bold update title.
- Optional secondary description of *why* the change was made, formatted as quiet secondary text without loud labels.
- References to affected stack entries.

---

## 5. Security & Isolation

- **API Keys**: No plaintext API keys may be written to disk. All credential calls must traverse the local environment resolver.
- **Logs**: Command execution logs must be written to `.residue/logs/` and rotated every 24 hours.
- **Process Spawning**: Any background process spawned by an agent must be registered in the system supervisor with a maximum lifetime of 600 seconds.

---

*End of Redacted Document. Full unredacted file is maintained under secure enclave `[REDACTED_ENCLAVE_ID]`. For access queries, contact security@micr.dev.*
