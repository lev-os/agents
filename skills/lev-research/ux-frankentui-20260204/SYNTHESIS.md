# Research Hub CLI UX — FrankenTUI 7-Step Discovery
**Date:** 2026-02-04
**Framework:** FrankenTUI (Rust TUI, inline mode + agent harness)
**Product:** Research Hub CLI — Real-time research progress visualization

---

## STEP 1: Problem Framing

### Current State (Pain)
Research processes (web scraping, document analysis, multi-turn LLM queries) are opaque to users:
- No visibility into which sources are being queried
- No feedback on confidence scores as research progresses
- No cost transparency (API calls, token spend) until job completion
- Terminal fills with raw logs that obscure actionable status
- No way to interrupt or adjust running queries without killing entire process

### Target State (Desired Outcome)
A **Research Hub CLI** that shows:
- **Real-time query status** — What research question is being asked, confidence level (0-100%)
- **Source discovery progress** — URLs queued, in-progress, fetched, parsed
- **Cost tracking** — API call count, token consumption, cost-per-question
- **Multi-turn research** — Chain of reasoning visible (Q→A→followup→answer)
- **Interactive controls** — Pause/resume queries, adjust scope, view sources inline

### User Motivation
Research engineers and data scientists running multi-source fact-checking, competitive analysis, or academic literature synthesis need **immediate visibility** into system behavior and progress without losing scrollback logs.

---

## STEP 2: Jobs to be Done (JTBD) — CLI User Perspective

### Primary Job: "Monitor Research Progress"
**When:** Starting a research query via CLI
**Desired Outcome:** Know, at a glance, what questions are being answered and which sources are being evaluated
**Effort Target:** < 2 seconds to understand current status

**Supporting sub-jobs:**
1. **See confidence trajectory** — Is confidence going up or down over time?
2. **Verify source diversity** — Are we hitting enough sources, or re-hitting the same ones?
3. **Check cost burn rate** — Am I spending $ too fast?
4. **Identify bottlenecks** — Which source is slow? Which API is rate-limited?

### Secondary Job: "Intervene When Needed"
**When:** Research takes unexpected direction or cost rises too fast
**Desired Outcome:** Pause current query, adjust settings, resume without data loss
**Effort Target:** < 1 keystroke to interrupt

### Tertiary Job: "Review Sources Later"
**When:** Completed research, need to audit which sources were used
**Desired Outcome:** Access source metadata (URL, fetch time, relevance score, excerpt)
**Effort Target:** Quick arrow-key navigation to expand any source

---

## STEP 3: Task Decomposition

### Task Tree
```
Research Hub CLI (inline TUI)
├── [VIEW] Status Header (1 line)
│   ├── Current question / Query title
│   └── Elapsed time | Model name | Confidence % | Cost $
│
├── [VIEW] Source Discovery Progress (6-8 lines)
│   ├── Grid: [URLs queued] [In progress] [Fetched] [Parsed]
│   ├── Count-based bars with per-category color
│   └── Sparkline: confidence (10-frame rolling window)
│
├── [VIEW] Cost Tracker (3 lines)
│   ├── API calls: N calls | Rate limit: X/min
│   ├── Tokens: N_used / N_budget | $/1000 tokens
│   └── Projected cost: $X.XX (if linear extrapolation)
│
├── [VIEW] Multi-Turn Research Log (fill)
│   ├── Turn 1: Q: "Who founded X?" | A: "..." | Confidence: 85%
│   ├── Turn 2: Q: "When did X happen?" | A: "..." | Confidence: 92%
│   └── (scrollable)
│
├── [CONTROL] Input Line (1 line)
│   └── Keymap: Pause/Resume (SPC), Adjust scope (A), View sources (+), Quit (Q/Ctrl+C)
│
└── [OVERLAY] Sources Inline (modal, on-demand)
    ├── List of fetched sources (URL, fetch_time_ms, relevance_score)
    └── Arrow keys to expand source excerpt
```

### Critical Paths
1. **Start → Immediate Feedback** (render status before first API call)
2. **Progress Update → Render** (new source found? update grid; new answer? log turn)
3. **User Input → React** (SPC pauses research, A opens config modal)
4. **Exit Path** (Ctrl+C or Q → save session metadata, print summary, clean exit)

