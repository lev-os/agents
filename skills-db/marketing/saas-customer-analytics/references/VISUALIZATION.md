# Visualization & Dashboard UX

> A number without context is noise. A number with trend, comparison, and target is a decision. Design every visualization to move the viewer from "what happened" to "what should I do" in under 3 seconds.

## The Hierarchy of Analytical Insight

Every metric display should progress through these layers:

```
Layer 1: WHAT    — The number ($1,240 MRR)
Layer 2: VERSUS  — Comparison (▲ 8.1% vs last month)
Layer 3: SHAPE   — Trend over time (sparkline showing trajectory)
Layer 4: WHY     — Decomposition (new MRR +$200, churned -$60)
Layer 5: SO WHAT — Recommended action (3 subscribers at risk, intervene?)
```

Most dashboards stop at Layer 1 or 2. World-class analytics reach Layer 5.

---

## Library Selection

| Library | Best For | Bundle | SSR? | Why Choose |
|---------|---------|--------|------|------------|
| **Recharts** | Line, area, bar, composed | 48KB | Yes | React-native, responsive, best defaults for standard charts |
| **Visx** (Airbnb) | Custom/bespoke | 12KB+ | Yes | D3 primitives as React components, total control, smallest bundle per chart |
| **Nivo** | Heatmaps, Sankey, chord, waffle | 80KB+ | Yes | Beautiful out-of-box, strong a11y, built-in legends and tooltips |
| **Tremor** | KPI cards, metric lists | 35KB | Yes | Built for analytics dashboards, Tailwind-native, opinionated and fast |
| **Observable Plot** | Exploratory, statistical | 50KB | No | Grammar-of-graphics, excellent for quick prototyping and statistical charts |
| **D3** (direct) | Force layouts, custom interactions | 80KB | No | When no React wrapper exists; use sparingly with `useRef` + `useEffect` |
| **Framer Motion** | Value animations, transitions | 32KB | No | Spring physics for counting animations, chart entrance, layout transitions |
| **react-spring** | Lightweight animation | 18KB | No | Alternative to Framer Motion if you need smaller bundle |

### Recommended Stacks by Project Size

| Scale | Stack | Rationale |
|-------|-------|-----------|
| MVP / solo founder | Tremor only | Fastest to production, KPI cards + basic charts |
| Growth stage | Recharts + Tremor + Framer Motion | Full chart coverage + polished cards + animations |
| Enterprise | Recharts + Nivo + Visx + Framer Motion | Heatmaps, Sankeys, custom viz, full control |

---

## Chart Type Selection Matrix

| Metric | Chart Type | Why | Anti-Pattern |
|--------|-----------|-----|-------------|
| Revenue over time | **Filled area** | Shows magnitude + direction, fill emphasizes accumulation | Don't use bar (too discrete for continuous metric) |
| Revenue composition (plan tiers, segments) | **Stacked area** | Shows parts + total simultaneously | Don't use pie (hard to compare slices over time) |
| Payment provider split | **Donut** with center value | Proportions of a whole, center shows total MRR | Don't use bar (proportions, not magnitudes) |
| Churn rate trend | **Line** with reference line | Trend vs threshold, clean readability | Don't use area (churn is a rate, not accumulating) |
| Revenue projections (Monte Carlo) | **Fan chart** (3-band area) | Honest uncertainty — wider = less certain | Never use single line (false precision) |
| Cohort retention | **Heatmap** | 2D pattern recognition via color intensity | Don't use line per cohort (spaghetti) |
| Health distribution | **Horizontal stacked bar** | Proportion of critical/high/medium/low at a glance | Don't use pie (too many segments) |
| User journey | **Sankey diagram** | Flow magnitude + drop-off points | Don't use funnel (funnels hide parallel paths) |
| Conversion funnel | **Vertical funnel** | Stage-by-stage narrowing with drop-off % | Don't use bar (doesn't show sequential flow) |
| Break-even progress | **Progress bar** with marker | Single dimension, current vs target | Don't use gauge (overkill for binary metric) |
| Runway | **Colored badge** or progress bar | Single urgent value, color = severity | Don't use chart (one number doesn't need a chart) |
| New vs churned subscribers | **Diverging bar** | Signed comparison per period | Don't use stacked (hides cancellation magnitude) |
| Survival curve | **Step function** | Kaplan-Meier convention, steps at events | Don't use smooth line (implies interpolation) |
| At-risk subscribers | **Sortable table** with badges | Actionable list, not pattern recognition | Don't use chart (need per-user detail) |
| Daily summary | **Card grid** with sparklines | Scannable multi-metric overview | Don't use single chart (too many metrics) |

