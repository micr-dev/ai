---
name: "codebase-memory-mcp"
description: "Use codebase-memory-mcp for structural code intelligence through a local MCP knowledge graph: symbols, references, call chains, architecture, impact analysis, graph queries, and indexed code search."
---

# Codebase Memory MCP

Use `codebase-memory-mcp` first when code exploration needs structural answers: symbols, references, call chains, imports, dependents, architecture risk, cross-service routes, or git-diff impact. It builds a local SQLite-backed knowledge graph from tree-sitter parsing and Hybrid LSP semantic resolution.

Use direct file reads after the graph identifies the relevant files. Use `fff`, `rg`, or file discovery tools for exact text, non-code files, comments, generated output, or when indexing is unavailable or not worth it.

## Startup

Verify the binary exists:

```bash
command -v codebase-memory-mcp
codebase-memory-mcp --version
```

Check indexed projects:

```bash
codebase-memory-mcp cli list_projects
```

If the current repository is missing and structural queries will materially help, index it with an absolute path:

```bash
codebase-memory-mcp cli index_repository '{"repo_path": "/absolute/path/to/repo"}'
```

Do not stop after discovering that a real project is unindexed when graph answers would materially help. Either index it, or state why direct reads/search are the better path for this task.

## Query Selection

Projects and indexing:

- `list_projects` - List indexed projects and graph sizes.
- `index_repository` - Index a repository into the graph.
- `index_status` - Check indexing status for a repository.
- `delete_project` - Remove a project from the local graph store.

Search and snippets:

- `search_graph` - Find graph nodes by label, name pattern, file pattern, and degree filters.
- `search_code` - Grep-like text search within indexed project files.
- `get_code_snippet` - Read source for a function by qualified name. Use `search_graph` to discover names first.

Tracing and architecture:

- `trace_path` - Traverse inbound/outbound call paths for a function.
- `detect_changes` - Map git diff to affected symbols and risk.
- `get_architecture` - Summarize languages, packages, routes, hotspots, boundaries, layers, clusters, and ADRs.
- `get_graph_schema` - Show labels, edge types, counts, and property definitions.
- `query_graph` - Run read-only Cypher-like graph queries.
- `manage_adr` - Create, read, update, and delete architecture decision records.
- `ingest_traces` - Ingest runtime traces to validate HTTP call edges.

Every MCP tool can be invoked through the CLI:

```bash
codebase-memory-mcp cli search_graph '{"name_pattern": ".*Handler.*", "label": "Function"}'
codebase-memory-mcp cli trace_path '{"function_name": "Search", "direction": "both"}'
codebase-memory-mcp cli query_graph '{"query": "MATCH (f:Function) RETURN f.name LIMIT 5"}'
```

Use `--raw` when piping to `jq`:

```bash
codebase-memory-mcp cli --raw search_graph '{"label": "Function"}' | jq '.results[].name'
```

## Common Workflows

Find a symbol:

```bash
codebase-memory-mcp cli search_graph '{"name_pattern": ".*AuthService.*"}'
```

Check usage before editing:

```bash
codebase-memory-mcp cli trace_path '{"function_name": "AuthService", "direction": "both", "max_depth": 3}'
```

Understand a project:

```bash
codebase-memory-mcp cli get_graph_schema '{}'
codebase-memory-mcp cli get_architecture '{"repo_path": "/absolute/path/to/repo"}'
```

Assess uncommitted changes:

```bash
codebase-memory-mcp cli detect_changes '{"repo_path": "/absolute/path/to/repo"}'
```

## Codex Integration Notes

Codex is configured with the `codebase-memory-mcp` MCP server:

```toml
[mcp_servers.codebase-memory-mcp]
command = "/home/ubuntu/.local/bin/codebase-memory-mcp"
args = []
```

Use MCP tools when they are exposed in the current turn. Use CLI mode when the MCP tool is unavailable, exact shell output is easier to validate, or a command needs to be composed with local shell tools.

Do not enable `auto_index` or commit shared graph artifacts unless the user asks. Automatic indexing and `.codebase-memory/graph.db.zst` are useful project-level choices, not default session side effects.

## Hygiene

Local indexes live under `~/.cache/codebase-memory-mcp/`. Project graph artifacts may appear under `.codebase-memory/` when explicitly exported or when a project opts into shared graph snapshots.

Do not leave unrelated `.codebase-memory/`, `.gitattributes`, or generated graph artifacts in a user-facing diff unless the task is to set up codebase-memory-mcp or the user explicitly accepts that tooling state.
