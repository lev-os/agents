---
name: frankentui
description: >-
  Build showcase-grade FrankenTUI screens. Use when working in ftui-demo-showcase,
  diagnosing TUI issues with doctor_frankentui, polishing TUI UX, or replacing
  placeholder interfaces.
---

# frankentui

## Table of Contents

- Mandatory First Pass
- Non-Negotiable Showcase Contract (Global Shell, Color, Search, Markdown, Panes, Forms, Space, Drag, i18n, Diagnostics, Responsive, Text Editing, Config, Hyperlinks)
- Cross-Cutting Design Patterns
- doctor_frankentui Diagnostic Workflow (Visual-First)
- Quick Router | Workflow | Quality Gates | Cass Mining | Anti-Slop Rule | References

Skill for architecture-accurate, showcase-level work in FrankenTUI, especially
`ftui-demo-showcase`.

## Mandatory First Pass

- Read `AGENTS.md` fully.
- Read `README.md` fully.
- Run cass archaeology before major polish work:
  - `cass status --json && cass index --json`
  - `cass search "under construction placeholder" --workspace /data/projects/frankentui --json --fields minimal --limit 20`
  - `cass search "mind-blowing dashboard" --workspace /data/projects/frankentui --json --fields minimal --limit 20`
  - `cass search "improve TUI" --workspace /data/projects/frankentui --json --fields minimal --limit 20`
- Verify runtime architecture contracts before editing:
  - `crates/ftui-core/src/terminal_session.rs`
  - `crates/ftui-runtime/src/program.rs`
  - `crates/ftui-runtime/src/terminal_writer.rs`
  - `crates/ftui-render/src/{frame.rs,buffer.rs,diff.rs,presenter.rs}`

## Non-Negotiable Showcase Contract

If the task is "make this screen good" or "upgrade weak TUI UI", treat these as
default requirements.

Important: this contract is capability-gated.
- Global shell + discoverability + resize resilience are always required.
- Feature-specific contracts (search, markdown streaming, adjustable panes, forms)
  are required only when that capability is part of the screen.

### Global Shell Invariants (Always)

- `Ctrl+T` cycles theme globally and must remain reachable:
  - app key handler: `crates/ftui-demo-showcase/src/app.rs:3805`
  - palette command: `crates/ftui-demo-showcase/src/app.rs:3043`
  - palette dispatch: `crates/ftui-demo-showcase/src/app.rs:4870`
- Tab strip is not optional chrome. It is screen navigation + visual identity:
  - tab rendering + hit regions: `crates/ftui-demo-showcase/src/chrome.rs:330`
  - per-screen accent backgrounds in active tabs: `crates/ftui-demo-showcase/src/chrome.rs:362`
  - accent map for every screen: `crates/ftui-demo-showcase/src/chrome.rs:1298`
  - accent token source: `crates/ftui-demo-showcase/src/theme.rs:260`
- Bottom status bar must communicate navigation and state:
  - status bar renderer: `crates/ftui-demo-showcase/src/chrome.rs:595`
  - tab navigation hint text: `crates/ftui-demo-showcase/src/chrome.rs:726`
  - clickable state toggles and hit regions: `crates/ftui-demo-showcase/src/chrome.rs:636`
- Help overlay must merge global and screen-specific keybindings:
  - keybinding hint builder: `crates/ftui-demo-showcase/src/chrome.rs:1109`
  - help modal renderer: `crates/ftui-demo-showcase/src/chrome.rs:1176`
  - current screen binding handoff: `crates/ftui-demo-showcase/src/app.rs:4058`

### Color Harmony Invariants (Always)

- Prefer curated theme tokens over ad-hoc color choices.
  - screen accent palette: `crates/ftui-demo-showcase/src/theme.rs:260`
- Explicitly support standard demo theme rotation via `Ctrl+T`:
  - `Cyberpunk Aurora`
  - `Darcula`
  - `Lumen Light`
  - `Nordic Frost`
  - plus accessibility `High Contrast` support
  - canonical theme enum + names: `crates/ftui-extras/src/theme.rs:26`
  - standard theme set (non-accessibility): `crates/ftui-extras/src/theme.rs:49`
  - app default theme starts at Cyberpunk Aurora: `crates/ftui-demo-showcase/src/app.rs:2652`