---

## STEP 4: Information Architecture

### Zone Layout (Inline Mode, ~12–16 lines)

```
┌─────────────────────────────────────────────────────────────────┐
│ LOGS (above UI, scrollback preserved)                            │
│ [previous research runs, system debug, etc.]                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
   ↓ cursor save (DEC 7)

┌─────────────────────────────────────────────────────────────────┐
│ [HEADER]                                                         │
│ Q: What is the history of X?  [▁▂▃▄▅ 76%]  $0.23   ⏱ 2:45      │
├─────────────────────────────────────────────────────────────────┤
│ [PROGRESS GRID]                                                  │
│ Queued: 12  ⟳ Running: 2  ✓ Fetched: 18  ◐ Parsed: 15          │
│ Confidence: [████████▒░░░░░░░░] 72% → 76% (↑4% in 30s)         │
├─────────────────────────────────────────────────────────────────┤
│ [COST TRACKER]                                                   │
│ API: 24 calls | Tokens: 2,147 / 4,000 | Cost: $0.23             │
├─────────────────────────────────────────────────────────────────┤
│ [RESEARCH LOG]                                                   │
│ Q1: Founder?  → A: Alice (85%)     Q2: When?  → A: 1999 (92%)  │
├─────────────────────────────────────────────────────────────────┤
│ [INPUT]                                                          │
│ Pause (SPC) | Scope (A) | Sources (+) | Quit (Q)               │
└─────────────────────────────────────────────────────────────────┘
   ↑ cursor restore (DEC 8)
```

### Data Flow (Streaming)
```
Research Backend (async)
    ↓
Message Channel (mpsc)
    ↓
Runtime Loop (tick 100ms)
    ├─ Poll channel → update state (counts, confidence, cost)
    ├─ Render frame (view calls render() on widgets)
    └─ Present diff (only changed cells)
```

### Zones & Priority (for graceful degradation)
| Zone | Essential | Priority | Cost | Fallback |
|------|-----------|----------|------|----------|
| Header (status + ETA) | YES | 1.0 | 50µs | Single line: "Q: ... [76%]" |
| Progress grid | YES | 0.9 | 80µs | Text: "12 queued, 2 running..." |
| Cost tracker | NO | 0.7 | 40µs | Omit if budget tight |
| Research log | NO | 0.6 | 200µs | Show only last 2 turns |
| Input hints | YES | 0.5 | 10µs | Always show (1 line) |

---

## STEP 5: Interaction Model

### Keyboard Shortcuts (Pi-style Keybinding Policy, bd-2vne.1)

```
[PASSTHROUGH — Normal Input]
  SPC         → Pause/Resume research (toggle)
  A           → Open scope adjustment modal
  +           → Toggle inline sources overlay (Esc Esc alt)
  Q           → Quit gracefully (save session metadata)
  Ctrl+C      → Hard quit (Ctrl+C suppressed if running)
  Ctrl+D      → Soft quit (cancel research if running, else quit)
  PageUp/Dn   → Scroll research log

[MODAL — Scope Adjustment (A)]
  1-9         → Set max sources per category (1=strict, 9=broad)
  C           → Toggle cost-aware mode (pause if budget exceeded)
  S           → Save & apply
  Esc         → Close modal without changes

[OVERLAY — Sources Inline (+ or Esc Esc)]
  ↑/↓         → Navigate sources list
  Enter       → Expand/collapse source excerpt
  C           → Copy URL to clipboard
  O           → Open URL in browser
  Esc         → Close overlay

[ANYTIME]
  Ctrl+T      → Cycle theme (dark/light/alt)
```

