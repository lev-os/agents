---
name: aria
description: W3C standard for making web applications accessible to assistive technologies through semantic roles, properties, and states
---

# ARIA (Accessible Rich Internet Applications)

## Overview
ARIA (Accessible Rich Internet Applications) is a W3C standard that defines a set of HTML attributes to make web content and applications accessible to people with disabilities. It bridges the gap between complex, dynamic web applications and assistive technologies like screen readers, enabling users who rely on these tools to understand and interact with modern interfaces.

Native HTML elements (buttons, links, form inputs) have built-in accessibility semantics. But when developers build custom components (date pickers, autocomplete, tabs, modals) or single-page apps with dynamic content, assistive technologies lose context. ARIA provides:
- **Roles**: Define what an element is (button, navigation, alert, dialog)
- **Properties**: Describe characteristics (label, description, required, checked)
- **States**: Communicate dynamic changes (expanded, selected, hidden, invalid)

ARIA is a Living W3C Recommendation, meaning it evolves with web technology. As of 2025, ARIA 1.3 is the active standard.

## When to Use
- Building custom UI components without native HTML equivalents (autocomplete, tree view, tab panels)
- Creating single-page applications with dynamic content updates
- Implementing interactive widgets (drag-and-drop, tooltips, carousels)
- Updating content without page reloads (live regions, notifications)
- Enhancing semantic meaning where HTML falls short
- Ensuring legal compliance (WCAG 2.1 AA requires accessible interfaces)

## The Five Rules of ARIA

### Rule 1: Don't Use ARIA If You Can Use Native HTML
Native HTML elements have built-in keyboard support, focus management, and semantics. Always prefer `<button>` over `<div role="button">`. Use `<nav>` over `<div role="navigation">`. Semantic HTML is simpler, more robust, and better supported.

**Example:** Don't use `<div role="button" tabindex="0">Click Me</div>`. Use `<button>Click Me</button>` instead.

### Rule 2: Don't Change Native Semantics Unless Absolutely Necessary
Don't override native element roles. `<button role="heading">` is confusing and breaks expectations. If you need a heading, use `<h1>`-`<h6>`, not a button.

**Example:** L `<h2 role="button">` ’ Use `<h2>Heading</h2>` and `<button>Action</button>` separately.

### Rule 3: All Interactive ARIA Controls Must Be Keyboard Accessible
If a user can click it with a mouse, they must be able to operate it with a keyboard. Tab to focus, Enter/Space to activate, Arrow keys for navigation within widgets. Don't create keyboard traps.

**Example:** Custom dropdown menu requires: Tab (focus trigger), Enter (open menu), Arrow keys (navigate options), Enter (select), Escape (close).

### Rule 4: Don't Use role="presentation" or aria-hidden="true" on Focusable Elements
Hiding an element from screen readers while allowing keyboard focus creates confusion. Users tab to "nothing" and don't know what they've focused. Remove from tab order if hidden from assistive tech.

**Example:** L `<button aria-hidden="true">Save</button>` ’ If hidden, use `tabindex="-1"` or remove from DOM.

### Rule 5: All Interactive Elements Must Have Accessible Names
Buttons, links, and form inputs need labels. Use visible text, `aria-label`, or `aria-labelledby`. Screen reader users must know what an element does before interacting.

**Example:** Icon-only button: `<button aria-label="Close dialog"><X icon></button>`

## Implementation Steps

### Step 1: Start with Semantic HTML
Use native elements first. Only add ARIA when HTML semantics are insufficient. This foundation ensures maximum compatibility and minimum maintenance.

**Example:** Form with native elements needs minimal ARIAjust associate labels with inputs using `<label for="email">`.

### Step 2: Identify Missing Semantics
When building custom widgets, ask: What is this element? What state is it in? How does it relate to other elements? These questions map to ARIA roles, states, and properties.

**Example:** Custom tab interfacenative HTML has no "tab" element. Needs ARIA: `role="tablist"`, `role="tab"`, `role="tabpanel"`, `aria-selected`, `aria-controls`.

### Step 3: Apply Appropriate ARIA Roles
Roles define element type. Use landmark roles for page structure (`banner`, `navigation`, `main`, `contentinfo`), widget roles for interactive components (`button`, `checkbox`, `dialog`, `menu`), and document roles for content structure (`article`, `heading`, `list`).

**Example:** Page header: `<header role="banner">`, Main content: `<main role="main">`, Footer: `<footer role="contentinfo">`.

### Step 4: Add ARIA Properties
Properties describe characteristics. Common properties: `aria-label` (accessible name), `aria-labelledby` (reference to label element), `aria-describedby` (additional description), `aria-required` (mandatory field), `aria-invalid` (validation error).

**Example:** Search input: `<input type="text" aria-label="Search products" aria-describedby="search-help">` with `<div id="search-help">Enter product name or SKU</div>`.

### Step 5: Manage ARIA States
States reflect dynamic changes. Update via JavaScript when UI changes. Common states: `aria-expanded` (collapsible sections), `aria-selected` (tabs, list items), `aria-checked` (checkboxes, switches), `aria-disabled` (inactive elements), `aria-hidden` (content not relevant to assistive tech).

