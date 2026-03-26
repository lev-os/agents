---
name: testing-real-service-e2e-no-mocks
description: >-
  Build mock-free integration and E2E tests that hit real databases, real APIs,
  and real services with structured logging. Use when: replacing mocked tests
  with real-DB tests, transaction rollback isolation, test data factories,
  structured JSON-line test logging, webhook simulation, or billing flow
  verification. Covers Vitest, Supabase, Stripe test mode, and testcontainers.
metadata:
  filePattern:
    - "**/integration/**"
    - "**/e2e/**"
    - "**/test-db*"
    - "**/test*factory*"
    - "**/test*harness*"
  bashPattern:
    - "\\b(REAL_API_TESTS|integration.test|test.db|transaction.rollback|test.factory)\\b"
  priority: 60
---

# Perfect E2E & Integration Tests (No Mocks)

> **The One Rule:** If a mock hides a bug that would break production,
> the mock is worse than no test at all. Test the real thing.

> **The Case Against Mocks:** Every mock is a lie about how the system works.
> Mocks pass when reality fails. The more critical the path (billing, auth,
> data deletion), the more dangerous the mock. Test real databases, real APIs,
> real webhooks, real payment providers in test mode.

## The Loop (Mandatory)

```
1. IDENTIFY    → Which mocked test hides the most production risk?
2. PROVISION   → Set up real test infrastructure (DB, API keys, webhooks)
3. ISOLATE     → Transaction rollback per test (no shared state, no cleanup)
4. FACTORY     → Build test data factories (realistic, not minimal)
5. LOG         → Structured JSON-line logging: phase, timing, DB snapshots
6. VERIFY      → Assert against real responses, not mocked return values
7. GUARD       → Production URL blocklist — never hit prod from tests
8. REGRESSION  → Every production bug → mock-free regression test
```

## Mock Risk Assessment Matrix

Before writing a test, score how dangerous mocking is:

| Code Path | Production Impact | Mock Divergence Risk | Last Bug from Mock | Score |
|-----------|:-----------------:|:--------------------:|:------------------:|-------|
| *function* | 1-5 (revenue/data) | 1-5 (how often mock lies) | date or N/A | Impact × Risk |

**Rule:** Score ≥ 8 = MUST be mock-free. Score ≥ 4 = SHOULD be mock-free.
Score < 4 = mock is acceptable (low-risk helper functions).

---

## The Anti-Mock Manifesto

### Why Mocks Lie

| Mock Pattern | The Lie | The Production Bug It Hides |
|-------------|---------|----------------------------|
| `vi.mock("@/lib/db/client")` | DB always responds instantly | Connection pool exhaustion, query timeout |
| `mockStripe.subscriptions.cancel.mockResolvedValue({})` | Stripe always succeeds | Rate limiting, network errors, invalid subscription state |
| `vi.mock("@/lib/email/sender")` | Emails always send | Template rendering errors, DNS failures, rate limits |
| `mockDb.query.subscriptions.findMany.mockResolvedValue([{status: "active"}])` | Data shape matches reality | Schema drift, missing columns, wrong types |
| `vi.mock("@/lib/services/subscription")` | Business logic works | Cascade deletion, grace period edge cases |

### The Fix: Test Pyramid Without Mocks

```
                    ┌──────────┐
                    │  E2E     │  Real browser, real API, real payment provider
                    │ (few)    │  Stripe test mode, PayPal sandbox
                    ├──────────┤
                    │ Integr.  │  Real DB (transaction rollback), real services
                    │ (many)   │  Factory-seeded data, structured logging
                    ├──────────┤
                    │  Unit    │  Pure functions ONLY — no I/O, no DB, no network
                    │ (most)   │  Mocks acceptable ONLY for pure function deps
                    └──────────┘
```

**Critical insight:** Most projects have an inverted pyramid (many unit tests
with mocks, few integration tests). Flip it for critical paths.

---

## Pattern 1: Transaction Rollback Isolation

The foundation pattern. Every test runs in a transaction that's rolled back.
Zero cleanup needed. Zero shared state.

