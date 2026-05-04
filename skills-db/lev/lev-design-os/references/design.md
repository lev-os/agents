# Design Phase

This phase establishes the visual identity and application structure.

---

## Design Tokens

**Command:** `/design-tokens`
**Output:** `product/design-system/colors.json`, `product/design-system/typography.json`

### Process

1. **Check Prerequisites** - Verify `product-overview.md` exists
2. **Explain Process** - Colors and typography for consistent design
3. **Choose Colors** - Help user select from Tailwind palette:
   - **Primary** - Main accent (buttons, links)
   - **Secondary** - Complementary accent (tags, highlights)
   - **Neutral** - Backgrounds, text, borders
4. **Choose Typography** - Help user select Google Fonts:
   - **Heading** - Titles, section headers
   - **Body** - Paragraphs, UI text
   - **Mono** - Code, technical content
5. **Create Files** - Write JSON config

### Tailwind Color Options
- **Warm:** red, orange, amber, yellow, lime
- **Cool:** green, emerald, teal, cyan, sky, blue
- **Purple:** indigo, violet, purple, fuchsia, pink, rose
- **Neutral:** slate, gray, zinc, neutral, stone

### Popular Font Pairings
- **Modern & Clean:** DM Sans + IBM Plex Mono
- **Professional:** Inter + JetBrains Mono
- **Friendly:** Nunito Sans + Fira Code
- **Bold & Modern:** Space Grotesk + Source Code Pro
- **Tech-forward:** JetBrains Mono + Inter

### Output Format

**colors.json:**
```json
{
  "primary": "lime",
  "secondary": "emerald",
  "neutral": "stone"
}
```

**typography.json:**
```json
{
  "heading": "DM Sans",
  "body": "DM Sans",
  "mono": "IBM Plex Mono"
}
```

---

## Design Shell

**Command:** `/design-shell`
**Output:** `product/shell/spec.md`, `src/shell/components/`

### Process

1. **Check Prerequisites** - Verify overview and roadmap exist
2. **Analyze Structure** - Review sections for navigation
3. **Choose Layout Pattern:**
   - **A. Sidebar Navigation** - Vertical nav left, content right (dashboards, admin)
   - **B. Top Navigation** - Horizontal nav top, content below (simpler apps)
   - **C. Minimal Header** - Logo + user menu only (wizard flows)
4. **Gather Details** - Ask about:
   - User menu placement
   - Mobile behavior (collapsible, hamburger)
   - Additional nav items (Settings, Help)
   - Default view on app load
5. **Create Spec & Components**

### Components Created

```
src/shell/components/
├── AppShell.tsx      # Main wrapper, accepts children + navigationItems + user
├── MainNav.tsx       # Navigation component (sidebar or top)
├── UserMenu.tsx      # Avatar + dropdown
└── index.ts          # Exports
```

### Component Requirements
- Props-based (portable)
- Apply design tokens if defined
- Support light/dark mode with `dark:` variants
- Mobile responsive
- Use Tailwind CSS
- Use lucide-react for icons

### Shell Preview
```tsx
// src/shell/ShellPreview.tsx
export default function ShellPreview() {
  return (
    <AppShell
      navigationItems={[...]}
      user={{ name: 'Alex Morgan' }}
      onNavigate={(href) => console.log('Navigate:', href)}
      onLogout={() => console.log('Logout')}
    >
      <div>Content Area</div>
    </AppShell>
  )
}
```

---

## Design Screen

**Command:** `/design-screen`
**Output:** `src/sections/[section-id]/components/`, preview wrapper

### Prerequisites
- `product/sections/[section-id]/spec.md` (run `/shape-section`)
- `product/sections/[section-id]/data.json` (run `/sample-data`)
- `product/sections/[section-id]/types.ts` (run `/sample-data`)

### Process

1. **Select Section** - Which section to design
2. **Check Design Tokens** - Apply if defined
3. **Analyze Requirements** - Read spec, data, types
4. **Identify Views** - List, detail, form views needed
5. **Create Props-Based Component**

### Component Structure

```tsx
import type { InvoiceListProps } from '@/../product/sections/invoices/types'

export function InvoiceList({
  invoices,
  onView,
  onEdit,
  onDelete,
  onCreate
}: InvoiceListProps) {
  return (
    <div className="max-w-4xl mx-auto">
      {invoices.map(invoice => (
        <div key={invoice.id}>
          <span>{invoice.clientName}</span>
          <button onClick={() => onView?.(invoice.id)}>View</button>
        </div>
      ))}
    </div>
  )
}
```

### Design Requirements
- **Mobile responsive** - Use `sm:`, `md:`, `lg:` prefixes
- **Light & dark mode** - Use `dark:` variants
- **Props-based** - Data via props, never import data.json
- **Callbacks optional** - Use `onClick={() => onDelete?.(id)}`

### Preview Wrapper
```tsx
// src/sections/invoices/InvoiceList.tsx (preview)
import data from '@/../product/sections/invoices/data.json'
import { InvoiceList } from './components/InvoiceList'

export default function InvoiceListPreview() {
  return (
    <InvoiceList
      invoices={data.invoices}
      onView={(id) => console.log('View:', id)}
    />
  )
}
```

---

## Next Phase

After completing Design, proceed to **Sections** (`references/sections.md`):
- Shape each section's specification
- Generate sample data and types
- Create screen designs
