# Find — Cross-IDE Skill Search Reference

Portable skill discovery using `rg` (ripgrep) with `grep`/`find` fallback. Searches across all major AI IDE skill locations without framework dependencies.

---

## Core Principle

**Skills are files.** Every major AI IDE stores skills/rules/commands as markdown or YAML files in predictable locations. `rg` is the universal search tool that works everywhere.

---

## IDE Skill Paths

### Comprehensive Path Map

```bash
# Claude Code
$HOME/.claude/commands/              # Slash commands
$HOME/.claude/skills/                # Skills (if supported)
$HOME/.claude/agents/                # Agent definitions

# Agent Skills (universal convention)
$HOME/.agents/skills/                # Canonical skill location
$HOME/.agents/skills-db/             # Skills database / marketplace installs

# Cursor
$HOME/.cursor/rules/                 # Cursor rules
$HOME/.cursor/skills/                # Cursor skills (if directory exists)
$HOME/.cursorrc                      # Cursor config (may reference rules)

# Windsurf
$HOME/.windsurf/rules/               # Windsurf rules
$HOME/.windsurf/cascade/rules/       # Cascade-specific rules

# Continue.dev
$HOME/.continue/                     # Continue config directory
$HOME/.continue/config.json          # May reference custom tools
$HOME/.continue/rules/               # Continue rules (if exists)

# Cline
$HOME/.cline/rules/                  # Cline rules
$HOME/.cline/instructions/           # Cline instructions

# Roo Code
$HOME/.roo/rules/                    # Roo Code rules
$HOME/.roo/modes/                    # Roo Code custom modes

# Project-local (any IDE)
.claude/commands/                    # Project-local Claude commands
.claude/skills/                      # Project-local skills
.cursor/rules/                       # Project-local Cursor rules
.agents/skills/                      # Project-local agent skills
```

### Path Array (for scripting)

```bash
GLOBAL_SKILL_PATHS=(
  "$HOME/.claude/commands"
  "$HOME/.claude/skills"
  "$HOME/.claude/agents"
  "$HOME/.agents/skills"
  "$HOME/.agents/skills-db"
  "$HOME/.cursor/rules"
  "$HOME/.cursor/skills"
  "$HOME/.windsurf/rules"
  "$HOME/.windsurf/cascade/rules"
  "$HOME/.continue"
  "$HOME/.continue/rules"
  "$HOME/.cline/rules"
  "$HOME/.cline/instructions"
  "$HOME/.roo/rules"
  "$HOME/.roo/modes"
)

LOCAL_SKILL_PATHS=(
  ".claude/commands"
  ".claude/skills"
  ".cursor/rules"
  ".agents/skills"
)

# Filter to only existing paths
VALID_PATHS=()
for p in "${GLOBAL_SKILL_PATHS[@]}" "${LOCAL_SKILL_PATHS[@]}"; do
  [ -d "$p" ] && VALID_PATHS+=("$p")
done
```

---

## Search Patterns

### Search by Name

Find skills whose name matches a query:

```bash
# Primary: rg across SKILL.md and *.md files
rg -l -i "${QUERY}" \
  --glob="SKILL.md" \
  --glob="*.md" \
  --max-depth=3 \
  "${VALID_PATHS[@]}" 2>/dev/null

# Also check directory names
for p in "${VALID_PATHS[@]}"; do
  ls -d "$p"/*"${QUERY}"*/ 2>/dev/null
done
```

### Search by Trigger

Find skills that trigger on specific keywords:

```bash
# Search YAML frontmatter triggers
rg -i "triggers?:.*${QUERY}" \
  --glob="*.md" \
  --glob="*.yaml" \
  --glob="*.yml" \
  --max-depth=3 \
  "${VALID_PATHS[@]}" 2>/dev/null

# Search trigger arrays
rg -i "^\s*-\s*.*${QUERY}" \
  --glob="SKILL.md" \
  -B5 \
  "${VALID_PATHS[@]}" 2>/dev/null | grep -B5 "triggers"
```

### Search by Description

Find skills whose description matches:

```bash
rg -i "description.*${QUERY}" \
  --glob="SKILL.md" \
  --glob="*.md" \
  -A3 \
  --max-depth=3 \
  "${VALID_PATHS[@]}" 2>/dev/null
```

### Search by Content

Full-text search across all skill files:

```bash
rg -i "${QUERY}" \
  --glob="*.md" \
  --glob="*.yaml" \
  --glob="*.yml" \
  -l \
  --max-depth=4 \
  "${VALID_PATHS[@]}" 2>/dev/null
```

---

## Output Format

### Standard Output

```
📂 {skill-name}
   Path:        {full path to SKILL.md or main file}
   IDE:         {claude-code | cursor | windsurf | continue | cline | roo | universal}
   Description: {first line of description, truncated to 100 chars}
   Triggers:    {comma-separated trigger list}
   Version:     {version if found}
---
```

### Summary Line

```
Found {n} skills matching "{query}" across {m} IDE locations.
```

### Detailed Output (with `--verbose`)

