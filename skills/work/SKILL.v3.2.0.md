---
name: work
description: Unified lifecycle/process router. Concurrent FSM that discovers context, runs embedded alignment checks, researches, proposes, specs behavior, and routes to specialist skills. Guard scoring is constant, not gated. Artifacts are spec-first.
version: 3.2.0
extends: []
related_skills:
  - lev-research
  - lev-cdo
  - ux
  - lev-learn
  - workflow
  - lev-portable
  - br
  - bd
  - td
skill_type: workflow
category: process-lifecycle
primitive_owner: work
tools:
  - lev CLI
  - tracker CLI (br | bd | td)
  - cm CLI
  - cass CLI
  - skill-discovery CLI
  - jq
storage:
  beads: .beads/
  custom_types:
    report: "custom:report"
    proposal: "custom:proposal"
    spec: "custom:spec"
    system: "custom:system"
    learning: "custom:learning"
---

# Work: FSM Lifecycle Router (v3)

**One entry point for all work.** Concurrent FSM with PLANNING and EXECUTION phases. Guard scoring runs constantly (not as a gate). DISCOVER runs interview, memory prefetch, prior art, and search concurrently. All artifacts stored as beads custom types.

```
                       PLANNING PHASE                                               EXECUTION PHASE
  ┌───────────────────┐   ┌───────┐   ┌──────────┐   ┌─────────┐   ┌──────┐   ┌─────────┐   ┌──────────┐   ┌──────┐   ┌───────┐
  │     DISCOVER      │──▶│ ALIGN │──▶│ RESEARCH │──▶│ PROPOSE │──▶│ SPEC │──▶│ EXECUTE │──▶│ VALIDATE │──▶│ EMIT │──▶│ LEARN │
  │   (concurrent)    │   └───────┘   └──────────┘   └─────────┘   └──────┘   └─────────┘   └──────────┘   └──────┘   └───────┘
  │                   │    north star   deeper code    CDO graph     BDD +      spawn         layer-dep      close      cm outcome
  │ ┌──────────────┐  │   ALIGN gate    analysis       5-role        contracts  team/agents   strictness     bead       cm reflect
  │ │ Interview(fg)│  │    classify     C1-C4 map      think         accept.    inline        gates          update     br learning
  │ │ PriorArt(bg) │  │    layers       DoR compl.     proposal      criteria   cm add                      status     cass index
  │ │ Search  (bg) │  │    alignment                   bead                    (learn)
  │ └──────────────┘  │    verdict
  │                   │
  │ ╔════════════════╗│    Guard is NOT a step -- it scores 6 categories every turn.
  │ ║ GUARD(constant)║│    <=30% -> PASS | 30-60% -> ASK inline | >60% -> interview skill
  │ ╚════════════════╝│
  └───────────────────┘
```

---

## Task Tracker Adapter (bd | br | td)

The work skill is backend-agnostic for task tracking. Detect which tool is available and route through the adapter. **Preference order: bd > br > td.**

### Detection

```bash
# Prefer bd (Go, auto-commit) > br (Rust, non-invasive) > td (Python, lightweight)
command -v bd && TRACKER=bd || { command -v br && TRACKER=br || { command -v td && TRACKER=td || TRACKER=none; }; }
```

### Operation Map

| Operation | bd (preferred) | br (supported) | td (lightweight) |
|-----------|---------------|-------------|------------------|
| **create** | `bd create --title="..." --type=task` | `br create --title="..." --type=task` | `td add "..."` |
| **list** | `bd list --status=open` | `br list --status=open` | `td` / `td -g {group}` |
| **search** | `bd search "{kw}"` | `br search "{kw}"` | N/A (grep local) |
| **show** | `bd show {id}` | `br show {id}` | `td {id}` |
| **update** | `bd update {id} --status=X` | `br update {id} --status=X` | `td {id} edit` |
| **close** | `bd close {id}` | `br close {id}` | `td {id} complete` |
| **deps** | `bd dep add {p} {c}` | `br dep add {p} {c}` | N/A |
| **ready** | `bd ready` | `br ready` | N/A |
| **sync** | `bd sync` (auto-git) | `br sync --flush-only` + manual git | N/A (local SQLite) |
| **epic** | `bd epic {id}` | `br epic {id}` | N/A (use groups: `td -g {epic}`) |

### Behavioral Differences

- **bd sync** auto-commits and pushes — no manual git needed
- **br sync** exports JSONL only — you must `git add .beads/ && git commit` manually
- **td** has no sync/deps/ready — degrade gracefully (skip dep gates, no ready filtering)

