# Research CLI (research-cli)

FrankenTUI-based CLI interface for the OCLaw Research Hub.

## Overview

`research-cli` provides both inline and fullscreen terminal UIs for research tasks using the FrankenTUI framework.

## Features

- **Inline Mode**: Compact 20-row display that doesn't take over your terminal
- **Fullscreen Mode**: Full-screen TUI with more detail
- **Real-time Progress**: Live progress bars, source counts, and cost tracking
- **State Machine**: `idle → searching → extracting → complete`
- **Custom Widgets**: Progress bar, source list, cost tracker

## Architecture

```
research-cli/
├── src/
│   ├── main.rs           # CLI entry point (clap)
│   ├── app.rs            # ResearchApp (Model/Update/View)
│   ├── commands/         # Subcommands
│   │   ├── search.rs     # Execute search
│   │   ├── status.rs     # Show status
│   │   └── history.rs    # Show history
│   └── widgets/          # Custom FrankenTUI widgets
│       ├── progress_bar.rs
│       ├── source_list.rs
│       └── cost_tracker.rs
└── Cargo.toml            # Dependencies (ftui-*, clap, tokio)
```

## Usage

### Search (inline mode)
```bash
cargo run --bin research -- search "rust async programming"
```

### Search (fullscreen mode)
```bash
cargo run --bin research -- --fullscreen search "machine learning fundamentals"
```

### Status
```bash
cargo run --bin research -- status
cargo run --bin research -- status --session-id abc123
```

### History
```bash
cargo run --bin research -- history
cargo run --bin research -- history --limit 20 --filter "rust"
```

## Controls

- **SPACE**: Pause/Resume
- **Q**: Quit
- **PageUp/PageDown**: Scroll log viewer
- **Ctrl+C**: Force quit

## State Machine

1. **Idle**: Initial state
2. **Searching**: Discovering sources (0-40% progress)
3. **Extracting**: Analyzing sources (40-100% progress)
4. **Complete**: Research finished
5. **Error**: Something went wrong

## FrankenTUI Integration

### Harness Pattern

The app follows the `ftui-harness` pattern:

```rust
impl Model for ResearchApp {
    type Message = Msg;

    fn init(&mut self) -> Cmd<Self::Message>;
    fn update(&mut self, msg: Msg) -> Cmd<Self::Message>;
    fn view(&self, frame: &mut Frame);
    fn subscriptions(&self) -> Vec<Box<dyn Subscription<Self::Message>>>;
}
```

### Custom Widgets

All widgets implement `ftui_widgets::Widget`:

```rust
impl Widget for ProgressBar {
    fn render(self, area: Rect, frame: &mut Frame) {
        // Render logic
    }
}
```

## Dependencies

### FrankenTUI (path deps for now)
- `ftui-core` - Events, geometry
- `ftui-render` - Frame, buffer
- `ftui-runtime` - App, Model, Cmd
- `ftui-widgets` - Block, LogViewer, StatusLine
- `ftui-style` - Colors, styles
- `ftui-layout` - Flex layouts
- `ftui-extras` - Charts, timers, themes

### Other
- `clap` - CLI parsing
- `tokio` - Async runtime
- `reqwest` - HTTP client (future use)
- `serde/serde_json` - Serialization
- `anyhow/thiserror` - Error handling
- `tracing` - Logging

## Building

```bash
# Check syntax
cargo check

# Build
cargo build

# Run
cargo run --bin research -- search "test query"

# Build release
cargo build --release
```

## Next Steps

1. Connect to actual research backend API
2. Implement session persistence (SQLite?)
3. Add more widgets (confidence meter, citation tree)
4. Add chart visualization for cost trends
5. Implement proper history tracking
6. Add export to markdown/JSON

## References

- FrankenTUI: `/tmp/frankentui/`
- Harness examples: `/tmp/frankentui/crates/ftui-harness/examples/`
- Widget showcase: `/tmp/frankentui/crates/ftui-demo-showcase/`
