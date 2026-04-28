---
name: propose
description: "Write or update a task's dna.yaml + execution.yaml. The Plan lane verb."
triggers:
  - propose
  - define
  - frame
---

# /propose — Lifecycle Transition: Plan Lane

Write the authored root for a task: `dna.yaml` (what) + `execution.yaml` (how).
Pattern: **cascade** (ordered derivation chain). Gate: **frame_complete_gate**.

## When to Use

- After `/capture` or `/interview` converges (ambiguity <= 0.2)
- When crystallizing a discussed idea into an executable task
- To update an existing task's definition or execution plan

## Protocol

### Step 1: Detect Mode

```
target = .lev/tasks/<task-id>/
if target/dna.yaml exists → UPDATE mode (read existing, merge delta)
else → CREATE mode (gather from scratch)
```

### Step 2: Gather Context (CREATE) or Load Existing (UPDATE)

For CREATE, extract from conversation / captured artifacts:
- **intent** — one sentence: what does this task accomplish?
- **acceptance** — list of concrete pass/fail criteria (minimum 1)
- **constraints** — list of boundaries, budget limits, scope fences
- **entity_kind** — from `dna/entities.yaml` types
- **lifecycle_target** — target state after completion

For UPDATE, read existing `dna.yaml`, identify the delta, merge.

### Step 3: Write dna.yaml

```yaml
# .lev/tasks/<task-id>/dna.yaml
ontology: <from dna/graph.yaml>
intent: "<one-sentence purpose>"
entity_kind: <type from dna/entities.yaml>
lifecycle_target: <target state>
acceptance:
  - "<criterion 1>"
  - "<criterion 2>"
local_refs: [<paths to related specs, designs, plans>]
local_constraints:
  - "<constraint 1>"
```

### Step 4: Write execution.yaml

```yaml
# .lev/tasks/<task-id>/execution.yaml
topology: <one of 8 patterns — see below>
runtime_profile: <profile name>
validation_chain:
  - gate: frame_complete_gate
  - gate: convergence_gate
receipt_policy: append_only
checkpoint_policy: forward_only
budget:
  max_iterations: <N>
  timeout: <duration>
exit_conditions:
  - "<condition>"
```

**8 topology patterns** (from `dna/standards/metrics.yaml`):
`sequence` | `protocol` | `strategy` | `judgment` | `cascade` | `loop` | `fan_out` | `reducer`

### Step 5: Validate — frame_complete_gate

```
PASS if: dna.yaml.acceptance.length >= 1 AND execution.yaml.topology != null
FAIL: re-run /propose to complete the missing fields
```

### Step 5.5: Determinism Gate (MANDATORY)

`/propose` output MUST be Turing-complete before emit. An executor receiving
the proposal must be able to dispatch every stage without further human
decisions. No OR forks disguised as proposals.

**Scan for non-determinism before emit:**

| Pattern | Examples | Verdict |
|---------|----------|---------|
| Proposal-level OR fork | "either symlink or diff guard"; "(A) fix qmd or (B) fallback" | FORBIDDEN |
| Option list as acceptance | "pick one: symlink / hook / generator"; "options: a, b, c" | FORBIDDEN |
| Quantity hedge | "at minimum", "at least", "covers some of", "possibly including" | FORBIDDEN |
| Mechanism hedge | "via X, build step, or Y"; "one of symlink / hook" | FORBIDDEN |
| Name-level OR | stage id `qmd_repair_or_skill_route` | FORBIDDEN |
| Predicate-level OR | `eval: "x has_key 'a' OR has_key 'b'"` inside a T0 WASM gate | ALLOWED (boolean expression, not a choice) |
| Enumerated exhaustive list | "covers exactly these 20 invariants: [full list]" | ALLOWED (exhaustive != hedge) |
| Model fallback list | `final_boss_model defaults codex-5.4-xhigh; acceptable overrides: opus-4-7, composer-2` | ALLOWED (default + explicit override set) |

**When non-determinism is detected, loop until Turing-complete:**

