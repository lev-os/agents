# ftui-demo-showcase Deep Dive

This file is the implementation-level map of the showcase app.

## 1. Entry and Program Wiring

`main.rs` chooses screen mode, budgets, evidence sink, and runs `Program`.

- `crates/ftui-demo-showcase/src/main.rs:16`
- `crates/ftui-demo-showcase/src/main.rs:20`
- `crates/ftui-demo-showcase/src/main.rs:70`
- `crates/ftui-demo-showcase/src/main.rs:134`
- `crates/ftui-demo-showcase/src/main.rs:180`
- `crates/ftui-demo-showcase/src/main.rs:199`

## 2. Screen Registry and IA

Registry is the single source of truth:

- `SCREEN_REGISTRY` constant: `crates/ftui-demo-showcase/src/screens/mod.rs:122`
- registry accessor: `crates/ftui-demo-showcase/src/screens/mod.rs:592`
- app test asserts current length `45`: `crates/ftui-demo-showcase/src/app.rs:6561`

Category definitions:

- `crates/ftui-demo-showcase/src/screens/mod.rs:66`

Current category counts (from `SCREEN_REGISTRY`):

- `ScreenCategory::Tour = 3`
- `ScreenCategory::Core = 6`
- `ScreenCategory::Visuals = 8`
- `ScreenCategory::Interaction = 11`
- `ScreenCategory::Text = 7`
- `ScreenCategory::Systems = 10`

## 3. App Shell and Global State

`AppModel` owns global showcase behavior:

- screen routing
- overlays and palette
- a11y toggles
- deterministic controls
- mouse dispatch and hit-test cache

References:

- `crates/ftui-demo-showcase/src/app.rs:2564`
- `crates/ftui-demo-showcase/src/app.rs:2963`
- `crates/ftui-demo-showcase/src/app.rs:3887`
- `crates/ftui-demo-showcase/src/app.rs:3922`

View layering order in `AppModel::view`:

1. tab bar
2. bordered content slot
3. active screen render
4. overlays (a11y/tour/help/debug/perf/evidence)
5. command palette top layer
6. status bar

References:

- `crates/ftui-demo-showcase/src/app.rs:3922`
- `crates/ftui-demo-showcase/src/app.rs:3985`
- `crates/ftui-demo-showcase/src/app.rs:4034`

## 4. ScreenStates Hub

`ScreenStates` centralizes per-screen state, lazy init, tick routing, and panic isolation.

References:

- struct: `crates/ftui-demo-showcase/src/app.rs:922`
- lazy deterministic visual effects handoff: `crates/ftui-demo-showcase/src/app.rs:1155`
- update dispatch: `crates/ftui-demo-showcase/src/app.rs:1180`
- tick dispatch: `crates/ftui-demo-showcase/src/app.rs:1327`
- theme fanout: `crates/ftui-demo-showcase/src/app.rs:1413`
- panic boundary + fallback widget: `crates/ftui-demo-showcase/src/app.rs:1435`

## 5. Command Palette Model

Palette actions are built from registry metadata plus global commands.

References:

- action builder: `crates/ftui-demo-showcase/src/app.rs:2963`
- registry loop for actions/tags: `crates/ftui-demo-showcase/src/app.rs:2973`
- refresh and action resolution: `crates/ftui-demo-showcase/src/app.rs:3060`

## 6. Mouse Routing and Hit Layering

Central dispatcher explicitly defines priority chain and click/scroll handling.

References:

- dispatcher: `crates/ftui-demo-showcase/src/app.rs:4208`
- click router: `crates/ftui-demo-showcase/src/app.rs:4471`
- scroll router: `crates/ftui-demo-showcase/src/app.rs:4538`

Priority order:

1. command palette
2. overlays
3. status toggles
4. tabs/category tabs
5. pane content

## 7. Chrome, Hit IDs, and Status Surfaces

Chrome module defines hit-id ranges and rendering/hit registration for tabs, categories, overlays, and status controls.

References:

- hit-id base constants: `crates/ftui-demo-showcase/src/chrome.rs:26`
- hit classifier: `crates/ftui-demo-showcase/src/chrome.rs:117`
- tab bar + hit regions: `crates/ftui-demo-showcase/src/chrome.rs:330`
- category tabs: `crates/ftui-demo-showcase/src/chrome.rs:431`
- status bar state + renderer: `crates/ftui-demo-showcase/src/chrome.rs:554`
- help overlay renderer: `crates/ftui-demo-showcase/src/chrome.rs:1186`
- accent mapping by screen id: `crates/ftui-demo-showcase/src/chrome.rs:1298`

## 8. Theme and Accessibility Control Plane

Theme file provides both visual tokens and runtime a11y mutation hooks:

- `set_large_text`, `set_motion_scale`, `motion_scale`
- `apply_large_text`, `scale_spacing`
- screen accent token module

References:

- `crates/ftui-demo-showcase/src/theme.rs:95`
- `crates/ftui-demo-showcase/src/theme.rs:120`
- `crates/ftui-demo-showcase/src/theme.rs:131`
- `crates/ftui-demo-showcase/src/theme.rs:169`
- `crates/ftui-demo-showcase/src/theme.rs:180`
- `crates/ftui-demo-showcase/src/theme.rs:260`

## 9. Dashboard Screen (Flagship Layout Engine)

Dashboard is a large stateful multi-panel screen with panel links, splitter drags, and adaptive layout tiers.

Core state:

- `crates/ftui-demo-showcase/src/screens/dashboard.rs:3252`
- includes simulated data, markdown stream, syntax cache, chart mode, focus/hover, panel rectangles, bottom splitter state

Interaction model:

- pointer panel mapping and preferred link targets:
  - `crates/ftui-demo-showcase/src/screens/dashboard.rs:3430`
  - `crates/ftui-demo-showcase/src/screens/dashboard.rs:3502`
- pane-link registration into chrome hit grid:
  - `crates/ftui-demo-showcase/src/screens/dashboard.rs:5598`
- splitter handles and drag updates:
  - `crates/ftui-demo-showcase/src/screens/dashboard.rs:3452`
  - `crates/ftui-demo-showcase/src/screens/dashboard.rs:5620`

Responsive tiers:

- large: `>= 100x30`
- medium: `>= 70x20`
- tiny: fallback

References:

- layout renderers: `crates/ftui-demo-showcase/src/screens/dashboard.rs:5666`
- update/tick/view impl: `crates/ftui-demo-showcase/src/screens/dashboard.rs:6006`
- threshold switch: `crates/ftui-demo-showcase/src/screens/dashboard.rs:6170`

