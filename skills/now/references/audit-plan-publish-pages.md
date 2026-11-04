# Audit / plan publish pages

Use this pattern when a session produces a concise audit plus migration/cutover plan and the user asks to publish a `lev.now` page.

## Recommended bundle

- `spec.json` — the RenderSpec for the visual page.
- `index.html` — clean rendered HTML, **without** `--show-source` unless explicitly debugging renderer internals.
- `plan.md` — the durable plan artifact copied into the publish folder so the public URL has a readable source plan at `/plan.md`.

Keep the saved plan in the repo’s plan/workstream area and copy it into the page bundle before publishing. The page should reference the repo plan path, but the published bundle should also include `plan.md` for external readers.

## QA checklist

1. Render once locally.
2. Run HTML text checks for distinctive content, absence of missing-element placeholders, and absence of debug/source sections.
3. If lev.now `--qa` fails because Playwright is missing, do not treat the render as failed. Fall back to browser-based local visual QA and report the screenshot-stack gap tersely.
4. Open the local file in a browser and visually inspect hero, cards, table, diagram/timeline, and footer/end state.
5. Publish the clean folder/directory bundle with the here-now publish script.
6. Verify the live URL with HTTP 200 and a distinctive text probe.
7. Verify `/plan.md` separately when it is included in the bundle.

## Pitfalls

- Do not publish a build rendered with `--show-source` unless the user explicitly asked for renderer debugging/source disclosure.
- Do not report an earlier throwaway publish URL if a later clean publish supersedes it.
- When the publish target is a bundle directory, publish the directory, not just the HTML file, so support files such as `plan.md` are available.
