```markdown
# Deduplication Agent - Find & Merge Duplicates

## Your Role
Identify duplicate frameworks across all 15 domains and merge them intelligently.

## Context
- Scan all `docs/domains/*/task.csv` files
- Compare framework names, descriptions, sources
- Merge when found in both mental-models and practitioner tracks

## Your Task
Find duplicates, merge best content, avoid duplicate YAMLs.

### Your Process

**Step 1: Scan All CSVs (10 min)**
```bash
# Extract all framework names
for dir in docs/domains/*/; do
  tail -n +2 "$dir/task.csv" | cut -d, -f2
done | sort | uniq -d > potential-duplicates.txt
```

**Step 2: Investigate Each Duplicate (5 min each)**

For each in `potential-duplicates.txt`:
1. Find which domains have it
2. Compare:
   - Track (mental-models vs practitioner)
   - Status (KNOWN vs UNKNOWN)
   - Score (which is higher quality?)
   - YAML (which is more detailed?)

**Step 3: Decision Logic**

**Case A: Same framework, both COMPLETE**
- Keep the higher-scoring version
- Add tags to YAML: `tags: ["mental-models", "practitioner-frameworks"]`
- Mark duplicate in CSV: `status: DUPLICATE, notes: "See domain X ID #Y"`

**Case B: Same framework, one KNOWN, one UNKNOWN**
- Keep the KNOWN version
- Mark UNKNOWN as duplicate
- Add note about other track mention

**Case C: Similar but different (e.g., "First Principles" vs "First Principles Thinking")**
- Review manually
- If truly different: keep both
- If same: merge as Case A

**Step 4: Merge YAML Content**

When merging:
```yaml
metadata:
  tags:
    - "mental-models"
    - "practitioner-frameworks"
  cross_domain_applications:
    - "[Mental models perspective]"
    - "[Practitioner perspective]"

context:
  framework_overview: |
    [Merge both descriptions, note dual origins]

  # Include best sections from both versions
```

**Step 5: Update All References**

```bash
# Find any integration references to duplicate
grep -r "duplicate-framework-slug" contexts/patterns/*/context.yaml

# Update to point to canonical version
```

**Step 6: Generate Report**

Create `deduplication-report.md`:

```markdown
# Deduplication Report

## Summary
- Total frameworks scanned: [X]
- Duplicates found: [Y]
- Duplicates merged: [Z]

## Duplicate Pairs
### 1. [Framework Name]
- **Domains**: [Domain 1], [Domain 2]
- **Tracks**: [Track 1], [Track 2]
- **Decision**: [Keep Domain 1, merge content from Domain 2]
- **Action**: [Updated YAML, marked CSV duplicate]

### 2. [Framework Name]
...

## Cross-Domain Patterns
[Frameworks appearing in 3+ domains - note as highly cross-applicable]

## Recommendations
[Suggestions for improving domain boundaries if many duplicates]
```

### Quality Gates
- ❌ Two identical frameworks with separate YAMLs = Must merge
- ❌ Duplicate marked but YAML not updated = Incomplete
- ✅ All duplicates either merged or documented = Complete

### When to Run
- After all domains have generated YAMLs
- Before final count and status report
- Periodically if new frameworks added

### Output Deliverables
1. `deduplication-report.md`
2. Updated YAMLs with merged content
3. Updated task.csv files with DUPLICATE status
```

---

## Phase 3: Parse sources.md → sources.json

### Script: parse-sources.js

```javascript
#!/usr/bin/env node
// parse-sources.js - Extract links from sources.md

const fs = require('fs');
const path = require('path');

const sourcesPath = path.join(__dirname, 'docs/seed/sources.md');
const outputPath = path.join(__dirname, 'docs/sources.json');

const content = fs.readFileSync(sourcesPath, 'utf8');

// Match [title](url) pattern
const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;

const sources = [];
let match;
let currentQuery = '';

const lines = content.split('\n');

for (const line of lines) {
  // Capture search query lines (lines without links)
  if (!line.includes('](') && line.trim().length > 0 && !line.startsWith('[')) {
    currentQuery = line.trim();
  }

  // Extract links
  while ((match = linkRegex.exec(line)) !== null) {
    sources.push({
      title: match[1],
      url: match[2],
      search_query: currentQuery
    });
  }
}

const output = {
  generated: new Date().toISOString(),
  count: sources.length,
  sources: sources
};

fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));

console.log(`✅ Extracted ${sources.length} links to ${outputPath}`);
```

**Run:**
```bash
node parse-sources.js
```

**Expected output:** `docs/sources.json` with ~2,148 entries

---

## Phase 4: Domain Extraction

Extract 15 domain.md files from seed docs.

### Mental Models Domains (from index.md)

#### domains/01-core-mental-models/domain.md
