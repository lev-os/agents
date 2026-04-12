# Resilience Patterns

> Your analytics are only as reliable as the event pipeline feeding them. One lost webhook = wrong MRR. One stuck cron = stale insights. Build for failure.

## Email Retry & Dead Letter Queue

### Retry Policy

```
Attempt 1: Immediate
Attempt 2: 1 minute later (initial delay)
Attempt 3: 2 minutes later (2x backoff)
Attempt 4: 4 minutes later
Attempt 5: 8 minutes later (capped at 1 hour)

Jitter: ±10% on each delay to prevent thundering herd
```

### Error Classification

| Error Type | Retryable? | Example |
|-----------|-----------|---------|
| `network_timeout` | Yes | DNS failure, connection reset |
| `rate_limit` | Yes | 429 from email provider |
| `server_error` | Yes | 500 from email provider |
| `invalid_email` | No | Malformed address |
| `auth_failure` | No | Bad API key |
| `validation_error` | No | Missing required field |
| `unsubscribed` | No | User opted out |
| `unknown` | First 2 only | Conservative approach |

### Dead Letter Queue (DLQ)

After max retries, move to DLQ for manual review:

```typescript
EmailDlqEntry {
  id: string;
  originalJobId: string;
  templateKey: string;
  recipientEmail: string;
  payload: JSONB;                   // Full original email payload
  contentHash: string;              // For deduplication
  errorHistory: Array<{             // Last 10 attempts
    attempt: number;
    timestamp: Date;
    errorType: string;
    message: string;
  }>;
  status: 'pending' | 'processed';
  processingResult: 'retried' | 'discarded' | null;
  retentionExpiresAt: Date;         // 30-day retention
}
```

### DLQ Operations

| Operation | When | Guard |
|-----------|------|-------|
| Retry | Admin reviews and wants to resend | Claim-based lock (15 min lease) |
| Discard | Permanently invalid (bad address) | Record discard reason |
| Auto-purge | After 30 days | Cron job |

### Lease-Based Claiming

Prevents two admins from retrying the same DLQ entry simultaneously:

```sql
UPDATE email_dlq
SET claimed_at = NOW(), claimed_by = :admin_id
WHERE id = :entry_id
  AND (claimed_at IS NULL OR claimed_at < NOW() - INTERVAL '15 minutes')
RETURNING *;
```

If `claimed_at` is recent, another admin is already handling it.

---

## Distributed Locking

### Redis-Based Lock (Optional)

```typescript
async function acquireLock(key: string, ttlMs: number): Promise<string | null> {
  const token = crypto.randomUUID();
  const result = await redis.set(key, token, { NX: true, PX: ttlMs });
  return result === 'OK' ? token : null;
}

async function releaseLock(key: string, token: string): Promise<boolean> {
  // Lua script: only release if we own it
  const script = `
    if redis.call("get", KEYS[1]) == ARGV[1] then
      return redis.call("del", KEYS[1])
    else
      return 0
    end
  `;
  return (await redis.eval(script, [key], [token])) === 1;
}
```

### PostgreSQL Advisory Locks (Transaction-Scoped)

For operations that must be serialized within a database transaction:

```sql
-- Acquire lock scoped to this transaction (auto-released on commit/rollback)
SELECT pg_advisory_xact_lock(hashtext('stripe:sub_xyz123'));

-- Now safe to read-modify-write subscription status
UPDATE subscriptions SET status = 'active' WHERE external_id = 'sub_xyz123';
```

**Use cases:**
- Subscription status updates (prevent concurrent webhook race conditions)
- Team seat count updates (prevent double-billing during concurrent checkouts)
- Payment event processing (prevent duplicate side effects)

### Graceful Fallback

If Redis is unavailable, the lock should degrade gracefully:

```typescript
async function withOptionalLock<T>(key: string, fn: () => Promise<T>): Promise<T> {
  try {
    const token = await acquireLock(key, 30_000);
    if (!token) throw new Error('Could not acquire lock');
    try {
      return await fn();
    } finally {
      await releaseLock(key, token);
    }
  } catch {
    // Redis down — proceed without lock, log warning
    logger.warn({ key }, 'Distributed lock unavailable, proceeding without');
    return fn();
  }
}
```

---

## Rate Limiting

### Tiered Architecture

| Tier | Rate | Who | Rationale |
|------|------|-----|-----------|
| Anonymous | 600 req/min | Unauthenticated | Prevent abuse |
| Authenticated | 30,000 req/min | Logged-in users | Generous but bounded |
| Subscriber | Unlimited* | Paying customers | Never block payers |
| CLI | 30,000 req/min | CLI clients | Same as authenticated |

*"Unlimited" = 10M req/min. Technically bounded but effectively infinite.

### Analytics Endpoint Overrides

Analytics endpoints are computationally expensive. Apply tighter limits:

| Endpoint | Anonymous | Authenticated | Subscriber |
|----------|-----------|--------------|------------|
| General API | 600/min | 30K/min | 10M/min |
| Analytics API | 2K/min | 20K/min | 10M/min |
| Monte Carlo | — | 12/min | 12/min |

### Subscriber Bypass

**Paying customers NEVER get rate limited.** This is a product decision, not a technical one. A rate-limited subscriber will churn.

