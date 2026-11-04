# Live publish QA pattern

Use this when a session asks to render, QA, republish, and verify a static report/page rather than merely produce a link.

## Pattern

1. Publish from the directory that should become the web root, ensuring `index.html` is at that root.
2. Capture the script's current `siteUrl` and `publish_result.*` lines. Treat these lines as authoritative for auth mode, permanence, expiry, and claim URL.
3. Open the live `siteUrl` in a browser, not just local files.
4. Verify content with at least one structural/text check:
   - Browser snapshot shows expected title/heading/nav/section from the latest update.
   - If the update targeted a specific section, check that section's text appears on the live page.
5. Check browser console for JavaScript errors and failed runtime messages.
6. For visual/report pages, do one visual pass: confirm the key section is visible/readable and no obvious layout breakage exists.
7. Final user reply should include: live URL, what changed, auth/permanence/expiry status, and the concrete verification results.

## Pitfalls

- Do not stop after the publish command. The deliverable is the live page plus QA evidence.
- Do not infer permanence from local state files. Use the current script output.
- Do not report a stale URL from a previous run if the latest script returned a new `siteUrl`.
- Do not treat a clean local render as enough; verify the deployed URL.