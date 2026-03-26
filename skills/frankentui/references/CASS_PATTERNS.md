# Cass Patterns for FrankenTUI UI Quality

This file captures historical prompt patterns used to push FrankenTUI from weak UI surfaces to showcase-level quality.

## 1. Repro Commands

```bash
cass status --json && cass index --json

cass search "mind-blowing dashboard" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "pathetic under construction placeholder" --workspace /data/projects/frankentui --json --fields minimal --limit 20
cass search "visual polish" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "beads_viewer" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "search as you type" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "Ctrl+T cycle theme" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "streaming markdown" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "drag divider resize panes" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "forms validation" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "rounded borders semantic colors" --workspace /data/projects/frankentui --json --fields minimal --limit 50
```

Inspect candidate hits:

```bash
cass view /path/to/session.jsonl -n <line> -C 20
```

## 2. High-Signal Historical Hits

### Pattern A: Replace Placeholder Screen with Flagship Dashboard

Source:

- `/home/ubuntu/.claude/projects/-data-projects-frankentui/636d87b6-e82e-40c1-92cf-2995341901d7/subagents/agent-a9d065a.jsonl:1`

Observed ask pattern:

- explicitly rejects placeholder quality
- asks for "mind-blowing" first screen
- demands dense multi-panel composition
- requires live effects + charts + markdown + code + theme/system info
- enforces reflow from tiny to large terminals

### Pattern B: "Everything, Everywhere, All at Once" Plan Framing

Source:

- `/home/ubuntu/.claude/projects/-data-projects-frankentui/2a2428ec-9bc8-4f2e-9ade-24bf62d09921.jsonl:4`

Observed ask pattern:

- convert vague "make it better" into explicit layout tiers
- define exact panel assignments and feature coverage
- include build/lint/test/snapshot verification plan

### Pattern C: Borrow Visual Polish from Other High-Quality TUI Projects

Source:

- `/home/ubuntu/.claude/projects/-data-projects-frankentui/154fc5bf-7e6f-436b-9237-d95b26d06135/subagents/agent-a76ea13.jsonl:1`

Observed ask pattern:

- investigate external TUI style baseline (`/dp/beads_viewer`)
- extract concrete visual techniques
- port polish techniques back into showcase screens

### Pattern D: Capability-Gated Requirement Framing

Observed ask pattern:

- explicitly separates always-on requirements from capability-specific ones
- insists that irrelevant capabilities must not be forced into every screen
- demands strict quality bars for capabilities that do exist (search, markdown, forms, panes)

### Pattern E: Discoverability + Semantic Segmentation Emphasis

Observed ask pattern:

- requires bottom-visible shortcut guidance and help overlay coverage
- demands section-dense screens use clear bordered delineation
- demands semantic color separation (meaningful accents, not random color noise)
- demands explicit support for `Ctrl+T` theme rotation across named themes (Cyberpunk Aurora, Darcula, Lumen Light, Nordic Frost, High Contrast)
- encourages liberal text effects and graphical indicators for high-signal data

## 3. Distilled Prompt Formula

When you need showcase-level UI outcomes, prompts that worked repeatedly share this shape:

1. Name the current weak state explicitly.
2. Name the target emotional bar (flagship/demo-worthy).
3. Split requirements into always-on vs capability-gated expectations.
4. Enumerate concrete capabilities that must appear in the target screen.
5. Require responsive tiers with exact size thresholds and tiny-space behavior.
6. Require keyboard + mouse interaction plus discoverability hints.
7. Require section delineation (rounded borders + semantic color accents) when many panes exist.
8. Require verification commands and tests.

## 4. Anti-Pattern Formula

Weak prompts that lead to mediocre output usually:

- ask for "make this nicer" without required feature coverage,
- force every capability into every screen (instead of capability-gating),
- skip responsive constraints,
- skip interaction requirements,
- skip section delineation and semantic color strategy,
- skip verification gates.

## 5. Operationalized Requirements for This Skill

Derived from the hits above, this skill treats the following as default requirements for showcase surfaces:

- no placeholder-only views,
- multi-panel responsive composition,
- integrated visual + data + textual panels,
- explicit interaction mapping (mouse + keyboard),
- stable theming and accessibility controls,
- deterministic and testable behavior for animated subsystems.

Capability-gated requirements:

- search quality contract when search exists,
- streaming markdown contract when markdown output exists,
- pane resize contract when dynamic split panes exist,
- forms/validation contract when structured input exists,
- rounded bordered segmentation + semantic color separation when many sections exist,
- liberal but purposeful text effects and metric indicators for data-rich showcase surfaces.

