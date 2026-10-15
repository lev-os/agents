---
name: ui-ux-pro-max
description: Comprehensive design guide for web and mobile applications. Contains 50+ styles, 97 color palettes, 57 font pairings, 99 UX guidelines, and 25 chart types across 9 technology stacks.
---

# UI/UX Pro Max - Design Intelligence

Comprehensive design guide for web and mobile applications containing 50+ styles, 97 color palettes, 57 font pairings, 99 UX guidelines, and 25 chart types across 9 technology stacks with searchable database and priority-based recommendations.

## When to Apply

Reference these guidelines when:
* Designing new UI components or pages
* Choosing color palettes and typography
* Reviewing code for UX issues
* Building landing pages or dashboards
* Implementing accessibility requirements

## Rule Categories by Priority

| Priority | Category            | Impact   | Domain            |
| -------- | ------------------- | -------- | ----------------- |
| 1        | Accessibility       | CRITICAL | ux                |
| 2        | Touch & Interaction | CRITICAL | ux                |
| 3        | Performance         | HIGH     | ux                |
| 4        | Layout & Responsive | HIGH     | ux                |
| 5        | Typography & Color  | MEDIUM   | typography, color |
| 6        | Animation           | MEDIUM   | ux                |
| 7        | Style Selection     | MEDIUM   | style, product    |
| 8        | Charts & Data       | LOW      | chart             |

## Quick Reference

### 1. Accessibility (CRITICAL)

* `color-contrast` - Minimum 4.5:1 ratio for normal text
* `focus-states` - Visible focus rings on interactive elements
* `alt-text` - Descriptive alt text for meaningful images
* `aria-labels` - aria-label for icon-only buttons
* `keyboard-nav` - Tab order matches visual order
* `form-labels` - Use label with for attribute

### 2. Touch & Interaction (CRITICAL)

* `touch-target-size` - Minimum 44x44px touch targets
* `hover-vs-tap` - Use click/tap for primary interactions
* `loading-buttons` - Disable button during async operations
* `error-feedback` - Clear error messages near problem
* `cursor-pointer` - Add cursor-pointer to clickable elements

### 3. Performance (HIGH)

* `image-optimization` - Use WebP, srcset, lazy loading
* `reduced-motion` - Check prefers-reduced-motion
* `content-jumping` - Reserve space for async content

### 4. Layout & Responsive (HIGH)

* `viewport-meta` - width=device-width initial-scale=1
* `readable-font-size` - Minimum 16px body text on mobile
* `horizontal-scroll` - Ensure content fits viewport width
* `z-index-management` - Define z-index scale (10, 20, 30, 50)

### 5. Typography & Color (MEDIUM)

* `line-height` - Use 1.5-1.75 for body text
* `line-length` - Limit to 65-75 characters per line
* `font-pairing` - Match heading/body font personalities

### 6. Animation (MEDIUM)

* `duration-timing` - Use 150-300ms for micro-interactions
* `transform-performance` - Use transform/opacity, not width/height
* `loading-states` - Skeleton screens or spinners

### 7. Style Selection (MEDIUM)

* `style-match` - Match style to product type
* `consistency` - Use same style across all pages
* `no-emoji-icons` - Use SVG icons, not emojis

### 8. Charts & Data (LOW)

* `chart-type` - Match chart type to data type
* `color-guidance` - Use accessible color palettes
* `data-table` - Provide table alternative for accessibility

## How to Use

**Step 1: Analyze User Requirements**

Extract key information: product type (SaaS, e-commerce, portfolio, dashboard), style keywords (minimal, playful, professional), industry (healthcare, fintech, gaming), stack (React, Vue, Next.js, default html-tailwind).

**Step 2: Generate Design System (REQUIRED)**

Always start with `--design-system` flag to get comprehensive recommendations. Command: `python3 skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "Project Name"`

This searches 5 domains in parallel (product, style, color, landing, typography), applies reasoning rules, returns complete design system with pattern, style, colors, typography, effects, and anti-patterns to avoid.

**Step 3: Supplement with Detailed Searches**

Use domain searches for additional details: `--domain style|chart|ux|typography|landing|color`

**Step 4: Stack Guidelines**

Get implementation-specific best practices: `--stack html-tailwind|react|nextjs|vue|svelte|swiftui|react-native|flutter|shadcn`

## Pre-Delivery Checklist

**Visual Quality:**
* No emojis as icons (use SVG from Heroicons/Lucide)
* All icons from consistent set
* Brand logos correct (Simple Icons)
* Hover states don't cause layout shift
* Use theme colors directly (bg-primary) not var() wrapper

**Interaction:**
* All clickable elements have `cursor-pointer`
* Hover states provide clear visual feedback
* Transitions smooth (150-300ms)
* Focus states visible for keyboard navigation

**Light/Dark Mode:**
* Light mode text has sufficient contrast (4.5:1 minimum)
* Glass/transparent elements visible in light mode
* Borders visible in both modes
* Test both modes before delivery

**Layout:**
* Floating elements have proper spacing from edges
* No content hidden behind fixed navbars
* Responsive at 375px, 768px, 1024px, 1440px
* No horizontal scroll on mobile

**Accessibility:**
* All images have alt text
* Form inputs have labels
* Color is not the only indicator
* `prefers-reduced-motion` respected