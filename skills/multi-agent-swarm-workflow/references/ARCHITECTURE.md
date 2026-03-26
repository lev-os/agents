# Swarm Architecture

## Table of Contents
- [System Overview](#system-overview)
- [Component Roles](#component-roles)
- [Data Flow](#data-flow)
- [Agent Lifecycle](#agent-lifecycle)

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         BEADS (br)                              │
│     (Task graph with dependencies, priorities, status)          │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
┌─────────────────────────────┐  ┌─────────────────────────────┐
│        BV (bv)              │  │     AGENT MAIL              │
│  (What to work on next)     │  │  (Coordination layer)       │
│  - --robot-triage           │  │  - File reservations        │
│  - --robot-next             │  │  - Message threading        │
│  - --robot-insights         │  │  - Contact management       │
└─────────────────────────────┘  └─────────────────────────────┘
         │                            │
         └──────────────┬─────────────┘
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NTM + AGENTS                                 │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐         │
│  │ CC  │  │ CC  │  │ Cod │  │ Gmi │  │ CC  │  │ Cod │         │
│  │ 1   │  │ 2   │  │ 1   │  │ 1   │  │ 3   │  │ 2   │         │
│  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘         │
│  All agents are identical. All read same AGENTS.md.             │
│  Any can do any work. Failures replaced by new identical agent. │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Roles

| Component | Role | Key Commands |
|-----------|------|--------------|
| **Beads (br)** | Shared task pool | `br ready`, `br close`, `br list` |
| **BV (bv)** | Decentralized prioritization | `bv --robot-next`, `bv --robot-triage` |
| **Agent Mail** | Coordination layer | `send_message`, `file_reservation_paths` |
| **NTM** | Agent lifecycle management | `ntm spawn`, `ntm send`, `ntm dashboard` |
| **AGENTS.md** | Project context | Shared by all agents |

---

## Data Flow

### Task Selection Flow

```
Agent needs work
       │
       ▼
bv --robot-next ──► Returns bd-123
       │
       ▼
Agent claims bd-123
       │
       ├── br update bd-123 --status in_progress
       │
       └── send_message(..., subject="[bd-123] Starting...", thread_id="bd-123")
```

### File Reservation Flow

```
Agent starts on bd-123
       │
       ▼
file_reservation_paths(paths=["src/auth/**"], reason="bd-123")
       │
       ├── Conflict? ──► Coordinate via Agent Mail
       │
       └── No conflict ──► Work proceeds
       │
       ▼
Work complete
       │
       ▼
release_file_reservations(...)
```

### Coordination Flow

```
Agent A                          Agent B
   │                                │
   │  send_message(to=["B"])        │
   │ ─────────────────────────────► │
   │                                │
   │  ◄───────────────────────────  │
   │    reply_message(...)          │
   │                                │
```

---

## Agent Lifecycle

### Spawn Phase

```bash
ntm spawn myproject --cc=3 --cod=2 --gmi=1
```

Creates:
- 3 Claude Code sessions (cc-1, cc-2, cc-3)
- 2 Codex sessions (cod-1, cod-2)
- 1 Gemini session (gmi-1)

### Initialize Phase

```bash
ntm send myproject --all "$(cat marching_orders.txt)"
```

Each agent:
1. Reads AGENTS.md, README.md
2. Understands project architecture
3. Registers with Agent Mail
4. Introduces itself to other agents

### Work Phase

```
┌─────────────────────────────────────────────────┐
│                 WORK LOOP                       │
│                                                 │
│  1. bv --robot-next → find bead                 │
│  2. Claim bead, reserve files                   │
│  3. Implement                                   │
│  4. Self-review                                 │
│  5. Release files, close bead                   │
│  6. Check mail, respond                         │
│  7. Goto 1                                      │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Recovery Phase

When agent crashes or compacts:

```bash
# Add replacement agent
ntm add myproject --cc=1

# Send recovery prompt
ntm send myproject --pane cc-4 "$(cat marching_orders.txt)"
```

New agent picks up seamlessly — reads same AGENTS.md, sees same beads.

---

## The Flywheel

```
PLAN ──► BEADS ──► SWARM ──► REVIEW ──► COMMIT
  │                  │          │         │
  │                  │          └────┬────┘
  │                  │               │
  │                  └───── REPEAT ──┘
  │                              │
  │         v2 PLAN ◄────────────┘
  │              │
  └──────────────┘
```

Each cycle improves:
- **CASS** remembers solutions
- **CM** distills patterns
- **UBS** catches more issues
- **BV** shows graph health

---

## Recommended Agent Mix

| Project Size | Claude (Opus) | Codex | Gemini | Total |
|--------------|---------------|-------|--------|-------|
| Small        | 2             | 1     | 0      | 3     |
| Medium       | 3             | 2     | 1      | 6     |
| Large        | 5             | 3     | 2      | 10    |

**Note:** Mix is recommended because different models have different strengths. Claude excels at architecture, Codex at raw coding, Gemini at broad knowledge.
