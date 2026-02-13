---
name: lev
description: |
  [WHAT] CLI and SDK reference surface for Lev primitives.
  [HOW] Maps natural language aliases to stable primitives: get/work/ask/check/go.
  [WHEN] Use when you need command syntax, alias mapping, protocol routing, or SDK usage.
  [WHY] Keeps CLI usage stable while lifecycle/process logic lives in `work`.

  Triggers: "lev", "leviathan", "get", "search", "find", "lookup", "read", "ls",
            "research", "think", "spec", "plan", "execute", "analyze", "design",
            "validate", "align", "lifecycle", "work", "check", "scan", "security", "daemon",
            "daemons", "ask", "wiz", "wizard", "go", "handoff", "exit", "learn", "workflow", "skill"
skill_type: how-to
category: cli
primitive_owner: lev
lifecycle_owner: work

lifecycle_integration:
  router: true
  lifecycle_owner: work
  mode: delegate
  delegation:
    ephemeral: [work]
    captured: [work]
    classified: [work]
    crystallizing: [work]
    crystallized: [work]
    manifesting: [work]
    completed: [work]
    discarded: [work]

protocol_handlers:
  core:
    - lev://get?query={q}&depth={d}&scope={s}
    - lev://find?query={q}&scope={s}  # legacy alias -> lev://get
    - lev://exec?task={t}&epic={e}
    - lev://lifecycle?from={f}&to={t}
    - lev://research?depth={d}&topic={t}
    - lev://align?check={c}
  plugins:
    - workshop://intake/{platform}
    - timetravel://pattern/{name}
  skill:
    - skill://{skill-name}?{params}
  flowmind:
    - flowmind://entity-lifecycle?state={s}

plankton: true
constitutional: true
reference_protocol: "flowmind://lev-core-protocol"

action_directives:
  handoffs: "Load lev to resume: lev://lifecycle?from=handoff"
  proposals: "Convert to spec: lev://lifecycle?from=crystallizing&to=crystallized"
  specs: "Execute: lev://exec?epic={bd_epic_id}"
  reports: "Design solution: lev://lifecycle?from=captured&to=crystallizing"

sub_skills:
  # Core 12
  - lev-find
  - lev-research
  - lev-index
  - lev-cdo
  - lev-ultra
  - lev-align  # legacy standalone; prefer `work` alignment gate
  - lev-test
  - lev-lifecycle
  - work
  - lev-learn
  - lev-builder
  - lev-workshop
  # Additional
  - lev-clwd
  - lev-intake
  - lev-ux
  - lev-examples
  - skill-builder
  - lev-computer-use
---

# Lev: Plankton Router

**IMPORTANT:** This skill is "plankton" - always referenced in handoffs, proposals, specs, and compact summaries. Every mention should be action-oriented.

---

## Lev Concept

**What is lev?**
Lev is the master router and entry point for the entire Leviathan ecosystem. It's a "plankton" skill - small, foundational, referenced everywhere, and essential to the lifecycle.

**Why plankton?**
Like plankton in an ocean ecosystem:
- **Foundational:** Everything feeds from it
- **Distributed:** Referenced in every lifecycle artifact
- **Action-oriented:** Always includes next actions
- **Constitutional:** Defines core protocols

**When to use:**
- ANY work request (get, think, spec, execute)
- Entity lifecycle transitions
- Protocol handler lookups
- Skill discovery

**Plankton behavior:**
Every lifecycle artifact (report, proposal, spec, handoff) should reference lev with action directives:
- "Load lev to advance this work"
- "Use lev://lifecycle to transition states"
- "Execute via lev://exec"

---

## CLI Commands

### Primary: lev (entry point)

```bash
# Auto-routes based on keywords
lev get "auth middleware patterns"
lev "research authentication patterns"
lev "design user management system"
lev "spec implementation behavior for feature X"
lev "execute epic clawd-h2qg"
```

### Core Primitive: lev get

