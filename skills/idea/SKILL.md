---
name: idea
description: Use when shaping rough intent into one bounded outcome (crystallize, make it bounded), when scattered material needs a domain model, ontology, taxonomy or one normalized structure, or when resuming an idea in .lev.
---

# 🧙‍♂️ Idea — shaping

Idea owns **shaping**: it turns rough intent into one **bounded** outcome that
another worker can finish without rebuilding the conversation. The person says
"I think these things belong together", leaves, and comes back to the whole
answer, the work behind it and the evidence. They never assemble it from pieces.

Shape in **one pass**. Do the discovery yourself: read the code, the data, the
intakes and the web; run the smallest spike that could prove you wrong. Ask
the person only what evidence cannot settle and what changes the outcome; a
pass with zero questions is a good pass.

## Where Idea sits

| Layer | Owns |
|---|---|
| Lev / work | Sees that the outcome still needs shaping and routes here. |
| **Idea** | Moves the idea from `captured` through `crystallizing` and returns the evidence for `crystallized`: intent, target state, resolved mappings. |
| Domain skills | Answer the part of the shape they own. Idea **consults** them and keeps the answer. |
| Project | Declares the entity, its transitions and verifier. The person's readback (approve, clarify, defer, reject) is alignment, a separate axis from maturity. |
| Next owner | Takes the brief into planning (lev-plan), a spike (poc) or domain delivery. |

"Is it clear enough to act on?" is maturity, and Idea answers it. "Are we doing
it?" is the person's decision. A fully shaped idea can still be paused.

## Shape it