### Degradation Rules

When `td` is the only backend:
- Skip dependency-based gates (no `dep` support)
- Skip `ready` filtering (list all open instead)
- Map groups to epics (`td -g {epic-name}`)
- Search falls back to `td` + grep

When no tracker is available (`TRACKER=none`):
- Continue without task integration; note in artifact
- Prior art check skips BD/tracker queries

---

## Responsibility Boundary

- `lev` owns CLI/protocol routing only.
- `work` owns lifecycle-stage logic and artifact contracts.
- `lev-builder` owns build/migrate execution patterns.

Do not place artifact-format instructions in command shims. Keep format contracts in this skill and its templates.

---

## Entity Lifecycle (7 States + Discarded Branch)

```
ephemeral → captured → classified → crystallizing → crystallized → manifesting → completed
    ↓           ↓          ↓             ↓               ↓              ↓            ↓
 [none]    [report     [report +     [proposal       [spec          [handoff     [archive
            bead]      alignment]     bead]           bead]          bead]        bead]
                                       ↘ discarded
```

| Stage | Bead Type | Sub-Skills | Keywords |
|-------|-----------|-----------|----------|
| **ephemeral** | None (brainstorm) | Inline | "explore", "brainstorm", "understand" |
| **captured** | `custom:report` | `lev get`, `lev-research` | "get", "research", "analyze", "scan", "find", "lookup", "read", "ls" |
| **classified** | `custom:report` + alignment | `work` ALIGN gate, `lev-portable` | "classify", "align", "categorize" |
| **crystallizing** | `custom:proposal` | `lev-cdo`, `lev-learn`, `thinking-parliament` | "design", "propose", "architect", "learn", "guide me" |
| **crystallized** | `custom:spec` | `planning`, tracker | "plan", "implement", "specify" |
| **manifesting** | handoff bead | Team coordination, tracker | "working on", "in progress" |
| **completed** | archive bead | `lev-lifecycle` | "done", "finished", "closed" |
| **discarded** | tombstone link | `work` guard + validation | "discard", "drop", "reject" |

Learning artifacts are created post-completion by LEARN, but `custom:learning` is not a lifecycle state.
All artifacts are stored as beads custom types (not files on disk). A hook generates markdown views from beads for human readability.

---

## Shortcuts

| Key | Action | Route |
|-----|--------|-------|
| `(l)` | Start learn interview | `learn [context]` |
| `(p)` | Start proposal | `work --stage=crystallizing` |
| `(u)` | Show update diff | `work --stage=update` |
| `(s)` | Browse skills | skills-db query (inline) |
| `(d)` | Design/UX hub | `ux` hub |

---

## Operational Command Constellation

These are agent <-> human operational commands and aliases. Map them to root primitives, not ad-hoc flows.

Canonical source for CLI alias + FSM stage + schema handler mapping:
- `~/.agents/skills/work/references/command-matrix.md`

| Command / Alias | Primitive | Route | Notes |
|-----------------|-----------|-------|-------|
| `work` | lifecycle | `work` | DISCOVER -> ALIGN -> route |
| `plan` | crystallized-intent | `work` -> SPEC | Legacy alias normalized to spec output |
| `spec` | crystallized | `work` -> SPEC | Primary crystallized artifact |
| `propose` | proposal | `work` -> PROPOSE | CDO graph deliberation |
| `tracker` | execution tracking | tracker (br/bd/td) | Task graph + status |
| `check` | validation | `work` VALIDATE | Alignment, DoR, drift |
| `go` | execute | `work` -> EXECUTE | Start manifesting |
| `handoff` | continuity | `work` EMIT | Canonical checkpoint output |
| `exit` | session close | `work` EMIT -> LEARN | Emit handoff + learn ceremony |
| `learn` | guided intake | `lev-learn` via DISCOVER | Interview loop (foreground track) |
| `align` | alignment | `work` -> ALIGN gate | North star check, drift detection |
| `workflow` | workflow mgmt | `workflow` | List/create/run workflow skills |
| `skill` | skill ops | `skill-builder` or skill lookup | Build/discover/install path |
| `ask`, `wiz` | wizard mode | `interview` via DISCOVER | Guard >60% routes here automatically |
| `scan`, `security` | assurance | `work` VALIDATE | Can route to specialist security skills |
| `daemon`, `daemons` | runtime ops | `lev-core` | Operational status/health |
| `reflect` | learning | `work` LEARN | cm reflect + learnings bead |

### External Context Primitive

Use `lev get` as the root external context-gathering primitive.

Compatibility note: if `lev get` is not available in the current CLI build, use `lev find` as a temporary alias.