---

## The KPI Card Anatomy

The most important UI component. Gets looked at 100x more than any chart.

```
┌─────────────────────────────────┐
│ ○ Monthly Recurring Revenue     │  ← Title: muted, 12-13px
│                                 │
│ $1,240                          │  ← Value: bold, 28-32px, dominant
│ ▲ 8.1% vs last month           │  ← Trend: colored, with direction icon
│                                 │
│ ╭─────────────────╮             │  ← Sparkline: 30-day, no axis labels
│ │    ╱╲   ╱╲  ╱   │             │     Pure shape = pure trend signal
│ │╱──╱  ╲─╱  ╲╱    │             │
│ ╰─────────────────╯             │
└─────────────────────────────────┘
```

### Design Rules

| Element | Rule | Rationale |
|---------|------|-----------|
| Value | Largest element (28-32px) | Eye goes here first |
| Trend | Emerald ▲ or Rose ▼ | Instant positive/negative signal |
| Inverted metrics | Rose for ▲ churn, Emerald for ▼ churn | "Down is good" for cost/churn metrics |
| Sparkline | No axis labels, no tooltips | Pure trend shape, detail lives in drill-down |
| Click target | Entire card is clickable | Navigate to detail page |
| Loading | Skeleton matching card dimensions | Prevents layout shift |

### Implementation Pattern

```tsx
<SparklineCard
  title="Monthly Recurring Revenue"
  value={mrr}
  format="currency"          // or "percent", "number", "duration"
  change={mrrChangePercent}
  invertColor={false}         // true for churn, burn rate
  trend={last30DaysData}      // Array<{ date: string, value: number }>
  color="emerald"
  href="/admin/analytics/revenue"
/>
```

---

## Color System

### Semantic Color Mapping

| Meaning | Color | Tailwind Token | Use For |
|---------|-------|---------------|---------|
| Growth / health | Emerald 500 | `text-emerald-500` | Revenue up, healthy scores, positive trend |
| Decline / risk | Rose 500 | `text-rose-500` | Churn up, health declining, negative trend |
| Warning | Amber 500 | `text-amber-500` | Past due, approaching threshold |
| Neutral | Zinc 400 | `text-zinc-400` | Stable, no change |
| Critical | Red 600 | `text-red-600` | Runway critical, immediate action required |
| Info | Blue 500 | `text-blue-500` | Milestones, informational badges |
| Primary metric | Zinc 900 (dark mode: 50) | `text-zinc-900` | Main value in KPI cards |

### The Cardinal Rule

**Never encode meaning in color alone.** Always pair with: icon (▲ ▼ ●), text label, pattern, or position.

Reason: 8% of men have red-green color blindness. Your SaaS founder checking metrics on a phone screen in sunlight may not see the difference between emerald and rose.

### Uncertainty Bands (Fan Charts)

```
P90 band: emerald-100 fill (almost transparent green)
P50 line: emerald-500 stroke, 2px (solid, dominant)
P10 band: rose-100 fill (almost transparent red)
```

Visual grammar: green tint = upside, red tint = downside, solid line = most likely. The bands should be labeled at the right edge ("Optimistic", "Most likely", "Pessimistic").

---

## Dashboard Layout Patterns

### Overview Page (3-Second Scan)

