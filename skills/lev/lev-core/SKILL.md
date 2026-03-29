---
name: lev-core
description: |
  [WHAT] CLI operations reference for lev runtime management.
  [HOW] Routes to daemon/debug/reference commands and links canonical docs.
  [WHEN] Use for daemon status, runtime checks, and operational troubleshooting.
  [WHY] Keeps runtime ops discoverable while lifecycle/process behavior stays in `work`.

  Triggers: "install lev", "lev daemon", "lev status", "manage daemons", "lev architecture", "debug lev", "lev setup"
skill_type: how-to
category: cli-ops

lifecycle_integration:
  stage: all stages (orchestration)
  input_artifact: lev operation request (install/daemon/debug)
  output_artifact: lev environment state + logs
---

# Lev Core Wizard

Master orchestration for the Leviathan development environment.

## Five-Fold Understanding

Before we begin, let me understand your quest:

1. **Evolution** - Fresh install or existing lev setup?
2. **Impact** - What are you trying to achieve? (dev environment, daemon management, debugging)
3. **Relationships** - Which project? (leviathan monorepo, external project, global setup)
4. **Essence** - The ONE thing blocking you right now?
5. **Paradigm** - Are you fighting lev or working with it?

## Choose Your Path

**What do you need help with?**

1. **Install & Setup (Legacy)** - Historical setup/upgrade guidance
   → Load: `references/install.md`

2. **Daemon Management** - Start, stop, monitor poly daemons
   → Load: `references/daemon.md`

3. **Debugging** - Something broken? Troubleshoot common issues
   → Load: `references/debug.md`

4. **Quick Reference** - Just need a command?
   → See Quick Commands below

5. **Something else?** - Tell me your quest

## Quick Commands

| Command | Description |
|---------|-------------|
| `lev install` | Legacy install path (prefer docs + runtime checks) |
| `lev status` | Show current system status |
| `lev get <query>` | Semantic search across codebase |
| `lev check --log="msg"` | Log progress checkpoint (lifecycle hook) |
| `lev events tail` | Tail lifecycle events |
| `lev events query --type=X` | Query events by type |
| `lev events stats` | Event statistics |
| `lev daemon list` | Show all registered daemons |
| `lev daemon start <name>` | Start a specific daemon |
| `lev daemon stop <name>` | Stop a specific daemon |
| `lev daemon logs <name>` | View daemon logs |
| `bd ready` | Show issues ready to work |
| `bd stats` | Project statistics |

## Architecture Overview

> For full architecture details, run these bash commands against ~/lev or see:
> `~/.agents/skills/lev/references/architecture-primer.md`

```
~/.config/lev/              # Global (user-level, XDG-compliant)
├── config.yaml             # Global settings
├── profiles/               # Exec profiles (planned)
└── runners/                # Runner protocol manifests (planned)

.lev/                       # Local (project-level)
├── config.yaml             # Project configuration (fractal: inline key → domain file → domain folder glob)
├── config/{domain}.yaml    # Per-domain config files
├── exec-profiles/          # Project exec profiles
└── pm/                     # Project management (handoffs, plans, intake)

core/                       # 20 modules (real layout)
├── domain/                 # Shared contracts: ProtocolAdapter, ExecTransport, Route, Target, Action
├── poly/                   # Protocol projector: registry.yaml, 5 surfaces (CLI/MCP/HTTP/gRPC/WS), codegen
├── exec/                   # Thin execution engine: createExec(dispatch), CLIAdapter, MCPAdapter
├── harness/                # Heavy runtime: TmuxHarness, AdapterRegistry (6 adapters), profile-loader
├── orchestration/          # Dispatch: A2A dispatcher, loop, DAG, stage policies
├── flowmind/               # Flow compilation + session management
├── graph/                  # Graph runtime: types, views, adapters, compositor
├── index/                  # Semantic search indexes
├── config/                 # Fractal config resolution
└── ...                     # + event-bus, event-machines, plugin-manager, etc.
```

## Key Patterns

- **ProtocolAdapter<TExternal, TInternal>** — pure-function transforms between API conventions (domain)
- **ExecTransport** — domain defines interface, poly implements at boot (DI pattern)
- **Route.parse('lev://module/fractal/item')** — URI routing for everything (domain)
- **A2A Job Dispatcher** — AgentJob → JobExecutor → AgentJobResult (orchestration)
- **TmuxHarness** — owned spawn primitive: spawn/send/capture/kill on lev-<id> sessions (harness)
- **Fractal Config** — inline key → domain file → domain folder glob (NOT single config.yaml)
- **DNA Contracts** — 3 .dna.yaml files, 25+ constraints, gate vs aspirational enforcement

## Protocols

| Protocol | Purpose | Example |
|----------|---------|---------|
| `lev://` | Internal routing | `lev://poly/runners/claude` |
| `bin://` | Binary handler dispatch | `bin://ck` |
| `grpc://` | gRPC service dispatch | `grpc://leann:50052` |
| `http://` | HTTP handler dispatch | `http://deer-flow:8001` |
| `skill://` | Load agent skills | `skill://lev-core` |
| `bd://` | Query beads issues | `bd://lev-001b` |

## External Tools (NOT our code)

- **ntm** — External Go tool for tmux agent spawning. We own TmuxHarness instead.
- **bd/beads** — Issue tracking (Rust CLI)
- **ck** — Code knowledge search (Rust CLI)

## Related Skills

- `bd` - Issue tracking with dependency graphs
- `lev-builder` - Module placement decisions
- `lev-cdo` - Architecture-aware deliberation
- `lev get` - Semantic search across codebase (`lev-find` backend, legacy name)
- `lev-index` - Vector index management
- `lev-learn` - Event analysis and system improvement
- `lev-align` - Drift detection and remediation

## Phase Navigation

Each reference follows the wizard pattern:
- 1-5 options presented based on context
- Combined choices welcome ("1,3")
- Pivot anytime ("actually, let's...")
- Back navigation available

When ready, tell me which path you'd like to take.

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
You are the prompt-architect-enhanced specialist for lev-core, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

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