```
1. RESEARCH — run Shell / Grep / Glob / Read to resolve via evidence.
   Examples:
   - "symlink or hook?"  → `ls -la .claude/skills .agents/skills` → if already symlinked, choice is decided.
   - "fix qmd or route around?" → `which qmd; npm list` → if external package, repair is out-of-scope.
   - "expression or fuzzy gate?" → `rg -n '^\s*eval:' corpus/*.yaml` → whatever the existing convention uses.

2. If research resolves → update the proposal deterministically, rescan.

3. If research does NOT resolve → /interview IMMEDIATELY.
   Use AskQuestion (or the user-facing question surface) with:
   - the specific fork
   - the evidence gathered
   - 2-N concrete options with trade-offs
   Do not emit the proposal with the fork still present.

4. After interview, update the proposal deterministically, rescan.

5. Loop until zero non-determinism patterns remain.
```

**Determinism gate rules:**

- A proposal with even ONE unresolved fork FAILS the determinism gate,
  regardless of how well-framed the rest is.
- Research before interview — cheap evidence beats expensive human time.
- Interview before emit — never emit a proposal that requires the executor to make proposal-level decisions.
- Rename any stage id containing "or" to the resolved choice (e.g.
  `qmd_tooling_repair_or_skill_route` → `docling_skill_rewrite_rg_primary`).

**What counts as "Turing-complete" for /propose output:**

- Every acceptance criterion has a single deterministic success test.
- Every cascade stage has a single `focus`, a concrete `touch` set, and a single `verify` command.
- Every mechanism choice is resolved (not "one of X/Y/Z").
- Every quantity is exact (not "at minimum N").
- Every default is explicit; override sets are enumerated if present.

### Step 5.6: Project DNA Awareness (MANDATORY when proposal ships rule sets)

When the proposal ships a **rule set** — invariants, gates, constraints,
policies, standards, validation semantics — it must land as (or extend) a
**DNA-backed registry**, not as Python literals, bespoke yaml, or prose.

"Baking the cake": `/propose` is the verb that ties rule sets to DNA. Future
`/exec`, `/capture`, `/work`, and `/ll` invocations all read DNA. A rule that
lives only in code is a rule that drifts.

**Discover DNA roots before proposing rule sets (lev-idiomatic keys):**

```
1. Read `.lev/config.yaml` (lev puts project config here, not top-level)
   and enumerate:
     - `paths.dna`          — primary DNA directory (single string)
     - `flows.roots[]`      — fractal-scanner roots for flows/schemas/gates
     - `contracts.<name>`   — declared contract surfaces with source + overlays
   Lev's canonical shape (from ~/lev/.lev/config.yaml):
     paths:
       dna: dna/
     contracts:
       canon:
         source: dna/contracts-canon.dna.yaml
         overlays: []
     flows:
       roots:
         - dna
         - plugins/*/flows
         - .lev/flows

2. If no `.lev/config.yaml` exists, fall back to conventional roots:
   - `dna/`            (top-level, typically normative contracts — canonical home)
   - `.lev/dna/`       (workspace-scoped — often derived projections, not normative)
   - `data/dna/`       (data-submodule DNA — often needs centralization upward)
   - `plugins/dna/`    (lev-style projection plugin; rare outside lev core)

3. For each root, enumerate `*.dna.yaml`, `*.meta.dna.yaml`, and a canonical
   index if present (e.g. `dna/contracts-canon.dna.yaml` with
   `canonical_contracts: []`). Report what exists.

