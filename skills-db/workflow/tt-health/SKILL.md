---
name: workflow-tt-health
description: Adapter health monitoring and diagnostics for the timetravel research library. Invoke with /workflow tt-health.
skill_type: workflow
category: process-workflow
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
---

# Workflow: Timetravel Health

Run health checks, diagnose failures, and optionally auto-fix issues across all timetravel research adapters at `~/digital/leviathan/plugins/timetravel/`.

Every step spawns a **fresh subagent** (poly sparkle pattern). State flows only through handoff artifacts at `.lev/pm/handoffs/tt-health-*.md`.

## Trigger

- User wants to check adapter health / availability
- Adapters are failing or returning unexpected results
- `/workflow tt-health [--fix auto|manual|interactive] [--adapter <name>]`

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `fix_mode` | no | `auto` (apply safe fixes), `manual` (report only), `interactive` (ask per fix). Default: manual |
| `adapter` | no | Scope to a single adapter instead of all |
| `verbose` | no | Include response samples in diagnostics |

## Steps

### Step 1: Scan Adapters

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read `~/digital/leviathan/plugins/timetravel/src/adapters/index.ts` for registered adapters
- Run `cd ~/digital/leviathan/plugins/timetravel && npx timetravel adapters` for JSON inventory
- Run `cd ~/digital/leviathan/plugins/timetravel && npx timetravel status` for dashboard view

**Action**:
- Build complete adapter inventory: name, envKey, capabilities, available status
- If `--adapter` specified, filter to that single adapter
- Count: total, available, unavailable

**Handoff**: `.lev/pm/handoffs/tt-health-1-scan.md`
```yaml
total_adapters: <n>
available: <n>
unavailable: <n>
adapters:
  - name: brave
    env_key: BRAVE_API_KEY
    available: true
    capabilities: [search]
  - name: valyu
    env_key: VALYU_API_KEY
    available: false
    capabilities: [search, extract]
```

---

### Step 2: Test Each Adapter

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoff from Step 1
- For each available adapter, prepare a test query

**Action**:
- For each available adapter, run: `npx timetravel search "test query" --adapter <name>`
- Record: response time, source count, error (if any)
- For unavailable adapters, record reason (missing env var)
- Test query: `"timetravel health check <timestamp>"` (unique per run)

**Handoff**: `.lev/pm/handoffs/tt-health-2-test.md`
```yaml
test_results:
  - adapter: brave
    status: pass | fail | skip
    response_time_ms: <n>
    source_count: <n>
    error: null | "<message>"
  - adapter: valyu
    status: skip
    reason: missing VALYU_API_KEY
```

---

### Step 3: Diagnose Failures

**Agent Type**: Explore
**Skills**: `skill://lev-research`
**Research**:
- Read handoffs from Steps 1-2
- For each failed adapter, read its source file: `src/adapters/<name>.ts`
- Check env vars: which are set vs missing
- Look for known error patterns: 401 (bad key), 429 (rate limit), timeout, DNS failure

**Action**:
- Categorize each failure:
  - `missing_env` — env var not set
  - `invalid_key` — 401/403 response
  - `rate_limited` — 429 response
  - `timeout` — request timed out
  - `api_error` — unexpected API response
  - `bug` — code error in adapter
- Recommend fix for each category
- Severity: critical (all adapters down), high (strategy broken), medium (degraded), low (optional adapter)

**Handoff**: `.lev/pm/handoffs/tt-health-3-diagnose.md`
```yaml
diagnoses:
  - adapter: <name>
    category: missing_env | invalid_key | rate_limited | timeout | api_error | bug
    severity: critical | high | medium | low
    details: "<description>"
    recommended_fix: "<action>"
    auto_fixable: true | false
overall_health: healthy | degraded | critical
```

---

### Step 4: Apply Fixes

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoff from Step 3
- Read fix_mode input (auto, manual, interactive)

**Action**:
- If `fix_mode = manual`: skip this step, report fixes needed
- If `fix_mode = auto`: apply all auto-fixable fixes
  - `missing_env`: prompt user to set env var (cannot auto-fix)
  - `invalid_key`: prompt user to check/rotate key (cannot auto-fix)
  - `rate_limited`: add backoff/retry if not present in adapter code
  - `timeout`: increase timeout config if adapter supports it
  - `bug`: attempt code fix if diagnosis is clear
- If `fix_mode = interactive`: present each fix and ask user before applying

**Handoff**: `.lev/pm/handoffs/tt-health-4-fixes.md`
```yaml
fixes_applied:
  - adapter: <name>
    fix: "<description>"
    result: success | failed | skipped
fixes_pending:
  - adapter: <name>
    fix: "<description>"
    reason: "requires user action"
```

---

### Step 5: Verify Fixes

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoffs from Steps 2-4
- Only run if fixes were applied in Step 4

**Action**:
- Re-run health checks for fixed adapters: `npx timetravel search "verify fix" --adapter <name>`
- Compare before/after results
- If still failing after fix: escalate with detailed error

**Handoff**: `.lev/pm/handoffs/tt-health-5-verify.md`
```yaml
verification:
  - adapter: <name>
    before: fail
    after: pass | fail
    notes: "<details>"
overall_improvement: "<X of Y fixed>"
```

---

### Step 6: Generate Report

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read all handoffs from Steps 1-5

**Action**:
- Compile health dashboard report:
  - Adapter status table (name, status, response time, source count)
  - Failure diagnosis summary
  - Fixes applied and results
  - Recommendations for manual fixes
  - Strategy impact analysis (which strategies are degraded)
- Save to `.lev/pm/handoffs/tt-health-6-report.md`
- Print summary to console

**Handoff**: `.lev/pm/handoffs/tt-health-6-report.md`
```yaml
report_type: health-dashboard
overall_health: healthy | degraded | critical
adapters_healthy: <n>/<total>
strategies_impacted: [<list>]
action_items: [<list>]
```

## Outputs

- Health dashboard report: `.lev/pm/handoffs/tt-health-6-report.md`
- Per-adapter test results
- Diagnosis and fix log
- 6 handoff artifacts in `.lev/pm/handoffs/tt-health-*.md`

## Validation

- [ ] All registered adapters were scanned
- [ ] Available adapters were tested with a live query
- [ ] Failures categorized with actionable diagnosis
- [ ] Fixes applied match fix_mode policy
- [ ] Verification re-ran for fixed adapters
- [ ] Final report includes strategy impact analysis
- [ ] All 6 handoff files created

## Usage

```bash
/workflow tt-health                          # Manual report only
/workflow tt-health --fix auto               # Auto-fix safe issues
/workflow tt-health --fix interactive        # Ask before each fix
/workflow tt-health --adapter brave          # Check single adapter
/workflow tt-health --verbose                # Include response samples
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
You are the prompt-architect-enhanced specialist for workflow-tt-health, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

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