```yaml
steps:
  - id: orient
    action: Find the subject, its sources and any existing record
    instruction: |
      Use the supplied topic or the active conversation. Collect the person's
      own words for this subject, including earlier turns and forked threads;
      their repeated questions are evidence of the outcome they want. For a
      named existing idea, resolve and read its record first. When `lev` is
      installed, run `lev find "<3-6 topic words>" --type plan --type design
      --type decision --type idea --json`, then the same query with `--type idea`
      alone. Read the first call's first 5 cards, then the second call's first 5
      cards not already shown (decision 20261105-find-idea-writer-call). Then
      read each call's link lines (`result.data.links`: every record the first
      10 cards cite or that cites them, one line each, with its `summary` and
      the card it was reached from) and open the records that fit; lev find
      picks none of them. If the
      idea names a workstream, the second call is the first call with
      `--workstream <its id>` (decision 20261101-find-prior-art-workstream-call).
      If `lev` fails, say so in one line and `rg` over `.lev`. Follow the
      project's Lev context and workstream rules before artifact writes.
    validation: "Subject, the person's verbatim words, source basis and existing-record status are known."

  - id: infer
    action: State the intent and the ideal state
    instruction: |
      Name who must be able to do what when this works, and what the person
      keeps asking for that earlier answers gave only in part. Treat their
      suggested names, tools and schemas as clues; keep explicit decisions and
      constraints. Write current state and ideal state side by side. When two
      readings would produce materially different results, name both and
      look for the evidence that picks one.
    validation: "One plain sentence of intent, a beneficiary, and current vs ideal are written; any rival reading has the evidence that settles it or is a question."

  - id: investigate
    action: Trace one real case end to end
    instruction: |
      Inspect representative raw inputs, the current output, its real consumer,
      existing decisions and prior attempts. Pick one concrete case and follow
      it from source to consumer. Use prior-art for local precedent, research
      for external facts, intake for supplied URLs and files, and poc for a
      feasibility spike. Honor local-only and authorization limits. Record
      evidence you could not get and keep working on what it does not block.
    validation: "One real case is traced with file:line or source refs; every consequential claim has a source, an (assumption) tag or a named gap."

  - id: route_domains
    action: Detect the domains and consult each one
    instruction: |
      Read the case and decide which domains it touches; most touch several.
      For each, load the domain skill and use the routes in it that apply.
      Consult means you take its method and finding back into one answer;
      ownership of the shape stays here.
      - Things, identities, relationships, terms, ontology, taxonomy: domain
        modeling, done here with references/fundamentals.md.
      - Data, files, storage, fetching, system boundaries ("this is coding"):
        arch, plus references/fundamentals.md.
      - People's behavior, flows, screens ("there's also design"): ux.
      - How it looks, moves or is shown: creative.
      - A choice between viewpoints or a first-principles reset: pov.
      - Other domains: find the owner with skill-discovery and use its native
        methods and artifacts.
      Software design decisions that need the person's judgment go to interview
      as named questions, not as a whole interview.
    validation: "Every touched domain names the skill consulted and what it changed in the shape; a domain with no owner stays visible as a gap; when fundamentals.md applies, each of its sections is applied or skipped with a reason."

  - id: bound
    action: Bound the work
    instruction: |
      Give the smallest complete outcome, what is outside it, the sequence,
      the owner of each part, permitted changes, an acceptance check someone
      else can run, the evidence that would disprove the design, and the stop
      condition (check passes, budget ends, or a named dependency blocks).
      Show one concrete object, record, file layout or example when it makes
      the design testable.
    validation: "Another worker could start from the brief alone: outcome, scope, owner, check, stop condition and a concrete example are all present."

  - id: ask
    action: Ask only the highest-leverage questions
    instruction: |
      A question qualifies only when its answer changes the outcome or the
      authority, and investigation cannot settle it. Bundle every qualifying
      question into one turn, each with your recommended default and its
      consequence, and keep doing the work it does not block. Use the
      wizard-question shape below for a question. When none qualifies, proceed.
    validation: "Each question asked names why evidence could not settle it and the default taken if unanswered."

  - id: capture
    action: Save the idea when a write is authorized
    instruction: |
      Apply the save rules below. Resolve the project's idea home and owning
      writer from live declarations. Reuse an existing record and identity.
      On a new idea, check duplicates and load the owning template. Discover
      Lev read verbs through help; do not invent a write command. If no idea
      writer exists and direct authoring is authorized, write the YAML record
      at its declared home and read it back. That fallback claims no runtime
      admission. Keep revision and readback fields null until their real owner
      supplies them; capture permission belongs in the ledger.
    validation: "Every authorized change has a read-back artifact, or its unwritten content and blocker are in the ledger."

  - id: bind_domain
    action: Compare the idea with manifestation domains
    instruction: |
      Load references/domain-binding.yaml. Compare candidate terms, relations,
      outputs, constraints and checks with declared domain contracts. Retrieval
      proposes; evidence establishes fit. Keep partial coverage, alternatives
      and unknowns. If missing coverage is established, add a proposed plugin
      or extension dependency and route it through the plugin-build workflow
      within authorized scope; the idea stays unbound until that contract resolves.
    validation: "Each binding names its source basis and coverage; unknown coverage keeps a proposed dependency or gap."

  - id: return
    action: Return the brief and hand it to its next owner
    instruction: |
      Render the shaping brief below. Check the five lenses: each one is
      answered or named as unknown. Hand the brief to the project's declared
      next owner. If the person authorized execution, carry it through and
      report what actually passed.
    validation: "The brief names the outcome, evidence, unknowns, saved location and next owner; no readiness claim exceeds its evidence."
```

## The five lenses

Every brief accounts for all five, including unknowns. They check the shape;
they are not a question per turn. A supplied answer satisfies its lens.

| Lens | Question | Reveals |
|---|---|---|
| 🌊 Evolution | How did this come to be? | Origin, prior attempts, current situation |
| 🎯 Impact | What problem does it uniquely solve? | Beneficiary, outcome, why it matters |
| 🔗 Relationships | How does it connect to everything else? | Dependencies, related ideas, owners |
| 💎 Essence | What is the ONE fundamental truth? | The central idea in one plain sentence |
| 🚀 Paradigm | What assumption does it challenge? | A changed assumption, or an honest increment |

Design from intent (JP 2026-10-28): earlier captures and decisions are evidence
of what the person means, not the answer. Shape what should happen from first
principles; an explicit ruling still stands.

## The shaping brief

ADHD layout: outcome first, short blocks, a picture before prose. The first
screen (outcome, picture, bounded work, maturity) must stand alone; detail
follows it. Put long tables (full vocabularies, ledgers) in the saved record
and link them; when nothing may be saved, put them last.

<shaping-brief>
🧙‍♂️ **{Title}**: {intended outcome in one sentence}

**Current → ideal:** {current flow} → {ideal flow} (a small diagram when the flow crosses boundaries)

