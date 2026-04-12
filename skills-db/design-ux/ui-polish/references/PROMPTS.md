# UI/UX Polish Prompts — Reference

## Table of Contents
- [Main Polish Prompt](#main-polish-prompt)
- [Focused Prompts](#focused-prompts)
- [Multi-Agent Coordination](#multi-agent-coordination)
- [Creating Beads](#creating-beads)

---

## Main Polish Prompt

### The Standard Prompt

```
I still think there are strong opportunities to enhance the UI/UX look and feel and to make everything work better and be more intuitive, user-friendly, visually appealing, polished, slick, and world class in terms of following UI/UX best practices like those used by Stripe, don't you agree? And I want you to carefully consider desktop UI/UX and mobile UI/UX separately while doing this and hyper-optimize for both separately to play to the specifics of each modality. I'm looking for true world-class visual appeal, polish, slickness, etc. that makes people gasp at how stunning and perfect it is in every way.  Use ultrathink.
```

### General Scrutiny Alternative

```
Great, now I want you to super carefully scrutinize every aspect of the application workflow and implementation and look for things that just seem sub-optimal or even wrong/mistaken to you, things that could very obviously be improved from a user-friendliness and intuitiveness standpoint, places where our UI/UX could be improved and polished to be slicker, more visually appealing, and more premium feeling and just ultra high quality, like Stripe-level apps.
```

---

## Focused Prompts

### Desktop-Only Focus

```
Focus specifically on the desktop experience of [PAGE/COMPONENT]. Consider:
- Keyboard navigation
- Hover states
- Multi-column layouts
- Whitespace usage
- Power user affordances

Make it feel like a premium desktop application. Use ultrathink.
```

### Mobile-Only Focus

```
Focus specifically on the mobile experience of [PAGE/COMPONENT]. Consider:
- Touch target sizes (44px minimum)
- Thumb-friendly navigation
- Swipe gestures
- Bottom sheet patterns
- Mobile-first responsive design

Make it feel like a premium mobile app. Use ultrathink.
```

### Animation/Transition Focus

```
Review all animations and transitions in the application. Consider:
- Entrance/exit animations
- Loading state transitions
- Hover feedback
- Page transitions
- Micro-interactions

Ensure they're subtle, purposeful, and consistent with premium apps like Stripe. Use ultrathink.
```

### Typography Focus

```
Review typography across the application. Consider:
- Font hierarchy (h1-h6, body, caption)
- Line heights
- Letter spacing
- Font weights
- Responsive font sizes

Achieve a premium, readable typographic system. Use ultrathink.
```

### Spacing/Layout Focus

```
Review spacing and layout across the application. Consider:
- Vertical rhythm
- Consistent padding
- Section spacing
- Component spacing
- Grid alignment

Achieve pixel-perfect consistency. Use ultrathink.
```

### Color/Contrast Focus

```
Review color usage and contrast across the application. Consider:
- WCAG accessibility standards
- Color hierarchy
- Consistent accent usage
- Dark/light mode consistency
- Color for meaning (error, success, warning)

Achieve both beauty and accessibility. Use ultrathink.
```

---

## Multi-Agent Coordination

### Agent 1: Desktop Polish

```
You are Agent 1, focusing on desktop UI/UX polish for [PROJECT].

Focus areas:
- All pages at 1024px+ width
- Hover states
- Keyboard navigation
- Multi-column layouts

Use file reservations to avoid conflicts. Run the polish prompt repeatedly for your focus area.
```

### Agent 2: Mobile Polish

```
You are Agent 2, focusing on mobile UI/UX polish for [PROJECT].

Focus areas:
- All pages at mobile widths
- Touch targets
- Mobile navigation
- Gesture support

Use file reservations to avoid conflicts. Run the polish prompt repeatedly for your focus area.
```

### Agent 3: Animations

```
You are Agent 3, focusing on animations and transitions for [PROJECT].

Focus areas:
- Loading states
- Page transitions
- Hover feedback
- Micro-interactions

Use file reservations to avoid conflicts. Focus on making everything feel smooth and premium.
```

---

## Creating Beads

For systematic UI/UX work, create beads:

```bash
# Page-specific polish
br create "Polish homepage UI/UX for desktop" -t enhancement -p 2
br create "Polish homepage UI/UX for mobile" -t enhancement -p 2
br create "Polish dashboard UI/UX for desktop" -t enhancement -p 2
br create "Polish dashboard UI/UX for mobile" -t enhancement -p 2

# Focus-area polish
br create "Improve animation/transition consistency" -t enhancement -p 3
br create "Enhance typography hierarchy" -t enhancement -p 3
br create "Fix spacing inconsistencies" -t enhancement -p 3
br create "Improve color contrast for accessibility" -t enhancement -p 2
```

---

## Iteration Tracking

### After Each Pass, Note:

```markdown
## Polish Pass #[N]

### Desktop Changes
- [ ] Change 1
- [ ] Change 2

### Mobile Changes
- [ ] Change 1
- [ ] Change 2

### Before/After Notes
- Previous: [description]
- After: [description]

### Remaining Opportunities
- [ ] Still could improve X
- [ ] Consider Y
```

### Knowing When to Stop

Stop iterating when:
- Changes become trivial (single pixel adjustments)
- Model says "I don't see significant opportunities"
- Reviewers consistently approve without suggestions
- Performance concerns outweigh visual gains