`lev get` is the root external-context primitive. It progressively expands retrieval depth:

Compatibility note: if your local CLI does not yet expose `lev get`, use `lev find` as the temporary alias.

```bash
# Depth 0: current conversation/session context only
lev get "auth"

# Depth 1: include filesystem and local project artifacts
lev get "auth" --depth=fs

# Depth 2: include BD/tasks state
lev get "auth" --depth=bd

# Depth 3: include external research backends
lev get "auth" --depth=research
```

Depth order is deterministic: `context -> filesystem -> bd -> research`.

### SDK (TypeScript / JavaScript)

```ts
import { lev } from "@lev-os";

const context = await lev.get("auth middleware", { depth: "research" });
const quick = await lev.get("open epics", { depth: "bd" });
```

`lev.get(...)` is the SDK mirror of `lev get`.

### Primitive Alias Constellation

Map natural language to stable primitives:

| Primitive | CLI | SDK | Common Aliases |
|-----------|-----|-----|----------------|
| Context gather | `lev get` | `lev.get(...)` | `ls`, `read`, `search`, `find`, `lookup`, `scan`, `research`, `prior art` |
| Lifecycle route | `work` | `lev.work(...)` | `plan`, `spec`, `workflow`, `skill`, `learn` |
| Wizard clarify | `ask` / `wiz` | `lev.ask(...)` | `wizard`, `guide me`, `unstuck` |
| Validate/ops | `check` | `lev.check(...)` | `align`, `security`, `daemons`, `status` |
| Execute/close | `go` / `handoff` / `exit` | `lev.go(...)` | `do it`, `ship`, `resume`, `close` |

Alias priority:
1. Exact primitive match (`get`, `work`, `ask`, `check`, `go`)
2. Alias resolution to primitive
3. Lifecycle stage routing via `work` when ambiguous

### Protocol Handlers

```bash
# lev:// protocol (kernel-level)
lev://get?query=auth&depth=fs&scope=code
# legacy alias:
lev://find?query=auth&scope=code
lev://exec?epic=clawd-h2qg
lev://lifecycle?from=captured&to=crystallizing
lev://research?depth=deep&topic=authentication
lev://align?check=north-star

# skill:// protocol (syscall-level)
skill://lev-research?depth=deep
skill://planning?mode=team

# flowmind:// protocol (scheduler-level)
flowmind://entity-lifecycle?state=captured

# workshop:// protocol (plugin-level)
workshop://intake/github
workshop://intake/youtube

# timetravel:// protocol (plugin-level)
timetravel://pattern/decision-making
```

---

## Responsibility Boundary

Use this split to avoid CLI/workflow overlap.

- `lev` owns intent parsing, protocol dispatch, and routing to specialist skills.
- `lev` does not own lifecycle artifact schemas (`report`, `proposal`, `spec`, `handoff`).
- `work` owns lifecycle stage detection and artifact generation contracts.
- `lev-builder` owns build/migrate flows (POC → production placement and validation).

If a request asks for session continuity output (`handoff`, checkpoints, compact), `lev` routes to `work` manifesting behavior instead of embedding format logic here.

Single-source command matrix (CLI ↔ lifecycle FSM ↔ schema handlers):
- `~/.agents/skills/work/references/command-matrix.md`

### Router Precedence

Use deterministic precedence when intents overlap:

1. `lev` resolves command aliases and primitive intent (`get`, `work`, `ask`, `check`, `go`).
2. `work` owns lifecycle-stage classification and artifact contracts.
3. `workflow` handles explicit workflow management (`list`, `create`, `run`), not lifecycle routing.
4. Application-level extensions remain outside core CLI/SDK primitive ownership and should route via their own clients.

Tie-break rules:
- If request includes lifecycle + artifact intent (`spec`, `handoff`, `manifest`, `resume`) -> route to `work`.
- If request includes explicit `/workflow` operations -> route to `workflow`.
- If request is pure context retrieval -> route to `get`.

