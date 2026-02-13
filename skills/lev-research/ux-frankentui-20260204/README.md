# Research Hub CLI UX Discovery — FrankenTUI Framework

**Project Code:** `oclaw-tdz` (OpenClaw research terminal display)
**Date:** 2026-02-04
**Framework:** FrankenTUI 7-step UX Pipeline

## Overview

This directory contains the complete UX discovery synthesis for a **Research Hub CLI** — a real-time terminal UI tool that visualizes research progress (multi-turn queries, source discovery, cost tracking) without losing scrollback logs.

## Key Deliverables

### SYNTHESIS.md (547 lines, 32KB)
Comprehensive 7-step UX pipeline covering:

1. **Problem Framing** — Research transparency gap (no visibility into source queries, confidence, cost)
2. **Jobs to be Done** — Three user needs: monitor progress, intervene when needed, review sources later
3. **Task Decomposition** — Widget breakdown (header, progress grid, cost tracker, research log, input hints, sources overlay)
4. **Information Architecture** — Inline mode layout preserving scrollback + 6 widget zones with priority (essential vs. optional)
5. **Interaction Model** — Keybindings (SPA, A, +, Q), state machine (IDLE → RUNNING → PAUSED → COMPLETED), streaming events
6. **Component Intents** — 6 widgets with signal priority, props, and render specs
7. **ASCII Wireframes** — 6 key frames from initial query (18% confidence) through completed research (92% confidence)

### Architecture Decisions

**Why Inline Mode (not alt-screen)?**
- Preserves scrollback for research logs
- No full-screen flicker or cursor drift
- Multi-terminal friendly for parallel research
- Uses FrankenTUI's hybrid strategy (scroll-region optimization + overlay redraw fallback)

**Why Elm/Bubbletea Pattern?**
- Deterministic state (confidence, cost, counts derived from single source)
- Message-driven architecture (research backend sends events)
- Testable via snapshot tests
- Hot-reload ready for rapid iteration

**Why Graceful Degradation (Budget System)?**
- 1000-cell terminal: render all 5 zones
- 500-cell terminal: omit cost tracker, compact log
- 200-cell terminal: header + progress + footer only
- Essential widgets always render; optional degrade under frame-time pressure

## Widget Specifications

| Widget | Essential | Priority | Cost | Renders |
|--------|-----------|----------|------|---------|
| StatusHeader | YES | 1.0 | 50µs | Q, confidence %, ETA, cost, model |
| ProgressGrid | YES | 0.9 | 80µs | Source pipeline (queued→running→fetched→parsed) + sparkline |
| CostTracker | NO | 0.7 | 40µs | API calls, tokens, cost, projected spend |
| ResearchLog | NO | 0.6 | 200µs | Q→A turns with confidence scores |
| InputHints | YES | 0.5 | 10µs | Key map (Pause, Scope, Sources, Quit) |
| SourcesInline | NO | 0.3 | 150µs | Modal overlay with URL list, excerpts |

## Keyboard Shortcuts

**Core Actions:**
- **SPC** — Pause/Resume research
- **A** — Adjust research scope (modal)
- **+** / **Esc Esc** — Toggle sources overlay
- **Q** / **Ctrl+C** — Quit (gracefully or hard)

**Navigation:**
- **PageUp/Dn** — Scroll research log
- **↑/↓ (in overlay)** — Navigate sources
- **Enter (in overlay)** — Expand/collapse excerpt

**Copy/Browse:**
- **C (in overlay)** — Copy URL to clipboard
- **O (in overlay)** — Open in browser

**Utility:**
- **Ctrl+T** — Cycle theme (dark/light/alt)

## Implementation Phases (4 weeks)

### Week 1: Core Widgets
- [ ] StatusHeader (essential, render first)
- [ ] ProgressGrid (essential, source pipeline + sparkline)
- [ ] CostTracker (medium priority, cost + tokens)

### Week 2: Interaction Layer
- [ ] Keybinding mapper (SPC, A, +, Q)
- [ ] Modal system (scope adjustment)
- [ ] Input hints footer

### Week 3: Advanced Views
- [ ] ResearchLog widget (scrollable Q→A turns)
- [ ] SourcesInline overlay (URL list + excerpts)
- [ ] Budget system (graceful degradation)

### Week 4: Integration & Polish
- [ ] Connect to research backend (message channel)
- [ ] Session save/load (metadata, history)
- [ ] Theme cycling, responsive layout
- [ ] E2E snapshot tests (all 6 wireframes)

## Design Rationale

### Inline Mode Strategy
FrankenTUI uses a **hybrid inline strategy** (ADR-001):
- Default: **Scroll-region optimization** (modern terminals without muxes)
- Fallback: **Overlay redraw** (tmux/screen, or when unsupported)

Both strategies preserve **cursor position via DEC 7/8** and **synchronized output (mode 2026)**.

### Elm/Bubbletea Architecture
Research Hub CLI follows FrankenTUI's **Model/Update/View** pattern:
```
Message Channel (research backend)
    ↓
Update (modify state: counts, confidence, cost)
    ↓
View (render widgets based on state)
    ↓
Present (diff-based ANSI output)
```

### Message-Driven Streaming
Backend emits events; UI reacts deterministically:
- `source_found` → update count, redraw progress grid
- `fetch_done` → move source from "running" to "fetched", redraw grid
- `confidence_updated` → update header, redraw 1 line
- `answer_added` → append turn to log, scroll viewport

## Wireframe Reference

