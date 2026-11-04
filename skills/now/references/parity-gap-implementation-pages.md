# Parity Gap + Implementation Plan Publish Pages

Use this when the user asks to turn parity artifacts (scorecards, parity matrices, registry hooks, or capability-contract comparisons) into a published lev.now page with a gap analysis and implementation plan.

## Trigger examples

- "Did you go L3 parity? I wanna see that then make a gap analysis + impl plan ... make a skill://now page and publish it"
- "Publish a parity dashboard from the scorecard and plan"
- "Show extract/build/reject gaps with implementation steps"

## Required workflow

1. **Verify the source artifacts before writing the page.** Inspect the parity matrix/registry/scorecard and count rows by disposition (for example `extract`, `build`, `reject`). Do not infer L3 coverage from memory.
2. **Separate evidence from recommendations.** The page should distinguish:
   - observed parity rows and source paths,
   - gaps/risks,
   - implementation plan,
   - acceptance gates and validation commands,
   - open caveats.
3. **Preserve durable artifacts next to the page.** For published bundles, include a `plan.md` or equivalent source document alongside `index.html`/RenderSpec when the page is a plan, not just a visual dashboard.
4. **Handle requested external model runs honestly.** If the user requested a specific model/agent run and it cannot be executed, do not fabricate that output. Generate from verified local artifacts only if that still satisfies the task, and include a short caveat in the page/source docs saying which run was unavailable and what evidence was used instead.
5. **Use a reader-friendly structure.** Prefer compact hero + parity summary + gap cards + implementation phases + validation gates + source links. Avoid turning long analysis into a decorative KPI-only dashboard.
6. **Publish and verify live assets.** After publish, verify the live root URL and any sidecar assets such as `/plan.md` and `/render-spec.json` return HTTP 200 and contain distinctive terms from the artifacts.

## Reporting

For a publish request, the user-facing final answer should lead with the published URL. Keep caveats short and only include them if they affect trust in the artifact (for example, a requested model run could not be executed).