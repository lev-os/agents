# UX Discovery Index — Research Hub CLI (FrankenTUI)

**Location:** `~/.agents/skills/lev-research/ux-frankentui-20260204/`
**Date:** 2026-02-04
**Framework:** FrankenTUI 7-Step UX Pipeline + Elm/Bubbletea Architecture

---

## Files in This Directory

### 1. SYNTHESIS.md (547 lines, 28KB) — MAIN DELIVERABLE
**Read this first for complete 7-step UX pipeline**

Contains the full, detailed specification:
- **Step 1: Problem Framing** — Pain points (transparency gap) → desired outcome (real-time visibility)
- **Step 2: Jobs to be Done** — Three user needs with effort targets
- **Step 3: Task Decomposition** — Widget breakdown, critical paths, zone priorities
- **Step 4: Information Architecture** — Inline mode layout, data flow, zones with priorities
- **Step 5: Interaction Model** — Keyboard shortcuts, state machine, streaming events
- **Step 6: Component Intents** — 6 widgets with signal priority, props, render specs
- **Step 7: ASCII Wireframes** — 6 key frames from initial (18%) to completed (92%)

Also includes:
- Implementation roadmap (4 weeks)
- Design rationale (why inline, why Elm, why budget system)
- Success criteria (MVP)
- Keyboard quick reference
- References to FrankenTUI docs

**Audience:** Product managers, architects, engineers doing detailed planning
**Time to read:** 30-45 minutes for full understanding

---

### 2. README.md (240 lines, 10KB) — QUICK REFERENCE
**Read this for executive overview and implementation planning**

High-level guide covering:
- Product overview (what, why, who)
- Widget specifications table (all 6 components with priority/cost)
- Keyboard shortcuts reference (all bindings)
- 4-week implementation plan with checkboxes
- Design rationale (3 key decisions explained)
- Success criteria (latency, flicker, throughput, etc.)
- Integration points with FrankenTUI
- File structure and next steps

**Audience:** Project managers, tech leads, stakeholders
**Time to read:** 10-15 minutes

---

### 3. EXECUTIVE_SUMMARY.txt (500+ lines, 16KB) — STAKEHOLDER BRIEF
**Read this for high-level understanding and decision support**

Distilled version including:
- Key insight (the research transparency problem)
- Architecture decision (inline mode + Elm/Bubbletea + budget system)
- Widget breakdown (6 components, essential vs. optional)
- Interaction model (keyboard shortcuts, state machine)
- Wireframe frames (6 key moments, 5-line descriptions)
- Implementation roadmap
- Success criteria
- Design principles
- FrankenTUI integration points
- Questions for stakeholders

**Audience:** Non-technical stakeholders, product leads, executives
**Time to read:** 15-20 minutes

---

## How to Use This Directory

### For Different Roles:

**Product Manager:**
1. Start with EXECUTIVE_SUMMARY.txt (15 min)
2. Review wireframes in SYNTHESIS.md (10 min)
3. Check success criteria in README.md (5 min)
4. Discuss questions for stakeholders with team

**Engineer (Building Core Widgets):**
1. Read SYNTHESIS.md (45 min) for full context
2. Focus on Step 6 (Component Intents) for widget specs
3. Reference README.md widget table for priority/cost
4. Check ftui-harness/src/main.rs for pattern reference

**Engineer (Building Interaction Layer):**
1. Read Step 5 (Interaction Model) in SYNTHESIS.md
2. Check keyboard shortcuts table in README.md
3. Review state machine diagram
4. Reference keybinding-policy.md in FrankenTUI

**Engineer (Building Backend Integration):**
1. Read Step 4 (Information Architecture) for data flow
2. Review Section "Inline Updates (Streaming Events)" in SYNTHESIS.md
3. Design event schema based on message types listed
4. Connect research backend to message channel

**Stakeholder (Approving Design):**
1. Read EXECUTIVE_SUMMARY.txt (20 min)
2. Review wireframes (6 frames in SYNTHESIS.md)
3. Check "Questions for Stakeholders" section
4. Approve or request changes

---

## Key Sections by Task

### Understanding the Product
- EXECUTIVE_SUMMARY.txt: "KEY INSIGHT: THE RESEARCH HUB PROBLEM"
- SYNTHESIS.md: "Step 1: Problem Framing"
- SYNTHESIS.md: "Step 2: Jobs to be Done"

### Designing Widgets
- SYNTHESIS.md: "Step 6: Component Intents" (full specs for all 6 widgets)
- README.md: "Widget Specifications Table" (quick reference)
- SYNTHESIS.md: "Step 4: Information Architecture" → "Zones & Priority" table