**Example:** Accordion: `<button aria-expanded="false" aria-controls="panel-1">Section Title</button>`. When clicked, update to `aria-expanded="true"`.

### Step 6: Implement Keyboard Support
ARIA roles create expectations for keyboard behavior. Follow ARIA Authoring Practices Guide patterns. Tab moves between widgets, Arrow keys navigate within widgets, Enter/Space activate, Escape cancels or closes.

**Example:** Modal dialog: Focus trap (Tab cycles within modal), Escape closes, Return focus to trigger element on close.

### Step 7: Use Live Regions for Dynamic Content
When content updates without page reload (notifications, status messages, search results), use `aria-live` to announce changes. Values: `polite` (wait for pause in speech), `assertive` (interrupt immediately), `off` (don't announce).

**Example:** Form submission: `<div role="status" aria-live="polite">Form submitted successfully!</div>`. Screen reader announces after current speech completes.

### Step 8: Test with Assistive Technologies
Test with actual screen readers (NVDA on Windows, VoiceOver on macOS/iOS, TalkBack on Android). Automated tools (axe, Lighthouse) catch common errors but can't evaluate user experience. Manual testing reveals confusing interactions.

**Example:** Navigate entire UI with keyboard only. Use screen reader to complete key tasks. Can you tell what's focused? What actions are available? What happens when you interact?

## Common ARIA Patterns

**Modal Dialogs:** `role="dialog"`, `aria-modal="true"`, `aria-labelledby` (dialog title), focus trap, Escape to close.

**Tab Panels:** `role="tablist"` (container), `role="tab"` (triggers), `role="tabpanel"` (content), `aria-selected`, `aria-controls`.

**Disclosure Widgets (Accordions):** `<button aria-expanded="false" aria-controls="content-id">`, Arrow keys to navigate, Enter/Space to toggle.

**Autocomplete:** `role="combobox"`, `aria-expanded`, `aria-autocomplete="list"`, `aria-activedescendant` (current suggestion), `role="listbox"` for results.

**Alerts & Notifications:** `role="alert"` (important, assertive), `role="status"` (polite updates), `aria-live="polite"` or `"assertive"`.

## Common Pitfalls
- L **ARIA Soup:** Adding ARIA everywhere. Overuse creates noise for screen readers. Use only when necessary.
- L **Stale States:** Setting `aria-expanded="false"` but not updating to `"true"` when opened. Inconsistent state confuses users.
- L **Missing Keyboard Support:** Adding `role="button"` without keyboard activation. Roles create expectationsfulfill them.
- L **Invisible Labels:** `aria-label` on `<div>` without role. Non-interactive elements ignore aria-label unless they have a role.
- L **Redundant ARIA:** `<button aria-label="Close">Close</button>`. Visible text is already accessible, aria-label overrides unnecessarily.
- L **Breaking Focus:** Modal opens but focus stays on trigger. Users tab through background content instead of modal. Trap focus in modal.

## Real-World Application

**Situation:** Custom dropdown menu built with divs fails accessibility audit. Screen reader users can't navigate options or understand menu state.

**Current Implementation (Broken):**
```html
<div class="dropdown" onclick="toggleMenu()">
  Options
  <div class="menu" style="display:none;">
    <div onclick="selectOption(1)">Option 1</div>
    <div onclick="selectOption(2)">Option 2</div>
  </div>
</div>
```

**Problems:** No semantic roles, not keyboard accessible, no state indication, click handlers on divs.

**ARIA Solution:**
```html
<button aria-haspopup="true" aria-expanded="false" aria-controls="menu-1" id="menu-button">
  Options
</button>
<ul role="menu" id="menu-1" aria-labelledby="menu-button" hidden>
  <li role="menuitem" tabindex="-1">Option 1</li>
  <li role="menuitem" tabindex="-1">Option 2</li>
</ul>
```

**JavaScript:** Update `aria-expanded` on toggle, manage focus (Enter opens, Arrow keys navigate, Enter selects, Escape closes), return focus to button on close.

**Outcome:** Passes WCAG 2.1 AA. Screen reader announces "Options, button, collapsed" ’ "Options, button, expanded, menu with 2 items" ’ "Option 1, menu item 1 of 2".

## Complementary Frameworks
- WCAG (Web Content Accessibility GuidelinesARIA helps achieve compliance)
- Semantic HTML (foundation before adding ARIA)
- Keyboard Navigation Patterns (ARIA creates expectations for keyboard UX)
- Screen Reader Testing (validate ARIA implementation)

## Learning Resources
- WAI-ARIA Authoring Practices Guide (APG) by W3C (canonical implementation patterns)
- MDN Web Docs: ARIA documentation and examples
- WebAIM: ARIA tutorials and testing techniques
- axe DevTools: Automated accessibility testing browser extension

## Metadata
**Domain:** Web Development, Accessibility, UI Engineering
**Confidence:** High - W3C standard with 15+ years of adoption
**Practitioner Weight:** 10/10 (Mandatory for accessible web applications)
**Execution Complexity:** Medium-High (Clear rules, but implementation requires testing)
**ROI Evidence:** High - Legal compliance, expanded user base, improved UX for all

## Related
- wcag
- semantic-html
- accessibility-testing
- keyboard-navigation
- screen-reader-testing
- inclusive-design
