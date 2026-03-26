# Funnel Analysis in GA4

## Table of Contents
- [Building Custom Funnels](#building-custom-funnels)
- [Buyers vs Non-Buyers](#buyers-vs-non-buyers-analysis)
- [Post-Conversion Analysis](#post-conversion-analysis)
- [Retention & Cohorts](#retention--cohorts)
- [Exporting Data](#exporting-data)

---

## Building Custom Funnels

GA4's **Funnel Exploration** lets you define any events as funnel steps.

### Create a Funnel

1. GA4 > **Explore** > Create new exploration
2. Choose **Funnel exploration** template
3. Configure steps:

### Example: Landing to Sign-up Funnel

| Step | Event | Condition (optional) |
|------|-------|---------------------|
| 1 | `page_view` | `page_location` contains `/landing` |
| 2 | `scroll_depth` | `scroll_percent` >= 50 |
| 3 | `section_view` | `section_name` = `pricing` |
| 4 | `cta_click` | `cta_position` = `hero` or `pricing` |
| 5 | `sign_up` | (none) |

### Funnel Settings

| Setting | Options | When to Use |
|---------|---------|-------------|
| **Open funnel** | Users can enter at any step | Exploratory analysis |
| **Closed funnel** | Users must complete all steps in order | Strict conversion path |
| **Elapsed time** | Show time between steps | Identify friction points |
| **Next action** | Show what users do after dropping | Find alternative paths |

### Reading Funnel Reports

```
Step 1: page_view         1,000 users (100%)
    ↓ 70% continue, 30% drop
Step 2: scroll_depth        700 users (70%)
    ↓ 60% continue, 40% drop
Step 3: section_view        420 users (42%)
    ↓ 50% continue, 50% drop
Step 4: cta_click           210 users (21%)
    ↓ 40% continue, 60% drop
Step 5: sign_up              84 users (8.4%)
```

**Key metrics**:
- **Completion rate**: 8.4% (84/1000 = overall conversion)
- **Biggest drop-off**: Step 3→4 (50%) — users see pricing but don't click CTA
- **Action**: Test pricing page CTA copy, placement, or offer

### Save to Library

After building a useful funnel, save it:
1. Click **Save** in exploration
2. GA4 > Library > Add to collection

This makes it accessible alongside standard reports.

---

## Buyers vs Non-Buyers Analysis

Since your SaaS has only paid users, "buyers" = users who completed `sign_up`.

### Create Segments

1. In any Exploration, click **Segments** > Create segment
2. **Segment 1: Converters**
   - Condition: Event = `sign_up`
3. **Segment 2: Non-converters**
   - Condition: NOT (Event = `sign_up`)

### Compare Behavior

Apply both segments to see differences:

| Metric | Converters | Non-Converters | Insight |
|--------|------------|----------------|---------|
| Avg scroll_depth | 75% | 35% | Converters read more content |
| section_view: pricing | 90% | 40% | Pricing page is critical |
| Pages/session | 4.2 | 1.8 | Converters explore more |
| Avg session duration | 5:30 | 1:20 | Engagement predicts conversion |

### Build Audience for Remarketing

1. GA4 Admin > Audiences > New audience
2. Name: "Engaged Non-Converters"
3. Conditions:
   - `scroll_depth` >= 50 AND
   - NOT `sign_up`
4. Membership duration: 30 days

Export to Google Ads for retargeting campaigns.

---

## Post-Conversion Analysis

Track what new users do after sign-up.

### First Session Behavior

Create exploration with:
- Dimension: `feature_name` (from `feature_use` events)
- Metric: Event count
- Segment: Users who did `sign_up` in last 7 days

### Activation Metrics

Define "activation" as completing key actions:

```
// Example activation events
sign_up → first_project_created → first_export → invited_teammate
```

Track each as separate events or with `feature_use`:

```tsx
trackEvent('feature_use', { feature_name: 'first_project_created' });
trackEvent('feature_use', { feature_name: 'first_export' });
```

### Time to First Action

In Funnel exploration with elapsed time:

| Step | Event | Median Time |
|------|-------|-------------|
| 1 | `sign_up` | — |
| 2 | `feature_use` (any) | 2 min |
| 3 | `feature_use` = `first_export` | 15 min |

Fast time-to-value indicates good onboarding.

---

## Retention & Cohorts

### Retention Report

GA4 > Reports > Retention

Shows:
- **User retention**: % returning in week 1, 2, 3...
- **Engagement retention**: % active users returning
- **Lifetime value**: Revenue/engagement over time

### Cohort Analysis

1. GA4 > Explore > Cohort exploration
2. Cohort: Users who did `sign_up`
3. Return criteria: Any event (or specific feature_use)
4. Granularity: Weekly

### Improving Retention Data with User-ID

Default GA4 uses cookies — loses users across devices/browsers.

**User-ID tracking** ties sessions together:

```tsx
// After auth, push user_id to dataLayer
window.dataLayer?.push({ user_id: session.user.id });
```

In GTM:
1. Create Data Layer Variable: `user_id`
2. In GA4 Config tag > Fields to Set:
   - Field: `user_id`
   - Value: `{{DL - user_id}}`

GA4 Admin:
1. Data Streams > Web stream > Configure
2. Enable "User-ID" reporting

This enables:
- Cross-device tracking
- Accurate user counts
- Better retention metrics

---

## Exporting Data

### BigQuery Export

For advanced analysis beyond GA4 UI:

1. GA4 Admin > BigQuery Links > Link
2. Choose project, dataset, frequency (daily/streaming)
3. Query raw events in BigQuery

```sql
-- Example: Conversion rate by landing page
SELECT
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'page_location') as landing_page,
  COUNTIF(event_name = 'sign_up') / COUNT(DISTINCT user_pseudo_id) as conversion_rate
FROM `project.dataset.events_*`
WHERE event_name IN ('page_view', 'sign_up')
GROUP BY landing_page
ORDER BY conversion_rate DESC
```

### Looker Studio

Connect GA4 directly to Looker Studio for dashboards:

1. Looker Studio > Create > Data source > Google Analytics
2. Select GA4 property
3. Build charts with GA4 dimensions/metrics

### CSV Export

From any Exploration:
1. Click **Export** (top right)
2. Choose CSV, Google Sheets, or PDF

---

## Quick Reference

### Funnel Exploration Checklist

- [ ] Define 4-6 key steps (not too granular)
- [ ] Decide open vs closed funnel
- [ ] Enable elapsed time to find friction
- [ ] Compare segments (device, traffic source)
- [ ] Save to Library for reuse

### Segment Ideas

| Segment | Condition | Use Case |
|---------|-----------|----------|
| Converters | Event `sign_up` | Analyze convert behavior |
| High-intent | scroll_depth >= 75 | Retargeting |
| Pricing viewers | section_view = pricing | Test pricing page |
| Mobile users | Device category = mobile | Mobile optimization |
| Organic | Source = google, medium = organic | SEO analysis |

### Key Questions This Answers

1. Where do users drop off in the funnel?
2. What do converters do differently than non-converters?
3. Which features do new users adopt first?
4. Are users returning after sign-up?
5. What's the time-to-first-action?
