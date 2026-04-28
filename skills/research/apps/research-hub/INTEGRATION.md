# Research Hub - Tauri Backend Integration

## Overview

The Research Hub Tauri app is now fully wired to a real Rust backend with CLI integrations and event streaming. Mock data has been removed from the Dashboard.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (SolidJS)                      │
│                                                             │
│  Dashboard.tsx ──► services/tauri.ts ──► Tauri IPC        │
│       │                                                     │
│       └──► Event Listeners (research:progress, etc.)       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Rust Backend (Tauri)                     │
│                                                             │
│  commands.rs ──► research.rs ──► CLI Wrappers              │
│       │                              │                      │
│       └──────► Event Emitter ────────┘                      │
│                (research:progress,                          │
│                 research:source_found,                      │
│                 research:complete)                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      CLI Tools (Shell)                      │
│                                                             │
│  • valyu search "<query>"                                   │
│  • firecrawl scrape <url>                                   │
│  • brave-search "<query>"                                   │
└─────────────────────────────────────────────────────────────┘
```

## Backend Implementation

### Rust Modules

1. **`src-tauri/src/research.rs`**
   - Core types: `Source`, `Turn`, `Session`
   - Session state management
   - CLI wrapper functions for Valyu, Firecrawl, Brave
   - Mock search fallback for testing

2. **`src-tauri/src/commands.rs`**
   - Tauri commands: `search_start`, `search_pause`, `search_resume`, `session_list`, `session_get`
   - Background research task runner
   - Event emission: `research:progress`, `research:source_found`, `research:complete`

3. **`src-tauri/src/lib.rs`**
   - Module registration
   - Session store initialization
   - Command handler registration

### Frontend Integration

1. **`src/services/tauri.ts`**
   - Type-safe Tauri command wrappers
   - Event listener helpers
   - TypeScript interfaces matching Rust backend

2. **`src/components/Dashboard.tsx`**
   - Real-time event listeners via `onMount`
   - Async search submission via `searchStart()`
   - Pause/resume controls via `searchPause()` / `searchResume()`
   - Session loading from backend on startup

## Event Flow

### Starting a Search

```
User submits form
    │
    ▼
Dashboard.tsx calls tauri.searchStart(query, mode)
    │
    ▼
Rust: commands::search_start creates Session
    │
    ▼
Spawns background task: run_research_task()
    │
    ▼
Loop through turns (2 for quick, 5 for deep):
    │
    ├─► Run CLI search (valyu, brave, firecrawl)
    ├─► Emit "research:source_found" per source
    ├─► Complete turn
    ├─► Emit "research:progress" with turn stats
    └─► Repeat
    │
    ▼
Emit "research:complete" when done
```

### Dashboard Updates

```
research:progress event
    │
    ▼
Frontend listener updates ActiveSession state
    │
    ▼
SolidJS reactivity updates UI (progress bars, stats)
```

## Testing

### Mock Mode (Default)

Currently uses `run_mock_search()` which simulates:
- 500ms delay per search
- Returns 2 sample sources per turn
- Incremental confidence/cost/duration

**To test:**
```bash
cd apps/research-hub
pnpm tauri dev
```

1. Enter a search query
2. Click "Search"
3. Watch progress bars update in real-time
4. Test pause/resume buttons
5. Verify sources count increments

### Real CLI Mode

Replace mock search with real CLIs in `commands.rs`:

```rust
// In run_research_task(), replace:
let sources = run_mock_search(&query, &mode).await?;

// With:
let valyu_results = run_valyu_search(&query).await?;
let brave_results = run_brave_search(&query).await?;
// Parse and combine results
```

**Prerequisites:**
```bash
# Install CLIs
npm install -g @valyu/cli
npm install -g firecrawl-cli
brew install brave-cli  # or equivalent
```

## Commands

### Tauri Commands

| Command | Parameters | Returns | Description |
|---------|-----------|---------|-------------|
| `search_start` | `query: String, mode: String` | `String` (session ID) | Start new research session |
| `search_pause` | `sessionId: String` | `()` | Pause active session |
| `search_resume` | `sessionId: String` | `()` | Resume paused session |
| `session_list` | - | `Vec<Session>` | Get all sessions |
| `session_get` | `sessionId: String` | `Session` | Get session by ID |

### Events

| Event | Payload | Description |
|-------|---------|-------------|
| `research:progress` | `ProgressPayload` | Turn completed, stats updated |
| `research:source_found` | `SourcePayload` | New source discovered |
| `research:complete` | `ResultPayload` | Research session finished |

## Next Steps

### XState Integration

To wire the XState machine (`src/machines/researchMachine.ts`):

1. Create an actor from the machine in Dashboard.tsx
2. Subscribe to Tauri events and send XState events:
   - `research:progress` → `send({ type: 'TURN_COMPLETE', ... })`
   - `research:source_found` → `send({ type: 'SOURCE_FOUND', ... })`
   - `research:complete` → `send({ type: 'COMPLETE' })`
3. Use XState state to drive UI instead of direct signals

### Real CLI Integration

1. Install CLI tools (Valyu, Firecrawl, Brave)
2. Update `commands.rs` to use real CLI wrappers
3. Add JSON parsing for CLI output
4. Implement error handling for CLI failures

### Persistence

Add session persistence to Rust backend:
- Use `serde` to serialize sessions to JSON
- Store in app data directory via `tauri::api::path::app_data_dir()`
- Load on startup, save on changes

## Troubleshooting

**Build errors:**
```bash
cd src-tauri
cargo clean
cargo build
```

**Frontend doesn't connect:**
- Check Tauri dev server is running
- Verify commands are registered in `lib.rs`
- Check browser console for errors

**Events not firing:**
- Verify listeners are set up in `onMount`
- Check Rust code emits events via `app.emit()`
- Ensure event names match exactly

## File Locations

```
apps/research-hub/
├── src/
│   ├── components/
│   │   └── Dashboard.tsx          ← UI with real backend calls
│   ├── services/
│   │   └── tauri.ts               ← Tauri IPC wrapper
│   └── machines/
│       └── researchMachine.ts     ← XState (not yet wired)
├── src-tauri/
│   ├── src/
│   │   ├── lib.rs                 ← App entry + command registration
│   │   ├── commands.rs            ← Tauri commands + background tasks
│   │   └── research.rs            ← Core types + CLI wrappers
│   └── Cargo.toml                 ← Dependencies
└── INTEGRATION.md                 ← This file
```

## Status

- ✅ Rust backend with commands
- ✅ Event streaming (progress, source, complete)
- ✅ CLI wrappers (mock mode active)
- ✅ Frontend integration
- ✅ Pause/resume controls
- ⏳ XState machine integration (types ready, not wired)
- ⏳ Real CLI calls (infrastructure ready, needs implementation)
- ⏳ Session persistence