### State Machine
```
IDLE
  ↓ (user enters query, presses Enter)
RUNNING
  ├─ Receive "pause" (SPC) → PAUSED
  ├─ Receive "scope" (A) → RUNNING + MODAL_OPEN
  ├─ Receive "quit" (Q) → CLEANUP → EXIT
  └─ Research done → COMPLETED

PAUSED
  ├─ Receive "resume" (SPC) → RUNNING
  └─ Receive "quit" (Q) → CLEANUP → EXIT

COMPLETED
  ├─ Receive "sources" (+) → COMPLETED + OVERLAY_OPEN
  ├─ Receive "review" (R) → Show summary & stats
  └─ Receive "quit" (Q) → EXIT

MODAL_OPEN / OVERLAY_OPEN
  ├─ Receive "apply" (S/Enter) → close modal, return to parent state
  └─ Receive "cancel" (Esc) → close modal, return to parent state
```

### Inline Updates (Streaming Events)
```
Event: "source_found"
  → Update: counts.queued += 1
  → Render: progress grid (redraw 1 cell)

Event: "fetch_done"
  → Update: counts.running -= 1; counts.fetched += 1
  → Render: progress grid + sparkline (redraw 2 cells)

Event: "confidence_updated"
  → Update: confidence = 76%
  → Render: header (redraw 1 line)

Event: "cost_updated"
  → Update: cost = $0.23, tokens = 2,147
  → Render: cost tracker (redraw 3 lines)

Event: "answer_added"
  → Update: research_log.push(new_turn)
  → Render: research log (append 1-3 lines)
```

---

## STEP 6: Component Intents

### 1. StatusHeader Widget
**Intent:** Provide one-line context for entire research session
**Signal:** Header is "essential" (always rendered if possible)
**Props:**
- `query: String` — current research question
- `confidence: u8` — 0-100%
- `elapsed: Duration` — time since start
- `cost: f32` — $ spent so far
- `model: String` — "claude-3.5" or similar

**Render:**
```
Q: What is the history of...  [████████▒░] 76%  $0.23  ⏱ 2:45
```

### 2. ProgressGrid Widget
**Intent:** Show source pipeline visually (queued → running → fetched → parsed)
**Signal:** High priority (0.9) for UX clarity
**Props:**
- `queued: usize`, `running: usize`, `fetched: usize`, `parsed: usize`
- `confidence_history: Vec<u8>` — last 10 samples for sparkline

**Render:**
```
Queued: 12 [████] ⟳ Running: 2 [██░░░] ✓ Fetched: 18 [██████] ◐ Parsed: 15 [█████░]
Confidence: [████████▒░░░░░░░░] 72% → 76% (↑4% in 30s)
```

### 3. CostTracker Widget
**Intent:** Surface API spend and token usage for cost-aware research
**Signal:** Medium priority (0.7); omit if budget tight
**Props:**
- `api_calls: usize`, `rate_limit: usize`
- `tokens_used: usize`, `tokens_budget: usize`
- `cost_per_1k_tokens: f32`
- `elapsed: Duration`

**Render:**
```
API: 24 calls | Rate limit: 60/min  |  Tokens: 2,147 / 4,000  |  Cost: $0.23
Projected cost if linear: $0.31 (⚠ approaching budget)
```

### 4. ResearchLog Widget
**Intent:** Show Q→A chains with confidence at a glance
**Signal:** Scrollable; preserve only last N turns in viewport
**Props:**
- `turns: Vec<Turn>` — each turn has query, answer, confidence
- `selected: Option<usize>` — highlighted turn (for review)

**Render:**
```
Q: Founder?    → A: Alice (85%)    Q: When?    → A: 1999 (92%)
Q: Location?   → A: Silicon Valley (78%)
```

### 5. SourcesInline Widget (Modal)
**Intent:** Let user explore fetched sources without losing main UI
**Signal:** Overlay; low priority (0.3) render cost
**Props:**
- `sources: Vec<SourceMetadata>` — URL, fetch_time, relevance, excerpt
- `selected: Option<usize>` — which source is expanded
- `view_mode: SourceViewMode` — compact vs. detailed

**Render:**
```
[SOURCES INLINE]
  1. https://example.com/article    fetched: 234ms  rel: 0.92
     >>> "Alice founded the company in 1999..."
  2. https://wiki.example.com/...   fetched: 145ms  rel: 0.88
     (press ↓ to expand)
  ...
  (ESC to close, C to copy URL, O to open in browser)
```

