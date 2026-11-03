# Research / repo-intake pages with lev.now

Use this reference when a session turns a paper, repo family, or prior-art analysis into a published lev.now page.

## Durable pattern

1. **Preserve raw sources before analysis**
   - Save paper text/PDF/API metadata and fetched README/site pages under the intake workspace, e.g. `workshop/intake/<slug>/sources/`.
   - Keep source capture separate from generated analysis artifacts so provenance remains auditable.

2. **Split artifacts by job, then render a reader bundle**
   - Create concise markdown artifacts for:
     - paper intake summary
     - repo inventory with clone path, URL, SHA, and evidence quote/location
     - convergence/prior-art mapping
     - implementation plan / recommended disposition
   - Then embed or summarize them in a `sidebar-toc` RenderSpec. Do not force every source into decorative bespoke sections.

3. **Use subagents for independent evidence lanes when available**
   - Lane A: repo inventory and citation/evidence extraction.
   - Lane B: convergence against local prior art.
   - Lane C: lev.now rendering/publish constraints.
   - Parent agent should verify and write final artifacts/page.

4. **Recommended page structure**
   - Compact editorial hero: paper, official repo, disposition.
   - KPI row: fit, implementation effort, evidence confidence, risk.
   - Source inventory table: official/referenced repos, role, SHA, evidence.
   - Architecture/convergence diagram: target paper concepts mapped to local system primitives.
   - Implementation path: deterministic code vs LLM responsibilities.
   - Risks/pitfalls: prompt-only isolation, missing evaluator receipts, over-prescriptive orchestrator behavior.
   - Final decision / next steps.

5. **Render / QA / publish commands**
   - Render: `npx tsx plugins/now/src/cli.ts "$SPEC" --output "$SITE_DIR/index.html"`
   - QA if available: add `--qa --qa-width 1440` and repeat at mobile width.
   - Publish directory root, not just a loose HTML file, when possible:
     `bash /opt/data/agents/skills/here-now/scripts/publish.sh "$SITE_DIR" --title "<title>" --client lev-now`

## 1:1 embedded markdown gallery reuse

When the user asks for the same quality/layout as a previous analysis page, prefer cloning the prior lev.now RenderSpec frame rather than re-inventing the page from scratch:

1. Locate the prior spec in `~/.agents/levnow/` and reuse its `custom-html` shell, CSS, markdown renderer JS, search UI, copy button, and document-list behavior.
2. Replace only the hero copy, metric pills, metric cards, and embedded `docs` array with the new artifact set.
3. If the old JS embeds `const docs = [...]`, parse the first top-level array safely instead of doing brittle string splits on a specific delimiter. Then preserve the renderer/search/copy code after the array.
4. Keep the same compact hero + metric row + toolbar + sidebar doc list + document pane layout when the user explicitly requested 1:1 continuity.
5. Verify locally with `agent-browser` and a search for a distinctive embedded-analysis term, not just by checking that the HTML file exists.

## Live publish verification

After publishing, verify the public URL on two layers:

1. Fetch the deployed HTML into a temporary file and search for title plus distinctive embedded terms. Avoid unsafe `curl | python` patterns; write with `curl -o` first, then inspect.
2. Open the live URL with `agent-browser`, confirm the accessibility snapshot shows the hero/sidebar/document pane, and use visual inspection for the first viewport.
3. `web_extract` may only surface the static shell/visible text and miss JS-embedded markdown; use it as a smoke check, not as the only proof that the embedded markdown bundle deployed.

## Pitfalls

- Do not publish from working notes alone. Write durable artifacts first, then render from them.
- Do not treat a cloned repo as paper-cited unless source evidence supports it; mark extra support repos separately.
- Do not encode transient setup failures as lasting rules. If screenshot QA tooling is unavailable, fall back to browser inspection and report the fallback, but do not claim lev.now QA is generally broken.
- Keep local paths out of the final user-facing publish response when a public URL is produced.
