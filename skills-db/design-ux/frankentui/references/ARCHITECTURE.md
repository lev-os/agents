# FrankenTUI Architecture

This is the minimum architecture model required before touching `ftui-demo-showcase`.

## 1. Layer Contracts

FrankenTUI is a strict layered pipeline:

1. Input: `TerminalSession` and event parsing (`ftui-core`)
2. Runtime loop: `Model` + `Cmd` + scheduling (`ftui-runtime`)
3. Render kernel: `Frame -> Buffer -> BufferDiff -> Presenter` (`ftui-render`)
4. Output coordinator: `TerminalWriter` (`ftui-runtime`)

Primary references:

- `crates/ftui-core/src/terminal_session.rs:284`
- `crates/ftui-runtime/src/program.rs:105`
- `crates/ftui-runtime/src/program.rs:233`
- `crates/ftui-runtime/src/program.rs:3010`
- `crates/ftui-render/src/frame.rs:354`
- `crates/ftui-render/src/buffer.rs:210`
- `crates/ftui-render/src/diff.rs:975`
- `crates/ftui-render/src/presenter.rs:324`
- `crates/ftui-runtime/src/terminal_writer.rs:436`

## 2. Runtime Core (Elm/Bubbletea Style)

`Model` contract:

- `init()`
- `update(msg)`
- `view(frame)`
- `subscriptions()`

Reference:

- `crates/ftui-runtime/src/program.rs:105`

Execution flow:

- `Program::run()` event loop
- `render_frame()` builds/presents each frame
- terminal presentation delegated to `TerminalWriter::present_ui_owned`

References:

- `crates/ftui-runtime/src/program.rs:3396`
- `crates/ftui-runtime/src/program.rs:3407`
- `crates/ftui-runtime/src/program.rs:3874`
- `crates/ftui-runtime/src/program.rs:4032`

## 3. Render Kernel

Core render types:

- `Cell` optimized comparison (`bits_eq`)
- `Buffer` row-major store + dirty tracking
- `BufferDiff` full/dirty diff computation
- `Presenter` ANSI emission and sync bracket behavior

References:

- `crates/ftui-render/src/cell.rs:301`
- `crates/ftui-render/src/cell.rs:371`
- `crates/ftui-render/src/buffer.rs:210`
- `crates/ftui-render/src/buffer.rs:251`
- `crates/ftui-render/src/buffer.rs:508`
- `crates/ftui-render/src/buffer.rs:860`
- `crates/ftui-render/src/diff.rs:975`
- `crates/ftui-render/src/diff.rs:1047`
- `crates/ftui-render/src/diff.rs:1070`
- `crates/ftui-render/src/presenter.rs:401`

## 4. Output Coordinator

`TerminalWriter` is the one-writer gate and screen-mode coordinator.

Key contracts:

- inline + inline-auto + alt-screen modes
- one-writer serialization of presents/log writes
- inline positioning/cleanup and cursor safety

References:

- `crates/ftui-runtime/src/terminal_writer.rs:203`
- `crates/ftui-runtime/src/terminal_writer.rs:436`
- `crates/ftui-runtime/src/terminal_writer.rs:1038`
- `crates/ftui-runtime/src/terminal_writer.rs:1155`
- `crates/ftui-runtime/src/terminal_writer.rs:1545`

## 5. Terminal Lifecycle / RAII

`TerminalSession` is the RAII lifecycle boundary.

Critical property: drop-based cleanup guarantees restoration on panic/unwind paths.

References:

- `crates/ftui-core/src/terminal_session.rs:284`
- `crates/ftui-core/src/terminal_session.rs:301`
- `crates/ftui-core/src/terminal_session.rs:750`
- `crates/ftui-core/src/terminal_session.rs:825`
- `crates/ftui-core/src/terminal_session.rs:856`

## 6. Public Facade

`ftui` crate reexports the stack for downstream consumers.

References:

- `crates/ftui/src/lib.rs:29`
- `crates/ftui/src/lib.rs:41`
- `crates/ftui/src/lib.rs:59`
- `crates/ftui/src/lib.rs:74`

## 7. Demo Showcase Bootstrap

The demo app configures screen mode, budgeting, and evidence sink then runs `Program`.

References:

- `crates/ftui-demo-showcase/src/main.rs:16`
- `crates/ftui-demo-showcase/src/main.rs:70`
- `crates/ftui-demo-showcase/src/main.rs:134`
- `crates/ftui-demo-showcase/src/main.rs:180`
- `crates/ftui-demo-showcase/src/main.rs:199`

## 8. Mouse Routing and Hit-Testing Infrastructure

`Frame` provides a hit-region registration system for mouse interaction:

- `frame.register_hit(rect, HitId, HitRegion, data)` registers a clickable area
- `HitRegion` variants: `Content`, `Scrollbar`, `Link`, `Splitter`
- `HitId` is a u32 identifier; screens define base constants to partition the namespace

The canonical dispatch chain in the app shell resolves hits in priority order:
command palette > overlays > status toggles > tabs > pane content.

References:

- hit-id base constants: `crates/ftui-demo-showcase/src/chrome.rs:26`
- hit classifier: `crates/ftui-demo-showcase/src/chrome.rs:117`
- app click router: `crates/ftui-demo-showcase/src/app.rs:4471`
- scrollbar hit region: `crates/ftui-demo-showcase/src/screens/widget_gallery.rs:412`
- link hit region: `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs:290`

## 9. Layout Caching Pattern (Cell<Rect>)

All interactive screens cache layout rectangles from the `view()` phase for use during `update()`:

```
// view(): compute and store
self.layout_panel.set(panel_rect);

// update(): test mouse position
if self.layout_panel.get().contains(mouse.x, mouse.y) { ... }
```

This avoids recalculating layout on every event and prevents borrow checker conflicts
between the mutable view and immutable update phases. Use `std::cell::Cell<Rect>` (not `RefCell`).

References:

- dashboard panel rects: `crates/ftui-demo-showcase/src/screens/dashboard.rs:5597`
- kanban column rects: `crates/ftui-demo-showcase/src/screens/kanban_board.rs:870`
- inline mode layout rects: `crates/ftui-demo-showcase/src/screens/inline_mode_story.rs:112`

## 10. Keyboard Drag Manager (Accessibility)

`KeyboardDragManager` from `ftui_widgets` provides a framework for keyboard-accessible drag-and-drop:

- `KeyboardDragConfig` configures behavior (snap targets, announce mode)
- `DropTargetInfo` defines named drop zones with bounds
- `DragPayload::text()` creates portable drag data
- The system emits announcements for screen readers

References:

- `crates/ftui-demo-showcase/src/screens/drag_drop.rs:358`
- `crates/ftui-demo-showcase/src/screens/drag_drop.rs:446`

## 11. Hover Stabilization

`HoverStabilizer` from `ftui_core` dampens noisy hover state changes to prevent visual flickering:

```
let stabilized = self.hover_stabilizer.update(raw_target, (x, y), Instant::now());
if stabilized != self.current_hover { /* apply */ }
```

References:

- `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:635`

## 12. Responsive Layout API

`ftui_layout` provides structured responsive design primitives:

- `Breakpoint` enum: XS, SM, MD, LG, XL
- `Breakpoints::new(sm, md, lg)` defines custom width thresholds
- `ResponsiveLayout::new(default).at(Breakpoint::Md, flex)` defines per-tier layouts
- `Visibility::visible_above(Breakpoint::Md)` conditionally hides components
- `Responsive<T>::new(default).at(bp, value).resolve(bp)` switches values per breakpoint

References:

- `crates/ftui-demo-showcase/src/screens/responsive_demo.rs:91`
- `crates/ftui-demo-showcase/src/screens/responsive_demo.rs:134`
- `crates/ftui-demo-showcase/src/screens/responsive_demo.rs:289`
- `crates/ftui-demo-showcase/src/screens/responsive_demo.rs:309`

## 13. Constraint Debugging

`LayoutDebugger` and `LayoutRecord` visualize constraint solver behavior:

- `LayoutRecord::new(name, requested, received, constraints).with_child(...)` tracks hierarchy
- `LayoutConstraints::new(min_w, max_w, min_h, max_h)` stores bounds
- `ConstraintOverlay` renders debug visualization over layout regions
- Status detection: OK (satisfied), UNDER (below minimum), OVER (above maximum)

References:

- `crates/ftui-demo-showcase/src/screens/layout_inspector.rs:273`
- `crates/ftui-demo-showcase/src/screens/layout_inspector.rs:199`

## 14. Deterministic Rendering and Verification

For testable animations and reproducible rendering:

- Use seed-driven LCG (`lcg_next(state)`) for pseudo-random buffer generation
- FNV-1a 64-bit checksums (`checksum_buffer()`) verify buffer equivalence
- `BufferDiff::compute()` vs `BufferDiff::compute_dirty()` strategy comparison
- Environment variables: `FTUI_DEMO_SEED`, `FTUI_DEMO_RUN_ID`, `FTUI_DEMO_SCREEN_MODE`
- JSONL export for CI/CD verification reports

References:

- `crates/ftui-demo-showcase/src/screens/determinism_lab.rs:296`
- `crates/ftui-demo-showcase/src/screens/determinism_lab.rs:510`
- `crates/ftui-demo-showcase/src/screens/determinism_lab.rs:579`

## 15. Text Metrics Pipeline

`ftui_text` provides grapheme-aware text measurement:

- `display_width(text)` returns terminal cell count (handles CJK, emoji, combining marks)
- `grapheme_count(text)` returns extended grapheme cluster count
- `grapheme_width(g)` returns width of a single grapheme (0, 1, or 2)
- `graphemes(text)` returns an iterator of `&str` grapheme clusters
- `truncate_with_ellipsis(text, width, "...")` safely truncates
- `wrap_text(text, width, WrapMode)` wraps at word/char boundaries

Key rule: `display_width()` for layout, `grapheme_count()` for editing. Never `.len()` for display.

References:

- `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:677`
- `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:100`

## 16. Cross-Cutting Design Patterns

### Enum-Driven Focus Management

Use an enum to model which panel has focus. Implement `next()`/`prev()` for cycling.
Mouse clicks set focus via hit-testing. Keyboard navigation uses Tab/Shift-Tab or directional keys.

```
enum FocusPanel { Editor, Search, Replace, View }
```

- `crates/ftui-demo-showcase/src/screens/forms_input.rs:34`
- `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:588`
- `crates/ftui-demo-showcase/src/screens/shakespeare.rs:343`

### Basis Points for Splitter Ratios

Use basis points (0-10000 bps) instead of pixels for resizable splitter positions.
Survives terminal resizing without losing user intent.

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

## 17. Edit Guardrails

When changing showcase screens:

- respect runtime contracts (no ad-hoc terminal writes),
- keep all drawing in `view(&mut Frame)`,
- maintain deterministic behavior hooks for tests,
- preserve one-writer and RAII boundaries,
- use `Cell<Rect>` layout caching for hit-testing (not recalculation),
- register hit regions for all clickable surfaces,
- support both keyboard and mouse navigation for accessibility.