---

## Workflows

### Workflow 1: Entity Lifecycle Routing

**Use case:** User makes a request, lev routes to appropriate lifecycle stage

**Steps:**
1. Parse user request for keywords
2. Detect lifecycle stage (ephemeral → manifesting)
3. Route to appropriate sub-skill
4. Generate lifecycle-appropriate artifact

**Example:**
```bash
# User: "Research authentication patterns"
lev "research authentication patterns"
  ↓ keyword: "research"
  ↓ stage: captured
  ↓ route: lev-research
  ↓ output: .lev/pm/reports/auth-patterns-2026-01-28.md
```

**Routing Table:**

| Keywords | Lifecycle Stage | Route To | Output Artifact |
|----------|----------------|----------|-----------------|
| "get", "find", "search", "lookup", "ls", "read", "scan" | captured | `lev get` | Inline context bundle |
| "research", "analyze", "prior art" | captured | `lev get --depth=research` | `report.md` |
| "design", "propose", "architect" | crystallizing | `lev-cdo` | `proposal.md` |
| "plan", "spec", "implement" | crystallized | `work` | `spec.md` |
| "execute", "do it" | manifesting | `bd` | Task execution |
| "align", "check", "drift", "north star" | any | `work` (alignment gate) | Validation notes |
| "security", "scan" | any | `work` (security gate) | Security findings |
| "daemon", "daemons", "status" | any | `lev-core` | Runtime status |
| "lifecycle", "state" | any | `lev-lifecycle` | State query |
| "workshop", "intake" | ephemeral | `lev-workshop` | Workshop artifact |
| "work" | auto-detect | `work` | Stage-appropriate artifact |
| "handoff", "checkpoint", "session compact", "resume context" | manifesting | `work` | `handoff.md` |
| "learn", "improve" | any | `lev-learn` | Proposal |
| "build", "create skill" | crystallizing | `lev-builder` | Skill scaffold |
| "test", "validate" | any | `lev-test` | Test results |
| "index", "reindex" | any | `lev-index` | Index status |
| "ultra", "deep dive" | captured | `lev-ultra` | Ultra-deep analysis |

---

### Workflow 2: Protocol Handler Resolution

**Use case:** Prompt contains lev:// or skill:// reference, needs context injection

**Steps:**
1. Intercept protocol URIs in prompt (syscall pattern)
2. Resolve to skill or kernel function
3. Inject context at runtime
4. Execute with injected context

**Example:**
```bash
# Prompt: "Research auth using skill://lev-research and lev://get?query=auth"
  ↓ [syscall interception]
  ↓ skill://lev-research → resolve to ~/.claude/skills/lev-research/
  ↓ lev://get?query=auth → execute lev get with progressive depth
  ↓ [kernel mode: inject contexts]
  ↓ Return to user space with loaded contexts
```

**Protocol Resolution Table:**

| Protocol | Resolves To | Example | Handler |
|----------|-------------|---------|---------|
| `lev://get` | lev.get primitive (`lev-find` + `lev-research`) | `lev://get?query=auth&depth=bd` | Progressive context gather |
| `lev://find` | Legacy alias to `lev://get` | `lev://find?query=auth&scope=code` | Alias |
| `lev://exec` | bd execution | `lev://exec?epic=clawd-h2qg` | Task runner |
| `lev://lifecycle` | lev-lifecycle skill | `lev://lifecycle?from=captured&to=crystallizing` | State machine |
| `lev://research` | lev-research skill | `lev://research?depth=deep&topic=auth` | Research orchestrator |
| `lev://align` | work alignment gate | `lev://align?check=north-star` | Alignment validator |
| `skill://{name}` | Skill loader | `skill://planning?mode=team` | Skill registry |
| `flowmind://{path}` | FlowMind scheduler | `flowmind://entity-lifecycle?state=captured` | Compiler/runtime |
| `workshop://{plugin}` | Workshop plugin | `workshop://intake/github` | Plugin loader |
| `timetravel://{pattern}` | Research pattern | `timetravel://pattern/decision-making` | Pattern library |

