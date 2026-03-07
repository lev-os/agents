---
name: wcag
description: Make web content accessible to people with disabilities by following POUR principles - Perceivable, Operable, Understandable, Robust
---

# WCAG (Web Content Accessibility Guidelines)

## Overview

The Web Content Accessibility Guidelines (WCAG) are international standards published by the World Wide Web Consortium's (W3C) Web Accessibility Initiative (WAI), defining how to make web content accessible to people with disabilities. WCAG ensures that people with visual, auditory, motor, cognitive, and neurological disabilities can perceive, operate, understand, and interact with digital content.

The guidelines are organized around four foundational principles known as POUR: Perceivable (information presented in ways all users can perceive), Operable (interface usable by all), Understandable (clear information and operation), and Robust (compatible with assistive technologies). WCAG defines three conformance levels: A (minimum), AA (target for most organizations), and AAA (highest). The current version is WCAG 2.2 (October 2023), with 13 guidelines and specific testable success criteria.

## When to Use

- Designing or developing any web content, application, or digital product
- Legal compliance required (ADA, Section 508, EU Accessibility Act)
- Expanding audience reach (1 in 4 adults has a disability in the US)
- Building products for government, education, or healthcare sectors
- Conducting accessibility audits or QA testing
- Onboarding designers/developers to accessibility standards
- Evaluating third-party components or libraries for accessibility

## The Process

### Step 1: Perceivable - Information Presentable to All Users

Ensure all information and UI components can be perceived through multiple senses (not sight alone).

**Text Alternatives (1.1):**
- Provide alt text for images: `<img alt="Bar chart showing 40% revenue increase">`
- Captions for videos, transcripts for audio

**Adaptable Content (1.3):**
- Use semantic HTML: `<nav>`, `<main>`, `<article>` not just `<div>`
- Information not conveyed by color alone (color + icon + text)

**Distinguishable (1.4):**
- 4.5:1 contrast ratio for normal text, 3:1 for large text
- Text resizable to 200% without loss of functionality
- Don't use images of text when actual text works

**Example:** Color-blind user can't see red error states → use red + error icon + "Error: " text prefix.

### Step 2: Operable - Interface Usable by All

Ensure all functionality is accessible via keyboard, with enough time to interact, and without causing seizures.

**Keyboard Accessible (2.1):**
- All functionality available via keyboard (Tab, Enter, Space, Arrows)
- Visible focus indicators: `button:focus { outline: 2px solid blue; }`
- No keyboard traps (can tab into and out of all elements)

**Enough Time (2.2):**
- No timeouts, or allow users to extend time
- Ability to pause/stop auto-updating content (carousels, news tickers)

**Navigable (2.4):**
- Skip navigation links: "Skip to main content"
- Descriptive page titles and headings (`<h1>`, `<h2>` hierarchy)
- Multiple ways to navigate (menu, search, sitemap)

**Example:** Keyboard-only user navigating form - can tab between fields, see focus state, submit with Enter key.

### Step 3: Understandable - Clear Information and Operation

Make content readable, predictable, and help users avoid/correct mistakes.

**Readable (3.1):**
- Specify language: `<html lang="en">`
- Avoid jargon, define unusual terms
- Reading level appropriate for audience

**Predictable (3.2):**
- Consistent navigation across pages
- No unexpected context changes (opening link in new tab? warn user)
- Predictable form behavior (focus on field doesn't auto-submit form)

**Input Assistance (3.3):**
- Clear error messages: "Email format invalid. Example: user@example.com"
- Labels for all form inputs: `<label for="email">Email</label>`
- Error prevention: confirm before submitting irreversible actions

**Example:** User misspells email → inline error message explains format + example + error persists until fixed.

### Step 4: Robust - Compatible with Assistive Technologies

Ensure content works across browsers, devices, and assistive technologies now and in the future.

**Compatible (4.1):**
- Valid HTML (proper nesting, unique IDs, closed tags)
- ARIA attributes for complex widgets: `role="dialog"`, `aria-labelledby`, `aria-describedby`
- Status messages announced to screen readers: `role="status"`, `aria-live="polite"`

**Example:** Custom dropdown built with `<div>` instead of `<select>` → add `role="listbox"`, `role="option"`, keyboard handling, and `aria-expanded` to work with screen readers.

### Step 5: Test with Real Users and Assistive Technology

Automated tools catch ~30% of issues. Manual testing with keyboard, screen readers, and real users finds the rest.

**Testing checklist:**
- Keyboard navigation (unplug mouse, use only keyboard)
- Screen reader (NVDA, JAWS, VoiceOver) - can you complete tasks?
- Zoom to 200%, resize text - does layout break?
- Color contrast checker tools
- User testing with people who use assistive technologies

### Step 6: Aim for AA Conformance (Recommended)

Level A is minimum (severe accessibility barriers removed). AA is the target for most organizations (addresses major barriers, legally defensible). AAA is aspirational (not always achievable for all content).

**AA requirements include:** 4.5:1 contrast, captions for videos, no keyboard traps, clear error messages, focus indicators, skip navigation.

## Example Application

**Situation:** E-commerce site failing accessibility audit - screen reader users couldn't checkout, color-blind users missed error states, keyboard-only navigation broken.

**Application of WCAG:**
- **Perceivable:** Added alt text to all product images, 4.5:1 contrast on text, error states use icon + color + text
- **Operable:** Fixed keyboard navigation (focus indicators visible, tab order logical, Enter submits forms), extended timeout warnings
- **Understandable:** Rewrote error messages ("Invalid input" → "Email must include @ symbol"), added example formats, consistent navigation
- **Robust:** Fixed HTML validation errors, added ARIA labels to custom components, tested with NVDA screen reader

**Outcome:** Accessibility compliance from 34% to 94% (AA level), conversion rate increased 18% (accessible checkout benefited all users), legal risk eliminated.

## Anti-Patterns

- ❌ Treating accessibility as "nice to have" or post-launch addition
- ❌ Relying solely on automated testing tools (miss 70% of issues)
- ❌ Using ARIA as Band-Aid for non-semantic HTML (semantic first, ARIA second)
- ❌ Hiding content with `display: none` and expecting screen readers to access it
- ❌ Removing focus indicators for "aesthetics" (makes keyboard navigation impossible)
- ❌ Building inaccessible components then trying to retrofit ARIA
- ❌ Assuming accessibility only helps disabled users (benefits everyone - mobile, elderly, situational)

## Related

- aria (Accessible Rich Internet Applications - semantic attributes)
- design-systems (bake accessibility into reusable components)
- semantic-html (foundation for accessible markup)
- inclusive-design (designing for diversity from start)
- assistive-technology (screen readers, switch controls, magnifiers)
