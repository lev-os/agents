/* ============================================================
   lane-chip-filter.js
   Reusable chip-group filter bound to any row-dataset.

   Contract (HTML):
     <div class="lane-chip-filter"
       data-target="#someList"
       data-attr="data-lane"
       data-chips='[{"id":"all","label":"ALL"},{"id":"near","label":"NEAR","count":3}]'>
     </div>

   Behavior:
     - Renders chips with aria-pressed; first chip (or id="all") active by default.
     - Click toggles .hidden on target children whose attr value doesn't match.
     - "all" (or "*") unhides everything.
     - Counts auto-computed from target children if omitted.
     - Emits CustomEvent('lane-chip-filter:change', {detail:{id, targetSelector}}).
     - Accepts external filter predicates via addFilter(fn) for AND-combine.
   ============================================================ */

(function () {
  const REGISTRY = new WeakMap();

  function computeCount(target, attr, id) {
    if (!target) return 0;
    if (id === 'all' || id === '*') return target.children.length;
    let n = 0;
    for (const child of target.children) {
      if (child.getAttribute(attr) === id) n++;
    }
    return n;
  }

  function init(root) {
    if (REGISTRY.has(root)) return REGISTRY.get(root);

    const targetSel = root.dataset.target;
    const attr = root.dataset.attr || 'data-lane';
    const target = targetSel ? document.querySelector(targetSel) : null;
    let chips = [];
    try {
      chips = JSON.parse(root.dataset.chips || '[]');
    } catch (e) {
      console.error('[lane-chip-filter] invalid data-chips JSON', e);
      return null;
    }
    if (!target) {
      console.warn('[lane-chip-filter] target not found:', targetSel);
    }

    const predicates = new Set();
    let activeId = chips.find(c => c.id === 'all')?.id || chips[0]?.id || 'all';

    root.setAttribute('role', 'group');
    root.setAttribute('aria-label', root.dataset.label || 'Filter chips');
    root.innerHTML = '';

    const chipEls = chips.map((chip, idx) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'lcf-chip';
      btn.dataset.chipId = chip.id;
      btn.setAttribute('role', 'button');
      btn.setAttribute('aria-pressed', String(chip.id === activeId));
      btn.tabIndex = chip.id === activeId ? 0 : -1;

      const label = document.createElement('span');
      label.className = 'lcf-chip__label';
      label.textContent = chip.label;
      btn.appendChild(label);

      const countVal = chip.count ?? computeCount(target, attr, chip.id);
      const count = document.createElement('span');
      count.className = 'lcf-chip__count';
      count.textContent = countVal;
      btn.appendChild(count);

      btn.addEventListener('click', () => activate(chip.id));
      btn.addEventListener('keydown', (e) => onKey(e, idx));
      root.appendChild(btn);
      return btn;
    });

    function applyFilters() {
      if (!target) return;
      for (const child of target.children) {
        const v = child.getAttribute(attr);
        const laneOk = activeId === 'all' || activeId === '*' || v === activeId;
        let extOk = true;
        for (const fn of predicates) {
          if (!fn(child)) { extOk = false; break; }
        }
        child.classList.toggle('hidden', !(laneOk && extOk));
      }
    }

    function activate(id) {
      activeId = id;
      chipEls.forEach(el => {
        const pressed = el.dataset.chipId === id;
        el.setAttribute('aria-pressed', String(pressed));
        el.tabIndex = pressed ? 0 : -1;
      });
      applyFilters();
      root.dispatchEvent(new CustomEvent('lane-chip-filter:change', {
        bubbles: true,
        detail: { id, targetSelector: targetSel }
      }));
    }

    function onKey(e, idx) {
      const last = chipEls.length - 1;
      let nextIdx = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') nextIdx = idx === last ? 0 : idx + 1;
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') nextIdx = idx === 0 ? last : idx - 1;
      else if (e.key === 'Home') nextIdx = 0;
      else if (e.key === 'End') nextIdx = last;
      else if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        activate(chipEls[idx].dataset.chipId);
        return;
      }
      if (nextIdx !== null) {
        e.preventDefault();
        const target = chipEls[nextIdx];
        target.focus();
        activate(target.dataset.chipId);
      }
    }

    const api = {
      activate,
      getActive: () => activeId,
      addFilter: (fn) => { predicates.add(fn); applyFilters(); return () => { predicates.delete(fn); applyFilters(); }; },
      refresh: applyFilters,
      recount: () => {
        chipEls.forEach(el => {
          const countEl = el.querySelector('.lcf-chip__count');
          if (countEl) countEl.textContent = computeCount(target, attr, el.dataset.chipId);
        });
      },
    };
    REGISTRY.set(root, api);
    applyFilters();
    return api;
  }

  function initAll(scope) {
    const ctx = scope || document;
    return Array.from(ctx.querySelectorAll('.lane-chip-filter')).map(init).filter(Boolean);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => initAll());
  } else {
    initAll();
  }

  window.LaneChipFilter = { init, initAll, get: (el) => REGISTRY.get(el) };
})();
