---
name: work
description: |
  [WHAT] Session lifecycle router — handoff-first, entity-tracked, prior-art-aware
  [HOW] 6-step operational loop: handoff → track → align → research → plan → close
  [WHEN] Use for all tracked work: plan, design, build, research, analyze, handoff, resume, close
  Triggers: "work", "plan", "design", "research", "handoff", "close", "resume"
---

# Work: Session Lifecycle Router (v5)

```
┌─────────┐    ┌───────┐    ┌───────┐    ┌──────────┐    ┌─────────┐    ┌───────┐
│ HANDOFF  │───→│ TRACK │───→│ ALIGN │───→│ RESEARCH │───→│ EXECUTE │───→│ CLOSE │
│ cp + fill│    │entity │    │ gate  │    │prior art │    │plan/do  │    │push   │
└────┬─────┘    └───┬───┘    └───┬───┘    └────┬─────┘    └────┬────┘    └───┬───┘
     │              │            │              │               │             │
     └──────────────┴────── update handoff every 3 actions ────┴─────────────┘
```

**HARD RULE:** 3+ substantive actions without a handoff tick → STOP. Log ticks first.
Substantive = bd create/close, file written/edited, stack step recorded, decision made, user correction.

---

## Step 1: Handoff

Copy the template, fill it out, keep it current every turn.

```bash
# New session
cp ~/.agents/skills/work/templates/handoff.md .lev/pm/handoffs/{YYYYMMDD}-{workstream}-{component}-session-{N}.md

# Resuming
cat .lev/pm/handoffs/{existing-handoff}.md
```

The template has instructions for every section. Follow them. Key sections to fill immediately:

- **You Are Here** — one sentence, what's happening right now
- **Next Agent Brief** — goal, done condition, current slice, out of scope
- **Entity Matrix** — real files at real paths (see Step 2)
- **Timeline** — log a tick for every action

Update cadence: every 3 actions (0-50% context), every 2 (50-75%), every 1 (75%+).

Shard to `session-{N+1}` at ~500 lines, >15 ticks, >5 entities, or >3 pivots.

---

## Step 2: Track Entities

An entity is a **file at a path**. Not a concept. Not a label.

```markdown
| # | File | Path | State | Issue | Next |
|---|------|------|-------|-------|------|
| 1 | SKILL.md | ~/.claude/skills/autodev-loop/SKILL.md | manifesting | lev-ga9 | tighten 793→450 |
| 2 | settings.json | ~/.claude/settings.json | captured | lev-548 | wire hook |
```

States:

| State | Path | Means |
|-------|------|-------|
| `ephemeral` | `.lev/scratch/` | exploring |
| `captured` | `.lev/pm/reports/` | researched |
| `crystallizing` | `.lev/pm/designs/` | shaping |
| `crystallized` | `.lev/pm/plans/` | ready to build |
| `manifesting` | code / handoffs | building |
| `completed` | `.lev/pm/validation-reports/` | done |

**BAD:** `| 1 | stack↔flowmind parity | classified |` — concept, no path.
**GOOD:** `| 1 | hygiene.flow.yaml | plugins/core-sdlc/flows/hygiene.flow.yaml | captured | — | wire steps |`

---

## Step 3: Align

Gate. Must pass before executing.

- [ ] Objective stated in handoff
- [ ] Scope bounded (Out of Scope filled)
- [ ] Entity matrix has ≥1 row with a real file path
- [ ] User signaled alignment

If **crystallization signal** fires from lifecycle hook:
1. STOP. Do not continue.
2. Update entity matrix.
3. Show user the matrix + what you were about to do.
4. Wait for confirmation.

---

## Step 4: Prior Art

Search before creating. Launch subagents in parallel:

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

If writing a research report:

```bash
cp ~/.agents/skills/work/templates/report.md .lev/pm/reports/{slug}.md
```

Follow the template instructions. Save findings with evidence.

---

## Step 5: Plan + Execute

Skip if brainstorming. Enter when there's a concrete slice.

### Choose template by work type