DO NOT invent keys like `dna_roots:`, `flowmind_indexing:`, or
`canonical_contracts_ref:` at the root. Those are zero-consumer names.
Use `paths.dna`, `contracts.<name>.source`, `flows.roots`. If you need a
key that doesn't exist yet, check ~/lev for the convention before inventing.
```

**Proposal rules:**

- **Extend before create.** If an existing registry has the right shape
  and owner, extend it with a new `invariants:`/`constraints:` entry
  rather than spawning a new file.
- **If creating a new registry, ship the schema too.** The proposal includes
  one stage for the JSON Schema (`.lev/dna/schemas/<name>.schema.yaml`) and
  a meta-contract file (`<name>.meta.dna.yaml`) that validates the registry
  against the schema + parity to downstream consumers.
- **Index it.** If the project has a canonical index (e.g.
  `dna/contracts-canon.dna.yaml`), the proposal adds the new registry
  to `canonical_contracts[]` in the same stage that creates the registry.
  Unindexed DNA is non-normative and invites drift.
- **Structured steering, not prose.** Registries that fire on runtime
  violations should declare `on_fail[]` as a list of typed steering
  records, not a single prose string. Recommended kinds (adapt to domain):
  `direction`, `pointer`, `docling_lookup`, `workflow_ref`, `per_row_breadcrumb`,
  `stdout_filter`. This is the bi-directional-communication dogfood — the
  registry controls both the gate and the agent's feedback signal.
- **Python / TS / whatever is a RUNNER, not a HOLDER.** The proposal's
  implementation stage refactors consumers to load DNA at startup and
  iterate. Rule definitions inside code bodies are a smell.
- **Backrefs both ways.** WASM corpus entries, subagent prompts, test
  fixtures, and workflow skill sections all cite DNA ids. Meta-contract
  asserts parity.

**Patterns to emulate (read these before proposing):**

- `~/lev/dna/core/onboarding.dna.yaml` — constraints + failure_modes + runnable validation.script
- `~/lev/dna/gates.dna.yaml` — meta-contract validates the gates file itself (self-referential)
- `~/lev/context/schema/src/formal-verification.schema.yaml` — rich fallback_strategies + compliance enum schema
- `<project>/dna/contracts-canon.dna.yaml` — canonical_contracts[] as the index of truth

**Determinism × DNA awareness composition:**

| Proposal shape | DNA awareness verdict |
|---|---|
| "Add 9 Python function calls in `_semantic_invariants()`" | FAIL — invariants belong in a DNA registry |
| "Add 20 invariants to `data/dna/grounding-invariants.dna.yaml`" | PASS |
| "Write a new yaml at `config/validators.yaml`" | FAIL — bespoke yaml; use DNA conventions |
| "Extend `dna/safety-contract.dna.yaml` with 3 new constraints" | PASS — extending existing registry |
| "Embed JSON schema inline in the proposal" | FAIL — ship schema as a sibling file, reference it |

### Step 6: Advance

If `frame_complete_gate` AND `determinism_gate` AND (when applicable)
`dna_awareness_gate` pass, task state advances to `proposed` (next:
`/capture` resolves decision_point).

If any gate fails, stay in Plan lane. Report which gate failed, cite
research attempts, and — for determinism forks — open the interview
immediately. For DNA awareness failures, redirect the proposal to
extend/create a registry before re-emitting.

### Step 7: Show The Proposal

Do not stop at "task written." After writing or updating the task, render the
proposal back to the user in a compact execution-facing summary.

Required sections, in this order:

1. **DNA** — a few bullets covering:
   - intent / end state
   - acceptance highlights
   - key constraints / boundaries
2. **Execution** — a few bullets covering:
   - topology + runtime profile
   - stage/step highlights
   - key verifiers / exit conditions
3. **Exec Menu** — use the same menu shape as `/capture` Step 6 so the user can
   immediately see how the proposal would be executed

Rules:
- Keep DNA to **3-5 bullets max**
- Keep Execution to **3-5 bullets max**
- Keep the Exec Menu to **max 5 items**
- Prefer grouped/high-signal bullets, not field dumps
- Always show the actual task id/path when helpful
- If in UPDATE mode, summarize the **delta** first, then show the refreshed proposal
- Render each exec menu item as the **D′ card** (see Output Format below) — domain-forward, no file paths, no git-diff verbs

### Artifact specs (required for any artifact that lands on disk)

When a proposal ships a new **artifact class** (folder shape, file template,
directory convention), it must include a **disk-spec** in the proposal:

- **Shape**: required files + optional files + forbidden names
- **Fields**: required/optional fields per file + their types
- **Naming**: file/folder naming convention (e.g. flat `<name>.dna.yaml` vs folder `<name>/dna.yaml`)
- **Graduation**: when the artifact evolves (e.g. flat → folder at ≥3 concerns)
- **Validation**: how a machine verifies conformance

Inline templates in the exec menu preview are still powerful for humans — the
disk-spec is what the executor writes against. Both matter: the preview shows
intent, the disk-spec shows structure.

## KPIs (from dna/lifecycle-kpis.yaml)

| KPI | Weight | Move On |
|-----|--------|---------|
| frame_completeness | 0.35 | = 1.0 |
| determinism | 0.20 | = 1.0 (zero unresolved forks, zero hedges) |
| dna_awareness | 0.20 | = 1.0 when proposal ships rule sets (DNA-backed registry + schema + index) |
| acceptance_specificity | 0.15 | >= 0.8 |
| execution_readiness | 0.10 | >= 0.75 |

## Red Flags — STOP

If you catch yourself writing any of these into a `/propose` output, STOP and
loop back to Step 5.5:

- "either X or Y" / "one of X, Y, Z"
- "A or B" as a stage id, acceptance, or verifier
- "at minimum", "at least", "including but not limited to"
- "covers … and more" / "among others"
- "pick one: A / B / C" inside acceptance
- "can be X or Y" in a verify command
- Multiple candidate mechanisms listed in a single stage's `focus`
- Exec menu item that says "TBD" / "to be decided" / "depends on research"

**All of these mean: research first, interview if needed, then re-emit. Do
not ship a proposal that punts decisions downstream.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "The executor can pick" | Then /propose didn't finish its job. Deterministic or it's not a proposal. |
| "Both options are valid" | Then evidence should show which is already in place or conventional. Research. |
| "User will tell executor later" | That's an interview you should have opened before emit. |
| "Leaving flexibility for future" | Flexibility at propose time = ambiguity at exec time. Exit-conditions can evolve; mechanisms can't. |
| "At minimum covers the main cases" | List the exact cases. "Main" is a hedge, not a spec. |
| "The task is too complex to resolve" | Shard the task. Each shard must still be deterministic. |
| "Just put the rules inline, it's faster" | Rules inline in code == rules that drift. Use DNA. |
| "We don't need a schema for 3 rules" | Yes you do. Meta-contracts stay cheap at small scale and mandatory at large. Schema now. |
| "The registry doesn't need to be indexed" | Unindexed DNA is non-normative. Add it to canonical_contracts[] in the same stage. |

## HUD

End every `/propose` with the HUD line from `~/.claude/skills/_shared/graph-footer.md`.

## Output Format

Rendered output uses a **template-driven card shape**. Each exec menu item is
one card. File paths do NOT appear in the preview — they live in
`execution.yaml.stages[].write_scope` where the machine looks. The preview is
for humans: domain-forward, strategy-first, no git-diff verbs.

### Card Template (D′)

```md
## Proposal: <task-id>

