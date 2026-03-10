# Export Phase

This phase generates the complete handoff package for implementation.

---

## Export Product

**Command:** `/export-product`
**Output:** `product-plan/`, `product-plan.zip`

### Prerequisites

**Required:**
- `product/product-overview.md`
- `product/product-roadmap.md`
- At least one section with screen designs

**Recommended:**
- `product/data-model/data-model.md`
- `product/design-system/colors.json`
- `product/design-system/typography.json`
- `src/shell/components/AppShell.tsx`

### Export Structure

```
product-plan/
├── README.md                    # Quick start guide
├── product-overview.md          # Product summary
│
├── prompts/                     # Ready-to-use prompts
│   ├── one-shot-prompt.md       # Full implementation prompt
│   └── section-prompt.md        # Section-by-section template
│
├── instructions/
│   ├── one-shot-instructions.md # All milestones combined
│   └── incremental/
│       ├── 01-foundation.md     # Design tokens, data model, shell
│       ├── 02-[section].md      # First section
│       └── [NN]-[section].md    # Subsequent sections
│
├── design-system/
│   ├── tokens.css
│   ├── tailwind-colors.md
│   └── fonts.md
│
├── data-model/
│   ├── README.md
│   ├── types.ts
│   └── sample-data.json
│
├── shell/
│   ├── README.md
│   ├── components/
│   └── screenshot.png
│
└── sections/[section-id]/
    ├── README.md
    ├── tests.md                 # TDD instructions
    ├── components/
    ├── types.ts
    ├── sample-data.json
    └── screenshot.png
```

---

## Generated Prompts

### one-shot-prompt.md

Pre-written prompt that instructs coding agent to:
1. Read all documentation
2. Ask clarifying questions about:
   - Authentication (email/password, OAuth, magic links)
   - User modeling (single-user, multi-tenant, roles)
   - Tech stack preferences
   - Backend business logic
3. Create implementation plan
4. Build entire app

### section-prompt.md

Template for incremental implementation:
1. Define SECTION_NAME, SECTION_ID, milestone number
2. Read section-specific docs
3. Ask clarifying questions
4. Use TDD approach with tests.md
5. Implement section

---

## Generated Instructions

### Preamble (in all instructions)

```markdown
## About These Instructions

**What you're receiving:**
- Finished UI designs (React components with full styling)
- Data model definitions (TypeScript types and sample data)
- UI/UX specifications (user flows, requirements, screenshots)
- Design system tokens (colors, typography, spacing)
- Test-writing instructions for each section (for TDD approach)

**What you need to build:**
- Backend API endpoints and database schema
- Authentication and authorization
- Data fetching and state management
- Business logic and validation
- Integration of provided UI components with real data

**Important guidelines:**
- **DO NOT** redesign or restyle the provided components
- **DO** wire up callback props to your routing and API
- **DO** replace sample data with real data from backend
- **DO** implement error handling and loading states
- **DO** implement empty states when no records exist
- **DO** use test-driven development with tests.md
```

### Foundation Milestone (01-foundation.md)

Covers:
- Design tokens configuration
- Data model types
- Routing structure
- Application shell integration

### Section Milestones (NN-[section].md)

Each section includes:
- Overview of functionality
- Key capabilities
- TDD workflow reference
- Components to copy
- Callbacks to wire up
- Empty state handling
- Expected user flows
- Done criteria

---

## Test Instructions (tests.md)

Each section gets framework-agnostic test instructions:

```markdown
# Test Instructions: [Section]

## User Flow Tests

### Flow 1: [Primary Flow]
**Success Path:**
- Setup: [preconditions]
- Steps: [user actions with exact UI labels]
- Expected: [specific assertions]

**Failure Path:**
- Setup: [conditions causing failure]
- Expected: [error handling]

## Empty State Tests
- Primary empty state (no records)
- Related records empty
- Filtered/search empty

## Component Interaction Tests
- Renders correctly
- User interactions
- Loading/error states

## Edge Cases
- Long names, 100+ items, transitions
```

---

## How to Use Export

### Option A: Incremental (Recommended)

1. Copy `product-plan/` to codebase
2. Start with `01-foundation.md`
3. For each section:
   - Open `prompts/section-prompt.md`
   - Fill in section variables
   - Paste into coding agent
   - Answer questions, implement
4. Review after each milestone

### Option B: One-Shot

1. Copy `product-plan/` to codebase
2. Open `prompts/one-shot-prompt.md`
3. Paste into coding agent
4. Answer clarifying questions
5. Let agent plan and implement

---

## Component Transformation

When exporting, components are transformed:
- Import paths changed from `@/...` to relative
- Design OS-specific imports removed
- Preview wrappers excluded (not portable)
- Only props-based components included

---

## Final Output

After export:
1. `product-plan/` directory with all assets
2. `product-plan.zip` for easy download
3. Restart dev server to see Export page
4. Download zip, copy to implementation project
5. Use prompts to guide coding agent