Aliases that resolve here:
- `ls`, `read`, `search`, `find`, `lookup`, `scan`, `research`, `prior art`

Progressive depth:
- `context` -> current conversation/workspace state
- `fs` -> filesystem and local artifacts
- `tracker` -> task graph and open work (br/bd/td)
- `beads` -> bead search (br search, cass search)
- `research` -> external sources

---

## Quick-Keyword Artifact/Action Glossary

| Keyword(s) | Stage | Bead Type | Action |
|------------|-------|-----------|--------|
| "get", "research", "analyze", "scan", "find", "lookup", "read", "ls" | captured | `custom:report` | DISCOVER -> `lev get` (or `lev-research` for deep mode) |
| "align", "north star", "drift", "classify" | classified | `custom:report` | ALIGN gate (embedded) |
| "design", "propose", "architect" | crystallizing | `custom:proposal` | PROPOSE -> `lev-cdo` + 5-role Think |
| "learn", "guide me", "unstuck" | crystallizing | `custom:proposal` | DISCOVER interview track -> PROPOSE |
| "plan", "implement", "specify" | crystallized | `custom:spec` | SPEC -> `planning` + tracker |
| "working on", "in progress", "handoff", "exit" | manifesting | handoff bead | EXECUTE -> EMIT |
| "done", "finished", "closed" | completed | archive bead | EMIT -> LEARN -> `lev-lifecycle` |
| "reflect", "learnings", "retro" | completed (post-close) | `custom:learning` | LEARN -> `cm reflect` + `br create` |

---

## FSM States: PLANNING PHASE

### DISCOVER -- Concurrent Context Gathering

DISCOVER is the entry point. It runs four tracks concurrently with a constant guard scoring function. All results save to `custom:report` beads.

```
/work "{idea}"
    │
    ▼
DISCOVER (concurrent, not sequential)
├── Interview (foreground)
│   └── Ask user questions, rolling bg research per question
├── Memory Prefetch (background)
│   └── cm context + cass search (workspace-first, global fallback)
├── Prior Art (background)
│   └── br search, lev get, cass search, tracker list
├── Search (background)
│   └── Codebase grep, online search, skill discovery
└── Guard (constant -- runs every turn, not a pre-step)
    ├── Score 6 categories: Objective, Scope, Constraints, Environment,
    │   Dependencies, Success Criteria
    ├── Each scored: MISSING (full weight) | PARTIAL (half) | PRESENT (0)
    ├── Weights: Objective (20%), Scope (20%), Constraints (15%),
    │   Environment (15%), Dependencies (15%), Success Criteria (15%)
    │
    ├── Score <=30%  -> PASS (sufficient, advance to ALIGN)
    ├── Score 30-60% -> ASK (structured questions inline)
    └── Score >60%   -> route to interview skill (wizard-mode)
```

**Confidence formula:**

```
base_confidence = 1.0 - (guard_score / 100)
layer_modifier: Site/Structure -0.1, Skin/Services +0.0, Space +0.05, Stuff +0.1
think_modifier: agreement >80% +0.1, 50-80% +0.0, <50% -0.1
final = base + layer_modifier + think_modifier
```

**Memory prefetch** runs as part of DISCOVER before heavy research fan-out:

| Step | Command | Policy |
|------|---------|--------|
| Procedural recall | `cm context "{kw}" --workspace "$PWD" --limit 3 --history 1 --json` | Workspace-first |
| Episodic recall | `cass search "{kw}" --workspace "$PWD" --json --limit 5 --max-content-length 180` | Workspace-first |
| Global fallback | retry without `--workspace` only if low-signal workspace hits | Fail-open |
| Injection budget | summarize to short bullets with provenance links | Keep compact |

Low-signal criteria (default): generic prompt, zero thinking signal, empty/weak workspace hits.

**Skill discovery** runs as part of the Search background track:

| Priority | Source | Path |
|----------|--------|------|
| 1 | Project-local skills | `.claude/skills/`, `.agents/skills/` in project |
| 2 | Global canonical skills | `~/.agents/skills/` |
| 3 | Skills DB | `~/.agents/skills-db/` (use `/skill find` or `grep`) |
| 4 | POC skills | `~/lev/workshop/poc/skills/` |
| 5 | Polymath skills | `~/lev/workshop/intake/cc-polymath/skills/` |

**Lookup Tool:** Use the `/skill` command shim if available, or `grep -r "{kw}" ~/.agents/skills-db/` directly.

**Prior art search** runs as part of the PriorArt background track:

| Source | Search Method |
|--------|--------------|
| Beads | `br search "{kw}"` ; `br list --label-any "{kw}"` |
| Tracker tasks | `$TRACKER list --status=open \| grep -i "{kw}"` ; `$TRACKER search "{kw}"` |
| Codebase & docs | `lev get "{kw}" --scope=all --depth=research` |
| CASS index | `cass search "{kw}" --robot --limit 10` |
| Existing skills | `lev get "{kw}" --scope=knowledge --depth=fs --pattern="SKILL.md"` |

**If substantial prior art found**, present findings and ask:
1. Review existing work?
2. Extend existing work?
3. Proceed with new work anyway?

**Flexible ordering:** Steps have dependency gates, not fixed sequence. If prior art returns empty fast, skip ahead. If interview reveals complexity, loop back. Guard score dropping below 30% unblocks ALIGN regardless of other tracks.

**Skip guard when:** Explicit file paths provided, multi-turn context established, `--no-guard` flag, or resuming from saved session.

**Output:** `custom:report` beads with discovery results, guard scores, and skill manifest.

### ALIGN -- North Star Alignment

Check project alignment before deeper work. This is an embedded `work` gate. Use `lev-align` only for standalone deep-dive audits.

```
ALIGN:
├── North star exists?
│   ├── YES -> Compare current state to north star
│   │   └── Drift type? (Stale Docs | Product Pivot | Coverage Gap | Status Drift | Path Drift)
│   └── NO -> Deep research codebase -> define north star -> save as custom:system bead
├── Classify layers (lev-portable):
│   ├── Stewart Brand shearing layers: Site | Structure | Skin | Services | Space Plan | Stuff
│   ├── Depth: L0 (overview) -> L1 (structure) -> L2 (details) -> L3 (runtime)
│   └── Persistence: System graph (permanent) vs CDO graph (ephemeral)
└── Output: alignment verdict (aligned | drift | gap)
```

| Layer | Timescale | Risk | Examples |
|-------|-----------|------|----------|
| Site | Decades | High | DB schema, core model |
| Structure | 30-50y | High | Auth, API contracts |
| Skin | 20y | Medium | UI framework, design system |
| Services | 7-15y | Medium | CI/CD, monitoring |
| Space Plan | 3-7y | Lower | Routes, features |
| Stuff | Daily | Lowest | Copy, env vars |

**If no alignment data exists**, create a `custom:system` bead to capture project context:

```bash
br create "System: {project}" \
  --type '{"custom":"system"}' \
  --labels "system,alignment,{project}" \
  --description "{north star + context}"
```

**Execution tiers** (determined by layer classification):

| Classification | Tier | Pattern |
|---|---|---|
| Stuff + L3 + CDO | Direct | Just do it |
| Space Plan + L2 | Brief | 5-bullet spec -> execute |
| Skin/Services + L1-L2 | Standard | Plan -> execute -> review |
| Structure + L1 | Deliberate | Proposal -> approval -> execute -> review |
| Site + L0-L1 | Formal | Proposal -> approval -> phases -> multi-gate review |

### RESEARCH -- Deep Analysis

Deeper investigation informed by DISCOVER results and ALIGN verdict. Runs only when the task warrants it (skipped for Stuff/Space Plan tier).

| Activity | Method | Output |
|----------|--------|--------|
| Code analysis | Read files, trace dependencies | Understanding of current state |
| Content review | Review prior art beads | Context for proposal |
| Design review | Architecture patterns, anti-patterns | Alignment assessment |
| C1-C4 mapping | Site/Structure layer analysis | Impact assessment |
| DoR completion | Fill remaining guard categories | Ready for PROPOSE |

**Save to:** `custom:report` beads with research findings.

**Skip when:** Guard score <=30% at DISCOVER exit AND layer is Stuff/Space Plan (tier Direct or Brief).

### PROPOSE -- Solution Design

Draft a proposal using CDO graph deliberation. Uses 5-role Think (from lev-portable).

```
PROPOSE:
├── Think deliberation (5 roles, layer-weighted):
│   ├── Advocate, Critic, Systems Thinker, Pragmatist, Wild Card
│   ├── Layer weighting: Site/Structure -> heavy Critic + Systems Thinker
│   │                    Stuff -> heavy Pragmatist + Wild Card
│   ├── Devil's advocate trigger when >70% agreement
│   └── Light mode (>=0.80 confidence): Advocate + Critic only
├── Draft proposal -> custom:proposal bead
├── If ephemeral -> inline response (still stored in beads)
├── If prior art exists -> extend, don't duplicate
├── Surface discovered skills:
│   ├── Pull skill manifest from DISCOVER Search track report bead
│   ├── If design/UX keywords detected -> propose loading `ux` hub
│   ├── Query skills-db: lev-skill resolve "{topic}" --json | jq '.results[:5]'
│   └── Include in dashboard footer (inline, does NOT block FSM)
```