---

### Workflow 3: FSM State Transition

**Use case:** Move entity through lifecycle stages

**Steps:**
1. Determine current state
2. Validate transition (gates)
3. Execute transition
4. Generate next artifact

**Example:**
```bash
# Transition: captured → crystallizing
lev://lifecycle?from=captured&to=crystallizing
  ↓ current: .lev/pm/reports/auth-analysis.md
  ↓ gate: prior_art_check
  ↓ transition: design phase
  ↓ output: .lev/pm/proposals/auth-solution.md
```

**FSM State Machine:**

```
ephemeral → captured → classified → crystallizing → crystallized → manifesting → completed
    ↓           ↓          ↓             ↓               ↓             ↓            ↓
 [inline]   [report]   [typed]       [proposal]      [spec]      [handoff]    [archive]
                                 ↘ discarded
```

**State Transition Gates:**

| Transition | Gate | Check |
|------------|------|-------|
| ephemeral → captured | None | Auto-transition on research request |
| captured → classified | intent_classification | classify entity + route ownership |
| classified → crystallizing | prior_art_check | Search BD, docs, skills for existing work |
| crystallizing → crystallized | dor_check, alignment_check | DoR complete, aligns with north star |
| crystallized → manifesting | validation_suite | Spec approved, tasks ready |
| manifesting → completed | done_state | All criteria met |
| crystallizing → discarded | rejection_gate | reject/park invalid proposals with tombstone |

---

## Relates (Cross-References)

### Sub-Skills (Routes To)

#### Core 12 Sub-Skills

1. **`skill://lev-find`** - Unified search backend for `lev get` (legacy skill name)
   - Semantic search across codebase, docs, sessions, tasks, memory
   - RRF fusion across indexes
   - Use for: context gathering, prior art checks, discovery

2. **`skill://lev-research`** - Deep research (ANALYZE)
   - Multi-perspective orchestrated discovery
   - Query expansion, cross-validation
   - Use for: complex topics, architecture exploration, gap analysis

3. **`skill://lev-index`** - Code/doc indexing
   - Maintain search indexes
   - Reindex on changes
   - Use for: index health, rebuilds

4. **`skill://lev-cdo`** - Graph thinking (THINK)
   - Agentic orchestration
   - Classification → routing → execution
   - Use for: strategic design, multi-agent workflows

5. **`skill://lev-ultra`** - Ultra-deep analysis
   - Deepest level research
   - Comprehensive exploration
   - Use for: complex problem spaces requiring exhaustive analysis

6. **`skill://lev-align`** - Legacy standalone alignment audit
   - Default behavior: alignment runs inside `work` ALIGN gate
   - Use standalone only for explicit drift-audit deep dives

7. **`skill://lev-test`** - Testing validation
   - Test suite execution
   - Validation gates
   - Use for: quality checks, test results

8. **`skill://lev-lifecycle`** - Entity lifecycle management
   - State machine orchestration
   - Idea/session/synth lifecycles
   - Use for: state transitions, entity queries

9. **`skill://work`** - Unified lifecycle router
   - Auto-detects lifecycle stage
   - Routes to specialist skills
   - Use for: ANY work request (auto-routing)

10. **`skill://lev-learn`** - Pattern analysis & proposals
    - Event analysis
    - Improvement proposals
    - Use for: learning from patterns, evolution

11. **`skill://lev-builder`** - Skill builder
    - Scaffold new skills
    - Skill structure generation
    - Use for: creating new skills

12. **`skill://lev-workshop`** - Workshop lifecycle
    - Intake → analysis → poc → poly
    - Plugin development
    - Use for: building new lev components

#### Additional Sub-Skills

