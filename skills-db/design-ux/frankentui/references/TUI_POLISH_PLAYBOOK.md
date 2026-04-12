# TUI Polish Playbook

This is the practical conversion guide from weak/naive surfaces to showcase-grade screens.

## 1. Capability Gates (Read First)

Showcase quality is capability-gated:

- Always required:
  - global shell compatibility (tabs/status/help/palette),
  - theme cycling + discoverable keybindings,
  - robust resize behavior (including tight-space fallback),
  - coherent token-based styling and interaction semantics,
  - intentional palette discipline (neutrals for surfaces, accents for highlights).
- Required only when capability exists:
  - search excellence contract,
  - markdown streaming contract,
  - adjustable pane contract,
  - forms/validation contract,
  - high-signal text effects + metrics visualization for data-rich screens,
  - section delineation contract for section-dense layouts.

When selecting a concrete reference screen, use the full registry-order atlas in
`DEMO_SHOWCASE_DEEP_DIVE.md` section `22` to pick the closest matching showcase pattern.

## 2. Naive -> Showcase Matrix

| Naive Pattern | Why It Looks Bad | Showcase Pattern | Canonical Reference |
|---------------|------------------|------------------|---------------------|
| One paragraph saying "under construction" | No information density, no interaction | Adaptive multi-panel composition with live state | `crates/ftui-demo-showcase/src/screens/dashboard.rs:5666` |
| Single static layout | Breaks on resize and cramped terminals | Explicit large/medium/tiny layout tiers | `crates/ftui-demo-showcase/src/screens/dashboard.rs:6174` |
| Tiny terminals clip or panic | UX collapses when space constrained | Show minimal meaningful fallback content | `crates/ftui-demo-showcase/src/screens/shakespeare.rs:613` |
| Screen ignores global shell | Feels disconnected and inconsistent | Respect tab/status/help/palette integration | `crates/ftui-demo-showcase/src/app.rs:3928` |
| No global theme shortcut | Theme feels hidden and brittle | Global `Ctrl+T` + palette action | `crates/ftui-demo-showcase/src/app.rs:3805` |
| Colors are picked ad hoc | Visual language feels noisy and inconsistent | Use curated theme tokens with neutral bases + semantic accents | `crates/ftui-demo-showcase/src/theme.rs:260` |
| Monochrome tabs | Weak navigation affordance | Accent-colored active tabs per screen | `crates/ftui-demo-showcase/src/chrome.rs:362` |
| No bottom shortcut discoverability | Hidden power features | Status bar with nav and toggles | `crates/ftui-demo-showcase/src/chrome.rs:595` |
| No per-screen help key map | Users cannot discover controls | Merge global + screen keybindings in help overlay | `crates/ftui-demo-showcase/src/chrome.rs:1109` |
| Many sections blend together visually | Hard to scan hierarchy and semantics | Rounded bordered panels + semantic color accents per section | `crates/ftui-demo-showcase/src/screens/dashboard.rs:3847` |
| Search requires submit | Slow and clunky | True search-as-you-type | `crates/ftui-demo-showcase/src/screens/shakespeare.rs:519` |
| Search has flat styling | Active result not legible | Match hierarchy (marker, line highlight, active emphasis) | `crates/ftui-demo-showcase/src/screens/code_explorer.rs:1235` |
| Search has no context aids | Poor navigation confidence | Match radar + sparkline + neighborhood list | `crates/ftui-demo-showcase/src/screens/code_explorer.rs:1907` |
| Markdown appears only after full completion | No streaming feedback | Incremental `render_streaming` + cursor + progress | `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:676` |
| Multi-pane layout is rigid | Wasted space + no user control | Draggable splitters with bounded ratios | `crates/ftui-demo-showcase/src/screens/dashboard.rs:3452` |
| Forms are plain inputs without feedback | Low trust and poor completion flow | Required/error/progress badges + status telemetry | `crates/ftui-demo-showcase/src/screens/forms_input.rs:506` |
| Form edits are fragile | Users fear making changes | Undo/redo stack + visible history | `crates/ftui-demo-showcase/src/screens/forms_input.rs:693` |
| Data screen is mostly text numbers | Weak at-a-glance signal | Rich charts/sparklines and graphical indicators | `crates/ftui-demo-showcase/src/screens/dashboard.rs:3841` |
| Important text has no emphasis | High-signal events get lost | Liberal but purposeful text effects (gradient/glow/wave/reveal) | `crates/ftui-demo-showcase/src/screens/shakespeare.rs:873` |
| Drag reorder is mouse-only | Inaccessible, no keyboard alternative | Full keyboard drag via `KeyboardDragManager` with screen reader announcements | `crates/ftui-demo-showcase/src/screens/drag_drop.rs:358` |
| Drag has no visual feedback | Users lose context of source and target | Dimmed ghost source + highlighted drop target + focus indicator | `crates/ftui-demo-showcase/src/screens/kanban_board.rs:464` |
| Text uses `.len()` for layout | Breaks on CJK, emoji, combining marks | Use `display_width()` for terminal cells, `grapheme_count()` for editing | `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:677` |
| No RTL support | Arabic/Hebrew layouts broken | `Flex::flow_direction()` auto-mirrors layout for RTL locales | `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:606` |
| Fixed layout ignores terminal width | Wastes space on large, clips on small | `ResponsiveLayout` with `Breakpoint` tiers + `Visibility` gating | `crates/ftui-demo-showcase/src/screens/responsive_demo.rs:134` |
| Hover state flickers on mouse movement | Noisy UX from jitter | `HoverStabilizer` dampens rapid state changes | `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:635` |
| Config changes are lost on exit | Users must re-configure every session | Serde JSON round-trip with preset system (built-in + custom) | `crates/ftui-demo-showcase/src/screens/widget_builder.rs:134` |
| No way to debug layout constraints | Layout issues invisible | `LayoutDebugger` + `ConstraintOverlay` visualize solver behavior | `crates/ftui-demo-showcase/src/screens/layout_inspector.rs:273` |
| Animation is non-reproducible | Cannot test or snapshot animated screens | Deterministic mode with seed-driven LCG + FNV-1a checksums | `crates/ftui-demo-showcase/src/screens/determinism_lab.rs:296` |
| Links are plain text | No clickable URLs in terminal | OSC-8 hyperlinks via `frame.register_link()` + `HitRegion::Link` | `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs:290` |

