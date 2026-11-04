# Slack Pass 2 + Pass 3 read-only review page

Use this pattern for a user-requested page that must show both semantic intake and Notion reconciliation without creating or modifying Notion records.

## Required artifact contract

1. **Pass 2 is source-backed extraction.** Preserve the per-unit evaluation outputs, proposal kind/title/summary/confidence, source ID/content hash, and quoted excerpt. Do not report a unit canary as a full pass.
2. **Pass 3 is a separate read-only phase.** Record a timestamped Notion snapshot before matching candidates. Track the exact sources queried, their page cursors, completion status, and record counts.
3. **Paginate to completion.** A `has_more=true` response is not a complete snapshot. Fetch remaining cursors before labeling a snapshot complete; deduplicate a boundary item if the provider repeats it across pages.
4. **Keep two ledgers:**
   - `proposal-actions.json`: one dry-run reconciliation decision per Pass-2 proposal, including proposed destination, match evidence/similarity, and `write_allowed: false`.
   - `source-coverage.json`: one row per admitted `(source_object_id, content_hash)` tuple, including proposal links or a no-action disposition. Assert coverage equals the admitted-source count.
5. **No invented ownership or remote metadata.** If no safe canonical destination or controlled value is available, use a review disposition instead of guessing.

## Now-page content shape

For a full run, use a compact operational header and `sidebar-toc` reader layout instead of a decorative dashboard. Include:

- run status KPIs: readable units, proposals by kind, source coverage, remote writes (= 0);
- a phase timeline distinguishing Pass 2, fresh Pass 3 snapshot, and the unexecuted projection gate;
- a **full Pass-2 table** with proposal title, summary, confidence, and source excerpt;
- a **full Pass-3 table** with proposed action, destination, and best live match;
- an audit callout with absolute artifact paths and a clear statement that projection did not run.

For very large tables, ensure the page uses the renderer’s table/fullscreen affordance and QA at desktop and mobile widths. The JSON ledgers remain the authoritative complete representation.

## Verification checklist

- Assert every Pass-2 proposal appears once in the Pass-3 action ledger.
- Assert every admitted source tuple appears once in coverage.
- Assert all snapshot targets are complete and all paginated sources reached `has_more=false`.
- Assert no Notion create/update calls occurred and `write_allowed` is false for every action.
- Render the page, run visual QA, and report the local HTML path for a non-published page.