```
┌─────────┬─────────┬─────────┬─────────┐
│ MRR     │ Subs    │ Churn   │ Runway  │  ← KPI row: scannable metrics
│ $1,240  │ 52      │ 4.2%    │ 8.2 mo  │
│ ▲ 8.1%  │ ▲ 3     │ ▼ 0.3%  │ ▲ 1.2   │
└─────────┴─────────┴─────────┴─────────┘
┌───────────────────────────────────────┐
│ Insights (severity-sorted)            │  ← Action items first
│ [!] Runway < 3 months                │     Severity: critical > warning > info
│ [⚠] Churn spike: 30d > 2x baseline   │     Dismissible (7-day snooze)
│ [i] MRR milestone: $1,000            │
└───────────────────────────────────────┘
┌──────────────────┬────────────────────┐
│ MRR Trend (area) │ Health Dist (bar)  │  ← Two-column for related metrics
│ 30-day filled    │ Crit/Hi/Med/Low    │
└──────────────────┴────────────────────┘
```

### Revenue Deep Dive

```
┌──────────────────────┬────────────────┐
│ MRR History (area)   │ Provider (donut)│
│ 90-day, annotated    │ Stripe vs PayPal│
├──────────────────────┴────────────────┤
│ Revenue Waterfall (diverging bar)      │
│ New ████████████ +$200                 │
│ Churned ████ -$60                      │
│ Net █████████████████ +$140            │
├───────────────────────────────────────┤
│ Churn Trend (line + threshold)         │
│ ── 30d actual   --- 90d baseline       │
│ Shaded zone: critical churn region     │
└───────────────────────────────────────┘
```

### Information Hierarchy Rules

| Position | Content | Rationale |
|----------|---------|-----------|
| Top row | KPI cards (most critical 3-5 metrics) | First thing seen |
| Below KPIs | Insights / alerts | Demands attention before drill-down |
| Middle | Primary trend chart | Context for the KPI numbers |
| Bottom | Secondary breakdowns, tables | Detail for investigation |
| Sidebar (optional) | Navigation, filters, date range | Controls, not data |

---

## Number Formatting

| Type | Format | Example | Rule |
|------|--------|---------|------|
| Currency | `$X,XXX` | $1,240 | No decimals unless < $10 |
| Large currency | `$XXk` / `$X.Xm` | $14.9k | Abbreviate above $10k |
| Percentage | `X.X%` | 8.1% | Always one decimal |
| Count | `X,XXX` | 1,240 | Comma separators |
| Duration | `X.X months` / `Xd Xh` | 8.2 months | Context-appropriate units |
| Trend | `▲ X.X%` / `▼ X.X%` | ▲ 8.1% | Arrow + value + direction |
| Null / unavailable | Em dash `—` | — | Never show "null", "N/A", or blank |
| Zero | `0` or `$0` | $0 | Show zero explicitly, never hide |

### Animated Value Transitions

When a metric updates, animate from old → new with spring physics:

```tsx
<AnimatedValue
  value={mrr}
  format={(v) => `$${v.toLocaleString()}`}
  stiffness={120}
  damping={20}
/>
```

This draws the eye to the change. Use `prefers-reduced-motion` media query to disable for accessibility.

---

## Advanced Visualization Patterns

### Revenue Waterfall Chart

Shows MRR movement: starting MRR + new - churned - contraction + expansion = ending MRR.

```
Starting MRR  ██████████████████ $1,100
  + New       ████████           +$200
  + Expansion ██                 +$40
  - Churned   ████               -$60
  - Contraction █                -$20
  = Ending    ████████████████████ $1,260
```

Each bar starts where the previous ended. Green for positive, red for negative.

### Survival Curve (Kaplan-Meier)

```tsx
// Step-function chart showing subscriber survival probability over time
<LineChart data={survivalData}>
  <Line dataKey="survivalPct" type="stepAfter" stroke="emerald-500" strokeWidth={2} />
  <Area dataKey="ciUpper" type="stepAfter" fill="emerald-100" stroke="none" />
  <Area dataKey="ciLower" type="stepAfter" fill="white" stroke="none" />
  <ReferenceLine y={50} stroke="zinc-300" strokeDasharray="4 4" label="Median survival" />
</LineChart>
```

### Comparison Overlays

For before/after or cohort-vs-cohort comparison:

```tsx
// Overlay two time series with distinct styling
<Line dataKey="current" stroke="emerald-500" strokeWidth={2} />
<Line dataKey="previous" stroke="zinc-300" strokeWidth={1} strokeDasharray="6 3" />
```

