---
name: product-craft
description: Apply the 12 rules of product craft to build products users love and return to. Covers user personas, UX principles, brand foundation, information architecture, design systems, state design, onboarding, performance, micro-interactions, and activation events. Use when auditing product quality, designing UX, planning onboarding, or defining activation metrics.
metadata:
  author: kingly-agency
  version: '1.0'
---

# Product Craft Skill

Apply the 12 rules of product craft to build products users love and return to. Based on Harshil Tomar's 12 Rules framework, enhanced with Lev-lens mapping.

## Evidence and procedure

Inspect the supplied description, screenshots, repository evidence or live
product only when the request authorizes that access. Ask for missing
information only when it changes the finding. Evaluate each rule as satisfied,
partial, missing, unknown or not applicable, and attach evidence and rationale.
Separate observed evidence from synthetic hypotheses. Prioritize three actions
by demonstrated user impact; state effort as quick, medium or major with a
basis. Define activation collaboratively when it is unsettled. A screenshot
does not prove performance, retention or recovery. In the UX hub, report inline
unless the user explicitly requests a saved artifact.

## The 12 Rules

### Rule 1: User Persona Before Code
Define the exact daily workflow, specific frustration, and current workaround before writing a line of code.

**Test**: Can you describe your user in 2 sentences — their role, their daily pain, and what they're doing instead?

**Template**:
> "[Name] is a [role] at [company type] who [daily workflow]. They're frustrated by [specific pain] and currently [workaround], which costs them [time/money/risk]."

**Red flags**: Personas described as demographics only ("25–35 year olds who use SaaS") with no workflow or frustration defined.

Demographic ranges are an example of a failure mode, not a substitute for
evidence about the actual user. Reuse existing persona and study artifacts;
label an inferred persona as a hypothesis.

### Rule 2: Define the Feel Before Design
UX principles come before wireframes. Decide: fast and minimal for power users? Guided for beginners? Both (adaptive)?

**Map the critical user journey to the "aha moment"**:
1. Entry point → 2. First meaningful action → 3. Value experienced → 4. Aha moment → 5. Habit formed

**UX Principle examples**:
- "Speed over features" — every interaction must be fast; cut anything slow
- "Progressive disclosure" — show complexity only when the user is ready for it
- "Opinionated defaults" — make the right choice the default; allow customization later

Treat these as candidate principles. Test the tradeoff against the supplied
workflow rather than assuming that speed, guidance or a default is always best.
Habit formation is a possible outcome to investigate, not an observation to
assume from the journey map.

### Rule 3: Brand Foundation Before Components
Brand = every decision in front of a user. A button label, an error message, an empty state — all brand.

**Brand Foundation elements**:
- **Name**: Memorable, pronounceable, domain-available
- **Tagline**: Outcome-first, 5–8 words max
- **Brand pillars**: 3 adjectives that govern all decisions (e.g., Fast, Honest, Human)
- **Positioning statement**: "For [ICP], [product] is the [category] that [key benefit] because [proof]"
- **Voice & tone**: How does the product "talk"? Define for: labels, buttons, error messages, empty states, success messages

Tagline length and three brand pillars are source examples, not limits. Reuse
existing brand decisions before proposing new ones.

### Rule 4: Information Architecture Before Screens
Map every page, section, and flow on paper. Group by user intent, not code structure.

**Steps**:
1. List every task a user can perform
2. Group tasks by intent (not by where data lives)
3. Define navigation model: tab bar, sidebar, breadcrumb, wizard, or hub-and-spoke
4. Validate IA with a card sort (5–10 users)
5. Only then move to wireframes

**Test**: Can a new user find [critical feature] within 60 seconds without help?

The 60-second check and a 5–10-person card sort are source suggestions. Adapt
the method and threshold to the product, task risk and available evidence.

### Rule 5: Layout Consistency Across Roles
Same component behavior, visual hierarchy, and interaction patterns regardless of user role or permission level.

