---
name: workflow-rust-plan
description: |
  Rust planning workflow that queries the rust-librarian knowledge base before code generation.
  Injects idiomatic patterns, known error pitfalls, and API references into the planning context.
  Feeds into the SDLC plan-execute-verify flow with an optional compile-fix loop.
disable-model-invocation: true
context: fork
agent: general-purpose
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
tags: rust, workflow, planning, sdlc, patterns, codegen
---

# Workflow: Rust Plan

A **5-step planning workflow** for Rust development tasks. Queries the `rust-librarian`
knowledge base to enrich plans with idiomatic patterns, then optionally feeds into the
SDLC plan-execute-verify loop.

## When to Use

- Before implementing any non-trivial Rust feature
- When writing Rust code involving ownership, lifetimes, async, or unsafe
- When planning a new Rust crate or module
- When you want compile-fix loop guardrails on generated Rust code

## Config

```yaml
# --- Required ---
task: <string>                  # What needs to be built

# --- Optional ---
crate_context: <string>         # Path to existing crate (reads Cargo.toml, src/)
target_crate: <string>          # Which crate to modify (for workspace projects)
compile_fix: <bool>             # Enable compile-fix loop (default: false)
max_fix_attempts: <int>         # Max compile-fix iterations (default: 3)
patterns_limit: <int>           # Max pattern results to inject (default: 5)
error_limit: <int>              # Max error examples to inject (default: 3)
skip_search: <bool>             # Skip knowledge base search (default: false)
plan_only: <bool>               # Stop after plan (default: false)
```

## Steps

### Step 1: Context Gathering

Understand what exists and what is needed.

```
1. Read task description
2. If crate_context provided:
   - Read Cargo.toml (deps, features, edition)
   - Read src/lib.rs or src/main.rs (public API surface)
   - Identify existing patterns (error handling, async, serde)
3. Extract key Rust concepts:
   - Ownership/borrowing implications
   - Concurrency model (sync, async, threads)
   - Error handling strategy (Result, anyhow, thiserror)
   - Trait requirements
   - Unsafe needs
```

### Step 2: Knowledge Base Query

Search `rust-librarian` for relevant patterns and pitfalls.

```
1. Query project-rust-patterns:
   - Search patterns matching task domain
   - "HTTP server" -> "async HTTP handler pattern"
   - "CLI" -> "clap derive pattern"

2. Query project-rust-books-guides:
   - Search relevant Rust Book chapters
   - References -> "borrowing and lifetimes"
   - Enums -> "pattern matching enum"

3. Query project-rust-error-examples:
   - Search common errors in task domain
   - Async -> "error[E0277] Future is not Send"
   - Borrowing -> "error[E0502] cannot borrow as mutable"

4. Collect top results (patterns_limit + error_limit)
5. Format as planning context block
```

**Search execution** (calls rust-librarian API or CLI):
```bash
# If search API running:
curl -s -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query":"<concepts>","projects":["rust-knowledge"],"framework":"rust","limit":5}'

# If using skill directly:
/rust-librarian search "<concepts>"
```

### Step 3: Plan Generation

Generate a Rust-aware implementation plan.

```
Synthesize into plan with sections:

## Approach
- Strategy and which patterns apply

## Crate Structure
- Files to create/modify
- Module organization, public API

## Dependencies
- Required crates + versions + feature flags

## Implementation Notes
- Ownership/lifetime considerations
- Error handling approach
- Concurrency model
- Known pitfalls to avoid (from error search)

## Validation
- cargo check, cargo clippy -- -D warnings
- cargo test strategy
```

If `plan_only=true` -> STOP here, return plan.

### Step 4: Execute

Implement the plan. Optionally use compile-fix loop.

```
1. Write code following plan
2. Run validation:
   - cargo check
   - cargo clippy -- -D warnings
   - cargo test

3. If compile_fix=true and check fails:
   a. Parse errors via: cargo check --message-format=json
   b. Extract error[E####] codes
   c. Query rust-librarian for each error code
   d. Apply fixes informed by knowledge base
   e. Retry up to max_fix_attempts
```

**Structured error parsing** (better than RustCoder's stderr scraping):
```bash
cargo check --message-format=json 2>&1 | \
  python3 -c "
import sys, json
for line in sys.stdin:
    try:
        msg = json.loads(line)
        if msg.get('reason') == 'compiler-message':
            code = msg['message'].get('code')
            if code: print(f'ERROR: {code[\"code\"]}')
            print(msg['message'].get('rendered',''))
    except: pass
"
```

### Step 5: Verify & Report

Validate and report results.

```
1. Full validation:
   - cargo check
   - cargo clippy -- -D warnings
   - cargo test
   - cargo doc --no-deps (if public API)

2. Report:
   - Files created/modified
   - Patterns applied (with source attribution)
   - Pitfalls avoided (error code references)
   - Test results

3. SDLC integration:
   - Update BD issue with evidence
   - Link to spec if exists
```

## SDLC Mapping

Maps to plan-execute-verify flow stages:

| Workflow Step | SDLC Stage |
|--------------|------------|
| Steps 1-3 | PROPOSE (context + search + plan) |
| Plan review | GATE (human or automated) |
| Step 4 | EXECUTE (implementation + compile-fix) |
| Step 5 | VERIFY (validation + report) |

## Examples

```bash
# Plan a feature with knowledge enrichment
/workflow rust-plan task="Implement concurrent rate limiter with token bucket"

# Plan with existing crate context
/workflow rust-plan task="Add WebSocket support" crate_context="crates/lev-gateway"

# Plan + execute with compile-fix
/workflow rust-plan task="Create CLI parser" compile_fix=true max_fix_attempts=5

# Plan only
/workflow rust-plan task="Design error handling for lev-reactive" plan_only=true
```

## Related

- `rust-librarian` -- Knowledge base skill (search + ingestion)
- `plugins/core-sdlc/` -- SDLC plan-execute-verify flow
- `core/flowmind/` -- FlowMind execution engine
- `os/agent/performance-engine/` -- Go docs system (architecture reference)
