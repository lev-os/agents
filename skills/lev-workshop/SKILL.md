---
name: lev-workshop
description: |
  [WHAT] Workshop lifecycle for building and evolving plugins, hooks, and integrations
  [HOW] Four phases: intake (capture ideas), analysis (scope/approach), POC (build prototype), poly integration (promote to production targets)
  [WHEN] Use when developing new lev capabilities, promoting POCs to production, or systematically building hooks/plugins
  [WHY] Ensures systematic development from idea to production with quality gates at each phase

  Triggers: "workshop this", "analyze for workshop", "poc this", "integrate to poly", "workshop status", "build capability", "new hook"
version: 1.0.0
skill_type: workflow
category: process-workshop
extends: lev-lifecycle
tools:
  - lifecycle hooks (references/hooks.md)
  - claude-agent-sdk (for LLM decision points)
  - bd (for tracking workshop items)
storage:
  workshop_items: ~/lev/workshop/
  poc_staging: ~/lev/workshop/poc/
  integration_queue: ~/lev/workshop/integration/

lifecycle_integration:
  stage: all stages (workshop lifecycle)
  input_artifact: idea/requirement/integration request
  output_artifact: production-ready plugin/hook/integration
---

# Lev Workshop

The workshop is where ideas become capabilities. It's the factory floor for building hooks, plugins, and integrations that extend lev's functionality.

## Workshop Lifecycle

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   INTAKE    │ →  │  ANALYSIS   │ →  │     POC     │ →  │    POLY     │
│             │    │             │    │             │    │ INTEGRATION │
│ Raw idea or │    │ Understand  │    │ Build       │    │ Production  │
│ requirement │    │ scope &     │    │ working     │    │ deployment  │
│             │    │ approach    │    │ prototype   │    │ & routing   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
     │                   │                   │                   │
     ▼                   ▼                   ▼                   ▼
 config_loader     dependency_checker   checkpoint_manager   quality_gate
 error_handler     progress_reporter    error_handler        success_handler
                   quality_gate         quality_gate         escalation_handler
```

## When to Use

| Trigger | Action |
|---------|--------|
| "workshop this" | Start intake for new capability |
| "analyze for workshop" | Deep-dive on requirements |
| "poc this" | Build proof of concept |
| "integrate to poly" | Promote POC to production |
| "workshop status" | Show items in each phase |
| "what's in poc?" | List active prototypes |

## Phase Details

### Phase 1: Intake

**Purpose:** Capture raw ideas, requirements, or problems that need solving.

**Input:** Natural language description, error message, feature request, or observed pattern.

**Process:**
1. `config_loader` - Load relevant domain context
2. `error_handler` - If intake is from error, parse and classify
3. Classify intake type:
   - `hook` - Lifecycle hook meta-prompt
   - `plugin` - External integration
   - `pattern` - Reusable workflow
   - `fix` - Bug fix or improvement

**Output:** Workshop item in `~/lev/workshop/intake/`

```yaml
# ~/lev/workshop/intake/item-001.yaml
id: ws-001
type: hook
title: "Retry with circuit breaker"
source: "Observed repeated failures in CB3 scraping"
created: "2026-01-13T10:00:00Z"
status: intake
raw_input: |
  CB3 keeps hitting rate limits and retrying forever.
  Need a circuit breaker pattern.
```

### Phase 2: Analysis

**Purpose:** Understand scope, dependencies, and approach before building.

**Process:**
1. `dependency_checker` - What does this need?
2. `progress_reporter` - Track analysis progress
3. Research existing implementations
4. Define success criteria
5. `quality_gate` - Is analysis complete enough to proceed?

**Questions to answer:**
- What existing hooks/plugins does this interact with?
- What's the minimal viable implementation?
- What are the edge cases?
- How will we test it?

**Output:** Analysis document added to workshop item

```yaml
# Updated item-001.yaml
analysis:
  dependencies:
    - error_handler (hook)
    - checkpoint_manager (hook)
  approach: |
    1. Track failure count per operation
    2. Open circuit after N failures
    3. Half-open state for testing
    4. Auto-close after cooldown
  success_criteria:
    - Circuit opens after 3 failures
    - Half-open after 30s
    - Full close after 3 successes
  estimated_complexity: medium
  analysis_complete: true
```

### Phase 3: POC (Proof of Concept)

**Purpose:** Build a working prototype to validate the approach.

**Process:**
1. `checkpoint_manager` - Save state frequently during development
2. Build minimal implementation
3. `error_handler` - Handle development errors
4. Test against success criteria
5. `quality_gate` - Does POC meet criteria?

**Location:** `~/lev/workshop/poc/<item-id>/`

**POC requirements:**
- Must run standalone
- Must have basic tests
- Must document usage
- Must log decisions

**Output:** Working prototype with test results

```yaml
# Updated item-001.yaml
poc:
  location: ~/lev/workshop/poc/ws-001/
  files:
    - circuit_breaker.py
    - test_circuit_breaker.py
    - README.md
  test_results:
    passed: 8
    failed: 0
  demo_command: "python circuit_breaker.py --demo"
  poc_complete: true