Solid = current period. Dashed = comparison period. Label both in legend.

---

## Loading, Error, and Empty States

**Every visualization MUST implement all three.** Missing states are the #1 dashboard UX bug.

### Loading
```tsx
<Skeleton className="h-[200px] w-full animate-pulse rounded-lg bg-zinc-800/50" />
```
Match skeleton dimensions to the chart it replaces. Prevents layout shift.

### Error
```tsx
<InlineError
  message="Revenue data unavailable"
  detail="Stripe API returned 503"
  onRetry={() => queryClient.invalidateQueries(['revenue'])}
/>
```
Always include: what failed + retry button. Never blank screen.

### Empty (No Data Yet)
```tsx
<EmptyState
  icon={BarChart3}
  title="No revenue data yet"
  description="Revenue metrics appear after your first paid subscription."
  action={{ label: "View setup guide", href: "/admin/health" }}
/>
```
Empty is NOT error. Guide the user toward the action that will populate the chart.

### Stale / Cached
```tsx
<Badge variant="outline" className="text-amber-500 text-xs">
  Cached · Updated {timeAgo(lastCalculated)}
</Badge>
```
Show on any metric older than its expected refresh interval. Users make decisions on these numbers — they must know if they're stale.

---

## Accessibility (a11y)

| Requirement | Implementation | Why It Matters |
|-------------|---------------|----------------|
| Color-blind safe | Icons (▲▼●), text labels, patterns alongside color | 8% of men are red-green color blind |
| Screen reader | `aria-label` on charts, `role="img"`, text summary | Vision-impaired users |
| Keyboard navigation | `tabIndex`, focus rings on interactive elements | Motor-impaired users, power users |
| Reduced motion | `prefers-reduced-motion` check, static fallback | Vestibular disorders |
| Contrast | 4.5:1 minimum (WCAG AA) for text on chart backgrounds | Readability in all lighting |
| Data table alternative | Toggle between chart and table view | Universal access to underlying data |

---

## Responsive Design

| Viewport | Adaptation |
|----------|-----------|
| Desktop (> 1280px) | Full grid (3-4 columns), side-by-side charts, expanded tables |
| Laptop (1024-1280px) | 2-3 columns, smaller sparklines |
| Tablet (768-1024px) | Stack charts vertically, keep KPI row, collapsible sidebar |
| Mobile (< 768px) | Single column, horizontal-scroll KPI cards (`snap-x`), simplified charts (less data points, no legends) |

### Mobile-Specific Rules

- KPI cards: horizontal scroll with snap alignment, not 2×2 grid
- Charts: reduce to 14-day window (not 30), fewer grid lines
- Tables: collapse to card view per row
- Sidebar: hamburger menu, not persistent

---

## Cognitive Design Principles

| Principle | Application | Example |
|-----------|------------|---------|
| **Pre-attentive processing** | Use color, size, position — processed in < 200ms | Red badge on at-risk count |
| **Gestalt grouping** | Related metrics in same card/section | MRR + ARR in one card row |
| **Progressive disclosure** | Overview → detail on click | KPI card → full chart page |
| **Context, not just data** | Always show comparison (vs target, vs last period) | "62% of break-even" not just "32 subscribers" |
| **Annotation over decoration** | Label important events on charts | "Price change" marker on MRR timeline |
| **Consistent mental model** | Same metric always looks the same everywhere | MRR is always emerald area chart |

---

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| 3D charts | Distort data, unprofessional | Flat 2D always |
| Pie chart with > 5 slices | Impossible to compare thin slices | Horizontal bar |
| Dual Y-axes | Visually misleading correlations | Two separate charts stacked |
| Rainbow color scheme | No semantic meaning, visual noise | 2-3 color semantic palette |
| Auto-updating without indicator | Users don't trust changing numbers | Show "Live" badge + update animation |
| Chart without units | "$1,240" vs "1,240 subscribers" is ambiguous | Always label axes and values |
| Tooltips as primary data | Mobile users can't hover | Show key values inline, tooltips for detail |
