# Research/reference pages with source sidecars

Use this when a lev.now page summarizes research or architecture analysis and refers to a durable source artifact such as `phase2-research-synthesis.md`.

## Pattern

1. Render the page normally from the RenderSpec.
2. Run the visual QA gate. If the page is a dense research/reference artifact and the first viewport is mostly an oversized hero, prefer `meta.layout: "sidebar-toc"` over shipping a presentation-style hero. The first viewport should show the hero *and* useful downstream content.
3. Re-render and browser-QA the local file. Confirm:
   - first viewport exposes useful content, not only the hero;
   - sidebar/table-of-contents does not overlap content;
   - tables are readable at desktop width;
   - diagrams are not clipped and fullscreen controls are visible;
   - the pause/gate section remains explicit if the page should stop before design/implementation.
4. If the rendered page links or names a source artifact, publish a directory rather than a single HTML file:

```bash
SITE=~/.agents/levnow/<slug>-site
mkdir -p "$SITE"
cp ~/.agents/levnow/<slug>.html "$SITE/index.html"
cp /path/to/source-artifact.md "$SITE/source-artifact.md"
bash /opt/data/agents/skills/here-now/scripts/publish.sh "$SITE" --title "<Title>" --client lev-now
```

5. Verify the live site URL and every sidecar URL. Check for distinctive terms from both the page and sidecar.

## Verification notes

- Sidecar Markdown may be served through a viewer that HTML-escapes punctuation and expands markdown, so exact phrase checks can fail for strings with punctuation such as `Google v. Oracle` vs `Google v Oracle`. Verify multiple stable substrings instead, e.g. `Google`, `Oracle`, `Strangler Fig`, and `CapabilityRuntimePort`.
- If lev.now screenshot QA reports missing Playwright, do not encode that as a permanent failure. Fall back to browser visual QA for the current run and report the setup limitation only for that run.
