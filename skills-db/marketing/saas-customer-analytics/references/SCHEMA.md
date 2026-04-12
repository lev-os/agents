# Database Schema Patterns

> The schema is the contract between your payment pipeline, analytics engine, and dashboard. Get it right once.

## Core Tables

### 1. Users

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  display_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 2. Subscriptions (Mutable Current State)

```sql
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  provider TEXT NOT NULL,              -- 'stripe' | 'paypal' | 'gratis'
  external_id TEXT,                    -- Stripe sub ID or PayPal sub ID
  status TEXT NOT NULL DEFAULT 'none', -- 'none' | 'active' | 'past_due' | 'cancelled' | 'paused_for_org'
  last_event_at TIMESTAMPTZ,          -- Event ordering protection
  current_period_start TIMESTAMPTZ,
  current_period_end TIMESTAMPTZ,
  cancelled_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(provider, external_id)
);

CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_cancelled ON subscriptions(cancelled_at);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
```

**Key design decisions:**
- `last_event_at` prevents stale webhooks from overwriting newer state
- `past_due` is still "active" for MRR purposes (grace period)
- `paused_for_org` is for users who moved to an org subscription
- One user can have multiple subscription records (history)

### 3. Payment Events (Immutable Ledger)

```sql
CREATE TABLE payment_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  provider TEXT NOT NULL,
  event_type TEXT NOT NULL,
  event_id TEXT NOT NULL,
  user_id UUID REFERENCES users(id),
  payload JSONB NOT NULL,
  processed_at TIMESTAMPTZ,
  reconciled_at TIMESTAMPTZ,
  retry_count INTEGER DEFAULT 0,
  last_error TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(provider, event_id)
);

CREATE INDEX idx_pe_unprocessed ON payment_events(created_at) WHERE processed_at IS NULL;
CREATE INDEX idx_pe_user ON payment_events(user_id, created_at);
CREATE INDEX idx_pe_type ON payment_events(event_type, created_at);
```

**NEVER modify or delete rows.** This is your financial audit trail.

### 4. Organizations (Team Billing)

```sql
CREATE TABLE organizations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  owner_user_id UUID NOT NULL REFERENCES users(id),
  billing_email TEXT,
  subscription_status TEXT DEFAULT 'none',
  max_seats INTEGER DEFAULT 3,

  -- Stripe
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  stripe_last_event_at TIMESTAMPTZ,

  -- PayPal
  paypal_customer_id TEXT,
  paypal_subscription_id TEXT,
  paypal_plan_id TEXT,
  paypal_payer_id TEXT,
  paypal_status TEXT,
  paypal_last_event_at TIMESTAMPTZ,

  -- Checkout state
  pending_checkout_provider TEXT,
  pending_checkout_session_id TEXT,
  pending_checkout_url TEXT,
  pending_checkout_expires_at TIMESTAMPTZ,

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 5. Usage Events (Append-Only Analytics)

```sql
CREATE TABLE usage_events (
  id UUID PRIMARY KEY,              -- Client-supplied for idempotency
  user_id UUID NOT NULL REFERENCES users(id),
  skill_id TEXT,                    -- Feature/product ID
  skill_name TEXT,                  -- Feature/product name
  event_type TEXT NOT NULL,         -- 'invoke' | 'install' | 'uninstall' | 'update' | 'search'
  timestamp TIMESTAMPTZ NOT NULL,
  duration_ms INTEGER,
  success BOOLEAN DEFAULT true,
  error_code TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_ue_user_time ON usage_events(user_id, timestamp);
CREATE INDEX idx_ue_skill_time ON usage_events(skill_id, timestamp);
CREATE INDEX idx_ue_time ON usage_events(timestamp);
```

**Client-supplied ID**: Allows CLI/client to retry without duplicates.

### 6. Usage Stats Daily (Precomputed Aggregates)

```sql
CREATE TABLE usage_stats_daily (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  date DATE NOT NULL,
  total_skill_uses INTEGER DEFAULT 0,
  unique_skills_used INTEGER DEFAULT 0,
  UNIQUE(user_id, date)
);
```

Populated by daily cron job for sub-500ms dashboard queries.

---

## Analytics-Specific Tables

### 7. Customer Health Scores

```sql
CREATE TABLE customer_health_scores (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) UNIQUE,
  health_score INTEGER NOT NULL,        -- 0-100
  churn_risk TEXT NOT NULL,             -- 'low' | 'medium' | 'high' | 'critical'
  engagement_score INTEGER NOT NULL,    -- 0-25
  breadth_score INTEGER NOT NULL,       -- 0-25
  recency_score INTEGER NOT NULL,       -- 0-25
  payment_score INTEGER NOT NULL,       -- 0-25
  factors JSONB,                        -- Full factor details
  calculated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 8. Customer Health History

```sql
CREATE TABLE customer_health_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  health_score INTEGER NOT NULL,
  calculated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_chh_user_time ON customer_health_history(user_id, calculated_at);
```

Enables trend detection (improving/stable/declining).

### 9. Churn Predictions

```sql
CREATE TABLE churn_predictions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  risk_score INTEGER NOT NULL,
  risk_level TEXT NOT NULL,
  factors JSONB NOT NULL,
  recommended_actions JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 10. Intervention Rules & Executions

```sql
CREATE TABLE intervention_rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE,
  description TEXT,
  enabled BOOLEAN DEFAULT true,
  subject_type TEXT NOT NULL,         -- 'user' | 'organization'
  conditions JSONB NOT NULL,
  threshold JSONB NOT NULL,
  actions JSONB NOT NULL,
  cooldown_hours INTEGER DEFAULT 168,
  priority INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE intervention_executions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  rule_id UUID NOT NULL REFERENCES intervention_rules(id),
  subject_type TEXT NOT NULL,
  subject_id TEXT NOT NULL,
  actions_taken JSONB NOT NULL,
  metrics_snapshot JSONB,
  executed_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE intervention_outcomes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  execution_id UUID NOT NULL REFERENCES intervention_executions(id),
  outcome TEXT NOT NULL,
  measured_at TIMESTAMPTZ,
  days_after_intervention INTEGER
);
```

### 11. Insight Dismissals

```sql
CREATE TABLE insight_dismissals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  insight_id TEXT NOT NULL,
  admin_user_id UUID NOT NULL REFERENCES users(id),
  dismissed_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ NOT NULL     -- 7 days from dismissal
);
```

### 12. AI Briefs

```sql
CREATE TABLE ai_briefs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  type TEXT NOT NULL,                 -- 'daily' | 'weekly'
  summary TEXT NOT NULL,
  highlights JSONB,
  alerts JSONB,
  recommendations JSONB,
  metrics JSONB NOT NULL,
  generated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 13. Audit Log