```typescript
// tests/utils/test-db.ts
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import { beforeAll, beforeEach, afterEach, afterAll } from "vitest";

let testDb: PostgresJsDatabase;
let testSql: postgres.Sql;

export function withTestTransaction(options?: { suiteName?: string }) {
  beforeAll(async () => {
    testSql = postgres(TEST_DATABASE_URL, {
      prepare: false,
      max: 1,           // Single connection for transaction isolation
      idle_timeout: 0,   // Keep alive for test duration
    });
    testDb = drizzle(testSql, { schema });
  });

  beforeEach(async () => {
    await testSql`BEGIN`;
    await testSql`SAVEPOINT test_savepoint`;
  });

  afterEach(async () => {
    await testSql`ROLLBACK TO SAVEPOINT test_savepoint`;
    await testSql`ROLLBACK`;
  });

  afterAll(async () => {
    await testSql.end();
  });
}

export function getTestDb() { return testDb; }
```

**Usage:**
```typescript
describe("Subscription lifecycle", () => {
  withTestTransaction({ suiteName: "sub_lifecycle" });

  it("creates active subscription", async () => {
    const db = getTestDb();
    // Insert real data into real database
    const [user] = await db.insert(users).values({
      email: "test@example.com",
      subscriptionStatus: "none",
    }).returning();

    const [sub] = await db.insert(subscriptions).values({
      userId: user.id,
      provider: "stripe",
      externalId: "sub_test_123",
      status: "active",
      currentPeriodStart: new Date(),
      currentPeriodEnd: new Date(Date.now() + 30 * 86400000),
    }).returning();

    expect(sub.status).toBe("active");
    expect(sub.userId).toBe(user.id);
    // Transaction rolls back automatically — no cleanup needed
  });
});
```

---

## Pattern 2: Test Data Factories

Factories create REALISTIC test data, not minimal stubs.

```typescript
// tests/utils/test-user-factory.ts
import { randomUUID } from "node:crypto";

interface UserFactoryOptions {
  email?: string;
  subscriptionStatus?: SubscriptionStatus;
  isAdmin?: boolean;
  customerId?: string;
}

export async function createTestUser(
  db: PostgresJsDatabase,
  options: UserFactoryOptions = {}
): Promise<User> {
  const defaults = {
    id: randomUUID(),
    email: `test-${randomUUID().slice(0, 8)}@test.jeffreys-skills.md`,
    subscriptionStatus: "none" as const,
    isAdmin: false,
    customerId: `cus_test_${randomUUID().slice(0, 8)}`,
    displayName: "Test User",
    createdAt: new Date(),
    updatedAt: new Date(),
  };

  const [user] = await db.insert(users)
    .values({ ...defaults, ...options })
    .returning();

  return user;
}

// Subscription factory — creates full subscription chain
export async function createTestSubscription(
  db: PostgresJsDatabase,
  userId: string,
  options: Partial<typeof subscriptions.$inferInsert> = {}
): Promise<Subscription> {
  const defaults = {
    id: randomUUID(),
    userId,
    provider: "stripe" as const,
    externalId: `sub_test_${randomUUID().slice(0, 8)}`,
    status: "active" as const,
    currentPeriodStart: new Date(),
    currentPeriodEnd: new Date(Date.now() + 30 * 86400000),
    createdAt: new Date(),
    updatedAt: new Date(),
  };

  const [sub] = await db.insert(subscriptions)
    .values({ ...defaults, ...options })
    .returning();

  // Also update the denormalized users table
  await db.update(users)
    .set({
      subscriptionStatus: sub.status,
      subscriptionProvider: sub.provider,
      customerId: options.customerId ?? defaults.externalId,
    })
    .where(eq(users.id, userId));

  return sub;
}
```

---

## Pattern 3: Structured Test Logging

Every mock-free test MUST produce structured logs. When a test fails in CI,
you need to know the DB state, the timing, and the exact assertion failure.

```typescript
// tests/utils/test-logger.ts
export class TestLogger {
  testStart(name: string): void;
  phase(p: "setup" | "act" | "assert" | "teardown"): void;
  dbSnapshot(table: string, rows: unknown[], label?: string): void;
  assertMatch(field: string, expected: unknown, actual: unknown): boolean;
  testEnd(result: "pass" | "fail"): void;
  summary(): SuiteSummary;
}

// Vitest integration: auto-tracks test lifecycle
export function withTestLogging(suite: string): TestLogger;
```

