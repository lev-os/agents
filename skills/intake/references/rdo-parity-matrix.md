# RDO and L3 parity matrix checkpoint for Lev intake

When an intake target is classified as `extract`, do not stop at a narrative analysis report. Add a refinement decision object (RDO) and an L3 parity matrix before closing.

## Required checkpoint

1. Preserve/capture the raw source first, then analyze.
2. Produce the analysis report with a clear recommendation.
3. If the disposition is `extract`, add an RDO section to the analysis report with:
   - kind/disposition
   - observations
   - future-state links
   - queued intent or follow-up link
   - conflicts/risks
   - recommended delta
   - validation plan
   - traceability/provenance
4. Create or update the canonical parity target under `.lev/pm/parity/<target>.yaml` with L3 feature rows.
5. Register the target in `.lev/pm/parity/index.yaml` when required by the local parity registry.
6. Regenerate parity projections/reports with the repo-local parity scorecard tool.
7. Verify that the new target parses, appears in generated scorecard/index outputs, and has no unclassified rows. If the full registry check is blocked by an unrelated pre-existing repo issue, report that precisely instead of calling the whole check green.

## Pitfall

A brief/recommendation alone is incomplete for extract-style Lev intake when the local playbook requires RDO + parity matrix artifacts. The user explicitly treats missing RDO or parity rows as not following the intake instructions.