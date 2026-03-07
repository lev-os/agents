# Validation Decision Tree
**Date**: 2025-12-10

## Decision Flow

```
┌─────────────────────────────────────────────────────────────┐
│ START: Validate SKILL.md                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │ File exists?         │
          └──────┬──────┬────────┘
                 │ NO   │ YES
                 ▼      │
          ❌ REGENERATE │
                        ▼
          ┌──────────────────────┐
          │ Has YAML markers     │
          │ (^---$)?             │
          └──────┬──────┬────────┘
                 │ NO   │ YES
                 ▼      │
          🔧 ADD ---    │
             wrapper    │
                        ▼
          ┌──────────────────────┐
          │ Has name: field?     │
          └──────┬──────┬────────┘
                 │ NO   │ YES
                 ▼      │
          🔧 ADD name:  │
             {slug}     │
                        ▼
          ┌──────────────────────┐
          │ name matches slug?   │
          └──────┬──────┬────────┘
                 │ NO   │ YES
                 ▼      │
          🔧 FIX name   │
             to slug    │
                        ▼
          ┌──────────────────────┐
          │ Has description?     │
          └──────┬──────┬────────┘
                 │ NO   │ YES
                 ▼      │
          🔧 EXTRACT   │
             from       │
             Overview   │
                        ▼
          ┌──────────────────────┐
          │ Description adequate?│
          │ (20-200 chars)       │
          └──────┬──────┬────────┘
                 │ NO   │ YES
                 ▼      │
          ✍️ IMPROVE   │
             description│
                        ▼
          ┌──────────────────────┐
          │ Line count OK?       │
          │ (50-400 lines)       │
          └──────┬──────┬────────┘
                 │ NO   │ YES
                 ▼      │
          ⚠️ FLAG for  │
             review     │
                        ▼
          ┌──────────────────────┐
          │ Has [TODO] markers?  │
          └──────┬──────┬────────┘
                 │ YES  │ NO
                 ▼      │
          ❌ INCOMPLETE │
             regenerate │
                        ▼
                  ✅ PASS
```

## Failure Types & Actions

### 1. MISSING_YAML_MARKERS
**Detection**: No `---` at start of file
**Decision**: ADD frontmatter wrapper
**Action**:
```bash
# Prepend frontmatter
echo "---" > temp.md
echo "name: {slug}" >> temp.md
echo "description: {extract from line 1}" >> temp.md
echo "---" >> temp.md
echo "" >> temp.md
cat SKILL.md >> temp.md
mv temp.md SKILL.md
```

### 2. MISSING_NAME
**Detection**: No `name:` field in frontmatter
**Decision**: ADD name field
**Action**:
```bash
# Insert after first ---
sed -i '1a\
name: {slug}' SKILL.md
```

### 3. NAME_MISMATCH
**Detection**: `name: Title Case` ≠ directory `slug-case`
**Decision**: CHANGE name to match slug
**Action**:
```bash
sed -i 's/^name:.*/name: {slug}/' SKILL.md
```
**Validation**: Name MUST match directory slug exactly

### 4. MISSING_DESCRIPTION
**Detection**: No `description:` field
**Decision**: EXTRACT from Overview/One-Liner
**Action**:
```bash
# Get first meaningful paragraph
desc=$(grep -A1 "^## Overview\|^## One-Liner" SKILL.md | tail -1 | head -c 150)
sed -i '2a\
description: '"$desc" SKILL.md
```

### 5. DESC_TOO_SHORT
**Detection**: Description < 20 chars
**Decision**: EXPAND with context
**Action**: Manual review - description needs more detail

### 6. DESC_TOO_LONG
**Detection**: Description > 200 chars
**Decision**: TRIM to essence
**Action**: Manual review - condense to one-line trigger

### 7. HAS_TODO_MARKERS
**Detection**: Contains `[TODO]` or `[TODO:]`
**Decision**: REGENERATE (incomplete)
**Action**: Flag for research-artifact-generator

### 8. TOO_SHORT
**Detection**: < 50 lines
**Decision**: REGENERATE (stub file)
**Action**: Flag for research-artifact-generator

### 9. TOO_LONG
**Detection**: > 400 lines
**Decision**: WARN (verbose but acceptable if quality is high)
**Action**: Optional trim for scannability

### 10. LEGITIMATE_BRACES
**Detection**: Contains `{}` but in examples/code
**Decision**: IGNORE (not actual placeholders)
**Examples**:
- Instructional: `{cadence}`, `{source}`, `{variable}`
- Code: `@{viewModel}`, `{color: "#fff"}`
- JSON: `{"key": "value"}`
**Action**: No fix needed - update validator to skip these

## Validation Quality Gates

### YAML Frontmatter (REQUIRED)
```yaml
---
name: exact-slug-match  # MUST match directory name
description: One-line summary with trigger (20-200 chars)
---
```

### Description Quality Checklist
- [ ] 20-200 characters
- [ ] Describes WHAT the framework does
- [ ] Includes WHEN to use it (trigger)
- [ ] Avoids vague language
- [ ] Self-contained (no external refs needed)

**Good Description Examples:**
- ✅ "Break down complex problems to fundamental truths and rebuild solutions from scratch when existing approaches are too expensive or inefficient"
- ✅ "Outmaneuver competition by cycling through observe-orient-decide-act faster than opponents, operating inside their decision-making tempo"

**Bad Description Examples:**
- ❌ "A framework for thinking" (vague, no trigger)
- ❌ "Important mental model" (no action, obvious)
- ❌ "{Insert description here}" (placeholder)

## CLI Usage

```bash
# Check pattern
./scripts/validate-cli.sh ergodicity

# Auto-fix pattern
./scripts/validate-cli.sh ergodicity fix

# Generate report
./scripts/validate-cli.sh ergodicity report

# Batch validate all
for dir in contexts/patterns/*/; do
    slug=$(basename "$dir")
    ./scripts/validate-cli.sh "$slug"
done
```
