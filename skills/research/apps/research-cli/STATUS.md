# Research CLI Scaffold - Build Status

## Current State

Initial scaffold created with FrankenTUI integration. The scaffold includes:

✅ **Completed:**
- Basic project structure (`src/main.rs`, `src/app.rs`, `src/widgets/`, `src/commands/`)
- Custom widgets (ProgressBar, SourceList, CostTracker)
- CLI argument parsing with clap
- FrankenTUI Model/Update/View pattern
- Cargo.toml with ftui dependencies
- README with usage examples

⚠️ **Build Issues Remaining:**

1. **Color API Conversion** - `Style::fg()` expects `PackedRgba`, not `Color`
   - Need to convert `Color` → `PackedRgba` via `color.to_rgb()` → `PackedRgba::from(rgb)`
   - OR use `Rgb::new(r, g, b)` directly

2. **Backend Integration** - User added backends module
   - Missing `src/backends/mod.rs` and implementations
   - Need trait definitions for ResearchBackend
   - Borrow checker issues in `app.rs` with `backend_rx`

3. **Command Module** - User modified command structure
   - Commands moved to separate files (search.rs, status.rs, history.rs)
   - Need to export command structs properly

## Quick Fix for Color Issues

Replace all `Color::Ansi16(Ansi16::Xyz)` with direct RGB:

```rust
use ftui_render::cell::PackedRgba;

// Green
Style::new().fg(PackedRgba::rgb(0, 255, 0))

// Cyan
Style::new().fg(PackedRgba::rgb(0, 255, 255))

// Yellow
Style::new().fg(PackedRgba::rgb(255, 255, 0))

// Red
Style::new().fg(PackedRgba::rgb(255, 0, 0))

// Gray (BrightBlack approximation)
Style::new().fg(PackedRgba::rgb(128, 128, 128))
```

## Next Steps

1. Fix widget Color → PackedRgba conversions
2. Create backends module with trait
3. Fix borrow checker issue in app.rs
4. Verify `cargo check` passes

## Files Created

```
~/.agents/skills/lev-research/apps/research-cli/
├── Cargo.toml
├── README.md
├── FIXES.md
├── STATUS.md (this file)
└── src/
    ├── main.rs
    ├── app.rs
    ├── commands/
    │   ├── mod.rs
    │   ├── search.rs
    │   ├── status.rs
    │   └── history.rs
    └── widgets/
        ├── mod.rs
        ├── progress_bar.rs
        ├── source_list.rs
        └── cost_tracker.rs
```

## Build Command

```bash
cd ~/.agents/skills/lev-research/apps/research-cli
cargo check
```

## Expected Result

After fixes, should compile with 0 errors (warnings OK for unused code).