- Use neutral tones for large surfaces/chrome, and reserve higher-chroma accents for focus/highlights.
  - tab bar neutral base: `crates/ftui-demo-showcase/src/theme.rs:723`
  - status bar neutral base: `crates/ftui-demo-showcase/src/theme.rs:736`
  - focused panel accent rule: `crates/ftui-demo-showcase/src/theme.rs:779`
- Keep semantic color mappings intentional (status, priority, screen accents).
  - semantic style system: `crates/ftui-demo-showcase/src/theme.rs:32`
- Respect contrast discipline already encoded in theme tests.
  - WCAG contrast test suite: `crates/ftui-demo-showcase/src/theme.rs:1309`
  - screen accent contrast validation: `crates/ftui-demo-showcase/src/theme.rs:1459`

### Search Excellence Invariants (When Search Exists)

- Search-as-you-type (not submit-only).
- Clear focus entry and exit (`/` or `Ctrl+F`, `Esc`).
- Fast match navigation (`Enter`/`Tab`/arrows and `n/N` style repeat).
- Match count visibility (`current/total`) in search bar and/or status bar.
- Strong visual hierarchy for matches:
  - list-level marker/gutter style,
  - line-level highlight,
  - active-match emphasis stronger than passive matches.
- Contextual affordances around results:
  - match radar/density sparkline,
  - nearest context snippet,
  - summary panel.

Reference implementations:
- Shakespeare: `crates/ftui-demo-showcase/src/screens/shakespeare.rs`
- SQLite Code Explorer: `crates/ftui-demo-showcase/src/screens/code_explorer.rs`
- Log Search: `crates/ftui-demo-showcase/src/screens/log_search.rs`
- Virtualized Search: `crates/ftui-demo-showcase/src/screens/virtualized_search.rs`
- Markdown Live Editor: `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs`

### Streaming Markdown Invariants (When Markdown/LLM Output Exists)

- Use full GFM-style rendering (tables, task lists, admonitions, math, syntax-highlighted code).
  - themed markdown + GFM extensions: `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:578`
- Support true incremental rendering for streaming output (not full re-render only at completion).
  - stream fragment renderer: `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:676`
  - streaming renderer call: `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:686`
- Show explicit stream status and progress.
  - streaming panel status + progress: `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:905`
  - mini progress bar: `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:952`
- Provide direct controls for stream lifecycle.
  - play/pause + turbo + restart keys: `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:1101`
  - focus-aware scroll controls: `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:1053`

### Dynamic Pane Invariants (When Multi-Panel Layout Exists)

- Model pane geometry explicitly and map pointer position to active/focused pane.
  - panel hit mapping: `crates/ftui-demo-showcase/src/screens/dashboard.rs:3414`
- Render visible splitter handles and support drag-to-resize with clamped bounds.
  - splitter drag update: `crates/ftui-demo-showcase/src/screens/dashboard.rs:3452`
  - splitter handle renderer: `crates/ftui-demo-showcase/src/screens/dashboard.rs:5620`
- Keep drag state robust (cancel/clear on mouse-up and keyboard interaction).
  - drag lifecycle in update: `crates/ftui-demo-showcase/src/screens/dashboard.rs:6006`
  - keyboard clears drag latch: `crates/ftui-demo-showcase/src/screens/dashboard.rs:6099`
- Register pane hit regions so mouse navigation and deep links stay reliable.
  - pane hit registration: `crates/ftui-demo-showcase/src/screens/dashboard.rs:5597`

### Multi-Section Visual Delineation Invariants (When Screen Has Many Sections)

- Major sections should be visually boxed with rounded borders.
  - dashboard panels use rounded borders: `crates/ftui-demo-showcase/src/screens/dashboard.rs:3847`
  - forms panels use rounded borders: `crates/ftui-demo-showcase/src/screens/forms_input.rs:764`
