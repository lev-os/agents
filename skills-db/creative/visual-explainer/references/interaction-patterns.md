# Interaction Patterns Reference

Reference document for all interactive JavaScript patterns used in the visual-explainer decision template. These patterns power the browser-side interaction layer — search, filtering, daemon connectivity, response panels, and embed mode.

---

## Connection Manager (LevConnection)

Manages optional WebSocket connectivity to the Lev daemon. Degrades gracefully to clipboard mode when the daemon is offline.

### States

| Status | Meaning | Indicator |
|---|---|---|
| `connected` | WebSocket open to daemon | Green dot |
| `fallback` | Daemon unreachable, clipboard mode | Amber dot |
| `disconnected` | Initial state, not yet attempted | Gray dot |

### Implementation

```javascript
var LevConnection = {
  ws: null,
  status: 'disconnected',
  reconnectTimer: null,

  init: function() {
    var self = this;
    fetch('http://localhost:9849/health', { signal: AbortSignal.timeout(2000) })
      .then(function(r) { if (!r.ok) throw new Error(); return r; })
      .then(function() {
        self.ws = new WebSocket('ws://localhost:9849/exec/stream');
        self.ws.onopen = function() {
          self.status = 'connected';
          self.updateIndicator();
        };
        self.ws.onclose = function() {
          self.status = 'fallback';
          self.updateIndicator();
          self.scheduleReconnect();
        };
        self.ws.onerror = function() {
          self.status = 'fallback';
          self.updateIndicator();
        };
      })
      .catch(function() {
        self.status = 'fallback';
        self.updateIndicator();
      });
  },

  scheduleReconnect: function() {
    if (this.reconnectTimer) return;
    var self = this;
    this.reconnectTimer = setTimeout(function() {
      self.reconnectTimer = null;
      self.init();
    }, 5000);
  },

  updateIndicator: function() {
    var dot = document.getElementById('conn-dot');
    if (!dot) return;
    dot.className = 'conn-dot conn-' + this.status;
    dot.title = this.status === 'connected' ? 'Connected to Lev daemon'
      : this.status === 'fallback' ? 'Clipboard mode (daemon offline)'
      : 'Disconnected';
  },

  exec: function(task) {
    if (this.status !== 'connected' || !this.ws || this.ws.readyState !== WebSocket.OPEN) {
      return Promise.resolve(null);
    }
    var ws = this.ws;
    return new Promise(function(resolve) {
      var chunks = [];
      var handler = function(e) {
        var msg = JSON.parse(e.data);
        if (msg.type === 'chunk') chunks.push(msg.data);
        else if (msg.type === 'done') {
          ws.removeEventListener('message', handler);
          resolve({
            output: msg.output,
            chunks: chunks,
            tokenUsage: msg.tokenUsage,
            duration_ms: msg.duration_ms
          });
        }
        else if (msg.type === 'error') {
          ws.removeEventListener('message', handler);
          resolve(null);
        }
      };
      ws.addEventListener('message', handler);
      ws.send(JSON.stringify({ type: 'exec', task: task }));
    });
  }
};
```

### Protocol

1. On page load, `LevConnection.init()` fires a health check to `http://localhost:9849/health`
2. If healthy, opens WebSocket to `ws://localhost:9849/exec/stream`
3. On close/error, falls back to clipboard mode and schedules reconnect (5s interval)
4. `exec(task)` sends `{ type: 'exec', task: '...' }` and collects streamed chunks until `done` or `error`

---

## Response Panel

Fixed panel that appears above the action bar when Claude returns output (via daemon or future integrations).

### Behavior

- Initially hidden (`display: none`)
- Activated via `showResponsePanel(content)` which sets text and adds `.show` class
- Copy button copies panel content to clipboard
- Dismiss button removes `.show` class
- Slide-up animation on appearance

### HTML Structure