### Planning Interaction
- SYNTHESIS.md: "Step 5: Interaction Model" → "Keyboard Shortcuts"
- SYNTHESIS.md: "Step 5: Interaction Model" → "State Machine"
- README.md: "Keyboard Shortcuts Reference"

### Visualizing the UI
- SYNTHESIS.md: "Step 7: ASCII Wireframes" (6 key frames)
- EXECUTIVE_SUMMARY.txt: "WIREFRAME FRAMES (6 KEY MOMENTS)"

### Implementing
- SYNTHESIS.md: "Implementation Roadmap (FrankenTUI Harness)" → Phase 1-4
- README.md: "4-Week Implementation Plan"
- EXECUTIVE_SUMMARY.txt: "NEXT STEPS" → 7 detailed steps

### Verifying Success
- README.md: "Success Criteria (MVP)"
- EXECUTIVE_SUMMARY.txt: "SUCCESS CRITERIA (MVP)"
- SYNTHESIS.md: "Success Criteria (MVP)"

---

## Quick Facts

| Aspect | Details |
|--------|---------|
| **Product** | Research Hub CLI — Real-time research progress visualization |
| **Framework** | FrankenTUI (Rust TUI, inline mode, agent harness) |
| **Architecture** | Elm/Bubbletea pattern (Model/Update/View) |
| **Screen Mode** | Inline (preserves scrollback) with hybrid scroll-region strategy |
| **Widgets** | 6 components (3 essential, 3 optional) |
| **Cost per Frame** | ~370µs total (header 50µs + grid 80µs + hints 10µs + extras 230µs) |
| **Keyboard** | 10+ shortcuts (SPC pause, A scope, + sources, Q quit) |
| **States** | IDLE → RUNNING → PAUSED → COMPLETED → EXIT |
| **Degradation** | Graceful via budget system (omit non-essential under load) |
| **Terminal Support** | 80x24 through 160x50 (tested sizes) |
| **Persistence** | Session save/load (metadata format TBD) |
| **MVP Timeline** | 4 weeks (1 core, 2 interaction, 3 advanced, 4 polish) |

---

## Architecture Overview

```
RESEARCH BACKEND (async, multi-threaded)
    ├─ API: query research questions
    ├─ Fetch: crawl URLs
    ├─ Extract: parse documents
    └─ Emit events: source_found, fetch_done, confidence_updated, answer_added

MESSAGE CHANNEL (mpsc)
    └─ Async-safe bridge between backend and UI

RUNTIME LOOP (FrankenTUI)
    ├─ Tick every 100ms (spinner animation)
    ├─ Poll message channel
    ├─ Update state (counts, confidence, cost)
    ├─ Call view() to render widgets
    └─ Present diff (only changed cells)

RENDER ENGINE
    ├─ Frame buffer (2D grid of cells)
    ├─ Scissor stack (clipping regions)
    ├─ Buffer diff (compute delta from last frame)
    └─ ANSI presenter (emit escape sequences)

TERMINAL OUTPUT (Inline Mode)
    ├─ Save cursor (DEC 7)
    ├─ Write ANSI (queued messages)
    ├─ Restore cursor (DEC 8)
    └─ Synchronized output (mode 2026, atomic)
```

---

## Widget Hierarchy

```
ResearchHubUI (Model)
├─ StatusHeader (1 line, essential)
│  └─ Query + Confidence + ETA + Cost + Model name
├─ ProgressGrid (2 lines, essential)
│  └─ Queued | Running | Fetched | Parsed (with sparkline)
├─ CostTracker (3 lines, optional, priority 0.7)
│  └─ API calls | Tokens | Cost | Projection
├─ ResearchLog (fill, optional, priority 0.6)
│  ├─ Turn 1: Q → A (Confidence %)
│  ├─ Turn 2: Q → A (Confidence %)
│  └─ ... (scrollable)
├─ InputHints (1 line, essential)
│  └─ Key map: Pause | Scope | Sources | Quit
└─ SourcesInline (modal, optional, priority 0.3)
   ├─ Source 1: URL (fetch time, relevance, excerpt)
   ├─ Source 2: URL (...)
   └─ ... (overlay, on-demand)
```

---

## References & Links