```bash
# Research / audit / scan
cp ~/.agents/skills/work/templates/report.md .lev/pm/reports/{slug}.md

# Design / proposal
cp ~/.agents/skills/work/templates/design.md .lev/pm/designs/{slug}.md
cp ~/.agents/skills/work/templates/proposal.md .lev/pm/proposals/{slug}.md

# Implementation plan
cp ~/.agents/skills/work/templates/plan.md .lev/pm/plans/plan-{kind}-{slug}.md

# Behavioral spec
cp ~/.agents/skills/work/templates/spec.md .lev/pm/specs/spec-{slug}.md
```

Each template has `## How To Fill This Out` at the top. Read it. Follow it.

### Prompt stacks (when deeper process needed)

```bash
# Decompose a plan into bd issues (5 steps, 3 anti-laziness review passes)
npx lev stack init --stack plan-to-beads
npx lev stack next --session $SID    # step 1: extract work items
npx lev stack record --session $SID --step extract-workitems --report ./report.md

# Deepen a vague plan (3 steps: decompose → research → synthesize)
npx lev stack init --stack sdlc-deepen-plan
npx lev stack next --session $SID    # step 1: decompose topics

# Validate implementation against spec
npx lev stack init --stack sdlc-exec-validate
npx lev stack next --session $SID    # step 1: validate gates
```

Flow definitions: `plugins/core-sdlc/flows/{stack-name}.flow.yaml`
Step prompts: `plugins/prompt-stack/prompts/steps/sdlc/`

### Gates

| Gate | Checks | Blocks |
|------|--------|--------|
| Preflight | handoff exists + objective + evidence ref | execution |
| Design ready | approach + acceptance criteria + rollback | non-trivial work |
| Close ready | validation evidence + blockers resolved + next action | session close |

### Subagents

Spawn for multi-file work. Each returns: `edited_files` + 1-2 sentence summary + `report_path` if >5000 tokens.

---

## Step 6: Close

```bash
# 1. Final handoff update — matrix, decisions, ticks, questions
# 2. Promote architectural decisions
cp ~/.agents/skills/work/templates/decision.md .lev/pm/decisions/d{N}-{slug}.md

# 3. Write validation report if code changed
cp ~/.agents/skills/work/templates/validation-report.md .lev/pm/validation-reports/{slug}.md

# 4. Commit and push
git add {files}
git commit -m "{message}"
git pull --rebase && git push

# 5. If bd dolt remote configured:
bd dolt pull && bd dolt push
```

### Done check

Before marking `completed`: goal met + done condition satisfied + no gaps. If gaps → update roadmap, re-enter lifecycle.

---

## Templates

All at `~/.agents/skills/work/templates/`. Copy to destination, follow instructions inside.

| Template | `cp` to | When |
|----------|---------|------|
| `handoff.md` | `.lev/pm/handoffs/` | Every session (Step 1) |
| `report.md` | `.lev/pm/reports/` | Research, audit, scan (Step 4) |
| `plan.md` | `.lev/pm/plans/` | Implementation slice (Step 5) |
| `design.md` | `.lev/pm/designs/` | Shaping solution (Step 5) |
| `proposal.md` | `.lev/pm/proposals/` | Non-trivial proposal (Step 5) |
| `spec.md` | `.lev/pm/specs/` | Behavioral contract (Step 5) |
| `decision.md` | `.lev/pm/decisions/` | Promote arch decision (Step 6) |
| `validation-report.md` | `.lev/pm/validation-reports/` | Validate work (Step 6) |

---

## Tracker

Detect: `bd > br > td > none`.

| Op | bd | br | td |
|----|-----|-----|-----|
| create | `bd create --title "..." --type task` | `br create ...` | `td add "..."` |
| list | `bd list --status open` | `br list ...` | `td` |
| update | `bd update {id} --status {s}` | `br update ...` | `td {id} edit` |
| close | `bd close {id}` | `br close ...` | `td {id} complete` |
| search | `bd search "{q}"` | `br search ...` | grep fallback |

Tracker = current slice only. Roadmap stays in handoff.

---

## Errors

| Error | Do |
|-------|----|
| No handoff | Create one first (Step 1) |
| No tracker | Continue, note in handoff |
| Gate failed | Block, add tick |
| 3x gate fail | Escalate to user |
| Crystallization signal | STOP → update matrix → show user → wait |
| 3+ actions no tick | STOP → log ticks → continue |