## 10. Visual Effects Screen (High-Complexity Engine)

`VisualEffectsScreen` is dual-mode (`Canvas` + `TextEffects`) with many effect families, deterministic test mode, quality gating, and panic-safe rendering.

Core structures:

- screen struct: `crates/ftui-demo-showcase/src/screens/visual_effects.rs:85`
- effect enum and catalog: `crates/ftui-demo-showcase/src/screens/visual_effects.rs:187`
- demo mode enum: `crates/ftui-demo-showcase/src/screens/visual_effects.rs:341`

Determinism and quality:

- deterministic mode fields: `crates/ftui-demo-showcase/src/screens/visual_effects.rs:171`
- quality-driven stride and rendering adaptation:
  - `crates/ftui-demo-showcase/src/screens/visual_effects.rs:3284`
  - `crates/ftui-demo-showcase/src/screens/visual_effects.rs:4277`
- deterministic tick enable:
  - `crates/ftui-demo-showcase/src/screens/visual_effects.rs:3512`

Input + mode routing:

- update handler: `crates/ftui-demo-showcase/src/screens/visual_effects.rs:4036`
- text-effects tab controls and canvas controls in same handler

Render path:

- view handler: `crates/ftui-demo-showcase/src/screens/visual_effects.rs:4205`
- effect render wrapped by `catch_unwind`:
  - `crates/ftui-demo-showcase/src/screens/visual_effects.rs:19`
  - `crates/ftui-demo-showcase/src/screens/visual_effects.rs:4296`

Tick path:

- panic fallback + fps stats + deterministic frame-time handling:
  - `crates/ftui-demo-showcase/src/screens/visual_effects.rs:4380`

## 11. What "Showcase Quality" Means Here

In this project, high-quality screens are expected to combine:

- responsive multi-tier layout,
- meaningful live state changes,
- keyboard + mouse interaction,
- hit-tested navigable panes,
- compatibility with help/status/palette overlays,
- theme and a11y compliance,
- deterministic hooks for replay/test environments.

The dashboard and visual-effects screens are the primary executable references for this standard.

## 12. Capability-Gated Showcase Contract

Showcase quality is capability-gated, not one-size-fits-all.

- Always required for showcase screens:
  - global shell compatibility (tab bar, status bar, help overlay, palette),
  - keyboard discoverability via `keybindings()`,
  - theme/a11y compliance,
  - graceful behavior under small terminal sizes.
- Required only when the capability exists in the screen:
  - search quality contract (if screen has search),
  - streaming markdown contract (if screen renders markdown/LLM output),
  - adjustable pane contract (if screen is multi-pane with resize affordances),
  - form/validation contract (if screen captures structured user input).

## 13. Global Shell Contract (Always-On)

Theme cycling is globally reachable via both keyboard and palette:

- app key handler (`Ctrl+T`): `crates/ftui-demo-showcase/src/app.rs:3805`
- palette command entry (`cmd:cycle_theme`): `crates/ftui-demo-showcase/src/app.rs:3043`
- command dispatch from palette: `crates/ftui-demo-showcase/src/app.rs:4870`
- theme mutation handler: `crates/ftui-demo-showcase/src/app.rs:3365`

Tab/status/help chrome is first-class UI, not optional decoration:

- tab bar rendering + hit regions: `crates/ftui-demo-showcase/src/chrome.rs:330`
- active tab accent styling: `crates/ftui-demo-showcase/src/chrome.rs:362`
- per-screen accent map: `crates/ftui-demo-showcase/src/chrome.rs:1298`
- status bar rendering + navigation hints: `crates/ftui-demo-showcase/src/chrome.rs:595`
- status toggle strip + hit regions: `crates/ftui-demo-showcase/src/chrome.rs:636`
- status hit registration: `crates/ftui-demo-showcase/src/chrome.rs:962`
- help overlay hint builder (global + screen bindings): `crates/ftui-demo-showcase/src/chrome.rs:1109`
- help includes global `Ctrl+T` hint: `crates/ftui-demo-showcase/src/chrome.rs:1142`
- app-level handoff of screen keybindings: `crates/ftui-demo-showcase/src/app.rs:4058`

## 14. Search Excellence Contract (Capability: Search)

### 14.1 Search-As-You-Type Core

Shakespeare and Code Explorer both enforce immediate search updates with a minimum query threshold:

- Shakespeare `perform_search` + min length 2: `crates/ftui-demo-showcase/src/screens/shakespeare.rs:217`
- Shakespeare live update on keystroke: `crates/ftui-demo-showcase/src/screens/shakespeare.rs:519`
- Code Explorer `perform_search` + min length 2: `crates/ftui-demo-showcase/src/screens/code_explorer.rs:468`
- Code Explorer live update on keystroke: `crates/ftui-demo-showcase/src/screens/code_explorer.rs:811`

Log Search and Virtualized Search provide instant update models with richer modes:

- Log Search live update engine: `crates/ftui-demo-showcase/src/screens/log_search.rs:1077`
- Log Search default literal + case-insensitive config: `crates/ftui-demo-showcase/src/screens/log_search.rs:680`
- Virtualized Search fuzzy filter update + score ordering: `crates/ftui-demo-showcase/src/screens/virtualized_search.rs:795`
- Virtualized Search fuzzy matcher/scoring: `crates/ftui-demo-showcase/src/screens/virtualized_search.rs:544`

### 14.2 Focus and Navigation Semantics

Search entry/exit and match traversal are explicit and fast:

- Shakespeare `/` to enter search + `n/N`: `crates/ftui-demo-showcase/src/screens/shakespeare.rs:531`
- Shakespeare next/prev match behavior: `crates/ftui-demo-showcase/src/screens/shakespeare.rs:243`
- Code Explorer `/` focus + `n/N` + `Ctrl+G`: `crates/ftui-demo-showcase/src/screens/code_explorer.rs:822`
- Code Explorer search-mode next/prev with Enter/Tab/Arrows: `crates/ftui-demo-showcase/src/screens/code_explorer.rs:798`
- Log Search mode controls (`Ctrl+C`, `Ctrl+R`, `Ctrl+X`): `crates/ftui-demo-showcase/src/screens/log_search.rs:995`
- Virtualized Search `/` focus and auto-focus while typing from list: `crates/ftui-demo-showcase/src/screens/virtualized_search.rs:1327`
- Markdown Live Editor `Ctrl+F`, `Ctrl+N/P`: `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs:599`