## 3. Upgrade Procedure (Always-On Baseline)

- [ ] Register screen IA metadata in `SCREEN_REGISTRY`.
  - `crates/ftui-demo-showcase/src/screens/mod.rs:122`
- [ ] Keep screen inside app content slot and compatible with global chrome.
  - `crates/ftui-demo-showcase/src/app.rs:3948`
- [ ] Provide explicit keybindings via `fn keybindings()`.
  - `crates/ftui-demo-showcase/src/app.rs:4058`
- [ ] Expose meaningful single-letter or compact shortcuts where possible.
  - `crates/ftui-demo-showcase/src/screens/dashboard.rs:6200`
- [ ] Delineate each major section with a visible bordered container.
  - `crates/ftui-demo-showcase/src/screens/forms_input.rs:764`
- [ ] Use theme tokens and screen accents, not ad-hoc color literals.
  - `crates/ftui-demo-showcase/src/chrome.rs:1298`
- [ ] Keep neutrals on large surfaces and accents on highlights/focus states.
  - `crates/ftui-demo-showcase/src/theme.rs:723`
- [ ] Ensure resize resilience and tiny-space fallback.
  - `crates/ftui-demo-showcase/src/screens/dashboard.rs:5813`

## 4. Capability Modules (Apply Only If Present)

### 4.1 Search Module

- [ ] `/` or `Ctrl+F` enters search focus.
- [ ] Live update on every edit event.
- [ ] Enter/Tab/arrows and `n/N` navigate matches.
- [ ] Show `current/total` matches.
- [ ] Render active-match emphasis stronger than passive matches.
- [ ] Add contextual search aids (radar/sparkline/snippets) for large datasets.

References:

- `crates/ftui-demo-showcase/src/screens/shakespeare.rs:531`
- `crates/ftui-demo-showcase/src/screens/shakespeare.rs:859`
- `crates/ftui-demo-showcase/src/screens/code_explorer.rs:798`
- `crates/ftui-demo-showcase/src/screens/code_explorer.rs:1907`
- `crates/ftui-demo-showcase/src/screens/log_search.rs:1077`
- `crates/ftui-demo-showcase/src/screens/virtualized_search.rs:1051`

### 4.2 Markdown Streaming Module

