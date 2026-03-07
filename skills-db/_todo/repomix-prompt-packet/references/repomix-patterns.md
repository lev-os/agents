# Repomix Command Patterns Reference

## Compression Modes Deep Dive

### No Compression (Default)

**When to use:**
- Bug investigation requiring full implementation details
- Code review where logic matters
- Security audits needing complete code analysis
- Implementation planning requiring exact code understanding

**Configuration:**
```json
{
  "compression": {
    "enabled": false
  }
}
```

**Command:**
```bash
npx repomix --output full-context.md
```

**Token Impact:** Highest - includes all implementation code
**Best For:** Small to medium codebases (<50K LOC)

---

### Standard Compression Mode

**When to use:**
- General code review with balanced detail
- Refactoring analysis maintaining some implementation context
- Documentation generation with code examples
- Moderate token optimization needed

**Configuration:**
```json
{
  "compression": {
    "enabled": true,
    "keep_signatures": true,
    "keep_interfaces": false,
    "keep_docstrings": true
  }
}
```

**What's preserved:**
- Function and class definitions with full implementation
- Docstrings and comments
- Type signatures

**What's removed:**
- Nothing (this is balanced mode)

**Command:**
```bash
npx repomix --config-override '{"compression": {"enabled": true, "keep_signatures": true, "keep_docstrings": true}}' --output standard.md
```

**Token Impact:** Medium - balanced approach
**Best For:** Medium to large codebases (50K-200K LOC)

---

### Interface Mode

**When to use:**
- API documentation generation
- Architectural overview and planning
- Understanding public interfaces without implementation details
- Maximum token efficiency while preserving structure

**Configuration:**
```json
{
  "compression": {
    "enabled": true,
    "keep_interfaces": true,
    "keep_signatures": true,
    "keep_docstrings": true
  }
}
```

**What's preserved:**
- Function signatures (names, parameters, return types)
- Class definitions (properties, method signatures)
- Docstrings and type hints
- Imports and exports

**What's removed:**
- Function bodies and implementation logic
- Private methods (language-dependent)

**Command:**
```bash
npx repomix --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' --output interfaces.md
```

**Token Impact:** Low - 60-80% reduction typical
**Best For:** Large codebases (200K+ LOC), architectural analysis

---

### Minimal Compression Mode

**When to use:**
- Configuration file analysis
- Constants and environment variable review
- Maximum token efficiency
- Focus on global state and module structure

**Configuration:**
```json
{
  "compression": {
    "enabled": true,
    "keep_signatures": false,
    "keep_interfaces": false,
    "keep_docstrings": false
  }
}
```

**What's preserved:**
- Global variables and constants
- Imports and module dependencies
- Top-level code execution

**What's removed:**
- All function and class definitions
- Implementation details
- Docstrings

**Command:**
```bash
npx repomix --config-override '{"compression": {"enabled": true, "keep_signatures": false, "keep_interfaces": false}}' --output minimal.md
```

**Token Impact:** Minimal - 90%+ reduction possible
**Best For:** Very large codebases, configuration-focused analysis

---

## Output Format Patterns

### Markdown Format

**Best for:**
- Human readability
- General LLM consumption
- Documentation generation
- Code review

**Features:**
- Syntax highlighting via code blocks
- Clear section headers
- Maintained formatting

**Command:**
```bash
npx repomix --style markdown --output repo.md
```

**Example Output Structure:**
```markdown
# Repository Structure

[AI-oriented explanation]

## Files

### src/index.ts

\`\`\`typescript
// code here
\`\`\`
```

---

### XML Format

**Best for:**
- Structured data extraction
- Tool integration and parsing
- Automated processing workflows
- Machine-readable output

**Features:**
- Strict structure
- Easy parsing
- Metadata embedded

**Command:**
```bash
npx repomix --style xml --output repo.xml
```

**Example Output Structure:**
```xml
<repository>
  <metadata>
    <file_count>42</file_count>
    <token_count>15432</token_count>
  </metadata>
  <files>
    <file path="src/index.ts">
      <content>...</content>
    </file>
  </files>
</repository>
```

---

### Plain Text Format

**Best for:**
- Maximum compatibility
- Minimal parsing overhead
- Simple processing pipelines
- Token efficiency

**Features:**
- No markup overhead
- Clean separators
- Direct copy/paste

**Command:**
```bash
npx repomix --style plain --output repo.txt
```

---

## Advanced Configuration Patterns

### Security-First Pattern

**Use case:** Sharing snapshots externally or with teams

```bash
npx repomix \
  --config-override '{
    "security": {
      "enable_security_check": true,
      "exclude_suspicious_files": true
    }
  }' \
  --output secure-snapshot.md
```

**Features:**
- Scans for secrets and credentials
- Excludes flagged files automatically
- Safe for external sharing

---

### Line Numbers for Debugging

**Use case:** Bug investigation with precise code references

```bash
npx repomix \
  --config-override '{
    "output": {
      "show_line_numbers": true
    }
  }' \
  --output debug-context.md \
  --style markdown
```

**Benefits:**
- Easy code referencing in bug reports
- Precise line-level analysis
- Better collaboration

---

### Selective Directory Inclusion

**Use case:** Focus on specific modules or layers