### 14.3 Match Visibility and Effects

Search state is surfaced with explicit counts and visual hierarchy:

- Shakespeare match counter + animated effects: `crates/ftui-demo-showcase/src/screens/shakespeare.rs:859`
- Shakespeare per-line/current-match highlighting: `crates/ftui-demo-showcase/src/screens/shakespeare.rs:965`
- Code Explorer match counter + animated effects: `crates/ftui-demo-showcase/src/screens/code_explorer.rs:1123`
- Code Explorer current-match marker + stronger emphasis: `crates/ftui-demo-showcase/src/screens/code_explorer.rs:1235`
- Code Explorer search total in status bar: `crates/ftui-demo-showcase/src/screens/code_explorer.rs:2214`
- Log Search mode badges (`SEARCH`, `Aa/aa`, `lit/re`, ctx): `crates/ftui-demo-showcase/src/screens/log_search.rs:1107`
- Virtualized Search character-level highlight in result rows: `crates/ftui-demo-showcase/src/screens/virtualized_search.rs:1051`
- Markdown Live Editor `current/total` matches in search bar: `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs:403`

### 14.4 Contextual Search Affordances

Code Explorer demonstrates search context surfaces beyond a plain list:

- match radar panel entry point: `crates/ftui-demo-showcase/src/screens/code_explorer.rs:1907`
- density sparkline in radar: `crates/ftui-demo-showcase/src/screens/code_explorer.rs:1938`
- local match neighborhood list with active marker: `crates/ftui-demo-showcase/src/screens/code_explorer.rs:1959`

## 15. Streaming Markdown Contract (Capability: Markdown/LLM Output)

### 15.1 Full GFM Styling and Incremental Rendering

- themed GFM extensions (task lists, admonitions, math, tables): `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:578`
- stream fragment extraction: `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:670`
- streaming renderer call (`render_streaming`): `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:686`
- blinking streaming cursor: `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:688`

### 15.2 Streaming UX Controls and Observability

- variable typing speed + char-boundary safety: `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:598`
- explicit stream status and percent in title: `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:905`
- mini progress bar rendering: `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:952`
- markdown-likelihood detection panel: `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:967`
- controls (`Space`, `r`, `f`, scroll) in handler: `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:1101`
- controls surfaced in keybindings: `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:1171`

### 15.3 Streaming in Flagship Dashboard

- dashboard stream tick progression: `crates/ftui-demo-showcase/src/screens/dashboard.rs:3557`
- dashboard markdown panel status + `render_streaming`: `crates/ftui-demo-showcase/src/screens/dashboard.rs:5229`
- dashboard stream reset on commands: `crates/ftui-demo-showcase/src/screens/dashboard.rs:6114`

## 16. Dynamic Adjustable Panes Contract (Capability: Resizable Multi-Panel Layout)

Dashboard is the canonical implementation.

- per-panel hit mapping: `crates/ftui-demo-showcase/src/screens/dashboard.rs:3414`
- clamped ratio math for primary/secondary splitters: `crates/ftui-demo-showcase/src/screens/dashboard.rs:3442`
- drag update routine: `crates/ftui-demo-showcase/src/screens/dashboard.rs:3452`
- splitter handle rendering with active visual state: `crates/ftui-demo-showcase/src/screens/dashboard.rs:5620`
- layout-time splitter hit rect placement: `crates/ftui-demo-showcase/src/screens/dashboard.rs:5713`
- drag lifecycle in event loop (down/drag/up): `crates/ftui-demo-showcase/src/screens/dashboard.rs:6006`
- defensive drag cancel on keyboard interaction: `crates/ftui-demo-showcase/src/screens/dashboard.rs:6099`
- discoverability hint in footer line: `crates/ftui-demo-showcase/src/screens/dashboard.rs:5591`
- explicit keybinding entry for drag behavior: `crates/ftui-demo-showcase/src/screens/dashboard.rs:6238`

Quality tests for this capability:

- ratio update under drag: `crates/ftui-demo-showcase/src/screens/dashboard.rs:6339`
- drag state clears on mouse up variants: `crates/ftui-demo-showcase/src/screens/dashboard.rs:6376`
- drag state clears on keyboard interaction: `crates/ftui-demo-showcase/src/screens/dashboard.rs:6409`

## 17. Forms Contract (Capability: Structured Data Entry)

### 17.1 Forms and Input Screen

- mixed field types + required validators: `crates/ftui-demo-showcase/src/screens/forms_input.rs:159`
- panel focus model (form/search/password/editor): `crates/ftui-demo-showcase/src/screens/forms_input.rs:34`
- status line with progress/error/undo telemetry: `crates/ftui-demo-showcase/src/screens/forms_input.rs:362`
- touched/dirty-aware validation filtering: `crates/ftui-demo-showcase/src/screens/forms_input.rs:430`
- summary badges (`READY`, `NEEDS ATTN`, etc.): `crates/ftui-demo-showcase/src/screens/forms_input.rs:506`
- undo/redo snapshots + history stack: `crates/ftui-demo-showcase/src/screens/forms_input.rs:560`
- undo/redo operations: `crates/ftui-demo-showcase/src/screens/forms_input.rs:693`
- undo history panel rendering: `crates/ftui-demo-showcase/src/screens/forms_input.rs:721`
- full keybinding contract surfaced: `crates/ftui-demo-showcase/src/screens/forms_input.rs:1116`

### 17.2 Form Validation Screen

- real-time/on-submit mode model: `crates/ftui-demo-showcase/src/screens/form_validation.rs:294`
- mode toggle behavior and transitions: `crates/ftui-demo-showcase/src/screens/form_validation.rs:343`
- submit pipeline + success/error toasts: `crates/ftui-demo-showcase/src/screens/form_validation.rs:309`
- explicit error summary pane: `crates/ftui-demo-showcase/src/screens/form_validation.rs:361`
- keybinding discoverability for validation actions: `crates/ftui-demo-showcase/src/screens/form_validation.rs:645`

## 18. Graceful Resizing and Tight-Space Behavior

When terminal space is constrained, screens should still present sensible output.

Reference patterns:

- explicit tiered layouts (`large` / `medium` / `tiny`): `crates/ftui-demo-showcase/src/screens/dashboard.rs:6174`
- tiny fallback renderer path: `crates/ftui-demo-showcase/src/screens/dashboard.rs:5813`
- minimum-size fallback message (Shakespeare): `crates/ftui-demo-showcase/src/screens/shakespeare.rs:613`
- minimum-size fallback message (Code Explorer): `crates/ftui-demo-showcase/src/screens/code_explorer.rs:892`
- area-gated subpanels (forms header/footer): `crates/ftui-demo-showcase/src/screens/forms_input.rs:779`
- area-gated undo panel suppression: `crates/ftui-demo-showcase/src/screens/forms_input.rs:722`
- empty-area early return guards (markdown screen): `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:1128`

Verification examples:

- dashboard empty-area no-panic case: `crates/ftui-demo-showcase/src/screens/dashboard.rs:6581`
- dashboard threshold tests: `crates/ftui-demo-showcase/src/screens/dashboard.rs:6586`
- form validation renders at small size: `crates/ftui-demo-showcase/src/screens/form_validation.rs:739`

## 19. Visual Signal Density Contract (Capability: Data-Rich or Showcase Surfaces)

When a screen is intended to be a flagship or data-dense experience, use rich text effects and
graphical indicators as first-class information design tools.

Text-effects references:

- Shakespeare search/status effects (`AnimatedGradient`, `Glow`, `Reveal`): `crates/ftui-demo-showcase/src/screens/shakespeare.rs:873`
- Shakespeare status wave for active match context: `crates/ftui-demo-showcase/src/screens/shakespeare.rs:1653`
- Code Explorer match banner effects: `crates/ftui-demo-showcase/src/screens/code_explorer.rs:1137`
- Code Explorer status effects when matches exist: `crates/ftui-demo-showcase/src/screens/code_explorer.rs:2224`
- Dashboard effect catalog and effect builder: `crates/ftui-demo-showcase/src/screens/dashboard.rs:3049`
- Dashboard animated header treatment: `crates/ftui-demo-showcase/src/screens/dashboard.rs:3763`

Graphical-indicator references:

- Dashboard chart orchestrator + mode switching: `crates/ftui-demo-showcase/src/screens/dashboard.rs:3841`
- Dashboard graceful fallback to minimal sparkline under height pressure: `crates/ftui-demo-showcase/src/screens/dashboard.rs:3910`
- Dashboard labeled sparklines for CPU/MEM/NET metrics: `crates/ftui-demo-showcase/src/screens/dashboard.rs:3938`
- Dashboard tiny-layout sparklines still preserve metrics signal: `crates/ftui-demo-showcase/src/screens/dashboard.rs:5856`
- Dedicated Data Viz screen sparkline panel: `crates/ftui-demo-showcase/src/screens/data_viz.rs:113`
- Dedicated Data Viz bar/line chart panels: `crates/ftui-demo-showcase/src/screens/data_viz.rs:216`

Practical reading:

- Do not add effects as decoration-only noise.
- Prefer effects that reinforce state transitions, search relevance, or status urgency.
- Keep reduced-space and reduced-motion behavior sane (fallback to readable plain signals).

## 20. Multi-Section Delineation Contract (Capability: Section-Dense Screens)

For screens with many sections/panels, visual segmentation is mandatory:

- each major section should have a bordered container, typically rounded borders,
- border + accent color should communicate semantic role/focus/state,
- adjacent sections should be visually distinguishable without relying only on text labels.

References:

- Dashboard section containers (`Rounded` + semantic panel accent): `crates/ftui-demo-showcase/src/screens/dashboard.rs:3847`
- Dashboard semantic border style by focused panel: `crates/ftui-demo-showcase/src/screens/dashboard.rs:3852`
- Forms section containers (`Rounded`): `crates/ftui-demo-showcase/src/screens/forms_input.rs:764`
- Forms semantic focus accent handling: `crates/ftui-demo-showcase/src/screens/forms_input.rs:760`
- Data Viz panel containers with semantic accents: `crates/ftui-demo-showcase/src/screens/data_viz.rs:119`

## 21. Color-System Discipline (Always)

Color combinations should be intentional and theme-driven:

- use neutrals for large regions/chrome surfaces,
- use brighter accents for highlights, focus, and semantic events,
- choose accents from the curated theme set to keep contrast/complement coherence.
- verify visual coherence across theme rotation (`Cyberpunk Aurora`, `Darcula`, `Lumen Light`, `Nordic Frost`) and accessibility `High Contrast`.

References:

- `crates/ftui-demo-showcase/src/app.rs:3805`
- `crates/ftui-extras/src/theme.rs:26`
- `crates/ftui-extras/src/theme.rs:49`
- screen accent palette map: `crates/ftui-demo-showcase/src/theme.rs:260`
- neutral tab surface style: `crates/ftui-demo-showcase/src/theme.rs:723`
- neutral status surface style: `crates/ftui-demo-showcase/src/theme.rs:736`
- focus-vs-unfocused panel border rule: `crates/ftui-demo-showcase/src/theme.rs:779`
- contrast guardrail tests: `crates/ftui-demo-showcase/src/theme.rs:1309`
- screen accent WCAG checks: `crates/ftui-demo-showcase/src/theme.rs:1459`

## 22. Drag-and-Drop Contract (Capability: Reorderable/Moveable Items)

Three-phase drag state machine is the canonical pattern:

1. **Down** (arm): Record source item, sync keyboard focus, initiate drag state
2. **Drag** (update): Track cursor position, update hover target column/row
3. **Up** (commit): Move item if target differs from source, clear drag state

Mouse drag references:

- kanban drag state machine: `crates/ftui-demo-showcase/src/screens/kanban_board.rs:321`
- kanban column hit-testing: `crates/ftui-demo-showcase/src/screens/kanban_board.rs:284`
- kanban card hit-testing: `crates/ftui-demo-showcase/src/screens/kanban_board.rs:947`

Keyboard drag via `KeyboardDragManager`:

- keyboard drag handler: `crates/ftui-demo-showcase/src/screens/drag_drop.rs:358`
- drop target builder: `crates/ftui-demo-showcase/src/screens/drag_drop.rs:446`
- drag mode switching (sortable/cross-container/keyboard): `crates/ftui-demo-showcase/src/screens/drag_drop.rs:501`

Visual feedback layers:

- drag source rendered dimmed/ghost: `crates/ftui-demo-showcase/src/screens/kanban_board.rs:476`
- drop target highlighted with success color: `crates/ftui-demo-showcase/src/screens/kanban_board.rs:464`
- drop preview hint text: `crates/ftui-demo-showcase/src/screens/kanban_board.rs:464`
- keyboard focus uses heavy border: `crates/ftui-demo-showcase/src/screens/kanban_board.rs:383`

Undo/redo for drag operations:

- history stack + redo stack: `crates/ftui-demo-showcase/src/screens/kanban_board.rs:668`
- redo cleared on new move: `crates/ftui-demo-showcase/src/screens/kanban_board.rs:236`

## 23. Accessibility Contract (Capability: Keyboard-Heavy or i18n Screens)

### Keyboard Navigation Parity

Every mouse interaction must have a keyboard equivalent:

- Tab/Shift-Tab panel cycling: `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:1049`
- Arrow/hjkl grid navigation: `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:1049`
- Home/End and PageUp/PageDown: `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:1049`
- Space/Enter activation: `crates/ftui-demo-showcase/src/screens/drag_drop.rs:358`

### Hover Stabilization

Use `HoverStabilizer` to prevent hover flickering from noisy mouse position:

- stabilizer initialization: `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:635`
- stabilizer update in mouse handler: `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:805`

### Text Metrics for i18n

- `display_width()` for terminal cell count (handles CJK, emoji, combining marks)
- `grapheme_count()` for extended grapheme cluster count
- `grapheme_width()` for single grapheme width (0, 1, or 2 cells)
- `truncate_with_ellipsis()` for width-safe truncation
- `wrap_text()` for word-aware wrapping

References:

- width metrics demo: `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:677`
- grapheme stress tests: `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:100`
- RTL flow direction: `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:606`
- plural forms system: `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:1064`
- grapheme inspector: `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:816`

## 24. Diagnostic and Telemetry Contract (Capability: Debugging/Inspection Surfaces)

### JSONL Structured Logging

All diagnostic screens use JSONL with structured entries:

- `DiagnosticEntry` with seq, timestamp_us, kind, coordinates, checksum: `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:173`
- `DiagnosticEventKind` enum for event classification: `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:122`
- determinism report format: `crates/ftui-demo-showcase/src/screens/determinism_lab.rs:604`
- text editor diagnostic format: `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:52`

### Telemetry Hooks

External observers without modifying core logic:

- callback-based telemetry hooks: `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:476`
- on_hit_test, on_hover_change, on_target_click, on_any_event hooks

### Deterministic Rendering Verification

- Seed-driven LCG buffer generation: `crates/ftui-demo-showcase/src/screens/determinism_lab.rs:296`
- FNV-1a 64-bit checksums: `crates/ftui-demo-showcase/src/screens/determinism_lab.rs:1301`
- Multi-strategy diff comparison (Full/DirtyRows/FullRedraw): `crates/ftui-demo-showcase/src/screens/determinism_lab.rs:510`
- Fault injection for detection testing: `crates/ftui-demo-showcase/src/screens/determinism_lab.rs:510`
- Cell-by-cell mismatch detection: `crates/ftui-demo-showcase/src/screens/determinism_lab.rs:1279`

### Bayesian Evidence Display

- Posterior parameters (mu, sigma-squared, alpha, beta): `crates/ftui-demo-showcase/src/screens/explainability_cockpit.rs:693`
- Log Bayes factor with decomposed contributions: `crates/ftui-demo-showcase/src/screens/explainability_cockpit.rs:763`
- Conformal prediction bounds and risk status: `crates/ftui-demo-showcase/src/screens/explainability_cockpit.rs:812`
- VOI gain and sampling decisions: `crates/ftui-demo-showcase/src/screens/voi_overlay.rs:140`
- Dual data source pattern (runtime snapshot + fallback): `crates/ftui-demo-showcase/src/screens/voi_overlay.rs:331`

## 25. Responsive Layout Contract (Capability: Breakpoint-Driven Layouts)

### Structured Responsive Design

- `ResponsiveLayout` builder: `crates/ftui-demo-showcase/src/screens/responsive_demo.rs:134`
- `Breakpoints::new(sm, md, lg)` custom thresholds: `crates/ftui-demo-showcase/src/screens/responsive_demo.rs:91`
- `Breakpoints::DEFAULT` standard thresholds: XS<60, SM 60-89, MD 90-119, LG 120-159, XL 160+

### Visibility and Value Switching

- `Visibility::visible_above(Breakpoint::Md)` conditional gating: `crates/ftui-demo-showcase/src/screens/responsive_demo.rs:289`
- `Responsive<T>::resolve(bp)` per-breakpoint values: `crates/ftui-demo-showcase/src/screens/responsive_demo.rs:309`

### Intrinsic Sizing

- Dynamic constraint computation at render time: `crates/ftui-demo-showcase/src/screens/intrinsic_sizing.rs:92`
- Content-aware column widths with minimum floors: `crates/ftui-demo-showcase/src/screens/intrinsic_sizing.rs:252`
- `FitContentBounded { min, max }` constraint: `crates/ftui-demo-showcase/src/screens/layout_inspector.rs:365`

### Layout Debugging

- `LayoutDebugger` + `LayoutRecord` hierarchy: `crates/ftui-demo-showcase/src/screens/layout_inspector.rs:273`
- `ConstraintOverlay` visualization: `crates/ftui-demo-showcase/src/screens/layout_inspector.rs:576`
- Overflow/underflow detection with color-coded status: `crates/ftui-demo-showcase/src/screens/layout_inspector.rs:199`
- Three-step solver visualization (Constraints -> Allocation -> Final): `crates/ftui-demo-showcase/src/screens/layout_inspector.rs:114`

## 26. Text Editing Contract (Capability: Text Editor Surfaces)

### TextArea Widget Usage

- Initialization with line numbers and soft wrap: `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs:183`
- Cursor tracking via `TextArea::cursor()` returning `CursorPosition`: `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:1542`
- Selection via `TextArea::selected_text()` and `select_right()`: `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs:296`

### Search and Replace

- `search_ascii_case_insensitive()` for byte-range results: `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:868`
- Single replace by byte-range slicing: `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:997`
- Replace-all in reverse order to preserve offsets: `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:997`
- Search recomputation on every keystroke: `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs:296`

### Live Preview

- 50/50 split editor + preview: `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs:671`
- `MarkdownRenderer` with syntax highlighting: `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs:280`
- Diff mode for width diagnostics: `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs:463`

## 27. Configuration Persistence Contract (Capability: User Config/Presets)

### Snapshot Serialization

- Serde-derivable snapshot types: `crates/ftui-demo-showcase/src/screens/widget_builder.rs:134`
- JSON export with structured metadata: `crates/ftui-demo-showcase/src/screens/widget_builder.rs:421`
- Import with validation: `crates/ftui-demo-showcase/src/screens/table_theme_gallery.rs:478`

