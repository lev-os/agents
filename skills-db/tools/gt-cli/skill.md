# Gas Town (gt CLI) Skill

## Overview

Gas Town is a multi-agent orchestration system for Claude Code that provides persistent work tracking via git-backed hooks. Scales to 20-30 agents by eliminating context loss during restarts.

## When to Use

- Multi-agent orchestration with work persistence
- GUPP (propulsion) pattern for autonomous execution
- Hook-based work assignment that survives restarts
- Convoy tracking for multi-issue work
- MEOW (Mayor-Enhanced Orchestration Workflow) patterns

## CLI Command Reference

### Workspace Setup

```bash
gt install <path>              # Initialize workspace
gt rig add <name> <repo>       # Add project container
gt rig list                    # List rigs
gt crew add <name> --rig <rig> # Create crew workspace
```

### Agent Operations

```bash
gt agents                      # List active agents
gt sling <issue> <rig>         # Assign work to agent (creates hook)
gt sling <issue> --agent cursor # Override agent runtime
gt mayor attach                # Start Mayor session
gt prime                       # Startup with hook check (outputs role context)
```

### Work Tracking

```bash
gt convoy create <name> [issues...] # Create convoy for tracking
gt convoy list                      # List convoys (dashboard)
gt convoy show [id]                 # Show convoy details
gt convoy status <id>               # Status of convoy
```

### Hooks & Persistence

```bash
gt hook                        # Show hooked work
gt hook <bead-id>              # Attach work to hook
gt hook <bead-id> -f           # Force replace existing
gt hook show <agent>           # Compact view of agent's hook
gt done                        # Signal work ready for merge
gt unsling                     # Remove work from hook
```

### Molecules & Formulas

```bash
gt formula list                # List available formulas
gt formula show <name>         # Show formula details
gt formula run <name>          # Execute formula

gt mol attach <bead> <mol>     # Pin molecule to bead
gt mol detach <bead>           # Unpin molecule
gt mol status                  # Current molecule status
```

### Configuration

```bash
gt config agent set <name> <cmd>  # Set custom agent
gt config default-agent <name>    # Set default runtime
```

## GUPP Mechanism

**GUPP = Gas Town Universal Propulsion Protocol**

Core principle: "If you find something on your hook, YOU RUN IT."

### Startup Sequence (via `gt prime`)

1. Detect role from current directory
2. Check for hooked work
3. IF work hooked:
   - Display "🚨 AUTONOMOUS WORK MODE 🚨"
   - Show assignment details
   - BEGIN IMMEDIATELY - no waiting
4. Send propulsion nudge via tmux
5. Run bd prime for workflow context
6. Inject pending mail

### Propulsion Loop

```bash
1. gt hook                    # What's hooked?
2. bd mol current             # Where am I in molecule?
3. Execute step
4. bd close <step> --continue # Close and auto-advance
5. GOTO 1
```

## MEOW Pattern

**MEOW = Mayor-Enhanced Orchestration Workflow**

### 7-Step Workflow

1. **Tell Mayor** - Describe what to build
2. **Mayor analyzes** - Breaks down into tasks
3. **Convoy creation** - Groups related issues
4. **Agent spawning** - Spawns polecats via `gt sling`
5. **Work distribution** - Issues hooked to agents
6. **Progress monitoring** - Track via `gt convoy status`
7. **Completion** - Mayor summarizes results

### Mayor Commands

```bash
gt mayor attach                        # Enter Mayor mode
gt convoy create "Feature X" issue-1 issue-2 --notify
gt sling issue-1 myproject             # Distribute to agent
gt convoy list                         # Monitor progress
```

## Polecat Lifecycle

### States

- `working` - Actively working on assigned issue
- `done` - Completed, ready for Witness cleanup
- `stuck` - Needs human assistance

### Commands

```bash
gt polecat spawn <name>        # Create and start polecat
gt polecat list                # List all polecats
gt polecat status <name>       # Show session info
gt polecat cycle <name>        # Graceful shutdown
gt polecat kill <name>         # Force terminate
```

## Agent Roles

| Role | Command | Responsibility |
|------|---------|----------------|
| Mayor | `gt mayor attach` | Global coordinator |
| Deacon | `gt deacon status` | Town-level health |
| Witness | `gt witness status` | Polecat health monitoring |
| Refinery | `gt refinery status` | Merge queue processing |
| Polecat | `gt polecat spawn` | Worker agent |
| Crew | `gt crew add` | Persistent worker |

## Environment Variables

```bash
GT_ROLE                # Role override
GT_RIG                 # Current rig
GT_POLECAT             # Polecat name
GT_SESSION_ID          # Session ID
BEADS_DIR              # Beads database location
```

## Anti-Patterns to Avoid

1. Don't read formulas directly - Use `bd cook` → `bd mol pour`
2. Don't wait after announcing - GUPP requires immediate execution
3. Don't use 3-command transitions - Use `bd close --continue`
4. Don't create manual convoys - Use `gt sling` (auto-creates)
5. Don't poll for work - Hooks are the assignment source

## Source

Repository: https://github.com/steveyegge/gastown
