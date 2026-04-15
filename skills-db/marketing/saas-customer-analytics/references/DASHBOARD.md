# Admin Dashboard Architecture

> The dashboard is where analytics become decisions. Design for glanceability, graceful degradation, and progressive depth.

## Layout Philosophy

```
┌─────────────────────────────────────────────────────────────┐
│  Sidebar          │  Main Content                           │
│  ────────         │  ─────────────                          │
│  Overview ●       │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  Analytics ▸      │  │ MRR │ │ ARR │ │ Run │ │ B/E │     │
│    Revenue        │  │     │ │     │ │ way │ │     │     │
│    Engagement     │  └─────┘ └─────┘ └─────┘ └─────┘     │
│    Cohorts        │                                         │
│    Health         │  ┌─────────────────────────────────┐   │
│  Projections ▸    │  │  Insights Widget                 │   │
│    Unit Econ      │  │  [critical] Runway < 3mo         │   │
│    Runway         │  │  [warning] Churn spike detected  │   │
│    Scenarios      │  │  [info] MRR milestone: $1k       │   │
│    Monte Carlo    │  └─────────────────────────────────┘   │
│  Health ▸         │                                         │
│  Users            │  ┌─────────────────────────────────┐   │
│  Support          │  │  Projections Widget              │   │
│  Billing          │  │  [MRR trend] [Runway bar]       │   │
│                   │  └─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Data Fetching Strategy

### TanStack Query Hooks

Each widget gets its own query hook with appropriate stale time:

```typescript
// Summary widget (frequent refresh)
useProjectionsSummary(cash, days) → staleTime: 60_000 (1min)

// Analytics pages (acceptable staleness)
useUnitEconomics(cac?) → staleTime: 300_000 (5min)
usePaymentFees(days) → staleTime: 300_000 (5min)
useRunway(cash) → staleTime: 300_000 (5min), enabled: cash > 0
useBreakEven() → staleTime: 300_000 (5min)

// Compute-heavy (on-demand only)
useScenarios() → mutation (POST, no auto-refresh)
useMonteCarlo() → mutation (POST, no auto-refresh)

// Real-time
useAdminEvents() → SSE streaming (no staleTime)
```

### Graceful Degradation Pattern

```typescript
const settled = await Promise.allSettled([
  fetchMrr(),
  fetchChurn(),
  fetchFees(),
  fetchBehavioral(),
]);

// Each result is independent — failures don't cascade
const mrr = settled[0].status === 'fulfilled' ? settled[0].value : null;
const churn = settled[1].status === 'fulfilled' ? settled[1].value : null;
// ...

// Widget shows what it has, marks missing sections
```

**Display states per metric:**
1. **Loading** → Skeleton placeholder (animated pulse)
2. **Success** → Metric value with sparkline
3. **Error** → Inline error with retry button
4. **Stale** → Value with "cached N minutes ago" indicator
5. **Unavailable** → "Not configured" with setup link

---

## Widget Catalog

### Projections Widget (Overview Dashboard)

4 metric cards + 30-day MRR trend chart:

| Card | Source | Format |
|------|--------|--------|
| MRR | summary.mrr | Currency ($X,XXX) |
| ARR | summary.arr | Currency ($XX,XXX) |
| Runway | summary.runwayMonths | "X.X months" or "Profitable" |
| Break-Even | summary.breakEvenProgress | "X/Y subscribers (Z%)" |

**Expansion:** Clicking a card navigates to the detail page.

### Insights Widget

Severity-sorted feed of actionable insights:

- **Critical** (red): Demands immediate action
- **Warning** (orange): Should investigate
- **Info** (blue): Informational milestone

Each insight has: title, description, evidence, suggested action, dismiss button (7-day snooze).

### Live Metrics Widget

SSE-streamed real-time counters:
- Active users right now
- Signups today
- Revenue today

Animated value transitions (spring animation) when values update.

---

## Chart Components

### SparklineCard
Mini chart embedded in a metric card. Shows 7-30 day trend.

### Area Chart
Multi-area chart for revenue trends (new MRR, churned MRR, net MRR stacked).

### Donut Chart
Provider breakdown (Stripe vs PayPal), segment breakdown (individual vs org).

### Funnel Chart
Conversion funnel: Visit → Signup → Activate → Subscribe.

### Heatmap
Cohort retention: rows = signup week, columns = weeks since signup, color = retention %.

### Sankey Diagram
User journey flow: Landing → Features → Pricing → Checkout → (Success | Abandon).

---

## Page Architecture

### Revenue Page
- MRR history line chart (30/60/90d)
- Provider breakdown donut
- New vs churned waterfall
- Growth rate trend

### Health Page
- Health score distribution bar chart (critical/high/medium/low)
- At-risk user table (sortable, filterable)
- Health trend sparklines per user

### Projections Hub
- Unit economics card grid
- Runway gauge visualization
- Break-even progress bar
- Links to: Scenarios, Monte Carlo

### Scenario Planning Page
- Multi-scenario comparison table
- Input sliders: price, churn, growth, costs
- Side-by-side MRR projections

### Monte Carlo Page
- Fan chart (P10/P50/P90 bands over time)
- Survival probability meter
- Runway distribution histogram
- Input form: iterations, months, parameters

---

## Error Handling Patterns

### Section Error Boundary

Wrap each widget in an error boundary so one crash doesn't take down the page:

```tsx
<SectionErrorBoundary fallback={<InlineError message="Failed to load" onRetry={refetch} />}>
  <ProjectionsWidget />
</SectionErrorBoundary>
```

### Inline Error Component

```tsx
<InlineError
  message="Unit economics unavailable"
  onRetry={() => queryClient.invalidateQueries(['unit-economics'])}
/>
```

### Empty State Component

```tsx
<AdminEmptyState
  icon={BarChart3}
  title="No revenue data yet"
  description="Revenue metrics appear after your first subscription."
  action={{ label: "View setup guide", href: "/admin/health" }}
/>
```

---

## Caching Strategy

| Layer | TTL | Invalidation |
|-------|-----|-------------|
| API response cache | 60s (summary) | Cache key includes params |
| TanStack Query | 60s-5min | staleTime per hook |
| Server memory cache | 60s (adapter) | Key: `${cash}:${days}` |
| Browser | Tab lifetime | refetchOnWindowFocus |

**Never cache Monte Carlo results** — they're stochastic (different each time by design).

---

## Admin Authentication

```typescript
// API route guard
export async function GET(request: NextRequest) {
  const authResult = await requireAdmin(request);
  if (authResult instanceof Response) return authResult; // 401/403
  // ... proceed with admin logic
}
```

All analytics endpoints require admin auth. Never expose financial data to non-admin users.

---

## Sidebar Navigation

Expandable groups that auto-expand based on current pathname:

```
/admin → Overview (no group expansion)
/admin/analytics/* → Analytics group expanded
/admin/projections/* → Projections group expanded
/admin/health/* → Health group expanded
```

**Runway badge:** If not profitable, show runway months on the Billing nav item as a colored badge (green > 6mo, yellow 3-6mo, red < 3mo).

---

## Design Tokens

| Element | Token | Value |
|---------|-------|-------|
| Positive trend | emerald-500 | Growth, health, revenue up |
| Negative trend | rose-500 | Churn, decline, risk |
| Neutral | zinc-400 | Stable, no change |
| Warning | amber-500 | Needs attention |
| Critical | red-500 | Immediate action |
| Info | blue-500 | Milestones, informational |

Use consistent color coding across all charts, badges, and indicators.