### 6. InputHints Widget
**Intent:** Always-visible key map for current mode
**Signal:** Essential (always rendered)
**Props:**
- `state: UIState` — which keybindings are active
- `paused: bool` — affects hint text (Resume vs. Pause)

**Render:**
```
Pause (SPC) | Scope (A) | Sources (+) | Quit (Q)
```

---

## STEP 7: ASCII Wireframes for Inline Progress Display

### Frame 1: Initial Query (RUNNING, 5 seconds in)
```
┌──────────────────────────────────────────────────────────────────┐
│ Q: What is the early history of internet protocols?              │
│ [██░░░░░░░░░░░░░░░░░░░░░░░░░] 18%  $0.02  ⏱ 0:05               │
├──────────────────────────────────────────────────────────────────┤
│ Queued: 8 ⟳ Running: 1 ✓ Fetched: 2 ◐ Parsed: 1                │
│ Confidence: [██░░░░░░░░░░░░░░░░] 18% → 18% (stable)             │
├──────────────────────────────────────────────────────────────────┤
│ API: 3 calls | Tokens: 234 / 4,000 | Cost: $0.02                │
├──────────────────────────────────────────────────────────────────┤
│ Q1: What were early protocols? → (waiting for answer...)         │
├──────────────────────────────────────────────────────────────────┤
│ Pause (SPC) | Scope (A) | Sources (+) | Quit (Q)                │
└──────────────────────────────────────────────────────────────────┘
```

### Frame 2: Mid-Research (RUNNING, 1:30 in, confidence climbing)
```
┌──────────────────────────────────────────────────────────────────┐
│ Q: What is the early history of internet protocols?              │
│ [████████████░░░░░░░░░░░░░░░] 58%  $0.14  ⏱ 1:30                │
├──────────────────────────────────────────────────────────────────┤
│ Queued: 2 ⟳ Running: 3 ✓ Fetched: 15 ◐ Parsed: 13              │
│ Confidence: [███████████░░░░░░] 42% → 58% (↑16% in 60s)         │
├──────────────────────────────────────────────────────────────────┤
│ API: 14 calls | Tokens: 1,245 / 4,000 | Cost: $0.14             │
├──────────────────────────────────────────────────────────────────┤
│ Q1: Protocols? → A: TCP/IP, SMTP, HTTP (58%)                    │
│ Q2: When? → A: 1960s-1980s (62%)      Q3: Founders?  → ...      │
├──────────────────────────────────────────────────────────────────┤
│ Pause (SPC) | Scope (A) | Sources (+) | Quit (Q)                │
└──────────────────────────────────────────────────────────────────┘
```

### Frame 3: Research Paused (PAUSED)
```
┌──────────────────────────────────────────────────────────────────┐
│ Q: What is the early history of internet protocols?              │
│ [████████████░░░░░░░░░░░░░░░] 58%  $0.14  ⏱ 1:30  [⏸ PAUSED]   │
├──────────────────────────────────────────────────────────────────┤
│ Queued: 2 ⟳ Running: 0 ✓ Fetched: 15 ◐ Parsed: 13              │
│ Confidence: [███████████░░░░░░] 42% → 58% (frozen)              │
├──────────────────────────────────────────────────────────────────┤
│ API: 14 calls | Tokens: 1,245 / 4,000 | Cost: $0.14             │
├──────────────────────────────────────────────────────────────────┤
│ Q1: Protocols? → A: TCP/IP, SMTP, HTTP (58%)                    │
│ Q2: When? → A: 1960s-1980s (62%)      Q3: Founders?  → ...      │
├──────────────────────────────────────────────────────────────────┤
│ Resume (SPC) | Scope (A) | Sources (+) | Quit (Q)               │
└──────────────────────────────────────────────────────────────────┘
```

