---
name: product-craft
description: Apply the 12 rules of product craft to build products users love and return to. Covers user personas, UX principles, brand foundation, information architecture, design systems, state design, onboarding, performance, micro-interactions, and activation events. Use when auditing product quality, designing UX, planning onboarding, or defining activation metrics.
metadata:
  author: kingly-agency
  version: '1.0'
---

# Product Craft Skill

Apply the 12 rules of product craft to build products users love and return to. Based on Harshil Tomar's 12 Rules framework, enhanced with Lev-lens mapping.

## The 12 Rules

### Rule 1: User Persona Before Code
Define the exact daily workflow, specific frustration, and current workaround before writing a line of code.

**Test**: Can you describe your user in 2 sentences — their role, their daily pain, and what they're doing instead?

**Template**:
> "[Name] is a [role] at [company type] who [daily workflow]. They're frustrated by [specific pain] and currently [workaround], which costs them [time/money/risk]."

**Red flags**: Personas described as demographics only ("25–35 year olds who use SaaS") with no workflow or frustration defined.

### Rule 2: Define the Feel Before Design
UX principles come before wireframes. Decide: fast and minimal for power users? Guided for beginners? Both (adaptive)?

**Map the critical user journey to the "aha moment"**:
1. Entry point → 2. First meaningful action → 3. Value experienced → 4. Aha moment → 5. Habit formed

**UX Principle examples**:
- "Speed over features" — every interaction must be fast; cut anything slow
- "Progressive disclosure" — show complexity only when the user is ready for it
- "Opinionated defaults" — make the right choice the default; allow customization later

### Rule 3: Brand Foundation Before Components
Brand = every decision in front of a user. A button label, an error message, an empty state — all brand.

**Brand Foundation elements**:
- **Name**: Memorable, pronounceable, domain-available
- **Tagline**: Outcome-first, 5–8 words max
- **Brand pillars**: 3 adjectives that govern all decisions (e.g., Fast, Honest, Human)
- **Positioning statement**: "For [ICP], [product] is the [category] that [key benefit] because [proof]"
- **Voice & tone**: How does the product "talk"? Define for: labels, buttons, error messages, empty states, success messages

### Rule 4: Information Architecture Before Screens
Map every page, section, and flow on paper. Group by user intent, not code structure.

**Steps**:
1. List every task a user can perform
2. Group tasks by intent (not by where data lives)
3. Define navigation model: tab bar, sidebar, breadcrumb, wizard, or hub-and-spoke
4. Validate IA with a card sort (5–10 users)
5. Only then move to wireframes

**Test**: Can a new user find [critical feature] within 60 seconds without help?

### Rule 5: Layout Consistency Across Roles
Same component behavior, visual hierarchy, and interaction patterns regardless of user role or permission level.

**Requirements**:
- Master layout grid defined and never broken
- Component behavior is identical whether user is admin or viewer
- Visual hierarchy (H1 → H2 → body → caption) consistent on every screen
- Role differences are data/permission differences, not layout differences

### Rule 6: Design System Before First Screen
Token system first, components second, screens third.

**Token system**:
- **Spacing scale**: 4px base unit (4, 8, 12, 16, 24, 32, 48, 64, 96)
- **Type scale**: Define 5–6 levels (display, H1, H2, body, caption, label)
- **Color tokens**: Named by role, not value (see Rule 7)

**Component library requirements**:
- Every component documented with ALL states (default, hover, focus, active, disabled, loading, error)
- No one-off components — if it's built twice, it's a component

### Rule 7: Color Palette as Retention Decision
Colors set trust expectations. Match palette to what your user expects from products in this space.

**Full token set required**:
- **Primary**: Brand color, used for primary actions
- **Secondary**: Supporting accent
- **Semantic**: success (green), warning (yellow/amber), error (red), info (blue)
- **Neutral scale**: 9–11 steps from white to black (background, surface, border, text)
- **Dark mode**: Define separately; don't just invert

**Trust mapping**:
- Finance/health: Blues and greens signal safety and stability
- Developer tools: Dark mode first, high contrast, monospace accents
- Consumer/lifestyle: Warmer palettes, more expressive

### Rule 8: Design Every State
The happy path is 20% of interactions. Design the other 80%.

**Required states for every UI element**:
| State | What It Covers |
|---|---|
| Default | Normal loaded state |
| Loading | Data is fetching; use skeleton screens, not spinners |
| Empty | Zero data, new user, or no results |
| Error | Something failed; tell user what happened AND what to do next |
| Edit | Inline editing mode |
| Success | Action completed; confirm with micro-feedback |
| Zero-data | First session, no history yet |
| Partial data | Some data loaded, more coming |

**Empty state is critical**: It's every new user's first experience. Empty states must include: what this section does, why it's empty, and one clear CTA to add data.

**Error message formula**: "[What happened]. [Why it happened if useful]. [What to do next]."
- Bad: "Error 403"
- Good: "You don't have access to this workspace. Ask your admin to add you, or sign in with a different account."