```typescript
if (tier === 'subscriber') {
  // Skip Redis entirely — zero latency impact
  return { limited: false, remaining: Infinity };
}
```

### Redis Failure Handling

```typescript
// Exponential backoff on Redis failures (10s → 5min cap)
let redisBackoffMs = 0;
const BACKOFF_MAX = 300_000; // 5 minutes

async function checkRateLimit(key: string, limit: number): Promise<boolean> {
  if (redisBackoffMs > 0 && Date.now() < lastRedisFailure + redisBackoffMs) {
    return false; // Allow all during backoff (fail open)
  }

  try {
    const result = await redis.incr(key);
    redisBackoffMs = 0; // Reset on success
    return result > limit;
  } catch {
    redisBackoffMs = Math.min(BACKOFF_MAX, Math.max(10_000, redisBackoffMs * 2));
    lastRedisFailure = Date.now();
    return false; // Fail open — never block users due to Redis outage
  }
}
```

---

## Cron Job Architecture

### Analytics Cron Schedule

| Job | Schedule | Duration Limit | Purpose |
|-----|----------|---------------|---------|
| Webhook reconciliation | `*/5 * * * *` | 300s | Retry failed webhooks |
| Email retry | `*/5 * * * *` | 300s | Process email job queue |
| Dunning reminders | `0 9 * * *` | 60s | Send payment failure emails |
| Tag analytics | `0 3 * * *` | 300s | Aggregate daily tag metrics |
| Daily aggregates | `0 3 * * *` | 300s | Precompute usage_stats_daily |
| Monthly insights | `0 8 1 * *` | 120s | Generate monthly digest email |

### Cron Security

All cron endpoints must verify the `CRON_SECRET` header:

```typescript
export async function GET(request: NextRequest) {
  const authHeader = request.headers.get('authorization');
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return new Response('Unauthorized', { status: 401 });
  }
  // ... cron logic
}
```

### Cron Idempotency

Crons can be triggered multiple times (Vercel retries on timeout). Make them idempotent:

```typescript
// Tag analytics: upsert, not insert
await db.insert(tagMetrics)
  .values({ tagName, date, views, clicks })
  .onConflictDoUpdate({
    target: [tagMetrics.tagName, tagMetrics.date],
    set: { views: sql`EXCLUDED.views`, clicks: sql`EXCLUDED.clicks` },
  });
```

### Cron Monitoring

Each cron job should report its outcome:

```typescript
const result = {
  processed: 0,
  failed: 0,
  skipped: 0,
  alertsSent: 0,
  durationMs: Date.now() - startTime,
};

logger.info({ job: 'webhook-reconciliation', ...result }, 'Cron complete');
return Response.json(result);
```

---

## Admin Audit Logging

### Non-Blocking Pattern

Audit logging must NEVER block the admin action:

```typescript
async function logAdminAction(action: AdminAction): Promise<void> {
  try {
    await db.insert(auditLog).values({
      adminUserId: action.userId,
      actionType: action.type,
      entityType: action.entityType,
      entityId: action.entityId,
      beforeState: action.before,
      afterState: action.after,
      metadata: action.metadata,
      ipAddress: action.ip,
      userAgent: action.userAgent,
    });
  } catch (error) {
    // Log failure but DON'T throw — admin action should still succeed
    logger.error({ error, action }, 'Audit log write failed');
  }
}
```

### Audit Action Types

Comprehensive enum covering all admin operations:

| Category | Actions |
|----------|---------|
| User management | view_user, update_user, suspend_user |
| Subscription | manual_cancel, manual_extend, retry_payment |
| Content moderation | delist_skill, warn_user, restore_skill |
| Billing | refund, adjust_invoice, update_plan |
| Configuration | update_settings, rotate_key, toggle_feature |
| Support | respond_ticket, escalate, close_ticket |

### Before/After State

For any mutation, record what changed:

```typescript
{
  beforeState: { status: 'active', role: 'member' },
  afterState: { status: 'suspended', role: 'member' },
}
```

This enables rollback analysis and compliance auditing.

---

## Idempotency Checklist

Every write operation in the analytics pipeline should be idempotent:

- [ ] Webhook events: `UNIQUE(provider, event_id)` prevents duplicates
- [ ] Email jobs: Content hash deduplication within 24h window
- [ ] Cron aggregations: `ON CONFLICT DO UPDATE` (upsert)
- [ ] Subscription updates: `WHERE last_event_at < $new_event_at`
- [ ] DLQ operations: Lease-based claiming prevents concurrent processing
- [ ] Rate limit counters: Sliding window with atomic increment
- [ ] Intervention executions: Cooldown check before firing

---

## Failure Modes & Recovery

| Failure | Detection | Recovery |
|---------|-----------|---------|
| Webhook lost | Reconciliation cron finds unprocessed events | Auto-retry up to 5x |
| Email stuck | DLQ entry with `pending` status | Admin manual retry/discard |
| Cron missed | Monitoring alert on missing log entry | Manual trigger via API |
| Redis down | Backoff counter > 0 | Fail open (allow all), log warning |
| DB connection lost | Query timeout/error | Retry with backoff, circuit breaker |
| Stale webhook | `last_event_at` comparison | Silently skip (newer state preserved) |