```sql
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  event_type TEXT NOT NULL,
  event_data JSONB,
  ip_address TEXT,
  user_agent TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_user ON audit_log(user_id);
CREATE INDEX idx_audit_type ON audit_log(event_type);
CREATE INDEX idx_audit_time ON audit_log(created_at);
```

---

## Query Patterns

### MRR Calculation Query

```sql
-- Individual MRR
SELECT COUNT(*)::int AS count
FROM subscriptions s
INNER JOIN users u ON s.user_id = u.id
WHERE s.status IN ('active', 'past_due')
  AND s.provider IN ('stripe', 'paypal')
  AND u.email NOT LIKE '%@test.yourdomain.com';

-- Organization MRR (fetch seat counts, calculate in app)
SELECT subscription_status, max_seats
FROM organizations
WHERE subscription_status IN ('active', 'past_due')
  AND (stripe_subscription_id IS NOT NULL OR paypal_subscription_id IS NOT NULL)
  AND COALESCE(stripe_subscription_id, '') NOT LIKE 'sub_test_%'
  AND name NOT LIKE 'E2E Team%';
```

### Churn Rate Query

```sql
-- Active at start of period
SELECT COUNT(*)
FROM subscriptions
WHERE created_at < :period_start
  AND (cancelled_at IS NULL OR cancelled_at >= :period_start);

-- Churned during period
SELECT COUNT(*)
FROM subscriptions
WHERE cancelled_at >= :period_start
  AND cancelled_at < :period_end;
```

### Behavioral Profile Query

```sql
-- Activity counts for a subscriber
SELECT
  COUNT(DISTINCT DATE(timestamp)) FILTER (WHERE timestamp >= NOW() - INTERVAL '7 days') AS active_days_7,
  COUNT(DISTINCT DATE(timestamp)) FILTER (WHERE timestamp >= NOW() - INTERVAL '30 days') AS active_days_30,
  COUNT(*) FILTER (WHERE timestamp >= NOW() - INTERVAL '7 days') AS events_7,
  COUNT(*) FILTER (WHERE timestamp >= NOW() - INTERVAL '14 days') AS events_14,
  COUNT(*) FILTER (WHERE timestamp >= NOW() - INTERVAL '30 days') AS events_30,
  COUNT(*) FILTER (WHERE timestamp >= NOW() - INTERVAL '28 days' AND timestamp < NOW() - INTERVAL '14 days') AS events_prev_14,
  COUNT(DISTINCT event_type) FILTER (WHERE timestamp >= NOW() - INTERVAL '30 days') AS unique_types_30,
  COUNT(DISTINCT skill_id) FILTER (WHERE timestamp >= NOW() - INTERVAL '30 days') AS unique_skills_30
FROM usage_events
WHERE user_id = :user_id;
```

### Payment Fee Aggregation

```sql
-- Fee report from immutable ledger
SELECT
  DATE(created_at) AS day,
  provider,
  COUNT(*) AS transaction_count,
  SUM((payload->>'amount')::numeric) AS total_amount
FROM payment_events
WHERE event_type IN ('invoice.payment_succeeded', 'PAYMENT.SALE.COMPLETED')
  AND created_at >= NOW() - INTERVAL ':days days'
GROUP BY DATE(created_at), provider
ORDER BY day;
```

---

## Migration Discipline

For every schema change:
1. Create SQL migration file with timestamp prefix
2. Run migration before deploying code that depends on it
3. Test rollback path
4. Never leave schema drift for "later"
