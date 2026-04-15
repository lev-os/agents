---
name: work
description: Use when starting any tracked work session, resuming from a handoff, planning, designing, building, researching, or closing a session
---

# Work: Session Lifecycle Router (v6)

**Core principle:** Every session has a handoff, every action updates it, every decision is tracked. No freestyle.

**Violating the letter of this process is violating the spirit of tracked work.**

## The Iron Law

```
NO WORK WITHOUT A HANDOFF. NO DECISION WITHOUT EVIDENCE. NO CLOSE WITHOUT A PUSH.
```

If you haven't created or loaded a handoff, you cannot proceed to any other step.

<HARD-GATE>
YOU MUST follow Steps 1-6 in order. You MUST update the handoff when events happen.
Skipping steps or "just doing it" is a failure mode, not efficiency.
</HARD-GATE>

## The Gate Function

```
BEFORE starting any work:

1. HANDOFF: Load existing or create new (.lev/pm/handoffs/)
2. TRACK: Add ≥1 entity with a real file path to the matrix
3. ALIGN: Objective stated, scope bounded, user confirmed
4. SEARCH: Prior art checked (grep .lev/pm/, bd search, docs/)
5. ROUTE: Match work type to the right sub-skill
6. ONLY THEN: Execute

Skip any step = untracked work = lost context = wasted session
```

---

## Step 1: Handoff (MANDATORY — before everything else)

```bash
# New session
cp ~/.agents/skills/work/templates/handoff.md .lev/pm/handoffs/{YYYYMMDD}-{workstream}-session-{N}.md

# Resuming
cat .lev/pm/handoffs/{existing-handoff}.md
```

Fill immediately:
- **You Are Here** — one sentence, current state
- **Next Agent Brief** — goal, done condition, scope, out of scope
- **Entity Matrix** — real files at real paths (Step 2)
- **Timeline** — log every action

Shard at ~500 lines, >15 ticks, >5 modified entities, or >3 pivots.

**Update the handoff when ANY of these happen:**
- Decision made or changed
- File written, edited, or created
- User gives feedback or correction
- BD issue created or closed
- Research produces a finding
- About to context-switch or close

Reading files, grepping, scanning → NOT update triggers.

---

## Step 2: Track Entities

An entity is a **file or directory at a path**. Not a concept. Not a label.

```markdown
| # | File | Path | State | Canonical Ref | Decision | Next |
|---|------|------|-------|---------------|----------|------|
| 1 | SKILL.md | ~/.agents/skills/work/SKILL.md | modified | — | D1 | update |
```

States: `loaded` | `captured` | `modified` | `created` | `planned` | `completed`

```
✅ | 1 | hygiene.flow.yaml | plugins/core-sdlc/flows/hygiene.flow.yaml | captured | — | wire steps |
❌ | 1 | stack↔flowmind parity | classified |  ← concept, no path = WRONG
```

---

## Step 3: Align

Gate. MUST pass before executing.

```
BEFORE proceeding past this step:

1. CHECK: Objective stated in handoff?
2. CHECK: Scope bounded (Out of Scope filled)?
3. CHECK: Entity matrix has ≥1 row with a real file path?
4. CHECK: User signaled alignment?
5. IF .lev/validation-gates.yaml exists: Load, filter, check enforced gates
6. ONLY THEN: Proceed to Step 4

Any check fails = STOP. Fix it. Do not proceed.
```

**If crystallization signal fires:** STOP. Update entity matrix. Show user the matrix + what you were about to do. Wait for confirmation.

---

## Step 4: Prior Art (NEVER skip)

Search before creating. YOU MUST run these searches:

```bash
ls .lev/pm/plans/ .lev/pm/designs/ .lev/pm/specs/ .lev/pm/decisions/
grep -rl "{topic}" .lev/pm/ docs/specs/ docs/design/
grep -l "{topic}" docs/ARCHITECTURE.md
bd search "{topic}"
```

Report findings:

```markdown
| Found | Path | Relation | Action |
|-------|------|----------|--------|
| {name} | {path} | extends / supersedes | update / create new |
```

**No prior art found?** State explicitly: "No existing artifacts found for {topic}." Then proceed.

---

## Step 5: Route + Execute

