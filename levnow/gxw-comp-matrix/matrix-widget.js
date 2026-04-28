// matrix-widget — drop-in standalone matrix component.
// Contract: <div class="matrix-widget" data-matrix='{...}'></div>
// Auto-hydrates all .matrix-widget nodes on DOMContentLoaded.

const KIND_LABELS = {
  direct:   'DIRECT · CONTRIBUTION',
  family:   'FAMILY · MATCH',
  adjacent: 'ADJACENT',
  none:     'NO OVERLAP',
};

const LANE_LABEL_FALLBACK = {
  near: 'near', mid: 'mid', far: 'far', adapter: 'adapter', out: 'stays·out',
};

function parseMatrix(root) {
  const raw = root.getAttribute('data-matrix');
  if (!raw) throw new Error('matrix-widget: missing data-matrix attribute');
  try {
    return JSON.parse(raw);
  } catch (err) {
    throw new Error('matrix-widget: invalid JSON in data-matrix: ' + err.message);
  }
}

function laneLabelFor(cfg, lane) {
  if (!lane) return '';
  if (cfg.laneLabels && cfg.laneLabels[lane]) return cfg.laneLabels[lane];
  return LANE_LABEL_FALLBACK[lane] || lane;
}

function normalizeCellKind(kind) {
  if (kind === 'direct' || kind === 'family' || kind === 'adjacent') return kind;
  return 'none';
}

function getCell(cells, rowId, colId) {
  const row = cells && cells[rowId];
  if (!row) return { kind: 'none', binding: null };
  const entry = row[colId];
  if (entry == null) return { kind: 'none', binding: null };
  if (typeof entry === 'string') return { kind: normalizeCellKind(entry), binding: null };
  return {
    kind: normalizeCellKind(entry.kind),
    binding: entry.binding || null,
  };
}

function buildHeader(cfg) {
  const hd = document.createElement('div');
  hd.className = 'mw-hd-row';

  const corner = document.createElement('div');
  corner.className = 'mw-corner';
  corner.innerHTML = `
    <div class="mw-impl-lbl">${escapeHtml(cfg.rowLabel || 'ROW')} ↓</div>
    <div class="mw-arrow">${escapeHtml(cfg.colLabel || 'COL')} →</div>
  `;
  hd.appendChild(corner);

  cfg.cols.forEach(col => {
    const h = document.createElement('div');
    h.className = 'mw-flow-h';
    h.dataset.col = col.id;
    const n = col.n ? `<div class="mw-n">${escapeHtml(col.n)}</div>` : '';
    const laneTag = col.lane ? `<div class="mw-lane-tag">${escapeHtml(col.lane)}</div>` : '';
    h.innerHTML = `
      ${n}
      <div class="mw-fname">${escapeHtml(col.short || col.name || col.id)}</div>
      ${laneTag}
    `;
    hd.appendChild(h);
  });
  return hd;
}

function buildRow(cfg, row) {
  const r = document.createElement('div');
  r.className = 'mw-impl-row';
  r.dataset.row = row.id;
  if (row.lane) r.dataset.lane = row.lane;

  const ic = document.createElement('div');
  ic.className = 'mw-impl-cell';
  const laneTag = row.lane
    ? `<span class="mw-lane ${row.lane}">${escapeHtml(laneLabelFor(cfg, row.lane))}</span>`
    : '';
  const uniq = Number.isFinite(row.uniq)
    ? `<span>uniq · ${'★'.repeat(row.uniq)}${'·'.repeat(Math.max(0, 5 - row.uniq))}</span>`
    : '';
  ic.innerHTML = `
    <div class="mw-name">${escapeHtml(row.label || row.id)}</div>
    <div class="mw-tags">${laneTag}${uniq}</div>
  `;
  r.appendChild(ic);

  cfg.cols.forEach(col => {
    const cm = getCell(cfg.cells, row.id, col.id);
    const c = document.createElement('div');
    c.className = 'mw-cell';
    c.dataset.k = cm.kind;
    c.dataset.row = row.id;
    c.dataset.col = col.id;
    c.innerHTML = `<span class="mw-glyph"></span>`;
    r.appendChild(c);
  });

  return r;
}

function buildLegend() {
  const legend = document.createElement('div');
  legend.className = 'mw-legend';
  legend.innerHTML = `
    <div class="mw-item"><span class="mw-g direct"></span>direct</div>
    <div class="mw-item"><span class="mw-g family"></span>family</div>
    <div class="mw-item"><span class="mw-g adjacent"></span>adjacent</div>
    <div class="mw-item"><span class="mw-g none"></span>none</div>
  `;
  return legend;
}

function buildLaneFilters(cfg, laneFilters) {
  const group = document.createElement('div');
  group.className = 'mw-group mw-lane-filters';
  const lbl = document.createElement('span');
  lbl.className = 'mw-lbl';
  lbl.textContent = cfg.laneFilterLabel || 'Filter · lane';
  group.appendChild(lbl);
  laneFilters.forEach(lane => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'mw-chip';
    btn.dataset.lane = lane.id;
    btn.setAttribute('aria-pressed', lane.id === 'all');
    const n = Number.isFinite(lane.count) ? `<span class="mw-n">${lane.count}</span>` : '';
    btn.innerHTML = `${escapeHtml(lane.label || lane.id.toUpperCase())}${n}`;
    group.appendChild(btn);
  });
  return group;
}

function buildBindingPanel(cfg) {
  const bp = document.createElement('div');
  bp.className = 'mw-binding-panel binding-panel';
  bp.innerHTML = `
    <div class="mw-label">
      <div>BINDING</div>
      <div class="mw-pair"><span class="mw-impl">—</span></div>
      <div class="mw-kind none">hover a cell</div>
    </div>
    <div class="mw-text">
      <span class="mw-empty">${escapeHtml(cfg.bindingHint || 'Hover a cell to see the binding.')}</span>
    </div>
  `;
  return bp;
}