- Section borders/colors should encode semantics (focus/state/domain accents), not random decoration.
  - semantic panel border styling with screen accents: `crates/ftui-demo-showcase/src/screens/dashboard.rs:3852`
  - data-viz panel accent styling by focus: `crates/ftui-demo-showcase/src/screens/data_viz.rs:113`
  - form panel semantic accent/focus: `crates/ftui-demo-showcase/src/screens/forms_input.rs:760`

### Forms Invariants (When Data Entry Exists)

- Support mixed form/input affordances with explicit focus management.
  - panel focus model: `crates/ftui-demo-showcase/src/screens/forms_input.rs:34`
  - left/right panel rendering: `crates/ftui-demo-showcase/src/screens/forms_input.rs:1077`
- Use validation with user-state awareness (dirty/touched vs forced full validation).
  - touched/dirty filtered validation: `crates/ftui-demo-showcase/src/screens/forms_input.rs:430`
  - summary badges (ready/errors/progress): `crates/ftui-demo-showcase/src/screens/forms_input.rs:506`
- Include undo/redo and visible history for confidence while editing.
  - undo/redo stack ops: `crates/ftui-demo-showcase/src/screens/forms_input.rs:693`
  - undo history panel: `crates/ftui-demo-showcase/src/screens/forms_input.rs:721`
- Provide robust validation demo patterns (real-time vs on-submit, error summary, injection).
  - mode toggle + immediate behavior: `crates/ftui-demo-showcase/src/screens/form_validation.rs:342`
  - submit flow + notifications: `crates/ftui-demo-showcase/src/screens/form_validation.rs:309`
  - error summary panel: `crates/ftui-demo-showcase/src/screens/form_validation.rs:361`

### Space-Constrained Resilience Invariants (Always)

- Screens must degrade gracefully and still show meaningful content in tight terminals.
- Use explicit layout tiers with a tiny fallback for constrained sizes.
  - tier switch: `crates/ftui-demo-showcase/src/screens/dashboard.rs:6174`
  - tiny layout fallback: `crates/ftui-demo-showcase/src/screens/dashboard.rs:5813`
- Gate optional subpanels by area so core controls remain visible.
  - forms header/footer gating by height: `crates/ftui-demo-showcase/src/screens/forms_input.rs:779`
  - undo panel suppressed when too small: `crates/ftui-demo-showcase/src/screens/forms_input.rs:722`
- Guard empty areas and keep rendering no-op safe.
  - markdown screen empty-area guard: `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:1128`
  - forms screen empty-area guard: `crates/ftui-demo-showcase/src/screens/forms_input.rs:1077`
- Add tests proving small-size behavior.
  - dashboard threshold tests: `crates/ftui-demo-showcase/src/screens/dashboard.rs:6586`
  - form validation small-size render test: `crates/ftui-demo-showcase/src/screens/form_validation.rs:739`

### Drag-and-Drop Invariants (When Drag-and-Drop Exists)

- Implement three-phase drag state machine: Down (arm) -> Drag (update hover) -> Up (commit or cancel).
  - kanban drag protocol: `crates/ftui-demo-showcase/src/screens/kanban_board.rs:321`
  - drag_drop sortable + cross-container modes: `crates/ftui-demo-showcase/src/screens/drag_drop.rs:358`
- Provide full keyboard accessibility via `KeyboardDragManager` with announcements for screen readers.
  - keyboard drag handler: `crates/ftui-demo-showcase/src/screens/drag_drop.rs:358`
  - drop target info builder: `crates/ftui-demo-showcase/src/screens/drag_drop.rs:446`
- Show visual feedback layers: dimmed ghost for drag source, highlight for drop target, focus indicator for keyboard.
  - drag source dimming: `crates/ftui-demo-showcase/src/screens/kanban_board.rs:476`
  - drop target highlight: `crates/ftui-demo-showcase/src/screens/kanban_board.rs:464`
- Sync keyboard focus and mouse selection to the same item on every interaction.
  - focus sync on click: `crates/ftui-demo-showcase/src/screens/kanban_board.rs:898`
