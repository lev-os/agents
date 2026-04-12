---
name: ui-polish
description: >-
  Iterative UI/UX polishing for Stripe-level visual quality. Use when app
  already works and looks decent, wanting to elevate to world-class through
  multiple passes. Not for complete overhauls.
---

<!-- TOC: THE EXACT PROMPT | Why It Works | When to Use | Iteration Protocol | References -->

# UI/UX Polish — Iterative Enhancement Workflow

> **When to Use:** App already works and looks decent, you want to elevate it.
>
> **When NOT to Use:** App is broken, styling is fundamentally wrong, or starting from scratch.
>
> **Key Insight:** Asking for agreement ("don't you agree?") motivates better polish. Instructing to consider desktop vs mobile separately leads to much better outcomes.

---

## THE EXACT PROMPT — UI/UX Polish

This prompt is used so frequently it's worth putting on a Stream Deck button:

```
I still think there are strong opportunities to enhance the UI/UX look and feel and to make everything work better and be more intuitive, user-friendly, visually appealing, polished, slick, and world class in terms of following UI/UX best practices like those used by Stripe, don't you agree? And I want you to carefully consider desktop UI/UX and mobile UI/UX separately while doing this and hyper-optimize for both separately to play to the specifics of each modality. I'm looking for true world-class visual appeal, polish, slickness, etc. that makes people gasp at how stunning and perfect it is in every way.  Use ultrathink.
```

### Best Models

| Model | Configuration |
|-------|---------------|
| **Claude Code + Opus 4.5** | Use ultrathink |
| **Codex + GPT 5.2** | High/Extra-High reasoning |
| **Gemini CLI** | Good |

---

## Why This Prompt Works

| Element | Effect |
|---------|--------|
| "don't you agree?" | Engages reasoning about whether improvements are possible |
| "desktop and mobile separately" | Prevents compromise solutions that are mediocre on both |
| "world class", "Stripe" | Sets high anchor point |
| "makes people gasp" | Pushes toward exceptional quality |
| "ultrathink" | Extended thinking for thorough analysis |

---

## Iteration Protocol

### The Workflow

```
1. App already works and looks decent
   ↓
2. Run the polish prompt
   ↓
3. Agent makes incremental improvements
   ↓
4. Repeat many times (10+ iterations)
   ↓
5. Small improvements compound dramatically
```

### Why Multiple Passes Work

- Each pass makes some incremental improvement (even if minor)
- These really add up after 10 iterations
- Multiple agents can work simultaneously on different areas
- Cumulative effect is dramatic

---

## What Typically Gets Improved

### Visual Polish
- Spacing and padding consistency
- Typography hierarchy
- Color contrast and accessibility
- Shadow and depth effects
- Border radius consistency
- Hover/focus states

### Interaction Design
- Button feedback
- Loading states
- Transitions and animations
- Error/empty state design

### Desktop vs Mobile

| Desktop Optimizations | Mobile Optimizations |
|----------------------|---------------------|
| Keyboard navigation | Touch target sizes |
| Hover states | Mobile-specific navigation |
| Multi-column layouts | Gesture support |
| Sidebar navigation | Performance |
| Power user shortcuts | Responsive breakpoints |

---

## When to Use vs When NOT

### USE When:
- App works correctly
- Basic styling is in place
- Want to elevate from "decent" to "world-class"
- Ready for iterative refinement

### DON'T Use When:
- App is broken or buggy (fix bugs first)
- Styling is fundamentally wrong (need complete overhaul)
- No basic design system in place
- Starting from scratch

For complete overhauls, establish a design system and component library first.

---

## Tips

1. **Don't skip iterations** — Even when changes seem small, keep going
2. **Review changes** — Make sure improvements don't break things
3. **Test on real devices** — Desktop browser != mobile experience
4. **Consider accessibility** — WCAG compliance matters
5. **Keep performance in mind** — Pretty but slow is bad UX

---

## References

| Topic | Reference |
|-------|-----------|
| Additional prompts | [PROMPTS.md](references/PROMPTS.md) |
| Improvement checklist | [CHECKLIST.md](references/CHECKLIST.md) |