**Save to:** `custom:proposal` bead.

```bash
br create "Proposal: {topic}" \
  --type '{"custom":"proposal"}' \
  --labels "proposal,{layer},{domain}" \
  --description "{proposal content}"
```

**Team structure** (determined here, not in a separate PLAN step):

| Complexity | Signals | Strategy | Tool |
|-----------|---------|----------|------|
| Simple | Single file, one skill | Direct execution | None |
| Medium | 2-3 files, multiple skills | Parallel subagents | Task tool, 2-4 agents |
| Complex | Multi-file, cross-cutting | Formal team | TeamCreate + Task tool |

### SPEC -- Behavioral Specification

Crystallize the proposal into an actionable spec with BDD scenarios and contracts.

**Save to:** `custom:spec` bead. Break into epics + tasks in BD.

```bash
br create "Spec: {topic}" \
  --type '{"custom":"spec"}' \
  --labels "spec,{layer},{domain}" \
  --description "{spec content with BDD scenarios}"
```

**Spec must include:** BDD scenarios (Given/When/Then), contracts, acceptance criteria, team structure, and workstream assignments. See VALIDATE gates for full requirements.

#### PROPOSE Dashboard Footer

Every PROPOSE output ends with a structured footer. This is a display convention (not a gate). The agent renders it as markdown; the user responds with a number or letter shortcut.

```
---
🔨 **Work:** {stage} | 🎯 {layer} | 📊 Guard: {score}%

**Skills loaded:** {loaded_list}
**Available:** {available_count} more via skills-db

🪄 **Next:**
1. [s] Skills — browse/load from skills-db
2. [r] Research — deepen with lev-research
3. [p] Prior art — review beads and artifacts
4. Proceed to SPEC
5. All of the above
6. ⬅️ Back to DISCOVER

#### SPEC Promotion Path

When a spec passes validation (`gate:propose-spec`) and template questions are answered, the agent must identify the promotion target:

1. **Start:** `.lev/pm/specs/spec-{topic}.md` (Ephemeral Draft)
2. **Review:** Gate passes.
3. **Promote:** Move to `docs/specs/spec-{module}.md` (Canonical)
   - If module exists: Update existing spec.
   - If new module: Create new spec file.
   - Naming: Use `spec-{module}.md` for core, `spec-{module}-{slug}.md` for extensions.

#### FlowMind Naming Structure & Config Keys

The `work` skill recognizes specific configuration keys for identifying specs and promoting them:

| Key | Value Pattern | Purpose |
|-----|---------------|---------|
| `naming_structure` | `flowmind` | Enforce `spec-{module}.md` naming |
| `filename_mask` | `core-*-mask` | Regex for validating core filenames |
| `spec_target` | `docs/specs/` | Target directory for promotion |

Example Config (`.lev/config.yaml`):
```yaml
work:
  naming_structure: flowmind
  filename_mask: "spec-.*\\.md"
  spec_target: "docs/specs/"
```
---
```

Shortcut behavior:
- [s] -> lev-skill resolve "{topic}" --json, present results, offer to cat SKILL.md
- [r] -> route to lev-research with current context
- [p] -> br search "{topic}" + cass search "{topic}"

---

## FSM States: EXECUTION PHASE

> **Note:** ROUTE and MANIFESTING are sub-operations within the EXECUTION PHASE, not distinct FSM states. The FSM states are the 7 states (+ discarded branch) in the diagram above. ROUTE selects which skill to invoke; MANIFESTING describes the handoff contract format.

### ROUTE -- Sub-Skill Routing

| Stage | Primary Skill | Secondary Skills | When |
|-------|--------------|------------------|------|
| **ephemeral** | None | `thinking-parliament` | Meta questions only |
| **captured** | `lev get` | `lev-research`, `deep-research` | Progressive context gathering |
| **captured** | `lev-research` | None | Deep research mode |
| **crystallizing** | `lev-learn` | `lev-cdo` | Guided intake when user invokes learn mode |
| **crystallizing** | `lev-cdo` | `thinking-parliament`, `work` alignment gate | Strategic design |
| **crystallizing** | `ux` | `lev-cdo`, `planning` | Product/design/UX shaping before spec |
| **crystallized** | `planning` | tracker | Spec authoring with BDD + contracts |
| **manifesting** | tracker | `lev-clwd` | Task tracking/coordination + handoff emission |
| **completed** | `lev-lifecycle` | None | Archive and summarize |