**Requirements**:
- Master layout grid defined and never broken
- Component behavior is identical whether user is admin or viewer
- Visual hierarchy (H1 → H2 → body → caption) consistent on every screen
- Role differences are data/permission differences, not layout differences

Shared patterns should stay predictable, but materially different tasks or
permissions can justify a different layout. Record the reason instead of
forcing identical screens.

### Rule 6: Design System Before First Screen
Token system first, components second, screens third.

**Token system**:
- **Spacing scale**: 4px base unit (4, 8, 12, 16, 24, 32, 48, 64, 96)
- **Type scale**: Define 5–6 levels (display, H1, H2, body, caption, label)
- **Color tokens**: Named by role, not value (see Rule 7)

**Component library requirements**:
- Every component documented with ALL states (default, hover, focus, active, disabled, loading, error)
- No one-off components — if it's built twice, it's a component

The 4px scale and five-to-six type levels are examples. Repeated behavior is a
reuse candidate; do not create an abstraction without a real second use.

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

These domain-to-color associations are illustrative hypotheses, not universal
stereotypes or evidence of trust, retention or conversion. Check contrast,
non-color meaning, user expectations and observed outcomes for the product.

### Rule 8: Design Every State
The happy path is described here as 20% of interactions. Treat the 20/80 split
as an illustrative, unverified planning heuristic; measure the product's actual
state distribution. Design the other states that the workflow requires.

**States to consider for each UI element; mark inapplicable states with a reason**:
| State | What It Covers |
|---|---|
| Default | Normal loaded state |
| Loading | Data is fetching; choose a skeleton or spinner for the wait and task (see Rule 10) |
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

The source recommends skeletons rather than spinners; treat that as a
contextual suggestion, not a universal rule. The formula and pair are teaching examples. Check the actual cause, permissions
and available recovery before choosing the wording; do not invent a recovery
path just to satisfy the pattern.

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

Longer setup may be necessary for safety, consent or product constraints. Keep
required validation and consent, and explain why a field is needed before
deferring or removing it.

### Rule 10: Performance as Product Feature
Speed is a feature. Slow products feel broken even if they work.

**Targets**:
- Core actions (save, navigate, search): < 200ms perceived
- Page load (LCP): < 2.5 seconds on median connection
- Time to interactive: < 3.5 seconds
- API responses: < 500ms for synchronous calls; use async + polling for anything longer

These are source-supplied starting heuristics, not universal standards or
proof that users will perceive the product as fast. Measure critical actions
under named devices, network conditions and realistic data; adjust budgets to
the product. Optimistic updates need rollback and must not misrepresent an
irreversible success.

**Techniques**:
- Skeleton screens over spinners (users tolerate the same wait longer with skeletons)
- Optimistic UI updates (update the UI before the server confirms)
- Lazy load below-the-fold content
- Prefetch the most likely next action

Skeletons, optimistic updates, lazy loading and prefetching are options. Use
them when the measured wait and task support the choice; a spinner or no
prefetch can be correct in another context.

### Rule 11: Micro-Interactions
Every click gets feedback. Micro-interactions make the product feel "alive" vs. "clunky."

**Animation timing**:
- 100–150ms: Instant feedback (button press, checkbox)
- 150–300ms: State transitions (modals, tooltips, dropdowns) — sweet spot
- 300–500ms: Page transitions, major state changes
- > 500ms: Feels slow; only for dramatic reveals

These ranges are tuning examples, not mandates. Respect reduced-motion settings,
keyboard and touch input, and use feedback that remains perceivable without
animation or hover.

**Required micro-interactions**:
- Button press feedback (scale or color shift)
- Form field focus states
- Success confirmation (checkmark animation or color pulse)
- Error highlight; shake is optional when appropriate and motion is allowed
- Hover states where a pointer is available; retain keyboard and touch feedback
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

