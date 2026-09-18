---
name: lev-audit
description: Run the Lev guard rulebook (dna/gates/guard-rulebook.yaml). `daily` runs the guards grep can be trusted with; `weekly` has an agent check every judgment-based rule with evidence and writes a receipt. Use on a schedule or before landing a large branch.
---

# /lev-audit [daily|weekly]

Grep is only allowed to be the last word where the rulebook says `keep-mechanical`.
Everything else is a rule an agent reads, checks with evidence, and signs.

## Inputs
- `~/lev/dna/gates/guard-rulebook.yaml` — families, guards, dispositions, `agent_evidence` per family.
- `~/lev/.lev/validation-gates.yaml`, `~/lev/dna/gates.yaml` — gate ids the rulebook points at.
- Scripts live in `~/lev/tooling/scripts/`.

## daily (default)
1. For every guard with `disposition: keep-mechanical`, run its script from `~/lev`. Also run `pnpm axes-check`.
   Guards may carry an `args` field; pass it (shell-globbed, from ~/lev) to the script.
2. Append one row per guard to `~/lev/.lev/state/audit/<YYYY-MM-DD>-daily.jsonl`
   (`{family, guard, disposition, mechanical, evidence}`).
3. Any failure: open a bd issue `audit: <family>/<guard> failed` with the command output. Do not fix.

## weekly
1. Do the daily run first.
2. For every guard with `mechanical+agent-review` or `agent-rule-only`, delegate one worker per **family**
   (sonnet or /codex-runner, never opus). Give the worker the family's `rule` and `agent_evidence` text verbatim.
   The worker must: run the script (if any) as a pre-filter, then gather the evidence the family names
   (import graph, live probe, doc diff, sampled plugins), and return `pass|fail` per guard with `file:line`
   or command output as evidence. A pass without evidence is a fail.
3. Append rows to `<date>-weekly.jsonl` with `agent` and `evidence` filled.
4. Every `agent: fail` → bd issue `audit: <family>/<guard>: <one-line finding>`.
5. Reply with a table: family · guards · mechanical · agent · issues opened. No prose beyond one line per failure.

## Rules
- Never edit code during an audit. Findings become bd issues.
- Never trust a regex pass for a judgment rule; say `n/a` for mechanical when the family says the script proves nothing.
- Unknown guard mechanism → mark `tbd` and add a row asking for classification; do not guess.
- Schedule: add to `~/lev/.lev/flows/lev-mgmt.schedule.yaml` (daily 09:00 `lev-audit daily`, Monday `lev-audit weekly`) — the same tick parity-scorecard uses.
