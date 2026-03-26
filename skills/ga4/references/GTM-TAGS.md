# GTM Tag Configurations

## Table of Contents
- [Initial Setup](#initial-setup)
- [GA4 Configuration Tag](#ga4-configuration-tag)
- [User-ID Configuration](#user-id-configuration)
- [Scroll Depth Tracking](#scroll-depth-tracking)
- [Section Visibility Tracking](#section-visibility-tracking)
- [CTA Click Tracking](#cta-click-tracking)
- [Custom Event Tags](#custom-event-tags)
- [Consent Mode](#consent-mode)
- [Publishing & Testing](#publishing--testing)

---

## Initial Setup

### 1. Create GTM Container

1. Go to [tagmanager.google.com](https://tagmanager.google.com)
2. Create Account > Create Container (Web)
3. Copy container ID: `GTM-XXXXXXX`

### 2. Install in Next.js 16

```bash
npm install @next/third-parties
```

```tsx
// app/layout.tsx
import { GoogleTagManager } from '@next/third-parties/google'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <GoogleTagManager gtmId="GTM-XXXXXXX" />
      </body>
    </html>
  )
}
```

**What @next/third-parties does**:
- Injects GTM script after hydration (not blocking)
- Adds `<noscript>` fallback automatically
- Handles client-side navigation for SPA

### Manual Installation (Alternative)

If not using @next/third-parties:

```tsx
// app/layout.tsx
import Script from 'next/script'

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <Script id="gtm" strategy="afterInteractive">
          {`(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
          new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
          j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
          'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
          })(window,document,'script','dataLayer','GTM-XXXXXXX');`}
        </Script>
      </head>
      <body>
        <noscript>
          <iframe
            src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX"
            height="0"
            width="0"
            style={{ display: 'none', visibility: 'hidden' }}
          />
        </noscript>
        {children}
      </body>
    </html>
  )
}
```

---

## GA4 Configuration Tag

**Purpose**: Initialize GA4 and send pageviews on every route.

### Basic Configuration

| Setting | Value |
|---------|-------|
| Tag Type | Google Analytics: GA4 Configuration |
| Measurement ID | `G-XXXXXXXXXX` |
| Trigger | All Pages |

### With Debug Mode

For testing, add a debug_mode parameter:

| Field Name | Value |
|------------|-------|
| debug_mode | true |

**Remove or set to false before production!**

---

## User-ID Configuration

Enable cross-session, cross-device tracking for logged-in users.

### Step 1: Push user_id to dataLayer

```tsx
// After Supabase auth confirms
useEffect(() => {
  const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
    if (session?.user) {
      window.dataLayer?.push({ user_id: session.user.id });
    }
  });
  return () => subscription.unsubscribe();
}, []);
```

### Step 2: Create Data Layer Variable

| Setting | Value |
|---------|-------|
| Variable Type | Data Layer Variable |
| Data Layer Variable Name | `user_id` |
| Variable Name | `DL - user_id` |

### Step 3: Configure GA4 Config Tag

In your GA4 Configuration tag:

**Fields to Set**:
| Field Name | Value |
|------------|-------|
| user_id | `{{DL - user_id}}` |

### Step 4: Enable in GA4

1. GA4 Admin > Data Streams > Your stream
2. Configure tag settings > User-ID: Enable

**Benefits**:
- Same user tracked across devices/browsers
- More accurate unique user counts
- Better retention and cohort analysis

---

## Scroll Depth Tracking

Track 25%, 50%, 75%, 90% scroll milestones (GA4's built-in only does 90%).

### Step 1: Enable Built-in Variables

Variables > Configure > Enable:
- ☑ Scroll Depth Threshold
- ☑ Scroll Depth Units
- ☑ Scroll Direction

### Step 2: Create Scroll Trigger

| Setting | Value |
|---------|-------|
| Trigger Type | Scroll Depth |
| Trigger Name | `Scroll - 25/50/75/90` |
| Scroll Type | Vertical Scroll Depths |
| Percentages | `25, 50, 75, 90` |
| Enable this trigger on | All Pages |

### Step 3: Create GA4 Event Tag

| Setting | Value |
|---------|-------|
| Tag Type | Google Analytics: GA4 Event |
| Configuration Tag | Your GA4 Config |
| Event Name | `scroll_depth` |
| Trigger | `Scroll - 25/50/75/90` |

**Event Parameters**:
| Parameter Name | Value |
|----------------|-------|
| scroll_percent | `{{Scroll Depth Threshold}}` |

---

## Section Visibility Tracking

Track which specific page sections users actually view (more precise than scroll).

### Step 1: Add Tracking Attributes to HTML

```tsx
<section className="ga-section-tracking" data-section-name="hero">
  {/* Hero content */}
</section>

<section className="ga-section-tracking" data-section-name="features">
  {/* Features content */}
</section>

<section className="ga-section-tracking" data-section-name="pricing">
  {/* Pricing content */}
</section>

<section className="ga-section-tracking" data-section-name="testimonials">
  {/* Testimonials */}
</section>
```

### Step 2: Create Auto-Event Variable

| Setting | Value |
|---------|-------|
| Variable Type | Auto-Event Variable |
| Variable Type | Element Attribute |
| Attribute Name | `data-section-name` |
| Variable Name | `AEV - section-name` |

### Step 3: Create Element Visibility Trigger

| Setting | Value |
|---------|-------|
| Trigger Type | Element Visibility |
| Selection Method | CSS Selector |
| Element Selector | `.ga-section-tracking` |
| When to fire | Once per element |
| Minimum Percent Visible | 50 |
| Observe DOM changes | ☑ (for SPAs) |

### Step 4: Create GA4 Event Tag

| Setting | Value |
|---------|-------|
| Event Name | `section_view` |

**Event Parameters**:
| Parameter Name | Value |
|----------------|-------|
| section_name | `{{AEV - section-name}}` |

---

## CTA Click Tracking

Three methods from simplest to most flexible.

### Method A: No-Code (GTM DOM Variables)

Best for static buttons with fixed text.

#### HTML Markup

```html
<button
  class="cta-signup"
  data-cta_text="Start Free Trial"
  data-cta_position="hero"
>
  Start Free Trial
</button>
```

#### GTM Variables

**Variable 1: CTA Text**
| Setting | Value |
|---------|-------|
| Variable Type | DOM Element |
| Selection Method | CSS Selector |
| Element Selector | `.cta-signup` |
| Attribute Name | `data-cta_text` |
| Variable Name | `DOM - CTA Text` |

**Variable 2: CTA Position**
| Setting | Value |
|---------|-------|
| Selection Method | CSS Selector |
| Element Selector | `.cta-signup` |
| Attribute Name | `data-cta_position` |
| Variable Name | `DOM - CTA Position` |

#### GTM Trigger

| Setting | Value |
|---------|-------|
| Trigger Type | Click - All Elements |
| Fire on | Some Clicks |
| Condition | Click Classes contains `cta-signup` |

#### GTM Tag

| Setting | Value |
|---------|-------|
| Tag Type | GA4 Event |
| Event Name | `cta_click` |

**Parameters**:
| Name | Value |
|------|-------|
| cta_text | `{{DOM - CTA Text}}` |
| cta_position | `{{DOM - CTA Position}}` |

---

### Method B: Custom HTML Tag (Event Listener)

Best for dynamic content or when DOM Variables aren't reliable.

#### Custom HTML Tag

Create a Custom HTML tag that fires on All Pages:

```html
<script>
(function() {
  document.addEventListener('click', function(e) {
    var target = e.target.closest('.cta-signup');
    if (target) {
      window.dataLayer.push({
        event: 'cta_click',
        cta_text: target.getAttribute('data-cta_text') || target.textContent.trim(),
        cta_position: target.getAttribute('data-cta_position') || 'unknown'
      });
    }
  });
})();
</script>
```

#### Custom Event Trigger

| Setting | Value |
|---------|-------|
| Trigger Type | Custom Event |
| Event Name | `cta_click` |

#### Data Layer Variables

| Variable Name | Data Layer Variable Name |
|---------------|-------------------------|
| `DL - cta_text` | `cta_text` |
| `DL - cta_position` | `cta_position` |

#### GA4 Event Tag

Use the DL variables in your GA4 Event tag parameters.

---

### Method C: dataLayer Push from React

Most reliable for React/Next.js apps.

```tsx
// components/CTAButton.tsx
interface CTAButtonProps {
  text: string;
  position: 'hero' | 'nav' | 'footer' | 'pricing';
  href: string;
}

export function CTAButton({ text, position, href }: CTAButtonProps) {
  const handleClick = () => {
    window.dataLayer?.push({
      event: 'cta_click',
      cta_text: text,
      cta_position: position,
      cta_destination: href
    });
  };

  return (
    <a href={href} onClick={handleClick} className="cta-button">
      {text}
    </a>
  );
}
```

GTM: Custom Event trigger for `cta_click` with DL variables.

---

## Custom Event Tags

### Generic Handler for All Custom Events

Handle multiple custom events with one tag pattern.

#### Data Layer Variables

| Variable Name | DL Variable Name |
|---------------|-----------------|
| `DL - feature_name` | `feature_name` |
| `DL - experiment_variant` | `experiment_variant` |
| `DL - method` | `method` |
| `DL - user_id` | `user_id` |

#### Custom Event Trigger (Regex)

| Setting | Value |
|---------|-------|
| Trigger Type | Custom Event |
| Event Name | `sign_up|login|feature_use|cta_click` |
| Use regex matching | ☑ |

#### GA4 Event Tag

| Setting | Value |
|---------|-------|
| Event Name | `{{Event}}` |

**Event Parameters** (add all that apply):
| Parameter | Value |
|-----------|-------|
| method | `{{DL - method}}` |
| feature_name | `{{DL - feature_name}}` |
| experiment_variant | `{{DL - experiment_variant}}` |
| user_id | `{{DL - user_id}}` |

---

## Consent Mode

Required for GDPR compliance if you have EU users.

### Option 1: Consent Mode v2 (Basic)

Update GA4 Config tag with default consent state:

**Fields to Set**:
| Field | Value |
|-------|-------|
| ads_data_redaction | true |
| url_passthrough | true |

Add Consent Initialization tag (fires before all other tags):

```html
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}

// Default: deny all until consent given
gtag('consent', 'default', {
  'ad_storage': 'denied',
  'analytics_storage': 'denied',
  'wait_for_update': 500
});
</script>
```

### Option 2: Update Consent on User Action

When user accepts cookies:

```tsx
function acceptAnalyticsCookies() {
  window.gtag?.('consent', 'update', {
    'analytics_storage': 'granted'
  });
}
```

---

## Publishing & Testing

### Preview Mode

1. In GTM, click **Preview**
2. Enter your site URL
3. Tag Assistant panel shows:
   - ✅ Tags fired (with trigger matched)
   - ❌ Tags not fired (with reason)
   - Variables values at each event

### Debug Checklist

| Check | How |
|-------|-----|
| GTM loaded | Console: `window.google_tag_manager` defined |
| dataLayer events | Console: `window.dataLayer` shows pushes |
| GA4 receiving | GA4 DebugView shows events |
| Params correct | DebugView shows all expected parameters |

### Publish

1. Click **Submit** (top right)
2. Add version name/description
3. Click **Publish**

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Tag not firing | Trigger condition wrong | Check in Preview mode |
| Variables empty | Selector not matching | Test selector in browser |
| Events not in GA4 | Measurement ID wrong | Verify in GA4 Config tag |
| Duplicate events | Multiple triggers | Add trigger exclusions |

---

## Quick Reference

### Trigger Type Cheatsheet

| I want to track... | Trigger Type |
|-------------------|--------------|
| Page loads | Page View |
| Button clicks | Click - All Elements |
| Link clicks | Click - Just Links |
| Scroll depth | Scroll Depth |
| Element appears | Element Visibility |
| Form submit | Form Submission |
| Custom event pushed | Custom Event |
| Time on page | Timer |

### Variable Type Cheatsheet

| I need to capture... | Variable Type |
|---------------------|---------------|
| dataLayer value | Data Layer Variable |
| Element attribute | DOM Element |
| Current event data | Auto-Event Variable |
| Cookie value | 1st Party Cookie |
| URL parameter | URL |
| JavaScript result | Custom JavaScript |
