# UI/UX Quality Prompts

## Table of Contents
- [Basic UI/UX Scrutiny](#basic-uiux-scrutiny)
- [Deep UI/UX Enhancement](#deep-uiux-enhancement)
- [When to Use](#when-to-use)
- [Quality Standards](#quality-standards)

---

## Basic UI/UX Scrutiny

### THE EXACT PROMPT

```
Great, now I want you to super carefully scrutinize every aspect of the application workflow and implementation and look for things that just seem sub-optimal or even wrong/mistaken to you, things that could very obviously be improved from a user-friendliness and intuitiveness standpoint, places where our UI/UX could be improved and polished to be slicker, more visually appealing, and more premium feeling and just ultra high quality, like Stripe-level apps.
```

**Focus areas:**
- Workflow optimization
- User-friendliness
- Intuitiveness
- Visual appeal
- Premium feel

---

## Deep UI/UX Enhancement

### THE EXACT PROMPT

```
I still think there are strong opportunities to enhance the UI/UX look and feel and to make everything work better and be more intuitive, user-friendly, visually appealing, polished, slick, and world class in terms of following UI/UX best practices like those used by Stripe, don't you agree? And I want you to carefully consider desktop UI/UX and mobile UI/UX separately while doing this and hyper-optimize for both separately to play to the specifics of each modality. I'm looking for true world-class visual appeal, polish, slickness, etc. that makes people gasp at how stunning and perfect it is in every way.  Use ultrathink.
```

**Focus areas:**
- Desktop-specific optimization
- Mobile-specific optimization
- World-class visual appeal
- Stripe-level polish
- "Gasp" factor

---

## When to Use

| Phase | Prompt | Purpose |
|-------|--------|---------|
| Post-feature | Basic Scrutiny | Catch obvious UX issues |
| Post-milestone | Deep Enhancement | Polish to world-class |
| Pre-release | Both, iteratively | Final quality pass |

### Recommended Pattern

```
1. Complete all functional beads
2. Run Basic Scrutiny
3. Fix issues found
4. Run Deep Enhancement
5. Fix issues found
6. Repeat 4-5 until no changes
7. Release
```

---

## Quality Standards

### The Stripe Standard

Reference apps that exemplify world-class UI/UX:
- **Stripe Dashboard** — Clean, information-dense, intuitive
- **Linear** — Fast, keyboard-first, visually stunning
- **Vercel** — Minimal, elegant, developer-focused
- **Notion** — Flexible, polished, delightful details

### What "World-Class" Means

| Dimension | Standard |
|-----------|----------|
| **Visual** | Consistent spacing, typography, color |
| **Responsive** | Desktop AND mobile hyper-optimized |
| **Feedback** | Instant, informative, delightful |
| **Accessibility** | Keyboard navigation, screen readers |
| **Performance** | Instant perceived response |
| **Polish** | No rough edges, every detail considered |

### The "Gasp" Test

If a user doesn't think "wow, this is beautiful" on first interaction, keep iterating.

---

## Implementation Tips

### Desktop Focus

- Information density (show more)
- Keyboard shortcuts
- Multi-column layouts
- Hover states
- Right-click menus

### Mobile Focus

- Touch targets (44px minimum)
- Swipe gestures
- Single-column layouts
- Bottom navigation
- Pull-to-refresh

### Both Platforms

- Consistent design language
- Smooth animations (60fps)
- Clear visual hierarchy
- Immediate feedback
- Error prevention
