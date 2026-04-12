---
name: workflow-tt-strategy-create
description: Design and implement a custom search strategy for the timetravel research library. Invoke with /workflow tt-strategy-create.
skill_type: workflow
category: process-workflow
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
---

# Workflow: Timetravel Strategy Create

Design and implement a custom search strategy in `~/digital/leviathan/plugins/timetravel/`.

Every step spawns a **fresh subagent** (poly sparkle pattern). State flows only through handoff artifacts at `.lev/pm/handoffs/tt-strategy-create-*.md`.

## Trigger

- User needs a custom adapter mix for a specific domain or use case
- Existing strategies (quick, full, deep, max, academic, social) don't fit
- `/workflow tt-strategy-create "<name>" "<description>" [--adapters a,b,c]`

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `strategy_name` | yes | Kebab-case strategy identifier (e.g. `legal`, `news-pulse`, `competitive-intel`) |
| `description` | yes | What this strategy is optimized for |
| `adapters` | no | Comma-separated adapter list override |
| `mode` | no | Override orchestration mode: `parallel`, `sequential`, `first-success` |
| `synthesizer` | no | Adapter to use for synthesis (e.g. `oracle`) |

## Steps

### Step 1: Research Use Case

**Agent Type**: Explore
**Skills**: `skill://lev-research`
**Research**:
- Analyze the strategy description for: domain, depth requirements, speed requirements, source types needed
- Read existing strategies: `~/digital/leviathan/plugins/timetravel/src/strategy.ts`
- Read available adapters: `~/digital/leviathan/plugins/timetravel/src/adapters/index.ts`
- Check adapter capabilities vs use case needs

**Action**:
- Classify use case: speed-optimized, depth-optimized, breadth-optimized, domain-specific
- Identify which source types matter: web, academic, social, news, code, legal, etc.
- Map source types to available adapters
- Determine if synthesis is needed (complex/comparative queries = yes)

**Handoff**: `.lev/pm/handoffs/tt-strategy-create-1-research.md`
```yaml
strategy_name: <name>
use_case_type: speed | depth | breadth | domain
source_types_needed: [web, academic, social, ...]
candidate_adapters: [<list with rationale>]
synthesis_needed: true | false
speed_requirement: fast | moderate | slow-ok
```

---

### Step 2: Audit Existing Strategies

**Agent Type**: Explore
**Skills**: None
**Research**:
- Read `~/digital/leviathan/plugins/timetravel/src/strategy.ts` fully
- Map each existing strategy: name, adapters, mode, synthesizer
- Identify gaps: what combinations are NOT covered

**Action**:
- Compare new strategy needs against existing 6 strategies
- Check for overlap: if >80% same adapters as existing, recommend extending instead
- Identify unique value proposition of new strategy
- Verify no name collision

**Handoff**: `.lev/pm/handoffs/tt-strategy-create-2-audit.md`
```yaml
existing_strategies:
  - name: quick
    adapters: [brave, tavily]
    mode: first-success
  - name: full
    adapters: [brave, firecrawl, perplexity]
    mode: parallel
  # ... all 6
overlap_with: <closest existing strategy or "none">
overlap_percentage: <0-100>
unique_value: "<what this strategy adds>"
proceed: true | false
```

---

### Step 3: Design Adapter Mix

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoffs from Steps 1-2
- Run `cd ~/digital/leviathan/plugins/timetravel && npx timetravel status` for current availability

**Action**:
- Select 2-5 adapters with explicit justification per adapter
- Consider: availability (prefer adapters with keys set), complementarity (diverse source types), reliability
- If user provided `--adapters` override, validate they exist and document rationale
- Define fallback behavior: what if primary adapters unavailable

**Handoff**: `.lev/pm/handoffs/tt-strategy-create-3-design.md`
```yaml
selected_adapters:
  - name: brave
    role: "primary web search, fast baseline"
  - name: exa
    role: "neural/semantic for deeper relevance"
  - name: perplexity
    role: "AI-synthesized supplementary"
fallback_adapters: [<optional fallback list>]
adapter_count: <n>
```