- Include undo/redo for drag operations.
  - drag undo/redo stack: `crates/ftui-demo-showcase/src/screens/kanban_board.rs:668`

Reference implementations:
- Kanban Board: `crates/ftui-demo-showcase/src/screens/kanban_board.rs`
- Drag-Drop Demo: `crates/ftui-demo-showcase/src/screens/drag_drop.rs`

### Accessibility and i18n Invariants (When Internationalized or Keyboard-Heavy)

- Use `display_width()` for layout, `grapheme_count()` for editing positions. Never use `.len()` for display measurement.
  - i18n width metrics: `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:677`
- Handle combining marks, CJK double-width, emoji ZWJ sequences, and flag emojis correctly.
  - grapheme stress tests: `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:100`
- Support RTL flow direction via `Flex::flow_direction()` for Arabic and Hebrew layouts.
  - RTL mirroring: `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:606`
- Use `StringCatalog` with plural forms for multi-locale text (one/few/many/other).
  - plural form system: `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:1064`
- Provide full keyboard navigation as a peer to mouse (Tab/Shift-Tab panel cycling, arrow/vim navigation, Space/Enter activation).
  - mouse playground keyboard nav: `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:1049`
  - drag_drop keyboard drag: `crates/ftui-demo-showcase/src/screens/drag_drop.rs:358`

### Diagnostic and Telemetry Invariants (When Debugging/Inspection Surfaces Exist)

- Use JSONL structured logging with monotonic sequence numbers and FNV-1a checksums for verification.
  - diagnostic entry format: `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:173`
  - determinism export format: `crates/ftui-demo-showcase/src/screens/determinism_lab.rs:579`
- Support environment-variable-driven configuration for log paths and deterministic mode.
  - env var config: `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:52`
- Provide telemetry hooks (callbacks) for external observers without modifying core logic.
  - telemetry hooks: `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:476`
- Enable deterministic replay via seed-driven pseudo-random generation (LCG).
  - deterministic buffer gen: `crates/ftui-demo-showcase/src/screens/determinism_lab.rs:296`
- Display Bayesian evidence (posterior parameters, log Bayes factors, e-values, conformal bounds) when introspecting runtime decisions.
  - evidence cockpit: `crates/ftui-demo-showcase/src/screens/explainability_cockpit.rs:693`
  - VOI overlay: `crates/ftui-demo-showcase/src/screens/voi_overlay.rs:140`

Reference implementations:
- Explainability Cockpit: `crates/ftui-demo-showcase/src/screens/explainability_cockpit.rs`
- VOI Overlay: `crates/ftui-demo-showcase/src/screens/voi_overlay.rs`
- Determinism Lab: `crates/ftui-demo-showcase/src/screens/determinism_lab.rs`
- Mouse Playground: `crates/ftui-demo-showcase/src/screens/mouse_playground.rs`

### Responsive Layout Invariants (When Breakpoint-Driven Layouts Exist)

- Use `ResponsiveLayout` with `Breakpoint` tiers (XS/SM/MD/LG/XL) for structured responsive design.
  - breakpoint-driven layout: `crates/ftui-demo-showcase/src/screens/responsive_demo.rs:134`
- Use `Visibility::visible_above()` to conditionally hide components below their breakpoint tier.
  - visibility gating: `crates/ftui-demo-showcase/src/screens/responsive_demo.rs:289`
- Use `Responsive<T>::resolve(bp)` for per-breakpoint value switching (padding, labels, sizing).
  - responsive values: `crates/ftui-demo-showcase/src/screens/responsive_demo.rs:309`
- For content-aware sizing, compute constraints procedurally at render time with minimum floors.
  - intrinsic sizing with floors: `crates/ftui-demo-showcase/src/screens/intrinsic_sizing.rs:252`
- Use `LayoutDebugger` + `LayoutRecord` + `ConstraintOverlay` to visualize constraint solver behavior during development.
  - layout inspector: `crates/ftui-demo-showcase/src/screens/layout_inspector.rs:273`

