---
name: flowmind-author
description: "Authors FlowMind .flow.yaml graphs with validate, fix, promote, and measure steps. Use when user writes or audits flows, fixes violations, or advances lifecycle quality."
triggers:
  - "write a flow"
  - "create a flow"
  - "validate flow"
  - "audit flow"
  - "fix flow"
  - "promote flow"
  - "flow quality"
  - "flowmind"
  - ".flow.yaml"
---

# /flowmind-author — Write, Validate, Fix, Promote, Measure

## Intent Router

| Intent | Route | What happens |
|--------|-------|-------------|
| **Write** | Authoring guide | Decision matrix + pattern catalog + golden rule |
| **Validate** | Audit flow | Deterministic probes + domain lenses + typed findings |
| **Fix** | Meta-prompt KB + constraint-iterative | Structured reasoning chain per violation |
| **Promote** | Promotion ladder | Typed PromotionDecision with gate evidence |
| **Measure** | Telemetry analysis | FlowTelemetry: tokens, cost, outcome, wall time |

## Write a Flow

Load the authoring guide first:

```bash
# Canonical reference
cat ~/lev/docs/design/design-flowmind-authoring-guide.md
```

### The Golden Rule

> If you can express the check as `bash -c "..." && echo pass || echo fail`,
> it is a `lev.validate` node. Full stop.

### The Two Primitives

| Primitive | Op | AI involved? |
|-----------|-----|-------------|
| **Validate** | `lev.validate` | No — shell command, exit 0/1 |
| **Exec** | `lev.exec` | Yes — prompt dispatched to adapter |

Everything else is topology over these two primitives.

### Required Fields

```yaml
name: my-flow           # unique identifier
entry: first_node       # where execution starts

policy:
  determinism: true     # enforce reproducibility

knobs:                  # parameterize the flow
  my_param:
    type: string        # MUST have type declaration
    default: value

nodes:
  first_node:
    type: action
    description: |      # instruction-shaped, not vague
      What this node does and why.
    op: lev.validate    # or lev.exec
    ...
```

### Flow Patterns (from authoring guide)

| Pattern | When | Shape |
|---------|------|-------|
| Linear gate chain | Sequential deterministic checks | A→B→C→done |
| Implement-validate loop | Iterative constraint engineering | impl→gate→review→impl (loop) |
| Fan-out analysis | Independent domain lenses | load→{lens1,lens2,lens3}→synthesize |
| Adversarial review | Red-team a constraint | verify→probe→validate→generate→report |

## Validate a Flow

Run the audit flow against any `.flow.yaml`:

```bash
# Audit all flows in the repo
lev exec "audit all flows" \
  --flow ~/.lev/flows/lev-flowmind-audit.flow.yaml

# Audit a specific directory
lev exec "audit sdlc flows" \
  --flow ~/.lev/flows/lev-flowmind-audit.flow.yaml \
  --set scan_path=plugins/sdlc/flows/

# Audit a single flow
lev exec "audit this flow" \
  --flow ~/.lev/flows/lev-flowmind-audit.flow.yaml \
  --set scan_path=path/to/my.flow.yaml
```

### What the Audit Checks

1. **Syntax**: Valid YAML, required fields, reachable nodes, terminal nodes
2. **Spec parity**: `op:` is `lev.validate` or `lev.exec`, branch keys valid, knobs typed
3. **Patterns**: Golden rule enforced, iteration bounded, prompts exist
4. **Telemetry**: Terminal nodes present, descriptions are instructional
5. **Parity**: Duplicate flows across plugin directories flagged

## Fix a Flow

When the audit finds violations, use the remediation meta-prompt pattern:

```
VIOLATION: {description}
FLOW: {flow_file}
CANON RULE: {gate_id}

REASONING CHAIN:
1. Read {flow_file}
2. Identify the specific violation
3. Determine fix strategy
4. Apply fix (touch ONLY the flow file)
5. Verify with deterministic command
```

For project-specific constraint flows (like NAAC), the meta-prompt KB lives at:
`.lev/flows/prompts/naac-auditr-revival/kb-remediation-metaprompts.md`

General FlowMind fixes:
- Missing `entry:` → add entry field pointing to first node
- Orphaned node → wire it into a branch path or remove it
- `lev.exec` for deterministic check → change to `lev.validate`
- Untyped knob → add `type:` declaration
- Missing prompt file → create at path referenced by `prompt:` field

## Promote a Flow

Flows follow the same promotion ladder as other Lev artifacts:

```
workshop (experimental)
  → poc (proven in one project)
  → plugin (proven across projects)
  → core (canonical)
```

Promotion requires a typed `PromotionDecision`:
- `gate_pass_ratio == 1.0` for all authoritative gates
- `blocking_findings == []`
- Evidence artifacts exist
- Transition is on an allowed edge

## Measure a Flow

After execution, check `FlowTelemetry`:
- `total_tokens` — cost signal
- `wall_time_ms` — performance signal
- `outcome` — green/red/partial
- `gate_pass_ratio` — quality signal

Over N runs, flows build a track record. Successful patterns get promoted;
failing patterns get mutated or retired.

## Related

| Skill | Relationship |
|-------|-------------|
| `/work` | Lifecycle router — calls flowmind-author for flow-related work |
| `/levloop` | Loop scheduler — flows are the execution unit per tick |
| `/dump` → `/capture` | Capture pipeline — proposed flows should pass audit before filing |
| `/lev-builder` | POC→core placement — uses promotion ladder |
| `/naac` | NAAC operator console — `naac-auditr-revival` is the reference implementation |

## Reference Documents

| Doc | Location | What |
|-----|----------|------|
| Authoring guide | `~/lev/docs/design/design-flowmind-authoring-guide.md` | Decision matrix + patterns |
| FlowMind spec | `~/lev/docs/specs/spec-flowmind.md` | Behavioral contract |
| Lifecycle design | `~/lev/docs/design/design-flowmind-lifecycle.md` | Observability events |
| Evolutionary learning | `~/lev/docs/_inbox/flowmind-evolutionary-learning.md` | Self-improving flow thesis |
| Meta-substrate | `~/lev/docs/design/design-meta-substrate-declaration-compiler-ir-runtime.md` | 4-layer doctrine |
| NAAC reference impl | `naac/.lev/flows/naac-auditr-revival.flow.yaml` | Working constraint audit |
| NAAC meta-prompt KB | `naac/.lev/flows/prompts/naac-auditr-revival/kb-remediation-metaprompts.md` | Remediation templates |
