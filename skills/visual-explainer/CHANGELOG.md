# Changelog

## [0.4.3] - 2026-03-01

### Mermaid Zoom and Positioning Fixes
- **Fixed zoom clipping**: Replaced `transform: scale()` with CSS `zoom` property. Transform only changes visual appearance — content expanding upward/leftward goes into negative space which can't be scrolled to. Zoom changes actual layout size, so overflow scrolls normally in all directions.
- **Fixed vertical centering**: Changed `align-items: flex-start` to `align-items: center` so diagrams are centered both horizontally and vertically in their container.
- **Added initial zoom**: Complex diagrams can start at zoom > 1 (e.g., 1.4x) for better readability while keeping zoom controls functional.
- **Added min-height**: Containers now have `min-height: 400px` to prevent vertical flowcharts from compressing into unreadable thumbnails.
- Removed unnecessary `.mermaid-inner` wrapper — no longer needed with zoom-based approach.
- Updated JavaScript to use `INITIAL_ZOOM` constant for consistent reset behavior.
- Updated "Scaling Small Diagrams" section to use `zoom` instead of `transform: scale()` for consistency.

## [0.4.4] - 2026-03-02

### Hybrid Architecture Pattern
- New pattern for complex architectures (15+ elements): simple Mermaid overview (5-8 nodes) + CSS Grid cards for details
- Updated "Architecture / System Diagrams" section in SKILL.md with three-tier approach based on complexity
- Reduced max Mermaid node count from 15-20 to 10-12 in `libraries.md`
- Updated Mermaid scaling guidance to recommend hybrid pattern over scaling tricks for complex diagrams

## [0.4.2] - 2026-03-01

### Link Styling
- New "Link Styling" section in `css-patterns.md` — never rely on browser default link colors; use accent colors with sufficient contrast

## [0.4.1] - 2026-03-01

### Mermaid Layout Direction
- New "Layout Direction: TD vs LR" section in `libraries.md`
- Prefer `flowchart TD` (top-down) over `flowchart LR` (left-to-right) for complex diagrams
- LR spreads horizontally and makes labels unreadable with many nodes
- Rule: use TD for 5+ nodes or any branching; LR only for simple 3-4 node linear flows

### Documentation
- Simplified README: trimmed Usage section, consolidated Install, added Slide Deck Mode section
- Added `/generate-visual-plan` to command table

## [0.4.0] - 2026-02-28

### New Prompt Template
- `/generate-visual-plan` — generate visual implementation plans for features and extensions. Produces editorial/blueprint-style HTML pages with problem comparison panels, state machine diagrams, code snippets, edge case tables, and implementation notes. Designed for documenting feature specs before implementation.

### Prose Accent Patterns
Added patterns for use as accent elements within visual pages.

**`css-patterns.md`** — New "Prose Page Elements" section:
- Body text settings (font-size, line-height, max-width for comfortable reading)
- Lead paragraph patterns (larger size, drop cap variants)
- Pull quotes (border-left, centered with quotation mark)
- Section dividers (horizontal rule, ornamental)
- Article hero patterns (centered, editorial)
- Author byline pattern
- Prose-specific anti-patterns

**`libraries.md`** — New "Typography by Content Voice" section:
- Font recommendations by content type (literary, technical, bold, minimal)
- Special mention of Literata for screen reading

**`SKILL.md`** — New sections:
- "Prose Accent Elements" — when to use lead paragraphs, pull quotes, callouts
- "Documentation" — content-to-visual mapping (features→cards, steps→flows, APIs→tables)

### Overflow Fix: List Markers in Bordered Containers
- `css-patterns.md`: New section "List markers overlapping container borders" with three solutions
- Rule of thumb: use `list-style-position: inside` or `padding-left: 2em` for lists in bordered containers

