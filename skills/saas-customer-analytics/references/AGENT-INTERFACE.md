# Agent-Optimized Interfaces (Robot Mode)

> Humans and AI agents are co-consumers of your analytics. Humans need charts and color. Agents need structured JSON with pre-computed signals. Design both as first-class interfaces from day one.

## Why Agent Interfaces Matter

The SaaS analytics system produces dozens of metrics, dozens of insights, and dozens of at-risk subscribers. A human admin might check the dashboard once a day. An AI agent can monitor every 5 minutes, correlate across metrics, trigger interventions, and compose reports — but only if the data is structured for machine consumption.

**The parity contract:** Every number visible in the human admin dashboard MUST be available via the agent interface. Same data, different format.

---

## Design Principles

| Dimension | Human UI | Agent Interface |
|-----------|----------|----------------|
| **Format** | Charts, color, spatial layout | JSON with typed fields |
| **Density** | White space, one insight per card | Maximum data per token |
| **Context** | Visual trend (sparklines) | Numeric delta, ratio, z-score |
| **Navigation** | Click-through drill-down | Single query returns full context |
| **Interpretation** | Human pattern recognition | Pre-computed `significance` field |
| **Action** | "Click to investigate" | `next_actions[]` array with exact commands |
| **Error handling** | Error boundary + retry button | `ok: false` + `error` object + `fallback_data` |
| **Freshness** | "Updated 2 minutes ago" badge | `data_freshness: "fresh"|"stale"|"missing"` |

---

## CLI Command Design

Use your product's CLI binary name. The `analytics` subcommand tree should mirror the admin dashboard's information architecture exactly.

### Command Structure

```bash
# Entry point: full business state in one call (~500 tokens output)
your-cli analytics summary --json

# Domain queries
your-cli analytics revenue --json [--range 30d|90d|ytd]
your-cli analytics churn --json [--window 30|90]
your-cli analytics health --json [--segment all|at-risk|critical]
your-cli analytics projections --json [--cash 10000]
your-cli analytics cohorts --json [--months 6]
your-cli analytics engagement --json [--range 30d]

# Advanced modeling
your-cli analytics monte-carlo --json --iterations 1000 --months 12
your-cli analytics scenarios --json --price 25 --churn-override 0.03
your-cli analytics survival --json
your-cli analytics forecast --json --months 12

# Actionable
your-cli analytics at-risk --json [--limit 20] [--sort revenue|churn|health]
your-cli analytics interventions --json [--pending|--history]
your-cli analytics insights --json [--severity critical|warning|info]

# Delta (most token-efficient for recurring checks)
your-cli analytics diff --json [--since 1h|24h|7d]

# Infrastructure
your-cli analytics status --json    # Pipeline health, data freshness
```

### Design Rules for Agent CLIs

| Rule | Rationale |
|------|-----------|
| `--json` on every command | Machine-parseable by default, human-readable without flag |
| `--compact` for abbreviated keys | Saves 40-60% tokens for automated workflows |
| Deterministic key ordering | Enables reliable `jq` extraction without `.field?` guards |
| Exit code 0 even on partial failure | Agent reads `ok` field, doesn't rely on exit code for logic |
| Stderr for progress/debug | Stdout is pure JSON, stderr for "connecting..." messages |
| No interactive prompts behind `--json` | Agents can't answer "are you sure?" |

---

## Response Schema (Universal Contract)

Every response follows this envelope:

```typescript
interface AnalyticsResponse<T> {
  ok: boolean;                    // Did the query succeed?
  generated_at: string;           // ISO 8601 timestamp
  data_freshness: "fresh" | "stale" | "missing";
  stale_sources: string[];        // Which data sources are degraded
  cache_age_seconds: number;      // How old is this data
  data: T;                        // The actual payload
  signals: Signal[];              // Pre-computed alerts the agent should reason about
  next_actions: string[];         // Suggested follow-up commands
  error?: {                       // Only present when ok = false
    code: string;
    message: string;
    retryable: boolean;
  };
}

interface Signal {
  severity: "critical" | "warning" | "info";
  signal: string;                 // Machine-readable key: "churn_spike", "runway_critical"
  message: string;                // Human-readable explanation
  evidence: Record<string, number>; // Supporting data
  suggested_action: string;       // What to do about it
}
```

