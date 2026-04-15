# Transaction Rollback Isolation Deep-Dive

> The foundation of mock-free testing. Every test runs in a transaction that's rolled back. Zero cleanup. Zero shared state. Zero flakiness.

## How It Works

```
1. beforeAll: Open database connection
2. beforeEach: BEGIN transaction → SAVEPOINT
3. Test runs: INSERT, UPDATE, DELETE — all visible within transaction
4. afterEach: ROLLBACK TO SAVEPOINT → ROLLBACK transaction
5. afterAll: Close connection
```

The test sees its own writes but never commits them. The database is pristine for the next test.

## TypeScript/Vitest Implementation

```typescript
import { drizzle, type PostgresJsDatabase } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import { beforeAll, beforeEach, afterEach, afterAll } from "vitest";
import * as schema from "@/lib/db/schema";

let testSqlClient: postgres.Sql | null = null;
let testDb: PostgresJsDatabase<typeof schema> | null = null;

export function withTestTransaction(opts?: { suiteName?: string }) {
  beforeAll(async () => {
    testSqlClient = postgres(TEST_DATABASE_URL, {
      prepare: false,
      max: 1,           // Single connection — transaction isolation requires it
      idle_timeout: 0,   // Keep alive for entire test suite
    });
    testDb = drizzle(testSqlClient, { schema });
  });

  beforeEach(async () => {
    await testSqlClient!`BEGIN`;
    await testSqlClient!`SAVEPOINT test_savepoint`;
  });

  afterEach(async () => {
    try {
      await testSqlClient!`ROLLBACK TO SAVEPOINT test_savepoint`;
      await testSqlClient!`ROLLBACK`;
    } catch {
      // Connection may already be closed on test crash
    }
  });

  afterAll(async () => {
    if (testSqlClient) {
      await testSqlClient.end();
      testSqlClient = null;
      testDb = null;
    }
  });
}

export function getTestDb(): PostgresJsDatabase<typeof schema> {
  if (!testDb) throw new Error("Call withTestTransaction() in your describe block first");
  return testDb;
}
```

## Rust: sqlx #[sqlx::test]

sqlx provides the gold standard implementation. Each test gets its own database:

```rust
// sqlx creates a unique DB per test using SHA-512 hash of test path
// Name format: _sqlx_test_{64-char-hash} (always fits in 63-char PG limit)

#[sqlx::test]
async fn test_insert(pool: Pool<Postgres>) -> sqlx::Result<()> {
    // pool points to a fresh database with migrations applied
    sqlx::query("INSERT INTO users (name) VALUES ($1)")
        .bind("Alice")
        .execute(&pool)
        .await?;

    let (count,): (i64,) = sqlx::query_as("SELECT count(*) FROM users")
        .fetch_one(&pool)
        .await?;
    assert_eq!(count, 1);
    Ok(())
    // Database is dropped after test
}

// With fixtures
#[sqlx::test(fixtures("seed_users", "seed_subscriptions"))]
async fn test_with_seed_data(pool: Pool<Postgres>) -> sqlx::Result<()> {
    // fixtures/seed_users.sql and fixtures/seed_subscriptions.sql
    // are loaded before the test runs
    let users: Vec<User> = sqlx::query_as("SELECT * FROM users")
        .fetch_all(&pool)
        .await?;
    assert!(!users.is_empty());
    Ok(())
}
```

## Isolated Database Pattern (CREATE DATABASE template)

For tests that need COMMIT behavior (can't use transaction rollback):

```typescript
async function createIsolatedDatabase(suiteName?: string) {
    const { baseUrl, databaseName } = parseDatabaseUrl(TEST_DATABASE_URL);
    const isolatedName = `${databaseName}_${sanitize(suiteName)}_${uuid()}`;

    const adminClient = postgres(adminUrl, { prepare: false, max: 1 });

    // Clone schema from template database
    await adminClient.unsafe(
        `CREATE DATABASE ${isolatedName} TEMPLATE ${databaseName}`
    );

    const isolatedClient = postgres(isolatedUrl, { prepare: false, max: 1 });
    const db = drizzle(isolatedClient, { schema });

    return { db, cleanup: async () => {
        await isolatedClient.end();
        await adminClient.unsafe(`DROP DATABASE IF EXISTS ${isolatedName}`);
        await adminClient.end();
    }};
}
```

## When Transaction Rollback Doesn't Work

| Situation | Why | Alternative |
|-----------|-----|-------------|
| Testing COMMIT behavior | Rollback prevents commit | Isolated database |
| DDL statements (CREATE TABLE) | Auto-commits in PG | Isolated database |
| Testing connection pool behavior | Need multiple connections | Isolated database |
| Testing replication | Requires committed data | Isolated database |
| Cross-service tests | External service can't join TX | Cleanup registry |

## Testcontainers (Docker-Based Isolation)

```typescript
import { PostgreSqlContainer } from "@testcontainers/postgresql";

let container;
let db;

beforeAll(async () => {
    container = await new PostgreSqlContainer("postgres:16-alpine")
        .withDatabase("testdb")
        .start();

    const client = new Client({ connectionString: container.getConnectionUri() });
    await client.connect();
    db = drizzle(client);
    await migrate(db, { migrationsFolder: "./drizzle" });
}, 120_000);

afterAll(async () => {
    await container?.stop();
});
```

```rust
use testcontainers::{runners::AsyncRunner, ImageExt};
use testcontainers_modules::postgres::Postgres;

#[tokio::test]
async fn test_with_container() {
    let container = Postgres::default()
        .with_db_name("testdb")
        .with_init_sql("schema.sql".into())
        .start().await.unwrap();

    let port = container.get_host_port_ipv4(5432).unwrap();
    let url = format!("postgres://postgres:postgres@localhost:{port}/testdb");
    // Use real connection...
}
```