Routing logic:
- `captured` + simple query → `lev get`; deep ambiguity or broad unknowns → `lev-research`
- explicit `learn` intent or underspecified request needing guided intake → `lev-learn` (proposal + handoff)
- `crystallizing` + product/design/UX framing needed → `ux` hub (routes to design-os, pencil, or pipeline)
- `crystallizing` + needs adversarial validation → `thinking-parliament` + `lev-cdo`; else → `lev-cdo`
- `crystallized` → always `planning` (spec-authoring backend, DoR enforcement) + tracker
- `manifesting` → tracker + `lev-clwd` + mandatory handoff contract output

### MANIFESTING -- Handoff Contract (Required)

When emitting `handoff.md`, follow the checkpoint format contract below. This is the canonical handoff schema for continuity.

1. Write `3-15` checkpoints in chronological order.
2. For each checkpoint, use exactly one block type:
   - `⚡ CHECKPOINT Progress`
   - `📋 Code Context`
   - `📋 User feedback / ADR created`
3. Across checkpoints, include:
   - files worked on
   - files loaded into context
   - what was learned and why it matters
4. End with both:
   - `System Prompt for Next Agent`
   - `Context Confidence Score`
5. File location:
   - `.lev/pm/handoffs/{YYYYMMDD-HHMMSS}-{topic}.md`
6. Template source:
   - `~/.agents/skills/work/templates/handoff.md`

### EXECUTE -- Spawn Workers

Based on PROPOSE and ROUTE outputs:

1. **Direct execution:** Load matched skill inline, execute in current context
2. **Ephemeral subagents:** Spawn via Task tool with skill content injected into prompt
   - Each agent gets: task description + inlined skill content + workspace context
   - Instruct agents to return manifest of files touched + executive brief
3. **Formal team:** Create team config, spawn via TeamCreate + Task tool
   - Assign workstreams with skill-to-agent mapping
   - Set dependency ordering between workstreams

#### Inline Learning Capture

During execution, immediately capture learnings that survive context compaction:

| Trigger | Command | Category |
|---------|---------|----------|
| Bug fixed | `cm add "{description}" --category bug --json` | bug |
| Gotcha discovered | `cm add "{description}" --category {cat} --json` | architecture, testing, tooling |
| Performance issue | `cm add "{description}" --category performance --json` | performance |
| Security concern | `cm add "{description}" --category security --json` | security |

Categories: `bug`, `performance`, `architecture`, `testing`, `security`, `workflow`, `tooling`

**Why inline:** Context compaction loses session details. `cm add` persists immediately to the playbook, surviving any compaction event.

### VALIDATE -- Quality Gates

> Full per-gate definitions (layer modulation, confidence routing, failure actions): `./references/gates.md`

#### Gate Summary Matrix

| Gate | Transition | Severity | FORMAL Checks | DIRECT Checks | Confidence Skip |
|------|-----------|----------|---------------|---------------|-----------------|
| `gate:discover-align` | DISCOVER -> ALIGN | MANDATORY | 5/5 (strict) | 1/5 | >= 0.90 auto-pass |
| `gate:align-research` | ALIGN -> RESEARCH | CRITICAL | 7/7 | 2/7 | >= 0.90 skip to 3 |
| `gate:research-propose` | RESEARCH -> PROPOSE | MANDATORY | 6/6 | 1/6 | >= 0.90 skip to 1 |
| `gate:propose-spec` | PROPOSE -> SPEC | CRITICAL | 7/7 + human | 1/7 | >= 0.90 skip to 2 |
| `gate:spec-execute` | SPEC -> EXECUTE | CATASTROPHIC | 16/16 + human | 3/16 | Never fully skip |
| `gate:execute-validate` | EXECUTE -> VALIDATE | MANDATORY | 8/8 | 2/8 | >= 0.90 skip to 3 |
| `gate:validate-emit` | VALIDATE -> EMIT | CRITICAL | 10/10 + human | 1/10 | >= 0.90 layer-min |
| `gate:emit-learn` | EMIT -> LEARN | WARNING | 6/6 | 2/6 | >= 0.90 skip to 2 |

#### Confidence Routing Table

| Confidence | Gate Behavior |
|------------|---------------|
| >= 0.90 | Skip INFO + WARNING gates; execute MANDATORY+ only |
| 0.80 - 0.89 | Standard: all gates at their declared severity |
| 0.60 - 0.79 | All gates fire + deliberation mode (Think 5-role) required before PROPOSE |
| < 0.60 | All gates + extended checks + human review required before SPEC |