```
📂 {skill-name}
   Path:        {full path}
   IDE:         {ide}
   Description: {full description}
   Triggers:    {trigger list}
   Version:     {version}
   References:  {list of referenced files}
   Related:     {related_skills list if present}
   Size:        {line count}
---
```

---

## Metadata Extraction

When a SKILL.md is found, extract metadata from YAML frontmatter:

```bash
# Extract frontmatter from SKILL.md
extract_metadata() {
  local file="$1"
  local in_frontmatter=false
  local frontmatter=""

  while IFS= read -r line; do
    if [[ "$line" == "---" ]]; then
      if $in_frontmatter; then
        break  # End of frontmatter
      else
        in_frontmatter=true
        continue
      fi
    fi
    if $in_frontmatter; then
      frontmatter+="$line"$'\n'
    fi
  done < "$file"

  echo "$frontmatter"
}

# Parse specific fields
get_field() {
  local frontmatter="$1"
  local field="$2"
  echo "$frontmatter" | grep "^${field}:" | sed "s/^${field}:\s*//"
}
```

---

## IDE Detection

Detect which IDE the user is running in:

```bash
detect_ide() {
  # Claude Code
  if [ -n "$CLAUDE_CODE_WORKSPACE" ] || [ -n "$CLAUDE_SESSION_ID" ]; then
    echo "claude-code"
    return
  fi

  # Cursor
  if [ -n "$CURSOR_SESSION" ] || pgrep -f "cursor" > /dev/null 2>&1; then
    echo "cursor"
    return
  fi

  # Windsurf
  if [ -n "$WINDSURF_SESSION" ] || pgrep -f "windsurf" > /dev/null 2>&1; then
    echo "windsurf"
    return
  fi

  # Continue.dev (runs inside VS Code)
  if [ -f "$HOME/.continue/config.json" ]; then
    echo "continue-dev"
    return
  fi

  # Default
  echo "unknown"
}
```

---

## Fallback Search

When `rg` is not installed:

```bash
if ! command -v rg &> /dev/null; then
  echo "Note: rg (ripgrep) not found. Using grep fallback (slower)."

  # Fallback: find + grep
  find_skills_fallback() {
    local query="$1"
    for p in "${VALID_PATHS[@]}"; do
      find "$p" -name "*.md" -maxdepth 4 -exec grep -li "$query" {} \; 2>/dev/null
    done
  }

  # Fallback: directory name match
  find_by_name_fallback() {
    local query="$1"
    for p in "${VALID_PATHS[@]}"; do
      find "$p" -type d -iname "*${query}*" -maxdepth 3 2>/dev/null
    done
  }
fi
```

---

## Common Queries

| Intent | Query |
|--------|-------|
| Find all skills | `rg -l "^---" --glob="SKILL.md" ${VALID_PATHS[@]}` |
| Skills with triggers | `rg "^triggers:" --glob="SKILL.md" -l ${VALID_PATHS[@]}` |
| Skills by author | `rg "author:.*{name}" --glob="*.md" ${VALID_PATHS[@]}` |
| Skills with references | `rg "references/" --glob="SKILL.md" -l ${VALID_PATHS[@]}` |
| Skills mentioning a tool | `rg "tools:.*{tool}" --glob="SKILL.md" ${VALID_PATHS[@]}` |
| Count all skills | `rg -l "^---" --glob="SKILL.md" ${VALID_PATHS[@]} \| wc -l` |

---

## Cross-IDE Install Paths

When installing a skill to a new IDE:

```bash
install_skill() {
  local skill_dir="$1"  # Source skill directory
  local target_ide="$2" # Target IDE name

  case "$target_ide" in
    claude-code)
      cp -r "$skill_dir" "$HOME/.claude/commands/$(basename $skill_dir)/"
      ;;
    cursor)
      cp -r "$skill_dir" "$HOME/.cursor/skills/$(basename $skill_dir)/"
      ;;
    windsurf)
      cp -r "$skill_dir" "$HOME/.windsurf/rules/$(basename $skill_dir)/"
      ;;
    cline)
      cp -r "$skill_dir" "$HOME/.cline/rules/$(basename $skill_dir)/"
      ;;
    roo)
      cp -r "$skill_dir" "$HOME/.roo/rules/$(basename $skill_dir)/"
      ;;
    universal|*)
      cp -r "$skill_dir" "$HOME/.agents/skills/$(basename $skill_dir)/"
      ;;
  esac
}
```

---

## Quick Reference Card

```
🔍 FIND — search skills, 5 seconds

By name:    rg -l -i "auth" --glob="SKILL.md" ~/.agents/skills/
By trigger: rg -i "triggers.*auth" --glob="*.md" ~/.agents/skills/
By content: rg -i "authentication" --glob="*.md" -l ~/.agents/skills/
All skills: rg -l "^---" --glob="SKILL.md" ~/.agents/skills/ ~/.claude/commands/

No rg? → find ~/.agents/skills -name "*.md" -exec grep -li "auth" {} \;
```
