# UI/UX Polish Checklist — Reference

## Table of Contents
- [Visual Polish](#visual-polish)
- [Interaction Design](#interaction-design)
- [Desktop Specifics](#desktop-specifics)
- [Mobile Specifics](#mobile-specifics)
- [Accessibility](#accessibility)
- [Performance](#performance)

---

## Visual Polish

### Spacing & Layout
- [ ] Consistent padding throughout
- [ ] Vertical rhythm maintained
- [ ] Grid alignment consistent
- [ ] Section spacing uniform
- [ ] Component margins consistent
- [ ] No awkward whitespace gaps

### Typography
- [ ] Clear heading hierarchy (h1 > h2 > h3)
- [ ] Consistent body text size
- [ ] Appropriate line height (1.4-1.6 for body)
- [ ] Readable font sizes (16px+ for body)
- [ ] Limited font families (2-3 max)
- [ ] Consistent font weights

### Colors
- [ ] Primary/secondary colors defined
- [ ] Accent color used consistently
- [ ] Sufficient contrast ratios (4.5:1 for text)
- [ ] Semantic colors (error=red, success=green, etc.)
- [ ] Dark mode support (if applicable)
- [ ] Color blindness friendly

### Visual Hierarchy
- [ ] Most important elements stand out
- [ ] CTAs clearly visible
- [ ] Secondary actions de-emphasized
- [ ] Content scannable
- [ ] Focal points clear

### Polish Details
- [ ] Consistent border radius
- [ ] Appropriate shadow depths
- [ ] Icon size consistency
- [ ] Image aspect ratios maintained
- [ ] Placeholder states designed

---

## Interaction Design

### Button States
- [ ] Default state clear
- [ ] Hover state visible
- [ ] Active/pressed state
- [ ] Focus state (keyboard)
- [ ] Disabled state muted
- [ ] Loading state

### Form Elements
- [ ] Clear labels
- [ ] Placeholder text helpful
- [ ] Error states visible
- [ ] Validation feedback immediate
- [ ] Success confirmation
- [ ] Clear required indicators

### Feedback
- [ ] Click/tap feedback
- [ ] Loading indicators
- [ ] Progress indicators (long operations)
- [ ] Success/error toasts
- [ ] Confirmation dialogs (destructive actions)

### Navigation
- [ ] Current location clear
- [ ] Breadcrumbs (if deep hierarchy)
- [ ] Back navigation obvious
- [ ] Menu organization logical
- [ ] Search accessible

### Transitions
- [ ] Smooth page transitions
- [ ] Element entrance animations
- [ ] Exit animations
- [ ] Consistent timing (200-300ms)
- [ ] Easing functions appropriate
- [ ] No jarring movements

---

## Desktop Specifics

### Layout
- [ ] Multi-column layouts utilized
- [ ] Sidebar navigation (if applicable)
- [ ] Appropriate max-width constraints
- [ ] Above-fold content optimized
- [ ] Wide screen handling

### Keyboard Support
- [ ] Tab order logical
- [ ] Focus visible
- [ ] Escape closes modals
- [ ] Enter submits forms
- [ ] Shortcuts documented (power users)

### Hover States
- [ ] All interactive elements have hover
- [ ] Hover previews (where appropriate)
- [ ] Tooltip on hover (for icons)
- [ ] Cursor changes (pointer for clickable)

### Desktop Patterns
- [ ] Right-click context menus (if applicable)
- [ ] Drag and drop (where appropriate)
- [ ] Resizable panels (if applicable)
- [ ] Multi-select with shift/ctrl

---

## Mobile Specifics

### Touch Targets
- [ ] Minimum 44x44px touch targets
- [ ] Adequate spacing between targets
- [ ] Thumb-friendly placement
- [ ] No precision tapping required

### Mobile Navigation
- [ ] Bottom navigation (if applicable)
- [ ] Hamburger menu accessible
- [ ] Swipe gestures (where expected)
- [ ] Pull-to-refresh (if applicable)
- [ ] Back gesture supported

### Mobile Layouts
- [ ] Single column layouts
- [ ] Full-width buttons
- [ ] Scrollable content
- [ ] No horizontal scroll (except carousels)
- [ ] Sticky headers (where helpful)

### Mobile Patterns
- [ ] Bottom sheets for actions
- [ ] Modal drawers from edges
- [ ] Floating action buttons (if appropriate)
- [ ] Card-based layouts
- [ ] Collapsible sections

### Mobile Performance
- [ ] Fast initial load
- [ ] Images optimized
- [ ] Lazy loading implemented
- [ ] Smooth scrolling
- [ ] No layout shifts

---

## Accessibility

### WCAG Basics
- [ ] Color contrast (4.5:1 text, 3:1 UI)
- [ ] Text resizable to 200%
- [ ] Focus indicators visible
- [ ] Skip links available
- [ ] Alt text on images

### Screen Reader Support
- [ ] Semantic HTML
- [ ] ARIA labels where needed
- [ ] Heading hierarchy correct
- [ ] Form labels associated
- [ ] Live regions for updates

### Motor Accessibility
- [ ] Keyboard fully navigable
- [ ] No time limits (or extendable)
- [ ] Click targets adequate
- [ ] No gestures required (alternatives exist)

### Visual Accessibility
- [ ] Not relying on color alone
- [ ] Motion reducible (prefers-reduced-motion)
- [ ] Text not in images
- [ ] Sufficient font sizes

---

## Performance

### Load Performance
- [ ] Core content loads fast
- [ ] Above-fold prioritized
- [ ] Critical CSS inlined
- [ ] Images lazy loaded
- [ ] Fonts optimized

### Interaction Performance
- [ ] No input lag
- [ ] Smooth scrolling (60fps)
- [ ] Quick response to clicks
- [ ] Animations performant
- [ ] No jank

### Perception
- [ ] Loading states immediate
- [ ] Skeleton screens
- [ ] Progressive enhancement
- [ ] Optimistic updates
- [ ] Perceived performance good

---

## Quality Benchmarks

### Stripe-Level Quality Indicators

| Aspect | Standard |
|--------|----------|
| Typography | Perfect hierarchy, excellent readability |
| Spacing | Pixel-perfect consistency |
| Colors | Subtle, cohesive palette |
| Animations | Smooth, purposeful, not distracting |
| Interactions | Immediate feedback, delightful |
| Polish | No rough edges, every detail considered |

### Red Flags to Fix

- Inconsistent spacing between similar elements
- Different border radii in the same context
- Misaligned text or icons
- Jarring color transitions
- Slow or missing hover states
- Confusing navigation
- Missing loading states
- Text contrast issues
