---
name: workflow-tt-adapter-add
description: Scaffold, implement, test, and register a new timetravel research adapter. Invoke with /workflow tt-adapter-add.
skill_type: workflow
category: process-workflow
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
---

# Workflow: Timetravel Adapter Add

Add a new research adapter to `~/digital/leviathan/plugins/timetravel/`.

Every step spawns a **fresh subagent** (poly sparkle pattern). State flows only through handoff artifacts at `.lev/pm/handoffs/tt-adapter-add-*.md`.

## Trigger

- User wants to add a new search/research API as a timetravel adapter
- `/workflow tt-adapter-add <adapter-name> "<api-description>"`

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `adapter_name` | yes | Kebab-case adapter identifier (e.g. `serper`, `you-com`) |
| `api_description` | yes | Brief description of the API and its search endpoint |
| `api_docs_url` | no | URL to API documentation |
| `env_key` | no | Override env var name (default: `<ADAPTER_NAME>_API_KEY`) |

## Steps

### Step 1: Research API

**Agent Type**: Explore
**Skills**: `skill://lev-research`
**Research**:
- Read API docs at `api_docs_url` (if provided) or search for `"<adapter_name> API documentation"`
- Read the reference adapter: `~/digital/leviathan/plugins/timetravel/src/adapters/brave.ts`
- Read the adapter interface: `~/digital/leviathan/plugins/timetravel/src/adapter.ts`
- Examine 2-3 existing adapters in `~/digital/leviathan/plugins/timetravel/src/adapters/` for patterns

**Action**:
- Document: base URL, auth method, request params, response shape, rate limits
- Map response fields to `Source` interface (`title`, `url`, `snippet`, `sourceType`)
- Identify capabilities: `search`, `extract`, `news`, `video`, etc.

**Handoff**: `.lev/pm/handoffs/tt-adapter-add-1-research.md`
```yaml
api_base_url: https://...
auth_method: header | query | bearer
env_key: <KEY_NAME>
capabilities: [search, ...]
response_mapping:
  title: <path>
  url: <path>
  snippet: <path>
rate_limits: <description>
```

---

### Step 2: Scaffold

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoff from Step 1
- Read `~/digital/leviathan/plugins/timetravel/src/adapters/brave.ts` as template

**Action**:
- Create `~/digital/leviathan/plugins/timetravel/src/adapters/<adapter_name>.ts`
- Copy BraveAdapter structure, rename class to `<AdapterName>Adapter`
- Set `name`, `envKey`, `capabilities` from handoff
- Leave `search()` body as `// TODO: implement in Step 3`

**Handoff**: `.lev/pm/handoffs/tt-adapter-add-2-scaffold.md`
```yaml
file_created: src/adapters/<adapter_name>.ts
class_name: <AdapterName>Adapter
```

---

### Step 3: Implement

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoffs from Steps 1 and 2
- Read the scaffolded file

**Action**:
- Implement `isAvailable()` — check env var
- Implement `search(query)` — HTTP call to API, map response to `SearchResult`
- Implement `extract?(urls)` if API supports content extraction
- Use `axios` for HTTP (already a project dependency)
- Handle errors: catch and return `{ sources: [], duration, adapter: this.name }`

**Handoff**: `.lev/pm/handoffs/tt-adapter-add-3-implement.md`
```yaml
file_modified: src/adapters/<adapter_name>.ts
methods_implemented: [isAvailable, search, extract?]
status: complete
```

---

### Step 4: Register

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read `~/digital/leviathan/plugins/timetravel/src/adapters/index.ts` for export pattern
- Read `~/digital/leviathan/plugins/timetravel/src/strategy.ts` for strategy adapter lists

**Action**:
- Add import + export to `src/adapters/index.ts`
- Add adapter instance to `createAllAdapters()` array
- Optionally add adapter to relevant strategies in `STRATEGIES` constant if appropriate

**Handoff**: `.lev/pm/handoffs/tt-adapter-add-4-register.md`
```yaml
files_modified: [src/adapters/index.ts, src/strategy.ts]
strategies_updated: [<list or none>]
```

---

### Step 5: Write Tests

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read existing test files in `~/digital/leviathan/plugins/timetravel/tests/`
- Read handoffs from Steps 1-4

**Action**:
- Add adapter tests to `tests/adapters.test.ts` (or create `tests/adapters/<adapter_name>.test.ts`)
- Test: `isAvailable()` returns boolean
- Test: `search()` returns valid `SearchResult` shape
- Test: error handling returns empty sources
- If live test file exists (`tests/adapters.live.test.ts`), add a live smoke test

**Handoff**: `.lev/pm/handoffs/tt-adapter-add-5-tests.md`
```yaml
files_created: [<test files>]
test_count: <n>
```

---

### Step 6: Run Tests

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoff from Step 5

**Action**:
- Run `cd ~/digital/leviathan/plugins/timetravel && pnpm test`
- Run `cd ~/digital/leviathan/plugins/timetravel && pnpm build`
- Verify `timetravel status` shows new adapter (available if key set, unavailable if not)
- Verify `timetravel adapters` includes the new adapter in JSON output

**Handoff**: `.lev/pm/handoffs/tt-adapter-add-6-tests-run.md`
```yaml
test_result: pass | fail
build_result: pass | fail
adapter_visible: true | false
failures: [<list if any>]
```

---

### Step 7: Document

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoffs from all previous steps
- Read `~/digital/leviathan/plugins/timetravel/README.md` (if exists)
- Read `~/.agents/skills/lev-research/SKILL.md` for tool manifest table

**Action**:
- Update README.md (or create if missing) with adapter entry
- Add env var to `.env.example` if it exists
- Update `lev-research` SKILL.md tool manifest table with new adapter row
- Log final summary

**Handoff**: `.lev/pm/handoffs/tt-adapter-add-7-document.md`
```yaml
files_modified: [README.md, .env.example, lev-research/SKILL.md]
adapter_name: <name>
status: complete
```

## Outputs

- New adapter file: `src/adapters/<adapter_name>.ts`
- Updated registry: `src/adapters/index.ts`
- Test coverage: `tests/adapters/` or inline
- Documentation updates
- 7 handoff artifacts in `.lev/pm/handoffs/tt-adapter-add-*.md`

## Validation

- [ ] `pnpm build` passes with zero errors
- [ ] `pnpm test` passes (all existing + new tests)
- [ ] `timetravel status` shows adapter in list
- [ ] `timetravel search "test" --adapter <name>` returns results (if key available)
- [ ] Adapter implements `ResearchAdapter` interface correctly
- [ ] All 7 handoff files created

## Usage

```bash
/workflow tt-adapter-add serper "Google SERP API via serper.dev"
/workflow tt-adapter-add you-com "You.com AI search API" --api-docs https://api.you.com/docs
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
You are the prompt-architect-enhanced specialist for workflow-tt-adapter-add, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

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