### Frame 4: Sources Overlay (+ key pressed)
```
┌──────────────────────────────────────────────────────────────────┐
│ Q: What is the early history of internet protocols?              │
│ [████████████░░░░░░░░░░░░░░░] 58%  $0.14  ⏱ 1:30                │
├──────────────────────────────────────────────────────────────────┤
│ [SOURCES (15 total)]                                             │
│  1. wikipedia.org/wiki/Internet_protocol   rel:0.95 ⏱ 234ms    │
│     >>> "Internet protocols are the set of rules governing..." │
│  2. rfc-editor.org/rfc/rfc-history.txt    rel:0.92 ⏱ 198ms    │
│  3. cs.stanford.edu/~jeanini/protocols    rel:0.88 ⏱ 456ms    │
│     (press ↓ to expand)                                         │
│  ...                                                            │
│  (C)opy URL  (O)pen in browser  (↑/↓) navigate  (ESC) close   │
└──────────────────────────────────────────────────────────────────┘
```

### Frame 5: Scope Modal (A key pressed)
```
┌──────────────────────────────────────────────────────────────────┐
│ [ADJUST RESEARCH SCOPE]                                          │
│                                                                  │
│  Max sources per category: 3 (1=strict, 9=broad)               │
│  Current: 5                                                     │
│                                                                  │
│  Cost-aware mode: ON (pause if budget exceeded)                │
│                                                                  │
│  Save & Apply (S)  |  Cancel (ESC)                             │
└──────────────────────────────────────────────────────────────────┘
```

### Frame 6: Research Completed (COMPLETED, final state)
```
┌──────────────────────────────────────────────────────────────────┐
│ Q: What is the early history of internet protocols? [✓ DONE]    │
│ [████████████████████████████] 92%  $0.31  ⏱ 4:52                │
├──────────────────────────────────────────────────────────────────┤
│ Queued: 0 ⟳ Running: 0 ✓ Fetched: 28 ◐ Parsed: 28             │
│ Confidence: [████████████████░░] 92% (stabilized)              │
├──────────────────────────────────────────────────────────────────┤
│ API: 28 calls | Tokens: 2,847 / 4,000 | Cost: $0.31            │
├──────────────────────────────────────────────────────────────────┤
│ FINAL ANSWERS:                                                   │
│ Q1: Protocols? → A: TCP/IP, SMTP, HTTP, FTP (92%)              │
│ Q2: When? → A: Developed across 1960s-1980s (94%)              │
│ Q3: Founders? → A: Cerf, Kahn, Postel, others (89%)            │
├──────────────────────────────────────────────────────────────────┤
│ Review (R) | Export (E) | Sources (+) | Save session (S)       │
└──────────────────────────────────────────────────────────────────┘
```

---

## Implementation Roadmap (FrankenTUI Harness)

### Phase 1: Core Widgets (Week 1)
- [ ] `StatusHeader` widget (essential, render first)
- [ ] `ProgressGrid` widget (essential, source pipeline bars + sparkline)
- [ ] `CostTracker` widget (medium priority, cost + token tracking)

### Phase 2: Interaction Layer (Week 2)
- [ ] Keybinding mapper (pause/resume, scope adjustment)
- [ ] Modal system (scope adjustment dialog)
- [ ] Input hints footer

### Phase 3: Advanced Views (Week 3)
- [ ] `ResearchLog` widget (scrollable Q→A turns)
- [ ] `SourcesInline` overlay (modal with URL list, expandable excerpts)
- [ ] Graceful degradation (budget system for cost-aware rendering)

### Phase 4: Integration & Polish (Week 4)
- [ ] Connect to research backend (message channel)
- [ ] Session save/load (metadata, research history)
- [ ] Theme cycling, responsive layout
- [ ] E2E snapshot tests (all 6 frames above)

---

## Design Rationale

### Why Inline Mode?
- **Preserves scrollback:** Research logs continue to be visible above UI chrome
- **No alt-screen flicker:** Familiar terminal behavior, no full-screen clears
- **Streaming friendly:** New answers append to log without disrupting footer controls
- **Pair-programming ready:** Multiple terminals can run research in parallel without tab switching

### Why Elm/Bubbletea Pattern (Model/Update/View)?
- **Deterministic state:** Confidence, cost, and source counts derive from single state
- **Message-driven:** External research backend sends events (source_found, fetch_done, answer_added)
- **Testable:** Snapshot tests verify each frame renders correctly at key moments
- **Hot-reload ready:** FrankenTUI's debug mode with InjectionIII allows rapid iteration

