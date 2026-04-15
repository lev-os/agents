# Learning Flywheel Quick Start

## 5-Minute Workflow

### Step 1: Check Your History

```bash
cass status --json && cass index --json
```

### Step 2: Find Your Rituals

```bash
# Replace PROJECT with your project name
cass search "*" --workspace /data/projects/PROJECT --json --fields minimal --limit 500 \
  | jq '[.hits[] | select(.line_number <= 3) | .title[0:80]]
        | group_by(.) | map({prompt: .[0], count: length})
        | sort_by(-.count) | map(select(.count >= 5)) | .[0:20]'
```

Or use the helper script:

```bash
./scripts/mine_rituals.py --workspace /data/projects/PROJECT --min-count 5
```

### Step 3: Pick a Ritual

Look for patterns with `count >= 10`. These are your proven methodology.

### Step 4: Generate Draft

```bash
./scripts/generate_skill_draft.py \
  --prompt "the ritual prompt" \
  --count 15 \
  --workspace /data/projects/PROJECT \
  --output draft-skill.md
```

### Step 5: Refine

Edit the draft to:
1. Add proper triggers (when to use)
2. Explain why it works
3. Document counter-examples (when NOT to use)
4. Verify provenance links

### Step 6: Install

```bash
mkdir -p ~/.claude/skills/your-new-skill/
mv draft-skill.md ~/.claude/skills/your-new-skill/SKILL.md
```

---

## Key Numbers

| Threshold | Meaning |
|-----------|---------|
| 50+ sessions | Minimum for meaningful patterns |
| 10+ count | Validated ritual |
| 5-9 count | Emerging pattern |
| <5 count | One-off, not generalizable |

---

## Common Patterns to Look For

- Build/test commands you repeat
- Search patterns you use
- Error handling approaches
- Code review triggers
- Documentation patterns
- Git workflows
