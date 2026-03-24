# Intent Compiler Bootstrap

You are building a skill using the intent compiler pattern. A skill is not a document — it is an executable DAG declared in `dna.yaml`, walked by a CLI harness, with deterministic validation at each node.

## The Pattern

```
dna.yaml          → declares the graph (what nodes exist, how they connect)
nodes/*.md         → content at each node (loaded into LLM context one at a time)
bin/skill-step     → CLI that walks the DAG, tracks state, validates output
schemas/*.yaml     → contracts for what valid output looks like
```

The CLI communicates intent to the LLM (progressive disclosure — one node at a time).
The LLM communicates intent back by producing artifacts that match schemas.
The output of building a skill IS a new dna.yaml — the pattern is recursive.

  LLM → CLI: "I want to build a skill about database migrations" → CLI receives intent, walks the
  DAG, feeds the right node at the right time, validates output deterministically.

  CLI → LLM: Each node's content is a structured prompt. The CLI doesn't just echo text — it says
  "here's your context, here's your constraint, here's your output schema, go." The CLI is steering
   the LLM.

  LLM → CLI → LLM: The LLM produces a dna.yaml as OUTPUT. That dna.yaml IS the skill it just built.
   Which can then be compiled and run by the same CLI. The output is executable.

  Intent (natural language)
      ↓
  dna.yaml (structured declaration)
      ↓
  Runtime (CLI walks the DAG)
      ↓
  Artifacts (validated output)
      ↓
  dna.yaml (the artifact IS a new compilable program)

  It's an intent compiler. Natural language in, deterministic workflow out. The dna packet is the
  intermediate representation — like LLVM IR but for agent workflows. Human-readable,
  machine-executable, bidirectional.


## Example: dna.yaml

```yaml
name: db-migrations
version: 1.0.0
description: "Enforce backup-before-migrate and block direct prod migrations"
entry: intake

nodes:
  intake:
    description: "Classify the migration request"
    content: nodes/intake.md
    routes:
      execute: "User wants to run a migration"
      plan: "User wants to generate a migration plan"
      rollback: "User wants to undo a migration"
      prod_gate: "Any mention of production"
    validation:
      rule: "exactly one route selected"

  execute:
    description: "Run migration with mandatory preflight"
    content: nodes/execute.md
    requires: [intake]
    validation:
      rule: "backup file exists and is non-zero bytes"
      check: "ls -la $BACKUP_PATH | awk '{print $5}' shows > 0"
    on_failure: "Do not run migration. State which preflight check failed."
    next: deliver

  plan:
    description: "Generate migration plan with dry-run"
    content: nodes/plan.md
    requires: [intake]
    validation:
      rule: "plan file exists with at least one migration step"
    next: deliver

  rollback:
    description: "Undo migration via ORM rollback or backup restore"
    content: nodes/rollback.md
    requires: [intake]
    next: deliver

  prod_gate:
    description: "Hard block — no direct prod migrations"
    content: nodes/prod-gate.md
    requires: [intake]
    terminal: true
    validation:
      rule: "no migration command was executed against production"

  deliver:
    description: "Validate result and produce report"
    content: nodes/deliver.md
    requires: [execute, plan, rollback]
    terminal: true
    produces: report

anti_patterns:
  - excuse: "It's a simple migration, skip the backup"
    reality: "Simple migrations corrupt data too. Backup takes 10 seconds."
  - excuse: "Staging worked, prod will be fine"
    reality: "Staging and prod have different data. Always backup prod separately."
  - excuse: "I'll just run it quickly on prod"
    reality: "The prod_gate exists for this exact thought. Route there now."
  - excuse: "Rollback is built in, we don't need a backup"
    reality: "ORM rollbacks fail on data migrations. Backup is the safety net."
```

## BDD Requirements

```gherkin
Feature: Intent Compiler Skill Lifecycle

  Scenario: Skill has a valid dna.yaml
    Given a directory with dna.yaml
    When the CLI reads dna.yaml
    Then every node referenced in routes/next/requires has a matching entry in nodes
    And every node has a content path that resolves to a file on disk
    And every terminal node has validation.rule defined
    And the graph has no orphan nodes (every node reachable from entry)
    And the graph has no cycles (DAG property)

  Scenario: CLI walks the DAG
    Given a valid dna.yaml and a user request
    When the CLI starts at the entry node
    Then it loads nodes/{entry}.md into context
    And presents the node content to the LLM
    And waits for LLM output
    And validates output against the node's validation.rule
    And advances to the next node per routes or next

  Scenario: Report includes next node
    Given the CLI is at node N with $nextOnReport enabled
    When the LLM produces output for node N
    Then the CLI validates the output
    And appends the next node's content to the response
    And records metadata to XDG cache

  Scenario: Report does NOT include next node
    Given the CLI is at node N with $nextOnReport disabled
    When the LLM produces output for node N
    Then the CLI validates the output
    And returns only validation result
    And the LLM must call `skill-step next` explicitly

  Scenario: Validation fails
    Given the LLM output does not satisfy validation.rule
    When the CLI evaluates the output
    Then it returns the on_failure message
    And does NOT advance to the next node
    And increments the retry counter in XDG cache
    And after 3 retries, escalates to user

  Scenario: Skill produces a new skill
    Given the skill-builder is running
    When it reaches the scaffold node
    Then the LLM produces a dna.yaml for the NEW skill
    And the CLI validates the new dna.yaml against schemas/dna.schema.yaml
    And the new skill is a valid intent compiler (recursive)

  Scenario: XDG metadata tracking
    Given any skill invocation
    When a node completes
    Then the CLI writes to $XDG_CACHE_HOME/lev/skills/{name}/{session}.json
    And records: node_id, timestamp, retries, validation_result, duration_ms
    And the session file is append-only (no overwrites)

  Scenario: Anti-pattern detection
    Given a dna.yaml with anti_patterns defined
    When the LLM output contains text matching an excuse pattern
    Then the CLI flags it and includes the reality response
    And does NOT count it as a valid completion

  Scenario: Graph validation on load
    Given a dna.yaml
    When the CLI loads it
    Then it validates: no orphans, no cycles, all content paths exist
    And reports any structural errors before execution begins
    And refuses to run an invalid graph
```

## Directory Structure (what skill-builder produces)

```
{skill-name}/
├── dna.yaml              # The declaration — entry point, graph, schemas
├── nodes/
│   ├── intake.md         # Entry node content
│   ├── {route-a}.md      # Route-specific nodes
│   ├── {route-b}.md
│   └── deliver.md        # Terminal node
├── bin/
│   └── skill-step        # CLI harness (or symlink to shared one)
├── schemas/
│   └── {name}.schema.yaml  # Output validation schemas
└── anti_patterns.yaml    # Optional: extracted for reuse across skills
```

## How to Use This Bootstrap

1. Describe what the skill should do
2. The LLM produces a dna.yaml (the graph)
3. The LLM produces nodes/*.md (the content)
4. The CLI validates the graph (no orphans, no cycles, paths resolve)
5. Run it: `skill-step --skill {path} create`
6. The CLI walks the DAG, the LLM fills each node, validation gates enforce quality