### Why `signals` and `next_actions` Exist

Without these, the agent must:
1. Fetch all data
2. Compute its own thresholds
3. Decide what's anomalous
4. Figure out what command to run next

With them, the agent receives pre-digested intelligence and a menu of responses. This reduces agent reasoning load, prevents threshold miscalculation, and ensures the agent applies the same business rules as the human dashboard.

---

## Summary Endpoint (Agent Entry Point)

The single most important endpoint. Returns the full business state in ~500 tokens.

```json
{
  "ok": true,
  "generated_at": "2026-03-24T02:15:00Z",
  "data_freshness": "fresh",
  "stale_sources": [],
  "cache_age_seconds": 12,
  "data": {
    "revenue": {
      "mrr": 1240,
      "mrr_delta_30d": 140,
      "mrr_delta_pct": 12.7,
      "arr": 14880,
      "individual_mrr": 1040,
      "org_mrr": 200,
      "individual_count": 52,
      "org_count": 1
    },
    "unit_economics": {
      "arpu": 20,
      "ltv": 400,
      "gross_margin_pct": 95.2,
      "contribution_margin": 19.04,
      "break_even_subscribers": 3,
      "break_even_progress": 0.95,
      "is_break_even_reachable": true
    },
    "churn": {
      "rate_30d": 4.2,
      "rate_90d": 3.8,
      "spike_detected": false,
      "churned_last_30d": 2,
      "at_risk_count": 5,
      "revenue_at_risk": 100
    },
    "runway": {
      "months": 18.4,
      "is_profitable": false,
      "net_burn": 46,
      "available_cash": 10000
    },
    "engagement": {
      "activation_rate": 78.5,
      "d7_retention": 62.0,
      "d30_retention": 45.0,
      "dau_mau_ratio": 0.22,
      "ttfv_median_hours": 4.2
    },
    "health_distribution": {
      "critical": 2,
      "high": 3,
      "medium": 8,
      "low": 39,
      "total": 52
    }
  },
  "signals": [
    {
      "severity": "warning",
      "signal": "churn_approaching_spike",
      "message": "30d churn (4.2%) approaching 2x the 90d baseline (3.8%). Monitor closely.",
      "evidence": { "current": 4.2, "baseline": 3.8, "ratio": 1.1 },
      "suggested_action": "your-cli analytics at-risk --json --sort revenue"
    }
  ],
  "next_actions": [
    "your-cli analytics at-risk --json --sort revenue",
    "your-cli analytics insights --json --severity critical"
  ]
}
```

---

## Diff Endpoint (What Changed Since Last Check)

For recurring agent monitoring, the diff is vastly more token-efficient than re-reading the full summary:

```json
{
  "ok": true,
  "period": { "from": "2026-03-23T02:15:00Z", "to": "2026-03-24T02:15:00Z" },
  "changes": [
    {
      "metric": "mrr",
      "previous": 1200,
      "current": 1240,
      "delta": 40,
      "delta_pct": 3.3,
      "direction": "up",
      "significance": "normal"
    },
    {
      "metric": "churn_rate_30d",
      "previous": 3.8,
      "current": 8.2,
      "delta": 4.4,
      "delta_pct": 115.8,
      "direction": "up",
      "significance": "anomaly",
      "z_score": 3.2
    }
  ],
  "new_events": [
    { "type": "subscription_cancelled", "user_id": "user_abc", "at": "2026-03-23T14:00:00Z" },
    { "type": "subscription_created", "user_id": "user_xyz", "at": "2026-03-23T09:30:00Z" }
  ],
  "new_insights": [
    { "severity": "warning", "id": "churn-spike", "title": "Churn spike detected" }
  ]
}
```