- **`skill://lev-clwd`** - Clawdbot operations (daemon, gateway, voice)
- **`skill://lev-intake`** - Task intake workflows
- **`skill://lev-skill-builder`** - Skill construction
- **`skill://lev-computer-use`** - Computer use integration

### Protocol Handlers
- `lev://get` → lev.get primitive
- `lev://find` → legacy alias to lev://get
- `lev://exec` → bd execution engine
- `lev://lifecycle` → lev-lifecycle state machine
- `lev://research` → lev-research orchestrator
- `lev://align` → work alignment gate

### Lifecycle Artifacts
- Reports (captured) → proposals (crystallizing)
- Proposals (crystallizing) → specs (crystallized)
- Specs (crystallized) → handoffs (manifesting)
- Handoffs (manifesting) → archive (completed)

### Constitutional References
- Handoffs: "Load lev to resume work"
- Proposals: "Use lev to convert to spec"
- Specs: "Execute via lev://exec"
- Reports: "Design solution with lev"

---

## Validation Gates

### Entry Gate (Before Route)
- [ ] Request parsed successfully
- [ ] Keywords detected
- [ ] Lifecycle stage determined
- [ ] Sub-skill available

### Transition Gates (Between States)

**captured → crystallizing:**
- [ ] Prior art check complete (BD, docs, skills)
- [ ] No duplicate work found OR justified
- [ ] Research findings documented

**crystallizing → crystallized:**
- [ ] DoR validation complete
- [ ] Alignment check passed (`work` alignment gate)
- [ ] Design approved

**crystallized → manifesting:**
- [ ] Validation suite passed
- [ ] Spec approved
- [ ] Tasks created (if BD available)

**manifesting → completed:**
- [ ] Done state criteria met
- [ ] All tasks closed
- [ ] Artifacts archived

### Exit Gate (After Execution)
- [ ] Artifact generated
- [ ] Lifecycle position updated
- [ ] Next actions documented
- [ ] Plankton reference included

---

## Plankton Action Directives

**In templates, always include:**

### Handoffs
```markdown
## Next Steps
Load lev to resume work:
- Continue context gathering: `lev://get?query={topic}&depth=research`
- Design solution: `lev://lifecycle?from=captured&to=crystallizing`
- Execute spec: `lev://exec?epic={bd_epic_id}`
```

### Proposals
```markdown
## Next Steps
Use lev to advance this proposal:
- Create spec: `lev://lifecycle?from=crystallizing&to=crystallized`
- Validate alignment: `skill://work`
- Research alternatives: `lev://research?depth=deep&topic={topic}`
```

### Specs
```markdown
## Execution
Execute this spec:
- Scaffold epic: `lev://exec?spec=spec.md`
- Team mode: `lev://exec?epic={bd_epic_id}`
- Track progress: `skill://bd`
```

### Reports
```markdown
## Next Steps
Design solution from findings:
- Propose: `lev://lifecycle?from=captured&to=crystallizing`
- Research more: `lev://get?query={topic}&depth=research`
- Deep dive: `lev://research?depth=deep&topic={topic}`
```

---

## Sub-Skills Reference

Each sub-skill has its own SKILL.md with full detail. Lev acts as router.

```
lev/
├── SKILL.md                  # This file (router + plankton)
├── lev-find/
│   └── SKILL.md              # Search operations
├── lev-research/
│   └── SKILL.md              # Deep research workflows
├── lev-cdo/
│   └── SKILL.md              # Graph thinking
├── lev-lifecycle/
│   └── SKILL.md              # Entity lifecycle FSM
├── work/
│   └── SKILL.md              # Unified lifecycle router
├── lev-align/
│   └── SKILL.md              # Strategic alignment
├── lev-learn/
│   └── SKILL.md              # Pattern analysis
├── lev-builder/
│   └── SKILL.md              # Skill scaffolding
├── lev-workshop/
│   └── SKILL.md              # Workshop lifecycle
├── lev-ultra/
│   └── SKILL.md              # Ultra-deep analysis
├── lev-test/
│   └── SKILL.md              # Testing validation
├── lev-index/
│   └── SKILL.md              # Index management
├── lev-clwd/
│   └── SKILL.md              # Clawdbot operations
└── [other sub-skills...]
```

**Router decision logic:**
- If request is simple context gather → `lev get`
- If request needs deep analysis → lev-research
- If request needs design thinking → lev-cdo
- If request is execution → bd via work skill
- If request is ambiguous → work skill (auto-routes)
- If request mentions lifecycle → lev-lifecycle
- If request about alignment/security checks → work
- If request about building skills → lev-builder
- If request about workshop/intake → lev-workshop

---

## Usage Examples

### Example 1: Simple Get
```bash
lev get "authentication middleware"
  ↓ keyword: "get"
  ↓ route: lev.get primitive
  ↓ execute: progressive context gather
  ↓ output: inline results