**Usage in tests:**
```typescript
describe("Webhook idempotency", () => {
  const log = withTestLogging("webhook-idempotency");
  withTestTransaction();

  it("rejects duplicate webhook events", async () => {
    const db = getTestDb();

    log.phase("setup");
    const user = await createTestUser(db);
    const sub = await createTestSubscription(db, user.id);
    log.dbSnapshot("subscriptions", [sub], "before_webhook");

    log.phase("act");
    const event1 = await recordWebhookEvent({
      provider: "stripe",
      eventId: "evt_123",
      eventType: "customer.subscription.updated",
      payload: {},
    });
    const event2 = await recordWebhookEvent({
      provider: "stripe",
      eventId: "evt_123", // Same event ID — duplicate
      eventType: "customer.subscription.updated",
      payload: {},
    });

    log.phase("assert");
    log.assertMatch("first event recorded", true, event1);
    log.assertMatch("duplicate rejected", false, event2);
    expect(event1).toBe(true);
    expect(event2).toBe(false);  // Idempotency check
  });
});
```

**JSON-line output (to stderr, machine-parseable):**
```json
{"ts":"2026-03-23T07:10:11Z","suite":"webhook-idempotency","test":"rejects duplicate","phase":"setup","event":"phase_start"}
{"ts":"2026-03-23T07:10:11Z","suite":"webhook-idempotency","test":"rejects duplicate","phase":"setup","event":"db_snapshot","data":{"table":"subscriptions","row_count":1}}
{"ts":"2026-03-23T07:10:11Z","suite":"webhook-idempotency","test":"rejects duplicate","phase":"assert","event":"assertion","data":{"field":"first event recorded","expected":true,"actual":true,"match":true}}
{"ts":"2026-03-23T07:10:11Z","suite":"webhook-idempotency","test":"rejects duplicate","event":"test_end","data":{"result":"pass","duration_ms":45}}
```

---

## Pattern 4: Production Safety Guards

**Non-negotiable.** Test infrastructure MUST block production URLs.

```typescript
// tests/utils/real-db-harness.ts
const PROD_URLS = [
  "https://ircpwyadlwkkqivhegsy.supabase.co",  // Production Supabase
  "https://auth.jeffreys-skills.md",             // Production auth
];

export function getRealDbConfig(): { enabled: boolean; reason?: string } {
  if (env.REAL_API_TESTS !== "true") {
    return { enabled: false, reason: "REAL_API_TESTS not set" };
  }
  if (env.NODE_ENV === "production") {
    return { enabled: false, reason: "NODE_ENV=production" };
  }
  if (PROD_URLS.includes(env.NEXT_PUBLIC_SUPABASE_URL)) {
    return { enabled: false, reason: "Supabase URL is PRODUCTION" };
  }
  return { enabled: true };
}
```

```bash
# Environment validation before running tests
bun scripts/provision-test-env.ts --check
# Validates:
# - Supabase URL is NOT production
# - Stripe key is sk_test_* (NOT sk_live_*)
# - PayPal is sandbox mode
# - NODE_ENV is NOT production
```

---

## Pattern 5: Real Payment Provider Testing

```typescript
// Test with Stripe test mode — real API, fake money
describe("Stripe checkout flow", () => {
  withTestTransaction();

  it("creates checkout session with test mode keys", async () => {
    // Uses sk_test_* key — no real charges
    const session = await stripe.checkout.sessions.create({
      mode: "subscription",
      line_items: [{ price: env.STRIPE_PRICE_ID, quantity: 1 }],
      success_url: "http://localhost:3000/success",
      cancel_url: "http://localhost:3000/cancel",
      customer_email: "test@example.com",
    });

    expect(session.id).toMatch(/^cs_test_/);
    expect(session.url).toBeTruthy();
  });
});
```

---

## Pattern 6: Cleanup Registry (Safety Net)

For tests that can't use transaction rollback (e.g., cross-service tests):

```typescript
class CleanupRegistry {
  private entries: Array<{ type: string; id: string }> = [];

  track(type: string, id: string): void {
    this.entries.push({ type, id });
  }

  async cleanup(): Promise<{ cleaned: number; failed: number }> {
    let cleaned = 0, failed = 0;
    // Cleanup in reverse order (LIFO — respects FK constraints)
    for (const entry of this.entries.reverse()) {
      try {
        await this.deleteByType(entry.type, entry.id);
        cleaned++;
      } catch (e) {
        failed++;
      }
    }
    this.entries = [];
    return { cleaned, failed };
  }
}
```