```html
<div class="response-panel" id="response-panel">
  <div class="panel-header">
    <h4>Claude Response</h4>
    <div class="panel-actions">
      <button class="btn btn-secondary" onclick="copyResponse()">Copy</button>
      <button class="btn btn-secondary" onclick="dismissResponse()">Dismiss</button>
    </div>
  </div>
  <pre id="response-content"></pre>
</div>
```

### CSS

```css
.response-panel {
  position: fixed;
  bottom: 72px;
  left: 50%;
  transform: translateX(-50%);
  width: min(90vw, 800px);
  max-height: 50vh;
  background: var(--paper);
  border: 1px solid var(--border);
  border-radius: 8px;
  box-shadow: var(--card-shadow);
  overflow-y: auto;
  padding: 1rem 1.25rem;
  z-index: 200;
  display: none;
  animation: slideUp 0.3s ease;
}
.response-panel.show { display: block; }
.response-panel pre {
  white-space: pre-wrap;
  word-break: break-word;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.8rem;
  line-height: 1.5;
  margin: 0;
}
.response-panel .panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}
.response-panel .panel-header h4 {
  margin: 0;
  font-size: 0.85rem;
  color: var(--ink-muted);
}
.response-panel .panel-actions { display: flex; gap: 0.5rem; }
.response-panel .panel-actions button { font-size: 0.75rem; padding: 0.25rem 0.5rem; }

@keyframes slideUp {
  from { opacity: 0; transform: translateX(-50%) translateY(20px); }
  to   { opacity: 1; transform: translateX(-50%) translateY(0); }
}
```

### JavaScript

```javascript
function showResponsePanel(content) {
  var panel = document.getElementById('response-panel');
  var pre = document.getElementById('response-content');
  pre.textContent = content;
  panel.classList.add('show');
}

function dismissResponse() {
  document.getElementById('response-panel').classList.remove('show');
}

function copyResponse() {
  var text = document.getElementById('response-content').textContent;
  navigator.clipboard.writeText(text).then(function() {
    showToast('Response copied');
  });
}
```

---

## Connection Indicator

8px dot next to the progress bar that shows daemon connectivity status.

### CSS

```css
.conn-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
  margin-left: 0.5rem;
  vertical-align: middle;
  transition: background 0.3s;
}
.conn-connected { background: var(--green); box-shadow: 0 0 4px var(--green); }
.conn-fallback  { background: var(--amber); }
.conn-disconnected { background: var(--ink-muted); }
```

### HTML

Place inside `.progress-inner`, adjacent to the save indicator:

```html
<span id="conn-dot" class="conn-dot conn-disconnected"></span>
```

---

## Search + Filter

Client-side search and filtering — no daemon dependency. Operates entirely on DOM visibility.

### Components

1. **Search input** - text field with 200ms debounce, matches against title + insight + detail
2. **Filter chips** - auto-generated from bucket names, toggle visibility per bucket
3. **Undecided only toggle** - checkbox that hides items with a decision already made

### Implementation Strategy

- No re-render: uses `display: none` via `.filtered-out` CSS class on `.item-card` elements
- Each `.item-card` needs a `data-item-id` attribute for lookup against `ITEMS` array
- Filter chips are built dynamically from unique bucket names in `ITEMS`

### CSS

```css
.search-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
}
.search-bar input {
  flex: 1;
  padding: 0.4rem 0.75rem;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: var(--paper);
  color: var(--ink);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.8rem;
}
.filter-chips { display: flex; gap: 0.35rem; flex-wrap: wrap; }
.filter-chip {
  padding: 0.2rem 0.6rem;
  border: 1px solid var(--border);
  border-radius: 12px;
  font-size: 0.7rem;
  cursor: pointer;
  background: transparent;
  color: var(--ink-muted);
  transition: all 0.2s;
}
.filter-chip.active {
  background: var(--copper);
  color: var(--warm-white);
  border-color: var(--copper);
}
.item-card.filtered-out { display: none !important; }
```

### HTML

