---
name: pov
description: >
  Single-model forced-framing diversity with inline synthesis. Turn-manager protocol:
  unfold → synthesize → reduce → conclude. Use for decision synthesis and strategic
  alignment. Cheaper than /cdo, richer than /think.
triggers:
  - pov
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

**/pov is a turn manager, not a one-shot.** Each turn produces raw output, declares its successor, and stops. This is **unfolding** — prevents the model from simulating conclusions without doing the generative work.

## When to use

- Decision synthesis between 2-N options
- Strategic alignment across competing perspectives
- Terminology lockdown, IR design, vocabulary choice
- Conflict resolution where framing diversity > model independence

## When NOT to use

- Facts under dispute → `/cdo` (model independence catches blind spots)
- Code review / audit → `/review` or `/security-review`
- Single-chain reasoning → `/think`
- Parallel model comparison → `/tribunal`

## The 4-turn protocol

### Turn 1 — Unfold

Print 20-35 raw POVs. No synthesis. Each item:

- 1 sentence, ≤ 20 words
- Framed through a lens (persona or method)
- Marked `(safe)` | `(wildcard)` | `(tbd)`

**Lenses — pick 6-10 per invocation:**

- `systems_thinking`, `first_principles`, `figure_storming`
- `10x_dev`, `elon_musk`, `karpathy`, `sam_altman`
- `buffet_bezos_dimon`, `einstein_turing`
- `jesus_gandhi_god`
- `pre_mortem`, `reverse_brainstorm`, `second_order`, `opportunity_cost`

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

**Exit gate:** /pov cycle complete.

## Axioms

1. **Forced-framing diversity > persona identity** — one model producing N frames matches N models producing N similar frames, at 1/N the cost.
2. **Synthesis before enumeration** — 30 items without synthesis is noise; synthesis without 30 items is bias.
3. **Name theater before claiming rigor** — call out which thinking systems actually fired vs which were prompt-stems.
4. **Unfolding prevents simulation** — compressed turns let the model hallucinate conclusions without doing the generative work. Turn boundaries force real output.

## Costs & limits

- **Tokens**: ~2000-4000 per full cycle
- **Time**: 4 turns, no subagent round-trip
- **Blind-spot risk**: **high** (single model) — do not use for facts under dispute

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