Reference implementations:
- Responsive Demo: `crates/ftui-demo-showcase/src/screens/responsive_demo.rs`
- Intrinsic Sizing: `crates/ftui-demo-showcase/src/screens/intrinsic_sizing.rs`
- Layout Inspector: `crates/ftui-demo-showcase/src/screens/layout_inspector.rs`

### Text Editing Invariants (When Text Editor Surfaces Exist)

- Use `TextArea` widget with line numbers, soft wrap, and cursor tracking.
  - text editor setup: `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:1542`
  - markdown editor with soft wrap: `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs:183`
- Implement search/replace with `search_ascii_case_insensitive()` returning byte-range results.
  - search implementation: `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:868`
  - replace implementation: `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:997`
- Convert between byte offsets and line/grapheme positions for cursor jumps.
  - byte-to-cursor conversion: `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs:296`
- Provide undo/redo via `VecDeque<String>` with bounded history (FIFO eviction at limit).
  - undo stack: `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:647`
- For live preview (markdown), re-render only on content change, not every frame.
  - cached preview rendering: `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs:280`

Reference implementations:
- Advanced Text Editor: `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs`
- Markdown Live Editor: `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs`

### Configuration and Persistence Invariants (When User Configuration Exists)

- Use serde `Serialize`/`Deserialize` snapshot types for JSON round-trip import/export.
  - widget builder snapshots: `crates/ftui-demo-showcase/src/screens/widget_builder.rs:134`
  - table theme spec: `crates/ftui-demo-showcase/src/screens/table_theme_gallery.rs:478`
- Provide built-in presets (read-only) plus user-saveable custom presets.
  - preset system: `crates/ftui-demo-showcase/src/screens/widget_builder.rs:226`
  - custom preset saving: `crates/ftui-demo-showcase/src/screens/table_theme_gallery.rs:216`
- Use FNV-1a hashing for regression detection on configuration snapshots.
  - props hash: `crates/ftui-demo-showcase/src/screens/widget_builder.rs:934`
- Validate imported data before applying (spec.validate() pattern).
  - import validation: `crates/ftui-demo-showcase/src/screens/table_theme_gallery.rs:478`

Reference implementations:
- Widget Builder: `crates/ftui-demo-showcase/src/screens/widget_builder.rs`
- Table Theme Gallery: `crates/ftui-demo-showcase/src/screens/table_theme_gallery.rs`

### Hyperlink and Terminal Feature Invariants (When OSC-8 Links Exist)

- Register links with `frame.register_link(url)` and hit regions with `frame.register_hit(rect, hit_id, HitRegion::Link, link_id)`.
  - link registration: `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs:290`
- Provide keyboard navigation (Up/Down/Tab) as a peer to mouse hover/click for link activation.
  - keyboard link nav: `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs:81`
- Show visual distinction for focused vs hovered vs default links.
  - link styling: `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs:310`

Reference implementation:
- Hyperlink Playground: `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs`

## Cross-Cutting Design Patterns

These patterns recur across many screens and should be applied consistently.
See also [ARCHITECTURE.md](references/ARCHITECTURE.md) sections 9-17 for full details.

### Layout Caching for Hit-Testing

Store layout rectangles in `Cell<Rect>` during `view()`, read them in `update()` for mouse hit-testing.
This decouples rendering from event handling and avoids borrow checker issues.

```
// In view(): self.layout_panel.set(panel_rect);
// In update(): if self.layout_panel.get().contains(mouse.x, mouse.y) { ... }
```

Every interactive screen uses this pattern:
- `crates/ftui-demo-showcase/src/screens/dashboard.rs:5597`
- `crates/ftui-demo-showcase/src/screens/kanban_board.rs:870`
- `crates/ftui-demo-showcase/src/screens/drag_drop.rs:112`

### Enum-Driven Focus Management

Use an enum to model which panel has focus. Implement `next()`/`prev()` for cycling.
Mouse clicks set focus via hit-testing. Keyboard navigation uses Tab/Shift-Tab or directional keys.

```
enum FocusPanel { Editor, Search, Replace, View }
```

