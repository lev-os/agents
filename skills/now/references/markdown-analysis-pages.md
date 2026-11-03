# Markdown Analysis Page Pattern

Use this when a session produces multiple markdown analysis artifacts and the user wants a shareable `now` page rather than separate files or a bespoke dashboard.

## Shape

- Keep each generated artifact as a first-class document with its original title.
- Build a RenderSpec with a compact hero, source inventory, and one reader section per artifact.
- Prefer `meta.layout: "sidebar-toc"` for multi-document bundles.
- Render document bodies as markdown-like HTML, not over-designed cards.
- Add local anchors and a search/filter control for long bundles.

## Publish verification

After publishing, verify the live URL directly and search/fetch for distinctive terms from the embedded analysis. Use both machine checks and a visual smoke test when available:

- fetch/search the live HTML or extracted page for several anchor terms from different embedded artifacts;
- open the live URL in a browser and confirm the reader/tabs/table/diagram are readable;
- exercise any custom search/filter controls and confirm results narrow/highlight as expected.

This catches pages that render the frame but omit the source documents, publish stale local output, or ship an interactive reader whose embedded docs are present but unusable.

## User-facing reporting

For publish requests, lead with the URL. Mention auth/permanence and only the small operational facts the user asked for. Avoid dumping local intermediate paths unless the user asks for them or they are the deliverable.