```html
<div class="search-bar">
  <input type="text" id="search-input" placeholder="Search decisions..." />
  <div class="filter-chips" id="filter-chips"></div>
  <label style="font-size:0.75rem;white-space:nowrap;cursor:pointer;color:var(--ink-muted)">
    <input type="checkbox" id="undecided-toggle" style="margin-right:0.25rem" /> Undecided only
  </label>
</div>
```

### JavaScript

```javascript
var searchTimer = null;
document.getElementById('search-input').addEventListener('input', function() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(applyFilters, 200);
});
document.getElementById('undecided-toggle').addEventListener('change', applyFilters);

// Build filter chips from bucket names
(function() {
  var chips = document.getElementById('filter-chips');
  var buckets = {};
  ITEMS.forEach(function(item) { buckets[item.bucket] = true; });
  Object.keys(buckets).forEach(function(bucket) {
    var chip = document.createElement('button');
    chip.className = 'filter-chip active';
    chip.textContent = bucket;
    chip.dataset.bucket = bucket;
    chip.addEventListener('click', function() {
      this.classList.toggle('active');
      applyFilters();
    });
    chips.appendChild(chip);
  });
})();

function applyFilters() {
  var query = (document.getElementById('search-input').value || '').toLowerCase();
  var undecidedOnly = document.getElementById('undecided-toggle').checked;
  var activeChips = {};
  document.querySelectorAll('.filter-chip.active').forEach(function(c) {
    activeChips[c.dataset.bucket] = true;
  });

  document.querySelectorAll('.item-card').forEach(function(card) {
    var itemId = card.dataset.itemId;
    var item = null;
    for (var i = 0; i < ITEMS.length; i++) {
      if (ITEMS[i].id === itemId) { item = ITEMS[i]; break; }
    }
    if (!item) return;

    var visible = true;
    if (!activeChips[item.bucket]) visible = false;
    if (query && visible) {
      var searchable = (item.title + ' ' + item.insight + ' ' + (item.detail || '')).toLowerCase();
      if (searchable.indexOf(query) === -1) visible = false;
    }
    if (undecidedOnly && visible) {
      var key = getKey(item);
      if (decisions[key] && decisions[key].choice !== undefined) visible = false;
    }

    card.classList.toggle('filtered-out', !visible);
  });
}
```

---

## Embed Mode

Strips chrome (hero, nav, action bar) for iframe embedding. Exposes a `postMessage` API for the parent frame.

### Activation

`?embed=true` query parameter:

```javascript
if (new URLSearchParams(window.location.search).get('embed') === 'true') {
  document.body.classList.add('embed-mode');
}
```

### CSS

```css
.embed-mode .hero,
.embed-mode .bucket-nav,
.embed-mode .action-bar { display: none !important; }
.embed-mode .progress-bar-wrap { position: static; }
.embed-mode { padding-top: 0; }
```

### postMessage API

The embedded page responds to `getDecisions` messages from the parent frame:

```javascript
window.addEventListener('message', function(e) {
  if (e.data && e.data.type === 'getDecisions') {
    var pageId = document.querySelector('main').dataset.pageId;
    window.parent.postMessage({
      type: 'decisions',
      pageId: pageId,
      timestamp: new Date().toISOString(),
      decisions: decisions,
      items: ITEMS.map(function(item) {
        var key = getKey(item);
        var d = decisions[key];
        return {
          id: item.id,
          title: item.title,
          bucket: item.bucket,
          decided: !!(d && d.choice !== undefined),
          choice: d ? d.choice : null,
          notes: d ? d.notes : ''
        };
      })
    }, '*');
  }
});
```

### Parent Frame Usage

```javascript
// From parent page:
var iframe = document.getElementById('decision-frame');
iframe.contentWindow.postMessage({ type: 'getDecisions' }, '*');

window.addEventListener('message', function(e) {
  if (e.data.type === 'decisions') {
    console.log('Decisions from', e.data.pageId, e.data.decisions);
  }
});
```
