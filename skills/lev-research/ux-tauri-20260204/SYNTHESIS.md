# UX Discovery: Research Hub (Tauri Desktop App) v1.0

## Problem Statement

**When** running multi-step research operations, **users** cannot visualize progress, costs, confidence levels, or source discovery in real-time. Current CLI-only experience loses situational awareness during long-running operations.

**Pivot from TUI:** Terminal UIs are limited to developers. A cross-platform desktop app expands reach to non-technical users and provides richer visualization capabilities.

**Success Criteria:**
- Real-time visualization of research progress
- Cross-platform: macOS, Windows, Linux
- Cost tracking per operation with budget alerts
- Confidence level gauges (recursive research)
- Source discovery stream with relevance scores
- Session persistence across app restarts
- Offline mode with local cache

**Constraints:**
- Tauri 2.0 (Rust backend, web frontend)
- Bundle size < 25MB
- Memory < 100MB idle
- Native system tray integration
- Must integrate with existing research CLIs

---

## Jobs to Be Done (Top 3)

### Job 1: Progress Monitoring
> "When I run a deep research query, I want to see which turn I'm on and how confidence is building, so I can decide whether to let it continue or intervene."

**Triggers:** Deep search, valyu research, team spawns
**User Types:** Power users (INTJ), Operators (ISTJ)

### Job 2: Cost Awareness
> "When running multiple searches, I want to see cumulative cost in real-time, so I can stop before exceeding my budget."

**Triggers:** Any paid API call (valyu, firecrawl, brave)
**User Types:** Budget-conscious (ISTJ), Teams (ENTJ)

### Job 3: Research Library
> "When I complete research, I want it saved and searchable, so I can reference findings later without re-running queries."

**Triggers:** Search completion, manual save
**User Types:** Researchers (INTP), Knowledge workers (INFJ)

---

## Information Architecture

### Entities
| Entity | Attributes | Actions |
|--------|------------|---------|
| **Session** | id, query, status, created_at, cost, confidence | create, resume, pause, export, delete |
| **Turn** | number, query, confidence, sources_count, cost, duration | - |
| **Source** | url, title, type, relevance, snippet, cached | view, exclude, bookmark |
| **Budget** | daily_limit, monthly_limit, current_spend, alerts | set, reset |

### Navigation
```
Research Hub
├── Dashboard (default)
│   ├── Quick Search Bar
│   ├── Active Sessions
│   └── Cost Summary
├── Sessions
│   ├── Session List
│   ├── Session Detail
│   └── Export/Import
├── Library
│   ├── Saved Research
│   ├── Bookmarked Sources
│   └── Search History
└── Settings
    ├── API Keys
    ├── Budget Limits
    └── Preferences
```

---

## Task Graph (FSM)