---

## The Migration Path: Mocked → Mock-Free

When replacing an existing mocked test with a real-DB test:

```
1. READ the mocked test — understand WHAT it tests (not HOW)
2. IDENTIFY the assertions — what behavior is being verified?
3. CHECK if mock constants match reality:
   - Are mocked response shapes current? (schema drift?)
   - Are mocked status values current? (enum changes?)
   - Are mocked business rules current? (policy changes?)
4. WRITE the mock-free version using real DB + factories
5. RUN BOTH side by side — same assertions, different infrastructure
6. VERIFY the mock-free version catches bugs the mock didn't
7. DELETE the mocked version (don't keep both!)
```

**Common mock-reality divergences that cause production bugs:**
- Mocked `onDelete: "cascade"` — mock doesn't cascade, real DB does
- Mocked subscription status — mock allows transitions that business logic prevents
- Mocked webhook payloads — real webhook has fields the mock doesn't include
- Mocked email templates — mock doesn't render, so template errors go undetected

---

## Anti-Patterns (Hard Constraints)

| ✗ Never | Why | Fix |
|---------|-----|-----|
| Mock the database for billing tests | Hides cascade, FK, and transaction bugs | Transaction rollback isolation |
| Share state between tests | Order-dependent failures, flaky tests | Each test gets its own transaction |
| Skip structured logging | CI failures are undebuggable | JSON-line output with phase/timing/snapshots |
| Use production URLs in test env | One bad test can charge real money or delete real data | Production URL blocklist |
| Keep both mocked and mock-free versions | Maintenance burden, false confidence | Delete the mock when mock-free is proven |
| Hard-code test data | Fragile, doesn't catch edge cases | Use factories with randomized defaults |
| Forget cleanup for cross-service tests | Test data accumulates, contaminates MRR | Cleanup registry with LIFO ordering |
| Test against `localhost:3000` without running server | Silent pass with no actual verification | CI must start dev server or use direct imports |

---

## Checklist (Before Shipping Mock-Free Test Suite)

- [ ] Transaction rollback isolation for every test
- [ ] Test data factories (not hard-coded data)
- [ ] Structured JSON-line logging (phase, timing, DB snapshots)
- [ ] Production URL blocklist in test harness
- [ ] Stripe/PayPal use test mode keys (sk_test_*, sandbox)
- [ ] `provision-test-env.ts --check` validates all required env vars
- [ ] Mock Risk Matrix scored: all Score ≥ 8 paths are mock-free
- [ ] Cleanup registry for tests that can't use transactions
- [ ] Every production bug has a mock-free regression test
- [ ] Mocked versions deleted after mock-free is proven working
- [ ] CI runs mock-free tests on every PR

---

## References

| Need | Reference |
|------|-----------|
| Transaction rollback deep-dive | [TRANSACTION-ISOLATION.md](references/TRANSACTION-ISOLATION.md) |
| Factory patterns catalog | [FACTORIES.md](references/FACTORIES.md) |
| Structured logging formats | [LOGGING-FORMATS.md](references/LOGGING-FORMATS.md) |
| Payment provider test modes | [PAYMENT-TESTING.md](references/PAYMENT-TESTING.md) |
| Migration playbook: mock → real | [MIGRATION-PLAYBOOK.md](references/MIGRATION-PLAYBOOK.md) |

## Relationship to Other Testing Skills

| Technique | Use INSTEAD when | Use TOGETHER when |
|-----------|-----------------|-------------------|
| /testing-golden-artifacts | Output is complex, needs frozen reference | Goldens verify output of mock-free tests |
| /testing-conformance-harnesses | Testing against a spec, not just correctness | Conformance suite uses real DB harness |
| /testing-fuzzing | Finding crashes in parsers | Fuzz-found crashes become mock-free regression tests |
| /testing-metamorphic | Can't compute expected output | MRs validate relations in mock-free integration tests |
| /e2e-testing-for-webapps | Browser-level testing | E2E flows use same real-DB infrastructure |