### Preset System

- Built-in (read-only) presets: `crates/ftui-demo-showcase/src/screens/widget_builder.rs:226`
- User-saveable custom presets: `crates/ftui-demo-showcase/src/screens/table_theme_gallery.rs:216`
- Theme override chain (base -> property overrides -> state): `crates/ftui-demo-showcase/src/screens/table_theme_gallery.rs:410`

### Regression Detection

- FNV-1a 64-bit hash for configuration snapshots: `crates/ftui-demo-showcase/src/screens/widget_builder.rs:934`
- Deterministic logging with props_hash: `crates/ftui-demo-showcase/src/screens/widget_builder.rs:421`

## 28. Hyperlink Contract (Capability: OSC-8 Terminal Links)

### Link Registration

- `frame.register_link(url)` returns link_id: `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs:290`
- `frame.register_hit(rect, hit_id, HitRegion::Link, link_id)` maps coordinates: `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs:290`
- OSC-8 escape sequences: `\x1b]8;;{url}\x1b\\` open, `\x1b]8;;\x1b\\` close: `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs:120`

### Link Interaction

- Keyboard: Up/Down focus cycling, Enter/Space activation: `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs:81`
- Mouse: hover detection + click activation: `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs:205`
- Visual: focused (inverted), hovered (surface bg), default (link color): `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs:310`

## 29. Systematic Screen-by-Screen Inventory (All Registry Entries)

This section is a strict registry-order pass over every screen listed in `SCREEN_REGISTRY`.

