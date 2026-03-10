# Sections Phase

This phase defines each feature area with specifications, data, and screen designs.

---

## Shape Section

**Command:** `/shape-section`
**Output:** `product/sections/[section-id]/spec.md`

### Process

1. **Check Prerequisites** - Verify `product-roadmap.md` exists
2. **Select Section** - Auto-select if one, otherwise ask user
3. **Gather Input** - Invite user to share thoughts about the section
4. **Ask Clarifying Questions** (4-6):
   - Main user actions/tasks
   - Information to display
   - Key user flows (step-by-step)
   - UI patterns (tables, cards, modals)
   - Scope boundaries (what's excluded)
5. **Ask Shell Configuration** - Inside app shell or standalone?
6. **Draft & Refine** - Present spec, iterate
7. **Create File**

### Output Format

```markdown
# [Section Title] Specification

## Overview
[2-3 sentence description]

## User Flows
- [Flow 1: User can...]
- [Flow 2: User can...]
- [Flow 3: User can...]

## UI Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

## Configuration
- shell: true
```

### Key Notes
- Focus on UX/UI - no backend/database details
- Keep concise - only include what was discussed
- `shell: true` = inside app shell (default)
- `shell: false` = standalone page

---

## Sample Data

**Command:** `/sample-data`
**Output:** `product/sections/[section-id]/data.json`, `types.ts`

### Process

1. **Check Prerequisites** - Verify spec exists for section
2. **Check Global Data Model** - Use entity names if defined
3. **Analyze Specification** - Identify implied entities and fields
4. **Present Structure** - Explain data organization in plain language
5. **Generate Files** - Create data.json and types.ts

### data.json Structure

```json
{
  "_meta": {
    "models": {
      "invoices": "Each invoice represents a bill sent to a client.",
      "lineItems": "Individual charges listed on each invoice."
    },
    "relationships": [
      "Each Invoice contains one or more Line Items",
      "Invoices track which Client they belong to"
    ]
  },
  "invoices": [
    {
      "id": "inv-001",
      "invoiceNumber": "INV-2024-001",
      "clientName": "Acme Corp",
      "total": 1500.00,
      "status": "sent",
      "lineItems": [...]
    }
  ]
}
```

### types.ts Structure

```typescript
// Data Types
export interface LineItem {
  description: string
  quantity: number
  rate: number
}

export interface Invoice {
  id: string
  invoiceNumber: string
  clientName: string
  total: number
  status: 'draft' | 'sent' | 'paid' | 'overdue'
  lineItems: LineItem[]
}

// Component Props
export interface InvoiceListProps {
  invoices: Invoice[]
  onView?: (id: string) => void
  onEdit?: (id: string) => void
  onDelete?: (id: string) => void
  onCreate?: () => void
}
```

### Data Guidelines
- Generate realistic, believable data (not "Lorem ipsum")
- Include 5-10 records for main entities
- Include edge cases: empty arrays, long text, different statuses
- Use union types for status/enum fields
- Callback props should cover all spec actions
- Match entity names from global data model

---

## Screenshot Design

**Command:** `/screenshot-design`
**Output:** `product/sections/[section-id]/*.png`

### Process

1. **Capture Current State** - Take screenshot of screen design
2. **Save to Section** - Store in section directory
3. **Include in Export** - Screenshots provide visual reference

### Usage
- Run after `/design-screen` completes
- Captures visual reference for handoff
- Helps implementation agents match fidelity

---

## Section Workflow Summary

For each section in your roadmap:

```
1. /shape-section    → Define spec (flows, requirements)
2. /sample-data      → Generate data.json + types.ts
3. /design-screen    → Create React components
4. /screenshot-design → Capture visual reference
```

Then repeat for next section.

---

## Next Phase

After completing all Sections, proceed to **Export** (`references/export.md`):
- Generate complete handoff package
- Ready-to-use prompts for coding agents
- TDD-ready test instructions
