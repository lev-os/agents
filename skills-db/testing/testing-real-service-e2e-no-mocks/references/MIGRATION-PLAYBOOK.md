# Mock → Mock-Free Migration Playbook

> Step-by-step process for replacing mocked tests with real-DB integration tests.

## The Migration Loop

```
1. AUDIT     → Identify mocked test with highest Mock Risk Score
2. READ      → Understand WHAT it tests (not HOW it mocks)
3. CHECK     → Do mock return values match current schema/behavior?
4. WRITE     → New mock-free version using real DB + factories
5. VERIFY    → Run both side-by-side — same assertions pass?
6. DISCOVER  → Does mock-free version catch bugs mock didn't?
7. DELETE    → Remove the mocked version (don't keep both!)
```

## Step 1: Audit — Find the Riskiest Mocks

```bash
# Count mocked tests per file
grep -rl "vi.mock\|jest.mock" tests/ src/ | while read f; do
  count=$(grep -c "vi.mock\|jest.mock" "$f")
  echo "$count $f"
done | sort -rn | head -20
```

Score each mocked test:

| Test File | Mocks DB? | Mocks Payment? | Mocks Auth? | Last Bug | Score |
|-----------|:---------:|:--------------:|:-----------:|----------|-------|
| *file* | Y/N | Y/N | Y/N | date | Sum |

**Migrate highest-scoring files first.**

## Step 2: Read the Mocked Test

```typescript
// Example: mocked webhook handler test
vi.mock("@/lib/db/client", () => ({
    db: {
        query: { subscriptions: { findMany: vi.fn().mockResolvedValue([]) } },
        insert: vi.fn().mockReturnValue({ values: vi.fn() }),
    },
}));

// What does this ACTUALLY test?
// → It tests the webhook handler's LOGIC flow
// → But it does NOT test: DB constraints, cascade behavior, real queries
```

## Step 3: Check Mock Fidelity

Common mock-reality divergences:

| Mock Pattern | Real Behavior | Bug Hidden |
|-------------|---------------|------------|
| `mockResolvedValue([{status: "active"}])` | Real DB might return null | Null pointer in production |
| `mockResolvedValue({})` | Real Stripe returns complex object | Missing field access |
| `vi.mock("@/lib/db/client")` | Real DB has FK constraints | Cascade deletion bugs |
| `mockReturnValue({ success: true })` | Real email might fail | Silent email failures |

## Step 4: Write the Mock-Free Version

```typescript
// BEFORE: Mocked
vi.mock("@/lib/db/client");
it("creates subscription", () => {
    // Test uses fake DB that always succeeds
});

// AFTER: Mock-free
describe("creates subscription", () => {
    withTestTransaction();  // Real DB, transaction rollback

    it("creates subscription record", async () => {
        const db = getTestDb();
        const user = await createTestUser(db);

        const [sub] = await db.insert(subscriptions)
            .values({
                userId: user.id,
                provider: "stripe",
                externalId: "sub_test_123",
                status: "active",
                currentPeriodStart: new Date(),
                currentPeriodEnd: new Date(Date.now() + 30 * 86400000),
            })
            .returning();

        // Real DB enforces constraints
        expect(sub.userId).toBe(user.id);
        expect(sub.status).toBe("active");

        // Verify FK relationship actually works
        const subs = await db.query.subscriptions.findMany({
            where: eq(subscriptions.userId, user.id),
        });
        expect(subs).toHaveLength(1);
    });
});
```

## Step 5: Verify Parity

Run both tests to confirm the mock-free version catches the same assertions:

```bash
# Run original mocked test
bun test path/to/mocked-test.test.ts

# Run new mock-free test
REAL_API_TESTS=true bun test path/to/mock-free-test.test.ts

# Both should pass (if mock was accurate)
# If mock-free fails but mocked passes → mock was hiding a bug!
```

## Step 6: Discover Hidden Bugs

Things the mock-free version catches that mocks don't:

- Schema drift (column renamed, type changed)
- FK constraint violations (cascade deletes)
- Unique constraint violations (duplicate inserts)
- Transaction isolation issues (race conditions)
- Query performance (N+1 queries)
- Real error responses (connection timeout, rate limit)

## Step 7: Delete the Mock

```bash
# Remove the old mocked test file
rm src/lib/services/__tests__/old-mocked-test.test.ts

# Commit with clear message
git commit -m "test: replace mocked subscription test with real-DB integration test

The mock was hiding cascade deletion bugs (bd-odwdm.6).
New test uses transaction rollback isolation."
```

**CRITICAL: Do not keep both.** Maintaining a mocked version alongside a mock-free version doubles maintenance cost and creates confusion about which is authoritative.

## Common Migration Pitfalls

| Pitfall | Fix |
|---------|-----|
| Mock-free test is slower | Accept it — correctness > speed for critical paths |
| Can't mock external APIs | Use test mode (Stripe sk_test_*, PayPal sandbox) |
| Tests need specific DB state | Use factories, not hard-coded fixtures |
| Tests are order-dependent | Transaction rollback ensures isolation |
| Tests fail intermittently | Check for timestamp sensitivity, use fake timers |
