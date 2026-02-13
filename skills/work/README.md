# Work Skill: Usage Guide

**Version:** 3.0.0
**Created:** 2026-01-28
**Updated:** 2026-02-10
**Team:** lev-skill-planning

---

## What is the Work Skill?

The work skill is a **unified entity lifecycle router** that eliminates the confusion of choosing between multiple overlapping skills.

### The Problem

Before the work skill, users had to remember:
- When to use `plan` vs `planning`
- When to use `lev-research` vs `deep-research` vs `grok-research`
- When to use `lev-cdo` vs `thinking-parliament`
- What order to invoke skills (research → design → spec)

### The Solution

The work skill **automatically determines** what stage you're in and routes appropriately.

```bash
# Just describe what you want - work figures out the rest
work "Analyze test coverage"           # → Routes to lev-research, generates report.md
work "Design test automation solution" # → Routes to lev-cdo, generates proposal.md
work "Create behavioral spec"          # → Routes to planning, generates spec.md (BDD + contract)
```

---

## Quick Start

### Installation

The work skill is located at `~/.agents/skills/work/` and is ready to use.

**Check installation:**
```bash
[ -f ~/.agents/skills/work/SKILL.md ] && echo "✅ Installed" || echo "❌ Not found"
```

### Basic Usage

Invoke the work skill via Claude Code:

```
User: /work "Analyze the authentication system"
```

The work skill will:
1. Assess context (workspace, existing artifacts)
2. Detect lifecycle stage (captured - need research)
3. Check prior art (search BD, docs, skills)
4. Route to lev-research
5. Create a `custom:report` bead (with markdown view in `.lev/pm/reports/`)

---

## Usage Patterns

### Pattern 1: Research & Analysis

**Use when:** You need to gather information, understand a system, or analyze existing work.

**Examples:**
```
work "Analyze the current API architecture"
work "Research best practices for error handling"
work "Scan the codebase for security vulnerabilities"
work "Understand how authentication currently works"
```

**Output:** `custom:report` bead (`.lev/pm/reports/*.md` view)

**What happens:**
- Routes to `lev-research` or `lev-find`
- Searches codebase, docs, external sources
- Generates structured findings report
- Includes recommendations and next actions

---

### Pattern 2: Design & Architecture

**Use when:** You need to design a solution, evaluate options, or make architectural decisions.

**Examples:**
```
work "Design a caching strategy for the API"
work "Propose solution for rate limiting"
work "Architect the authentication refactor"
work "Design database migration approach"
```

**Output:** `custom:proposal` bead (`.lev/pm/proposals/*.md` view)

**What happens:**
- Routes to `lev-cdo` or `thinking-parliament`
- Evaluates multiple options
- Includes validation gates and trade-offs
- Provides recommendation with rationale

**Prerequisites:** Usually requires a research report first

---

### Pattern 3: Specification (Pre-Implementation)

**Use when:** You need a behavioral spec contract before execution begins.

**Examples:**
```
work "Create behavioral spec for caching"
work "Specify the authentication refactor"
work "Define contract for database migration execution"
work "Write BDD spec for API v2"
```

**Output:** `custom:spec` bead (`.lev/pm/specs/*.md` view)

**What happens:**
- Routes to `planning` skill
- Generates `spec.md` sections (BDD scenarios, contract, tests, success criteria)
- Creates BD tasks (if BD available)
- Includes workstream decomposition (if team mode)

**Prerequisites:** Usually requires a proposal first

**Note:** Execution work happens in the next lifecycle stage (`manifesting`), not in this stage.

---

### Pattern 4: Execution + Session Handoff

**Use when:** You need to document current work for session continuity.

**Examples:**
```
work "Create handoff for authentication work"
work "Document current state for next session"
work "Generate session handoff"
```

**Output:** `.lev/pm/handoffs/{YYYYMMDD-HHMMSS}-{topic}.md`

**What happens:**
- Uses checkpoint contract (3-15 chronological checkpoints)
- Captures file trail (worked files + loaded files + why they matter)
- Includes code-context and key-decision/ADR checkpoint blocks
- Ends with next-agent system prompt + context confidence score

---

## Complete Workflow Example

### Scenario: Add Rate Limiting to API

#### Step 1: Research (captured stage)

```
work "Analyze current API rate limiting approach"
```

**Output:** `custom:report` bead with markdown view at `.lev/pm/reports/api-rate-limiting-analysis-2026-01-28.md`

**Contains:**
- Current implementation (or lack thereof)
- Known issues and vulnerabilities
- Best practices research
- Recommendations for next steps

---

#### Step 2: Design (crystallizing stage)

```
work "Design rate limiting solution for API"
```

**Output:** `custom:proposal` bead with markdown view at `.lev/pm/proposals/api-rate-limiting-solution-2026-01-28.md`

**Contains:**
- Multiple implementation options (token bucket, leaky bucket, fixed window, sliding window)
- Trade-offs for each approach
- Validation gates (performance, scalability, cost)
- Recommended approach with rationale