#### Backtracking Table

| Gate Failure | Backtrack To | Condition |
|-------------|-------------|-----------|
| `gate:discover-align` | DISCOVER | Insufficient context — re-interview or re-search |
| `gate:align-research` | ALIGN or DISCOVER | Misclassification or missing north star |
| `gate:research-propose` | RESEARCH | Insufficient depth — deepen analysis |
| `gate:propose-spec` | PROPOSE or RESEARCH | Think disagreement or alignment drift |
| `gate:spec-execute` | SPEC or PROPOSE | Missing sections or invalid contracts |
| `gate:execute-validate` | EXECUTE | Incomplete work — finish remaining items |
| `gate:validate-emit` | EXECUTE or VALIDATE | Test failures or visual validation failure |
| `gate:emit-learn` | EMIT (retry) | Write failure — never blocks LEARN |

**Max backtrack depth:** 3 consecutive failures at the same gate before escalating to human review.

#### CATASTROPHIC gate:spec-execute (Inlined — Never Skip)

The spec completeness gate has 16 checks and **cannot be degraded or bypassed** by any mechanism (confidence, layer, user override):

| # | Check | Pass Condition |
|---|-------|---------------|
| 1 | Spec bead exists | `custom:spec` bead created |
| 2 | Executive summary | Present and <= 3 paragraphs |
| 3 | Context defined | Existing state AND target state documented |
| 4 | BDD scenarios | Given/When/Then covering primary flows |
| 5 | Input/Processing/Output | I/P/O triples defined per scenario |
| 6 | Dependencies declared | All external deps with versions/contracts |
| 7 | Integration points | All integration boundaries documented |
| 8 | Breaking changes | Explicitly noted (even if "none") |
| 9 | Recommended skills | Execution skills listed |
| 10 | Team structure | Team + workstreams if complexity > Simple |
| 11 | Unit test cases | Test cases defined |
| 12 | Integration tests | Integration test scenarios |
| 13 | E2E verification | E2E verification command specified |
| 14 | Success criteria | Measurable criteria with acceptance thresholds |
| 15 | BD tasks created | Spec decomposed into BD epics/tasks |
| 16 | Rollback plan | How to undo if execution fails |

**Layer modulation:** FORMAL = all 16 + human sign-off; DIRECT = checks 1, 3, 14 only. See `./references/gates.md` for full per-tier breakdown.

**Failure:** CATASTROPHIC BLOCK. List every failing check with remediation. Return to SPEC. After 3 consecutive failures, escalate to human. Never auto-waive. Never skip. Never degrade severity.

### EMIT -- Create Artifact Bead

Create the stage-appropriate bead and let the hook render a markdown view for human readability.

1. Create bead via `br create` with the correct custom type and labels
2. Hook auto-renders a markdown view from bead content
3. Report bead ID to user

| Stage | Bead Type | Labels |
|-------|-----------|--------|
| captured | `custom:report` | `report,{domain}` |
| crystallizing | `custom:proposal` | `proposal,{layer},{domain}` |
| crystallized | `custom:spec` | `spec,{layer},{domain}` |
| manifesting | handoff bead | `handoff,{topic}` |
| completed | archive bead | `archive,{domain}` |

Learning artifacts are emitted by LEARN after completion:
- `custom:learning` with labels `learning,retrospective,{domain}`

### LEARN -- Session Close Ceremony

Final FSM step. Reflects on the session, records outcomes, creates a learnings bead.

**Triggers:** Session end, `/handoff`, `/exit`, explicit `learn` close request.

#### Steps

1. **Record outcomes** for rules used this session:
   ```bash
   cm outcome {success|failure|mixed} {bullet-ids} --session $SESSION --json
   ```

2. **Add new learnings** not captured inline during EXECUTE:
   ```bash
   cm add "{learning}" --category {category} --json
   ```

3. **Reflect on session** (extract patterns):
   ```bash
   cm reflect --days 1 --json --dry-run
   # Review proposed rules. If good:
   cm reflect --days 1 --json
   ```

4. **Create learnings bead**:
   ```bash
   br create "Learnings: {topic}" \
     --type '{"custom":"learning"}' \
     --labels "learning,retrospective,{domain}" \
     --description "{extracted learnings}" \
     --status closed
   ```

5. **Index session** for future search:
   ```bash
   cass index
   ```

#### Skip Conditions

- Ephemeral/brainstorm sessions (no learnings to record)
- Session < 5 minutes (insufficient depth)
- User flag: `--no-learn`

