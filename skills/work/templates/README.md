# Lev Work Templates

**Location:** `~/.agents/skills/work/templates/`
**Created:** 2026-01-28
**Purpose:** Standardized markdown templates with YAML frontmatter for knowledge management

---

## Available Templates

### 1. report.md
**Use for:** Research findings, scan results, audits, analysis

**Key Features:**
- YAML frontmatter with metadata (status, scope, confidence, tags)
- Executive summary with quick stats
- Structured findings sections
- Validation checklist
- References and audit trail

**When to use:**
- After scanning/analyzing code or systems
- Documenting research findings
- Creating audit reports
- Sharing analysis results

**Example usage:**
```bash
cp ~/.agents/skills/work/templates/report.md ~/clawd/.lev/pm/reports/my-report.md
# Edit and fill in the template
```

---

### 2. proposal.md
**Use for:** Design solutions, architecture proposals, feature specifications

**Key Features:**
- YAML frontmatter with validation gates tracking
- Problem statement and solution approach
- Implementation phases with validation
- DoR validation section
- Prior art check
- Alignment check
- Approval gates
- Alternatives considered
- Risk assessment

**When to use:**
- Proposing new features or changes
- Architecture design documents
- Before starting complex work
- Need stakeholder approval

**Example usage:**
```bash
cp ~/.agents/skills/work/templates/proposal.md ~/clawd/.lev/pm/proposals/my-proposal.md
# Fill in problem, solution, validation gates
```

---

### 3. handoff.md
**Use for:** Session continuity, knowledge transfer between sessions/agents

**Key Features:**
- YAML frontmatter with session metadata
- Canonical checkpoint contract (3-15 chronological checkpoints)
- Three checkpoint blocks: Progress, Code Context, Key Decision/ADR
- Mandatory file trail: worked-on files, loaded files, and why they mattered
- System prompt section for next agent continuity
- Context confidence score with remaining uncertainty

**When to use:**
- End of work session
- Passing work to another agent/human
- Creating checkpoints
- Documenting session progress

**Example usage:**
```bash
cp ~/.agents/skills/work/templates/handoff.md .lev/pm/handoffs/$(date +%Y%m%d-%H%M%S)-topic.md
# Fill checkpoints + next-agent prompt + confidence score
```

---

### 4. plan.md
**Use for:** Implementation plans, detailed execution roadmaps

**Key Features:**
- YAML frontmatter with DoR validation tracking
- Goal and success definition
- Prior art check section
- Context and gotchas
- Implementation blueprint with phases
- Task breakdown with validation per phase
- Team execution strategy (if team mode)
- 4-level validation loop (syntax, unit, integration, E2E)
- Anti-patterns to avoid
- Rollback plan

**When to use:**
- Before implementing features
- Breaking down complex work
- Planning team execution
- Need structured implementation approach

**Example usage:**
```bash
cp ~/.agents/skills/work/templates/plan.md ~/clawd/.lev/pm/plans/my-plan.md
# Define goal, phases, validation strategy
```

---

## Template Design Principles

### 1. YAML Frontmatter
All templates use YAML frontmatter for:
- Metadata (dates, authors, status)
- Searchability (tags, IDs, relations)
- Validation tracking (DoR, gates, approvals)
- Type classification

### 2. Lev-Codifier Patterns
Templates follow lev-codifier principles:
- **Structured sections:** Clear hierarchy and navigation
- **Validation checklists:** Explicit quality gates
- **Cross-references:** Links to related work
- **Audit trails:** Track changes and decisions
- **Context preservation:** Enough info for cold starts

### 3. Markdown-First
- Human-readable
- Git-friendly (diffs work well)
- Tool-agnostic (works in any editor)
- Supports code blocks and tables

### 4. Adaptive Complexity
Templates support different complexity levels:
- **report.md:** Scales from quick scans to deep analysis
- **proposal.md:** Supports light DoR to full validation gates
- **handoff.md:** Works for 5-minute or multi-hour sessions
- **plan.md:** Adapts from solo to team execution

---

## Usage Patterns

### Pattern 1: Research → Proposal → Plan → Implementation
1. Use **report.md** to document research/analysis
2. Create **proposal.md** based on findings
3. Break down proposal into **plan.md**
4. Execute plan, create **handoff.md** at session end

### Pattern 2: Quick Implementation
1. Use **plan.md** (inline/light tier)
2. Skip proposal if change is small
3. Create **handoff.md** if work continues later

### Pattern 3: Session Continuity
1. Start session: Load previous **handoff.md**
2. Do work: Track decisions
3. End session: Create new **handoff.md**
4. Next session: Load latest handoff

### Pattern 4: Team Collaboration
1. Lead creates **plan.md** with team structure
2. Workers execute phases
3. Each worker creates **handoff.md** for their work
4. QA creates **report.md** with validation findings

---

## Validation Checklist

### Template Quality
- [ ] YAML frontmatter present and valid
- [ ] All sections have clear purpose
- [ ] Validation checklists included
- [ ] Reference sections included
- [ ] Examples/patterns shown where helpful

### Usability
- [ ] Easy to fill in (clear placeholders)
- [ ] Scales to different complexity levels
- [ ] Works standalone or as part of workflow
- [ ] Git-friendly (good diffs)

### Integration
- [ ] Links to related work
- [ ] Supports task/epic references
- [ ] Compatible with BD tracking
- [ ] Works with lev-codifier patterns

---

## Customization

### Adding Custom Sections
Templates are starting points - customize as needed:
- Add domain-specific sections
- Remove irrelevant sections
- Adjust validation levels
- Extend YAML frontmatter

### Project-Specific Templates
Create variants for specific needs:
```bash
cp report.md security-audit-report.md
# Customize for security-specific fields
```

---

## Integration with Lev Ecosystem

### BD Tracking
Templates support BD integration:
- YAML `related_tasks` field for task IDs
- References section links to epics
- Status tracking aligns with BD states

### Lev Get
Templates are searchable via lev get:
- YAML frontmatter indexed
- Content searchable
- Tags for categorization

### Validation Gates
Templates include validation tracking:
- DoR completion status
- Approval gates
- Quality checklists

---

## Maintenance

### Template Updates
- Version templates when structure changes
- Archive old versions if breaking changes
- Document changes in git commits

### Feedback Loop
- Improve templates based on usage
- Add missing sections as needs emerge
- Remove unused sections over time

---

## Examples

See examples of filled templates in:
- Reports: `~/clawd/.lev/pm/reports/`
- Proposals: `~/clawd/.lev/pm/proposals/` (or `~/lev/.lev/pm/proposals/`)
- Handoffs: `~/clawd/.lev/pm/handoffs/`
- Plans: `~/clawd/.lev/pm/plans/`

---

## Quick Reference

| Template | Primary Use | Complexity | Validation Focus |
|----------|-------------|------------|------------------|
| report.md | Analysis/findings | Adaptive | Quality of findings |
| proposal.md | Design/architecture | Full DoR | Approval gates |
| handoff.md | Session continuity | Adaptive | Completeness |
| plan.md | Implementation | Adaptive | 4-level validation |

---

*Templates created as part of lev-skill-planning initiative*
*Task #8: Create YAML frontmatter templates*