- [ ] Render full markdown/GFM theme quality (tables, task lists, admonitions, math).
- [ ] Stream fragments incrementally with `render_streaming`.
- [ ] Show clear stream state (progress/status/cursor).
- [ ] Bind controls for play/pause/restart/turbo and scrolling.

References:

- `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:578`
- `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:686`
- `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:905`
- `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:1101`

### 4.3 Adjustable Pane Module

- [ ] Define splitter hit regions and visible handles.
- [ ] Drag gestures update ratios with clamped min/max bounds.
- [ ] Drag state clears robustly on mouse-up and keyboard actions.
- [ ] Shortcuts/help text explicitly mention resizing.

References:

- `crates/ftui-demo-showcase/src/screens/dashboard.rs:3488`
- `crates/ftui-demo-showcase/src/screens/dashboard.rs:5620`
- `crates/ftui-demo-showcase/src/screens/dashboard.rs:6006`
- `crates/ftui-demo-showcase/src/screens/dashboard.rs:6238`

### 4.4 Forms Module

- [ ] Multi-control form types with clear focus model.
- [ ] Validation reflects touched/dirty semantics where appropriate.
- [ ] Status line communicates progress, errors, and state.
- [ ] Undo/redo exists for non-trivial editing workflows.
- [ ] Keybinding hints include submit/cancel/mode-switch behavior.

References:

- `crates/ftui-demo-showcase/src/screens/forms_input.rs:34`
- `crates/ftui-demo-showcase/src/screens/forms_input.rs:430`
- `crates/ftui-demo-showcase/src/screens/forms_input.rs:362`
- `crates/ftui-demo-showcase/src/screens/forms_input.rs:693`
- `crates/ftui-demo-showcase/src/screens/form_validation.rs:343`

### 4.5 Visual Signal Density Module

- [ ] Use text effects liberally but purposefully for high-signal text.
- [ ] Use graphical indicators (sparklines/charts/heatmaps/bars) for metrics.
- [ ] Preserve readability in reduced-space variants (fallback mini charts/text).

References:

- `crates/ftui-demo-showcase/src/screens/shakespeare.rs:873`
- `crates/ftui-demo-showcase/src/screens/code_explorer.rs:1137`
- `crates/ftui-demo-showcase/src/screens/dashboard.rs:3910`
- `crates/ftui-demo-showcase/src/screens/data_viz.rs:113`

### 4.6 Multi-Section Delineation Module

- [ ] Major sections are boxed with bordered panels (prefer `Rounded` by default).
- [ ] Panel border colors are semantic (domain/focus/state), not arbitrary.
- [ ] Section contrast remains clear in compact/tiny layouts.

References:

- `crates/ftui-demo-showcase/src/screens/dashboard.rs:3847`
- `crates/ftui-demo-showcase/src/screens/dashboard.rs:3852`
- `crates/ftui-demo-showcase/src/screens/forms_input.rs:764`
- `crates/ftui-demo-showcase/src/screens/forms_input.rs:760`
- `crates/ftui-demo-showcase/src/screens/data_viz.rs:119`

### 4.7 Color Harmony Module

- [ ] Build color pairings from theme tokens; avoid one-off RGB choices.
- [ ] Use neutral tones (`bg`, `alpha::SURFACE`) for large containers.
- [ ] Use semantic accent colors for highlights, focus, warnings, and status.
- [ ] Ensure contrast and readability remain within tested theme constraints.
- [ ] Validate appearance across the standard `Ctrl+T` theme rotation (`Cyberpunk Aurora`, `Darcula`, `Lumen Light`, `Nordic Frost`) and accessibility `High Contrast`.

References:

- `crates/ftui-demo-showcase/src/app.rs:3805`
- `crates/ftui-extras/src/theme.rs:26`
- `crates/ftui-extras/src/theme.rs:49`
- `crates/ftui-demo-showcase/src/theme.rs:260`
- `crates/ftui-demo-showcase/src/theme.rs:723`
- `crates/ftui-demo-showcase/src/theme.rs:736`
- `crates/ftui-demo-showcase/src/theme.rs:779`
- `crates/ftui-demo-showcase/src/theme.rs:1309`
- `crates/ftui-demo-showcase/src/theme.rs:1459`

### 4.8 Drag-and-Drop Module