| # | Screen | What It Demonstrates | High-Value Interaction Contract | Primary References |
|---|--------|----------------------|----------------------------------|--------------------|
| 1 | Guided Tour | Data-driven storyboard over registry metadata, tour-step callouts, deterministic autoplay with logging/evidence hooks. | Landing controls (step select, speed, start) plus active-tour controls (pause, prev/next, speed, exit). | `crates/ftui-demo-showcase/src/app.rs:4061`, `crates/ftui-demo-showcase/src/app.rs:4144`, `crates/ftui-demo-showcase/src/tour.rs:123`, `crates/ftui-demo-showcase/src/chrome.rs:169` |
| 2 | Dashboard | Canonical flagship composition: animated title/text effects, streaming markdown, charts, code preview, live activity, pane linking. | Single-letter power keys (`r/c/e/m/g/t`), mouse-hover/click routing, wheel feed scroll, drag divider for pane resize. | `crates/ftui-demo-showcase/src/screens/dashboard.rs:6003`, `crates/ftui-demo-showcase/src/screens/dashboard.rs:6199`, `crates/ftui-demo-showcase/src/screens/dashboard.rs:5620` |
| 3 | Shakespeare | Search-first text UX over large corpus with virtualized navigation and strong hit visibility hierarchy. | Search-as-you-type (`/`), fast traversal (`Enter`, arrows, `n/N`), mode/view toggles, pane focus with mouse. | `crates/ftui-demo-showcase/src/screens/shakespeare.rs:439`, `crates/ftui-demo-showcase/src/screens/shakespeare.rs:733`, `crates/ftui-demo-showcase/src/screens/shakespeare.rs:859` |
| 4 | Code Explorer | SQLite code navigation with syntax highlighting, hotspots, and context-rich search affordances (including radar/density). | `Ctrl+G` goto-line, hotspot jumping (`[`/`]`), feature spotlight cycling, search traversal and pane focus by mouse. | `crates/ftui-demo-showcase/src/screens/code_explorer.rs:720`, `crates/ftui-demo-showcase/src/screens/code_explorer.rs:971`, `crates/ftui-demo-showcase/src/screens/code_explorer.rs:1907` |
| 5 | Widget Gallery | Broad catalog of widget primitives/composites arranged as navigable sections and tabs. | Section stepping via `j/k` or arrows and click-to-switch tab workflow. | `crates/ftui-demo-showcase/src/screens/widget_gallery.rs:189`, `crates/ftui-demo-showcase/src/screens/widget_gallery.rs:316` |
| 6 | Layout Lab | Constraint + pane-layout laboratory with solver controls, pane timeline, and multi-gesture pane interactions. | Dense keyboard control surface (`1-5`, alignment/gap/margin/padding), undo/redo/replay, mouse/scroll/shift-click cluster operations. | `crates/ftui-demo-showcase/src/screens/layout_lab.rs:354`, `crates/ftui-demo-showcase/src/screens/layout_lab.rs:514` |
| 7 | Forms & Input | Mixed control types (text, checkbox, radio, select, number), panel focus model, text editing, and undo-aware form workflow. | Panel-switch keys, form traversal, submit/cancel semantics, undo/redo/historical inspection, click-to-focus. | `crates/ftui-demo-showcase/src/screens/forms_input.rs:911`, `crates/ftui-demo-showcase/src/screens/forms_input.rs:1116`, `crates/ftui-demo-showcase/src/screens/forms_input.rs:721` |
| 8 | Data Viz | High-density metrics presentation with sparkline/bar/line/chart modes and canvas rendering. | Panel switching, bar-direction toggles, chart reset, directional navigation and animated metric evolution. | `crates/ftui-demo-showcase/src/screens/data_viz.rs:719`, `crates/ftui-demo-showcase/src/screens/data_viz.rs:899` |
| 9 | File Browser | Navigable file tree + preview workflow with syntax rendering and human-readable metadata surfaces. | Panel switching, tree/list navigation, page stepping, hidden-file toggles, focused browsing rhythm. | `crates/ftui-demo-showcase/src/screens/file_browser.rs:777`, `crates/ftui-demo-showcase/src/screens/file_browser.rs:944` |
| 10 | Advanced | Composite advanced widgets (diagnostics/timers/spinners/macro-like controls) in panelized lab form. | Direct panel focus keys, pause/resume/reset controls, macro controls, click/scroll panel focus and cycling. | `crates/ftui-demo-showcase/src/screens/advanced_features.rs:673`, `crates/ftui-demo-showcase/src/screens/advanced_features.rs:809` |
| 11 | Table Theme Gallery | Theme preset gallery for table styling across border/zebra/header/highlight dimensions. | Preset selection via arrows/tab/home/end; style-parameter cycles (`V/H/Z/B/L`) plus import/export/save/reset loop. | `crates/ftui-demo-showcase/src/screens/table_theme_gallery.rs:802`, `crates/ftui-demo-showcase/src/screens/table_theme_gallery.rs:925` |
| 12 | Terminal Capabilities | Capability matrix/evidence/simulation views for terminal compatibility reasoning and policy checks. | View cycling, capability-row selection, profile simulation (`P` or `0-5`), export and mouse/scroll navigation. | `crates/ftui-demo-showcase/src/screens/terminal_capabilities.rs:1605`, `crates/ftui-demo-showcase/src/screens/terminal_capabilities.rs:1845` |
| 13 | Macro Recorder | Input event recording/playback with timeline + scenario focus and deterministic replay controls. | Record/play/pause, focus routing, timeline jump/page controls, loop/speed controls, click-to-focus panel selection. | `crates/ftui-demo-showcase/src/screens/macro_recorder.rs:1120`, `crates/ftui-demo-showcase/src/screens/macro_recorder.rs:1178` |
| 14 | Performance | Virtualized large-list stress screen focused on scroll throughput and stable list interaction. | Dense list navigation (`j/k`, page, `g/G`) and pointer+wheel list selection. | `crates/ftui-demo-showcase/src/screens/performance.rs:257`, `crates/ftui-demo-showcase/src/screens/performance.rs:346` |
| 15 | Markdown (Rich Text) | Full GFM rendering + streaming/fragment progression + typography features and panelized markdown observability. | Scroll by focused panel, stream control (`Space/r/f`), mode tweaks (`w/a`), mouse pane focus and stream scrolling. | `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:1008`, `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:1171`, `crates/ftui-demo-showcase/src/screens/markdown_rich_text.rs:676` |
| 16 | Mermaid Showcase (feature-gated) | Interactive Mermaid diagram renderer with tiering, viewport overrides, diagnostics and control plane. | Large keymap for layout/render/style/link/wrap/tier/zoom/inspect/search plus click/wheel behavior. | `crates/ftui-demo-showcase/src/screens/mermaid_showcase.rs:4184`, `crates/ftui-demo-showcase/src/screens/mermaid_showcase.rs:4394` |
| 17 | Mermaid Mega Showcase (feature-gated) | Over-the-top Mermaid lab with generation knobs, split-panel diagnostics, node selection and comparison modes. | Expanded multi-domain keymap (generation/perf/layout/view/diagnostics/compare/search/navigation) with diagram click semantics. | `crates/ftui-demo-showcase/src/screens/mermaid_mega_showcase.rs:3934`, `crates/ftui-demo-showcase/src/screens/mermaid_mega_showcase.rs:4022` |
| 18 | Visual Effects | High-performance FX playground with canvas and text-effects modes, deterministic/fallback-aware rendering paths. | Mode/effect/tab/easing/option controls with mixed keyboard/mouse behaviors and quality toggles. | `crates/ftui-demo-showcase/src/screens/visual_effects.rs:4033`, `crates/ftui-demo-showcase/src/screens/visual_effects.rs:4618` |
| 19 | Responsive Layout | Demonstrates responsive layout primitives (breakpoints, visibility rules, responsive values). | Custom breakpoint toggles, simulated width controls (`+/-`), click/wheel-based width/behavior adjustments. | `crates/ftui-demo-showcase/src/screens/responsive_demo.rs:334`, `crates/ftui-demo-showcase/src/screens/responsive_demo.rs:427` |
| 20 | Log Search | Streaming log viewer with live search/filter, mode badges, contextual search toggles and stream pausing. | `/` search, `f` filter, `n/N` traversal, regex/case/context toggles (`Ctrl+R/C/X`), pause/resume and wheel navigation. | `crates/ftui-demo-showcase/src/screens/log_search.rs:1194`, `crates/ftui-demo-showcase/src/screens/log_search.rs:1275` |
| 21 | Notifications | Toast queue lifecycle demo including severity/action variants and dismissal paths. | One-key notification injection by severity, dismiss-all control, click/wheel-triggered queue interactions. | `crates/ftui-demo-showcase/src/screens/notifications.rs:223`, `crates/ftui-demo-showcase/src/screens/notifications.rs:270` |
| 22 | Action Timeline | Deterministic ring-buffer event stream with filter stack and expandable detail panel. | Follow/filter toggles, timeline navigation (row/page/home/end), click/scroll event selection and inspection. | `crates/ftui-demo-showcase/src/screens/action_timeline.rs:760`, `crates/ftui-demo-showcase/src/screens/action_timeline.rs:903` |
| 23 | Intrinsic Sizing | Content-aware layout behavior across scenarios (sidebar collapse, flexible cards, auto-width columns). | Scenario and simulated-width controls with click/scroll scenario switching. | `crates/ftui-demo-showcase/src/screens/intrinsic_sizing.rs:447`, `crates/ftui-demo-showcase/src/screens/intrinsic_sizing.rs:561` |
| 24 | Layout Inspector | Solver and rect introspection surface with overlays/tree panels and step-wise replay of layout progression. | Scenario stepping, per-step traversal, overlay/tree toggles, click-targeted scenario/step changes, scroll cycling. | `crates/ftui-demo-showcase/src/screens/layout_inspector.rs:446`, `crates/ftui-demo-showcase/src/screens/layout_inspector.rs:602` |
| 25 | Advanced Text Editor | Multi-line editor with search/replace, selection metrics, and history-aware editing flow. | `Ctrl+F/H/G`, replace-all and focus cycling, undo/redo/history toggles, mode exit (`Esc`) and panel navigation. | `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:1290`, `crates/ftui-demo-showcase/src/screens/advanced_text_editor.rs:1600` |
| 26 | Mouse Playground | Hit-testing and pointer telemetry lab with jitter stabilization and overlay diagnostics. | Keyboard fallback for all major target navigation plus overlay/jitter/log controls and click-space parity. | `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:1016`, `crates/ftui-demo-showcase/src/screens/mouse_playground.rs:1291` |
| 27 | Form Validation | Validation-focused workflow with real-time/on-submit mode switching, error summary, and correction loop. | Field traversal, mode toggles, error injection/reset/clear, submit semantics, click/scroll field navigation. | `crates/ftui-demo-showcase/src/screens/form_validation.rs:505`, `crates/ftui-demo-showcase/src/screens/form_validation.rs:645` |
| 28 | Virtualized Search | Large-list fuzzy search with incremental filter updates and scored highlighting. | Slash-to-focus search, clear/unfocus (`Esc`), list navigation across item/page/extremes, click/wheel parity. | `crates/ftui-demo-showcase/src/screens/virtualized_search.rs:1238`, `crates/ftui-demo-showcase/src/screens/virtualized_search.rs:1448` |
| 29 | Async Tasks | Job queue observability with scheduling policy controls, fairness/aging toggles, progress, and retries. | Spawn/cancel/retry controls, scheduler/fairness toggles, row/page/home/end navigation, click/wheel selection. | `crates/ftui-demo-showcase/src/screens/async_tasks.rs:2000`, `crates/ftui-demo-showcase/src/screens/async_tasks.rs:2140` |
| 30 | Theme Studio | Token/preset inspection, contrast checks, and theme export pathways. | Navigation + apply controls (`Enter`), explicit `Ctrl+T` cycling, export paths (`e`/`E`), pointer-driven preset application. | `crates/ftui-demo-showcase/src/screens/theme_studio.rs:1106`, `crates/ftui-demo-showcase/src/screens/theme_studio.rs:1331` |
| 31 | Time-Travel Studio | Frame recording/scrubbing/comparison and integrity diagnostics for replay-based debugging. | Play/pause, frame stepping, markers, compare A/B controls, heatmap/diagnostic/export controls, timeline drag/click. | `crates/ftui-demo-showcase/src/screens/snapshot_player.rs:1614`, `crates/ftui-demo-showcase/src/screens/snapshot_player.rs:1696` |
| 32 | Performance Challenge | Degradation-tier stress harness with runtime metrics and recovery/cooldown semantics. | Reset/stress/cooldown/pause, sparkline mode switch, forced tier keys (`1-4`) for reproducible perf drills. | `crates/ftui-demo-showcase/src/screens/performance_hud.rs:1108`, `crates/ftui-demo-showcase/src/screens/performance_hud.rs:1227` |
| 33 | Explainability Cockpit | Unified evidence ledger for diff/resize/budget decisions and timeline inspection. | Refresh/clear/read controls, panel focus keys (`1-4`), timeline scrolling/navigation for postmortem workflow. | `crates/ftui-demo-showcase/src/screens/explainability_cockpit.rs:536`, `crates/ftui-demo-showcase/src/screens/explainability_cockpit.rs:623` |
| 34 | i18n Stress Lab | Locale, directionality, grapheme, pluralization and stress-edge-case validation surface. | Locale/panel/sample switching, RTL/LTR toggles, grapheme-cursor controls, export/report actions, click/wheel controls. | `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:930`, `crates/ftui-demo-showcase/src/screens/i18n_demo.rs:1005` |
| 35 | VOI Overlay | Value-of-information and ledger overlay view tuned for decision confidence/inspection. | Reset/toggle detail, ledger navigation, section cycling for focused VOI reading. | `crates/ftui-demo-showcase/src/screens/voi_overlay.rs:242`, `crates/ftui-demo-showcase/src/screens/voi_overlay.rs:374` |
| 36 | Inline Mode | Scrollback-preserving inline-mode narrative with compare mode and anchor-rate controls. | Pause/compare/anchor/height/rate toggles, stress burst, click/wheel interactions while preserving inline semantics. | `crates/ftui-demo-showcase/src/screens/inline_mode_story.rs:375`, `crates/ftui-demo-showcase/src/screens/inline_mode_story.rs:493` |
| 37 | Accessibility | A11y control panel for high-contrast/reduced-motion/large-text and overlay toggles. | One-key accessibility toggles with click parity and base-theme cycling support. | `crates/ftui-demo-showcase/src/screens/accessibility_panel.rs:433`, `crates/ftui-demo-showcase/src/screens/accessibility_panel.rs:482` |
| 38 | Widget Builder | Interactive sandbox to assemble/preset/toggle/export widget configurations deterministically. | Widget/preset navigation, property toggles, value adjustment, save/export/reset cycle, click/right-click behavior. | `crates/ftui-demo-showcase/src/screens/widget_builder.rs:706`, `crates/ftui-demo-showcase/src/screens/widget_builder.rs:852` |
| 39 | Command Palette Evidence Lab | Explainable ranking lab for command palette/hint scoring and match-mode analysis. | Match-mode toggles, bench mode, result navigation/execution, click/wheel parity for ranked action selection. | `crates/ftui-demo-showcase/src/screens/command_palette_lab.rs:483`, `crates/ftui-demo-showcase/src/screens/command_palette_lab.rs:595` |
| 40 | Determinism Lab | Diff-strategy equivalence validation with checksum timelines, fault injection and export/reporting. | Strategy selection, seed control, pause/fault toggles, run/all-run/export/reset, click-driven scenario/run inspection. | `crates/ftui-demo-showcase/src/screens/determinism_lab.rs:1105`, `crates/ftui-demo-showcase/src/screens/determinism_lab.rs:1208` |
| 41 | Hyperlink Playground | OSC-8 link registration + hit regions + keyboard parity for link activation. | Link focus cycling, activation, copy URL flow and pointer hit-testing integration. | `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs:458`, `crates/ftui-demo-showcase/src/screens/hyperlink_playground.rs:491` |
| 42 | Kanban Board | Three-column task board with drag-drop and deterministic keyboard movement history. | Column/card navigation, card movement, undo/redo and pointer drag parity. | `crates/ftui-demo-showcase/src/screens/kanban_board.rs:559`, `crates/ftui-demo-showcase/src/screens/kanban_board.rs:631` |
| 43 | Live Markdown Editor | Split editor+preview workflow with search focus and diff inspection mode. | Search focus/navigation, diff toggle, preview scroll controls, pane focus via mouse and edit/preview mode balance. | `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs:532`, `crates/ftui-demo-showcase/src/screens/markdown_live_editor.rs:699` |
| 44 | Drag & Drop Lab | Multi-mode drag/drop demo (sortable, cross-container, keyboard drag accessibility). | Mode-switch keymap and per-mode controls (move/transfer/pickup/drop/cancel) with click/scroll list navigation. | `crates/ftui-demo-showcase/src/screens/drag_drop.rs:501`, `crates/ftui-demo-showcase/src/screens/drag_drop.rs:620` |
| 45 | Quake E1M1 (Easter Egg) | Retro 3D renderer demo with quality/perf switching and gameplay-like controls. | Movement/look/jump/fire controls, quality cycling and reset path. | `crates/ftui-demo-showcase/src/screens/quake.rs:807`, `crates/ftui-demo-showcase/src/screens/quake.rs:916` |

Coverage verification sources:

- full registry order + metadata: `crates/ftui-demo-showcase/src/screens/mod.rs:122`
- per-screen keybinding fanout in app shell: `crates/ftui-demo-showcase/src/app.rs:4058`
