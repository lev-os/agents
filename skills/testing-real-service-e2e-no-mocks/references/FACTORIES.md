# Test Data Factory Patterns

> Factories create REALISTIC test data, not minimal stubs. Good factories make tests readable and catch edge cases that hard-coded data misses.

## TypeScript: fishery

```bash
npm install -D fishery @faker-js/faker
```

```typescript
import { Factory } from "fishery";
import { faker } from "@faker-js/faker";

// Seed for deterministic snapshot tests
faker.seed(42);

const userFactory = Factory.define<User>(({ sequence, params }) => ({
    id: params.id ?? `user-${sequence}`,
    email: params.email ?? faker.internet.email(),
    name: params.name ?? faker.person.fullName(),
    subscriptionStatus: params.subscriptionStatus ?? "none",
    isAdmin: params.isAdmin ?? false,
    customerId: `cus_test_${faker.string.alphanumeric(14)}`,
    createdAt: faker.date.past(),
    updatedAt: new Date(),
}));

// Usage
const user = userFactory.build();                    // Defaults
const admin = userFactory.build({ isAdmin: true });  // Override
const users = userFactory.buildList(5);              // Batch
```

### Factory Extensions

```typescript
const adminFactory = userFactory.params({ isAdmin: true });
const subscribedFactory = userFactory.params({
    subscriptionStatus: "active",
    subscriptionProvider: "stripe",
});

// Compositions
const subscribedAdmin = adminFactory.params({
    subscriptionStatus: "active",
});
```

### Async Factories (Persist to DB)

```typescript
const userFactory = Factory.define<User>(({ sequence }) => ({
    id: randomUUID(),
    email: `test-${sequence}@test.example.com`,
    name: `Test User ${sequence}`,
}));

// Register DB persistence
userFactory.onCreate(async (user) => {
    const [created] = await db.insert(users)
        .values(user)
        .returning();
    return created;
});

// Create and persist
const user = await userFactory.create();
const users = await userFactory.createList(3);
```

## Rust: fake-rs

```rust
use fake::{Dummy, Fake, Faker};
use fake::faker::name::en::*;
use fake::faker::internet::en::*;

#[derive(Debug, Dummy)]
struct TestUser {
    #[dummy(faker = "1000..9999")]
    id: u32,
    #[dummy(faker = "Name()")]
    name: String,
    #[dummy(faker = "FreeEmail()")]
    email: String,
    active: bool,
}

// Deterministic generation
use fake::rand::SeedableRng;
let mut rng = fake::rand::rngs::StdRng::seed_from_u64(42);
let user: TestUser = Faker.fake_with_rng(&mut rng);
```

## Manual Factory Pattern (No Dependencies)

```typescript
// For projects that don't want fishery
export function createTestUser(overrides: Partial<User> = {}): User {
    return {
        id: randomUUID(),
        email: `test-${randomUUID().slice(0, 8)}@test.jeffreys-skills.md`,
        name: "Test User",
        subscriptionStatus: "none" as const,
        isAdmin: false,
        customerId: `cus_test_${randomUUID().slice(0, 8)}`,
        createdAt: new Date(),
        updatedAt: new Date(),
        ...overrides,
    };
}

export function createTestSubscription(
    userId: string,
    overrides: Partial<Subscription> = {}
): Subscription {
    return {
        id: randomUUID(),
        userId,
        provider: "stripe" as const,
        externalId: `sub_test_${randomUUID().slice(0, 8)}`,
        status: "active" as const,
        currentPeriodStart: new Date(),
        currentPeriodEnd: new Date(Date.now() + 30 * 86400000),
        ...overrides,
    };
}
```

## Anti-Patterns

| ✗ Bad | ✓ Good |
|-------|--------|
| Hard-coded IDs (`"user-1"`) | Random UUIDs (parallel-safe) |
| Minimal data (`{ name: "x" }`) | Realistic data (faker) |
| Shared factory state | Each call returns fresh data |
| Factories that mutate globals | Pure functions with overrides |
| Factories that skip validation | Produce data that passes schema validation |
