# UX Discovery: Research TUI v1.0

## Problem Statement

**When** running multi-step research operations (recursive confidence, multi-source synthesis, team-based deep research), **users** cannot visualize progress, costs, confidence levels, or source discovery in real-time. They see only sequential CLI output, losing situational awareness during long-running operations.

**Success Criteria:**
- Real-time visualization of research progress
- Cost tracking per operation
- Confidence level display (recursive research)
- Source discovery stream
- Headless mode for CI/automation
- Session persistence across terminal restarts

**Constraints:**
- Terminal-only (no web UI)
- Must work over SSH
- Should not require additional runtimes (pure Node.js)
- Must integrate with existing CLIs (valyu, firecrawl, brave-search)

---

## Jobs to Be Done (Top 3)

### Job 1: Progress Monitoring
> "When I run a deep research query, I want to see which turn I'm on and how confidence is building, so I can decide whether to let it continue or intervene."

**Triggers:** `/search deep`, `valyu research`, team spawns
**User Types:** Power users (INTJ), Operators (ISTJ)

### Job 2: Cost Awareness
> "When running multiple searches, I want to see cumulative cost in real-time, so I can stop before exceeding my budget."

**Triggers:** Any paid API call (valyu, firecrawl, brave)
**User Types:** Budget-conscious (ISTJ), Teams (ENTJ)

### Job 3: Source Validation
> "When research finds sources, I want to see them stream in with metadata, so I can validate quality without waiting for completion."

**Triggers:** Search results arriving, content extraction
**User Types:** Researchers (INTP), QA (ISTJ)

---

## Task Graph

```
┌─────────────────────────────────────────────────────────────┐
│                    RESEARCH TUI FSM                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [INIT] ─────> [IDLE] ─────> [SEARCHING] ─────> [COMPLETE]  │
│                  │               │                  │        │
│                  │               ▼                  │        │
│                  │          [EXTRACTING]           │        │
│                  │               │                  │        │
│                  │               ▼                  │        │
│                  │         [SYNTHESIZING]          │        │
│                  │               │                  │        │
│                  ▼               ▼                  ▼        │
│              [ERROR] <───── [any state] ────> [PAUSED]      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**States:**
- `IDLE`: Waiting for input, showing session list
- `SEARCHING`: Running search operations (brave, firecrawl, valyu search)
- `EXTRACTING`: Scraping/crawling content
- `SYNTHESIZING`: AI synthesis (valyu answer/research, oracle)
- `COMPLETE`: Results ready, showing summary
- `PAUSED`: User intervention requested
- `ERROR`: Recoverable error state

---

## Information Architecture

### Entities
| Entity | Attributes | Actions |
|--------|------------|---------|
| **Session** | id, query, status, created_at, cost | create, resume, complete, export |
| **Turn** | number, query, confidence, sources, cost | - |
| **Source** | url, title, type, relevance | view, exclude |
| **Operation** | tool, status, duration, cost | cancel |

### Navigation
```
research-tui
├── Dashboard (default)
│   ├── Active Sessions
│   ├── Quick Search
│   └── Recent Results
├── Session View
│   ├── Progress Panel
│   ├── Sources Panel
│   └── Cost Panel
└── Settings
    ├── API Keys Status
    └── Preferences
```

---

## Wireframe: Main Dashboard

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🔍 Research TUI v1.0                          [H]elp [S]ettings [Q]uit │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─ Active Session ────────────────────────────────────────────────────┐│
│  │  Query: "AI agent frameworks 2026"                                  ││
│  │  Mode: deep (recursive confidence)                                  ││
│  │                                                                     ││
│  │  Progress: ████████████░░░░░░░░░░░░░ Turn 3/5 @ 72% confidence     ││
│  │                                                                     ││
│  │  ┌─ Current Turn ─────────────────────────────────────────────────┐││
│  │  │  🔄 Searching: "langchain vs crewai comparison 2026"           │││
│  │  │  ⏱  Duration: 12.3s                                            │││
│  │  │  💰 Cost: $0.0234 (session: $0.0891)                           │││
│  │  └────────────────────────────────────────────────────────────────┘││
│  │                                                                     ││
│  │  ┌─ Sources (14 found) ───────────────────────────────────────────┐││
│  │  │  ✓ arxiv.org/2026/agents-survey        relevance: 0.94         │││
│  │  │  ✓ langchain.dev/docs/agents           relevance: 0.91         │││
│  │  │  ✓ github.com/crewai/examples          relevance: 0.88         │││
│  │  │  ↓ 11 more...                                                  │││
│  │  └────────────────────────────────────────────────────────────────┘││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                          │
│  ┌─ Recent Sessions ───────────────────────────────────────────────────┐│
│  │  [1] 20260203-2300_kubernetes-scaling        ✓ completed  $0.12    ││
│  │  [2] 20260203-2215_react-patterns            ✓ completed  $0.08    ││
│  │  [3] 20260203-2100_auth-best-practices       ⏸ paused     $0.04    ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│  [N]ew search  [R]esume  [E]xport  [C]ancel                   Cost: $0.24│
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Wireframe: Headless Mode Output

```
research-tui run --headless --epic beads-xxx