## 6. Additional High-Signal Patterns

### Pattern F: Drag-and-Drop with Keyboard Accessibility

Observed ask pattern:

- requires three-phase drag state machine (Down/Drag/Up)
- demands full keyboard accessibility via `KeyboardDragManager`
- requires screen reader announcements during drag
- demands visual feedback: ghost source + highlighted drop target
- requires undo/redo for drag operations

Search queries:

```bash
cass search "keyboard drag" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "drag drop" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "kanban" --workspace /data/projects/frankentui --json --fields minimal --limit 50
```

### Pattern G: Internationalization and Grapheme Correctness

Observed ask pattern:

- requires `display_width()` for all layout width calculations
- demands CJK, emoji, combining marks, ZWJ, and flag emoji handling
- requires RTL layout via `Flex::flow_direction()`
- demands multi-locale `StringCatalog` with plural forms
- requires stress testing with grapheme width verification

Search queries:

```bash
cass search "display_width" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "grapheme" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "RTL" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "i18n" --workspace /data/projects/frankentui --json --fields minimal --limit 50
```

### Pattern H: Deterministic Rendering Verification

Observed ask pattern:

- requires seed-driven pseudo-random buffer generation
- demands FNV-1a checksums for buffer equivalence verification
- requires multi-strategy diff comparison (Full vs DirtyRows vs FullRedraw)
- demands JSONL export for CI/CD integration
- requires fault injection to test detection logic

Search queries:

```bash
cass search "determinism" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "checksum" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "FNV" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "BufferDiff" --workspace /data/projects/frankentui --json --fields minimal --limit 50
```

### Pattern I: Responsive Layout with Breakpoints

Observed ask pattern:

- requires `ResponsiveLayout` with formal `Breakpoint` tiers
- demands `Visibility::visible_above()` for component gating
- requires `Responsive<T>` for per-breakpoint value switching
- demands intrinsic sizing with minimum floors for content-aware layout
- requires `LayoutDebugger` for constraint solver visualization

Search queries:

```bash
cass search "ResponsiveLayout" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "Breakpoint" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "intrinsic sizing" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "LayoutDebugger" --workspace /data/projects/frankentui --json --fields minimal --limit 50
```

### Pattern J: Bayesian Evidence and Runtime Introspection

Observed ask pattern:

- requires evidence cockpit for viewing diff strategy decisions
- demands posterior display (mean, variance, alpha, beta)
- requires log Bayes factor visualization with decomposed contributions
- demands conformal prediction bounds and risk status
- requires dual data source pattern (runtime snapshot + fallback)

Search queries:

```bash
cass search "evidence" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "posterior" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "VOI" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "Bayes" --workspace /data/projects/frankentui --json --fields minimal --limit 50
```

### Pattern K: Text Editing with Search/Replace

Observed ask pattern:

- requires `TextArea` with line numbers, soft wrap, and cursor tracking
- demands byte-range search with `search_ascii_case_insensitive()`
- requires replace and replace-all with reverse-order substitution
- demands undo/redo with bounded history
- requires split-pane live preview for markdown editors

Search queries:

```bash
cass search "TextArea" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "search replace" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "markdown live" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "text editor" --workspace /data/projects/frankentui --json --fields minimal --limit 50
```

### Pattern L: Configuration Persistence and Presets

Observed ask pattern:

- requires serde snapshot types for JSON round-trip
- demands built-in (read-only) + user-saveable custom presets
- requires theme override chains (base -> overrides -> state)
- demands FNV-1a hashing for regression detection
- requires import validation before applying external data

Search queries:

```bash
cass search "preset" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "export JSON" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "widget builder" --workspace /data/projects/frankentui --json --fields minimal --limit 50
cass search "table theme" --workspace /data/projects/frankentui --json --fields minimal --limit 50
```

## 7. Additional Useful Sessions

- `/home/ubuntu/.claude/projects/-data-projects-frankentui/51ac1233-eb71-4199-9b87-1cfc1fb077b6.jsonl`
- `/home/ubuntu/.claude/projects/-data-projects-frankentui/4b571e13-20b7-43a2-bf32-ee3cf42f247f.jsonl`
- `/home/ubuntu/.claude/projects/-data-projects-frankentui/d8396483-ef5d-4a59-b2f1-941964b17c7b.jsonl`
- `/home/ubuntu/.claude/projects/-data-projects-frankentui/971aa952-637b-40b7-aa84-2fded3559a1e.jsonl`

Use these when you need more examples of "polish escalation" prompts and outcomes.