**The `significance` field is critical.** It tells the agent whether a change is `normal` (ignore), `notable` (mention in report), or `anomaly` (alert immediately) — pre-computed using the same Z-score / threshold logic as the human insight engine.

---

## At-Risk Subscriber List

The most actionable endpoint. Returns subscribers sorted by intervention priority:

```json
{
  "ok": true,
  "at_risk_subscribers": [
    {
      "user_id": "user_abc",
      "email": "alice@example.com",
      "health_score": 22,
      "churn_risk": "critical",
      "churn_probability": 0.78,
      "monthly_revenue": 20,
      "days_since_last_activity": 18,
      "subscription_age_days": 45,
      "top_drivers": ["30d_inactive", "declining_usage", "narrow_workflow"],
      "recommended_intervention": "rescue_email",
      "cooldown_remaining_hours": 0,
      "expected_save_probability": 0.15
    }
  ],
  "summary": {
    "total_at_risk": 5,
    "total_revenue_at_risk": 100,
    "critical_count": 2,
    "high_count": 3,
    "interventions_ready": 4,
    "interventions_on_cooldown": 1
  }
}
```

**Agent workflow:** Read list → for each user with `cooldown_remaining_hours == 0` and `expected_save_probability > 0.1` → trigger intervention → log action.

---

## REST API Design

Mirror the CLI tree as REST endpoints. Same JSON response schema:

```
GET  /api/admin/robot/summary
GET  /api/admin/robot/diff?since=24h
GET  /api/admin/robot/revenue?range=30d
GET  /api/admin/robot/churn?window=30
GET  /api/admin/robot/at-risk?sort=revenue&limit=20
GET  /api/admin/robot/health?segment=critical
GET  /api/admin/robot/insights?severity=critical
GET  /api/admin/robot/projections?cash=10000
GET  /api/admin/robot/engagement?range=30d
GET  /api/admin/robot/cohorts?months=6
POST /api/admin/robot/monte-carlo     { "iterations": 1000, "months": 12 }
POST /api/admin/robot/scenarios       { "price": 25, "churnOverride": 0.03 }
POST /api/admin/robot/intervene       { "userId": "...", "action": "rescue_email" }
GET  /api/admin/robot/status
```

**Auth:** Same admin auth as human endpoints. Agent authenticates via API key or JWT.
**Content-Type:** Always `application/json`. No HTML fallback.
**Rate limiting:** Agent endpoints use highest tier — these are your own automation tools, not external API consumers.

---

## Autonomous Agent Workflows

### Daily Health Check (5-minute cron)

```
1. GET /api/admin/robot/summary
2. IF any signal.severity == "critical":
     GET /api/admin/robot/at-risk?sort=revenue
     FOR each critical user WHERE cooldown == 0:
       POST /api/admin/robot/intervene { userId, action: recommended_intervention }
     LOG: "Triggered {n} interventions for ${x} revenue at risk"
3. IF churn.spike_detected:
     GET /api/admin/robot/diff?since=7d
     ANALYZE: Correlate spike with product changes, payment failures, seasonal patterns
     COMPOSE: "Churn spike analysis: likely caused by {finding}"
4. COMPOSE executive summary from summary data + signals
5. SEND to human operator via Slack / email / notification
```

### Weekly Strategic Report

```
1. GET /api/admin/robot/summary
2. GET /api/admin/robot/cohorts?months=3
3. POST /api/admin/robot/monte-carlo { iterations: 5000, months: 12 }
4. GET /api/admin/robot/insights
5. COMPOSE report:
   - MRR trajectory + P10/P50/P90 outlook
   - Cohort comparison: is retention improving or degrading?
   - Top 3 insights with specific recommended actions
   - At-risk subscribers requiring human attention
   - Intervention effectiveness (if causal data available)
6. SEND to founder/exec
```