```
┌─────────────────────────────────────────────────────────────┐
│                    RESEARCH HUB FSM                          │
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
- `IDLE`: Waiting for input, showing dashboard
- `SEARCHING`: Running search operations (brave, firecrawl, valyu)
- `EXTRACTING`: Scraping/crawling content
- `SYNTHESIZING`: AI synthesis (valyu answer/research, oracle)
- `COMPLETE`: Results ready, showing summary
- `PAUSED`: User intervention requested
- `ERROR`: Recoverable error state

---

## Wireframes

### Main Dashboard
```
┌─────────────────────────────────────────────────────────────────────────┐
│  🔍 Research Hub                                    [─] [□] [×]         │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  🔎  Search anything...                              [⚡ Deep]    │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌─ Active Sessions ─────────────────────────────────────────────────┐  │
│  │                                                                    │  │
│  │  ┌──────────────────────────────────────────────────────────────┐ │  │
│  │  │  🔄 "AI agent frameworks 2026"              Turn 3/5 @ 72%   │ │  │
│  │  │     ████████████░░░░░░░░░  Sources: 14  Cost: $0.089         │ │  │
│  │  └──────────────────────────────────────────────────────────────┘ │  │
│  │                                                                    │  │
│  │  ┌──────────────────────────────────────────────────────────────┐ │  │
│  │  │  ⏸️ "kubernetes scaling patterns"           Paused @ 85%     │ │  │
│  │  │     █████████████████░░░  Sources: 23  Cost: $0.142          │ │  │
│  │  └──────────────────────────────────────────────────────────────┘ │  │
│  │                                                                    │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌─ Today's Summary ──────────────────────────────────────────────────┐ │
│  │   Searches: 12   │   Sources: 156   │   Cost: $0.48 / $5.00       │ │
│  │   ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  10% of budget     │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  [📊 Dashboard]  [📚 Sessions]  [📖 Library]  [⚙️ Settings]            │
└─────────────────────────────────────────────────────────────────────────┘
```

### Session Detail View
```
┌─────────────────────────────────────────────────────────────────────────┐
│  ← Back   "AI agent frameworks 2026"                   [⏸️] [📤] [🗑️]  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Status: 🔄 Searching          Confidence: ████████░░ 72%              │
│  Turn: 3 of 5                  Cost: $0.089                            │
│  Duration: 47s                 Sources: 14 found                       │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─ Live Progress ───────────────────────────────────────────────────┐  │
│  │  Turn 1: "AI agent frameworks" → 8 sources, 45% conf              │  │
│  │  Turn 2: "langchain vs crewai 2026" → 11 sources, 62% conf        │  │
│  │  Turn 3: "autogen multi-agent patterns" → 14 sources, 72% conf    │  │
│  │  ⏳ Processing...                                                  │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌─ Sources (14) ────────────────────────────────────────────────────┐  │
│  │  ✓ arxiv.org/2026/agents-survey           relevance: 0.94  [📖]  │  │
│  │  ✓ langchain.dev/docs/agents              relevance: 0.91  [📖]  │  │
│  │  ✓ github.com/crewai/examples             relevance: 0.88  [📖]  │  │
│  │  ✓ microsoft.com/autogen/patterns         relevance: 0.85  [📖]  │  │
│  │  ... 10 more                                                      │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  [⏹️ Stop]  [⏸️ Pause]  [📋 Copy]  [💾 Save to Library]                │
└─────────────────────────────────────────────────────────────────────────┘
```

### System Tray (Collapsed)
```
┌──────────────────────────────┐
│  🔍 Research Hub             │
├──────────────────────────────┤
│  ● 2 active searches         │
│  ○ Cost today: $0.48         │
├──────────────────────────────┤
│  [Quick Search...]           │
│  [Open Dashboard]            │
│  [Pause All]                 │
├──────────────────────────────┤
│  [Quit]                      │
└──────────────────────────────┘
```

---

## Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Framework** | Tauri 2.0 | Cross-platform, small bundles (~15MB), Rust backend |
| **Frontend** | SolidJS + TailwindCSS | Best performance for real-time updates |
| **State** | XState | Robust FSM, visualization tools |
| **IPC** | Tauri Commands | Type-safe Rust ↔ JS bridge |
| **Storage** | SQLite (sqlx) | Local sessions, offline support |
| **Charts** | Apache ECharts | High-performance time series |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Research Hub (Tauri)                     │
├─────────────────────────────────────────────────────────────┤
│  Frontend (SolidJS)                                         │
│  ├── DashboardView       ← Session list, quick search       │
│  ├── SessionView         ← Progress, sources, cost panels   │
│  ├── LibraryView         ← Saved research, bookmarks        │
│  └── SettingsView        ← API status, preferences          │
├─────────────────────────────────────────────────────────────┤
│  State Machine (XState)                                     │
│  ├── States: idle → searching → extracting → synthesizing   │
│  ├── Events: START, SOURCE_FOUND, TURN_COMPLETE, ERROR      │
│  └── Context: session, turns[], sources[], cost             │
├─────────────────────────────────────────────────────────────┤
│  Rust Backend (Tauri Commands)                              │
│  ├── search::start()     ← Spawn research process           │
│  ├── search::pause()     ← Pause/resume control             │
│  ├── session::list()     ← Get all sessions                 │
│  ├── session::export()   ← Export to JSON/MD                │
│  └── budget::check()     ← Cost tracking                    │
├─────────────────────────────────────────────────────────────┤
│  Backend Adapters (Process spawning)                        │
│  ├── ValyuAdapter        ← valyu research/answer CLI        │
│  ├── FirecrawlAdapter    ← firecrawl scrape/extract         │
│  └── BraveAdapter        ← brave-search CLI                 │
├─────────────────────────────────────────────────────────────┤
│  Storage (SQLite via sqlx)                                  │
│  └── sessions, sources, budgets, settings                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Core Shell
- Tauri 2.0 project setup
- SolidJS + Vite frontend
- Basic window + system tray
- Dashboard skeleton

### Phase 2: Search Integration
- Rust backend adapters for CLIs
- IPC commands for search control
- Real-time progress events
- Session persistence (SQLite)

### Phase 3: Visualization
- Live progress charts
- Source list with relevance
- Cost tracking gauges
- Budget alerts

### Phase 4: Polish
- Library/bookmarks
- Export (JSON, MD, PDF)
- Keyboard shortcuts
- Settings sync

---

## BD Task Structure

```
research-hub [epic] Tauri Research Hub Desktop App
├── research-hub-1 [P1] Phase 1: Core Shell (Tauri + SolidJS)
├── research-hub-2 [P1] Phase 2: Search Integration ← blocked by 1
├── research-hub-3 [P2] Phase 3: Visualization ← blocked by 2
└── research-hub-4 [P2] Phase 4: Polish ← blocked by 3
```

---

## Comparison: TUI vs Desktop

| Aspect | TUI (Ink) | Desktop (Tauri) |
|--------|-----------|-----------------|
| **Bundle Size** | ~5MB (Node) | ~15MB |
| **Platforms** | Terminal only | macOS/Win/Linux |
| **Users** | Developers | Everyone |
| **Visualization** | ASCII charts | Full charts |
| **System Tray** | ❌ | ✅ |
| **Offline** | Limited | Full SQLite |
| **Background** | tmux required | Native |

**Verdict:** Desktop app is better for product, TUI remains useful for SSH/CI.
