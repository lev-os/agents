---
name: agent-field-kit
description: Portable coding-agent bootstrap bundle. Use when a local, remote, or containerized coding environment is missing the core CLI toolchain, PATH wiring, or niche operational skills like dcg, ntm, cass, ubs, defendr, and agentmail-cli.
---

# Agent Field Kit

Use this as the portable bootstrap layer for coding agents. It is intentionally independent from Leviathan runtime internals.

## When to Use This Skill

Trigger this skill when:
- a remote sandbox feels crippled compared to the local machine
- a fresh machine or container needs the agent toolchain installed
- you need to restore `PATH` helpers and shell integration quickly
- you need to know whether to use a baseline tool directly or load a niche leaf skill
- you want a clean Docker smoke test for the bundle

Do not use this skill for Leviathan-specific install/doctor/config work. That is a later layer.

## Quick Start

### Install the bundle

```bash
~/.agents/skills/agent-field-kit/scripts/install.sh --profile full --write-shell-rc
```

### Load the generated shell env immediately

```bash
source ~/.agent-field-kit/env.sh
```

### Run the Docker smoke test

```bash
~/.agents/skills/agent-field-kit/scripts/smoke-test.sh
```

## Routing Guide

### Baseline tools — use directly

For these tools, the model usually knows enough already. What matters is install status and the local opinionated use cases.

- `rg` / `ripgrep` — fast text search
- `fd` — fast file discovery
- `fzf` — interactive narrowing
- `tree` — structure snapshots
- `duckdb` — quick SQL over CSV/JSON/Parquet
- `git-delta` — readable diffs
- `xh` — readable HTTP requests
- `watchexec` — rerun on file changes
- `just` — project task runner
- `semgrep` — fast static analysis
- `gh` — GitHub CLI

Read [tool-bundle.md](references/tool-bundle.md) for install matrix and "when to use" notes.

### Niche tools — load leaf skills

Use these as focused skills instead of bloating this router:

- `dcg` → `~/.agents/skills/dcg/SKILL.md`
- `ntm` → `~/.agents/skills/ntm/SKILL.md`
- `cass` → `~/.agents/skills/cass/SKILL.md`
- `ubs` → `~/.agents/skills/ubs/SKILL.md`
- `defendr` → `~/.agents/skills/defendr/SKILL.md`
- `agentmail-cli` → `~/.agents/skills/agentmail-cli/SKILL.md`

## Golden Rules

1. Install the core toolchain first; don't route around missing binaries with weaker substitutes.
2. Keep baseline tool guidance short; load leaf skills only for niche workflows.
3. Treat Docker smoke tests as the truth surface for remote parity.
4. Prefer best-effort portability over perfect package-manager coverage in v1.

## Remote Access Playbook (from OpenClaw, Wave 6 — oc-04)

When the agent needs to reach a remote machine (air-gapped dev box, team server, cloud VM):

### Option 1: Tailscale (recommended for persistent sessions)

```bash
brew install tailscale
sudo tailscale up
# Assigns stable DNS: hostname.tailnet.name
ssh user@hostname.tailnet.name
```

Tailscale handles NAT traversal, MagicDNS, and auth without port forwarding setup.

### Option 2: Docker + SSH

```bash
docker run -d -p 2222:22 --name agent-box ubuntu:24.04
ssh -p 2222 user@localhost
```

Preferred for ephemeral sandboxes — disposable, reproducible, port-forwarded.

### Option 3: Trusted proxy gateway

```bash
curl -X POST http://gateway.local/register \
  -d '{"agent_id": "...", "capabilities": ["exec", "flow"]}'
```

Use when multiple agents share a managed gateway with unified auth.

Source: `.lev/pm/parity/openclaw.yaml`

## Files in This Skill

- `references/tool-bundle.md` — install matrix and per-tool usage guidance
- `scripts/install.sh` — portable installer
- `scripts/smoke-test.sh` — clean-room Docker validation