- [ ] Implement three-phase drag state machine: Down (arm) -> Drag (update hover) -> Up (commit/cancel).
- [ ] Provide `KeyboardDragManager` integration for full keyboard accessibility.
- [ ] Build `DropTargetInfo` list dynamically from current state.
- [ ] Show drag source as dimmed/ghost, drop target as highlighted with success color.
- [ ] Sync keyboard focus and mouse selection on every interaction.
- [ ] Include undo/redo for drag operations (clear redo on new move).
- [ ] Emit announcements for screen readers during keyboard drag.

References:

- `crates/ftui-demo-showcase/src/screens/kanban_board.rs:321`
- `crates/ftui-demo-showcase/src/screens/kanban_board.rs:668`
- `crates/ftui-demo-showcase/src/screens/drag_drop.rs:358`
- `crates/ftui-demo-showcase/src/screens/drag_drop.rs:446`

### 4.9 Accessibility and i18n Module

- [ ] Use `display_width()` for layout calculations, never `.len()` or `.chars().count()`.
- [ ] Use `grapheme_count()` and `graphemes()` for cursor/editing positions.
- [ ] Handle CJK double-width (2 cells), combining marks (0 cells), ZWJ emoji sequences.
- [ ] Use `truncate_with_ellipsis()` for width-safe truncation.
- [ ] Support RTL layout via `Flex::flow_direction(FlowDirection::Rtl)`.
- [ ] Use `StringCatalog` with `PluralForms` for multi-locale text.
- [ ] Provide full keyboard navigation as a peer to mouse for all interactive elements.

References:

- `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:677`
- `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:100`
- `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:606`
- `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:1064`
- `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:1049`

### 4.10 Diagnostic and Telemetry Module

- [ ] Use JSONL structured logging with monotonic sequence numbers.
- [ ] Include FNV-1a checksums for determinism verification.
- [ ] Support env-var-driven configuration (paths, deterministic mode, seeds).
- [ ] Provide telemetry hooks (callbacks) for external observers.
- [ ] Use `VecDeque` ring buffers with bounded capacity for event history.
- [ ] Display Bayesian evidence when introspecting runtime decisions.

References:

- `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:173`
- `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:476`
- `crates/ftui-demo-showcase/src/screens/determinism_lab.rs:579`
- `crates/ftui-demo-showcase/src/screens/explainability_cockpit.rs:693`
- `crates/ftui-demo-showcase/src/screens/voi_overlay.rs:140`

### 4.11 Responsive Layout Module

- [ ] Use `ResponsiveLayout` with `Breakpoint` tiers for structured responsive design.
- [ ] Use `Visibility::visible_above()` to hide components below their breakpoint.
- [ ] Use `Responsive<T>::resolve(bp)` for per-breakpoint value switching.
- [ ] For content-aware sizing, compute constraints procedurally with minimum floors.
- [ ] Use `LayoutDebugger` + `ConstraintOverlay` to visualize constraint solver during development.
- [ ] Support width override for testing responsive behavior at specific widths.

References:

- `crates/ftui-demo-showcase/src/screens/responsive_demo.rs:134`
- `crates/ftui-demo-showcase/src/screens/responsive_demo.rs:289`
- `crates/ftui-demo-showcase/src/screens/intrinsic_sizing.rs:252`
- `crates/ftui-demo-showcase/src/screens/layout_inspector.rs:273`

### 4.12 Text Editing Module

- [ ] Use `TextArea` widget with line numbers, soft wrap, and cursor tracking.
- [ ] Implement search with `search_ascii_case_insensitive()` returning byte-range results.
- [ ] Convert between byte offsets and line/grapheme positions via line iteration.
- [ ] Provide replace and replace-all with reverse-order byte-range substitution.
- [ ] Include undo/redo via bounded `VecDeque<String>` history stack.
- [ ] For split-pane editors, re-render preview only on content change.
- [ ] Support diff mode to diagnose width mismatches between source and rendered output.

References:

- `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:868`
- `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:997`
- `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:647`
- `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs:183`
- `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs:463`

### 4.13 Configuration Persistence Module

- [ ] Use serde `Serialize`/`Deserialize` snapshot types for JSON import/export.
- [ ] Provide built-in presets (read-only) plus user-saveable custom presets.
- [ ] Use FNV-1a hashing for regression detection on snapshots.
- [ ] Validate imported data before applying.
- [ ] Support theme override chains (base preset -> property overrides -> per-render state).

