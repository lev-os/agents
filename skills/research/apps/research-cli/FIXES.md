# API Fixes for FrankenTUI Integration

## Issues Found

1. `Rect` uses fields, not methods (`area.width` not `area.width()`)
2. `Color` enum uses `Ansi16` variant (e.g., `Color::Ansi16(Ansi16::BrightBlack)`)
3. Missing backend integration (simulated progress in app.rs)
4. Missing proper error types for widgets

## Fixes Applied

### Rect API
- Changed: `area.width()` → `area.width`
- Changed: `area.height()` → `area.height`
- Changed: `area.x()` → `area.x`
- Changed: `area.y()` → `area.y`

### Color API
- Changed: `Color::DarkGray` → `Color::Ansi16(Ansi16::BrightBlack)`
- Changed: `Color::Green` → `Color::Ansi16(Ansi16::Green)`
- Changed: `Color::Yellow` → `Color::Ansi16(Ansi16::Yellow)`
- Changed: `Color::Red` → `Color::Ansi16(Ansi16::Red)`
- Changed: `Color::Cyan` → `Color::Ansi16(Ansi16::Cyan)`

## Build Status

After fixes: `cargo check` should pass with 0 errors, possible warnings OK.
