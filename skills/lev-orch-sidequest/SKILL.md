---
name: sidequest
description: |
  Autonomous SDLC router. Takes a job, classifies complexity, executes the appropriate
  lev-* workflow (from trivial fix to full epic), and returns "done" with runnable instructions.
  One shot to full auto: spec/bd/poc/impl. Subagent returns completion artifact.

  Triggers: "sidequest", "side quest", "just do it", "autonomous", "one shot"
version: 1.0.0
skill_type: workflow
category: process-execution
triggers:
  - sidequest
  - side quest
  - just do it
  - autonomous task
  - one shot
---

# Sidequest - Autonomous SDLC Router

## Overview

Takes any job description and autonomously determines the right execution strategy — from a trivial one-liner to a full epic-driven SDLC with BD tracking. Returns "done" with a runnable instructions artifact.

## Quick Start

```
/sidequest fix the login timeout bug
/sidequest add SSO support for enterprise clients
/sidequest redesign the authentication system to support multi-tenant
```

## Architecture Context

> For current lev architecture, generate on the fly:
> `ls ~/lev/core/ | sort` (20 modules: domain, poly, exec, harness, orchestration, flowmind, graph...)
> `grep "id:" ~/lev/dna/*.dna.yaml` (DNA contracts — behavioral gates)
>
> Key primitives: ExecTransport (domain→poly DI), TmuxHarness (owned spawn), AdapterRegistry (6 adapters),
> A2A Dispatcher (AgentJob→JobExecutor), Route.parse('lev://module/fractal/item'), fractal config.
> ntm is EXTERNAL — use TmuxHarness for owned tmux spawn.

## Phase 0: Context Gathering (`lev get` pre-step)

Before classifying, gather context with semantic search:

```bash
SESSION_DIR="./tmp/sidequest-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$SESSION_DIR"

# Extract problem domain keywords
KEYWORDS="<extracted from job description>"

# Search for prior art, related code, and relevant skills
lev get "$KEYWORDS" --indexes codebase,tasks,skills,memory > "$SESSION_DIR/00-context.md" 2>/dev/null || \
lev get "$KEYWORDS" --indexes codebase,tasks,skills,memory > "$SESSION_DIR/00-context.md"

# Check if this work already exists in BD
bd list --status=open | grep -i "$KEYWORDS" >> "$SESSION_DIR/00-context.md"
```

**Fallback (if `lev get` slow/unavailable):**
```bash
# Timeout after 30 seconds, proceed with reduced context
timeout 30s sh -c 'lev get "$1" --indexes codebase,tasks > "$2" 2>/dev/null || lev find "$1" --indexes codebase,tasks > "$2"' _ "$KEYWORDS" "$SESSION_DIR/00-context.md" || {
  echo "# Context gathering timed out - using bd + grep fallback" > "$SESSION_DIR/00-context.md"
  bd list --status=open >> "$SESSION_DIR/00-context.md" 2>/dev/null
  # Fallback to grep for quick file discovery
  grep -r "$KEYWORDS" --include="*.ts" --include="*.md" -l . 2>/dev/null | head -20 >> "$SESSION_DIR/00-context.md"
}
```

**Escalation path:** If classification is uncertain after context gathering, route UP one level and note "escalated due to ambiguity" in DONE.md.

## Phase 1: Complexity Classification

Classify the job on 4 dimensions:

```
COMPLEXITY FACTORS:
├─ Scope: How many files/components affected? (1 | 2-5 | 6-15 | 15+)
├─ Clarity: How well-defined is the task? (exact | clear | fuzzy | unknown)
├─ Risk: What breaks if wrong? (nothing | recoverable | significant | critical)
└─ Sessions: Can this be done in one sitting? (yes | maybe | no | definitely not)
```

### Classification Matrix

| Scope | Clarity | Risk | Sessions | → Level |
|-------|---------|------|----------|---------|
| 1 file | exact | nothing | yes | TRIVIAL |
| 2-5 files | clear | recoverable | yes | BASE |
| 6-15 files | fuzzy | significant | maybe | DEEP |
| 15+ files | unknown | critical | no | EPIC |

**Tie-breaking:** When factors disagree, route UP one level. Better to over-spec than under-spec.

## Phase 2: Route to Handler

### TRIVIAL — Direct Execute

```
Criteria: 1 file, exact change, no risk, <10 LOC
Handler: Just do it. No BD, no spec artifact.

Steps:
1. Make the change
2. Run tests (if they exist)
3. Write DONE.md with what changed
```

### BASE — Plan + Implement

```
Criteria: 2-5 files, clear scope, recoverable risk
Handler: Lightweight spec → implement → validate

Steps:
1. Create minimal spec (5-10 bullet points + acceptance checks)
2. Implement changes
3. Run canned validations (test, build, lint)
4. bd create + bd close (single bead for tracking)
5. Write DONE.md with changes + validation results
```

### DEEP — Design-to-BD Flow