```bash
# Backend only
npx repomix \
  --config-override '{
    "include": ["src/api/**", "src/services/**", "src/models/**"]
  }' \
  --output backend.md

# Frontend only
npx repomix \
  --config-override '{
    "include": ["src/components/**", "src/pages/**", "src/hooks/**"]
  }' \
  --output frontend.md
```

**Benefits:**
- Reduced token count
- Focused analysis
- Parallel snapshot generation

---

### Multi-Format Generation

**Use case:** Different consumers with different needs

```bash
# Markdown for humans
npx repomix --style markdown --output docs.md

# XML for tools
npx repomix --style xml --output machine-readable.xml

# Plain for compatibility
npx repomix --style plain --output simple.txt
```

---

### Remote Repository Analysis

**Use case:** Analyze repos without local cloning

```bash
npx repomix \
  --remote https://github.com/username/repository.git \
  --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' \
  --output remote-analysis.md
```

**Benefits:**
- No local disk usage
- Quick analysis of public repos
- Evaluate before cloning

---

### Custom Output Location

**Use case:** Organized snapshot management

```bash
npx repomix \
  --output ./snapshots/$(date +%Y-%m-%d)-architecture.md \
  --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}'
```

---

## Configuration File Patterns

For recurring workflows, create saved configurations:

### Documentation Generation Config

**File:** `repomix.docs.json`

```json
{
  "output": {
    "file_path": "api-documentation.md",
    "style": "markdown",
    "show_line_numbers": false
  },
  "compression": {
    "enabled": true,
    "keep_interfaces": true,
    "keep_signatures": true,
    "keep_docstrings": true
  },
  "include": [
    "src/api/**",
    "src/controllers/**",
    "src/routes/**"
  ]
}
```

**Usage:**
```bash
npx repomix --config repomix.docs.json
```

---

### Debug Investigation Config

**File:** `repomix.debug.json`

```json
{
  "output": {
    "file_path": "debug-context.md",
    "style": "markdown",
    "show_line_numbers": true
  },
  "compression": {
    "enabled": false
  },
  "security": {
    "enable_security_check": false
  }
}
```

**Usage:**
```bash
npx repomix --config repomix.debug.json
```

---

### Security Audit Config

**File:** `repomix.security.json`

```json
{
  "output": {
    "file_path": "security-review.md",
    "style": "markdown",
    "show_line_numbers": true
  },
  "compression": {
    "enabled": false
  },
  "security": {
    "enable_security_check": true,
    "exclude_suspicious_files": false
  }
}
```

**Usage:**
```bash
npx repomix --config repomix.security.json
```

---

## Token Optimization Strategies

### Progressive Compression

Start with interface mode, then selectively expand:

```bash
# Step 1: Get overview (low tokens)
npx repomix --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' --output overview.md

# Step 2: After identifying area of interest, get full detail
npx repomix --config-override '{"include": ["src/auth/**"]}' --output auth-detail.md
```

---

### Module-Based Splitting

For large codebases, create focused snapshots:

```bash
# Generate snapshots per module
for module in api database frontend workers; do
  npx repomix \
    --config-override "{\"include\": [\"src/$module/**\"]}" \
    --output "snapshots/${module}.md"
done
```

---

### Smart Include/Exclude Patterns

Focus on production code, skip tests and configs:

```bash
npx repomix \
  --config-override '{
    "include": ["src/**", "lib/**"],
    "exclude": ["**/*.test.ts", "**/*.spec.js", "**/node_modules/**"]
  }' \
  --output production-code.md
```

---

## Common Command Combinations

### Quick Documentation

```bash
npx repomix --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' -o docs.md && echo "Generated: docs.md"
```

---

### Thorough Bug Analysis

```bash
npx repomix --config-override '{"output": {"show_line_numbers": true}, "security": {"enable_security_check": false}}' -o bug-context.md --style markdown
```

---

### Architectural Review

```bash
npx repomix --config-override '{"compression": {"enabled": true, "keep_interfaces": true, "keep_docstrings": true}}' -o architecture.md
```

---

### Pre-Sharing Security Check

```bash
npx repomix --config-override '{"security": {"enable_security_check": true, "exclude_suspicious_files": true}}' -o safe-snapshot.md && echo "Security checked ✓"
```

---

## Troubleshooting Common Issues

### "Output too large for LLM context"

**Solutions:**
1. Enable compression: `--config-override '{"compression": {"enabled": true}}'`
2. Use interface mode: `--config-override '{"compression": {"keep_interfaces": true}}'`
3. Split by module: `--config-override '{"include": ["src/specific-module/**"]}'`
4. Check token count first and adjust

---

### "Missing expected files"

**Solutions:**
1. Check `.gitignore` - repomix respects it
2. Verify paths: `--config-override '{"include": ["correct/path/**"]}'`
3. Use explicit include patterns instead of relying on defaults

---

### "Secrets detected in output"

**Solutions:**
1. Enable security check: `--config-override '{"security": {"enable_security_check": true}}'`
2. Review and clean before sharing
3. Add sensitive files to `.gitignore`

---

### "Compression removed too much context"

**Solutions:**
1. Reduce compression: switch from minimal to standard mode
2. Use selective includes to focus on specific areas
3. Generate multiple snapshots: one overview + detailed modules