function renderBinding(bp, row, col, kind, binding) {
  const rowName = row.label || row.id;
  const colName = col.name || col.short || col.id;
  const text = binding || (kind === 'none'
    ? `${rowName} does not contribute to ${colName}.`
    : kind === 'family'
      ? `${colName} — covers a family ${rowName} contributes to.`
      : kind === 'adjacent'
        ? `${rowName} orbits ${colName} but does not own it.`
        : `${rowName} directly contributes to ${colName}.`);
  const colTag = col.n ? `${escapeHtml(col.label || col.short || col.id)} · ${escapeHtml(col.n)}` : escapeHtml(col.short || col.id);
  const hint = col.blurb
    ? `<div class="mw-hint">${escapeHtml(colName.toUpperCase())} · ${escapeHtml(col.blurb)}</div>`
    : '';
  bp.innerHTML = `
    <div class="mw-label">
      <div>BINDING</div>
      <div class="mw-pair"><span class="mw-impl">${escapeHtml(rowName)}</span><span class="mw-op">×</span><span class="mw-flow">${colTag}</span></div>
      <div class="mw-kind ${kind}">${KIND_LABELS[kind]}</div>
    </div>
    <div class="mw-text">
      <div>${escapeHtml(text)}</div>
      ${hint}
    </div>
  `;
}

function escapeHtml(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function hydrate(root) {
  if (root.dataset.hydrated === '1') return;
  root.dataset.hydrated = '1';

  const cfg = parseMatrix(root);
  cfg.cells = cfg.cells || {};
  cfg.rows = cfg.rows || [];
  cfg.cols = cfg.cols || [];

  root.innerHTML = '';

  // Controls + legend
  const controls = document.createElement('div');
  controls.className = 'mw-controls';

  const laneFilters = Array.isArray(cfg.laneFilters) && cfg.laneFilters.length
    ? cfg.laneFilters
    : null;
  if (laneFilters) {
    controls.appendChild(buildLaneFilters(cfg, laneFilters));
  }
  controls.appendChild(buildLegend());
  root.appendChild(controls);

  // Scroll wrapper + grid
  const scroll = document.createElement('div');
  scroll.className = 'mw-scroll';

  const grid = document.createElement('div');
  grid.className = 'mw-grid';
  grid.style.gridTemplateColumns = `220px repeat(${cfg.cols.length}, minmax(36px, 1fr))`;

  grid.appendChild(buildHeader(cfg));
  cfg.rows.forEach(row => grid.appendChild(buildRow(cfg, row)));
  scroll.appendChild(grid);
  root.appendChild(scroll);

  // Binding panel
  const bp = buildBindingPanel(cfg);
  root.appendChild(bp);

  // Scroll-shadow toggle
  const updateScrollShadow = () => {
    scroll.classList.toggle('has-scroll', scroll.scrollWidth > scroll.clientWidth);
  };
  updateScrollShadow();
  if (typeof ResizeObserver !== 'undefined') {
    new ResizeObserver(updateScrollShadow).observe(scroll);
  } else {
    window.addEventListener('resize', updateScrollShadow);
  }

  // Hover — binding + row/col highlight
  scroll.addEventListener('mouseover', (e) => {
    const c = e.target.closest('.mw-cell');
    if (!c || !scroll.contains(c)) return;
    const rowId = c.dataset.row;
    const colId = c.dataset.col;
    const row = cfg.rows.find(r => r.id === rowId);
    const col = cfg.cols.find(co => co.id === colId);
    if (!row || !col) return;
    const cm = getCell(cfg.cells, rowId, colId);
    renderBinding(bp, row, col, cm.kind, cm.binding);
    scroll.querySelectorAll('.mw-cell.row-hi, .mw-cell.col-hi').forEach(el => el.classList.remove('row-hi', 'col-hi'));
    const parent = c.closest('.mw-impl-row');
    if (parent) parent.querySelectorAll('.mw-cell').forEach(el => el.classList.add('row-hi'));
    scroll.querySelectorAll(`.mw-cell[data-col="${CSS.escape(colId)}"]`).forEach(el => el.classList.add('col-hi'));
  });
  scroll.addEventListener('mouseleave', () => {
    scroll.querySelectorAll('.mw-cell.row-hi, .mw-cell.col-hi').forEach(el => el.classList.remove('row-hi', 'col-hi'));
  });

  // Lane filter
  if (laneFilters) {
    let active = 'all';
    const group = controls.querySelector('.mw-lane-filters');
    group.addEventListener('click', (e) => {
      const btn = e.target.closest('.mw-chip');
      if (!btn) return;
      active = btn.dataset.lane;
      group.querySelectorAll('.mw-chip').forEach(c => c.setAttribute('aria-pressed', c.dataset.lane === active));
      scroll.querySelectorAll('.mw-impl-row').forEach(r => {
        const show = active === 'all' || r.dataset.lane === active;
        r.classList.toggle('hidden', !show);
      });
    });
  }
}

function hydrateAll(rootDoc) {
  const doc = rootDoc || document;
  doc.querySelectorAll('.matrix-widget').forEach(el => {
    try { hydrate(el); }
    catch (err) {
      console.error('[matrix-widget]', err);
      el.innerHTML = `<pre style="color:#f88;padding:16px;font-family:monospace;">matrix-widget error: ${err.message}</pre>`;
    }
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => hydrateAll());
} else {
  hydrateAll();
}

export { hydrate, hydrateAll };