### Frame 1: Initial Query (5s in, 18% confidence)
Shows research starting up, first API calls, no sources fetched yet.

### Frame 2: Mid-Research (1:30 in, 58% confidence)
Shows 15 fetched sources, 3 in-progress, confidence climbing, 2 turns answered.

### Frame 3: Research Paused
Research frozen at 58%, showing current state, hints change to "Resume (SPC)".

### Frame 4: Sources Overlay (+ key)
Modal showing 15 fetched sources with URL, fetch time, relevance score, expandable excerpts.

### Frame 5: Scope Modal (A key)
Adjustment dialog for max sources per category, cost-aware mode toggle.

### Frame 6: Research Completed
Final state: 92% confidence, 28 sources parsed, $0.31 cost, all answers visible.

## FrankenTUI Integration Points

### From ftui-harness/src/main.rs:
- **Elm/Bubbletea pattern** — Model trait, Message enum, init/update/view/subscriptions
- **Inline mode** — ScreenMode::Inline { ui_height }, DEC 7/8 cursor save/restore
- **StatusLine widget** — Key hints, separators, left/center/right layout
- **Block widget** — Title, borders, style, inner area calculation
- **Budget system** — Budgeted<W>, WidgetSignal, priority scoring
- **LogViewer widget** — Streaming log appends, scrolling, markup support

### From ADR-001 (Inline Mode Strategy):
- **Terminal capabilities** — Detect mux, scroll-region, synchronized output
- **Cleanup invariants** — RAII Drop implementation for terminal state restoration
- **Cursor position** — DEC ESC7/ESC8 (more portable than CSI s/u)

### From Keybinding Policy:
- **ActionMapper** — Resolves Esc sequences, Ctrl+C priority, double-Esc detection
- **AppState** — Context for keybinding resolution (input_present, task_running, modal_open, overlay_open)

## Success Criteria (MVP)

| Criterion | Target |
|-----------|--------|
| Latency | UI updates within 100ms of backend event |
| Flicker | Zero cursor drift, no flashing on progress updates |
| Scrollback | Logs above UI always preserved, no truncation |
| Keystroke response | Pause/Resume/Scope/Sources in < 50ms |
| Terminal support | 80x24, 120x40, 160x50 all render correctly |
| Throughput | Handle 10+ source discoveries/sec without stutter |
| Persistence | Save/load research metadata across CLI runs |

## References

### FrankenTUI Docs
- **ADR-001: Inline Mode Strategy** — `/tmp/frankentui/docs/adr/ADR-001-inline-mode.md`
- **Agent Harness Pattern** — `/tmp/frankentui/crates/ftui-harness/src/main.rs` (reference app)
- **Widget Implementations** — `/tmp/frankentui/crates/ftui-widgets/src/` (37 widgets)
- **Keybinding Policy** — `/tmp/frankentui/docs/spec/keybinding-policy.md`
- **AGENTS.md** — `/tmp/frankentui/AGENTS.md` (development guidelines)

### Design Systems
- **Elm Architecture** — https://guide.elm-lang.org/architecture/
- **Bubbletea (Go TUI)** — https://github.com/charmbracelet/bubbletea (reference impl)
- **FrankenTUI Budget System** — `/tmp/frankentui/crates/ftui-widgets/src/budgeted.rs`

### UX Framework
This synthesis applies the **7-step UX pipeline** originally developed for Kingly Assistant:
1. Problem framing
2. Jobs to be Done
3. Task decomposition
4. Information architecture
5. Interaction model
6. Component intents
7. ASCII wireframes

## Next Steps

1. **Review & Validate** — Stakeholders confirm problem framing, JTBD, and wireframes
2. **Spike: Core Widgets** — Build StatusHeader, ProgressGrid, CostTracker in ftui-widgets
3. **Spike: Backend Integration** — Research backend → message channel → UI state updates
4. **Spike: Interaction** — Keybinding mapper, modals, overlay system
5. **Spike: Polish** — Theme cycling, responsive layout, session save/load
6. **E2E Tests** — Snapshot tests for all 6 wireframes + flicker validation
7. **Documentation** — Component API docs, event schema, session format

## File Structure

```
~/.claude/skills/lev-research/ux-frankentui-20260204/
├── README.md                    (this file)
├── SYNTHESIS.md                 (full 7-step UX pipeline)
└── [future: component specs, API schema, session format]
```

## Questions & Discussion

**Q: Why inline mode instead of full-screen?**
A: Inline mode preserves research logs in scrollback, which is valuable for audit and debugging. It also avoids the flicker and cursor corruption issues that plagued early implementations.

**Q: Why 6 widgets instead of 1 monolithic view?**
A: Modularity enables independent testing, reusability (StatusHeader works in other CLI tools), and graceful degradation (omit non-essential widgets under load).

**Q: Why Elm/Bubbletea instead of async/await directly?**
A: Elm pattern ensures deterministic state, making rendering predictable and testable. It's also battle-tested in production Go TUIs (Bubbletea).

**Q: How does this handle streaming research (continuous new sources)?**
A: Backend emits events via message channel; runtime loop polls channel every 100ms, updates state, and renders diff. No blocking.

**Q: What if research is slow and fills scrollback?**
A: LogViewer widget manages a fixed buffer (configurable, default 10,000 lines). Old entries are discarded; search results are preserved via session save.

---

**Generated:** 2026-02-04 by Claude Code (Haiku 4.5)
**Framework:** FrankenTUI 7-step UX Pipeline + Elm/Bubbletea Architecture
