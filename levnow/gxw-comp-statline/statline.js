/* ===== statline component =====
   Reads <div class="statline" data-stats='[{"k","v","unit"}, ...]'></div>
   Renders cells. Optionally animates integer <v> values 0 → target on scroll-in
   when the element carries data-animate="true".
*/
(function () {
  'use strict';

  const PARSE_INT_RE = /^-?\d+$/;

  function renderCell(stat) {
    const cell = document.createElement('div');
    cell.className = 'cell';

    const k = document.createElement('div');
    k.className = 'k';
    k.textContent = stat.k || '';

    const v = document.createElement('div');
    v.className = 'v';

    const value = stat.v == null ? '' : String(stat.v);
    const isInt = PARSE_INT_RE.test(value);

    const num = document.createElement('span');
    num.className = 'num';
    num.textContent = value;
    if (isInt) num.dataset.target = value;
    v.appendChild(num);

    if (stat.unit) {
      const unit = document.createElement('span');
      unit.className = 'unit';
      unit.textContent = stat.unit;
      v.appendChild(unit);
    }

    cell.appendChild(k);
    cell.appendChild(v);
    return cell;
  }

  function render(el) {
    const raw = el.getAttribute('data-stats');
    if (!raw) return;
    let stats;
    try {
      stats = JSON.parse(raw);
    } catch (e) {
      console.warn('[statline] bad JSON', e, raw);
      return;
    }
    if (!Array.isArray(stats)) return;
    el.innerHTML = '';
    stats.forEach((s) => el.appendChild(renderCell(s)));

    if (el.dataset.animate === 'true') {
      queueAnimate(el);
    }
  }

  function tween(node, target, duration) {
    const start = performance.now();
    const from = 0;
    function frame(now) {
      const t = Math.min(1, (now - start) / duration);
      // easeOutCubic
      const eased = 1 - Math.pow(1 - t, 3);
      const val = Math.round(from + (target - from) * eased);
      node.textContent = String(val);
      if (t < 1) requestAnimationFrame(frame);
      else node.textContent = String(target);
    }
    requestAnimationFrame(frame);
  }

  function animate(el) {
    el.querySelectorAll('.num[data-target]').forEach((node) => {
      const target = parseInt(node.dataset.target, 10);
      if (Number.isFinite(target)) tween(node, target, 800);
    });
  }

  function queueAnimate(el) {
    if (!('IntersectionObserver' in window)) {
      animate(el);
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animate(entry.target);
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.35 }
    );
    io.observe(el);
  }

  function mountAll(root) {
    (root || document).querySelectorAll('.statline[data-stats]').forEach(render);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => mountAll());
  } else {
    mountAll();
  }

  // Expose for dynamic remounts.
  window.Statline = { mountAll, render };
})();