Examples:
- `crates/ftui-demo-showcase/src/screens/forms_input.rs:34`
- `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:588`
- `crates/ftui-demo-showcase/src/screens/shakespeare.rs:343`

### Basis Points for Splitter Ratios

Use basis points (0-10000 bps) instead of pixels for resizable splitter positions.
This survives terminal resizing without losing user intent.

- `crates/ftui-demo-showcase/src/screens/dashboard.rs:3442`

### Tick-Driven Animation

Use `tick_count: u64` and `time: f64 = tick_count as f64 * factor` for smooth animation.
Apply to gradient phases, text effects, sparkline updates, and streaming progression.

- `crates/ftui-demo-showcase/src/screens/dashboard.rs:3557`
- `crates/ftui-demo-showcase/src/screens/shakespeare.rs:873`

### RefCell for Interior Mutability in Stateful Widgets

Use `RefCell<WidgetState>` to allow `view()` (which takes `&self`) to mutate widget state
when required by the framework's stateful widget rendering pattern.

- `crates/ftui-demo-showcase/src/screens/forms_input.rs:1077`
- `crates/ftui-demo-showcase/src/screens/form_validation.rs:65`

### VecDeque Ring Buffers for Bounded History

Use `VecDeque<T>` with `pop_front()` at capacity for bounded logs, undo stacks, and timelines.

- `crates/ftui-demo-showcase/src/screens/inline_mode_story.rs:246`
- `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:647`

### Deterministic Mode for Testing

Support environment-variable-driven deterministic mode that replaces timestamps with tick counts
and uses fixed seeds for reproducible test scenarios.

- `crates/ftui-demo-showcase/src/screens/determinism_lab.rs:296`
- `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:173`

### HoverStabilizer for Jitter Prevention

Use `HoverStabilizer` to prevent hover state flickering from noisy mouse position reports.

- `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:635`

## doctor_frankentui Diagnostic Workflow (Visual-First)

`doctor_frankentui` is not just for pass/fail capture plumbing. Use it to see real UI states and catch showcase regressions.

### Execution Checklist

- [ ] Capture full suite with `doctor_frankentui suite`.
- [ ] Inspect `report.json` for run health fields.
- [ ] Inspect `snapshot.png` and `timeline_strip.png` for every profile.
- [ ] Patch profiles or screen code based on visual evidence.
- [ ] Rebuild `doctor_frankentui` if profile env files changed.
- [ ] Re-run targeted profile, then full suite.

Decision tree:
- If `status=failed` -> fix capture/runtime failure first.
- If `status=ok` but visuals are wrong -> treat as real bug and fix.
- If `snapshot` is shell but timeline shows UI -> fix `snapshot_second`.
- If timeline is shell-only -> debug app startup/exit behavior.

### 1) Build and run suite captures

Use `rch` for compile/test work:

```bash
cd /data/projects/frankentui
rch exec -- cargo build -p doctor_frankentui -p ftui-demo-showcase
```

Run the full demo showcase sweep:

```bash
RUN_ROOT="/tmp/doctor_frankentui_demo_audit_$(date +%Y%m%d_%H%M%S)"
./target/debug/doctor_frankentui suite \
  --app-command '/data/projects/frankentui/target/debug/ftui-demo-showcase' \
  --project-dir /data/projects/frankentui \
  --run-root "$RUN_ROOT" \
  --suite-name demo_showcase_audit \
  --keep-going
```

### 2) Triage machine-readable run health

Do not stop at `success=4 failure=0`. Inspect per-run metadata:

```bash
REPORT="$RUN_ROOT/demo_showcase_audit/report.json"
jq -r '.runs[] | [
  .profile,
  .status,
  ("capture_error_reason=" + (.capture_error_reason // "null")),
  ("vhs_driver=" + (.vhs_driver_used // "unknown")),
  ("fallback_active=" + (.fallback_active|tostring)),
  ("snapshot_status=" + (.snapshot_status // "unknown")),
  ("snapshot_exists=" + (.snapshot_exists|tostring)),
  ("video_exists=" + (.video_exists|tostring)),
  ("video_duration_seconds=" + (.video_duration_seconds|tostring))
] | @tsv' "$REPORT"
```

