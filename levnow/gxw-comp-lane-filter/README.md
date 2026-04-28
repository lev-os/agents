# lane-chip-filter

Reusable chip-group filter. Binds to any row-dataset via `data-target` + `data-attr`, toggles `.hidden` on children that don't match the active chip, emits a `lane-chip-filter:change` event.

## Contract

```html
<div class="lane-chip-filter"
  data-target="#someList"
  data-attr="data-lane"
  data-label="Filter by lane"
  data-chips='[
    {"id":"all","label":"ALL"},
    {"id":"near","label":"NEAR","count":3}
  ]'></div>

<ul id="someList">
  <li data-lane="near">…</li>
  <li data-lane="mid">…</li>
</ul>
```

- **`data-target`** — CSS selector for the list whose children get filtered.
- **`data-attr`** — attribute on each child that identifies its group (default `data-lane`).
- **`data-chips`** — JSON array of `{id, label, count?}`. `count` auto-computes if omitted.
- **`data-label`** — ARIA label for the chip group.
- Default active chip: `id="all"` (or first chip).

## Behavior

- Click toggles `.hidden` on target children whose `data-{attr}` does not match the active chip id.
- `id: "all"` (or `"*"`) unhides everything.
- Emits `CustomEvent('lane-chip-filter:change', { detail: { id, targetSelector } })` bubbling from the root.

## Accessibility

- `role="group"` on root, `aria-pressed` toggled on each chip.
- Roving `tabindex`: active chip is `0`, others `-1`.
- Keyboard: `Tab` enters the group; `←/→/↑/↓` move + activate; `Home/End` jump to ends; `Enter/Space` activate.
- Visible focus ring via `:focus-visible`.

## Combine with text search (AND)

```js
const api = window.LaneChipFilter.get(document.getElementById('ledgerFilter'));
let query = '';
api.addFilter((el) => !query || (el.dataset.search || '').includes(query));

searchInput.addEventListener('input', () => {
  query = searchInput.value.trim().toLowerCase();
  api.refresh();
});
```

External predicates are AND-combined with the chip selection. `refresh()` re-runs them.

## Files

- `lane-chip-filter.js` — auto-inits every `.lane-chip-filter` on `DOMContentLoaded`. Exposes `window.LaneChipFilter = { init, initAll, get }`.
- `lane-chip-filter.css` — chip styling; inherits host design tokens (`--primary`, `--surface-*`, `--outline`) with GXW obsidian fallbacks.
