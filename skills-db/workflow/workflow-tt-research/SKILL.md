---
name: workflow-tt-research
description: Execute a research job with auto-strategy selection using the timetravel adapter library. Invoke with /workflow tt-research.
skill_type: workflow
category: process-workflow
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
---

# Workflow: Timetravel Research

Execute a full research workflow using the timetravel adapter library at `~/digital/leviathan/plugins/timetravel/`.

Every step spawns a **fresh subagent** (poly sparkle pattern). State flows only through handoff artifacts at `.lev/pm/handoffs/tt-research-*.md`.

## Trigger

- User wants to research a topic using the timetravel system
- `/workflow tt-research "<query>" [--strategy <name>] [--depth quick|standard|deep]`

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `query` | yes | Research query string |
| `strategy` | no | Override strategy (quick, full, deep, max, academic, social). Default: auto-selected |
| `depth` | no | Shorthand for strategy: quick=quick, standard=full, deep=deep |
| `output_dir` | no | Override output directory (default: `~/.config/LEV/research/sessions/<date>/<slug>/`) |

## Steps

### Step 1: Assess Query

**Agent Type**: Explore
**Skills**: `skill://lev-research`
**Research**:
- Analyze query complexity: single-fact, comparative, investigative, comprehensive
- Read available strategies: `~/digital/leviathan/plugins/timetravel/src/strategy.ts`
- Check user-provided strategy override

**Action**:
- Classify query type and recommend strategy
- If no strategy specified: quick for single-fact, full for comparative, deep for investigative, max for comprehensive
- Identify relevant adapters and potential gaps
- Create session directory: `~/.config/LEV/research/sessions/<date>/<slug>/`

**Handoff**: `.lev/pm/handoffs/tt-research-1-assess.md`
```yaml
query: <original query>
query_type: single-fact | comparative | investigative | comprehensive
recommended_strategy: <strategy name>
selected_strategy: <final choice>
session_dir: <path>
adapters_needed: [<list>]
```

---

### Step 2: Health Check

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoff from Step 1
- Run `cd ~/digital/leviathan/plugins/timetravel && npx timetravel status` to check adapter availability

**Action**:
- Verify all adapters needed by selected strategy are available
- If missing adapters: downgrade strategy or warn user
- Record adapter health snapshot

**Handoff**: `.lev/pm/handoffs/tt-research-2-health.md`
```yaml
strategy_viable: true | false
available_adapters: [<list>]
missing_adapters: [<list>]
adjusted_strategy: <name if changed, null if same>
```

---

### Step 3: Execute Search

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoffs from Steps 1-2
- Read strategy definition for orchestration mode

**Action**:
- Run `cd ~/digital/leviathan/plugins/timetravel && npx timetravel search "<query>" --strategy <name>`
- Capture JSON output
- Save raw results to `<session_dir>/artifacts/search_raw.json`
- If strategy has synthesizer, verify synthesis was included

**Handoff**: `.lev/pm/handoffs/tt-research-3-execute.md`
```yaml
strategy_used: <name>
adapters_responded: [<list>]
source_count: <n>
has_synthesis: true | false
raw_results_path: <path>
duration_ms: <n>
```

---

### Step 4: Synthesize

**Agent Type**: general-purpose
**Skills**: `skill://lev-research`
**Research**:
- Read handoff from Step 3
- Read raw results from `<session_dir>/artifacts/search_raw.json`
- If synthesis already present from oracle, use as base

**Action**:
- Deduplicate sources across adapters (by URL)
- Rank sources by relevance (title/snippet match to query)
- Generate synthesis: executive summary (2-3 sentences), key findings (3-5), evidence table
- Apply multi-perspective overlay if depth is deep or max
- Save to `<session_dir>/synthesis.md`

**Handoff**: `.lev/pm/handoffs/tt-research-4-synthesize.md`
```yaml
unique_sources: <n>
key_findings: <n>
perspectives_applied: [<list or none>]
synthesis_path: <path>
confidence: <0.0-1.0>
```

---

### Step 5: Generate Report

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoffs from Steps 1-4
- Read synthesis from Step 4

**Action**:
- Compile final research report using lev-research synthesis template:
  - Executive summary
  - Key findings with source citations
  - Evidence table (claim, source, confidence)
  - Open questions
  - Numbered source list with URLs
- Save to `<session_dir>/report.md`
- Save `<session_dir>/session.json` with metadata

**Handoff**: `.lev/pm/handoffs/tt-research-5-report.md`
```yaml
report_path: <path>
session_json_path: <path>
total_sources: <n>
confidence: <0.0-1.0>
```

---

### Step 6: Persist Job

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoffs from Steps 1-5
- Read job system: `~/digital/leviathan/plugins/timetravel/src/job.ts`

**Action**:
- Create a timetravel job record for re-runs: `npx timetravel job create -q "<query>" -s <strategy>`
- Record job ID in session metadata
- Optionally schedule if user requested recurring: `npx timetravel schedule add <job_id> -c <interval>`
- Print final summary with report path and job ID

**Handoff**: `.lev/pm/handoffs/tt-research-6-persist.md`
```yaml
job_id: <tt-...>
scheduled: true | false
schedule_interval: <cron or null>
report_path: <path>
status: complete
```

## Outputs

- Research report: `<session_dir>/report.md`
- Synthesis: `<session_dir>/synthesis.md`
- Raw results: `<session_dir>/artifacts/search_raw.json`
- Session metadata: `<session_dir>/session.json`
- Job record: `~/.config/LEV/timetravel/jobs/<job_id>/`
- 6 handoff artifacts in `.lev/pm/handoffs/tt-research-*.md`

## Validation

- [ ] Search returned at least 1 source
- [ ] Synthesis includes executive summary and key findings
- [ ] Report follows lev-research template structure
- [ ] Session directory contains all expected files
- [ ] Job record created and retrievable via `timetravel job list`
- [ ] All 6 handoff files created

## Usage

```bash
/workflow tt-research "state of AI agent frameworks 2026"
/workflow tt-research "rust vs go for CLI tools" --strategy academic
/workflow tt-research "trending AI on twitter" --strategy social
/workflow tt-research "comprehensive LLM evaluation" --depth deep
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
You are the prompt-architect-enhanced specialist for workflow-tt-research, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

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