---

#### Step 3: Spec (crystallized stage)

```
work "Create behavioral spec for rate limiting"
```

**Output:** `custom:spec` bead with markdown view at `.lev/pm/specs/api-rate-limiting-spec-2026-01-28.md`

**Contains:**
- BDD scenarios (Given/When/Then)
- Inputs/processing/outputs
- Dependencies, integration points, breaking changes
- Test coverage and success criteria
- BD tasks created (if available)
- Workstream guidance

---

#### Step 4: Execute (manifesting stage)

Work on implementation according to spec...

#### Step 5: Handoff (if switching context)

```
work "Create handoff for rate limiting work"
```

**Output:** `.lev/pm/handoffs/api-rate-limiting-session-2026-01-28.md`

**Contains:**
- What was accomplished
- Current state
- Next steps
- Open questions
- Related artifacts and tasks

---

## Advanced Usage

### Stage Override

Force a specific lifecycle stage:

```
work --stage=captured "Your request"      # Force research
work --stage=crystallizing "Your request" # Force design
work --stage=crystallized "Your request"  # Force spec
```

### Custom Output Locations

Override default output directories:

```bash
export LEV_PM_REPORTS="$HOME/custom/reports"
export LEV_PM_PROPOSALS="$HOME/custom/proposals"
export LEV_PM_SPECS="$HOME/custom/specs"
export LEV_PM_HANDOFFS="$HOME/custom/handoffs"

work "Your request"  # Uses custom locations
```

### Prior Art Review

If work skill finds existing related work:

```
⚠️ Prior Art Found

Related work:
- Task #123: Similar implementation (status: open)
- report-api-analysis-2026-01-15.md: Previous analysis

Options:
1. Review existing work
2. Extend existing work
3. Proceed with new work anyway

Choose: _
```

---

## Integration with Other Skills

### Lev Master Router

The `lev` skill automatically routes work requests to the work skill:

```
User: "Research the auth system"
lev → Detects work keyword → Routes to work skill
```

You can still invoke work directly:

```
User: /work "Research the auth system"
```

### Planning Skill

When work skill detects `crystallized` stage (need `spec.md`), it routes to the `planning` skill for BDD + contract-driven specification. Execution happens later in `manifesting` (`EXECUTE`), followed by `VALIDATE`/`EMIT`/`LEARN`.

### BD Integration

If BD is available in the workspace:
- work skill checks BD for prior art
- spec.md generation creates BD tasks
- Tasks link to the spec artifact
- Dependencies align to declared integration points and criteria

### Team Mode

If team mode enabled (variant.json: swarmModeEnabled: true):
- work skill delegates to planning skill
- planning skill decomposes into workstreams
- Teammates spawned and tasks assigned

---

## Templates

The work skill uses templates from `~/.agents/skills/work/templates/`:

| Template | Stage | Size | Status |
|----------|-------|------|--------|
| `report.md` | captured | 4.3K | ✅ Available |
| `proposal.md` | crystallizing | 10.8K | ✅ Available |
| `spec.md` | crystallized | 1.8K | ✅ Available |
| `handoff.md` | manifesting | 8.1K | ✅ Available |

**All templates complete!** Full lifecycle artifact generation is now supported.

---

## Artifact Contracts (Beads-First)

The current `work` model stores canonical artifacts as beads custom types. Markdown files under `.lev/pm/*` are human-readable views.

| Lifecycle stage | Canonical artifact | Custom type |
|-----------------|--------------------|-------------|
| captured | research report | `custom:report` |
| crystallizing | proposal | `custom:proposal` |
| crystallized | behavioral spec (`spec.md`) | `custom:spec` |
| classified alignment context | system context | `custom:system` |
| archived | retrospective learning | `custom:learning` |

Manifesting uses a handoff bead/checkpoint contract for continuity output.

## v3 Lifecycle Map (Canonical)

`DISCOVER -> ALIGN -> RESEARCH -> PROPOSE -> SPEC -> EXECUTE -> VALIDATE -> EMIT -> LEARN`

Artifacts are canonical beads; `.lev/pm/*.md` entries are human-readable views.

---

## Memory Flow (cm + cass)

`work` uses `cm` for durable learning capture and `cass` for indexed retrieval:

`EXECUTE -> cm add (inline learnings) -> LEARN -> cm outcome + cm reflect -> learning bead -> cass index`

`DISCOVER <- cm context (workspace-first) + cass search + br search` for prior-session and artifact recall.

### 5-Tier Memory Fit (Concise)

| 5-tier memory type | Where `work` fits |
|--------------------|-------------------|
| working | Active session context, guard scoring, interview loop |
| episodic | Handoff checkpoints and session outcomes |
| procedural | `cm` playbook rules from `cm add` / `cm reflect` |
| semantic | Searchable artifact knowledge via beads + `cass` |
| temporal | Chronological session recall and progression history |

---

## Validation Gates

The work skill enforces quality checks:

### Spec Validation (CATASTROPHIC)

