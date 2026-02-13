# AgentPing Web UI - Design System and ADA Standards

> Comprehensive reference for design tokens, accessibility requirements, and component development standards.
> Generated from codebase analysis: 136 components, 48 with ARIA coverage (35%), Cyber-Premium theme active.

---

## Table of Contents

1. [Design Token Reference](#1-design-token-reference)
2. [ADA Compliance Checklist](#2-ada-compliance-checklist)
3. [React Component Standards](#3-react-component-standards)
4. [Tailwind CSS Standards](#4-tailwind-css-standards)
5. [Storybook Story Standards](#5-storybook-story-standards)
6. [Component Variant Patterns](#6-component-variant-patterns)
7. [Do/Don't Guidelines](#7-dodont-guidelines)

---

## 1. Design Token Reference

### 1.1 Color Palette - Cyber-Premium Theme (Dark Mode)

#### Background Colors

| Token | CSS Variable | Hex Value | Usage |
|-------|-------------|-----------|-------|
| Primary BG | `--bg-primary` | `#050505` | Deepest black, page background |
| Secondary BG | `--bg-secondary` | `#0a0a0a` | Panels, sidebars |
| Tertiary BG | `--bg-tertiary` | `#121212` | Card backgrounds |
| Hover BG | `--bg-hover` | `#1a1a1a` | Hover states |
| Elevated BG | `--bg-elevated` | `#202020` | Modals, popovers, dropdowns |

#### Text Colors

| Token | CSS Variable | Hex Value | Usage |
|-------|-------------|-----------|-------|
| Primary Text | `--text-primary` | `#ededed` | Headings, primary content |
| Secondary Text | `--text-secondary` | `#a1a1aa` | Body text, descriptions |
| Muted Text | `--text-muted` | `#52525b` | Placeholders, disabled, hints |
| Text Glow | `--text-glow` | `rgba(237, 237, 237, 0.5)` | Neon text effects |

#### Accent Colors (Neon)

| Token | CSS Variable | Hex Value | Usage |
|-------|-------------|-----------|-------|
| Primary Accent | `--accent-primary` | `#00e5ff` | Cyan neon - links, focus, CTAs |
| Primary Dim | `--accent-primary-dim` | `rgba(0, 229, 255, 0.1)` | Backgrounds, subtle highlights |
| Success | `--accent-success` | `#00ff9d` | Green neon - success states |
| Success Dim | `--accent-success-dim` | `rgba(0, 255, 157, 0.1)` | Success backgrounds |
| Warning | `--accent-warning` | `#ffb800` | Amber neon - warnings |
| Warning Dim | `--accent-warning-dim` | `rgba(255, 184, 0, 0.1)` | Warning backgrounds |
| Danger/Error | `--accent-danger` | `#ff2a6d` | Pink/red neon - errors, destructive |
| Danger Dim | `--accent-danger-dim` | `rgba(255, 42, 109, 0.1)` | Error backgrounds |

#### Border & Glass Effects

| Token | CSS Variable | Value | Usage |
|-------|-------------|-------|-------|
| Border Color | `--border-color` | `rgba(255, 255, 255, 0.08)` | Default borders |
| Border Hover | `--border-hover` | `rgba(255, 255, 255, 0.15)` | Hover border states |
| Border Neon | `--border-neon` | `var(--accent-primary)` | Focused/active borders |
| Glass BG | `--glass-bg` | `rgba(10, 10, 10, 0.7)` | Glassmorphism panels |
| Glass Border | `--glass-border` | `rgba(255, 255, 255, 0.08)` | Glass effect borders |
| Glass Shadow | `--glass-shadow` | `0 8px 32px 0 rgba(0, 0, 0, 0.37)` | Glass panel shadows |

#### Glow Effects

```css
--accent-primary-glow: 0 0 10px rgba(0, 229, 255, 0.4), 0 0 20px rgba(0, 229, 255, 0.2);
```

### 1.2 Typography Scale

#### Font Families

| Token | CSS Variable | Value |
|-------|-------------|-------|
| Sans | `--font-sans` | `'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` |
| Mono | `--font-mono` | `'JetBrains Mono', 'Fira Code', Consolas, monospace` |

#### Font Sizes (Existing Pattern)

| Size | Value | Usage |
|------|-------|-------|
| xs | `11px` | Badges, labels, kbd |
| sm | `12px` | Small hints, metadata |
| base | `14px` | Body text (default) |
| md | `15px` | Slightly larger body |
| lg | `16px` | Input text (iOS zoom prevention) |
| xl | `18px` | H3, subheadings |
| 2xl | `24px` | H2, section titles |
| 3xl | `28px` | H1, page titles |

#### Font Weights

| Weight | Value | Usage |
|--------|-------|-------|
| Regular | `400` | Body text |
| Medium | `500` | Buttons, nav items |
| Semibold | `600` | Headings, emphasis |
| Bold | `700` | Strong emphasis, badges |

#### Line Heights

| Token | Value | Usage |
|-------|-------|-------|
| Tight | `1.2` | Headings |
| Normal | `1.5` | Body text (default) |
| Relaxed | `1.6` | Readable paragraphs |

#### Text Wrap Standards

```css
h1, h2, h3, h4, h5, h6 { text-wrap: balance; }
p, li { text-wrap: pretty; }
```

### 1.3 Spacing Scale (RAMS - Recommended)

| Token | Value | CSS Usage |
|-------|-------|-----------|
| 1 | `4px` | Tight gaps, icon margins |
| 2 | `8px` | Default gap, small padding |
| 3 | `12px` | Medium gap, button padding |
| 4 | `16px` | Section gaps, card padding |
| 5 | `20px` | Checkbox hit area |
| 6 | `24px` | Large gaps, modal padding |
| 8 | `32px` | Section margins |
| 10 | `40px` | Major section spacing |
| 12 | `48px` | Page margins |

**Note:** Current codebase uses hardcoded px values. Tailwind integration will standardize to spacing scale.

### 1.4 Border Radius

| Token | CSS Variable | Value | Usage |
|-------|-------------|-------|-------|
| XS | `--radius-xs` | `2px` | Tight radii, subtle rounding |
| SM | `--radius-sm` | `4px` | Buttons, small inputs |
| MD | `--radius-md` | `6px` | Default components |
| LG | `--radius-lg` | `8px` | Cards, panels |
| XL | `--radius-xl` | `12px` | Large modals, dialogs |
| Round | `--radius-round` | `9999px` | Pills, badges, avatars |

### 1.5 Shadows

| Token | CSS Variable | Value | Usage |
|-------|-------------|-------|-------|
| SM | `--shadow-sm` | `0 2px 4px rgba(0, 0, 0, 0.5)` | Subtle elevation |
| MD | `--shadow-md` | `0 4px 8px rgba(0, 0, 0, 0.6)` | Cards, buttons |
| LG | `--shadow-lg` | `0 8px 16px rgba(0, 0, 0, 0.7)` | Modals, popovers |

### 1.6 Z-Index Hierarchy

| Layer | CSS Variable | Value | Usage |
|-------|-------------|-------|-------|
| Base | `--z-base` | `0` | Normal flow |
| Dropdown | `--z-dropdown` | `100` | Dropdowns, select menus |
| Sticky | `--z-sticky` | `200` | Sticky headers, navs |
| Fixed | `--z-fixed` | `300` | Fixed elements |
| Modal Backdrop | `--z-modal-backdrop` | `400` | Overlay behind modals |
| Modal | `--z-modal` | `500` | Modal dialogs |
| Tooltip | `--z-tooltip` | `600` | Tooltips, popovers |

**Pattern:** Increment by 100 for major layers; use +1, +2 for sublayers within.

### 1.7 Animation & Transition Standards

#### Transition Guidelines (Vercel)

```css
/* CORRECT - Explicit properties */
transition: background-color 0.15s ease, border-color 0.15s ease, opacity 0.15s ease;
transition: transform 0.2s ease-out, opacity 0.2s ease-out;

/* INCORRECT - Never use */
transition: all 0.3s ease; /* Avoid */
```

#### Easing Functions

| Name | Value | Usage |
|------|-------|-------|
| Ease | `ease` | General transitions |
| Ease Out | `ease-out` | Enter animations |
| Ease In | `ease-in` | Exit animations |
| Smooth Out | `cubic-bezier(0.16, 1, 0.3, 1)` | Premium feel animations |
| Spring | `cubic-bezier(0.4, 0, 0.2, 1)` | Progress bars, sliders |

#### Standard Keyframes

```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes modal-pop {
  0% { opacity: 0; transform: scale(0.95); }
  100% { opacity: 1; transform: scale(1); }
}

@keyframes progress-slide {
  0% { background-position: 0 0; }
  100% { background-position: 20px 0; }
}
```

#### Reduced Motion Support (REQUIRED)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 2. ADA Compliance Checklist

### 2.1 Universal Requirements (All Components)

#### Color Contrast (WCAG 2.1 AA)

- [ ] **Normal text (< 18px):** Minimum 4.5:1 contrast ratio
- [ ] **Large text (>= 18px bold or >= 24px):** Minimum 3:1 contrast ratio
- [ ] **Interactive elements:** Minimum 3:1 against adjacent colors
- [ ] **Focus indicators:** 3:1 against background

**Current Theme Validation:**

| Combination | Ratio | Status |
|-------------|-------|--------|
| `#ededed` on `#050505` | 17.3:1 | PASS |
| `#a1a1aa` on `#050505` | 8.1:1 | PASS |
| `#52525b` on `#050505` | 3.5:1 | WARNING - Border |
| `#00e5ff` on `#050505` | 11.5:1 | PASS |
| `#ff2a6d` on `#050505` | 5.2:1 | PASS |
| `#ffb800` on `#050505` | 11.8:1 | PASS |
| `#00ff9d` on `#050505` | 14.4:1 | PASS |

#### Focus Indicators

```css
/* REQUIRED: All focusable elements */
:focus-visible {
  outline: 2px solid var(--accent-primary);
  outline-offset: 2px;
}

/* Remove outline on click, show on keyboard */
:focus { outline: none; }
```

#### Touch Targets

- [ ] **Minimum 44x44px** for mobile interactive elements
- [ ] **Minimum 24x24px** for desktop (32px recommended)
- [ ] `touch-action: manipulation;` on buttons (prevents double-tap zoom)

### 2.2 Component-Specific Checklists

#### Buttons

```tsx
// Required attributes
<button
  type="button" // or "submit"
  aria-label="Descriptive action" // if icon-only
  aria-disabled={isDisabled} // for custom disabled states
  aria-pressed={isToggle} // for toggle buttons
  disabled={isDisabled}
>
```

- [ ] Semantic `<button>` element (not div/span with onClick)
- [ ] `type="button"` for non-submit buttons
- [ ] `aria-label` for icon-only buttons
- [ ] `:disabled` styling distinct from normal state
- [ ] Focus visible on keyboard navigation
- [ ] Keyboard: Enter/Space to activate

#### Form Inputs

```tsx
<div className="form-field">
  <label htmlFor={id}>{label}</label>
  <input
    id={id}
    type="text"
    aria-describedby={hasError ? `${id}-error` : undefined}
    aria-invalid={hasError}
    aria-required={required}
  />
  {hasError && <span id={`${id}-error`} role="alert">{errorMessage}</span>}
</div>
```

- [ ] Associated `<label>` with matching `htmlFor`/`id`
- [ ] `aria-invalid="true"` for error states
- [ ] `aria-describedby` linking to error messages
- [ ] `aria-required="true"` for required fields
- [ ] Error messages use `role="alert"` for screen readers
- [ ] `font-size: 16px` minimum (prevents iOS auto-zoom)
- [ ] Never block paste (`onPaste` handlers forbidden)

#### Modals/Dialogs

```tsx
<div
  role="dialog" // or "alertdialog" for confirmations
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-description"
  tabIndex={-1} // for focus trap
>
  <h2 id="modal-title">Title</h2>
  <p id="modal-description">Description</p>
</div>
```

- [ ] `role="dialog"` or `role="alertdialog"`
- [ ] `aria-modal="true"`
- [ ] `aria-labelledby` pointing to title
- [ ] Focus trap: Tab cycles within modal
- [ ] Focus first focusable element on open
- [ ] Escape key closes modal
- [ ] `document.body.style.overflow = 'hidden'` when open
- [ ] Return focus to trigger element on close

#### Data Tables

```tsx
<table role="grid" aria-label="Data Table">
  <thead>
    <tr role="row">
      <th
        role="columnheader"
        aria-sort="ascending" // or "descending" | "none"
        scope="col"
      >
        Column Header
      </th>
    </tr>
  </thead>
  <tbody>
    <tr role="row" tabIndex={isClickable ? 0 : -1}>
      <td role="gridcell">Cell</td>
    </tr>
  </tbody>
</table>
```

- [ ] `role="grid"` on table container
- [ ] `aria-sort` on sortable columns
- [ ] `tabIndex={0}` on clickable rows
- [ ] Keyboard: Arrow keys for cell navigation
- [ ] Empty state: `colspan` with message

#### Progress Indicators

```tsx
<div
  role="progressbar"
  aria-valuenow={50}
  aria-valuemin={0}
  aria-valuemax={100}
  aria-label="Loading progress"
>
```

- [ ] `role="progressbar"`
- [ ] `aria-valuenow`, `aria-valuemin`, `aria-valuemax`
- [ ] `aria-label` describing what's loading
- [ ] For indeterminate: omit `aria-valuenow`

#### Navigation/Breadcrumbs

```tsx
<nav aria-label="Breadcrumb">
  <ol>
    <li>
      <a href="/" aria-current={isLast ? "page" : undefined}>Home</a>
    </li>
  </ol>
</nav>
```

- [ ] `<nav>` with `aria-label`
- [ ] `aria-current="page"` on current page
- [ ] Keyboard navigable links/buttons
- [ ] Separators have `aria-hidden="true"`

#### Accordions

```tsx
<button
  aria-expanded={isOpen}
  aria-controls={`panel-${id}`}
  id={`button-${id}`}
>
  Title
</button>
<div
  id={`panel-${id}`}
  role="region"
  aria-labelledby={`button-${id}`}
  hidden={!isOpen}
>
  Content
</div>
```

- [ ] `aria-expanded` on trigger button
- [ ] `aria-controls` linking button to panel
- [ ] Panel has `role="region"` and `aria-labelledby`
- [ ] Use `hidden` attribute, not CSS `display: none`

#### Toasts/Alerts

```tsx
<div
  role="alert"
  aria-live={isError ? "assertive" : "polite"}
>
  {message}
</div>
```

- [ ] `role="alert"` or `role="status"`
- [ ] `aria-live="polite"` for info, `assertive` for errors
- [ ] Auto-dismiss with adequate time (5-10s minimum)
- [ ] Dismiss button with `aria-label="Close notification"`

#### Sliders

```tsx
<input
  type="range"
  id={id}
  min={min}
  max={max}
  value={value}
  aria-label={label}
  aria-valuetext={`${value} ${unit}`}
/>
```

- [ ] Native `<input type="range">` preferred
- [ ] `aria-valuetext` for non-numeric values
- [ ] Keyboard: Arrow keys adjust value

### 2.3 Keyboard Navigation Patterns

| Key | Action |
|-----|--------|
| Tab | Move to next focusable element |
| Shift+Tab | Move to previous focusable element |
| Enter | Activate buttons, submit forms |
| Space | Toggle checkboxes, activate buttons |
| Escape | Close modals, cancel actions |
| Arrow Keys | Navigate within widgets (tabs, menus, grids) |
| Home/End | Jump to first/last item in lists |

### 2.4 Screen Reader Testing Checklist

- [ ] All images have alt text (or `alt=""` for decorative)
- [ ] Icons are `aria-hidden="true"` when decorative
- [ ] Form fields have visible labels
- [ ] Error messages are announced on appearance
- [ ] Dynamic content changes are announced
- [ ] Page title updates on navigation
- [ ] Heading hierarchy is logical (h1 > h2 > h3)

---

## 3. React Component Standards

### 3.1 File Structure

```
src/
  components/
    ComponentName/
      ComponentName.tsx       # Main component
      ComponentName.css       # Styles (until Tailwind migration)
      ComponentName.stories.tsx  # Storybook (future)
      ComponentName.test.tsx  # Tests (future)
      index.ts                # Re-export
```

**Current Pattern (Flat):**
```
src/
  components/
    ComponentName.tsx
    ComponentName.css
```

### 3.2 Props Interface Pattern

```tsx
// Named export for interface
export interface ComponentNameProps {
  /** Required props first */
  id: string;
  value: string;
  onChange: (value: string) => void;

  /** Optional props after, with defaults documented */
  variant?: 'default' | 'primary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  className?: string;

  /** Children last if applicable */
  children?: React.ReactNode;
}
```

### 3.3 Component Declaration Pattern

```tsx
import { useState, useCallback } from 'react';
import './ComponentName.css';

export interface ComponentNameProps {
  // ... props interface
}

export function ComponentName({
  id,
  value,
  onChange,
  variant = 'default',
  size = 'md',
  disabled = false,
  className = '',
}: ComponentNameProps) {
  // Internal state
  const [isOpen, setIsOpen] = useState(false);

  // Memoized callbacks
  const handleClick = useCallback(() => {
    if (!disabled) {
      setIsOpen(prev => !prev);
    }
  }, [disabled]);

  // Render
  return (
    <div
      className={`component-name component-name--${variant} component-name--${size} ${className}`}
      data-testid="component-name"
    >
      {/* ... */}
    </div>
  );
}
```

### 3.4 forwardRef Pattern (When Needed)

```tsx
import { forwardRef } from 'react';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className = '', ...props }, ref) => {
    return (
      <div className={`input-wrapper ${className}`}>
        {label && <label htmlFor={props.id}>{label}</label>}
        <input
          ref={ref}
          aria-invalid={!!error}
          {...props}
        />
        {error && <span role="alert">{error}</span>}
      </div>
    );
  }
);

Input.displayName = 'Input';
```

### 3.5 Export Pattern

```tsx
// Default export for components
export function Badge(props: BadgeProps) { /* ... */ }

// Named export for types
export type { BadgeProps };

// Or in index.ts:
export { Badge } from './Badge';
export type { BadgeProps } from './Badge';
```

### 3.6 Error Boundary Pattern

```tsx
import { Component, ErrorInfo, ReactNode } from 'react';

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.props.onError?.(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <div role="alert" className="error-boundary">
          <h2>Something went wrong</h2>
          <details>
            <summary>Error details</summary>
            <pre>{this.state.error?.message}</pre>
          </details>
        </div>
      );
    }
    return this.props.children;
  }
}
```

---

## 4. Tailwind CSS Standards

### 4.1 Utility-First Approach

```tsx
// CORRECT: Utility classes
<button className="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90 focus-visible:ring-2">

// AVOID: Custom CSS classes (only when necessary)
<button className="btn-primary">
```

### 4.2 Custom Property Integration

**tailwind.config.ts:**
```ts
export default {
  theme: {
    extend: {
      colors: {
        'bg-primary': 'var(--bg-primary)',
        'bg-secondary': 'var(--bg-secondary)',
        'bg-tertiary': 'var(--bg-tertiary)',
        'bg-hover': 'var(--bg-hover)',
        'bg-elevated': 'var(--bg-elevated)',
        'text-primary': 'var(--text-primary)',
        'text-secondary': 'var(--text-secondary)',
        'text-muted': 'var(--text-muted)',
        primary: 'var(--accent-primary)',
        success: 'var(--accent-success)',
        warning: 'var(--accent-warning)',
        danger: 'var(--accent-danger)',
        'border-default': 'var(--border-color)',
        'border-hover': 'var(--border-hover)',
      },
      borderRadius: {
        xs: 'var(--radius-xs)',
        sm: 'var(--radius-sm)',
        md: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
        xl: 'var(--radius-xl)',
      },
      fontFamily: {
        sans: 'var(--font-sans)',
        mono: 'var(--font-mono)',
      },
      boxShadow: {
        sm: 'var(--shadow-sm)',
        md: 'var(--shadow-md)',
        lg: 'var(--shadow-lg)',
        glass: 'var(--glass-shadow)',
      },
      zIndex: {
        dropdown: 'var(--z-dropdown)',
        sticky: 'var(--z-sticky)',
        fixed: 'var(--z-fixed)',
        'modal-backdrop': 'var(--z-modal-backdrop)',
        modal: 'var(--z-modal)',
        tooltip: 'var(--z-tooltip)',
      },
    },
  },
}
```

### 4.3 Responsive Prefixes (Mobile-First)

| Breakpoint | Min Width | Prefix |
|------------|-----------|--------|
| Default | 0px | (none) |
| sm | 640px | `sm:` |
| md | 768px | `md:` |
| lg | 1024px | `lg:` |
| xl | 1280px | `xl:` |
| 2xl | 1536px | `2xl:` |

```tsx
<div className="px-4 md:px-6 lg:px-8">
  <h1 className="text-xl md:text-2xl lg:text-3xl">
    Responsive Heading
  </h1>
</div>
```

### 4.4 Conditional Classes with clsx/tailwind-merge

```tsx
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

// Helper function
function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Usage
<button
  className={cn(
    // Base styles
    'px-4 py-2 rounded-md font-medium transition-colors',
    // Variant
    variant === 'primary' && 'bg-primary text-white hover:bg-primary/90',
    variant === 'secondary' && 'bg-bg-tertiary text-text-primary border border-border-default',
    variant === 'danger' && 'bg-danger text-white hover:bg-danger/90',
    // State
    disabled && 'opacity-50 cursor-not-allowed',
    // Custom
    className
  )}
>
```

### 4.5 Avoiding Inline Styles

```tsx
// AVOID
<div style={{ marginTop: 16, padding: 8 }}>

// PREFER
<div className="mt-4 p-2">

// Exception: Dynamic CSS custom properties
<div
  className="progress-fill"
  style={{ '--progress-color': color } as React.CSSProperties}
>
```

---

## 5. Storybook Story Standards

### 5.1 Story File Naming

```
ComponentName.stories.tsx
```

### 5.2 Meta Configuration Template

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { ComponentName } from './ComponentName';

const meta: Meta<typeof ComponentName> = {
  title: 'Components/Category/ComponentName',
  component: ComponentName,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered', // or 'fullscreen' | 'padded'
    docs: {
      description: {
        component: 'Brief description of the component and its purpose.',
      },
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'primary', 'danger'],
      description: 'Visual style variant',
    },
    size: {
      control: 'radio',
      options: ['sm', 'md', 'lg'],
    },
    disabled: {
      control: 'boolean',
    },
    onClick: { action: 'clicked' },
  },
  args: {
    // Default args
    variant: 'default',
    size: 'md',
    disabled: false,
  },
};

export default meta;
type Story = StoryObj<typeof ComponentName>;
```

### 5.3 Required Story Variants

#### Default

```tsx
export const Default: Story = {
  args: {
    children: 'Default Button',
  },
};
```

#### Responsive Variants

```tsx
export const Mobile: Story = {
  parameters: {
    viewport: { defaultViewport: 'mobile1' },
  },
  args: { /* ... */ },
};

export const Tablet: Story = {
  parameters: {
    viewport: { defaultViewport: 'tablet' },
  },
  args: { /* ... */ },
};

export const Desktop: Story = {
  parameters: {
    viewport: { defaultViewport: 'desktop' },
  },
  args: { /* ... */ },
};
```

#### State Variants

```tsx
export const Loading: Story = {
  args: {
    isLoading: true,
  },
};

export const Error: Story = {
  args: {
    error: 'Something went wrong',
  },
};

export const Empty: Story = {
  args: {
    items: [],
  },
};

export const Disabled: Story = {
  args: {
    disabled: true,
  },
};
```

### 5.4 ADA Testing with Play Functions

```tsx
import { within, userEvent, expect } from '@storybook/test';

export const AccessibilityTest: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Tab navigation
    await userEvent.tab();
    const button = canvas.getByRole('button');
    expect(button).toHaveFocus();

    // Keyboard activation
    await userEvent.keyboard('{Enter}');

    // Escape to close
    await userEvent.keyboard('{Escape}');

    // Check ARIA attributes
    expect(button).toHaveAttribute('aria-expanded', 'false');
  },
};

export const KeyboardNavigation: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Tab through all focusable elements
    const focusableElements = canvas.getAllByRole('button');
    for (const element of focusableElements) {
      await userEvent.tab();
      expect(document.activeElement).toBe(element);
    }
  },
};
```

### 5.5 Documentation with Autodocs

```tsx
const meta: Meta<typeof ComponentName> = {
  // ...
  parameters: {
    docs: {
      description: {
        component: `
## Overview

ComponentName provides...

## Accessibility

- Full keyboard navigation
- Screen reader support
- Focus management

## Usage

\`\`\`tsx
<ComponentName variant="primary" onClick={handleClick}>
  Label
</ComponentName>
\`\`\`
        `,
      },
    },
  },
};
```

---

## 6. Component Variant Patterns

### 6.1 Size Variants

```tsx
type Size = 'sm' | 'md' | 'lg';

const sizeClasses: Record<Size, string> = {
  sm: 'px-2 py-1 text-xs',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-3 text-base',
};

// Height standards
const sizeHeights: Record<Size, string> = {
  sm: 'h-7',    // 28px
  md: 'h-9',    // 36px
  lg: 'h-11',   // 44px (touch target)
};
```

### 6.2 Color/Intent Variants

```tsx
type Variant = 'default' | 'primary' | 'secondary' | 'danger' | 'success' | 'warning';

const variantClasses: Record<Variant, string> = {
  default: 'bg-bg-tertiary text-text-primary border-border-default',
  primary: 'bg-primary text-white hover:bg-primary/90',
  secondary: 'bg-transparent text-text-secondary border border-border-default hover:bg-bg-hover',
  danger: 'bg-danger text-white hover:bg-danger/90',
  success: 'bg-success text-black hover:bg-success/90',
  warning: 'bg-warning text-black hover:bg-warning/90',
};
```

### 6.3 Discriminated Union Props

```tsx
// Base props
interface BaseButtonProps {
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  className?: string;
}

// Button variant
interface NormalButtonProps extends BaseButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  href?: never;
  onClick?: () => void;
}

