---
name: cdo
description: |
  [WHAT] Adaptive multi-agent deliberation with composable presets
  [HOW] Composable args (quick/think/deep/full/debug + modifiers: hitl,bd,team,adaptive,lev-exec,exec)
  [WHEN] Design, architecture, complex problems, debugging, strategic analysis
  [WHY] Multi-turn adaptive thinking where turn N+1 is shaped by turn N's synthesis

  Triggers: "cdo", "think", "deliberate", "parliament", "multi-agent", "deep analysis", "debug rca"
skill_type: playbook
category: process-thinking
protocol_handlers:
  - lev://cdo?preset={quick|think|deep|full|debug}
plankton: false
metadata:
  triggers:
    - cdo
    - think
    - deliberate
    - parliament
    - multi-agent
    - deep analysis
    - debug rca
  tools:
    - Read
    - Write
    - Edit
    - Bash
    - Grep
    - Glob
    - Agent
    - TeamCreate
    - TaskCreate
    - TaskUpdate
    - TaskList
    - SendMessage
    - AskUserQuestion
  skill_evolver:
    enabled: true
    version: 2.0.0
    log_path: ~/.config/lev/logs/skills.jsonl
    hooks:
      - on_invoke
      - on_fail
      - on_success
---

# CDO — Adaptive Multi-Agent Deliberation

CDO is an adaptive multi-agent deliberation system. Agents save work to disk. A synthesizer runs between turns. Turn N+1's shape is determined by Turn N's synthesis — width, roles, skills, and focus all flex based on what the previous turn discovered.

This is NOT a pre-planned graph. It's an adaptive research workflow where the problem itself tells you what to do next.

The orchestrator never thinks. It dispatches, collects, and routes. All reasoning happens in agents.

---

## 1. Entry Point + Arg Parser

```
/cdo <args,...> <problem>
```

Args are composable, comma-separated. First token is base preset OR modifier. Additional tokens stack.

### Examples

```
/cdo think "Should we reduce node types?"
/cdo quick "Summarize A2A conflicts"
/cdo full "Evaluate architecture"
/cdo hitl "Design execution model"
/cdo bd,full "Track everything in beads"
/cdo team,full "Persistent teammates"
/cdo adaptive,team,full "Grow/shrink team per turn"
/cdo lev-exec "Multi-model comparison"
/cdo exec dev "POC dev team following lev sdlc"
/cdo exec arch "Architecture planning team"
/cdo debug "Gateway crashes"
```

### Arg Parse Order

1. **Base preset**: `quick` | `think` | `deep` | `full` | `debug`
   - If omitted, GAUGE determines it from problem complexity
2. **Modifiers** (stackable, comma-separated): `hitl`, `bd`, `team`, `adaptive`, `lev-exec`
   - Modifiers augment the base preset — they don't replace it
3. **Domain**: `exec dev` | `exec arch` | `exec <tag>`
   - Domain presets inject team shapes, skills, and integration targets
4. **Problem**: Everything after args — the actual question or task

### Parse Algorithm

```
tokens = split(args, ",")
for token in tokens:
  if token in {quick, think, deep, full, debug}:
    base_preset = token
  elif token in {hitl, bd, team, adaptive, lev-exec}:
    modifiers.add(token)
  elif token == "exec":
    domain = next_token  # dev, arch, or <tag>
  else:
    problem.append(token)

if not base_preset:
  base_preset = gauge(problem)
```

---

## 2. Presets Table

| Preset | Width | Max Turns | BD | Skills | Team Mode | Dashboard | Adaptive |
|--------|-------|-----------|-----|--------|-----------|-----------|----------|
| `quick` | 1-2 | 1 | No | No | Subagents | No | No |
| `think` | 2-4 | 2-3 | No | Optional | Subagents | No | No |
| `deep` | 3-8 | 3-5 | Yes | Yes | TeamCreate | Yes | No |
| `full` | 5-20 | 5-10 | Yes | Yes | TeamCreate | Yes | Yes |
| `debug` | 1-3 | 7 (fixed) | No | No | Subagents | No | No |

### Dashboard Rule

Unless `quick` or `think`, ALWAYS show the planning dashboard before T1.

### HITL Dashboard

Interactive DAG design — user sees a sample DAG with proposed turns, agents, roles, and skills. User can:

- Modify roles (add/remove/rename)
- Swap skills per agent
- Select power combos (e.g., "architect + critic + pragmatist")
- Adjust turn count and width
- Override convergence criteria

---

## 3. Domain Presets (exec variants)

