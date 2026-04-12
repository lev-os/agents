# GA4 Event Schemas

## Table of Contents
- [Event Model Overview](#event-model-overview)
- [Automatically Collected Events](#automatically-collected-events)
- [Enhanced Measurement Events](#enhanced-measurement-events)
- [Recommended Events](#recommended-events)
- [Custom Funnel Events](#custom-funnel-events)
- [Custom Parameters](#custom-parameters)
- [User Properties](#user-properties)
- [Event Naming Rules](#event-naming-rules)

---

## Event Model Overview

GA4 is **event-based** — everything is an event, not pageviews vs events like Universal Analytics.

```
Event Structure:
{
  event_name: "cta_click",           // Required
  event_params: {                     // Optional parameters
    cta_text: "Get Started",
    cta_position: "hero"
  },
  user_properties: {                  // Persistent user attributes
    customer_status: "paid"
  }
}
```

**Event hierarchy**:
1. **Automatically collected** — GA4 sends these without config
2. **Enhanced measurement** — Optional auto-tracking (toggle in GA4 Admin)
3. **Recommended events** — GA4's predefined schemas (use exact names)
4. **Custom events** — Your own events for specific needs

---

## Automatically Collected Events

These fire without any configuration:

| Event | Description |
|-------|-------------|
| `first_visit` | User's first visit to site |
| `session_start` | New session begins |
| `page_view` | Page loads (handled by GA4 Config tag) |
| `user_engagement` | User is active on page |
| `first_open` | First app open (mobile) |

**No action needed** — these work with basic GA4 Config tag.

---

## Enhanced Measurement Events

Toggle in GA4 Admin > Data Streams > Enhanced Measurement.

| Event | What It Tracks | Limitation |
|-------|---------------|------------|
| `scroll` | 90% scroll depth | Only 90%, not granular |
| `click` | Outbound link clicks | Not internal CTAs |
| `file_download` | PDF, doc, etc downloads | Based on file extension |
| `video_start/progress/complete` | YouTube embeds | Only YouTube |
| `form_start/submit` | Form interactions | May not catch all forms |
| `site_search` | Search queries | Requires query param config |

**Recommendation**: Enable all, but supplement with custom tracking for:
- Granular scroll (25/50/75/90%) via GTM
- Internal CTA clicks
- Non-YouTube videos
- Custom form tracking

---

## Recommended Events

Use GA4's exact event names to unlock default reports and ML features.

### sign_up (Critical for SaaS)

```json
{
  "event": "sign_up",
  "method": "google"
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `method` | string | "google", "email", "github", etc. |

**When to fire**: After Supabase confirms `SIGNED_IN` for new user.

### login

```json
{
  "event": "login",
  "method": "google"
}
```

Fire on returning user login (not first sign-up).

### purchase (If charging at sign-up)

```json
{
  "event": "purchase",
  "transaction_id": "txn_abc123",
  "value": 29.00,
  "currency": "USD",
  "items": [{
    "item_id": "pro_plan",
    "item_name": "Pro Plan",
    "price": 29.00
  }]
}
```

Use if users pay during sign-up flow.

### Other Recommended Events

| Event | Use Case |
|-------|----------|
| `search` | User searches your app |
| `share` | User shares content |
| `select_content` | User selects item/content |
| `view_item` | User views product/plan details |
| `begin_checkout` | User starts checkout |
| `add_to_cart` | User adds item to cart |

Full list: [GA4 Recommended Events](https://support.google.com/analytics/answer/9267735)

---

## Custom Funnel Events

### scroll_depth

Granular scroll tracking (GA4's built-in only does 90%).

```json
{
  "event": "scroll_depth",
  "scroll_percent": 50,
  "page_location": "https://example.com/landing"
}
```

| Parameter | Type | Values |
|-----------|------|--------|
| `scroll_percent` | number | 25, 50, 75, 90 |

**GTM Setup**: Scroll Depth trigger, `{{Scroll Depth Threshold}}` variable.

### section_view

Track which content sections users actually see (more precise than scroll).

```json
{
  "event": "section_view",
  "section_name": "pricing",
  "section_index": 3
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `section_name` | string | Identifier for section |
| `section_index` | number | Order on page (optional) |

**HTML**:
```html
<section class="ga-section-tracking" data-section-name="features">
```

**GTM Setup**: Element Visibility trigger, 50% visible, once per element.

### cta_click

Track call-to-action interactions.

```json
{
  "event": "cta_click",
  "cta_text": "Start Free Trial",
  "cta_position": "hero",
  "cta_destination": "/signup"
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `cta_text` | string | Button/link text |
| `cta_position` | string | hero, nav, footer, pricing, sidebar |
| `cta_destination` | string | Target URL (optional) |

### feature_use

Track in-app feature engagement.

```json
{
  "event": "feature_use",
  "feature_name": "export_report",
  "feature_category": "reports",
  "feature_value": "csv"
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `feature_name` | string | Specific feature used |
| `feature_category` | string | Feature grouping (optional) |
| `feature_value` | string | Feature-specific value (optional) |

**Strategy**: Single event + parameters > many separate events (avoids GA4's ~500 event name limit).

### experiment_view / experiment_convert

For A/B testing tracking.

```json
{
  "event": "experiment_view",
  "experiment_name": "hero_cta_test",
  "experiment_variant": "B"
}
```

Include `experiment_variant` in conversion events too:

```json
{
  "event": "sign_up",
  "method": "google",
  "experiment_variant": "B"
}
```

---

## Custom Parameters

Register in GA4 Admin > Custom Definitions before they appear in reports.

### Event-Scoped Parameters

| Parameter | Scope | Description |
|-----------|-------|-------------|
| `scroll_percent` | Event | Scroll depth percentage |
| `cta_text` | Event | Button text clicked |
| `cta_position` | Event | Location on page |
| `section_name` | Event | Page section viewed |
| `feature_name` | Event | Feature used |
| `feature_category` | Event | Feature group |
| `experiment_name` | Event | A/B test name |
| `experiment_variant` | Event | A/B test variant |

### How to Register

1. GA4 Admin > Custom Definitions > Create custom dimension
2. Dimension name: Friendly name for reports
3. Scope: Event (most cases) or User
4. Event parameter: Exact parameter name from your events

**Note**: Takes 24-48h to appear in reports after creation.

---

## User Properties

Persistent attributes tied to users (not events).

### Setting User Properties

**Via dataLayer**:
```tsx
window.dataLayer?.push({
  user_properties: {
    customer_status: 'paid',
    plan_tier: 'pro',
    signup_date: '2025-01-15'
  }
});
```

**Via GTM**: Create GA4 User Property tag.

### Common User Properties

| Property | Type | Description |
|----------|------|-------------|
| `customer_status` | string | "anonymous", "paid", "churned" |
| `plan_tier` | string | "starter", "pro", "enterprise" |
| `signup_date` | string | ISO date of sign-up |
| `user_id` | string | Your internal user ID |

### User-ID for Cross-Session

Push `user_id` after authentication:

```tsx
window.dataLayer?.push({ user_id: session.user.id });
```

Configure in GTM's GA4 Config tag:
- Fields to Set > `user_id` = `{{DL - user_id}}`

This enables:
- Cross-device tracking
- Accurate unique user counts
- Better retention metrics

---

## Event Naming Rules

### Constraints

| Rule | Limit |
|------|-------|
| Event name length | 40 characters max |
| Event name format | Lowercase, underscores, start with letter |
| Unique events per property | ~500 |
| Parameters per event | 25 max |
| Parameter name length | 40 characters max |
| Parameter value length | 100 characters max |

### Good vs Bad

```javascript
// GOOD
'sign_up'
'cta_click'
'feature_use'
'scroll_depth'

// BAD
'SignUp'              // No camelCase
'cta-click'           // No hyphens
'1_event'             // Can't start with number
'user_clicked_the_main_hero_signup_button'  // Too long/specific
```

### Consolidation Strategy

```javascript
// BAD: Separate events (wastes event name quota)
'clicked_hero_cta'
'clicked_nav_cta'
'clicked_footer_cta'
'clicked_pricing_cta'

// GOOD: Single event + parameter
{
  event: 'cta_click',
  cta_position: 'hero'  // or 'nav', 'footer', 'pricing'
}
```

---

## Quick Reference

### Full Event Payload Example

```tsx
window.dataLayer?.push({
  event: 'sign_up',
  method: 'google',
  user_id: 'usr_abc123',
  experiment_variant: 'B',
  user_properties: {
    customer_status: 'paid',
    plan_tier: 'pro'
  }
});
```

### Registration Checklist

- [ ] All custom parameters registered in GA4 Custom Definitions
- [ ] User properties registered (scope: User)
- [ ] 24-48h wait after registration for data to appear
- [ ] Test in DebugView to confirm params are received