```

### Phase 4: Poly Integration

**Purpose:** Promote POC to production across multiple integration targets.

**Process:**
1. `quality_gate` - Final validation before integration
2. Identify integration targets (poly = multiple destinations)
3. `success_handler` - Route to each target
4. `escalation_handler` - Handle integration failures

**Integration targets:**
- **lev-lifecycle** - New hook added to hooks.md
- **claude-agent-sdk** - Pattern added to patterns.md
- **Project-specific** - CB3, TimeTravel, josh-imessage, etc.
- **System** - `~/lev/plugins/` and project hooks for automated workflows

**Poly routing abstraction:**
```yaml
# Integration targets can register as recipients
integration_targets:
  lev_hooks:
    type: hook
    location: ~/.claude/skills/lev-lifecycle/references/hooks.md
    format: yaml_block

  agent_sdk_patterns:
    type: pattern
    location: ~/.claude/skills/claude-agent-sdk/references/patterns.md
    format: python_code

  cb3_tools:
    type: tool
    location: ~/cb3/src/tools/
    format: python_module

  timetravel_adapters:
    type: adapter
    location: ~/lev/research/timetravel/src/adapters/
    format: typescript_module
```

**Output:** Integrated capability with routing info

```yaml
# Updated item-001.yaml
integration:
  status: complete
  integrated_to:
    - target: lev_hooks
      location: ~/.claude/skills/lev-lifecycle/references/hooks.md
      section: "Hook 11: Circuit Breaker"
    - target: cb3_tools
      location: ~/cb3/src/tools/circuit_breaker.py
  routing_rules:
    - pattern: "error_handler returns retry && retry_count >= 3"
      route_to: circuit_breaker
  post_integration_hooks:
    - update_docs
    - notify_user
```

## Workshop Item Schema

```yaml
id: ws-XXX
type: hook | plugin | pattern | fix
title: string
source: string  # where this came from
created: timestamp
status: intake | analysis | poc | integrating | complete | archived

# Phase outputs
raw_input: string
analysis:
  dependencies: array
  approach: string
  success_criteria: array
  estimated_complexity: low | medium | high
  analysis_complete: boolean

poc:
  location: path
  files: array
  test_results: object
  demo_command: string
  poc_complete: boolean

integration:
  status: pending | in_progress | complete | failed
  integrated_to: array
  routing_rules: array
  post_integration_hooks: array

# Metadata
bd_issue: string  # linked bd bead
related_items: array
tags: array
```

## Process Tracking

Workshop items are tracked in bd for visibility across sessions:

```bash
# Create bd issue for workshop item
bd create "Workshop: Circuit Breaker Hook" -t feature -p 2 \
  -d "Build circuit breaker pattern for retry logic"

# Link workshop item to bd
# In item-001.yaml:
# bd_issue: ws-circuit-breaker-001

# Query workshop status
bd list --label workshop --status open
```

## CLI Commands

```bash
# Start new workshop item
lev workshop intake "Need circuit breaker for retries"

# Check workshop status
lev workshop status

# List items by phase
lev workshop list --phase poc

# Promote to next phase
lev workshop promote ws-001 --to analysis
lev workshop promote ws-001 --to poc
lev workshop promote ws-001 --to integration

# Run POC tests
lev workshop test ws-001

# Integrate to target
lev workshop integrate ws-001 --target lev_hooks

# Archive completed item
lev workshop archive ws-001
```

## Example: Building a New Hook

```bash
# 1. Intake
lev workshop intake "Error handler should support circuit breaker pattern"
# → Creates ws-001 in intake phase

# 2. Analysis
lev workshop analyze ws-001
# Agent asks questions, researches existing hooks
# → Adds analysis section, promotes to analysis phase

# 3. POC
lev workshop poc ws-001
# Agent builds prototype in poc/ws-001/
# → Creates files, runs tests, promotes to poc phase

# 4. Integration
lev workshop integrate ws-001 --target lev_hooks
# Agent adds to hooks.md, updates references
# → Routes to all configured targets

# 5. Complete
lev workshop complete ws-001
# Archives item, updates bd issue
```

## Integration with Claude Agent SDK

Workshop items that involve LLM decision points use the Claude Agent SDK:

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async def analyze_workshop_item(item_id: str):
    """Use agent to analyze workshop item requirements"""
    async for msg in query(
        prompt=f"""
        Analyze workshop item {item_id} for implementation:
        1. Read the raw input
        2. Identify dependencies on existing hooks/plugins
        3. Propose minimal implementation approach
        4. Define success criteria
        5. Estimate complexity
        """,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Grep", "Glob"],
            permission_mode="bypassPermissions"
        )
    ):
        if hasattr(msg, "result"):
            return msg.result
```

## Hooks Used Per Phase

| Phase | Hooks | Purpose |
|-------|-------|---------|
| Intake | config_loader, error_handler | Load context, parse errors |
| Analysis | dependency_checker, progress_reporter, quality_gate | Check requirements, track progress, validate completeness |
| POC | checkpoint_manager, error_handler, quality_gate | Save state, handle failures, validate prototype |
| Integration | quality_gate, success_handler, escalation_handler | Final validation, route to targets, handle failures |

## References

- `~/.claude/skills/lev-lifecycle/` - Parent lifecycle skill
- `~/.claude/skills/lev-lifecycle/references/hooks.md` - Hook meta-prompts
- `~/.claude/skills/claude-agent-sdk/` - Agent patterns for LLM integration
- `~/lev/workshop/` - Workshop storage

## Relates

### Master Router
- **Lev Master Router** (`lev/SKILL.md`) - Routes all lev-* skills
  Parent skill that dispatches to this skill based on keywords/context

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
You are the prompt-architect-enhanced specialist for lev-workshop, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

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
