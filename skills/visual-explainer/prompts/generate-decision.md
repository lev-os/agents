---
description: Generate an interactive decision capture page with localStorage auto-save — structured choices with radio options, notes, progress tracking, and JSON export
---
Load the visual-explainer skill (`~/.agents/skills/visual-explainer/SKILL.md`). Read it fully — the "Decision / Feedback Capture" section defines the structure.

Read the template at `./templates/decision.html` for the complete pattern including localStorage auto-save, event delegation, and responsive layout.

**Data gathering:**

1. **Identify decisions.** Scan the user's context (conversation, referenced files, plans, deliberation output) for items that need a choice. Each decision needs:
   - A short title (3-8 words)
   - An insight (1-2 sentences summarizing the key tension or finding — use `<strong>` and `<code>` for emphasis)
   - Detail/analysis (2-3 paragraphs of deeper context, optional but valuable)
   - 3 options with short labels and descriptions. Mark one as `recommended: true` if the evidence supports it
   - A priority/wave indicator

2. **Group into buckets.** Organize decisions into 2-6 thematic groups. Each bucket gets a number and name.

3. **Set page identity.** Choose a `data-page-id` for localStorage isolation (e.g., `cdo-s8`, `api-migration`, `q2-roadmap`). This must be unique per decision set.

**Required features (non-negotiable):**
- localStorage auto-save with 300ms debounce
- Visual save indicator ("Saved ✓" near progress bar)
- "Clear saved data" button with confirm dialog
- JSON export with clipboard + fallback
- Progress bar showing completion percentage
- Collapsible detail sections
- Event delegation (no re-renders on interaction)
- Both light and dark themes
- Print stylesheet
- Responsive layout

**Aesthetic:** Follow the visual-explainer skill's Think step — pick a distinctive palette and font pairing that differs from recent generations. The template uses Warm Charcoal + Copper with Space Grotesk + IBM Plex Mono, but each generation should vary.

Then follow the visual-explainer skill workflow (Think → Structure → Style → Deliver).

Ultrathink.

$@
