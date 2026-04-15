# Authentication: Google OAuth Bypass

## Table of Contents
- [The Problem](#the-problem)
- [The Solution](#the-solution)
- [Test User Architecture](#test-user-architecture)
- [Provisioning Scripts](#provisioning-scripts)
- [Global Auth Setup](#global-auth-setup)
- [Storage State Reuse](#storage-state-reuse)
- [Seed Data Management](#seed-data-management)
- [Troubleshooting](#troubleshooting)

---

## The Problem

Google OAuth cannot be automated:
- Google actively blocks automated browser logins
- CAPTCHA challenges appear after a few attempts
- OAuth flows involve redirects to Google's domain
- Session cookies are tied to Google's security checks
- Headless browsers are detected and blocked

```
❌ Attempting automated Google login:
   1. Navigate to /login
   2. Click "Sign in with Google"
   3. Redirected to accounts.google.com
   4. BLOCKED: CAPTCHA challenge
   5. Test fails
```

---

## The Solution

Create **special test users** in Supabase with **email/password authentication** that bypass Google OAuth entirely. These users:

1. Are created directly via Supabase Admin API
2. Have pre-confirmed emails (no verification needed)
3. Are marked with metadata (`is_test_user: true`)
4. Have deterministic, known passwords in environment variables
5. Have pre-seeded data for consistent assertions

```typescript
// The key insight: Supabase supports BOTH OAuth AND email/password
// Test users use email/password, production users use Google OAuth
// Same app, same database, different auth method

const { data, error } = await supabase.auth.signInWithPassword({
  email: process.env.E2E_TEST_EMAIL,    // e2e-test@app.test
  password: process.env.E2E_TEST_PASSWORD,
});

// This returns a valid session—no Google involved!
```

---

## Test User Architecture

### Five Test User Types

| Type | Email | Tier | Purpose |
|------|-------|------|---------|
| `primary` | `e2e-test@app.test` | Pro | Main test user with full data |
| `free` | `e2e-free@app.test` | Free | Paywall, limitations, upgrade flows |
| `premium` | `e2e-premium@app.test` | Premium | All features, advanced tests |
| `fresh` | `e2e-fresh@app.test` | None | Onboarding wizard, empty states |
| `admin` | `e2e-admin@app.test` | Admin | Admin panel, ops dashboards |

### Why `.test` TLD?

Per IANA reservation, `.test` is a reserved TLD that will never resolve:
- Test emails never accidentally go to real inboxes
- No risk of spamming real users
- Clear distinction between test and production data

### User Definition

```typescript
// tests/e2e/fixtures/test-users.ts
export const TEST_USERS = {
  primary: {
    type: 'primary',
    email: 'e2e-test@app.test',
    emailEnvVar: 'E2E_TEST_EMAIL',
    passwordEnvVar: 'E2E_TEST_PASSWORD',
    tier: 'pro',
    hasOnboarding: true,
    hasBrokerage: true,
    hasPortfolio: true,
    description: 'Main authenticated user for dashboard and feature tests',
    metadata: {
      is_test_user: true,
      test_user_type: 'primary',
      test_tier: 'pro',
      created_for: 'e2e-testing',
      do_not_delete: true,
    },
  },

  free: {
    type: 'free',
    email: 'e2e-free@app.test',
    emailEnvVar: 'E2E_FREE_EMAIL',
    passwordEnvVar: 'E2E_FREE_PASSWORD',
    tier: 'free',
    hasOnboarding: true,
    hasBrokerage: false,
    hasPortfolio: false,
    description: 'Free tier user for paywall and limitation tests',
    metadata: {
      is_test_user: true,
      test_user_type: 'free',
      test_tier: 'free',
      created_for: 'e2e-testing',
    },
  },

  // ... premium, fresh, admin
};
```

---

## Provisioning Scripts

### Create Test Users

```typescript
// scripts/provision-e2e-test-users.ts
import { createClient } from '@supabase/supabase-js';
import { TEST_USERS } from '../tests/e2e/fixtures/test-users';
import crypto from 'crypto';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!  // Admin key required
);

async function provisionUser(userConfig: typeof TEST_USERS.primary) {
  const password = crypto.randomBytes(32).toString('base64');

  // Create user with email/password (bypasses OAuth)
  const { data: authData, error: authError } = await supabase.auth.admin.createUser({
    email: userConfig.email,
    password,
    email_confirm: true,  // Auto-confirm, no verification email
    user_metadata: userConfig.metadata,
  });

  if (authError) throw authError;

  // Create profile and seed data
  await seedUserData(authData.user.id, userConfig);

  console.log(`Created ${userConfig.type} user:`);
  console.log(`  Email: ${userConfig.email}`);
  console.log(`  Password: ${password}`);
  console.log(`  Add to .env.local:`);
  console.log(`    ${userConfig.emailEnvVar}=${userConfig.email}`);
  console.log(`    ${userConfig.passwordEnvVar}=${password}`);
}

async function main() {
  const userType = process.argv[2] || 'all';

  if (userType === 'all') {
    for (const user of Object.values(TEST_USERS)) {
      await provisionUser(user);
    }
  } else {
    await provisionUser(TEST_USERS[userType]);
  }
}

main().catch(console.error);
```

### Usage

```bash
# Provision all test users
bun scripts/provision-e2e-test-users.ts

# Provision specific user
bun scripts/provision-e2e-test-users.ts --user=primary

# Dry run (show what would happen)
bun scripts/provision-e2e-test-users.ts --dry-run

# Force recreate (delete and recreate)
bun scripts/provision-e2e-test-users.ts --force
```

---

## Global Auth Setup

Authentication happens **once** at the start of a test run:

```typescript
// e2e/auth.global-setup.ts
import { chromium, type FullConfig } from '@playwright/test';
import { createClient } from '@supabase/supabase-js';

async function globalSetup(config: FullConfig) {
  const email = process.env.E2E_TEST_EMAIL;
  const password = process.env.E2E_TEST_PASSWORD;

  if (!email || !password) {
    throw new Error('E2E_TEST_EMAIL and E2E_TEST_PASSWORD must be set');
  }

  // Create Supabase client
  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );

  // Sign in with email/password (NOT OAuth)
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) throw new Error(`Auth failed: ${error.message}`);

  // Create browser and inject session
  const browser = await chromium.launch();
  const context = await browser.newContext();

  // Set Supabase session cookies
  await context.addCookies([
    {
      name: 'sb-access-token',
      value: data.session.access_token,
      domain: new URL(process.env.NEXT_PUBLIC_SUPABASE_URL!).hostname,
      path: '/',
      httpOnly: true,
      secure: true,
      sameSite: 'Lax',
    },
    {
      name: 'sb-refresh-token',
      value: data.session.refresh_token,
      domain: new URL(process.env.NEXT_PUBLIC_SUPABASE_URL!).hostname,
      path: '/',
      httpOnly: true,
      secure: true,
      sameSite: 'Lax',
    },
  ]);

  // Navigate to trigger session hydration
  const page = await context.newPage();
  await page.goto(config.projects[0].use.baseURL + '/');
  await page.waitForLoadState('networkidle');

  // Save storage state for reuse
  await context.storageState({ path: '.auth/user.json' });

  await browser.close();
  console.log('✓ Authentication setup complete');
}

export default globalSetup;
```

---

## Storage State Reuse

After global setup, all tests reuse the authenticated state:

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    // Setup project runs FIRST
    {
      name: 'setup',
      testMatch: /auth\.global-setup\.ts/,
    },

    // Feature tests depend on setup and load saved state
    {
      name: 'authenticated',
      dependencies: ['setup'],
      use: {
        storageState: '.auth/user.json',  // Load pre-authenticated state
        ...devices['Desktop Chrome'],
      },
    },
  ],
});
```

The `.auth/user.json` file contains:
```json
{
  "cookies": [
    {
      "name": "sb-access-token",
      "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "domain": "your-app.supabase.co",
      "path": "/",
      "httpOnly": true,
      "secure": true,
      "sameSite": "Lax"
    },
    {
      "name": "sb-refresh-token",
      "value": "abc123...",
      ...
    }
  ],
  "origins": []
}
```

---

## Seed Data Management

### Reset Script

```typescript
// scripts/reset-e2e-test-user.ts
import { TEST_USERS } from '../tests/e2e/fixtures/test-users';
import { SEED_DATA } from '../tests/e2e/fixtures/seed-data';
import { db } from '../src/lib/db';

type ResetMode = 'data-only' | 'full';

async function resetUser(userType: string, mode: ResetMode) {
  const user = TEST_USERS[userType];
  const seedData = SEED_DATA[userType];

  // Get user ID from Supabase
  const { data: userData } = await supabase.auth.admin.listUsers();
  const userId = userData.users.find(u => u.email === user.email)?.id;

  if (!userId) throw new Error(`User ${user.email} not found`);

  // Clear existing data (order matters for FK constraints)
  await db.transaction(async (tx) => {
    await tx.delete(alertTriggers).where(eq(alertTriggers.userId, userId));
    await tx.delete(alerts).where(eq(alerts.userId, userId));
    await tx.delete(positions).where(eq(positions.userId, userId));
    // ... more tables

    // Re-seed data
    if (mode === 'data-only' || seedData) {
      for (const position of seedData.positions) {
        await tx.insert(positions).values({ ...position, userId });
      }
      for (const alert of seedData.alerts) {
        await tx.insert(alerts).values({ ...alert, userId });
      }
      // ... more seed data
    }
  });

  console.log(`✓ Reset ${userType} user (mode: ${mode})`);
}
```

### Seed Data Definition

```typescript
// tests/e2e/fixtures/seed-data.ts
export const SEED_DATA = {
  primary: {
    tier: 'pro',
    profile: {
      planTier: 'pro',
      onboardingStatus: 'completed',
      riskTolerance: 'moderate',
      investmentObjectives: ['growth', 'income'],
    },
    positions: [
      {
        ticker: 'AAPL',
        name: 'Apple Inc.',
        quantity: 100,
        costBasis: 15000,
        currentValue: 17500,
      },
      {
        ticker: 'NVDA',
        name: 'NVIDIA Corporation',
        quantity: 50,
        costBasis: 20000,
        currentValue: 25000,
      },
      // ... more positions for predictable assertions
    ],
    alerts: [
      {
        name: 'AAPL Price Drop',
        type: 'price',
        ticker: 'AAPL',
        threshold: 150,
      },
    ],
  },

  free: {
    tier: 'free',
    profile: {
      planTier: 'free',
      onboardingStatus: 'completed',
    },
    positions: [],  // Free user has no positions
    alerts: [],
  },

  fresh: {
    tier: null,
    profile: {
      onboardingStatus: 'not_started',
    },
    positions: [],
    alerts: [],
  },
};
```

---

## Troubleshooting

### "Invalid credentials" Error

**Problem:** Email/password login fails even though user exists.

**Cause:** User was created with OAuth, not email/password.

**Fix:** Delete and recreate with email/password:
```bash
# Delete via Supabase dashboard or admin API
bun scripts/provision-e2e-test-users.ts --force --user=primary
```

### "Email sign-in is disabled" Error

**Problem:** Supabase instance has email auth disabled.

**Fix:** Enable in Supabase Dashboard:
1. Go to Authentication → Providers
2. Enable "Email" provider
3. Optionally keep "Confirm email" disabled for test users

### Session Expires During Tests

**Problem:** Tests fail after running for a while.

**Cause:** Access token expired (default: 1 hour).

**Fix:** Use longer token expiry or refresh mid-test:
```typescript
// Increase token expiry in Supabase settings
// OR add token refresh in long test suites
if (page.context().storageState().cookies[0].expires < Date.now()) {
  await refreshSession();
}
```

### CI Environment Variables

Set in GitHub Actions:
```yaml
env:
  E2E_TEST_EMAIL: ${{ secrets.E2E_TEST_EMAIL }}
  E2E_TEST_PASSWORD: ${{ secrets.E2E_TEST_PASSWORD }}
  NEXT_PUBLIC_SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
  NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}
```

---

## Security Considerations

1. **Never commit credentials** — Use `.env.local` (gitignored)
2. **Use `.test` TLD** — Emails can't leak to real addresses
3. **Mark test users** — `is_test_user: true` metadata for filtering
4. **Separate environments** — Production test users should have limited data
5. **Rotate passwords** — Regenerate periodically, especially after leaks