[2026-02-04T01:15:32Z] SESSION: 20260204-0115_ai-agent-frameworks
[2026-02-04T01:15:32Z] MODE: deep (confidence threshold: 0.85)
[2026-02-04T01:15:33Z] TURN 1/5: "AI agent frameworks 2026"
[2026-02-04T01:15:38Z]   └─ sources: 8, confidence: 0.45, cost: $0.0123
[2026-02-04T01:15:39Z] TURN 2/5: "langchain autogen crewai comparison"
[2026-02-04T01:15:45Z]   └─ sources: 12, confidence: 0.68, cost: $0.0156
[2026-02-04T01:15:46Z] TURN 3/5: "production agent deployment patterns"
[2026-02-04T01:15:52Z]   └─ sources: 14, confidence: 0.87, cost: $0.0189
[2026-02-04T01:15:52Z] COMPLETE: confidence 0.87 >= threshold 0.85
[2026-02-04T01:15:52Z] TOTAL: 3 turns, 34 sources, $0.0468
[2026-02-04T01:15:52Z] OUTPUT: ~/.config/LEV/research/sessions/2026-02-04/20260204-0115_ai-agent-frameworks/

{"session_id":"20260204-0115_ai-agent-frameworks","status":"complete","turns":3,"sources":34,"cost":0.0468,"confidence":0.87}
```

---

## Component Intents

```yaml
components:
  - name: ProgressBar
    role: Show turn progress and confidence level
    intent: Visual indication of recursive research progress
    inputs:
      - name: currentTurn
        type: number
      - name: maxTurns
        type: number
      - name: confidence
        type: number (0-1)
    outputs:
      - event: onComplete
    update_frequency: realtime

  - name: SourceStream
    role: Display sources as they're discovered
    intent: Real-time source validation
    inputs:
      - name: sources
        type: Source[]
    outputs:
      - event: onSourceClick
      - event: onSourceExclude
    update_frequency: realtime

  - name: CostTracker
    role: Show cumulative cost with budget warnings
    intent: Cost awareness and budget control
    inputs:
      - name: operations
        type: Operation[]
      - name: budget
        type: number (optional)
    outputs:
      - event: onBudgetExceeded
    update_frequency: realtime

  - name: SessionList
    role: Show recent and active sessions
    intent: Quick access to session history
    inputs:
      - name: sessions
        type: Session[]
    outputs:
      - event: onSessionSelect
      - event: onSessionResume
    update_frequency: user_driven

  - name: OperationLog
    role: Scrollable log of operations (headless primary)
    intent: Audit trail and debugging
    inputs:
      - name: operations
        type: Operation[]
    outputs:
      - event: onLogExport
    update_frequency: realtime
```

---

## Interaction States

```json
{
  "screens": [
    {
      "name": "Dashboard",
      "states": ["idle", "active_session", "loading"],
      "transitions": [
        {"from": "idle", "to": "active_session", "trigger": "session_started"},
        {"from": "active_session", "to": "idle", "trigger": "session_complete"},
        {"from": "*", "to": "loading", "trigger": "data_loading"}
      ]
    },
    {
      "name": "SessionView",
      "states": ["searching", "extracting", "synthesizing", "complete", "error", "paused"],
      "transitions": [
        {"from": "searching", "to": "extracting", "trigger": "search_complete"},
        {"from": "extracting", "to": "synthesizing", "trigger": "extraction_complete"},
        {"from": "synthesizing", "to": "complete", "trigger": "synthesis_complete"},
        {"from": "*", "to": "paused", "trigger": "user_pause"},
        {"from": "*", "to": "error", "trigger": "operation_failed"}
      ]
    }
  ]
}
```

---

## Technology Recommendations

### Framework: Ink (React for CLI)
- **Why:** React component model, familiar patterns, good ecosystem
- **Alternative:** Blessed (lower level, more control)

### Key Libraries
```json
{
  "ink": "^4.0.0",
  "ink-spinner": "^5.0.0",
  "ink-progress-bar": "^3.0.0",
  "ink-table": "^3.0.0",
  "ink-text-input": "^5.0.0",
  "zustand": "^4.0.0"
}
```

### File Structure
```
research-tui/
├── src/
│   ├── app.tsx              # Main Ink app
│   ├── components/
│   │   ├── Dashboard.tsx
│   │   ├── ProgressBar.tsx
│   │   ├── SourceStream.tsx
│   │   ├── CostTracker.tsx
│   │   └── SessionList.tsx
│   ├── hooks/
│   │   ├── useSession.ts
│   │   ├── useResearch.ts
│   │   └── useKeyboard.ts
│   ├── store/
│   │   └── research.ts      # Zustand store
│   └── headless/
│       └── runner.ts        # Headless mode
├── package.json
└── tsconfig.json
```

---

## Comparison to Current

| Aspect | Current (CLI) | Proposed (TUI) | Delta |
|--------|---------------|----------------|-------|
| Progress visibility | Spinners only | Full dashboard | +++ |
| Cost tracking | Post-hoc | Real-time | ++ |
| Source discovery | End of run | Streaming | ++ |
| Session management | Manual | Integrated | + |
| Headless/CI | Partial | First-class | + |
| Learning curve | Low | Low (same CLI) | = |

---

## Implementation Phases

### Phase 1: Core TUI (2-3 hours)
- Dashboard layout with Ink
- Progress bar component
- Session list view
- Keyboard navigation

### Phase 2: Research Integration (2-3 hours)
- Hook into valyu research events
- Source streaming
- Cost tracking
- State machine integration

### Phase 3: Headless Mode (1-2 hours)
- JSON output mode
- Log formatting
- Exit codes
- CI integration

### Phase 4: Polish (1-2 hours)
- Error handling
- Session persistence
- Settings panel
- Documentation

---

## CLI Interface

```bash
# Interactive TUI (default)
research-tui

# Start with query
research-tui "AI agent frameworks"

# Headless mode
research-tui --headless "query" --mode=deep --output=json

# Resume session
research-tui resume <session-id>

# Export session
research-tui export <session-id> --format=md|json

# Status (for scripts)
research-tui status --json
```

---

*Generated by /ux auto mode | 2026-02-04*
