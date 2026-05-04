# Planning Phase

This phase establishes the foundation: what you're building, why, and how it's structured.

---

## Product Vision

**Command:** `/product-vision`
**Output:** `product/product-overview.md`

### Process

1. **Gather Input** - Ask user to share raw notes, ideas, thoughts about the product
2. **Clarify** - Ask 3-5 targeted questions:
   - Product name (required)
   - Core description (1-3 sentences)
   - Key problems solved (1-5 pain points)
   - How problems are solved (concrete solutions)
   - Main features
3. **Draft & Refine** - Present summary, iterate until approved
4. **Create File** - Write to `product/product-overview.md`

### Output Format

```markdown
# [Product Name]

## Description
[1-3 sentence description]

## Problems & Solutions

### Problem 1: [Problem Title]
[How the product solves it]

### Problem 2: [Problem Title]
[How the product solves it]

## Key Features
- [Feature 1]
- [Feature 2]
- [Feature 3]
```

### Key Notes
- The `# [Product Name]` heading is required for parsing
- Be conversational, help user think through their product
- Always ensure product has a name

---

## Product Roadmap

**Command:** `/product-roadmap`
**Output:** `product/product-roadmap.md`

### Process

1. **Check Prerequisites** - Verify `product-overview.md` exists
2. **Analyze** - Read overview, identify logical sections
3. **Propose Sections** - Suggest 3-5 sections representing:
   - Navigation items (main UI areas)
   - Roadmap phases (build order)
   - Self-contained feature areas
4. **Refine** - Iterate based on user feedback
5. **Create File** - Write roadmap

### Output Format

```markdown
# Product Roadmap

## Sections

### 1. [Section Title]
[One sentence description]

### 2. [Section Title]
[One sentence description]

### 3. [Section Title]
[One sentence description]
```

### Key Notes
- Order by development priority
- Each section should be independently designable/buildable
- Section titles become navigation items
- Keep descriptions to one sentence

---

## Data Model

**Command:** `/data-model`
**Output:** `product/data-model/data-model.md`

### Process

1. **Check Prerequisites** - Verify overview and roadmap exist
2. **Analyze** - Review product and sections, identify implied entities
3. **Present Initial Analysis** - Suggest entities based on product
4. **Clarify** - Ask about:
   - Core entities users will create/view/manage
   - Key information each entity contains
   - How entities relate to each other
5. **Draft & Refine** - Present data model, iterate
6. **Create File** - Write data model

### Output Format

```markdown
# Data Model

## Entities

### [EntityName]
[Plain-language description of what this entity represents]

### [AnotherEntity]
[Plain-language description]

## Relationships

- [Entity1] has many [Entity2]
- [Entity2] belongs to [Entity1]
- [Entity3] belongs to both [Entity1] and [Entity2]
```

### Key Notes
- Keep minimal - entity names, descriptions, relationships
- Do NOT define detailed schemas, field types, or validation
- Use plain language a non-technical person understands
- Entity names should be singular (User, Invoice, Project)
- Leave room for implementation agent to extend

---

## Next Phase

After completing Planning, proceed to **Design System** (`references/design.md`):
- Design tokens (colors, typography)
- Application shell (navigation, layout)
