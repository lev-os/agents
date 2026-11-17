---
name: pov
description: >
  Point-of-view skill with three modes. Default (shape): zoom out, decompose, design the
  ideal state from intent and first principles, shown as pictures, without what exists;
  then, by complexity, a perspective pass for naming or competing views. Interactive:
  the original turn-manager protocol, unfold → synthesize → reduce → conclude, one turn
  per reply. Panel: many independent agents. Use for "pov", "zoom out", "decompose",
  "first principles", "ideal state", naming, decision synthesis and strategic alignment.
triggers:
  - pov
  - pov interactive
  - pov panel
  - zoom out
  - decompose
  - first principles
  - design from intent
  - ideal state
  - perspectives
  - synthesize options
  - strategic alignment
  - decision synthesis
  - conflict resolution
antitriggers:
  - factual verification
  - code review
  - adversarial audit
  - safety-critical cross-check
---

# /pov — Point-of-View Synthesis

## Modes

| The person says | Mode | What runs |
|---|---|---|
| `pov`, "zoom out", "decompose", "first principles", "ideal state" | **shape** (default) | [Shape](#shape-mode-default), then the perspective pass when the subject needs it |
| `pov interactive` | **interactive** | [The 4-turn protocol](#the-4-turn-protocol), one turn per reply, unchanged |
| `pov panel`, or "many agents", "independent perspectives" | **panel** | [Multi-agent panel variant](#multi-agent-panel-variant) |

JP set the modes on 2026-11-17: "If I say Interactive, then it does the 4 turns. By default, it does this, Zoom out, decompose 1st principles, ideal state. Uh, uses visual explanations, and then Depending on the complexity, it runs the [perspectives] like for naming and for different point perspectives."

## When to use

- Decision synthesis between 2-N options
- Strategic alignment across competing perspectives
- Terminology lockdown, IR design, vocabulary choice
- Conflict resolution where framing diversity > model independence
- What a thing is, where it lives or who owns it: shape first

## When NOT to use

- Facts under dispute → `/cdo` (model independence catches blind spots)
- Code review / audit → `/review` or `/security-review`
- Single-chain reasoning → `/think`
- Parallel model comparison → `/tribunal`

## Shape mode (default)

JP's order, in his words (2026-11-15): "decompose, zoom out, design from intent and first principles, look at the structure and pause (plain english words for everything, c1-c4 diagrams) - THEN, you look at prior art, levify it and make decisions". And: "use pov to zoom out and decompose from first principles first, then levify". He asked for this at least 18 times from 2026-10-08 to 2026-11-17 (count of his quoted words in the Leviathan decision records, 2026-11-17).

Do these steps in this order. Do not read the code, the records or prior art before step 6.

1. **Intent.** Say in one sentence what the person wants to be true when it is done. Say it as an outcome, not as a change to code.
2. **Zoom out.** Name the bigger system this belongs to, and who uses it: a person, a developer, an agent.
3. **Decompose.** List the capabilities the intent needs. Each one is a verb and a noun in plain words. No package names, no file names, no names that exist in the repo.
4. **Ideal state from first principles, as pictures.** Draw the capabilities as boxes, with C4 levels (context, then containers) and one sequence diagram for the main path. Show the pictures in the chat beside the words. Show only the ideal. Do not show what exists, and do not shape the boxes to fit it. Name the experts or practice behind each boundary (for example: hexagonal architecture, Cockburn; clean code, Martin; statecharts, Harel).
5. **Perspective pass, by complexity.** Choose one, and say which in one line:
   - **Simple** (one clear shape): skip it.
   - **Naming** (the boxes need names): run the 4 turns below in one reply, on the names only. Name by what a thing does; the most common industry term wins.
   - **Competing views** (two or more shapes are fair): run the 4 turns below in one reply, on the shapes, and show the winner's picture.
6. **Pause.** Show the picture and stop. Wait until the person agrees with it or changes it.
7. **Then levify.** Only now read what exists: the code, the records and prior art (`lev find`). Lay the ideal boxes over it. Show the gap: what to keep, what to move, what to delete, what to build.
8. **Then decide** on the gap, not on the code as it is.

Failure this mode prevents: starting from an inventory of the current code, so that the design copies what exists (Leviathan 2026-11-15: a state machine plan started from 50 machines in the code and showed no ideal).

**Exit gate:** the picture is shown and the person has answered. When the subject is a pure choice among options already agreed, say so in one line and use the 4 turns.

## The 4-turn protocol

**/pov is a turn manager, not a one-shot.** Each turn produces raw output, declares its successor, and stops. This is **unfolding** — prevents the model from simulating conclusions without doing the generative work. In interactive mode each turn is its own reply; in shape mode's perspective pass the four turns run in one reply, each under its own heading.

### Turn 1 — Unfold

Print 20-35 raw POVs. No synthesis. Each item:

- 1 sentence, ≤ 20 words
- Framed through a lens (persona or method)
- Marked `(safe)` | `(wildcard)` | `(tbd)`

**Lenses — pick 6-10 per invocation** from the review skill's lens list (`~/.agents/skills/review/references/lenses.md`): its Methods and Personas tables.

**Exit gate:** declare Turn 2 is next. Stop.

### Turn 2 — Synthesize

- **Conflicts** — find pairs/groups that genuinely oppose. Cite items by number. State the opposition evidenced.
- **Convergences** — find items where 3+ agree on the same direction. State the signal strength.
- **Resolution hints** — for each conflict, suggest "resolves as X" with evidence.

**Exit gate:** declare Turn 3 is next. Stop.

### Turn 3 — Reduce

Collapse to ONE of:

- **1 concrete sequence** — numbered steps with exit gates per step
- **1 axiom** — compressed invariant that makes the decision self-evident

**Exit gate:** declare Turn 4 is next. Stop.

### Turn 4 — Conclude

- **Top-expert recommendation** — name the domain, cite what practitioners in that field would do
- **Evidence anchors** — link back to Turn 2 convergences
- **Exit menu** — max 5 next-step options using the follow-up template
- **Zoom-out review** — one model wrote all the frames, so hand the Turn 3 reduction to the `review` skill: load the `review` skill by its name (the Skill tool with `review`; a host with no Skill tool opens ~/.agents/skills/review/SKILL.md), naming in its arguments the reduction, lens `zoom_out` (cold reader), and pov as the caller. Show the review skill's chat line (its Report section), or, when the review skill could not be loaded, the line 'review: could not run ({reason})' beside the recommendation, as advice. When review already ran on the same reduction in this work, cite that run's report file instead of a second run.

**Exit gate:** /pov cycle complete.

## Axioms

1. **Forced-framing diversity > persona identity** — one model producing N frames matches N models producing N similar frames, at 1/N the cost.
2. **Synthesis before enumeration** — 30 items without synthesis is noise; synthesis without 30 items is bias.
3. **Name theater before claiming rigor** — call out which thinking systems actually fired vs which were prompt-stems.
4. **Unfolding prevents simulation** — compressed turns let the model hallucinate conclusions without doing the generative work. Turn boundaries force real output.

## Multi-agent panel variant

When the user explicitly asks for many independent strategies, perspectives, or subagents, do not merely simulate the requested diversity inside the `/pov` cycle. Run a bounded **strategy panel**, then synthesize it:

1. **Ground the panel first.** Retrieve the current internal context and label huddle estimates, budgets, and uplift claims as hypotheses until verified.
2. **Assign non-overlapping lenses.** Useful set: product/design partner, operator workflow, investor/deal structure, SCAMPER, Blue Ocean/ERRC, CFO pre-mortem, architecture, JTBD/service design, founder-sales negotiation, and contrarian/opportunity cost.
3. **Dispatch in concurrency-safe batches.** Give each worker a self-contained brief, require a stance, discovery questions, bounded offer, trade-offs, and explicit no-go condition. Do not let workers mutate the same artifacts.
4. **List all lenses before the conclusion.** Preserve one short, attributable finding from every requested strategy; do not hide disagreement behind a generic synthesis.
5. **Synthesize around one decision, not ten ideas.** State: meeting objective, positioning sentence, discovery agenda, smallest paid next step, must-pass gates, prohibited promises, and close script.
6. **Keep capital and commercial tracks separate.** If a prospect is both investor and customer, do not let exploratory financing substitute for pilot payment, product commitments, exclusivity, data rights, or governance concessions.

Use this variant for strategic alignment; it does not replace factual verification or legal review.

## Costs & limits

- **Tokens**: ~2000-4000 per full cycle; a multi-agent panel is materially more expensive
- **Time**: 4 turns for the default cycle; panel synthesis adds worker round-trips
- **Blind-spot risk**: **high** for the default single-model cycle — do not use for facts under dispute

## vs other skills

| Skill | Use when |
|---|---|
| `/pov` | decision synthesis, framing diversity, strategic alignment |
| `/cdo` | multi-agent deliberation, facts under dispute, model independence matters |
| `/think` | structured single-chain reasoning |
| `/tribunal` | parallel model comparison with cross-agent consensus |

## Worked example

**2026-04-18 dogfood decision**: /pov decided whether to ship /pov.

- Capture: `.lev/pm/workstreams/lifecycle-engine/captures/20260418-pov-pattern-and-c2-licensing.yaml`
- 4 turns · 30 POVs → 4 conflicts + 5 convergences → 5-step sequence → Unix-philosophy conclusion
- Self-validation: /pov reasoning about /pov ship produced an actionable decision inline, single session, no subagents

## Provenance

Discovered organically during DNA-hardening work (2026-04-16 → 2026-04-19) as an emergent pattern in next-steps menus. Formalized after the user recognized the pattern outperformed /cdo for synthesis tasks at ~5% of orchestration cost.