**4-Lane Operator Model** (from tribunal #20, unanimous):

| Lane | Steps | Verbs | Gate to Next |
|------|-------|-------|-------------|
| **Shape** | 1-3 (Handoff, Track, Align) | /research, /prior-art, /interview | ambiguity ≤ 0.2 |
| **Plan** | 4 (Search + /propose + /capture) | /propose, /capture | frame_complete |
| **Exec** | 5 (Route + Execute) | /exec, /manifest | convergence ≥ 0.95 |
| **Close** | 6 (Close) | /qa, /accept, /handoff | drift < 0.3 |

Match work type to the right approach. This is a router, not a freestyle zone.

```
WHAT IS THE WORK?                          LIFECYCLE NODE
                                           (lifecycle.flow.yaml)
→ "I need to figure out WHAT to build"
    ENTRY: research → prior_art → ambiguity_check
    SKILL: /lev-research, /prior-art, /interview

→ "I know what to build, need to DESIGN it"
    ENTRY: propose → frame_check → capture → decision_point
    SKILL: /capture (inline propose prompt writes dna.yaml + execution.yaml)

→ "I need to RESEARCH something"
    ENTRY: research (direct --entry=research)
    SKILL: /lev-research → report artifact in .lev/pm/reports/

→ "I need to encode or update DNA first"
    ENTRY: capture (direct --entry=capture)
    SKILL: /capture → DNA artifact + cascade-ready execution path

→ "I have a spec, need to BUILD it"
    ENTRY: exec → convergence_check
    SKILL: /exec (resolves topology from execution.yaml)

→ "Something is BROKEN"
    ENTRY: exec (debug topology)
    SKILL: /cdo debug (multi-agent) OR /systematic-debugging (single)

→ "I need to DECIDE something"
    ENTRY: interview → ambiguity_check
    SKILL: /interview --framework=FirstPrinciples OR /cdo think

→ "I need to write a PROPOSAL or DESIGN doc"
    ENTRY: propose → frame_check
    Templates: design.md, proposal.md → .lev/pm/{designs,proposals}/
```

## Lifecycle FlowMind Router

`/work` is the **entry skill** for `lifecycle.flow.yaml` (18 nodes, 4 lanes, math-backed gates).
Every verb collapses to a lifecycle entry point. The router node inspects task state and branches.

### Verb Collapse Table

| Invocation | Entry Node | What Happens |
|------------|------------|-------------|
| `/work` (bare) | `router` | Scan task state, pick lane, run |
| `/work --entry=shape` | `research` | Shape lane: research → prior_art → ambiguity_check |
| `/capture` | `capture` | Plan lane: capture → decision_point |
| `/exec` | `exec` | Exec lane: exec → convergence_check |
| `/ok` | `ok` | Close lane: ok → drift_check → handoff → done |
| `/handoff` | `handoff` | Terminal: emit session continuity artifact |

### Manifest Lookup

`lifecycle-manifest.yaml` (`core/flowmind/system/lifecycle-manifest.yaml`) is the verb-to-skill-to-flow
source of truth. For any verb, it resolves: `skill` + `skill_dir` + `flow` + `entry_node` + `gate` + `gate_formula`.

### HUD Line

Every `/work` invocation emits a HUD status line:

```
[lifecycle] node={current} lane={shape|plan|exec|close} gate={name} score={value} → next={node|done}
```

### Aliases

- **`/ll` IS `/work` at loop pace.** Same router, same gates, tick-scheduled via `tick-loop.flow.yaml`.
- **`/siterep` IS `/work` status.** Reads lifecycle state without advancing. Dashboard, not action.

### Templates

All at `~/.agents/skills/work/templates/`. Copy to destination, follow instructions inside.

| Template | Destination | When |
|----------|-------------|------|
| `handoff.md` | `.lev/pm/handoffs/` | Every session (Step 1) |
| `report.md` | `.lev/pm/reports/` | Research, audit, scan |
| `plan.md` | `.lev/pm/plans/` | Implementation slice |
| `design.md` | `.lev/pm/designs/` | Shaping solution |
| `proposal.md` | `.lev/pm/proposals/` | Non-trivial proposal |
| `spec.md` | `.lev/pm/specs/` | Behavioral contract |
| `decision.md` | `.lev/pm/decisions/` | Promote arch decision |
| `validation-report.md` | `.lev/pm/validation-reports/` | Validate work |

### Prompt Stacks (deeper process)

```bash
npx lev stack init --stack plan-to-beads      # Decompose plan → bd issues
npx lev stack init --stack sdlc-deepen-plan   # Deepen vague plan
npx lev stack init --stack sdlc-exec-validate # Validate impl against spec
```

### Subagents

Spawn for multi-file work. Each MUST return:
```json
{"edited_files": ["<paths>"], "summary": "<1-2 sentences>", "report_path": "<if >5000 tokens>"}
```

---

## Step 6: Close

```
BEFORE claiming this session is complete:

1. VERIFY: Goal met? Done condition satisfied? No gaps?
2. UPDATE: Final handoff — matrix, decisions, ticks, open questions
3. PROMOTE: Architectural decisions → .lev/pm/decisions/d{N}-{slug}.md
4. VALIDATE: If code changed → run tests/build, write validation report
5. COMMIT: git add {files} && git commit -m "{message}"
6. PUSH: git pull --rebase && git push
7. SYNC: If bd dolt remote configured → bd dolt pull && bd dolt push
8. CONFIRM: git status shows "up to date with origin"

Skip any step = incomplete session = stranded work
```

If closing reveals unresolved or unprocessed handoffs:

1. Keep `work` as the entry surface and update the active handoff first.
2. If the operator already knows the exact handoff path, route to:
   `bun plugins/prompt-stack/src/cli.ts init --stack sdlc-handoff-close --project-dir /absolute/project/path`
3. If the operator needs to scan and choose from multiple handoffs, route to:
   `bun plugins/prompt-stack/src/cli.ts init --stack sdlc-handoff-rollup --project-dir /absolute/project/path`
4. Record each step output into `.lev/pm/reports/`.
5. Return to the active handoff after `record`/`validate` and update continuity there.

`work` owns the closeout decision. `stack` owns the execution-plane rollup loop.

```
✅ [Run git push] [See: "up to date with origin"] "Session complete"
❌ "Ready to push when you are" / "Work is done" (without pushing)
```

---

## Red Flags — STOP

If you catch yourself thinking:
- "I'll just do this one quick thing without a handoff"
- "Prior art search is overkill for this"
- "I don't need to track entities for something this small"
- "I'll update the handoff later"
- "The user knows what I'm doing, I don't need to write it down"
- "This is a simple task, I can skip alignment"
- "I'll push at the end" (then forgetting)
- "Ready to push when you are" (YOU must push, not the user)

**ALL of these mean: STOP. You're about to lose context.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Too simple for a handoff" | Simple tasks lose context too. Handoff takes 30 seconds. |
| "Prior art search is slow" | Finding existing work is faster than duplicating it. |
| "I'll track entities mentally" | You'll forget. Write it down. |
| "User didn't ask for alignment" | Alignment prevents wasted work. Do it anyway. |
| "I know which skill to use" | Route explicitly. "I know" = assumption. |
| "I'll push later" | Later = never. Push NOW. |
| "Work is done" (no push) | Work is NOT done until `git push` succeeds. |
| "Just one more thing before closing" | Close first. Open new session for new work. |

## Tracker

Detect: `bd > br > td > none`.

| Op | bd | br | td |
|----|-----|-----|-----|
| create | `bd create --title "..." --type task` | `br create ...` | `td add "..."` |
| list | `bd list --status open` | `br list ...` | `td` |
| update | `bd update {id} --status {s}` | `br update ...` | `td {id} edit` |
| close | `bd close {id}` | `br close ...` | `td {id} complete` |
| search | `bd search "{q}"` | `br search ...` | grep fallback |

## Errors

| Error | Do |
|-------|----|
| No handoff | Create one FIRST (Step 1). Do not proceed. |
| No tracker | Continue, note in handoff |
| Gate failed | Block, add tick to handoff |
| 3x gate fail | Escalate to user |
| Crystallization signal | STOP → update matrix → show user → wait |
| Event happened, no handoff update | STOP → update handoff → then continue |
| Sub-skill not found | Degrade: use the template directly instead of routing |
| Push failed | Resolve and retry. Do NOT close session without pushing. |
