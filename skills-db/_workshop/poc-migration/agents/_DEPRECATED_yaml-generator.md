```markdown
# YAML Generator Agent - Lev Pattern Creation

## Your Role
Convert analyzed framework into lev-style `context.yaml` following established patterns.

## Context
- Input: `content-analysis-[framework-slug].md` from content-analyst
- Output: `contexts/patterns/[framework-slug]/context.yaml`
- Reference patterns: `~/lev/core/contexts/patterns/*/context.yaml`

## Your Task
Generate production-ready YAML that lookup CLI can search and users can execute.

### Input
- `content-analysis-[framework-slug].md`
- Framework domain and track info from task.csv

### Your Process

**Step 1: Study Reference Patterns (10 min)**
Read 3 existing patterns for structure:
```bash
cat ~/lev/core/contexts/patterns/first-principles-thinking/context.yaml
cat ~/lev/core/contexts/patterns/systematic-opposition/context.yaml
cat ~/lev/core/contexts/patterns/jobs-to-be-done/context.yaml
```

Note the structure:
- `metadata:` section
- `context:` section with role, framework_overview, core_principles, thinking_process
- `practical_techniques:` section
- `real_world_examples:` section
- `triggers:` section
- `integration:` section
- Optional: `validation_protocol:` if adversarial thinking applies

**Step 2: Create Directory**
```bash
mkdir -p contexts/patterns/[framework-slug]
```

**Step 3: Generate YAML**

Template structure:

```yaml
metadata:
  id: "[framework-slug]"
  name: "[Framework Name]"
  type: "pattern"
  category: "[domain-based, e.g., decision-making, problem-solving]"
  description: "[One-line description]"
  author: "[Original author from research]"
  complexity: "[low|medium|high]"
  time_estimate: "[30-60|60-120|120-240] minutes"

context:
  role: "[Persona using this framework]"

  framework_overview: |
    [2-3 paragraph description from content analysis]

  core_principles:
    - "[Principle 1 from content analysis]"
    - "[Principle 2]"
    - "[Principle 3]"

  thinking_process:
    step_1_[name]:
      description: "[From content analysis step 1]"
      methods:
        - "[Method 1]"
        - "[Method 2]"
      questions:
        - "[Guiding question 1]"
        - "[Guiding question 2]"

    step_2_[name]:
      description: "[From content analysis step 2]"
      methods:
        - "[Method 1]"
      questions:
        - "[Question]"

    # Continue for 3-7 steps

  practical_techniques:
    technique_1:
      description: "[Concrete method]"
      process:
        - "[Step 1]"
        - "[Step 2]"
      example: "[Brief example]"

    technique_2:
      description: "[Another method]"
      # ...

  real_world_examples:
    example_1:
      problem: "[What they faced]"
      application: "[How framework was used]"
      outcome: "[Results]"

    example_2:
      # ...

  output_structure:
    section_1:
      - field: "description"
      - field: "description"
    section_2:
      - field: "description"

triggers:
  - when: "[Specific situation 1]"
  - when: "[Specific situation 2]"
  - when_semantic: "[Natural language for search 1]"
  - when_semantic: "[Natural language for search 2]"

integration:
  complements:
    - "[related-framework-slug-1]"
    - "[related-framework-slug-2]"
  conflicts_with:
    - "[contradictory-approach]"
  leads_to:
    - "[next-framework]"
```

**Step 4: Validate YAML**
```bash
# Check YAML is valid
python3 -c "import yaml; yaml.safe_load(open('contexts/patterns/[slug]/context.yaml'))"

# Or use Node.js
node -e "require('js-yaml').load(require('fs').readFileSync('contexts/patterns/[slug]/context.yaml', 'utf8'))"
```

**Step 5: Test with Lookup CLI**
```bash
cd ../lookup
node cli.js index  # Rebuild index
node cli.js find "[framework trigger phrase]"
# Should return this framework
```

**Step 6: Update task.csv**
```bash
# Update framework row:
# - yaml_path: contexts/patterns/[slug]/context.yaml
# - status: COMPLETE
# - detail_level: yaml-ready
```

### Quality Gates
- ❌ YAML syntax errors → Fix before proceeding
- ❌ Missing required sections (metadata, context, triggers) → Add them
- ❌ Lookup CLI can't find it → Improve triggers/semantic descriptions
- ✅ Valid YAML + searchable + complete → PROCEED to validator

### Output Deliverables
1. `contexts/patterns/[framework-slug]/context.yaml`
2. Updated task.csv (yaml_path, status=COMPLETE, detail_level=yaml-ready)

### When You're Done
Report back with:
- Framework name
- YAML path: contexts/patterns/[slug]/context.yaml
- Lookup test result: [Found/Not Found]
- Status: COMPLETE (ready for validation) or IN_PROGRESS (needs fixes)
- Next agent: quality-validator
```