### Mermaid Fixes
- Centering: narrow vertical flowcharts must be centered, not left-aligned
- Scaling: complex diagrams with 10+ nodes render too small — increase fontSize to 18-20px or use CSS scale transform
- Special characters: node labels starting with `/`, `\`, `(`, `{` must be quoted to avoid shape syntax conflicts
- New "Scaling Small Diagrams" section in css-patterns.md
- New "Node Label Special Characters" section in libraries.md

### Code Block Patterns
- `css-patterns.md`: New "Code Blocks" section with:
  - Basic pattern with `white-space: pre-wrap` (critical for preserving line breaks)
  - File header pattern for displaying code with filename
  - Implementation plan guidance: don't dump full files, show structure instead
- `SKILL.md`: New "Implementation Plans" section with structure guidance

## [0.3.0] - 2026-02-26

### Anti-Slop Guardrails
- Added explicit "Anti-Patterns (AI Slop)" section to SKILL.md with forbidden patterns
- Removed "Neon dashboard" and "Gradient mesh" from allowed aesthetics — they always produce generic output
- Categorized aesthetics as "Constrained" (safer) vs "Flexible" (use with caution)
- Explicit forbidden fonts: Inter, Roboto, Arial, Helvetica, system-ui as primary
- Explicit forbidden colors: indigo/violet range (`#8b5cf6`, `#7c3aed`, `#a78bfa`), cyan-magenta-pink combination
- Explicit forbidden effects: gradient text on headings, animated glowing box-shadows, emoji section headers
- Added "The Slop Test" — 7-point checklist to catch AI-generated patterns before delivery
- Strengthened typography guidance with 5 explicit good pairings to use
- Strengthened color guidance with 5 explicit good palettes to use
- Referenced `websocket-implementation-plan.html` as positive example of Blueprint aesthetic

### Template Fixes
- Replaced violet secondary colors in `mermaid-flowchart.html` with sky blue to match anti-slop guidelines
- Updated Mermaid themeVariables example in `libraries.md` to use teal/slate palette instead of violet

## [0.2.0] - 2026-02-25

### Slide Deck Mode
- New output format: magazine-quality slide deck presentations as self-contained HTML files
- 10 slide types: Title, Section Divider, Content, Split, Diagram, Dashboard, Table, Code, Quote, Full-Bleed
- SlideEngine JS: keyboard/touch/wheel navigation, progress bar, nav dots, slide counter, keyboard hints with auto-fade
- Cinematic transitions: fade + translateY + scale on slide entrance, staggered child reveals via IntersectionObserver
- 4 curated presets: Midnight Editorial, Warm Signal, Terminal Mono, Swiss Clean (each with full light/dark palette)
- Event delegation: Mermaid zoom, scrollable code/tables don't trigger slide navigation
- Responsive height breakpoints (700px, 600px, 500px) for projection and small viewports
- Typography scale 2–3× larger than scrollable pages (80–120px display, 28–48px headings, 16–24px body)
- Per-slide background variation, SVG decorative accents, compositional variety rules
- Proactive imagery: surf-cli integration for title/full-bleed backgrounds, inline sparklines, mini-charts
- New `/generate-slides` prompt template; existing prompts support `--slides` flag via SKILL.md workflow
- Unified `autoFit()` post-render function: auto-scales Mermaid SVGs, KPI values, and long blockquotes to fit their containers
- Fix Mermaid diagrams rendering tiny in slide containers (flex shrink-wrap + inline max-width)
- Fix KPI card overflow for text values (white-space + transform scale)
- Fix quote slides with long text (proportional font-size reduction)

### Files
- `references/slide-patterns.md` — slide engine CSS, all 10 type layouts, transitions, nav chrome, content density limits, presets
- `templates/slide-deck.html` — reference template demonstrating all 10 types in Midnight Editorial preset
- `prompts/generate-slides.md` — slash command for generating slide decks
- `SKILL.md` — new "Slide Deck Mode" section with slide routing, `--slides` flag detection, visual richness guidance

## [0.1.4] - 2026-02-24

- Removed Mermaid `handDrawn` mode — Rough.js hachure fills are hardcoded and render unreadable diagonal scribbles inside nodes with no user-facing override. All diagrams now use `look: 'classic'` with custom `themeVariables` for visual distinction.
- Added `package.json` for `pi install` support — installs the skill and all slash commands in one step instead of `git clone` + manual `cp`

## [0.1.3] - 2026-02-24

- Extended `classDef` color warning to also cover per-node `style` directives — both hardcode text color that breaks in the opposite color scheme
- Renamed `.node` card classes to `.ve-card` to fix CSS collision with Mermaid's internal `.node` class that broke diagram layout (PR #7)

## [0.1.2] - 2026-02-19

- Added sequence diagram syntax guidance to "Writing Valid Mermaid" — curly braces, brackets, and ampersands in message labels silently break rendering

## [0.1.1] - 2026-02-19

- Prompts no longer require the `pi-prompt-template-model` extension — each prompt now explicitly loads the skill itself
- Added "Writing Valid Mermaid" section to `libraries.md` (quoting special chars, simple IDs, max node count, arrow styles, pipe escaping)
- Fixed mobile scroll offset in `responsive-nav.md` — section headings now clear the sticky nav bar via `scroll-margin-top`
- Added video preview to README

## [0.1.0] - 2026-02-16

Initial release.

### Skill
- Core workflow: Think (pick aesthetic) → Structure (read template) → Style (apply design) → Deliver (write + open)
- 11 diagram types with rendering approach routing (Mermaid, CSS Grid, HTML tables, Chart.js)
- 9 aesthetic directions (monochrome terminal, editorial, blueprint, neon, paper/ink, sketch, IDE-inspired, data-dense, gradient mesh)
- Mermaid deep theming with `theme: 'base'` + `themeVariables`, hand-drawn mode, ELK layout
- Zoom controls (buttons, scroll-to-zoom, drag-to-pan) required on all Mermaid containers
- Proactive table rendering — agent generates HTML instead of ASCII for complex tables
- Optional AI-generated illustrations via surf-cli + Gemini Nano Banana Pro
- Both light and dark themes via CSS custom properties and `prefers-color-scheme`
- Quality checks: squint test, swap test, overflow protection, zoom controls verification

### References
- `css-patterns.md` — theme setup, depth tiers, node cards, grid layouts, data tables, status badges, KPI cards, before/after panels, connectors, animations (fadeUp, fadeScale, drawIn, countUp), collapsible sections, overflow protection, generated image containers
- `libraries.md` — Mermaid (CDN, ELK, deep theming, hand-drawn mode, CSS overrides, diagram examples), Chart.js, anime.js, Google Fonts with 13 font pairings
- `responsive-nav.md` — sticky sidebar TOC on desktop, horizontal scrollable bar on mobile, scroll spy

### Templates
- `architecture.html` — CSS Grid card layout, terracotta/sage palette, depth tiers, flow arrows, pipeline with parallel branches
- `mermaid-flowchart.html` — Mermaid flowchart with ELK + handDrawn mode, teal/cyan palette, zoom controls
- `data-table.html` — HTML table with KPI cards, status badges, collapsible details, rose/cranberry palette

### Prompt Templates
- `/generate-web-diagram` — generate a diagram for any topic
- `/diff-review` — visual diff review with architecture comparison, KPI dashboard, code review, decision log
- `/plan-review` — plan vs. codebase with current/planned architecture, risk assessment, understanding gaps
- `/project-recap` — project mental model snapshot for context-switching
- `/fact-check` — verify factual accuracy of review pages and plan docs against actual code