### DNA
- <intent / end state>
- <acceptance highlight>
- <constraint / boundary>

### Execution
- <topology + runtime profile>
- <stage highlight>
- <verifier / exit condition>

## Exec Menu (N of M)
```

Then, per menu item (in a fenced code block so monospace alignment holds):

```
━ <N> ━ <Item Title>                                                                                [<S|M|L>]

   INTENT    <one-sentence purpose, human language>
   STRATEGY  <how you attack it — approach, not file list>
   TOUCHES   <domain areas separated by · — optional>
   VERIFY    <what proves it's done, plain English — optional>

   /<skill> · <adapter> · <model>    ›    unblocks  <S#> · <S#>
```

### Slot rules

- **Required on every card:** `INTENT`, `STRATEGY`, footer line
- **Optional:** `TOUCHES`, `VERIFY` (skip when strategy line already carries the signal)
- **Never shown:** raw file paths, git diff verbs (M/A/D), nested a/b/c bullets
- **Complexity tag** `[S]` / `[M]` / `[L]` at right end of header bar
- **Footer:** `/<skill> · <adapter> · <model>    ›    unblocks  <stage ids>`
- **Header bar width:** pad `━` to fill a natural terminal width; don't pre-wrap content at 60 chars

### Field vocabulary

| Slot | Use for | Do NOT use for |
|------|---------|----------------|
| INTENT | end state in one sentence | a task list |
| STRATEGY | approach (`copy-reshape → delete → retarget`) | file lists |
| TOUCHES | domain areas (`authoring rules · architecture scope shape`) | module names as paths |
| VERIFY | how done is proved (`validation still 5/1 baseline`) | code asserts |
| HOW (footer) | `/skill · adapter · model` — execution metadata | file-path hints |

### Examples

Small item (S):
```
━ 2 ━ Relocate core-invariants to horizontal rollup                                                 [S]

   INTENT    Move the 11 cross-cutting invariants from dna/core/ (module scope) to dna/architecture/core/
             (horizontal scope). Content unchanged, home changes.
   STRATEGY  Copy-reshape → delete original → retarget validation.
   VERIFY    validation from new location still 5 PASS / 1 FAIL · no dangling refs to old path

   /exec · direct · sonnet    ›    unblocks  S6
