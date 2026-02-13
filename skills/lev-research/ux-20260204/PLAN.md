# Research TUI Implementation Plan

**Epic:** `oclaw-v13` - Research TUI: Real-time progress visualization
**Created:** 2026-02-04
**UX Spec:** `./SYNTHESIS.md`

---

## Overview

Build a terminal UI for real-time research progress tracking. Shows confidence levels, cost tracking, and source discovery as it happens. Supports headless mode for CI/automation.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     research-tui                             │
├─────────────────────────────────────────────────────────────┤
│  UI Layer (Ink/React)                                       │
│  ├── DashboardView       ← Session list, quick search       │
│  ├── SessionView         ← Progress, sources, cost panels   │
│  └── SettingsView        ← API status, preferences          │
├─────────────────────────────────────────────────────────────┤
│  State Machine (XState)                                     │
│  ├── States: idle → searching → extracting → synthesizing   │
│  ├── Events: START, SOURCE_FOUND, TURN_COMPLETE, ERROR      │
│  └── Context: session, turns[], sources[], cost             │
├─────────────────────────────────────────────────────────────┤
│  Backend Adapters (EventEmitter wrappers)                   │
│  ├── ValyuAdapter        ← valyu research/answer CLI        │
│  ├── FirecrawlAdapter    ← firecrawl scrape/extract         │
│  └── BraveAdapter        ← brave-search CLI                 │
├─────────────────────────────────────────────────────────────┤
│  Session Store (XDG: ~/.config/LEV/research/)               │
│  └── sessions.json, {session-id}.json                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Phases

### Phase 1: Core TUI Scaffold (`oclaw-7y0`)

**Goal:** Basic TUI shell with state machine

**Deliverables:**
- [ ] Project setup: `~/.claude/skills/lev-research/tui/`
- [ ] Package.json with Ink, XState, chalk deps
- [ ] State machine definition (FSM from UX spec)
- [ ] Basic layout components (Header, Footer, Panel)
- [ ] Session storage integration (existing XDG location)
- [ ] Entry point: `research-tui` CLI command

**Acceptance Criteria:**
```bash
research-tui          # Shows dashboard with session list
research-tui --help   # Shows usage
```

**Files to Create:**
```
tui/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.tsx           # Entry point
│   ├── machine.ts          # XState machine
│   ├── store.ts            # Session persistence
│   └── components/
│       ├── Dashboard.tsx
│       ├── Header.tsx
│       ├── Footer.tsx
│       └── Panel.tsx
└── dist/                   # Built output
```

---

### Phase 2: Backend Integration (`oclaw-3kw`)

**Goal:** Wire existing CLIs to emit progress events

**Deliverables:**
- [ ] EventEmitter wrapper for valyu CLI
- [ ] EventEmitter wrapper for firecrawl CLI
- [ ] EventEmitter wrapper for brave-search CLI
- [ ] Progress event protocol (turn, source, cost)
- [ ] SessionView with live updates

**Acceptance Criteria:**
```bash
research-tui "AI agents 2026"     # Live progress display
# Shows: Turn 1/5, sources streaming, cost accumulating
```

**Event Protocol:**
```typescript
interface ResearchEvent {
  type: 'turn_start' | 'source_found' | 'turn_complete' | 'error';
  timestamp: string;
  data: {
    turn?: number;
    maxTurns?: number;
    confidence?: number;
    source?: { url: string; title: string; relevance: number };
    cost?: number;
    error?: string;
  };
}
```

---

### Phase 3: Headless Mode (`oclaw-vjc`)

**Goal:** CI-friendly output without TUI

**Deliverables:**
- [ ] `--headless` flag to disable Ink rendering
- [ ] `--output=json` for structured output
- [ ] `--output=ndjson` for streaming JSON lines
- [ ] Progress to stderr, results to stdout
- [ ] Exit codes (0=success, 1=error, 2=low confidence)

**Acceptance Criteria:**
```bash
research-tui --headless "query" --output=json > results.json
# stderr shows progress lines
# stdout is valid JSON with results

research-tui --headless "query" --output=ndjson | jq .
# Streaming JSON lines as events occur
```

**Headless Output Format:**
```
[2026-02-04T01:15:32Z] TURN 1/5: sources: 8, confidence: 0.45, cost: $0.0123
[2026-02-04T01:15:39Z] TURN 2/5: sources: 12, confidence: 0.68, cost: $0.0156
[2026-02-04T01:15:46Z] TURN 3/5: sources: 14, confidence: 0.87, cost: $0.0189
[2026-02-04T01:15:52Z] COMPLETE: 3 turns, 34 sources, $0.0468
```

---

## DoR Checklist

### ENTRY
- [x] UX spec complete (`SYNTHESIS.md`)
- [x] BD tasks created with dependencies
- [ ] Existing CLI adapters reviewed

### DONE_STATE
- [ ] `research-tui` command available
- [ ] Live progress display working
- [ ] Headless mode for CI
- [ ] Session persistence across restarts

### CRITERIA
- Real-time visualization of turns, sources, costs
- Works over SSH (no fancy terminal features)
- Pure Node.js (no native deps)
- Integrates with existing CLIs without modification

### TOUCHPOINTS
- `~/.claude/skills/lev-research/backends/*/cli/`
- `~/.config/LEV/research/` (session storage)
- `/search` command shim

### INTEGRATION
- XDG-compliant paths
- Reuses existing backend CLIs
- Adds TUI layer without changing core logic

### E2E
```bash
# Full test
research-tui "test query" --mode=quick
# Should show progress, complete in <10s

# Headless test
research-tui --headless "test" --output=json | jq .confidence
# Should output numeric confidence value
```

---

## Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **TUI Framework** | Ink (React for CLI) | Composable, well-documented |
| **State Machine** | XState | Robust FSM, visualization tools |
| **Session Storage** | JSON files | Simple, debuggable, XDG-compliant |
| **Styling** | chalk + ink-box | Cross-platform terminal colors |

---

## Risks

| Risk | Mitigation |
|------|------------|
| Ink SSR issues over SSH | Test with `--headless` fallback |
| Backend CLIs not emitting events | Wrap stdout parsing as fallback |
| State machine complexity | Start simple, add states as needed |

---

## Next Action

Start with `oclaw-7y0` (Phase 1):

```bash
bd update oclaw-7y0 --status=in_progress
mkdir -p ~/.claude/skills/lev-research/tui
cd ~/.claude/skills/lev-research/tui
npm init -y
npm install ink ink-spinner ink-box xstate chalk
```
