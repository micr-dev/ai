---
name: crabbox
description: "Run commands in disposable Docker containers on Oracle Paris via Crabbox. Use for isolated tests, builds, or agent workloads without touching the Ashburn host."
allowed-tools: Bash(crabbox:*), Bash(ssh:*), Bash(cat:*), Bash(ls:*), Bash(cd:*)
---

# Crabbox — Disposable Docker Containers on Paris

## What this is

Each `crabbox run` creates a fresh Docker container on the Paris VPS (oracle-paris, 100.96.124.15 via Tailscale), syncs your current working directory, runs the command, then destroys the container. Containers are isolated and disposable — no cleanup needed.

## Pre-installed toolchain (matches box.ascii.dev)

- **Node.js 22** + npm + corepack (pnpm/yarn)
- **Bun**
- **Rust** (stable, cargo)
- **GitHub CLI** (gh)
- **git, rsync, build-essential, pkg-config, libssl-dev, libffi-dev**

## Usage

### One-shot run (creates container, runs, destroys)

```sh
# Run tests (install deps first since node_modules isn't synced)
crabbox run -- sh -c 'npm install && npm test'

# Or just run a build
crabbox run -- npm run build

# Rust
crabbox run -- cargo test

# Any shell command
crabbox run -- bash -c 'rustc --version && cargo --version && bun --version'
```

### Warm box (reuse across multiple runs — avoids reinstalling deps)

```sh
# Start a warm box
crabbox warmup --slug my-task --ttl 30m

# Install deps once
crabbox run --id my-task -- npm install

# Run tests repeatedly without reinstalling
crabbox run --id my-task -- npm test

# SSH into it interactively
crabbox ssh --id my-task

# Stop and destroy
crabbox stop my-task
```

## Important notes

- **node_modules is NOT synced.** Install deps inside the container or use a warm box.
- **Each one-shot run gets a fresh container.** No state carries over.
- **Concurrent runs work.** Each gets a different port. Safe to run multiple simultaneously.
- **Working directory must be a git repo** for sync to work properly.
- **Cost**: free, runs on Oracle Cloud free tier.

## Diagnostics

```sh
crabbox doctor          # Check provider health
crabbox list            # List active boxes
crabbox cleanup         # Clean up stale containers
```