### FrankenTUI Documentation
- **ADR-001: Inline Mode Strategy** — `/tmp/frankentui/docs/adr/ADR-001-inline-mode.md`
- **Agent Harness Pattern** — `/tmp/frankentui/crates/ftui-harness/src/main.rs` (1,858 lines)
- **Widget Library** — `/tmp/frankentui/crates/ftui-widgets/src/` (37 widgets)
- **Keybinding Policy** — `/tmp/frankentui/docs/spec/keybinding-policy.md`
- **Development Guidelines** — `/tmp/frankentui/AGENTS.md`

### Design Patterns
- **Elm Architecture** — https://guide.elm-lang.org/architecture/
- **Bubbletea (Go TUI)** — https://github.com/charmbracelet/bubbletea (reference)
- **Budget System** — `/tmp/frankentui/crates/ftui-widgets/src/budgeted.rs`

### Terminal Protocols
- **DEC Sequences** — ESC7/ESC8 (cursor save/restore)
- **ANSI Escape Codes** — CSI sequences (color, style)
- **Synchronized Output** — CSI ? 2026 h/l (atomic updates)
- **Scroll Region** — CSI t;b r (DECSTBM, optimization only)

---

## FAQ

**Q: Why inline mode and not full-screen?**
A: Inline mode preserves research logs in scrollback (valuable for audit), avoids flicker, and works better with terminal multiplexers. FrankenTUI uses hybrid strategy: scroll-region optimization + overlay fallback.

**Q: Why 6 widgets instead of 1 monolithic view?**
A: Modularity enables independent testing, reusability (StatusHeader works in other CLIs), graceful degradation (omit non-essential under load), and clearer responsibility separation.

**Q: How does streaming research work?**
A: Backend emits events via message channel; runtime polls every 100ms, updates state deterministically, and renders diff. No blocking I/O.

**Q: What if terminal is too small?**
A: Budget system gracefully degrades: 1000 cells (all widgets) → 500 cells (omit cost tracker) → 200 cells (header + progress + footer only). Essential widgets always render.

**Q: How is this different from other research CLIs?**
A: This design prioritizes transparency (confidence %, cost, source list), responsiveness (< 50ms keystroke latency), and preservation (scrollback, session save/load). Most research CLIs lack real-time visibility.

---

## Checklists

### Pre-Implementation Review
- [ ] Problem framing approved (transparency gap confirmed)
- [ ] JTBD validated (monitor, intervene, review)
- [ ] Widget breakdown accepted (6 components, priorities)
- [ ] Wireframes approved (all 6 frames)
- [ ] Keyboard shortcuts finalized
- [ ] Event schema defined (source_found, fetch_done, etc.)
- [ ] Success criteria accepted (latency, flicker, throughput)

### Week 1 (Core Widgets)
- [ ] StatusHeader renders correctly (1 line, 50µs)
- [ ] ProgressGrid renders correctly (2 lines, 80µs)
- [ ] CostTracker renders correctly (3 lines, 40µs)
- [ ] All widgets tested at 80x24, 120x40, 160x50
- [ ] Budget system scoring verified

### Week 2 (Interaction)
- [ ] Keybinding mapper implemented (SPC, A, +, Q)
- [ ] Modal system working (scope adjustment)
- [ ] Input hints footer displaying correctly
- [ ] State machine transitions verified

### Week 3 (Advanced Views)
- [ ] ResearchLog widget scrolling correctly
- [ ] SourcesInline overlay rendering
- [ ] URL expansion/collapse working
- [ ] Session save/load format defined

### Week 4 (Polish)
- [ ] Theme cycling working
- [ ] Responsive layout tested
- [ ] Snapshot tests for all 6 wireframes
- [ ] Flicker detection passing
- [ ] Documentation complete

---

## Versioning

**v1.0** — Initial 7-step UX pipeline discovery
- Date: 2026-02-04
- Framework: FrankenTUI + Elm/Bubbletea
- Widgets: 6 components (3 essential, 3 optional)
- Keybindings: 10+ shortcuts
- Wireframes: 6 key frames

Future versions may iterate on:
- Widget count or breakdown
- Keybinding scheme
- Theme options
- Session persistence format
- Streaming event schema

---

## Contact & Questions

For questions or feedback on this UX discovery:
- Consult EXECUTIVE_SUMMARY.txt "QUESTIONS FOR STAKEHOLDERS"
- Review SYNTHESIS.md "Design Rationale" section
- Reference README.md "Next Steps" section

---

**Generated:** 2026-02-04 by Claude Code (Haiku 4.5)
**Framework:** FrankenTUI 7-Step UX Pipeline + Elm/Bubbletea Architecture
**Status:** Ready for stakeholder review and implementation spikes