```

Large item (L):
```
━ 4 ━ Graduate core/flowmind to folder-mode (reference impl)                                        [L]

   INTENT    Prove the folder shape on the biggest module. Decompose flowmind.dna.yaml into index +
             invariants + spec + design + README, each file owning its concern.
   STRATEGY  Read existing DNA → split by concern → write 5 files → delete source → rerun validation.
   TOUCHES   flowmind module DNA · graduation pattern for the other 5 big modules · projection targets
   VERIFY    5 files exist · validation still green from new location · handlers/ paths match projection_targets

   /exec · codex · sonnet    ›    unblocks  orch/harness/poly/exec/event-bus graduation (later)
```

### Queue line (when Queue > 0)

```
Queue: N more items (<one-line bucket breakdown>)
```

Exec menu construction rules:
- Mirror `/capture` Step 6 menu shape and dispatch logic
- For `/propose`, menu items come from `execution.yaml` stages/steps
- Bundle related stages into one menu item when they share one execution lane
- Keep `adapter` and `model` distinct:
  - `adapter` = supported execution adapter (for example `direct`, `scout`)
  - `model` = reasoning tier used for that menu item (for example `haiku`, `sonnet`, `opus`)
- If a task uses a higher-level execution surface such as `pi` or `ralph`,
  represent that in `flow` or the item title/context, not as the adapter
- Do **not** default every item to the same adapter. Choose the adapter that
  matches the work shape, then choose the model separately
- If the task is not shovel-ready, the first menu item should be the missing
  framing/research action rather than pretending the task is executable
- If the task is shovel-ready, the first menu item should be the critical-path
  implementation batch

Adapter guidance:

| Work Shape | Preferred Adapter |
|------------|-------------------|
| Inventory / audit / repo scan / evidence gathering | `scout` or `pi` |
| Small direct task write / task artifact update | `direct` |
| Code implementation / integration lane | `codex` (or `direct` for tiny edits) |
| Review / verification / boundary enforcement | `claude-agent-sdk` |
| Fast evidence gathering / prior-art lookup | `scout` or `pi` |

Model guidance:

| Work Shape | Preferred Model |
|------------|-----------------|
| Fast evidence gathering / prior-art lookup | `haiku` |
| Standard implementation / integration | `sonnet` or `codex-5.4-xhigh` |
| Deep design / framing / tradeoff resolution | `opus` |
| Small deterministic task/file update | `default` |

Hard rules:
- Adapter is the execution mechanism. Model is the reasoning tier. Do NOT put
  `opus`, `haiku`, or `sonnet` in the adapter column.
- `pi` is a **scout-only adapter**. It does not run implementation, review, or
  direct-write lanes. If the menu item is anything other than scout-shaped
  (inventory / audit / prior-art / evidence / repo scan), `pi` is invalid —
  use `scout`, `codex`, `direct`, or `claude-agent-sdk` instead.
- `ralph` is a higher-level flow/orchestration, not an adapter. It belongs in
  the `flow` column.
- A menu where every entry says the same adapter is usually a smell — match
  the adapter to the work shape per item.

## Related

- `/capture` — upstream (resolves decision_point after propose)
- `/interview` — upstream (reduces ambiguity before propose)
- `/exec` — downstream (runs execution.yaml topology)
- `/work` — lifecycle router (may call /propose internally)