#### Learnings Bead Schema

```json
{
  "title": "Learnings: {topic}",
  "type": {"custom": "learning"},
  "labels": ["learning", "retrospective", "{domain}"],
  "description": "{what was learned and why it matters}",
  "status": "closed"
}
```

---

## Integration Points

### Lev Master Router

| Keywords | Route |
|----------|-------|
| get, search, find, lookup, read, ls, prior art | `lev get` |
| plan, design, build, research, analyze | **work** |
| learn, guide me, unstuck | **work** (`lev-learn` mode) |
| ask, wiz, wizard | **work** (`learn`/interview mode) |
| align, check, scan, security | **work** (validation gates) |
| workflow, workflows | `workflow` (create/list/run only) |
| execute, do it, run | **work** (routes to execute path; `lev exec` for direct imperative run) |
| install, setup, daemon, daemons | lev-core |

### Tracker Integration (br/bd/td)

- **Spec generated** → auto-create tasks via tracker adapter (if available), link spec artifact
- **Prior art check** → query tracker for related work
- **Completion** → close tasks, update status

### Team Mode

- Detect `variant.json` `swarmModeEnabled: true` or team keywords
- Delegate to `planning` skill for team decomposition
- Work skill orchestrates; planning skill executes workstream creation

---

## Error Handling

| Error | Severity | Response |
|-------|----------|----------|
| Confidence < 0.7 | WARN | Prompt user to clarify: research / design / spec / handoff |
| Tracker not available | INFO | Continue without task integration; note in artifact |
| Template missing | ERROR | Fallback to unstructured artifact; warn user |
| Spec validation fail | CATASTROPHIC | Block manifesting transition; list missing sections |
| Skill discovery empty | INFO | Proceed with inline execution; no skill injection |
| `learn` helper missing | WARN | Run inline interview loop in `work`; still emit proposal + handoff |
| CM/CASS not available | INFO | Skip LEARN ceremony; note in output |

---

## Configuration

| Env Var | Default | Purpose |
|---------|---------|---------|
| `LEV_PM_REPORTS` | `.lev/pm/reports/` | Report output dir |
| `LEV_PM_PROPOSALS` | `.lev/pm/proposals/` | Proposal output dir |
| `LEV_PM_SPECS` | `.lev/pm/specs/` | Spec output dir |
| `LEV_PM_HANDOFFS` | `.lev/pm/handoffs/` | Handoff output dir |

**Stage override:** `work --stage={ephemeral|captured|crystallizing|crystallized|manifesting}`

---

## Principles

1. **Progressive Disclosure** -- Start simple, add complexity as needed
2. **Fail Gracefully** -- Degrade when dependencies missing, don't block
3. **Validate Early** -- Check spec, prior art, alignment before proceeding
4. **Route, Don't Duplicate** -- Delegate to specialists, don't re-implement
5. **Context-Aware** -- Use workspace, artifacts, BD state for decisions
6. **Specs Drive Tests** -- Behavioral specs produce testable contracts
7. **Teams Scale Work** -- Match execution strategy to task complexity
8. **Learn Continuously** -- Capture learnings inline during execution; ceremony at session close

---

## Relates

### Master Router
- **Lev Master Router** (`lev/SKILL.md`) -- Routes all lev-* skills and work skill. Parent skill that dispatches to this skill for work requests.

### Related Skills
- `lev-research` -- Orchestrated research (DISCOVER + RESEARCH stages)
- `lev-cdo` -- Strategic design playbook (PROPOSE stage)
- `lev-learn` -- Guided interview intake to proposal (DISCOVER foreground track)
- `lev-align` -- Optional standalone drift-audit deep dive (ALIGN defaults to embedded work gate)
- `lev get` backend (`lev-find` legacy alias) -- Semantic context gather (DISCOVER background track)
- `br` / `bd` / `td` -- Task tracking via adapter (SPEC -> EXECUTE)
- `cm` -- Collective memory playbook (EXECUTE inline + LEARN ceremony)
- `cass` -- Content-addressable session search (DISCOVER + LEARN)

### Templates & References
- `./templates/report.md`
- `./templates/proposal.md`
- `./templates/spec.md`
- `./templates/handoff.md`
- `./references/gates.md` — Full per-gate definitions (layer modulation, confidence routing, failure actions)

---

**Status:** v3.2.0 -- Tracker adapter (br/bd/td) replaces hardcoded bd; gates integrated; EMIT beads-only; ROUTE/MANIFESTING clarified

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
You are the prompt-architect-enhanced specialist for work, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

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
