# L3: Sprint Orchestrator

> Multi-entity, cross-session dispatch layer. Sits above the `/work` FSM (L2) and lifecycle plugins (L1). Tracks N entities across M sessions with incremental handoffs, priority-scored tick dispatch, and team management via CDO primitives.

### A. Multi-Entity Tracking Schema

#### Entity Record Format

Each tracked entity has a canonical record. Stored in the session handoff document (not a separate database — the handoff IS the persistence layer until graph/CMS lands).

```yaml
entity:
  id: "<bead-id or slug>"          # Unique identifier (bd ID preferred, slug fallback)
  name: "<human-readable name>"     # Display name
  lifecycle: "<state>"              # draft | approved | implementing | parity | iterating
  last_gate: "<gate-name>"          # Last FSM gate passed (e.g., gate:propose-spec)
  blocked_by: []                    # List of entity IDs this is waiting on
  zoom: "<L0|L1|L2|L3>"            # Current working depth (dimension-model.md)
  layer: "<brand-layer>"            # Site | Structure | Skin | Services | Space Plan | Stuff
  priority: <1-5>                   # 1 = highest, 5 = lowest (computed, see Tick Dispatch)
  session_log:                      # Append-only, one entry per session that touches this entity
    - session: "<date-session#>"
      tick: "<tick#>"
      action: "<what happened>"
      gate: "<gate passed, if any>"
      artifacts: []                 # Beads, files, or reports created
```

#### Entity Matrix Rendering

Render as a table in every session handoff and sprint status output. This is the canonical view:

```
| # | Entity | Lifecycle | Last Gate | Blocked By | Zoom | Layer | Pri | Last Session |
|---|--------|-----------|-----------|------------|------|-------|-----|--------------|
| 1 | Runtime Contracts | implementing | spec-execute | — | L2 | Structure | 2 | S2-T6 |
| 2 | SDLC Plugin | draft | discover-align | Runtime Contracts | L1 | Services | 3 | S2-T5 |
```

#### State Transition Tracking

Every lifecycle state change is recorded in the entity's `session_log` with:
- **Timestamp**: session + tick (e.g., `S2-T6`)
- **From/To**: previous state and new state
- **Gate**: which gate validated the transition
- **Evidence**: bead ID, commit SHA, or report path that justified the transition