### Why Graceful Degradation (Budget System)?
- **Terminal with 1000 cells:** Show all 5 widget zones
- **Terminal with 500 cells:** Omit cost tracker, show compact research log (2 turns max)
- **Terminal with 200 cells:** Omit research log, show header + progress grid + footer only
- **Under load (frame > 16ms budget):** Essential widgets (header, progress, footer) always render

### Why Multi-Turn Research Log Visible?
- **Transparency:** User can see Q→A chain forming in real-time
- **Confidence tracking:** Each answer shows confidence %, builds trust
- **Audit trail:** Completed research includes full reasoning for reproducibility

---

## Success Criteria (MVP)

1. **Latency:** UI updates within 100ms of backend event (source_found, answer_added)
2. **Flicker:** Zero cursor drift, no flashing on progress updates (validated via ftui-harness flicker detection)
3. **Scrollback:** Logs above UI always preserved, no truncation
4. **Keystroke response:** Pause/Resume (SPC), Scope (A), Sources (+) respond in < 50ms
5. **Graceful degradation:** Renders correctly at 80x24, 120x40, and 160x50 terminal sizes
6. **Streaming:** Handles 10+ source discoveries per second without visual stutter
7. **Session persistence:** Save/load research metadata (questions, answers, sources) across CLI invocations

---

## References

### FrankenTUI Architecture
- **Inline Mode Strategy:** `/tmp/frankentui/docs/adr/ADR-001-inline-mode.md`
- **Agent Harness Pattern:** `/tmp/frankentui/crates/ftui-harness/src/main.rs`
- **Widget Implementations:** `/tmp/frankentui/crates/ftui-widgets/src/`
- **Keybinding Policy:** `/tmp/frankentui/docs/spec/keybinding-policy.md`

### Design Systems Referenced
- **Elm Architecture:** https://guide.elm-lang.org/architecture/
- **Bubbletea (Go TUI):** https://github.com/charmbracelet/bubbletea
- **Budget System:** `/tmp/frankentui/crates/ftui-widgets/src/budgeted.rs`

### UX Discovery Framework
This synthesis follows the **7-step UX pipeline**:
1. Problem framing (pain ↔ desired outcome)
2. Jobs to be Done (when, desired outcome, effort target)
3. Task decomposition (critical paths, zones)
4. Information architecture (layout, data flow, zones)
5. Interaction model (keyboard, state machine, streaming)
6. Component intents (6 widgets, signals, props, renders)
7. ASCII wireframes (6 key frames from initial → completed)

---

## Appendix: Keyboard Quick Reference

| Action | Shortcut | Context | Effect |
|--------|----------|---------|--------|
| Pause research | SPC | RUNNING | → PAUSED, freeze UI |
| Resume research | SPC | PAUSED | → RUNNING, restart |
| Adjust scope | A | Any | Open modal, no state change |
| View sources | + | Any | Toggle overlay (modal) |
| Toggle sources | Esc Esc | Any | Same as +, double-Esc |
| Quit gracefully | Q | Any | → CLEANUP → EXIT |
| Hard quit | Ctrl+C | Any | EXIT immediately |
| Soft quit | Ctrl+D | RUNNING | Cancel research, then EXIT |
| Soft quit | Ctrl+D | PAUSED | EXIT immediately |
| Scroll log up | PageUp | Any | Scroll viewport up |
| Scroll log down | PageDown | Any | Scroll viewport down |
| Copy URL | C | OVERLAY | Copy selected source URL |
| Open in browser | O | OVERLAY | Launch browser (if X11/WSL) |
| Navigate up | ↑ | OVERLAY | Move selection up |
| Navigate down | ↓ | OVERLAY | Move selection down |
| Expand/collapse | Enter | OVERLAY | Expand source excerpt |
| Close modal | Esc | MODAL | Return to parent state |
| Apply changes | S | MODAL (Scope) | Save & close |
| Theme cycle | Ctrl+T | Any | Next theme (light/dark/alt) |

---

**End of UX Synthesis**
Generated: 2026-02-04 by Claude Code (Haiku 4.5)
Framework: FrankenTUI inline mode + Elm/Bubbletea architecture
