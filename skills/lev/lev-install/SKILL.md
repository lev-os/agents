---
name: lev-install
description: |
  [WHAT] Legacy install/setup reference for Lev CLI.
  [HOW] Documents historical install paths and commands.
  [WHEN] Use only when explicitly troubleshooting installation behavior.
  [WHY] Active install guidance should live in `~/lev/docs` and runtime commands (`lev-core`).

  Triggers: "install lev", "lev install", "setup lev", "upgrade lev", "verify installation", "lev setup", "configure lev"
skill_type: reference
category: docs-legacy
status: deprecated

lifecycle_integration:
  stage: manifesting
  input_artifact: project to configure
  output_artifact: installed lev environment (.lev/ + ~/.config/lev/)
---

# Lev Install & Setup

> Deprecated as a primary skill. Prefer canonical docs in `~/lev/docs` plus `lev-core` runtime commands.

## Overview

Lev uses a fractal pattern with two installation locations:
- **Global:** `~/.config/lev` (user-level config, logs, state)
- **Local:** `./.lev` (project-level config and artifacts)

## Quick Start

```bash
# Install lev CLI globally
npm install -g @lev-os/lev
# or
pnpm add -g @lev-os/lev

# Initialize project
cd your-project
lev install

# Verify
lev --version
ls -la .lev/
ls -la ~/.config/lev/
```

## Install Commands

```bash
lev install                              # Create ~/.config/lev and .lev directories
lev upgrade                              # Force reinstall (alias for install --force)
lev install --force                      # Reinstall, overwrite existing
lev install --config ./path/to/config.yaml  # Use custom config
```

## What Gets Installed

| Path | Purpose |
|------|---------|
| `~/.config/lev/` | Global config, logs, state |
| `~/.config/lev/logs/` | Daemon log files |
| `~/.config/lev/daemons/` | pmdaemon process configs |
| `.lev/` | Project-local directory |
| `.lev/config.yaml` | Project configuration |

## Configuration

### Project Config (.lev/config.yaml)

```yaml
project:
  name: my-project

poly:
  daemons:
    - name: ck-lite
      autostart: true
      port: 18080
      env:
        LOG_LEVEL: debug

    - name: leann
      autostart: false
      healthcheck: /health

    - name: orchestrator
      autostart: false
```

### Common Daemons

| Daemon | Purpose | Default Port |
|--------|---------|--------------|
| `ck-lite` | Lightweight Claude kernel | 18080 |
| `leann` | Vector index server | 18081 |
| `orchestrator` | Multi-agent coordination | 18082 |

## Daemon Management

After installation, manage daemons with:

```bash
lev daemon list              # Show registered daemons
lev daemon start <name>      # Start a daemon
lev daemon stop <name>       # Stop a daemon
lev daemon restart <name>    # Restart a daemon
lev daemon logs <name>       # View daemon logs
lev daemon logs <name> --follow  # Tail logs
lev daemon status            # Health check all daemons
lev daemon start --autostart # Start all autostart daemons
lev daemon stop --all        # Stop all daemons
```

## Upgrading

```bash
# Upgrade lev CLI
npm update -g @lev-os/lev
# or
pnpm update -g @lev-os/lev

# Reinstall project artifacts
lev upgrade
# or
lev install --force
```

## Verify Installation

```bash
# Check CLI
lev --version

# Check directories
ls -la ~/.config/lev/
ls -la .lev/

# Check config
cat .lev/config.yaml

# Check daemons
lev daemon status

# Quick test
lev get "hello world"  # Should work if indexes exist
```

## Troubleshooting

### Installation Issues

| Issue | Solution |
|-------|----------|
| Permission denied on ~/.config/lev | `sudo chown -R $USER ~/.config/lev` |
| .lev not created | Run `lev install` from project root |
| Config not found | Check `.lev/config.yaml` exists |
| Command not found: lev | Ensure npm global bin is in PATH |

### Daemon Issues

| Issue | Solution |
|-------|----------|
| Daemons not starting | Check logs: `lev daemon logs <name>` |
| Port already in use | `lsof -i :<port>` then kill conflicting process |
| Health check failing | Verify endpoint: `curl localhost:<port>/health` |
| High memory usage | Restart: `lev daemon restart <name>` |

### Path Issues

```bash
# Find npm global bin
npm config get prefix

# Add to PATH (bash/zsh)
export PATH="$(npm config get prefix)/bin:$PATH"

# Verify
which lev
```

## Location Rules

The `.lev` location is **fixed** (fractal pattern):
- Global: `~/.config/lev` (cannot be moved)
- Local: `./.lev` (cannot be moved)

Artifact paths **within** `.lev` (indexes, bd, cache) can be configured in `config.yaml`.

## First-Time Setup Checklist

1. Install lev CLI globally
2. Run `lev install` in project root
3. Verify with `lev --version` and `ls .lev/`
4. Edit `.lev/config.yaml` for project-specific settings
5. Start daemons: `lev daemon start --autostart`
6. Test: `bd ready` to see available work

## Post-Install Commands

After successful installation:

```bash
bd ready              # See available work (if using beads)
lev get "query"      # Search codebase
lev daemon status     # Check daemon health
```

## Uninstall

```bash
# Remove project-local
rm -rf .lev/

# Remove global (careful - affects all projects)
rm -rf ~/.config/lev/

# Uninstall CLI
npm uninstall -g @lev-os/lev
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `lev install` | Initialize project |
| `lev upgrade` | Force reinstall |
| `lev daemon list` | Show daemons |
| `lev daemon start <n>` | Start daemon |
| `lev daemon status` | Health check |
| `lev --version` | Verify CLI |

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for lev-install, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