```

### Example 2: Deep Research
```bash
lev "research microservices architecture patterns"
  ↓ keyword: "research"
  ↓ route: lev-research
  ↓ execute: multi-perspective discovery
  ↓ output: .lev/pm/reports/microservices-analysis-2026-01-28.md
```

### Example 3: Design Work
```bash
lev "design a solution for user authentication"
  ↓ keyword: "design"
  ↓ stage: crystallizing
  ↓ route: lev-cdo
  ↓ execute: strategic planning
  ↓ output: .lev/pm/proposals/auth-solution-2026-01-28.md
```

### Example 4: Spec Authoring
```bash
lev "spec implementation behavior for auth system"
  ↓ keyword: "spec"
  ↓ stage: crystallized
  ↓ route: work
  ↓ execute: DoR-enforced spec generation
  ↓ output: .lev/pm/specs/auth-implementation-2026-01-28.md
```

### Example 5: Lifecycle Transition
```bash
lev "transition idea-001 from captured to crystallizing"
  ↓ keyword: "lifecycle", "transition"
  ↓ route: lev-lifecycle
  ↓ execute: state machine transition
  ↓ output: state updated, proposal generated
```

### Example 6: Alignment Check
```bash
lev "check if current work aligns with north star"
  ↓ keyword: "align", "north star"
  ↓ route: work (alignment gate)
  ↓ execute: drift detection + lifecycle validation
  ↓ output: alignment report
```

### Example 7: Auto-Routed Work
```bash
lev "analyze test coverage and propose improvements"
  ↓ keyword: "analyze", "propose"
  ↓ ambiguous stage
  ↓ route: work (auto-detect)
  ↓ work determines: captured (research) → crystallizing (design)
  ↓ output: report.md + proposal.md
```

---

## Integration Points

### With Entity Lifecycle
- Maps FSM states to appropriate sub-skills
- Generates lifecycle-appropriate artifacts
- Validates state transitions via gates

### With BD (Beads)
- Links specs to BD epics
- Tracks tasks via BD CLI
- Routes execution through BD

### With FlowMind
- Supports flowmind:// protocol handlers
- Integrates with compiler/runtime
- Enables YAML-first behavior

### With Workshop
- Routes intake requests to workshop plugins
- Supports workshop:// protocol
- Manages poc → poly transitions

### With Team Mode
- Delegates to planning skill for team decomposition
- Coordinates multi-agent workflows
- Tracks teammate assignments

---

## Principles

1. **Single Entry Point** - All lev operations start here
2. **Progressive Disclosure** - Start simple, route to specialists as needed
3. **Lifecycle Awareness** - Route based on entity state
4. **Protocol Driven** - Support URI-based invocation
5. **Plankton Behavior** - Always include action directives
6. **Constitutional** - Define core patterns, don't re-implement

---

**Plankton status:** ✅ ACTIVE
**Constitutional:** ✅ YES
**Always reference:** In all lifecycle artifacts with action directives

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
You are the prompt-architect-enhanced specialist for lev, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

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