// Link variant
interface LinkButtonProps extends BaseButtonProps {
  variant?: 'link';
  href: string;
  onClick?: never;
}

// Union type
type ButtonProps = NormalButtonProps | LinkButtonProps;

// Usage
function Button(props: ButtonProps) {
  if (props.variant === 'link') {
    return <a href={props.href} className={/* ... */}>{/* ... */}</a>;
  }
  return <button onClick={props.onClick} className={/* ... */}>{/* ... */}</button>;
}
```

### 6.4 Controlled vs Uncontrolled Patterns

```tsx
interface ControlledInputProps {
  value: string;
  onChange: (value: string) => void;
  defaultValue?: never;
}

interface UncontrolledInputProps {
  value?: never;
  onChange?: (value: string) => void;
  defaultValue?: string;
}

type InputProps = (ControlledInputProps | UncontrolledInputProps) & {
  id: string;
  label?: string;
};

function Input({ value, defaultValue, onChange, id, label }: InputProps) {
  const [internalValue, setInternalValue] = useState(defaultValue ?? '');

  const isControlled = value !== undefined;
  const currentValue = isControlled ? value : internalValue;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    if (!isControlled) {
      setInternalValue(newValue);
    }
    onChange?.(newValue);
  };

  return (
    <input
      id={id}
      value={currentValue}
      onChange={handleChange}
      aria-label={label}
    />
  );
}
```

---

## 7. Do/Don't Guidelines

### 7.1 Semantic HTML

| Do | Don't |
|----|-------|
| `<button>` for actions | `<div onClick>` for buttons |
| `<a href>` for navigation | `<button>` for links |
| `<input type="checkbox">` | Custom div checkboxes |
| `<nav>` for navigation | `<div class="nav">` |
| `<main>`, `<article>`, `<section>` | Divs everywhere |
| `<table>` for tabular data | Divs with flexbox for tables |

### 7.2 Icon Button Accessibility

```tsx
// DO
<button aria-label="Close dialog">
  <XIcon aria-hidden="true" />
