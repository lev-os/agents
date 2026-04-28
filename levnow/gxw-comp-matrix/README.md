# matrix-widget

Drop-in standalone parity/heatmap matrix. Renders a `rows × cols` grid with four
cell kinds, row+col hover highlight, hover-driven binding panel, and a chip lane
filter. No dependencies beyond standard browser APIs.

## Contract

```html
<link rel="stylesheet" href="matrix-widget.css">
<div class="matrix-widget" data-matrix='{...}'></div>
<script type="module" src="matrix-widget.js"></script>
```

The module auto-hydrates every `.matrix-widget` node on `DOMContentLoaded`.
`data-matrix` JSON payload keys:

| key | type | notes |
|---|---|---|
| `rows` | `[{id,label,lane?,uniq?}]` | Row axis. `lane` colors the row tag; `uniq` renders 0–5 stars. |
| `cols` | `[{id,short,name?,n?,lane?,blurb?}]` | Column axis. `short` is the vertical label; `n` is a prefix badge; `blurb` shows in the binding panel. |
| `cells` | `{rowId: {colId: "direct"\|"family"\|"adjacent"\|null \| {kind,binding}}}` | Cell kinds (all omitted → `none`). Inline object form carries a per-cell `binding` string. |
| `laneFilters` | `[{id,label,count?}]` | Optional chip filter; include `{id:"all"}` to show all rows. |
| `rowLabel`, `colLabel` | string | Corner header labels (default `ROW` / `COL`). |
| `laneFilterLabel` | string | Chip-group caption (default `Filter · lane`). |
| `bindingHint` | string | Placeholder text shown before the first hover. |
| `laneLabels` | `{lane:string}` | Per-lane display label override. |

Demo fixtures and mount logic live in `data-fixtures.js` + `index.html`.
Hover any `.mw-cell` to trigger the binding panel; click a `.mw-chip` in the
lane filter to hide non-matching rows.
