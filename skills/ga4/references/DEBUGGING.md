# Debugging & Troubleshooting

## Table of Contents
- [Validation Workflow](#validation-workflow)
- [Event-Specific Verification](#event-specific-verification)
- [Debug Tools](#debug-tools)
- [Common Issues](#common-issues)
- [Browser Console Debugging](#browser-console-debugging)
- [Checklist](#checklist)

---

## Validation Workflow

### The Three-Step Process

```
┌─────────────────────────────────────────────────────────────┐
│                    VALIDATION WORKFLOW                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   STEP 1: GTM Preview Mode                                   │
│   ════════════════════════                                   │
│   • Tags fire at correct moments?                            │
│   • Trigger conditions match?                                │
│   • Variables have expected values?                          │
│                     ↓                                        │
│   STEP 2: GA4 DebugView                                      │
│   ═════════════════════                                      │
│   • Events arrive in GA4?                                    │
│   • Event names correct?                                     │
│   • All parameters present?                                  │
│                     ↓                                        │
│   STEP 3: GA4 Realtime Report                                │
│   ═══════════════════════════                                │
│   • Live traffic appears?                                    │
│   • Events from real users?                                  │
│   • Data within 30 seconds?                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: GTM Preview Mode

1. In GTM, click **Preview** (top right)
2. Enter your site URL
3. Navigate your site in the new tab
4. Tag Assistant panel shows:
   - **Tags Fired** (green): Successfully triggered
   - **Tags Not Fired** (red): Trigger conditions not met
   - **Variables**: Current values at each event

**What to verify**:
- [ ] All expected tags fire (GA4 Config, scroll, CTA, etc.)
- [ ] Tags fire exactly once per action (not duplicated)
- [ ] Variables contain correct values
- [ ] No JavaScript errors in console

### Step 2: GA4 DebugView

1. GA4 > Admin > DebugView
2. Debug mode activates automatically when GTM Preview is open
3. Or force debug mode in GA4 Config tag: `debug_mode: true`

**What to verify**:
- [ ] Events stream in real-time as you navigate
- [ ] Event names match expected (e.g., `scroll_depth`, not `scroll`)
- [ ] Click event parameters to see all values
- [ ] User properties appear if configured

### Step 3: GA4 Realtime

1. GA4 > Reports > Realtime
2. Open incognito window (new session)
3. Perform test actions

**What to verify**:
- [ ] Events appear within 30 seconds
- [ ] Conversions show in "Conversions by event" card
- [ ] User count increments

---

## Event-Specific Verification

### page_view Events

**Expected behavior**: Fire on every route change.

| Check | Method |
|-------|--------|
| Fires on initial load | GTM Preview: Check first event |
| Fires on navigation | Navigate to new page, check Preview |
| Correct page_location | DebugView: Check parameter value |
| No duplicates | Should fire exactly once per page |

**Troubleshooting**:
| Issue | Cause | Fix |
|-------|-------|-----|
| No pageviews | GA4 Config tag not firing | Check All Pages trigger |
| Wrong page_location | SPA not updating | Enhanced Measurement handles this |
| Duplicate pageviews | Multiple GA4 Config tags | Remove duplicates |

### scroll_depth Events

**Expected behavior**: Fire at 25%, 50%, 75%, 90% thresholds.

| Check | Method |
|-------|--------|
| Fires at each threshold | Scroll slowly, watch Preview |
| scroll_percent value correct | DebugView: Should show 25, 50, 75, or 90 |
| Fires once per threshold | Scroll up and down, shouldn't re-fire |
| Works on all pages | Test on short and long pages |

**Troubleshooting**:
| Issue | Cause | Fix |
|-------|-------|-----|
| Fires immediately | Page shorter than viewport | Add minimum page height condition |
| Never fires | Wrong trigger type | Use Vertical Scroll Depths |
| Wrong percentages | Misconfigured trigger | Check percentages: `25, 50, 75, 90` |
| Fires multiple times | "Once per page" not set | Enable in trigger settings |

### section_view Events

**Expected behavior**: Fire when section becomes 50% visible.

| Check | Method |
|-------|--------|
| section_name correct | DebugView: Check parameter |
| Fires once per section | Scroll past multiple times |
| Works for all sections | Test each tracked section |
| Fires for dynamic sections | Test SPA navigation |

**Troubleshooting**:
| Issue | Cause | Fix |
|-------|-------|-----|
| Never fires | CSS selector not matching | Check `.ga-section-tracking` class |
| section_name undefined | Attribute name wrong | Use `data-section-name` exactly |
| Fires for wrong elements | Selector too broad | Be more specific |
| Doesn't work on SPA nav | DOM changes not observed | Enable "Observe DOM changes" |

### cta_click Events

**Expected behavior**: Fire on CTA button clicks.

| Check | Method |
|-------|--------|
| Fires on click | Click CTA, check Preview |
| cta_text correct | DebugView: Check parameter |
| cta_position correct | Should match data attribute |
| Fires for all CTAs | Test each CTA on page |

**Troubleshooting**:
| Issue | Cause | Fix |
|-------|-------|-----|
| Never fires | Click trigger condition wrong | Check Click Classes contains `cta-signup` |
| cta_text empty | DOM variable not resolving | Check selector and attribute name |
| Fires but params empty | Clicked child element | Use `.closest()` in Custom HTML |
| Fires multiple times | Event bubbling | Add stopPropagation or debounce |

### sign_up Events

**Expected behavior**: Fire exactly once when user completes registration.

| Check | Method |
|-------|--------|
| Fires after auth | Complete sign-up, check DebugView |
| Fires exactly once | Sign up, refresh, shouldn't re-fire |
| user_id present | Check parameter in DebugView |
| method correct | Should show "google" or auth method |

**Troubleshooting**:
| Issue | Cause | Fix |
|-------|-------|-----|
| Never fires | Auth state change not detected | Check Supabase onAuthStateChange |
| Fires multiple times | Event on every auth change | Add condition for first sign-up only |
| user_id missing | Not pushed to dataLayer | Add `user_id: session.user.id` |
| Fires on login too | Not distinguishing login vs signup | Track first visit vs returning |

**Critical**: This is your conversion event. Test thoroughly!

### feature_use Events

**Expected behavior**: Fire when user interacts with features.

| Check | Method |
|-------|--------|
| feature_name correct | Use feature, check DebugView |
| Fires once per action | Repeat action, should fire each time |
| Different features tracked | Test multiple features |

**Troubleshooting**:
| Issue | Cause | Fix |
|-------|-------|-----|
| feature_name undefined | Variable not in dataLayer | Check push includes feature_name |
| Not firing | Custom event trigger misconfigured | Check event name matches |

---

## Debug Tools

### Browser Console

#### Check dataLayer

```javascript
// View current dataLayer
console.log(window.dataLayer)

// Pretty print
console.table(window.dataLayer)

// Find specific events
window.dataLayer.filter(e => e.event === 'cta_click')
```

#### Watch dataLayer Pushes

```javascript
// Monitor all pushes in real-time
(function() {
  const original = window.dataLayer.push;
  window.dataLayer.push = function() {
    console.log('📊 dataLayer push:', arguments[0]);
    return original.apply(this, arguments);
  }
})();
```

#### Check GTM Loaded

```javascript
// Verify GTM is loaded
console.log('GTM loaded:', typeof window.google_tag_manager !== 'undefined')

// Get container ID
Object.keys(window.google_tag_manager || {}).filter(k => k.startsWith('GTM-'))
```

#### Force Debug Mode

```javascript
// Enable GA4 debug mode manually
window.dataLayer?.push({ debug_mode: true })
```

### Network Tab

1. DevTools > Network
2. Filter: `collect` or `google-analytics`
3. Click request > Payload tab
4. Check event parameters

**What to look for**:
- `en` = event name
- `ep.*` = event parameters
- `up.*` = user properties

### GTM Debug URL

Force GTM Preview on any page:
```
?gtm_debug=x
```

### GA4 DebugView URL

Direct link (replace PROPERTY_ID):
```
https://analytics.google.com/analytics/web/#/m/debugview?wpid=PROPERTY_ID
```

---

## Common Issues

### No Data at All

| Symptom | Cause | Fix |
|---------|-------|-----|
| Zero events in GA4 | GTM not installed | Add `<GoogleTagManager>` to layout |
| GTM loads but no GA4 | No GA4 Config tag | Create tag with Measurement ID |
| GA4 Config exists | Wrong Measurement ID | Verify `G-XXXXXXXXXX` |
| Correct ID | Container not published | Submit and publish in GTM |

### Partial Data

| Symptom | Cause | Fix |
|---------|-------|-----|
| Pageviews but no custom events | Triggers not configured | Set up event triggers |
| Events in GTM, not GA4 | Tag not connected to GA4 Config | Select config in event tag |
| Some users missing | Cookie consent blocking | Check consent mode |
| Intermittent data | Ad blockers | Expected; can't fix fully |

### Duplicate Events

| Symptom | Cause | Fix |
|---------|-------|-----|
| Double pageviews | Multiple GA4 scripts | Remove gtag.js if using GTM |
| Double custom events | Multiple triggers matching | Add exclusion conditions |
| React strict mode doubles | Dev environment | Normal; won't happen in prod |

### Custom Parameters Missing

1. Verify parameter is in dataLayer push
2. Check Data Layer Variable in GTM
3. Confirm parameter is in GA4 Event tag
4. **Register in GA4 Admin > Custom Definitions**
5. Wait 24-48 hours for data to appear

### Cookie Consent Issues

If using consent banner (GDPR):

```tsx
// Events won't fire until consent granted
function hasAnalyticsConsent(): boolean {
  // Check your consent management solution
  return localStorage.getItem('analytics_consent') === 'granted'
}

function trackEvent(event: string, params: object) {
  if (hasAnalyticsConsent()) {
    window.dataLayer?.push({ event, ...params })
  }
}
```

---

## Browser Console Debugging

### Complete Debug Script

```javascript
// Paste in console for comprehensive debugging
(function debugGA4GTM() {
  console.log('=== GA4 + GTM Debug ===');

  // Check GTM
  const gtmLoaded = typeof window.google_tag_manager !== 'undefined';
  console.log('GTM loaded:', gtmLoaded);
  if (gtmLoaded) {
    const containers = Object.keys(window.google_tag_manager).filter(k => k.startsWith('GTM-'));
    console.log('GTM containers:', containers);
  }

  // Check dataLayer
  console.log('dataLayer exists:', Array.isArray(window.dataLayer));
  console.log('dataLayer length:', window.dataLayer?.length || 0);

  // Recent events
  const events = (window.dataLayer || []).filter(e => e.event);
  console.log('Events pushed:', events.map(e => e.event));

  // Check for GA4
  const ga4Loaded = typeof window.gtag !== 'undefined';
  console.log('gtag loaded:', ga4Loaded);

  // Monitor future pushes
  if (window.dataLayer) {
    const original = window.dataLayer.push;
    window.dataLayer.push = function() {
      console.log('📊 New push:', arguments[0]);
      return original.apply(this, arguments);
    };
    console.log('Now monitoring dataLayer pushes...');
  }
})();
```

### Quick Checks

```javascript
// Is GTM loaded?
!!window.google_tag_manager

// Is dataLayer available?
Array.isArray(window.dataLayer)

// Last 5 events
window.dataLayer.slice(-5).filter(e => e.event).map(e => e.event)

// Check specific event was pushed
window.dataLayer.some(e => e.event === 'sign_up')
```

---

## Checklist

### Initial Setup

- [ ] `<GoogleTagManager gtmId="GTM-XXXXXXX" />` in root layout
- [ ] GTM container ID correct
- [ ] GA4 Measurement ID correct (`G-XXXXXXXXXX`)
- [ ] GA4 Configuration tag exists with All Pages trigger
- [ ] GTM container is **published** (not just saved)
- [ ] No duplicate GTM or gtag.js scripts

### Event Tracking

- [ ] Each event has correct name (lowercase, underscores)
- [ ] Parameters passed in dataLayer push
- [ ] Data Layer Variables created in GTM
- [ ] Triggers configured correctly
- [ ] GA4 Event tags use variables
- [ ] Custom dimensions registered in GA4 Admin (24-48h wait)

### Conversions

- [ ] `sign_up` event fires exactly once per conversion
- [ ] Event marked as conversion in GA4 Admin > Events
- [ ] Conversion appears in Realtime after test
- [ ] No false positives (login triggering sign_up)

### User-ID (If configured)

- [ ] `user_id` pushed to dataLayer after auth
- [ ] Data Layer Variable created for `user_id`
- [ ] GA4 Config tag has `user_id` in Fields to Set
- [ ] User-ID enabled in GA4 Admin

### A/B Testing

- [ ] Variant cookie set in middleware
- [ ] Cookie value accessible client-side
- [ ] `experiment_variant` included in events
- [ ] Custom dimension registered in GA4

### Pre-Launch

- [ ] Remove `debug_mode: true` from GA4 Config
- [ ] Test in incognito (fresh session)
- [ ] Test on mobile device
- [ ] Verify cookie consent flow works
- [ ] Check no console errors

---

## Getting Help

### Official Documentation

- GTM: [support.google.com/tagmanager](https://support.google.com/tagmanager)
- GA4: [support.google.com/analytics](https://support.google.com/analytics)
- GA4 Events: [developers.google.com/analytics/devguides/collection/ga4](https://developers.google.com/analytics/devguides/collection/ga4)
- @next/third-parties: [nextjs.org/docs/app/building-your-application/optimizing/third-party-libraries](https://nextjs.org/docs/app/building-your-application/optimizing/third-party-libraries)

### Community

- Stack Overflow: `[google-analytics-4]` or `[google-tag-manager]` tags
- GA4 Subreddit: r/GoogleAnalytics
- Measure Slack: measureslack.com

### Common Error Messages

| Error | Meaning | Fix |
|-------|---------|-----|
| "Measurement ID not set" | GA4 Config tag missing ID | Add `G-XXXXXXXXXX` |
| "No HTTP response" | Network blocked | Check ad blockers, consent |
| "Container not found" | Wrong GTM ID | Verify `GTM-XXXXXXX` |
| "Trigger never matched" | Conditions not met | Review trigger settings |