</button>

// DON'T
<button>
  <XIcon />
</button>
```

### 7.3 Form Labeling

```tsx
// DO - Visible label
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// DO - Hidden label (when design requires)
<label htmlFor="search" className="sr-only">Search</label>
<input id="search" type="search" placeholder="Search..." />

// DON'T - No label
<input type="email" placeholder="Email" />
```

### 7.4 Loading States

```tsx
// DO
<button disabled={isLoading} aria-busy={isLoading}>
  {isLoading ? <Spinner aria-hidden="true" /> : null}
  {isLoading ? 'Saving...' : 'Save'}
</button>

// DON'T
<button>
  {isLoading ? <Spinner /> : 'Save'}
</button>
```

### 7.5 Error Handling

```tsx
// DO
<input
  aria-invalid={!!error}
  aria-describedby={error ? 'email-error' : undefined}
/>
{error && (
  <span id="email-error" role="alert" className="text-danger">
    {error}
  </span>
)}

// DON'T
<input />
{error && <span className="error">{error}</span>}
```

### 7.6 Animation Usage

```tsx
// DO - Compositor-friendly
const style = {
  transform: `translateX(${offset}px)`,
  opacity: isVisible ? 1 : 0,
};

// DON'T - Layout-triggering
const style = {
  left: `${offset}px`,
  visibility: isVisible ? 'visible' : 'hidden',
};
```

### 7.7 Color-Only Information

```tsx
// DO - Color + icon + text
<Badge variant="error">
  <XIcon aria-hidden="true" /> Error