### 3) Inspect visuals, not just JSON

Open each profile’s `snapshot.png`, and generate timeline strips from `capture.mp4`:

```bash
SUITE_DIR="$RUN_ROOT/demo_showcase_audit"
for p in analytics-empty analytics-seeded messages-seeded tour-seeded; do
  d="$SUITE_DIR/demo_showcase_audit_${p}"
  ffmpeg -y -i "$d/capture.mp4" \
    -vf "fps=1,scale=640:-1,tile=8x1" \
    -frames:v 1 "$d/timeline_strip.png" >/dev/null 2>/dev/null
done
```

Then inspect:
- `.../snapshot.png` (single selected frame used by report)
- `.../timeline_strip.png` (temporal overview)
- `.../capture.mp4` (ground truth playback when needed)

### 4) Interpret common failure modes correctly

- `snapshot_status=ok` but shell prompt image:
  - technically captured, but diagnostically useless for UI quality.
- `snapshot_status=ok` and `snapshot_exists=true` but timeline shows app quit early:
  - snapshot second is landing after app exit.
- timeline has UI frames, snapshot is shell:
  - snapshot timing bug (profile config), not necessarily app rendering bug.
- timeline is shell-only:
  - app launch/runtime issue; inspect `vhs.log`, `run_summary.txt`, and `*.runner.log`.
- `fallback_active=true` or `vhs_driver_used=docker`:
  - host VHS/ttyd path degraded; diagnose separately before trusting timing comparisons.

### 5) Fix loop for profile and capture-quality issues

Adjust profile capture timing under:
- `crates/doctor_frankentui/profiles/*.env`

Most common fix: tune `snapshot_second` so it lands on a meaningful in-app frame before quit.

Important: profile env files are embedded by `include_str!`, so rebuild `doctor_frankentui` after profile edits:

```bash
rch exec -- cargo build -p doctor_frankentui
```

Re-run targeted profile quickly:

```bash
RUN_ROOT="/tmp/doctor_frankentui_verify_$(date +%Y%m%d_%H%M%S)"
./target/debug/doctor_frankentui suite \
  --profiles analytics-empty \
  --app-command '/data/projects/frankentui/target/debug/ftui-demo-showcase' \
  --project-dir /data/projects/frankentui \
  --run-root "$RUN_ROOT" \
  --suite-name analytics_empty_verify \
  --keep-going
```

Then run full suite again to ensure global coverage.

### 6) Required verification after doctor/franken captures tooling changes

```bash
rch exec -- cargo test -p doctor_frankentui
rch exec -- cargo clippy -p doctor_frankentui -- -D warnings
```

### Anti-patterns (Do Not Do These)

- Do not treat `success=4 failure=0` as sufficient proof of visual quality.
- Do not trust a single `snapshot.png` without checking timeline context.
- Do not patch screen code before confirming whether the issue is capture/profile timing.
- Do not forget that profile env files are compile-time embedded (`include_str!`).

## Quick Router

| Task | Go To |
|------|-------|
| Core crate architecture / contracts | [ARCHITECTURE.md](references/ARCHITECTURE.md) |
| Full demo-showcase internals + global interaction contract | [DEMO_SHOWCASE_DEEP_DIVE.md](references/DEMO_SHOWCASE_DEEP_DIVE.md) |
| Upgrade low-quality screens to showcase quality (naive -> premium patterns) | [TUI_POLISH_PLAYBOOK.md](references/TUI_POLISH_PLAYBOOK.md) |
| Visual diagnostics + doctor_frankentui playbook | [DOCTOR_FRANKENTUI_VISUAL_DIAGNOSTICS.md](references/DOCTOR_FRANKENTUI_VISUAL_DIAGNOSTICS.md) |
| Mine historical prompt patterns | [CASS_PATTERNS.md](references/CASS_PATTERNS.md) |

## Workflow