| Domain | Team Shape | Skills | Integration |
|--------|-----------|--------|-------------|
| `exec dev` | Dev Lead, Implementer, Reviewer, Tester | lev-sdlc, /work, entity lifecycle | `.lev/pm/` entities, bd tasks |
| `exec arch` | Architect, Critic, Systems, Pragmatist | /arch, ATAM, C4, ADR | `docs/specs/`, `docs/design/` |
| `exec <tag>` | Auto-composed from skill-discovery | lev-catalog search by tag | Workshop POC skills weighted |

When a domain is specified, its team shape becomes the T1 default. The synthesizer can still reshape subsequent turns.

---

## 4. The Core Loop

This is the beating heart of CDO. Everything else is configuration around this loop.

```
PARSE ARGS → resolve base preset + modifiers + domain
  │
  ├─ GAUGE → classify complexity (or accept preset override)
  │    Input: problem statement
  │    Output: recommended preset if none specified
  │    Method: token count, question marks, domain keywords, scope markers
  │
  ├─ BD INIT (if deep+ or bd modifier):
  │    ├─ bd create epic "CDO: {problem}" --json
  │    └─ Each turn → bd create task under epic
  │
  ├─ DASHBOARD (if deep+ or hitl modifier):
  │    ├─ Show proposed DAG: turns, agents, roles, skills
  │    ├─ If HITL: interactive — user modifies DAG, selects combos
  │    └─ If auto: display briefly, proceed
  │
  ├─ TEAM INIT (if deep+ or team modifier):
  │    └─ TeamCreate with initial roles from preset or domain
  │
  └─ TURN LOOP:
       │
       ├─ COMPOSE: Read previous synthesis (or input for T1)
       │    ├─ Decide width (adaptive: grow/shrink based on synthesis)
       │    ├─ Decide roles (from preset, domain, or synthesis directive)
       │    ├─ Skill discovery → 2-3 skills per agent
       │    │   Load: dispatch/skill-injection.md
       │    └─ Generate agent briefs
       │        Load: templates/agent-brief.md
       │
       ├─ DISPATCH:
       │    ├─ Subagent mode: parallel Agent calls in single message
       │    ├─ Team mode: SendMessage to existing teammates + spawn new if needed
       │    ├─ lev-exec mode: Bash → codex/openrouter for multi-model
       │    ├─ Each agent writes to: tmp/cdo-{session}/t{N}-{role}.md
       │    └─ BD: update turn task status → in_progress
       │
       ├─ SYNTHESIZE: Dedicated synthesis agent
       │    Load: engine/synthesis-protocol.md
       │    ├─ Reads ALL turn N artifacts from disk
       │    ├─ Produces: common ground, tensions, gaps, surprises
       │    ├─ Anti-groupthink check (>70% agreement = flag)
       │    ├─ NEXT TURN DIRECTIVE (YAML block):
       │    │     width: <int>
       │    │     roles: [list]
       │    │     skills: [list]
       │    │     focus: "<string>"
       │    │     confidence: <0-1>
       │    │     exit_ready: <bool>
       │    └─ BD: close turn task, create next turn task
       │
       └─ ADAPT:
            ├─ Auto mode: follow directive, advance to next turn
            ├─ Adaptive mode: grow/shrink team (add/remove teammates)
            ├─ Conflict escalation: pause if confidence drops or big tensions
            ├─ HITL mode: present updated dashboard, user picks next turn
            └─ Convergence: exit to FINAL if criteria met or max turns
                Load: engine/convergence.md
```

### Convergence Criteria

Exit the turn loop when ANY of:

- Synthesis `exit_ready: true` AND `confidence >= 0.8`
- Max turns reached for preset
- All tensions resolved (no new gaps in 2 consecutive turns)
- HITL user says "done"

### FINAL Output

When converged, the synthesizer produces `FINAL.md`:

- **Decision/Answer**: The actual output
- **Confidence**: Numeric + qualitative
- **Key Tensions**: What was debated, what won, why
- **Minority Reports**: Dissenting views that didn't win but deserve record
- **Action Items**: If applicable, concrete next steps
- BD: close epic if tracked

---

## 5. Artifact Structure

```
tmp/cdo-{timestamp}/
├── 00-input.md           # Original problem statement
├── 00-context.md         # Gathered context (files, code, docs)
├── t1-{role}.md          # Turn 1 agent outputs (one per agent)
├── t1-synthesis.md       # Turn 1 synthesis + next turn directive
├── t2-{role}.md          # Turn 2 agent outputs
├── t2-synthesis.md       # Turn 2 synthesis
├── ...
└── FINAL.md              # Converged output
```

### Artifact Rules

- Every agent writes its own file. No shared state between agents during a turn.
- Synthesis reads all turn files. Only synthesis produces the directive.
- The orchestrator reads ONLY the directive YAML block — not the full synthesis.
- FINAL.md is the only user-facing deliverable. Turn artifacts are audit trail.

---

## 6. When to Load Sub-Files

Progressive disclosure — only load what the current invocation needs.