### Continuous Anomaly Monitor (every 5 minutes)

```
1. GET /api/admin/robot/diff?since=1h
2. IF any change.significance == "anomaly":
     GET /api/admin/robot/at-risk
     COMPOSE: alert with change context + affected subscribers
     SEND immediate notification
3. GET /api/admin/robot/status
4. IF data_freshness == "stale" OR stale_sources.length > 0:
     ALERT: "Analytics pipeline degraded: {stale_sources}"
```

---

## Interpretation Templates for Agent Reports

### Executive Summary

```
## {product_name} Analytics Brief — {date}

**Revenue:** MRR is ${mrr} ({direction} {delta_pct}% month-over-month).
{IF is_profitable}Profitable at ${profit}/month.
{ELSE}Burning ${burn}/month — {runway_months} months runway remaining.{ENDIF}

**Subscribers:** {subscriber_count} active ({new_last_30d} new, {churned_last_30d} churned).
Monthly churn rate: {churn_rate_30d}%.

**Health:** {critical + high} subscribers at elevated churn risk,
representing ${revenue_at_risk}/month in recurring revenue.

{FOR EACH signal IN signals}
**{severity}:** {message}
→ Recommended: {suggested_action}
{ENDFOR}

**12-Month Outlook:** Monte Carlo P50 projects MRR at ${p50_mrr}.
Range: ${p10_mrr} (pessimistic) to ${p90_mrr} (optimistic).
Survival probability: {survival_pct}%.
```

### At-Risk Alert

```
## At-Risk: {email} (Health: {health_score}/100)

**Churn probability:** {churn_probability}%
**Monthly revenue:** ${revenue}
**Last active:** {days_since_activity} days ago

**Risk drivers:**
{FOR EACH driver IN top_drivers}
- {driver.label} (category: {driver.category}, impact: {driver.impact})
{ENDFOR}

**Recommended:** {recommended_intervention}
{IF cooldown > 0}Cooldown active — {cooldown} hours remaining.
{ELSE}Ready for intervention.{ENDIF}
```

---

## Token Efficiency Patterns

### Compact Mode (`--compact`)

Standard output uses readable keys. Compact mode uses abbreviated keys for 40-60% token savings:

| Standard Key | Compact Key | Savings |
|-------------|------------|---------|
| `monthly_recurring_revenue` | `mrr` | 80% |
| `delta_percent` | `d%` | 75% |
| `subscribers` | `subs` | 60% |
| `health_score` | `hs` | 75% |
| `churn_probability` | `cp` | 70% |
| `days_since_last_activity` | `idle_d` | 65% |
| `subscription_age_days` | `age_d` | 55% |
| `recommended_intervention` | `rec` | 70% |

### Omission Rules (Compact Mode)

- Omit fields with null/undefined value
- Omit empty arrays (`[]`)
- Omit boolean `false` (false is the default)
- Numbers as numbers, never strings (`1240` not `"1240"`)
- Dates as Unix epoch in compact mode (not ISO 8601)

```json
// STANDARD (89 tokens):
{ "mrr": 1240, "is_profitable": false, "monthly_profit": null, "stale_sources": [], "signals": [] }

// COMPACT (18 tokens):
{ "mrr": 1240 }
```

---

## MCP Server Integration

For agents that support the Model Context Protocol, expose analytics as MCP tools:

```json
{
  "tools": [
    {
      "name": "saas_analytics_summary",
      "description": "Full SaaS business state: MRR, churn, health, runway, engagement, pre-computed signals",
      "inputSchema": { "type": "object", "properties": {} }
    },
    {
      "name": "saas_analytics_diff",
      "description": "What changed in analytics since a given period. Returns only deltas with significance scores.",
      "inputSchema": {
        "type": "object",
        "properties": { "since": { "type": "string", "default": "24h", "description": "Period: 1h, 24h, 7d" } }
      }
    },
    {
      "name": "saas_analytics_at_risk",
      "description": "At-risk subscribers ranked by revenue impact with intervention recommendations",
      "inputSchema": {
        "type": "object",
        "properties": {
          "limit": { "type": "integer", "default": 10 },
          "sort": { "type": "string", "enum": ["revenue", "churn", "health"], "default": "revenue" }
        }
      }
    },
    {
      "name": "saas_analytics_intervene",
      "description": "Trigger a retention intervention (email, notification) for an at-risk subscriber",
      "inputSchema": {
        "type": "object",
        "properties": {
          "userId": { "type": "string", "description": "Target subscriber user ID" },
          "action": { "type": "string", "enum": ["rescue_email", "setup_guide", "notification", "churn_prediction"] }
        },
        "required": ["userId", "action"]
      }
    },
    {
      "name": "saas_analytics_monte_carlo",
      "description": "Run Monte Carlo simulation for revenue projections with P10/P50/P90 ranges",
      "inputSchema": {
        "type": "object",
        "properties": {
          "iterations": { "type": "integer", "default": 1000, "maximum": 10000 },
          "months": { "type": "integer", "default": 12, "maximum": 120 }
        }
      }
    }
  ]
}
```

This lets any MCP-compatible agent (Claude Code, Cursor, Codex, etc.) autonomously monitor and manage your SaaS analytics without custom integration code.

---

## Safety Guardrails

### Read vs Write Permissions

| Action Category | Agent Autonomy | Rationale |
|----------------|---------------|-----------|
| **Read any metric** | Autonomous | Pure observation, no side effects |
| **Generate reports** | Autonomous | Text output, no system changes |
| **Trigger email/notification intervention** | Autonomous (within cooldown) | Low-cost, reversible, cooldown prevents spam |
| **Run Monte Carlo / scenarios** | Autonomous (rate-limited) | CPU-intensive but no side effects |
| **Cancel subscription** | Human approval required | Irreversible revenue impact |
| **Issue refund** | Human approval required | Direct financial impact |
| **Change pricing** | Human approval required | Affects all future revenue |
| **Modify intervention rules** | Human approval required | Changes system behavior |
| **Delete user data** | Human approval required | Legal/compliance implications |

### Cooldown Enforcement

```
IF intervention.cooldown_remaining_hours > 0:
  SKIP intervention
  LOG: "Cooldown active for {user_id}, skipping {action}"

IF daily_intervention_count > max_daily_interventions:
  STOP all interventions
  ALERT: "Daily intervention budget exhausted ({count}/{max})"
```

### Audit Trail

Every agent action must be logged:

```json
{
  "actor": "agent:daily_monitor",
  "action": "trigger_intervention",
  "target": "user_abc",
  "intervention": "rescue_email",
  "reason": "health_score=22, churn_probability=0.78",
  "timestamp": "2026-03-24T02:15:00Z"
}
```

This enables: "what did the agent do today?" queries and intervention effectiveness measurement.

---

## Testing Agent Interfaces

### Contract Tests

For every endpoint, verify:
- Response matches the TypeScript interface exactly
- `ok: true` when data is available
- `ok: false` with `error` object when data is unavailable
- `signals` array is never null (empty array, not null)
- `next_actions` contains valid, executable commands
- `data_freshness` accurately reflects actual data age
- Compact mode omits expected fields

### Replay Tests

Record real agent sessions and replay:
1. Capture agent's sequence of API calls + responses
2. Replay against a test environment with known data
3. Verify agent reaches the same conclusions and actions
4. Regression: if agent behavior changes, something in the API changed

### Load Tests

Agent monitoring every 5 minutes means 288 summary calls/day. At 10 agents across different projects, that's 2,880 calls/day. Verify:
- Summary endpoint responds in < 200ms (cached)
- Diff endpoint responds in < 500ms
- Monte Carlo endpoint responds in < 2s (rate-limited to 12/min)