### Rule 9: Onboarding — Minimum Viable Data
Ask only what's needed for a valuable first session. Progressive disclosure always.

**Principles**:
- Never gate the product behind a 10-step setup wizard
- Collect data when it's needed, not upfront as a prerequisite
- Define the minimum information needed to deliver value in session 1
- Use progressive profiling: collect more data over time as trust builds

**Onboarding audit questions**:
- How many fields before the user sees value?
- Can the user skip any step and still reach the aha moment?
- Is there a sample/demo mode so users see value before entering their own data?

### Rule 10: Performance as Product Feature
Speed is a feature. Slow products feel broken even if they work.

**Targets**:
- Core actions (save, navigate, search): < 200ms perceived
- Page load (LCP): < 2.5 seconds on median connection
- Time to interactive: < 3.5 seconds
- API responses: < 500ms for synchronous calls; use async + polling for anything longer

**Techniques**:
- Skeleton screens over spinners (users tolerate the same wait longer with skeletons)
- Optimistic UI updates (update the UI before the server confirms)
- Lazy load below-the-fold content
- Prefetch the most likely next action

### Rule 11: Micro-Interactions
Every click gets feedback. Micro-interactions make the product feel "alive" vs. "clunky."

**Animation timing**:
- 100–150ms: Instant feedback (button press, checkbox)
- 150–300ms: State transitions (modals, tooltips, dropdowns) — sweet spot
- 300–500ms: Page transitions, major state changes
- > 500ms: Feels slow; only for dramatic reveals

**Required micro-interactions**:
- Button press feedback (scale or color shift)
- Form field focus states
- Success confirmation (checkmark animation or color pulse)
- Error shake or highlight
- Hover states on all interactive elements
- Loading progress on operations > 1 second

### Rule 12: Build for Day 3, Not Day 1
The activation event is the single action that most predicts retention. Engineer the first session around it.

**Activation event definition**:
- It's a specific, measurable action (not "user felt value")
- It's achievable in the first session for motivated users
- Users who complete it have meaningfully higher Day-30 retention

**Day-3 retention trigger**:
- What brings the user back on Day 3?
- Build a trigger: email, notification, progress reminder, or social proof
- If they don't return by Day 3, re-engagement probability drops sharply

## Product Craft Audit Template

```markdown
# Product Craft Audit — [Product]

## Score: [X/12 rules satisfied]

| Rule | Status | Evidence | Action Needed |
|---|---|---|---|
| 1. User Persona | ✅/⚠️/❌ | | |
| 2. UX Principles | ✅/⚠️/❌ | | |
| 3. Brand Foundation | ✅/⚠️/❌ | | |
| 4. Info Architecture | ✅/⚠️/❌ | | |
| 5. Layout Consistency | ✅/⚠️/❌ | | |
| 6. Design System | ✅/⚠️/❌ | | |
| 7. Color Palette | ✅/⚠️/❌ | | |
| 8. State Design | ✅/⚠️/❌ | | |
| 9. Onboarding | ✅/⚠️/❌ | | |
| 10. Performance | ✅/⚠️/❌ | | |
| 11. Micro-Interactions | ✅/⚠️/❌ | | |
| 12. Activation Event | ✅/⚠️/❌ | | |

## Activation Event Definition
- Event: [specific measurable action]
- Day 3 retention trigger: [what brings them back]
- Current measurement: [instrumented? yes/no]

## Top 3 Violations (Priority Fix):
1. 
2. 
3. 

## Recommendations:
```

## Lev-Lens Mapping

For teams building with Lev, map Product Craft findings directly to Lev concepts:

| Product Craft Rule | Lev Concept |
|---|---|
| Rule 1: User Persona | First-class node in the graph — define persona as a typed entity |
| Rule 4: Info Architecture | Intent routing layer — IA maps to how Lev routes user intent |
| Rule 6: Design System | Deterministic tokens shared across surfaces — token values as Lev config |
| Rule 8: State Design | Explicit execution states in FlowMind — model every state as a named flow state |
| Rule 12: Activation Event | Measurable contract in the event spine — instrument activation as a tracked event |

## Instructions

1. Ask the user about their product's current state (demo URL, screenshots, or description)
2. If a URL is provided, fetch the product and take screenshots to analyze visually
3. Walk through all 12 rules, scoring each as ✅ (satisfied), ⚠️ (partial), or ❌ (missing)
4. Identify the 3 most critical violations by impact on user retention
5. Define the activation event with the user (if not already defined)
6. Produce a Product Craft Audit document saved to workspace
7. Generate specific, actionable recommendations with priority order
8. If Lev is in use, map findings to Lev concepts in a dedicated section

## Output Format

Save to workspace: `product-craft-audit-[product-name].md`

Include:
- Completed Product Craft Audit table (all 12 rules scored with evidence)
- Overall score (X/12)
- Activation event definition (with instrumentation status)
- Top 3 violations with specific fix recommendations
- Full recommendations list ordered by impact
- Lev-lens mapping section (if applicable)
- Estimated effort per fix (quick win / medium / major refactor)
