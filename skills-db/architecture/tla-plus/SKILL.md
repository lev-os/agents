---
name: tla-plus
description: Use when learning or applying the TLA+ ecosystem end-to-end: selecting VS Code, Toolbox, or CLI; choosing PlusCal vs raw TLA+; writing specs above the code level; structuring properties and cfg files; running SANY, TLC, Apalache, or TLAPS; debugging counterexamples; checking refinement; validating traces; or mining the official examples corpus.
---

# TLA+ Ecosystem Workflow

TLA+ is for precise behavioral models, not code transcription. Stay finite, keep the model smaller than the implementation, and use the checker that matches the question.

```yaml
steps:
  - id: route_slice
    action: Route the request to one primary TLA+ slice
    instruction: |
      Pick exactly one primary route:

      | Route | Use it when | Load first |
      |-------|-------------|------------|
      | learn | You need a study path or orientation | references/learning.md |
      | setup | You need editor, CLI, or install guidance | references/tools.md |
      | model | You are drafting or revising a spec | references/modeling.md |
      | config | You are writing or fixing `.cfg` files, assumptions, invariants, or properties | references/properties-and-config.md |
      | tlc | You are running explicit-state checking with TLC | references/tools.md |
      | debug | TLC or a property failed and you need to isolate the cause | references/debugging.md |
      | refine | You need refinement, stuttering, or trace validation | references/refinement-and-traces.md |
      | prove | You need TLAPS or Apalache guidance | references/proof-and-symbolic.md |
      | examples | You need examples, case studies, or community pointers | references/examples-and-community.md |

      Write:

      ```text
      Route: <route>
      Why this route:
      ```
    validation: "Exactly one route is chosen and justified."
    on_failure: "Default to `model` for new specs, `debug` for failing checks, and `learn` for broad exploration."

  - id: choose_surface
    action: Choose the tool surface before touching the spec
    instruction: |
      Pick the working surface that matches the task:
      - VS Code extension for the fastest path to editing, PlusCal translation, TLC runs, completion, formatting, and PDF generation
      - CLI with `tla2tools.jar` for scripted use, non-Java integrations, and automation
      - Toolbox only if you specifically want that IDE surface; current official repo docs describe it as available but unmaintained

      CLI tools exposed by `tla2tools.jar` include:
      - `tla2sany.SANY` for parsing
      - `tlc2.TLC` for model checking
      - `tlc2.REPL` for expression evaluation
      - `pcal.trans` for PlusCal translation
      - `tla2tex.TLA` for LaTeX output

      Record:

      ```text
      Surface: VS Code | CLI | Toolbox
      Java:
      Commands or UI path:
      ```
    validation: "A concrete surface and run path are written down."
    on_failure: "Use VS Code for interactive work and CLI for automation."

  - id: choose_notation
    action: Choose PlusCal or raw TLA+
    instruction: |
      Use PlusCal when the artifact is mainly an algorithm or protocol with explicit control flow.

      Use raw TLA+ when the model is more relational, more modular, more mathematical, or more refinement-heavy than algorithmic.

      Keep the spec above the code level:
      - omit implementation detail that does not affect the behavior under study
      - model finite parameters first
      - prefer one bug-revealing model over one realistic but intractable model

      Write:

      ```text
      Notation: PlusCal | TLA+
      Why:
      Out-of-model details:
      ```
    validation: "Notation choice and omitted implementation details are stated."
    on_failure: "Reduce the problem to states, steps, and properties before adding syntax."

  - id: draft_model
    action: Draft the smallest useful behavior model
    instruction: |
      Start with:
      - state variables
      - initial state predicate
      - next-step relation or PlusCal algorithm
      - one type invariant
      - one safety property
      - one liveness or fairness property only if it matters now

      TLA+ skeleton:

      ```tla
      ------------------------------ MODULE Name ------------------------------
      EXTENDS Naturals, Sequences

      VARIABLES vars

      Init == ...
      Next == ...
      Spec == Init /\ [][Next]_vars

      TypeOK == ...
      Safety == ...
      =============================================================================
      ```

      If local process state is represented as a function, remember that all variables are still global. Add locality-style properties when accidental multi-process updates would be a bug.
    validation: "The draft has variables, Init, a transition relation, a spec shape, and at least one named property."
    on_failure: "Shrink the model to one queue, one process pair, one resource, or one failure mode."

  - id: separate_obligations
    action: Separate assumptions, invariants, properties, and config roles
    instruction: |
      Keep semantic levels straight:
      - `ASSUME` for constant-level facts about constants and static structure
      - `INVARIANT` or `INVARIANTS` in `.cfg` for state predicates checked in every reachable state
      - `PROPERTY` or `PROPERTIES` for temporal formulas, action properties, and refinement checks
      - `SPECIFICATION` in `.cfg` for full temporal specs; use `INIT` + `NEXT` only when checking safety without fairness

      Minimal `.cfg` skeleton:

      ```cfg
      SPECIFICATION Spec
      CONSTANTS
          N <- MC_N
      INVARIANTS
          TypeOK
          Safety
      PROPERTIES
          Liveness
      ```

      Keep expressions in `.tla` and use `.cfg` mostly to point at named formulas and constant replacements.
    validation: "The work distinguishes assumptions from invariants and temporal properties, and the config points at named formulas."
    on_failure: "If a formula mentions temporal operators like `[]`, `<>`, or `~>`, treat it as a property, not an invariant."

  - id: pick_engine
    action: Match the question to the checker
    instruction: |
      Use the right engine:
      - SANY for parse and early semantic sanity checks
      - TLC for explicit-state checking of finite executable models
      - Apalache for symbolic checking, bounded executions, and inductive invariants over fixed finite parameters
      - TLAPS for mechanically checked proofs, especially safety proofs after the model has stabilized

      Important limits:
      - TLC is mature and explicit-state
      - Apalache is symbolic and still experimental
      - TLAPS currently does not perform full temporal reasoning; treat it as strongest on safety-oriented proof obligations

      Record:

      ```text
      Engine:
      What question it answers:
      Why not the others first:
      ```
    validation: "A concrete engine is chosen with a question it is supposed to answer."
    on_failure: "Use SANY first, then TLC; escalate to Apalache or TLAPS only when that adds real signal."

  - id: check_small
    action: Run the smallest meaningful check first
    instruction: |
      Start with a tiny finite model:
      - minimize constants
      - keep collections and domains small
      - use one worker for small TLC runs when deterministic depth or diameter matters

      For each run, capture:

      ```text
      Model size:
      Engine:
      Property checked:
      Result:
      ```

      Do not add symmetry, view, alias, or advanced constraints until the base model is understood.
    validation: "Each run has a bounded model size and a recorded result."
    on_failure: "Reduce constants, remove optional constraints, and retry with the smallest failing configuration."

  - id: debug_counterexample
    action: Debug violations in the right order
    instruction: |
      If a `PROPERTY` fails:
      1. Remove the property and rerun invariants first.
      2. Fix any failing invariants before returning to liveness or refinement.
      3. Minimize the configuration until the smallest failing scenario remains.

      For every failure, summarize:

      ```text
      Check type: invariant | property | refinement
      Smallest failing configuration:
      Counterexample story:
      Suspected model mistake:
      Next spec change:
      ```

      Use trace output deliberately. TLC can dump traces, and trace validation only makes sense when the trace order and spec constants match reality.
    validation: "Every failure write-up includes a minimized configuration and a concrete next change."
    on_failure: "If the trace is too noisy, cut constants or remove non-essential behaviors until the failure becomes legible."

  - id: relate_behaviors
    action: Handle refinement, stuttering, and trace validation correctly
    instruction: |
      For refinement:
      - instantiate the abstract spec in the concrete one
      - use `WITH` when symbols differ
      - check refinement as a `PROPERTY`

      For stuttering:
      - `[Next]_vars` already allows stuttering
      - do not add explicit skip steps unless you have a very specific reason

      For trace validation:
      - use it only when the implementation trace is consistently ordered enough to compare against the spec
      - align CONSTANT values in the spec with the implementation that produced the trace

      Write:

      ```text
      Relation: refinement | stuttering | trace-validation
      Mapping or ordering assumption:
      Evidence target:
      ```
    validation: "The relation being checked and its mapping or ordering assumption are explicit."
    on_failure: "If you cannot explain the mapping between implementation events and spec actions, you are not ready to validate the trace."

  - id: mine_corpus
    action: Pull examples and ecosystem help from the official corpus
    instruction: |
      Use the corpus deliberately:
      - the `tlaplus/Examples` repo for validated examples and case studies
      - `specifications/SpecifyingSystems/` for book-aligned examples
      - manifest metadata and `.cfg` files to find examples using PlusCal, proofs, Apalache, symmetry, views, aliases, constraints, or known failing models
      - community channels when blocked

      Search patterns from the official examples repo:
      - `pluscal`, `proof`, `symbolic`, `deadlock failure`, `liveness failure`
      - `.cfg` keywords like `SYMMETRY`, `VIEW`, `ALIAS`, `CONSTRAINT`, `DEADLOCK`

      Record:

      ```text
      Example or corpus target:
      Why it matches:
      What to reuse:
      ```
    validation: "At least one concrete example or corpus source is named with a reuse reason."
    on_failure: "Start with the `SpecifyingSystems` examples or a beginner-friendly example from `tlaplus/Examples`."
```

## Reference Router

| Need | Load |
|------|------|
| Official corpus map and source ownership | `references/source-map.md` |
| Study order and learning ladder | `references/learning.md` |
| Editors, CLI, tools, and installation surfaces | `references/tools.md` |
| Modeling principles and PlusCal vs TLA+ | `references/modeling.md` |
| Assumptions, invariants, properties, and `.cfg` structure | `references/properties-and-config.md` |
| Starter snippets, trigger signals, and CLI patterns | `references/quick-reference.yaml` |
| Counterexample triage and failure debugging | `references/debugging.md` |
| Refinement, stuttering, and trace validation | `references/refinement-and-traces.md` |
| TLAPS and Apalache boundaries | `references/proof-and-symbolic.md` |
| Examples repo, case studies, and community | `references/examples-and-community.md` |

## Boundaries

- This skill covers the TLA+ ecosystem, not just the Lamport landing page.
- It prefers primary sources: Lamport pages, `tlaplus/*` repos, TLAPS docs, Apalache docs, and the official wiki.
- For Lean-specific proof-feedback loops, use `lean-formal-feedback-loop`.