**Bounded work:** {smallest complete outcome} · out: {excluded} · owner: {who} · check: {runnable check} · stop: {condition}

**Maturity:** {crystallizing, or crystallized when intent, target state and mappings are all resolved} · **Alignment:** {the person's readback, or unaligned}

**One real case:** {the traced example, with refs}

**Domains consulted:**
- {domain}: {skill} → {what it changed}

**The shape:** {entities, structure, file layout or record; one concrete example}

**Would disprove it:** {evidence}
**Still cloudy:** {unknowns, each tagged (assumption) or (tbd)}
**Saved:** {artifact and write result, or unsaved}
**Next owner:** {lev-plan, poc, a domain skill, or the person's decision}
**Experts:** {domain}: {what a top expert would do} ({practice or source}); one line per domain
</shaping-brief>

Render the Markdown without the XML wrapper or unresolved placeholders.

## When a question qualifies

Use the wizard's voice for a qualifying question: a short acknowledgment, the
insight that makes the question matter, and real choices. Adapt the number of
choices to the question; do not pad to five.

<wizard-question>
🧙‍♂️ {What I found, and why this one needs you.}

**Question {N}: {One clear question}**

1. 🎯 **{Recommended path}** — {consequence and reason}
2. 🔗 **{Alternative}** — {consequence}
3. ✨ **{Other real option, only if it exists}** — {consequence}

**My recommendation:** {number and short reason}. **If you don't answer:** {default}.

**Expert opinions:** {field}: {what a top expert would say} ({source or practice}); one line per relevant field (JP 2026-11-04).

Pick one, combine, or tell me your own path.
</wizard-question>

- `3` selects that path; `1,2` combines compatible parts (show conflicts first); `3, but focused on X` keeps X.
- A new idea changes the map. Keep the old branch and the reason for the pivot.
- A playful or unclear shorthand needs a small clarification; it is not permission to select everything.

When the person asks to explore an idea together instead of handing it off, run
the same steps one question at a time with this template, and stop when the
requested idea work is complete.

## Save only within the active scope

Shaping stays inline unless the person asks to save or project instructions
require it. A read-only request keeps proposed changes unsaved. Use YAML for
idea records; write Markdown only when requested. Preserve concurrent edits and
use revision checks when available. For a save, resume or recovery, load
[the record contract](references/record-contract.md) and the project's owning
schema and template; [the bundled template](templates/idea.yaml) is a fallback.

An ontology names the things, their meanings, relationships and constraints.
Reuse an existing term when its meaning fits; keep a new term as a candidate
with its source and open question. Track intended entities even when their
targets do not exist; existence, maturity, alignment and domain binding are
separate facts, and unknown existence is `null`.

Track this ledger in session state; show its delta on a save, failed write or handoff.

| Source intent | Compiled intent | Preservation | Disk / memory | Artifact ref | Route | Blocker | Confidence basis |
|---|---|---|---|---|---|---|---|
| {person's goal or constraint} | {operational reading} | {preserved, approved narrowing, or gap} | {disk, memory, or both} | {ref or none} | {owner or unresolved} | {gap or none} | {evidence, assumption, or unknown} |

On a preservation gap, keep the original and repair the reading before advancing.
The idea record's `status` is its state as a goal: shaping, pursuing, paused,
reached or dropped; a new idea starts at shaping. A saved file is not proof the
goal is reached; completion belongs to its verifier.

## Recover and stop

When meanings conflict, restate the goal, the conflict and its consequence,
then ask one qualifying question; keep the earlier answer intact. When a lookup
or writer fails, keep the candidate, report the gap, and stop the dependent
action after one targeted recovery attempt. A failed question or missing
evidence is never approval.

Finish when the brief passes its own checks, or the requested save has a
read-back record and named gaps. Defer or reject when that is the person's direction.

## References

- [Fundamentals](references/fundamentals.md): load when the shape involves data, files, storage, an app, or a domain model.
- [Domain binding](references/domain-binding.yaml): load when capture needs a manifestation owner, a design link or a missing-domain dependency.
- [The original wizard](references/wizard-source.json): load when the person asks for historical wording. Old commands, labels, timers and claims are history; this skill governs.
- [Source map](references/source-map.json): load when auditing parity or the v1 adaptations.