</Badge>

// DON'T - Color only
<Badge variant="error" />
```

### 7.8 Focus Management

```tsx
// DO - Return focus after modal close
const triggerRef = useRef<HTMLButtonElement>(null);

const handleClose = () => {
  setIsOpen(false);
  triggerRef.current?.focus();
};

// DON'T - Lose focus on close
const handleClose = () => {
  setIsOpen(false);
};
```

### 7.9 Dynamic Content

```tsx
// DO - Announce updates
<div aria-live="polite" aria-atomic="true">
  {message}
</div>

// DON'T - Silent updates
<div>{message}</div>
```

### 7.10 Images and Media

```tsx
// DO - Meaningful alt text
<img src={chart} alt="Sales increased 25% in Q4 2024" />

// DO - Decorative image
<img src={decoration} alt="" aria-hidden="true" />

// DON'T - Generic alt
<img src={chart} alt="Chart" />
```

---

## Appendix A: Quick Reference Cards

### Component Audit Template

```markdown
## [ComponentName]

### Current State
- [ ] ARIA attributes present
- [ ] Keyboard navigable
- [ ] Focus visible
- [ ] Color contrast compliant
- [ ] Touch targets adequate
- [ ] Reduced motion supported

### Required Updates
- [ ] Add role="..."
- [ ] Add aria-label="..."
- [ ] Add keyboard handlers
- [ ] Update focus styles
- [ ] Add Storybook story
```

### Storybook Story Checklist

- [ ] Meta with autodocs
- [ ] Default story
- [ ] All variant stories
- [ ] Mobile/Tablet/Desktop viewports
- [ ] Loading state
- [ ] Error state
- [ ] Empty state
- [ ] Disabled state
- [ ] Keyboard navigation play test
- [ ] Screen reader play test

---

## Appendix B: Theme Extension Roadmap

### Light Mode Variables

```css
:root[data-theme="light"] {
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --bg-tertiary: #f3f4f6;
  --bg-hover: #e5e7eb;
  --bg-elevated: #ffffff;

  --text-primary: #111827;
  --text-secondary: #4b5563;
  --text-muted: #9ca3af;

  --border-color: rgba(0, 0, 0, 0.1);
  --border-hover: rgba(0, 0, 0, 0.15);
}
```

### Additional Themes

1. **High Contrast** - Maximum AA compliance
2. **Solarized Dark** - Developer-friendly
3. **Minimal** - Reduced visual noise

---

*Document Version: 1.0*
*Generated: 2026-01-18*
*Source: AgentPing Web UI Analysis*
