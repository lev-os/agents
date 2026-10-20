# Live view data

The established view format uses `schema_version: 1`, an integer `revision`,
`updated_at`, `root_report` and a `reports` map. IDs are local navigation keys,
not newly invented task IDs. Report keys match their `id`; parent chains must
resolve without cycles. Reserve `::` for generated item-detail routes.

```json
{
  "schema_version": 1,
  "revision": 0,
  "updated_at": "2026-10-17T00:00:00Z",
  "root_report": "overview",
  "project": {"title": "Project progress"},
  "orchestrator": {"current": "Verified result and remaining work."},
  "reports": {
    "overview": {
      "id": "overview",
      "parent": null,
      "title": "Project progress",
      "status": "working",
      "items": [
        {
          "id": "preserve",
          "title": "Preserve unique work",
          "status": "pending",
          "owner": "Existing preservation owner",
          "outcome": "Required outcome, not a completion claim.",
          "proof": "Required independent evidence.",
          "stop": "The actual stop condition.",
          "actions": ["First bounded action", "Next action"]
        }
      ]
    }
  }
}
```

An item can reference another map entry with `report`. Set that report's
`parent` for Back navigation. Without a report reference, `actions` become a
work-item detail route. A report can have an empty work list while drafting.

Optional report fields: `subtitle`, `owner`, `outcome`, `proof`, `stop`, `body`
(paragraphs), `changes` (paragraphs), `current_vs_ideal`, `expert_method`, `links`.
Use statuses such as `pending`, `working`, `partial`, `blocked`, `decision`,
`ready`, or `done`. Scope any completion claim to its actual evidence.

Optional top-level view fields:

- `project.master`, `master_anchor`, and `workstream` supply source/footer links.
  Workstream has the verified `title`, `ref`, `status`, `stage`; omit unknowns.
- `owner_sections` holds sections with a `title`, `cards` of `title`/`text`, and
  an optional `note`. It feeds the System owners tab.
- `proof.gates` holds `title`/`text` pairs. `decisions` and
  `operational_decisions` hold `question`, `owner`, `blocks`. These display the
  existing owner's unresolved decisions; the view selects no option.
- A separate render `--reference` file may hold a `children` catalog. Each row
  can have `id`, `title`, `owner`, `plan_ref`, `implementation_status`, `exit_gate`.
  The renderer hides optional tabs with no data.

## Documents

`document_root` is a URL relative to the HTML. Default: `./`. For an HTML file
under `<served-root>/reports/example/`, use `../../` if documents are relative
to the served root. JSON data may have any filename; render embeds its relative
URL. The server serves only its declared root and rejects escaping symlinks.

```json
{"label":"Evidence","kind":"markdown","path":"reports/example/evidence.md"}
```

Use `markdown`, `html` or `text` for local files. Paths are relative to the
declared document root. Use `kind: external` and `href` for HTTP(S), `t3-thread`
or `lev` links. Markdown links resolve from the Markdown file's location.
HTML opens in a sandboxed frame. Local linked files must exist under the
served root. Keep private material outside it.

`links.overview_document` can hold a local link object for the root menu's
Back destination. Without it, root Back is disabled. The header always reserves
Back's space. All reviews the recommended order; it starts no operation.

## Updates and snapshots

The browser fetches JSON every two seconds. Updates retain the active report,
tab and open document. On read failure it labels retained data as a snapshot.
The helper's merge patch changes only the view: it does not update tasks.
After a template change, refresh the browser once. A copied HTML file has the
last embedded snapshot; live refresh and linked documents require the server.