| Condition | Load | Purpose |
|-----------|------|---------|
| Complexity >= deep | `dispatch/skill-injection.md` | Skill discovery + injection protocol |
| Team mode active | `dispatch/team-mode.md` | TeamCreate/SendMessage patterns |
| lev-exec mode | `dispatch/multi-model.md` | Multi-model dispatch via CLI |
| Preset == debug | `modes/debug.md` | 7-turn RCA protocol |
| Preset == full + parliament | `modes/parliament.md` | Multi-model parliament seats |
| Need convergence help | `engine/convergence.md` | Exit criteria + confidence calc |
| Synthesis turn | `engine/synthesis-protocol.md` | Synthesis agent instructions |
| Agent brief generation | `templates/agent-brief.md` | Brief template + role injection |
| Domain == exec dev | `domains/dev.md` | Dev team shape + SDLC integration |
| Domain == exec arch | `domains/arch.md` | Architecture team + ADR output |
| Domain == exec <tag> | `domains/generic.md` | Auto-compose from skill catalog |

---

## 7. Sub-Skills Reference

### engine/

| File | Purpose | Load When |
|------|---------|-----------|
| `synthesis-protocol.md` | How the synthesis agent operates — reading artifacts, producing directives, anti-groupthink | Every turn's SYNTHESIZE phase |
| `convergence.md` | Exit criteria, confidence calculation, when to force-exit vs extend | Adapt phase, when checking exit conditions |

### dispatch/

| File | Purpose | Load When |
|------|---------|-----------|
| `skill-injection.md` | How to discover and inject 2-3 skills per agent via skill-discovery | COMPOSE phase for deep+ presets |
| `team-mode.md` | TeamCreate/SendMessage patterns, teammate lifecycle, idle/wake | Team modifier or deep+ preset |
| `multi-model.md` | Multi-model dispatch via codex/openrouter CLI, response normalization | lev-exec modifier |

### modes/

| File | Purpose | Load When |
|------|---------|-----------|
| `debug.md` | 7-turn RCA protocol: reproduce → isolate → hypothesize → verify → fix → validate → document | debug preset |
| `parliament.md` | Multi-model parliament with genuine perspective diversity across providers | full preset with parliament intent |

### templates/

| File | Purpose | Load When |
|------|---------|-----------|
| `agent-brief.md` | Template for agent dispatch briefs — role, context, constraints, output format | COMPOSE phase, every turn |

### domains/

| File | Purpose | Load When |
|------|---------|-----------|
| `dev.md` | Dev team shape, SDLC lifecycle integration, entity management | exec dev domain |
| `arch.md` | Architecture team, ATAM/C4/ADR output patterns | exec arch domain |
| `generic.md` | Auto-compose team from skill-discovery catalog by tag | exec <tag> domain |

---

## 8. Anti-Patterns

**Don't pre-plan all turns at start.** The whole point is adaptive — turn N+1 is shaped by turn N. Planning T3 at T0 defeats the purpose.

**Don't let the orchestrator synthesize.** The orchestrator dispatches and routes. Synthesis is ALWAYS a dedicated agent that reads artifacts from disk. The orchestrator is a router, not a thinker.

**Don't let agents see each other's work during a turn.** Independence produces genuine diversity. Cross-pollination happens only through synthesis.

**Don't skip the dashboard for deep+.** The dashboard catches bad team composition before you burn 5 agent calls. Two seconds of preview saves minutes of wasted work.

**Don't use CDO for simple questions.** If the answer fits in one sentence, just answer it. CDO is for problems that benefit from multiple perspectives and iterative refinement.

**Don't force convergence.** If agents genuinely disagree after max turns, report the disagreement. Forced consensus is worse than honest tension.

**Don't recycle role names across turns without reason.** If synthesis says "drop the Pragmatist, add a Security Reviewer," do that. Roles are disposable.

---

## 9. Related Skills

- `skill://lev-research` — Deep research intelligence. CDO can dispatch research agents that use this skill for recon and evidence gathering.
- `skill://bd` — Beads issue tracking. CDO uses bd for epic/task tracking in deep+ presets and when the bd modifier is active.
- `skill://work` — Unified lifecycle router. CDO's exec dev domain aligns with /work's entity lifecycle and SDLC stages.
- `skill://arch` — Architecture analysis. CDO's exec arch domain loads /arch's ATAM, C4, and ADR frameworks into architect agents.
- `skill://lev-find` — Context gathering. CDO agents use find for codebase exploration during the COMPOSE phase.
- `skill://skill-discovery` — Skill catalog search. CDO's skill injection uses this to discover and load 2-3 skills per agent.
- `skill://lev-orch-thinking-parliament` — Legacy parliament mode. CDO subsumes this — use `modes/parliament.md` instead.