Transitions that require human approval (per decision #20 in sprint handoff):
- `draft -> approved` — CDO deliberation gate + human sign-off
- All others — can be automated if gate passes, but human can override

---

### B. Session Handoff Protocol

The handoff document is the continuity device. It grows incrementally across sessions. One file per sprint.

**Location:** `.lev/pm/handoffs/{YYYYMMDD}-{sprint-slug}.md`

#### Required Sections

##### 1. Session Lens
One paragraph: what zoom level are we operating at, what kind of work is this session about.

##### 2. Entity Matrix (Section A format)
Snapshot at session start. Updated at session end. Diff is the session's contribution.

##### 3. Decisions Log
Numbered, append-only. Each decision includes:
- **Decision number** (global across sprint, not per-session)
- **Statement** (what was decided)
- **Rationale** (why, in one sentence)
- **Source** (user directive, gate output, CDO deliberation, or inference)

##### 4. Tick Log
Append-only. One tick per meaningful state change. Format:

```markdown
#### Tick N: {Title} ({HH:MM or session marker})
- {What happened}
- {Entities affected}
- {Decisions made (reference by number)}
- {Subagents dispatched or completed}
- {Gate transitions}
```

**What constitutes a tick:**
- Entity lifecycle state change
- Gate evaluation (pass or fail)
- Subagent dispatch or completion
- Human decision or correction
- Research phase completion
- Session start/end

**What does NOT get a tick:**
- Routine file reads
- Intermediate thinking
- Tool failures and retries
- Questions asked without answers yet

##### 5. Open Questions
Tracked per-session, carried forward until resolved. Format:

```markdown
- [ ] {Question} — raised S{N}-T{M}, domain: {entity or general}
- [x] {Question} — raised S{N}-T{M}, resolved S{P}-T{Q}: {answer}
```

##### 6. Subagent Dispatch Log
Track every subagent and teammate dispatched:

```markdown
| Agent | Type | Task | Dispatched | Status | Result |
|-------|------|------|------------|--------|--------|
| oracle-poly | subagent | Deep poly/daemon audit | S2-T5 | RESOLVED | reports/poly-daemon-deep-analysis.md |
| shell-impl-a | teammate | Implement 13 shell components | S2-T5 | PENDING | — |
```

Status values: `DISPATCHED` -> `WORKING` -> `RESOLVED` | `FAILED` | `ABANDONED`

##### 7. Files Touched
Manifest of all files created or modified this session. Absolute paths.

##### 8. Research Reports
Links to saved context (reports, bead IDs, analysis outputs) that survive context compaction.

---

### C. Tick Dispatch

#### Priority Scoring

Each entity gets a priority score (1-5) recomputed at session start and after each tick. Lower = higher priority.

```
base_priority = layer_weight + lifecycle_weight

layer_weight:
  Site        = 1  (foundational, do first)
  Structure   = 1
  Skin        = 2
  Services    = 2
  Space Plan  = 3
  Stuff       = 4

lifecycle_weight:
  implementing = 0  (in-flight work, keep momentum)
  parity       = 0  (close to done, push through)
  approved     = 1  (ready to start)
  draft        = 2  (still forming)
  iterating    = 3  (maintenance mode, lower urgency)

modifiers:
  blocked_by non-empty       → +5 (deprioritize blocked entities)
  gate_ready (next gate passable) → -1 (promote gate-ready entities)
  stale (no activity in 2+ sessions) → +1 (slight deprioritization for stale work)
  human_requested            → override to 1 (user explicitly asks for this)

final_priority = clamp(base_priority + modifiers, 1, 5)
```

#### Cross-Entity Dependency Detection

Before dispatching a tick, scan the entity matrix for:

1. **Direct blocks**: Entity A's `blocked_by` contains Entity B
2. **Implicit blocks**: Entity A's spec references Entity B's contracts, and B is still in `draft`
3. **Resource conflicts**: Two entities modify the same files/modules (detected via spec `integration_points`)

When detected:
- If blocker is dispatchable, dispatch blocker first
- If blocker is blocked itself, flag as **deadlock risk** and escalate to human
- If resource conflict, serialize (don't parallelize) those entities

#### Session Capacity Estimation

At session start, estimate how many ticks fit:

```
capacity_factors:
  - Entity count: N entities in non-terminal state
  - Average tick cost: ~10-15 minutes for research/gate, ~20-30 for implementation
  - Session budget: ~2-3 hours typical (user can override)
  - Parallel capacity: up to 6 subagents + 2-3 teammates simultaneously

estimated_ticks = session_budget / avg_tick_cost
dispatchable = entities where blocked_by is empty, sorted by priority
plan = dispatchable[:estimated_ticks]
```

Present the session plan to the user before executing:

```
Session {N} Plan — {estimated_ticks} ticks, {len(dispatchable)} entities ready
Priority dispatch order:
1. {entity} — {lifecycle} — {reason this is next}
2. {entity} — {lifecycle} — {reason}
...
Blocked (will not dispatch): {blocked_entities with reasons}
```

#### Entity Readiness Assessment

Before dispatching an entity into the L2 `/work` FSM, verify:

| Check | Condition | If Failed |
|-------|-----------|-----------|
| Dependencies clear | `blocked_by` is empty | Skip, dispatch blocker instead |
| Prior session context | Last session's artifacts accessible | Load from handoff, or re-research |
| Gate state known | `last_gate` is valid and current | Re-evaluate gate before dispatch |
| Zoom appropriate | Working at declared zoom level | Adjust zoom if scope changed |
| Domain artifact exists (if implementing+) | Domain crystallization bead linked (e.g. `custom:spec` for SDLC, `custom:storyboard` for video) | Block — cannot implement without crystallized artifact |

---

### D. Deepen Route

**Deepen** is a named composition — not a lifecycle state, not a separate skill. It's a runtime process that attaches to an entity to enrich evidence before or during gate evaluation.

#### Composition

```
deepen(entity):
  1. CDO decompose(entity.crystallization_artifact)
     → Extract 3-7 research topics from the spec/proposal
     → Classify each topic: codebase, architecture, external, UX, testing

  2. skill-discovery(topics)
     → Search ~/.agents/skills/ for relevant skills per topic
     → Inject discovered skill content into research agent prompts

  3. parallel-research(topics)
     → Per topic, dispatch subagent:
        - Codebase topics: grep + read + trace dependencies
        - Architecture topics: read design docs + cross-reference specs
        - External topics: lev-research (online search + synthesis)
        - UX topics: load ux skill, analyze interaction patterns
        - Testing topics: read test suites, identify coverage gaps

  4. manifestation-review(results)
     → If /ux relevant: review design implications
     → If /arch relevant: review architectural coherence
     → If both: cross-reference UX feasibility against architecture constraints

  5. evidence-synthesis(all_results)
     → Merge all research into a single evidence brief
     → Score confidence per topic (0.0-1.0)
     → Identify gaps that need human input
     → Attach evidence brief to entity's bead as custom:report
```

#### Trigger Modes

| Mode | Trigger | Depth | Cost |
|------|---------|-------|------|
| **Auto** | `draft -> approved` gate transition | Full composition (all 5 steps) | 3-7 subagents |
| **Manual** | `/work deepen` command at any stage | Full composition | 3-7 subagents |
| **Confidence-gated** | Gate evaluation finds confidence < 0.80 | Steps 1-3 only (skip manifestation) | 2-5 subagents |

#### Auto Trigger Integration

When the CDO deliberation gate fires during `draft -> approved`:

```
1. CDO deliberation runs (5 roles evaluate spec)
2. If PASS: deepen fires automatically
   → Research enriches the approved spec
   → Evidence attaches to entity bead
   → Entity proceeds to implementing when deepen completes
3. If FAIL: return to draft with CDO feedback
   → No deepen (would waste resources on a rejected spec)
```

#### Manual Trigger

```
/work deepen [entity-id]
```

- If entity-id omitted, deepen the entity currently in focus
- Can run at any lifecycle stage (including `implementing` for mid-flight enrichment)
- Does not change entity lifecycle state
- Results attach as `custom:report` bead linked to the entity

#### Confidence-Gated Trigger

During any gate evaluation, if computed confidence < 0.80:

```
gate evaluating...
confidence = 0.72 (below threshold)
→ Auto-trigger deepen(steps 1-3) for the specific topics dragging confidence down
→ Re-evaluate gate with enriched evidence
→ If still < 0.80 after deepen: escalate to human
```

#### Deepen Output Format

```yaml
deepen_report:
  entity: "<entity-id>"
  trigger: "<auto|manual|confidence>"
  topics_researched: <N>
  confidence_before: <0.0-1.0>
  confidence_after: <0.0-1.0>
  evidence:
    - topic: "<topic name>"
      source: "<codebase|architecture|external|ux|testing>"
      findings: "<summary>"
      confidence: <0.0-1.0>
      skills_used: ["<skill names>"]
      artifacts: ["<file paths or bead IDs>"]
  gaps:
    - "<what still needs human input>"
  recommendation: "<proceed|deepen-further|escalate>"
```

---

### E. Team Management

#### When to Spawn Teammates vs Subagents

Use CDO complexity classification (from `lev-cdo` skill) to determine team shape:

| Entity Complexity | Signal | Strategy | Agents |
|-------------------|--------|----------|--------|
| **Quick** (single file, clear path) | Stuff/Space layer, confidence >= 0.90 | Direct execution in current context | 0 (inline) |
| **Base** (2-3 files, some ambiguity) | Skin/Services layer, confidence >= 0.80 | Parallel subagents for research + implementation | 2-4 subagents |
| **Deep** (multi-file, cross-cutting) | Structure layer, confidence >= 0.60 | Formal team with role-based teammates | 3-5 teammates + subagents |
| **Epic** (multi-phase, multi-entity) | Site layer, confidence < 0.60 | Full team + subagent swarm + BD tracking | 5-8 teammates + N subagents |

#### Skill Injection Protocol

Before spawning any agent (teammate or subagent), discover and inject relevant skills:

```
1. Extract keywords from entity spec/proposal
2. Search skill sources (priority order from work SKILL.md):
   a. Project-local: .claude/skills/, .agents/skills/ in project
   b. Global canonical: ~/.agents/skills/
   c. Skills DB: ~/.agents/skills-db/
   d. POC/polymath: ~/lev/workshop/poc/skills/, ~/lev/workshop/intake/cc-polymath/skills/
3. For each matched skill:
   a. Read SKILL.md content
   b. Inject as system prompt prefix for the agent
   c. Log which skills were injected (for audit trail)
```

**Teammate prompt template:**

```
You are {role_name} for the {entity_name} workstream.

### Loaded Skills
{injected_skill_content}

### Your Task
{task_description}

### Entity Context
- Lifecycle: {lifecycle_state}
- Last gate: {last_gate}
- Zoom: {zoom_level}
- Sprint: {sprint_id}

### Return Format
Return an executive brief with:
- edited_files: [<absolute paths>]
- bd_changes: "<summary or 'none'>"
- summary: "<1-2 sentences>"

If your output exceeds 5000 tokens, save a detailed report to:
  .lev/pm/reports/{YYYYMMDD}-{entity-slug}-{role}.md
and return only the executive brief.
```

#### Worker Lifecycle

```
SPAWN → ASSIGN → MONITOR → COLLECT → REMOVE

SPAWN:
  - Teammate: persistent, named, skill-injected
  - Subagent: ephemeral, task-scoped, skill-injected

ASSIGN:
  - Create TaskCreate with entity context
  - Set dependencies via TaskUpdate (addBlockedBy)
  - Assign owner via TaskUpdate (owner: agent-name)

MONITOR:
  - Teammates: check via TaskList periodically
  - Subagents: await Task tool completion
  - Idle teammates: OK (CDO convention — don't react unless re-assigning)
  - Stuck agents (no progress after 2 check-ins): escalate or reassign

COLLECT:
  - Read returned executive brief
  - If report file exists, note path in handoff (don't inline)
  - Update entity session_log with results
  - Update entity lifecycle state if gate passed

REMOVE:
  - Subagents: auto-terminate on task completion
  - Teammates: SendMessage shutdown_request when sprint or entity work completes
  - Always collect results before shutdown
```

#### Return Format by Zoom Level

Per dimension-model.md, agent returns scale with zoom:

| Zoom | Return Depth | Format |
|------|-------------|--------|
| **L0** | One line per file touched | `path: <one-line change summary>` |
| **L1** | Paragraph summary per task | Summary + decisions + file manifest |
| **L2** | Detailed report with code context | Full report (save to file if > 5000 tokens) |
| **L3** | Runtime trace with evidence | Report + test results + screenshots |

---

### F. Sprint Lifecycle

#### Definition

A sprint is a **goal-boxed** (not time-boxed) container for multi-session work. It tracks N entities from their current lifecycle state toward defined goals.

#### Sprint Record

```yaml
sprint:
  id: "<slug>"
  goal: "<what we're trying to accomplish>"
  started: "<YYYY-MM-DD>"
  sessions: <count>
  status: "<active|paused|completed|pivoted>"
  entity_goals:
    - entity: "<id>"
      target_state: "<lifecycle state to reach>"
      reached: <bool>
  decisions: <count>  # Total decisions across all sessions
  ticks: <count>      # Total ticks across all sessions
```

#### Sprint Start

1. **Snapshot entity matrix** — capture current state of all entities
2. **Define goals** — for each entity, what lifecycle state should it reach?
3. **Assess feasibility** — are goals achievable given dependencies and capacity?
4. **Set priorities** — run priority scoring (Section C) across all entities
5. **Create handoff document** — `.lev/pm/handoffs/{YYYYMMDD}-{sprint-slug}.md`
6. **Present sprint plan** to human for approval

#### Sprint Cadence

```
Session 1 → Handoff → Session 2 → Handoff → ... → Sprint Close
    |                     |                            |
    v                     v                            v
  Ticks 0-N           Ticks N+1-M                  Review all goals
  Entity work         Entity work                  Met? → Close
  Decisions           Decisions                    Not met? → Extend or Pivot
  Gate transitions    Gate transitions
```

**Between sessions:**
- Handoff document is the ONLY continuity device
- No state lives outside the handoff + beads
- Next session starts by reading the handoff and reconstituting context

**Session start protocol:**
1. Read sprint handoff document
2. Render entity matrix (current state)
3. Check for overnight changes (git log, bd list, new beads)
4. Recompute priorities
5. Present session plan (Section C capacity estimation)
6. Get human go-ahead

#### Sprint Close

A sprint closes when ONE of:
- **All goals met**: every entity reached its target lifecycle state
- **Explicit pivot**: human decides to change direction (document rationale as a decision)
- **Stall detected**: 2+ consecutive sessions with zero entity state transitions (escalate to human)

**Sprint close ceremony:**

```
1. Final entity matrix snapshot (before/after comparison with sprint start)
2. Decisions summary (all decisions, grouped by entity)
3. Metrics:
   - Sessions: N
   - Ticks: M
   - Entities advanced: X/Y
   - Goals met: A/B
   - Subagents dispatched: P (Q resolved, R failed)
4. Learnings extraction (feeds into L2 /work LEARN step):
   - What worked
   - What didn't
   - Process improvements for next sprint
5. Create sprint close bead:
   br create "Sprint: {slug} — Close" \
     --type '{"custom":"report"}' \
     --labels "sprint,close,{domain}" \
     --description "{close summary}"
6. Archive handoff (keep file, mark sprint status: completed)
```

#### Sprint Pivot

When goals change mid-sprint:

1. Record pivot decision with rationale (numbered in decisions log)
2. Update entity goals in sprint record
3. Recompute priorities with new goals
4. Do NOT create a new sprint — pivots are part of the sprint's history
5. Mark old goals as `pivoted` (not failed)

---

### G. Sprint Orchestrator Sub-Skill Routing

Use this router before each L3 tick dispatch. Goal: deterministic sub-skill selection, SDK-first orchestration, and stable handoffs.

| Sprint operation | Primary sub-skill | Secondary sub-skills | Dispatch condition |
|------------------|-------------------|----------------------|--------------------|
| Sprint/session bootstrap | `lev-cdo-router` | `lev-cdo` | Every session start before first tick |
| Complexity execution path | `lev-cdo-workflows` | `work` | Router returns `deep` or `epic` |
| Skill context injection | `skill-discovery` | `find-skills` | Before spawning any teammate/subagent |
| Human gate escalation | `agentping` | `work` gate hooks | CDO gate/hard blocker needs explicit approval |
| Evidence quality pass | `workflow-quality-audit` | `work` VALIDATE | Sprint close or parity promotion checks |
| External context sweep | `lev-find` | `research` | Confidence-gated deepen or stale evidence |

#### Routing policy

1. Run `lev-cdo-router` first for every new entity tick.
2. If complexity is `deep` or `epic`, chain `lev-cdo-workflows` before dispatch.
3. Always run `skill-discovery` before worker spawn and inject matched skills in prompts.
4. Use `agentping` only for explicit human-in-the-loop requirements.
5. Run `workflow-quality-audit` before sprint close to verify evidence coverage.

#### Worker return contract (required)

All sprint workers must return:

- `edited_files`: absolute-path file manifest
- `summary`: executive brief (1-2 sentences)
- `report_path`: required only when output exceeds 5000 tokens

### Integration with L2 /work FSM

The scheduling layer (L3) dispatches entities into the `/work` FSM (L2) one at a time:

```
L3 (scheduling)                    L2 (/work FSM)
├── Pick highest-priority entity
├── Check readiness (Section C)
├── Dispatch to /work              → DISCOVER → ALIGN → RESEARCH → PROPOSE → SPEC → EXECUTE → VALIDATE → EMIT → LEARN
├── Collect results                ←  (artifacts, gate results, learnings)
├── Update entity matrix
├── Record tick
├── Pick next entity
└── Repeat until session capacity exhausted
```

**Key boundary:** L3 owns *which* entity and *when*. L2 owns *how* the entity moves through its lifecycle. L1 plugins own *domain-specific* validation and transitions.

---

### Integration with L1 Lifecycle Plugins

Lifecycle plugins (SDLC, etc.) attach domain-specific behavior to gate transitions:

```
L3 dispatches entity → L2 runs FSM → Gate fires → L1 plugin validates

Example:
  Entity: "API v2 Migration" (layer: Structure)
  L2: gate:spec-execute fires (CATASTROPHIC)
  L1 (SDLC plugin): adds checks for:
    - CI pipeline exists for the target branch
    - Breaking change RFC published
    - Migration guide drafted
  L2: merges L1 checks into gate evaluation
  L3: records gate result in entity session_log
```

Plugin composition follows the overlay pattern:
- Abstract base handles scheduling/reminders/tracking
- Domain plugins overlay domain-specific gates