When generating `spec.md`, MUST include core contract sections:
- Executive summary + context
- BDD scenarios (Given/When/Then)
- Inputs/processing/outputs
- Dependencies + integration points + breaking changes
- Test coverage (unit/integration/E2E) + success criteria

**If missing → Blocks execution**

### Prior Art Check (MANDATORY)

Before creating any artifact, searches:
- BD for similar tasks/epics
- lev get for related docs
- Skills for existing capabilities

**If found → Prompts user to review/reuse**

### Architectural Alignment (CRITICAL)

When transitioning proposal → spec:
- Checks for XDG patterns
- Verifies fractal ownership
- Detects anti-patterns

**If violations found → Requires approval to bypass**

### Drift Detection (WARNING)

When references detected:
- Validates file paths resolve
- Checks symlinks not broken
- Verifies dependencies available

**If issues found → Warns but continues**

---

## Troubleshooting

### "I'm not sure what stage this is"

**Cause:** Low confidence in stage detection (< 0.7)

**Solution:** Be more explicit in your request:
- Instead of: "Help with auth"
- Try: "Analyze the authentication system" (research)
- Or: "Design auth refactor solution" (design)
- Or: "Create behavioral spec for auth" (crystallized)

---

### "Template not found"

**Cause:** Missing or inaccessible template in `~/.agents/skills/work/templates/`

**Solution:**
- Verify `report.md`, `proposal.md`, `spec.md`, `handoff.md` exist
- Re-sync/update local skills checkout
- Or: Proceed without template (creates basic structure)

---

### "BD not available"

**Cause:** No BD tracking in current workspace

**Solution:**
- Initialize BD: `bd init --prefix={project}`
- Or: Continue without BD integration (degrades gracefully)
- Or: Switch to workspace with BD

---

### Stage Detection Wrong

**Cause:** Ambiguous keywords or unexpected context

**Solution:**
- Override stage explicitly: `work --stage=captured "..."`
- Or: Provide more context in request
- Or: Invoke specialist skill directly if you know which one

---

## Best Practices

### 1. Follow the Lifecycle

Work progresses naturally:
```
Research (`custom:report`) → Design (`custom:proposal`) → Spec (`custom:spec`) → Execute → Handoff → Learn
```

Don't skip stages - each builds on the previous.

### 2. Let Work Skill Route

Instead of:
```
❌ "Use lev-research to analyze X"
```

Do:
```
✅ "Analyze X"  # Let work skill determine routing
```

### 3. Review Prior Art

When work skill finds related work, review it before proceeding. Saves time and prevents duplicate effort.

### 4. Use Clear Language

Stage detection works best with clear intent:
- "Analyze", "Research", "Scan" → Research stage
- "Design", "Propose", "Architect" → Design stage
- "Spec", "Specify", "Implement" → Crystallized (spec) stage

### 5. Check Output Locations

Work skill tells you where the markdown view was created (canonical artifact is a bead):
```
✅ Report view generated: .lev/pm/reports/api-analysis-2026-01-28.md
```

Always verify the file was created successfully.

---

## FAQ

### Q: Do I still need to know about other skills?

**A:** No! The work skill routes for you. However, you can still invoke specialist skills directly if you prefer.

### Q: Can I force a specific sub-skill?

**A:** Not directly, but you can override the stage which determines routing. Or invoke the specialist skill directly.

### Q: What if I want to use deep-research instead of lev-research?

**A:** Invoke deep-research directly. The work skill will use lev-research by default for captured stage, but you can bypass the router.

### Q: Does work skill replace planning skill?

**A:** No, work skill **routes to** planning skill in crystallized stage. Planning handles `spec.md` contract structure.

### Q: What happens if templates are missing?

**A:** Work skill creates artifacts without template structure. Functionality degrades gracefully.

### Q: Can I customize templates?

**A:** Not yet (future enhancement). Currently uses templates from `~/.agents/skills/work/templates/`.

### Q: Does work skill work without BD?

**A:** Yes! BD integration is optional. Work skill degrades gracefully:
- No prior art check against BD tasks
- No auto-creation of BD tasks from specs
- Everything else works normally

---

## Feedback & Issues

The work skill is version 3.0.0 - there may be rough edges.

**If you encounter issues:**
1. Check this README for troubleshooting
2. Review SKILL.md for detailed logic
3. Report to lev-skill-planning team
4. Or: Invoke specialist skills directly as fallback

**Future improvements tracked via lev-learn.**

---

## Version History

### v3.0.0 (2026-02-10)
- Concurrent FSM model (DISCOVER → ALIGN → RESEARCH → PROPOSE → SPEC → EXECUTE → VALIDATE → EMIT → LEARN)
- Crystallized output updated to `spec.md` / `custom:spec`
- Beads-first artifact contracts documented (`custom:report`, `custom:proposal`, `custom:spec`, `custom:system`, `custom:learning`)
- `cm` inline learning capture + LEARN ceremony + `cass` indexing flow documented

---

**Ready to use!** Start with: `work "Analyze something interesting"`