---

### Step 4: Define Orchestration

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoff from Step 3
- Read orchestration modes in `~/digital/leviathan/plugins/timetravel/src/strategy.ts` (`executeStrategy`)

**Action**:
- Choose mode based on use case:
  - `parallel` — best for breadth, depth (query all at once)
  - `sequential` — best for cascading refinement (each builds on previous)
  - `first-success` — best for speed (stop at first good result)
- Choose synthesizer if needed (typically `oracle` for complex queries)
- Document the full `Strategy` object shape

**Handoff**: `.lev/pm/handoffs/tt-strategy-create-4-orchestration.md`
```yaml
mode: parallel | sequential | first-success
synthesizer: oracle | null
strategy_object:
  name: <name>
  adapters: [<list>]
  mode: <mode>
  synthesizer: <name or null>
rationale: "<why this orchestration>"
```

---

### Step 5: Implement

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoff from Step 4
- Read `~/digital/leviathan/plugins/timetravel/src/strategy.ts` for exact insertion point

**Action**:
- Add new strategy to the `STRATEGIES` constant in `strategy.ts`
- Follow exact pattern of existing entries
- Ensure TypeScript types are satisfied

**Handoff**: `.lev/pm/handoffs/tt-strategy-create-5-implement.md`
```yaml
file_modified: src/strategy.ts
strategy_added: <name>
line_inserted_at: <approximate line>
```

---

### Step 6: Test

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoff from Step 5

**Action**:
- Run `cd ~/digital/leviathan/plugins/timetravel && pnpm build` — verify compilation
- Run `cd ~/digital/leviathan/plugins/timetravel && pnpm test` — verify no regressions
- Run `npx timetravel search "test query for <strategy_name>" --strategy <strategy_name>` — verify execution
- Record: adapters used, source count, duration, synthesis presence

**Handoff**: `.lev/pm/handoffs/tt-strategy-create-6-test.md`
```yaml
build_result: pass | fail
test_result: pass | fail
live_test:
  strategy: <name>
  adapters_responded: [<list>]
  source_count: <n>
  duration_ms: <n>
  has_synthesis: true | false
  status: pass | fail
```

---

### Step 7: Register and Document

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read all handoffs from Steps 1-6
- Read `~/.agents/skills/lev-research/SKILL.md` for strategy mapping table

**Action**:
- Update `lev-research` SKILL.md: add row to Strategy Mapping table
- Update `lev-research` SKILL.md: add row to CLI Usage section
- Update README.md if it exists
- Update any related skill files that reference strategy lists

**Handoff**: `.lev/pm/handoffs/tt-strategy-create-7-register.md`
```yaml
files_modified: [<list>]
strategy_name: <name>
documentation_updated: true
status: complete
```

## Outputs

- Updated strategy definition: `src/strategy.ts`
- Updated research skill: `lev-research/SKILL.md`
- Test verification artifacts
- 7 handoff artifacts in `.lev/pm/handoffs/tt-strategy-create-*.md`

## Validation

- [ ] Strategy compiles (`pnpm build` passes)
- [ ] All existing tests pass (`pnpm test`)
- [ ] New strategy executes via CLI
- [ ] At least 1 adapter responds with sources
- [ ] Strategy name doesn't collide with existing
- [ ] lev-research skill updated with new strategy mapping
- [ ] All 7 handoff files created

## Usage

```bash
/workflow tt-strategy-create legal "Optimized for legal research: case law, regulations, compliance"
/workflow tt-strategy-create news-pulse "Real-time news monitoring with social signal" --adapters brave,grok,hackernews --mode parallel
/workflow tt-strategy-create competitive-intel "Company/product competitive analysis" --synthesizer oracle
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
You are the prompt-architect-enhanced specialist for workflow-tt-strategy-create, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

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