```
Criteria: 6-15 files, fuzzy scope, significant risk
Handler: design-to-bd → agentic-execution → validate

Steps:
1. Research dispatch (2-3 parallel `lev get` queries)
2. Design document (stored in $SESSION_DIR/design.md)
3. BD scaffolding (epic + tasks with dependencies)
4. Agentic execution with turn-based dispatch:
   - Turn 1: Research/scaffold parallel
   - Turn 2: Implementation parallel
   - Turn 3: Validation (mandatory)
5. bd close when all validations pass
6. Write DONE.md with epic summary + instructions
```

### EPIC — Full SDLC

```
Criteria: 15+ files, unknown scope, critical risk, multi-session
Handler: thinking-parliament → design-to-bd → agentic-execution → ralph-tui

Steps:
1. Parliament deliberation (multi-modal, see thinking-parliament)
2. Design-to-BD with [A][B][C][V] workstreams
3. Agentic execution with wave-based parallelism:
   lev exec --epic=<id> --dry-run    # Preview waves
   lev exec --epic=<id>              # Execute
4. Ralph validation loop:
   - 3-round devil's advocate
   - Task-specific validations from BD descriptions
   - <promise>EPIC_COMPLETE</promise> required
5. bd sync + git push
6. Write DONE.md with full execution report
```

## Phase 3: Multi-Model Dispatch (when applicable)

For DEEP and EPIC levels, use multi-model dispatch for research/design:

```bash
# Parallel research with different models for perspective diversity
lev exec "Research: $ASPECT_A" --model=claude-sonnet-4-20250514 --adapter=claude-agent-sdk > "$SESSION_DIR/research-a.md" &
lev exec "Research: $ASPECT_B" --model=google/gemini-3-flash-preview --adapter=ai-sdk > "$SESSION_DIR/research-b.md" &
lev exec "Research: $ASPECT_C" --model=openai/gpt-5.2-pro --adapter=ai-sdk > "$SESSION_DIR/research-c.md" &
wait

# Synthesize with opus for deep reasoning
lev exec "Synthesize these research findings into a design..." --model=opus --adapter=cli
```

## Phase 4: Completion Artifact

Every sidequest produces `$SESSION_DIR/DONE.md`:

```markdown
# Sidequest Complete

## Job: <original description>
## Level: <TRIVIAL|BASE|DEEP|EPIC>
## Duration: <start → end timestamps>

## What Changed
- <file>: <description of change>
- ...

## Validations Run
- [ ] Tests: <pass/fail>
- [ ] Build: <pass/fail>
- [ ] Lint: <pass/fail>
- [ ] Task-specific: <details>

## Runnable Instructions (for human follow-up)
1. <any manual steps needed>
2. <deployment notes>
3. <monitoring to watch>

## BD Tracking
- Epic: <id or "none">
- Tasks closed: <list>
- Tasks remaining: <list or "none">
```

## Error Handling

```
IF classification uncertain:
  └─→ Route UP one level (over-spec, don't under-spec)

IF execution fails mid-stream:
  └─→ Write STALLED.md with:
      - What completed
      - What failed (error details)
      - What remains
      - Suggested recovery steps
  └─→ bd update <id> --status=blocked

IF validation fails:
  └─→ Retry once with fix attempt
  └─→ If still fails: escalate to STALLED.md
  └─→ Never close a task with failing validations
```

## Integration Points

| Tool | When Used | Purpose |
|------|-----------|---------|
| `lev get` | Phase 0 | Context gathering, prior art |
| `bd create/close` | BASE+ | Work tracking |
| `lev exec` | DEEP+ | Multi-model dispatch |
| `thinking-parliament` | EPIC | Multi-modal deliberation |
| `design-to-bd` | DEEP+ | Design → BD scaffolding |
| `agentic-execution` | DEEP+ | Turn-based parallel dispatch |
| `ralph-tui` | EPIC | Autonomous completion loop |

## Examples

### Trivial
```
/sidequest fix typo in README.md line 42

→ Level: TRIVIAL
→ Action: Fix typo, no tests needed
→ DONE.md: "Fixed typo: 'recieve' → 'receive' in README.md:42"
```

### Base
```
/sidequest add rate limiting to the /api/login endpoint

→ Level: BASE
→ Action: Spec (middleware placement, limits) → Implement → Test
→ BD: Single bead tracking the change
→ DONE.md: Files changed, test results, deployment notes
```

### Deep
```
/sidequest add WebSocket support for real-time notifications

→ Level: DEEP
→ Action: Research (3 models) → Design → BD scaffold → Implement → Validate
→ BD: Epic with 4-6 tasks + validation task
→ DONE.md: Architecture decisions, implementation summary, test coverage
```

### Epic
```
/sidequest redesign the entire auth system for multi-tenant support

→ Level: EPIC
→ Action: Parliament → Design → BD [A][B][C][V] → Agentic exec → Ralph loop
→ BD: Epic with 10+ tasks across workstreams
→ DONE.md: Full execution report with migration guide
```

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
You are the prompt-architect-enhanced specialist for lev-orch-sidequest, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

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