- [ ] 1. Confirm architecture guardrails in `references/ARCHITECTURE.md`.
- [ ] 2. Map target screen against global shell invariants and search invariants in `references/DEMO_SHOWCASE_DEEP_DIVE.md`.
- [ ] 2a. Cross-check the exact nearest demo pattern in the full registry atlas (`references/DEMO_SHOWCASE_DEEP_DIVE.md`, section `22`).
- [ ] 3. Apply concrete `Naive -> Showcase` deltas from `references/TUI_POLISH_PLAYBOOK.md`.
- [ ] 4. Mine relevant cass rituals and anti-patterns from `references/CASS_PATTERNS.md`.
- [ ] 5. Run quality gates and demo-sensitive tests.
- [ ] 5a. Run `doctor_frankentui` visual audit and review snapshots + timeline strips before declaring UX done.

## Quality Gates (Required)

Use remote compilation helper for heavy commands:

```bash
rch exec -- cargo check --workspace --all-targets
rch exec -- cargo clippy --workspace --all-targets -- -D warnings
cargo fmt --check
```

For showcase-sensitive changes:

```bash
rch exec -- cargo test -p ftui-demo-showcase
```

For search/chrome changes, also run:

```bash
rch exec -- cargo test -p ftui-demo-showcase shakespeare
rch exec -- cargo test -p ftui-demo-showcase code_explorer
rch exec -- cargo test -p ftui-demo-showcase log_search
rch exec -- cargo test -p ftui-demo-showcase virtualized_search
```

For markdown/panes/forms changes, also run:

```bash
rch exec -- cargo test -p ftui-demo-showcase markdown_rich_text
rch exec -- cargo test -p ftui-demo-showcase dashboard
rch exec -- cargo test -p ftui-demo-showcase forms_input
rch exec -- cargo test -p ftui-demo-showcase form_validation
```

## Cass Mining (Fast Path)

```bash
cass status --json && cass index --json
cass search "mind-blowing dashboard" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "under construction placeholder" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "improve TUI" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "search mode" --workspace /data/projects/frankentui --json --fields minimal --limit 50
```

Then inspect the top hits with:

```bash
cass view /path/to/session.jsonl -n <line> -C 20
```

Prompt-only filter:

```bash
cass search "under construction" --workspace /data/projects/frankentui --json --fields minimal --limit 100 \
  | jq '[.hits[] | select(.line_number <= 3)]'
```

## Anti-Slop Rule

Do not ship "placeholder UI" surfaces in showcase screens. Any screen intended as a flagship must provide:

- responsive layout tiers,
- meaningful motion or live data,
- interactive hit targets,
- command palette discoverability,
- status + help integration,
- global theme cycling (`Ctrl+T`),
- explicit keyboard discoverability (`fn keybindings()` + visible in help/status),
- graceful tiny-space behavior with usable fallbacks,
- streaming markdown quality when markdown output is present,
- adjustable panes when multi-panel layouts are present,
- strong section delineation (rounded borders + semantic color separation) for multi-section screens,
- intentional palette discipline (neutral regions + accent highlights from theme tokens),
- rich forms + validation quality when data entry is present,
- keyboard-accessible drag-and-drop with announcements when drag interactions are present,
- grapheme-aware text handling (`display_width()`, not `.len()`) for i18n correctness,
- deterministic rendering hooks and JSONL diagnostics for testable animation/state,
- configuration persistence (JSON round-trip, presets, validation on import) when user config exists,
- theme and accessibility compliance.

Use the `Naive -> Showcase` checklist in `references/TUI_POLISH_PLAYBOOK.md`.

## References

- [Architecture](references/ARCHITECTURE.md)
- [Demo Showcase Deep Dive](references/DEMO_SHOWCASE_DEEP_DIVE.md)
- [TUI Polish Playbook](references/TUI_POLISH_PLAYBOOK.md)
- [doctor_frankentui Visual Diagnostics](references/DOCTOR_FRANKENTUI_VISUAL_DIAGNOSTICS.md)
- [Cass Patterns](references/CASS_PATTERNS.md)