Day 3 and Day 30 are source windows, not universal laws. Cohort evidence can
test whether activation completion is associated with retention; association
does not establish causation. The sharp Day-3 drop claim is unverified. Choose
a consent-respecting return reason.

## Product Craft Audit Template

Use satisfied, partial, missing, unknown or not applicable in the status field.
Report unknown and not-applicable counts separately; the X/12 score describes
checklist coverage, not a validated quality or retention metric.

```markdown
# Product Craft Audit — [Product]

## Score: [X/12 rules satisfied]

| Rule | Status | Evidence | Action Needed | Effort |
|---|---|---|---|---|
| 1. User Persona | satisfied/partial/missing/unknown/N/A | | | |
| 2. UX Principles | satisfied/partial/missing/unknown/N/A | | | |
| 3. Brand Foundation | satisfied/partial/missing/unknown/N/A | | | |
| 4. Info Architecture | satisfied/partial/missing/unknown/N/A | | | |
| 5. Layout Consistency | satisfied/partial/missing/unknown/N/A | | | |
| 6. Design System | satisfied/partial/missing/unknown/N/A | | | |
| 7. Color Palette | satisfied/partial/missing/unknown/N/A | | | |
| 8. State Design | satisfied/partial/missing/unknown/N/A | | | |
| 9. Onboarding | satisfied/partial/missing/unknown/N/A | | | |
| 10. Performance | satisfied/partial/missing/unknown/N/A | | | |
| 11. Micro-Interactions | satisfied/partial/missing/unknown/N/A | | | |
| 12. Activation Event | satisfied/partial/missing/unknown/N/A | | | |

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

Mapping limits: verify the owning schema before writing a persona entity; treat
IA as a conceptual intent-routing mapping rather than deployed-routing proof;
reuse the actual token owner; keep UI and execution states distinct unless the
product evidence links them; and do not infer runtime or FlowMind write
authority from this table.

## Instructions (operative UX route)

1. Ask the user about their product's current state (demo URL, screenshots, or description)
2. If a URL is provided and access is authorized, fetch the product and take screenshots to analyze visually
3. Walk through all 12 rules, marking each satisfied, partial, missing, unknown or not applicable with evidence and rationale
4. Identify the 3 most critical violations or gaps by demonstrated user impact
5. Define the activation event with the user (if not already defined)
6. Return the audit inline unless the user explicitly requests a saved artifact
7. Generate specific, actionable recommendations with priority order and effort
8. If Lev is in use, map findings to Lev concepts in a dedicated section with the limits above

## Output Format

For a direct Product Craft request, suggest `product-craft-audit-[product-name].md`
as the filename only when a saved artifact is requested. The UX route returns
the same content inline by default.

Scorecard (always fill every row; status is satisfied, partial, missing, unknown or n/a):

| Rule | Status | Evidence | Action | Effort |
|---|---|---|---|---|
| 1. User persona | | | | |
| 2. UX principles | | | | |
| 3. Brand foundation | | | | |
| 4. Information architecture | | | | |
| 5. Layout consistency | | | | |
| 6. Design system | | | | |
| 7. Color palette | | | | |
| 8. State design | | | | |
| 9. Onboarding | | | | |
| 10. Performance | | | | |
| 11. Micro-interactions | | | | |
| 12. Activation event | | | | |

In a full UX run, write the same scorecard as `craft_audit.yaml` in the run folder and show the X/12 line in `summary.md`.

Include:
- Completed Product Craft Audit table (all 12 rules with status, evidence, action and effort)
- Overall score (X/12) with unknown and not-applicable counts
- Activation event definition (with instrumentation status)
- Top 3 violations with specific fix recommendations
- Full recommendations list ordered by impact
- Lev-lens mapping section (if applicable)
- Estimated effort per fix (quick win / medium / major refactor)

When this reference is loaded by the UX hub, return the audit inline unless the
user explicitly requests the suggested Markdown artifact. Keep the original
filename as a suggestion rather than an implicit write.