References:

- `crates/ftui-demo-showcase/src/screens/widget_builder.rs:134`
- `crates/ftui-demo-showcase/src/screens/widget_builder.rs:226`
- `crates/ftui-demo-showcase/src/screens/table_theme_gallery.rs:410`
- `crates/ftui-demo-showcase/src/screens/table_theme_gallery.rs:478`

### 4.14 Hyperlink Module

- [ ] Register links with `frame.register_link(url)` and hit regions with `HitRegion::Link`.
- [ ] Provide keyboard navigation (Up/Down/Tab) for link traversal.
- [ ] Style focused, hovered, and default links distinctly.
- [ ] Include E2E logging with JSONL for test validation.

References:

- `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs:290`
- `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs:81`
- `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs:310`

## 5. Space-Constrained Quality Checklist

- [ ] Explicitly handle `area.is_empty()` and return safely.
- [ ] Define minimum usable layout and tiny fallback mode.
- [ ] Hide non-critical subpanels when height/width is tight.
- [ ] Keep at least one high-signal indicator visible in tiny mode.
- [ ] Add tests for threshold boundaries and small-size rendering.

References:

- `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:1128`
- `crates/ftui-demo-showcase/src/screens/forms_input.rs:722`
- `crates/ftui-demo-showcase/src/screens/forms_input.rs:779`
- `crates/ftui-demo-showcase/src/screens/dashboard.rs:6586`
- `crates/ftui-demo-showcase/src/screens/form_validation.rs:739`

## 6. Quality Gates

```bash
rch exec -- cargo check --workspace --all-targets
rch exec -- cargo clippy --workspace --all-targets -- -D warnings
cargo fmt --check
rch exec -- cargo test -p ftui-demo-showcase
```

Capability-targeted test slices:

```bash
# Search/chrome:
rch exec -- cargo test -p ftui-demo-showcase shakespeare
rch exec -- cargo test -p ftui-demo-showcase code_explorer

# Markdown/panes/forms:
rch exec -- cargo test -p ftui-demo-showcase markdown_rich_text
rch exec -- cargo test -p ftui-demo-showcase dashboard
rch exec -- cargo test -p ftui-demo-showcase forms_input
rch exec -- cargo test -p ftui-demo-showcase form_validation

# Drag-and-drop/accessibility:
rch exec -- cargo test -p ftui-demo-showcase kanban_board
rch exec -- cargo test -p ftui-demo-showcase drag_drop
rch exec -- cargo test -p ftui-demo-showcase mouse_playground

# Layout/responsive:
rch exec -- cargo test -p ftui-demo-showcase responsive_demo
rch exec -- cargo test -p ftui-demo-showcase intrinsic_sizing
rch exec -- cargo test -p ftui-demo-showcase layout_inspector

# Text editing/i18n:
rch exec -- cargo test -p ftui-demo-showcase advanced_text_editor
rch exec -- cargo test -p ftui-demo-showcase markdown_live_editor
rch exec -- cargo test -p ftui-demo-showcase i18n_demo

# Systems/diagnostics:
rch exec -- cargo test -p ftui-demo-showcase determinism_lab
rch exec -- cargo test -p ftui-demo-showcase explainability_cockpit
rch exec -- cargo test -p ftui-demo-showcase voi_overlay

# Configuration/theming:
rch exec -- cargo test -p ftui-demo-showcase widget_builder
rch exec -- cargo test -p ftui-demo-showcase table_theme_gallery
rch exec -- cargo test -p ftui-demo-showcase hyperlink_playground
```

## 7. Non-Negotiables

- Do not ship placeholder-only showcase surfaces.
- Do not bypass central hit-testing/mouse routing.
- Do not hide power features from help/status discoverability.
- Do not force capability modules that are irrelevant to the screen.
- Do not ship section-dense screens without clear bordered segmentation and semantic color separation.
- Do not use arbitrary color mixes that bypass the curated theme palette.
- Do not skip quality gates after substantive changes.
- Do not use `.len()` or `.chars().count()` for display width calculations; use `display_width()`.
- Do not implement mouse-only drag interactions without keyboard accessibility.
- Do not hardcode layout widths without responsive fallbacks or minimum floors.
- Do not ship animated screens without deterministic mode support for testing.
- Do not store unbounded history/logs; use `VecDeque` with capacity limits.
