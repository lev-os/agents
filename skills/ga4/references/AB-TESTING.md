# A/B Testing Without Google Optimize

## Table of Contents
- [Why DIY](#why-diy)
- [Architecture Overview](#architecture-overview)
- [Implementation](#implementation)
- [Tracking Experiments](#tracking-experiments)
- [Supabase Logging (Backup)](#supabase-logging-backup)
- [Analyzing Results](#analyzing-results)
- [Statistical Significance](#statistical-significance)
- [Best Practices](#best-practices)
- [Alternatives](#alternatives)

---

## Why DIY

### Google Optimize is Dead

**Sunset date**: September 30, 2023 (including Optimize 360).

Google's statement: They do not plan to build A/B testing into GA4's interface.

### Your Options

| Option | Cost | Complexity | Best For |
|--------|------|------------|----------|
| DIY with cookies + GA4 | Free | Low | Most SaaS startups |
| GrowthBook (open source) | Free (self-hosted) | Medium | Feature flags + experiments |
| Optimizely | $2k+/mo | Low | Enterprise, visual editor |
| VWO | $300+/mo | Low | Visual editor, SMB |
| LaunchDarkly | $10/seat/mo | Medium | Feature flags + experiments |

**This guide focuses on the free DIY approach.**

---

## Architecture Overview

> **Next.js 16:** Use `src/proxy.ts` and export `proxy()` instead of `middleware.ts`.
> **Next.js <=15:** Use `middleware.ts` and export `middleware()`.

```
┌─────────────────────────────────────────────────────────────┐
│                      A/B Testing Flow                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   1. ASSIGN VARIANT (Server-side, no flicker)                │
│   ════════════════════════════════════════                   │
│   proxy.ts → Check cookie → Random assign → Set cookie       │
│                                                              │
│   2. RENDER VARIANT                                          │
│   ═════════════════                                          │
│   Page/Component → Read cookie → Show variant A or B         │
│                                                              │
│   3. TRACK EXPOSURE                                          │
│   ═════════════════                                          │
│   Client → dataLayer.push({ event: 'experiment_view', ... }) │
│                                                              │
│   4. TRACK CONVERSION                                        │
│   ══════════════════                                         │
│   Client → dataLayer.push({ event: 'sign_up', variant: X })  │
│                                                              │
│   5. ANALYZE (Optional: Supabase backup)                     │
│   ═════════════════════════════════════                      │
│   GA4 Segments: A vs B conversion rates                      │
│   Supabase: Raw data for statistical analysis                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key insight**: Proxy/middleware assignment prevents "flicker" (user seeing variant A, then switching to B).

---

## Implementation

### Step 1: Variant Assignment (Proxy/Middleware)

Assign variants **server-side** before page renders.

```tsx
// src/proxy.ts
import { NextResponse, type NextRequest } from 'next/server'

// Experiment configuration
const EXPERIMENTS = {
  hero_cta: { variants: ['A', 'B'], weight: 0.5 },  // 50/50 split
  pricing_order: { variants: ['A', 'B'], weight: 0.5 },
} as const;

export async function proxy(request: NextRequest) {
  const response = NextResponse.next()

  // Assign each experiment
  for (const [name, config] of Object.entries(EXPERIMENTS)) {
    const cookieName = `exp_${name}`
    const existing = request.cookies.get(cookieName)?.value

    if (!existing) {
      const variant = Math.random() < config.weight ? 'A' : 'B'
      response.cookies.set(cookieName, variant, {
        maxAge: 60 * 60 * 24 * 30,  // 30 days
        httpOnly: false,             // Need client-side access
        sameSite: 'lax',
        path: '/'
      })
    }
  }

  return response
}

export const config = {
  matcher: '/((?!api|_next/static|_next/image|favicon.ico).*)',
}
```

### Step 2: Read Variant (Server Component)

```tsx
// app/page.tsx
import { cookies } from 'next/headers'

export default function LandingPage() {
  const cookieStore = cookies()
  const heroVariant = cookieStore.get('exp_hero_cta')?.value || 'A'
  const pricingVariant = cookieStore.get('exp_pricing_order')?.value || 'A'

  return (
    <main>
      <HeroSection variant={heroVariant} />
      <PricingSection variant={pricingVariant} />
    </main>
  )
}
```

### Step 3: Render Variants

```tsx
// components/HeroSection.tsx
interface HeroSectionProps {
  variant: 'A' | 'B';
}

export function HeroSection({ variant }: HeroSectionProps) {
  const content = {
    A: {
      headline: "Start Your Free Trial",
      cta: "Try Free for 14 Days",
      ctaColor: "bg-blue-600"
    },
    B: {
      headline: "Get Started in Minutes",
      cta: "Start Now - No Credit Card",
      ctaColor: "bg-green-600"
    }
  };

  const v = content[variant];

  return (
    <section>
      <h1>{v.headline}</h1>
      <CTAButton
        text={v.cta}
        className={v.ctaColor}
        experimentVariant={variant}
      />
    </section>
  );
}
```

### Step 4: Client-Side Variant Reading

For client components that need the variant:

```tsx
'use client'
import { useEffect, useState } from 'react'

function getExperimentVariant(experimentName: string): string {
  if (typeof document === 'undefined') return 'A'

  const cookie = document.cookie
    .split('; ')
    .find(row => row.startsWith(`exp_${experimentName}=`))

  return cookie?.split('=')[1] || 'A'
}

export function useExperiment(experimentName: string) {
  const [variant, setVariant] = useState('A')

  useEffect(() => {
    setVariant(getExperimentVariant(experimentName))
  }, [experimentName])

  return variant
}
```

---

## Tracking Experiments

### Track Experiment Exposure

Fire when user **sees** the experiment (not on page load, but when variant renders).

```tsx
// components/HeroSection.tsx
'use client'
import { useEffect } from 'react'

export function HeroSection({ variant }: { variant: 'A' | 'B' }) {
  useEffect(() => {
    window.dataLayer?.push({
      event: 'experiment_view',
      experiment_name: 'hero_cta',
      experiment_variant: variant
    });
  }, [variant]);

  // ... render
}
```

### Track Conversions with Variant

Include variant in **all relevant conversion events**:

```tsx
function handleSignUp() {
  const variant = getExperimentVariant('hero_cta')

  window.dataLayer?.push({
    event: 'sign_up',
    method: 'google',
    experiment_name: 'hero_cta',
    experiment_variant: variant
  });
}

function handleCTAClick(ctaText: string, position: string) {
  const variant = getExperimentVariant('hero_cta')

  window.dataLayer?.push({
    event: 'cta_click',
    cta_text: ctaText,
    cta_position: position,
    experiment_variant: variant
  });
}
```

### GTM Configuration

1. **Data Layer Variable**: `experiment_variant`
2. **Data Layer Variable**: `experiment_name`
3. **Include in GA4 Event tags**:

| Parameter | Value |
|-----------|-------|
| experiment_name | `{{DL - experiment_name}}` |
| experiment_variant | `{{DL - experiment_variant}}` |

---

## Supabase Logging (Backup)

Log experiment data to Supabase for:
- Raw data backup
- Statistical significance calculations
- Custom analysis beyond GA4

### Create Table

```sql
CREATE TABLE experiment_events (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  user_id UUID REFERENCES auth.users(id),
  anonymous_id TEXT,
  experiment_name TEXT NOT NULL,
  experiment_variant TEXT NOT NULL,
  event_type TEXT NOT NULL,  -- 'view' | 'convert'
  metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_experiment_events_experiment ON experiment_events(experiment_name, experiment_variant);
CREATE INDEX idx_experiment_events_created ON experiment_events(created_at);
```

### Client Logging

```tsx
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

async function logExperimentEvent(
  experimentName: string,
  variant: string,
  eventType: 'view' | 'convert',
  metadata?: Record<string, any>
) {
  const { data: { user } } = await supabase.auth.getUser()

  await supabase.from('experiment_events').insert({
    user_id: user?.id || null,
    anonymous_id: getOrCreateAnonymousId(),  // localStorage-based
    experiment_name: experimentName,
    experiment_variant: variant,
    event_type: eventType,
    metadata: metadata || {}
  })
}

// Usage
logExperimentEvent('hero_cta', 'B', 'view')
logExperimentEvent('hero_cta', 'B', 'convert', { plan: 'pro' })
```

### Query for Analysis

```sql
-- Conversion rate by variant
SELECT
  experiment_variant,
  COUNT(*) FILTER (WHERE event_type = 'view') as views,
  COUNT(*) FILTER (WHERE event_type = 'convert') as conversions,
  ROUND(
    100.0 * COUNT(*) FILTER (WHERE event_type = 'convert') /
    NULLIF(COUNT(*) FILTER (WHERE event_type = 'view'), 0),
    2
  ) as conversion_rate
FROM experiment_events
WHERE experiment_name = 'hero_cta'
  AND created_at > NOW() - INTERVAL '7 days'
GROUP BY experiment_variant;
```

---

## Analyzing Results

### GA4 Exploration Method

1. GA4 > **Explore** > Free-form exploration
2. **Dimensions**: Add `experiment_variant`
3. **Metrics**: Add `Event count`, `Conversions`
4. **Filter**: `experiment_name = hero_cta`

### Create Comparison Segments

**Segment A**:
- Name: "Experiment A"
- Condition: `experiment_variant` exactly matches `A`

**Segment B**:
- Name: "Experiment B"
- Condition: `experiment_variant` exactly matches `B`

### Calculate Conversion Rate

| Segment | experiment_view | sign_up | Conv. Rate |
|---------|-----------------|---------|------------|
| A | 1,000 | 50 | 5.0% |
| B | 980 | 72 | 7.3% |

**Lift**: (7.3 - 5.0) / 5.0 = **46% improvement**

---

## Statistical Significance

GA4 doesn't calculate significance. Use external tools.

### Online Calculators

- [ABTestGuide Calculator](https://abtestguide.com/calc/)
- [Evan Miller's Calculator](https://www.evanmiller.org/ab-testing/chi-squared.html)

### Inputs Needed

| Input | Value |
|-------|-------|
| Control (A) visitors | 1,000 |
| Control conversions | 50 |
| Variant (B) visitors | 980 |
| Variant conversions | 72 |

### Minimum Sample Size

Rule of thumb for detecting a **10% relative lift** at 95% confidence:

| Baseline Conv. Rate | Sample Size per Variant |
|--------------------|------------------------|
| 2% | ~15,000 |
| 5% | ~6,000 |
| 10% | ~3,000 |
| 20% | ~1,500 |

**Use**: [Sample Size Calculator](https://www.evanmiller.org/ab-testing/sample-size.html)

### BigQuery Method (Advanced)

If using GA4 BigQuery export:

```sql
-- Chi-squared components
WITH experiment_data AS (
  SELECT
    (SELECT value.string_value FROM UNNEST(event_params)
     WHERE key = 'experiment_variant') as variant,
    event_name
  FROM `project.dataset.events_*`
  WHERE event_name IN ('experiment_view', 'sign_up')
    AND (SELECT value.string_value FROM UNNEST(event_params)
         WHERE key = 'experiment_name') = 'hero_cta'
)
SELECT
  variant,
  COUNTIF(event_name = 'experiment_view') as views,
  COUNTIF(event_name = 'sign_up') as conversions,
  COUNTIF(event_name = 'sign_up') / COUNTIF(event_name = 'experiment_view') as rate
FROM experiment_data
GROUP BY variant
```

Export to Python/R for chi-squared test.

---

## Best Practices

### Do

| Practice | Why |
|----------|-----|
| **One change per test** | Isolate variable impact |
| **Test for 2+ weeks** | Capture weekly patterns |
| **Document hypothesis** | "Changing X will increase Y by Z%" |
| **Decide sample size upfront** | Avoid peeking bias |
| **Test on meaningful pages** | High-traffic pages = faster results |
| **Use consistent experience** | Cookie persists 30 days |

### Don't

| Anti-pattern | Problem |
|--------------|---------|
| **Overlapping tests on same element** | Interactions confound results |
| **Ending early** | "B is winning after 2 days!" = noise |
| **Testing tiny differences** | <10% lift rarely worth it |
| **Multiple conflicting CTAs** | User confusion |
| **Changing test mid-run** | Invalidates data |
| **Ignoring segments** | Winner overall may lose for key segment |

### Overlapping Test Rules

**Safe overlap**:
- Test hero CTA + Test footer layout (different page areas)
- Test checkout flow + Test onboarding (different funnels)

**Dangerous overlap**:
- Test hero headline + Test hero CTA (same section)
- Test pricing copy + Test pricing layout (same decision point)

### Naming Convention

```
exp_{page}_{element}
```

Examples:
- `exp_landing_hero_cta`
- `exp_landing_pricing_order`
- `exp_signup_form_length`
- `exp_dashboard_onboarding`

---

## Alternatives

### Open Source (Self-Hosted)

**GrowthBook** - Feature flags + experiments
```bash
docker run -p 3100:3100 growthbook/growthbook
```

Features:
- Visual editor
- Statistical analysis built-in
- Feature flags
- Free self-hosted, paid cloud

**Unleash** - Feature flags (less A/B focused)

### Paid Platforms

| Platform | Pricing | Strengths | Weaknesses |
|----------|---------|-----------|------------|
| Optimizely | $2k+/mo | Enterprise features, visual editor | Expensive |
| VWO | $300+/mo | Visual editor, heatmaps | Limited analysis |
| AB Tasty | Custom | Personalization | Complex pricing |
| LaunchDarkly | $10/seat/mo | Feature flags + experiments | Developer-focused |

### When to Upgrade from DIY

Upgrade when you need:
- **Visual editor** (non-technical team runs tests)
- **5+ concurrent experiments**
- **Personalization** (show X to segment Y)
- **Built-in stats** (automated significance)
- **Audit trails** (compliance requirements)
- **100k+ monthly users** (scale concerns)

---

## Quick Reference

### Complete Flow

```tsx
// 1. proxy.ts (Next.js 16) / middleware.ts (<=15) - Assign
if (!request.cookies.get('exp_test')) {
  response.cookies.set('exp_test', Math.random() < 0.5 ? 'A' : 'B')
}

// 2. Server Component - Read
const variant = cookies().get('exp_test')?.value || 'A'

// 3. Client - Track exposure
useEffect(() => {
  dataLayer.push({ event: 'experiment_view', experiment_variant: variant })
}, [])

// 4. Client - Track conversion
dataLayer.push({ event: 'sign_up', experiment_variant: variant })

// 5. Supabase - Backup (optional)
await supabase.from('experiment_events').insert({ ... })

// 6. GA4 - Analyze
// Explore > Segments > Compare A vs B conversion rates
```

### Checklist

- [ ] Variant assigned in middleware (no flicker)
- [ ] Cookie persists 30 days
- [ ] `experiment_view` fires on variant render
- [ ] `experiment_variant` included in conversion events
- [ ] Custom dimension registered in GA4
- [ ] Minimum sample size calculated
- [ ] Test runs for 2+ full weeks
- [ ] Results exported before making decisions
