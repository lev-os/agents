# Use Case Decision Matrix

## Quick Decision Tree

```
START: What's your primary goal?
│
├─ Documentation Generation
│  └─ → Use INTERFACE MODE + Markdown
│      Command: npx repomix --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' -o docs.md
│
├─ Bug Investigation
│  └─ Do you need line numbers for precise references?
│      ├─ Yes → FULL CONTEXT + Line Numbers + Markdown
│      │   Command: npx repomix --config-override '{"output": {"show_line_numbers": true}}' -o debug.md
│      └─ No → FULL CONTEXT + Markdown
│          Command: npx repomix -o debug.md
│
├─ Architectural Planning
│  └─ → Use INTERFACE MODE + Markdown
│      Command: npx repomix --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' -o architecture.md
│
├─ Code Review
│  └─ How detailed does the review need to be?
│      ├─ High-level patterns → INTERFACE MODE + Markdown
│      │   Command: npx repomix --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' -o review.md
│      └─ Implementation details → STANDARD COMPRESSION + Markdown
│          Command: npx repomix --config-override '{"compression": {"enabled": true, "keep_signatures": true}}' -o review-detailed.md
│
├─ Security Audit
│  └─ → Use FULL CONTEXT + Security Scan + Line Numbers + Markdown
│      Command: npx repomix --config-override '{"security": {"enable_security_check": true}, "output": {"show_line_numbers": true}}' -o security.md
│
├─ Test Generation
│  └─ → Use INTERFACE MODE + Markdown
│      Command: npx repomix --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' -o test-context.md
│
└─ Configuration Analysis
   └─ → Use MINIMAL MODE + Plain Text
       Command: npx repomix --config-override '{"compression": {"enabled": true, "keep_signatures": false, "keep_interfaces": false}}' -o config.txt
```

---

## Use Case Profiles

### 1. Documentation Generation

**Goal:** Create API docs, user guides, or technical documentation

**Optimal Configuration:**
- **Compression:** Interface Mode (keep_interfaces: true)
- **Format:** Markdown
- **Line Numbers:** No
- **Security Scan:** No (unless sharing externally)

**Rationale:**
- Interface mode provides function signatures and docstrings without implementation clutter
- Markdown offers readable output with code formatting
- Line numbers add noise for documentation
- Security scanning only needed if sharing outside team

**Configuration:**
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
  }
}
```

**Token Impact:** ⭐⭐ (Low - 60-80% reduction)

**Prompt Pattern:**
```
This is a [framework] API for [purpose]. Generate comprehensive documentation
covering all endpoints, parameters, responses, and error codes. Organize by
resource type and include authentication requirements.
```

---

### 2. Bug Investigation

**Goal:** Provide full context for debugging specific errors or unexpected behavior

**Optimal Configuration:**
- **Compression:** None (full implementation)
- **Format:** Markdown
- **Line Numbers:** Yes
- **Security Scan:** No

**Rationale:**
- Full implementation needed to understand logic and data flows
- Line numbers enable precise code references in bug reports
- Markdown for readability
- Security scanning not relevant for internal debugging

**Configuration:**
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

**Token Impact:** ⭐⭐⭐⭐⭐ (Highest - no reduction)

**Prompt Pattern:**
```
Error: [exact error message]
Occurs when: [reproduction steps]
Expected: [correct behavior]
Actual: [what happens]

Trace the execution path, identify root cause, and suggest fix with code examples.
Focus on: [specific files or patterns]
```

---

### 3. Architectural Planning / Refactoring

**Goal:** Review system architecture and plan improvements or migrations

**Optimal Configuration:**
- **Compression:** Interface Mode
- **Format:** Markdown
- **Line Numbers:** No
- **Security Scan:** No

**Rationale:**
- Interface mode shows structure without implementation noise
- Focus on components, dependencies, and boundaries
- Implementation details distract from architectural concerns
- Markdown for clear structure visualization

**Configuration:**
```json
{
  "output": {
    "file_path": "architecture.md",
    "style": "markdown",
    "show_line_numbers": false
  },
  "compression": {
    "enabled": true,
    "keep_interfaces": true,
    "keep_signatures": true,
    "keep_docstrings": true
  }
}
```

**Token Impact:** ⭐⭐ (Low - 60-80% reduction)

**Prompt Pattern:**
```
Current state: [monolith/microservices/etc + pain points]
Goal: [desired architecture or specific improvement]

Analyze structure and provide:
1. Assessment of current coupling and dependencies
2. Proposed boundaries or refactoring with justification
3. Migration strategy considering [constraints]
4. Risk analysis and mitigation

Constraints: [uptime, team size, timeline, etc.]
```

---

### 4. Code Review (High-Level)

**Goal:** Review patterns, architecture, and general code quality

**Optimal Configuration:**
- **Compression:** Interface Mode
- **Format:** Markdown
- **Line Numbers:** No
- **Security Scan:** Optional

**Rationale:**
- Interfaces sufficient for pattern and structure review
- Markdown for organized, readable feedback
- Line numbers not necessary for high-level review
- Security scan useful if external sharing planned

**Configuration:**
```json
{
  "output": {
    "file_path": "code-review.md",
    "style": "markdown",
    "show_line_numbers": false
  },
  "compression": {
    "enabled": true,
    "keep_interfaces": true,
    "keep_signatures": true,
    "keep_docstrings": true
  },
  "security": {
    "enable_security_check": true
  }
}
```

**Token Impact:** ⭐⭐ (Low - 60-80% reduction)

**Prompt Pattern:**
```
Review for:
1. Architectural patterns and consistency
2. Code organization and modularity
3. Naming conventions and readability
4. Potential maintainability issues

Provide findings with severity levels and specific recommendations.
Prioritize: [architectural concerns over style]
```

---

### 5. Code Review (Implementation-Level)

**Goal:** Deep review including logic, algorithms, and implementation quality

**Optimal Configuration:**
- **Compression:** Standard Mode
- **Format:** Markdown
- **Line Numbers:** Yes
- **Security Scan:** Yes

**Rationale:**
- Need implementation details for logic review
- Standard compression balances detail with token efficiency
- Line numbers for precise issue location
- Security scan catches common vulnerabilities

**Configuration:**
```json
{
  "output": {
    "file_path": "detailed-review.md",
    "style": "markdown",
    "show_line_numbers": true
  },
  "compression": {
    "enabled": true,
    "keep_signatures": true,
    "keep_docstrings": true
  },
  "security": {
    "enable_security_check": true
  }
}
```

**Token Impact:** ⭐⭐⭐⭐ (Medium-High)

**Prompt Pattern:**
```
Deep code review focusing on:
1. Implementation correctness and edge cases
2. Performance and efficiency
3. Error handling completeness
4. Security vulnerabilities

For each issue:
- Severity, Location, Description, Impact, Recommendation with code
```

---

### 6. Security Audit

**Goal:** Comprehensive security analysis for vulnerabilities and compliance

**Optimal Configuration:**
- **Compression:** None (full context needed)
- **Format:** Markdown
- **Line Numbers:** Yes
- **Security Scan:** Yes

**Rationale:**
- Security requires full implementation visibility
- Line numbers for precise vulnerability location
- Security scan provides automated detection baseline
- Markdown for organized findings

**Configuration:**
```json
{
  "output": {
    "file_path": "security-audit.md",
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

**Token Impact:** ⭐⭐⭐⭐⭐ (Highest)

**Prompt Pattern:**
```
Security audit for [application type] handling [data sensitivity].

Focus areas:
1. Authentication & Authorization
2. Input validation & injection prevention
3. Data protection (encryption, PII handling)
4. Dependency vulnerabilities
5. [Domain-specific concerns]

For each vulnerability:
- OWASP category, Severity, Location, Attack vector, Impact, Remediation

Compliance: [GDPR, HIPAA, PCI-DSS, etc.]
```

---

### 7. Test Generation

**Goal:** Generate comprehensive test suites for existing code

**Optimal Configuration:**
- **Compression:** Interface Mode
- **Format:** Markdown
- **Line Numbers:** No
- **Security Scan:** No

**Rationale:**
- Interfaces show what needs testing without implementation noise
- Focus on public API surface
- Markdown for clear test structure
- Security scanning irrelevant for test generation

**Configuration:**
```json
{
  "output": {
    "file_path": "test-generation-context.md",
    "style": "markdown",
    "show_line_numbers": false
  },
  "compression": {
    "enabled": true,
    "keep_interfaces": true,
    "keep_signatures": true,
    "keep_docstrings": true
  }
}
```

**Token Impact:** ⭐⭐ (Low)

**Prompt Pattern:**
```
Generate comprehensive test suite for [module/component] covering:
1. Happy paths (expected inputs, normal flows)
2. Edge cases (boundary values, empty inputs, limits)
3. Error conditions (invalid inputs, exceptions, failures)
4. [Domain-specific scenarios]

Framework: [Jest, pytest, etc.]
Coverage goal: [percentage or specific paths]
Include setup, assertions, and descriptive test names.
```

---

### 8. Configuration Analysis

**Goal:** Review configuration files, environment variables, constants

**Optimal Configuration:**
- **Compression:** Minimal Mode
- **Format:** Plain Text
- **Line Numbers:** No
- **Security Scan:** Yes (critical for secrets detection)

**Rationale:**
- Minimal mode removes functions/classes, keeping only globals/constants
- Plain text sufficient for config analysis
- Security scanning critical for detecting hardcoded secrets
- Focus on configuration without code clutter

**Configuration:**
```json
{
  "output": {
    "file_path": "config-analysis.txt",
    "style": "plain",
    "show_line_numbers": false
  },
  "compression": {
    "enabled": true,
    "keep_signatures": false,
    "keep_interfaces": false,
    "keep_docstrings": false
  },
  "security": {
    "enable_security_check": true
  }
}
```

**Token Impact:** ⭐ (Minimal - 90%+ reduction)

**Prompt Pattern:**
```
Review configuration and environment setup for:
1. Missing required config values
2. Hardcoded secrets or credentials (CRITICAL)
3. Environment-specific inconsistencies
4. Insecure defaults
5. [Domain-specific config concerns]

Provide recommendations for proper config management.
```

---

### 9. Onboarding / Knowledge Transfer

**Goal:** Help new developers understand codebase structure and patterns

**Optimal Configuration:**
- **Compression:** Interface Mode
- **Format:** Markdown
- **Line Numbers:** No
- **Security Scan:** No

**Rationale:**
- Interfaces provide overview without overwhelming detail
- Markdown for readable documentation
- New developers need structure understanding, not implementation depth
- Security scanning not relevant for internal onboarding

**Configuration:**
```json
{
  "output": {
    "file_path": "codebase-overview.md",
    "style": "markdown",
    "show_line_numbers": false
  },
  "compression": {
    "enabled": true,
    "keep_interfaces": true,
    "keep_signatures": true,
    "keep_docstrings": true
  }
}
```

**Token Impact:** ⭐⭐ (Low)

**Prompt Pattern:**
```
Create onboarding guide for new developer joining [team/project].

Include:
1. High-level architecture overview
2. Key components and their responsibilities
3. Common patterns and conventions used
4. Important files/directories to know
5. Data flow for typical operations
6. Development setup and workflows

Audience: Mid-level developer familiar with [tech stack] but new to this codebase.
Tone: Welcoming and educational, not overwhelming.
```

---

### 10. Dependency Analysis

**Goal:** Map dependencies, identify coupling, plan modularization

**Optimal Configuration:**
- **Compression:** Minimal Mode (focus on imports)
- **Format:** Plain Text or XML
- **Line Numbers:** No
- **Security Scan:** No

**Rationale:**
- Minimal mode preserves imports while removing implementation
- Focus on dependency graph
- XML useful for tool-based graph generation
- Plain text for simple analysis

**Configuration:**
```json
{
  "output": {
    "file_path": "dependencies.txt",
    "style": "plain",
    "show_line_numbers": false
  },
  "compression": {
    "enabled": true,
    "keep_signatures": false,
    "keep_interfaces": false,
    "keep_docstrings": false
  }
}
```

**Token Impact:** ⭐ (Minimal)

**Prompt Pattern:**
```
Analyze dependency structure:
1. Map import relationships between modules
2. Identify circular dependencies
3. Highlight tight coupling points
4. Suggest modularization opportunities
5. Recommend dependency injection improvements

Visualize as: [dependency graph description or mermaid diagram]
```

---

## Selection Flowchart by Codebase Size

### Small Codebase (<20K LOC)

**Default Strategy:** Full context, no compression

```
Use Case          → Configuration
─────────────────────────────────
Documentation     → Interface Mode (optional optimization)
Bug Investigation → Full Context
Architecture      → Full Context (small enough)
Code Review       → Full Context
Security Audit    → Full Context + Security Scan
Test Generation   → Interface Mode
```

**Rationale:** Token limits unlikely to be exceeded; prioritize completeness over optimization.

---

### Medium Codebase (20K-100K LOC)

**Default Strategy:** Selective compression based on use case

```
Use Case          → Configuration
─────────────────────────────────
Documentation     → Interface Mode
Bug Investigation → Full Context (may need module focus)
Architecture      → Interface Mode
Code Review       → Standard Compression or Interface Mode
Security Audit    → Full Context + Module Focus if needed
Test Generation   → Interface Mode
```

**Rationale:** Balance between context and token efficiency; use compression for overview tasks.

---

### Large Codebase (100K-500K LOC)

**Default Strategy:** Compression required, consider module splitting

```
Use Case          → Configuration
─────────────────────────────────
Documentation     → Interface Mode + Module Focus
Bug Investigation → Module-Specific Snapshots (full context per module)
Architecture      → Interface Mode
Code Review       → Interface Mode or Multi-Snapshot Approach
Security Audit    → Module-Specific Snapshots + Security Scan
Test Generation   → Interface Mode per module
```

**Rationale:** Full codebase likely exceeds token limits; require focused snapshots or compression.

---

### Very Large Codebase (500K+ LOC)

**Default Strategy:** Module-based snapshots required

```
Use Case          → Configuration
─────────────────────────────────
Documentation     → Interface Mode per service/module
Bug Investigation → Specific Module/Service Only (full context)
Architecture      → Interface Mode + High-Level Only
Code Review       → Module-by-Module Interface Snapshots
Security Audit    → Service/Module Snapshots + Security Scan
Test Generation   → Interface Mode per component
```

**Rationale:** Full codebase impossible to fit; require strategic slicing and progressive disclosure.

**Example Multi-Snapshot Approach:**
```bash
# Generate per-service snapshots
for service in api database frontend workers; do
  npx repomix \
    --config-override "{\"include\": [\"services/$service/**\"], \"compression\": {\"enabled\": true, \"keep_interfaces\": true}}" \
    --output "snapshots/${service}-interface.md"
done
```

---

## Format Selection Guide

### When to Use Markdown

**Best for:**
- Human readability priority
- Documentation generation
- Code review and analysis
- General LLM consumption

**Advantages:**
- Syntax highlighting in code blocks
- Clear section structure
- Readable in any text viewer
- Widely supported

**Use when:** Output will be read by humans or general-purpose LLMs.

---

### When to Use XML

**Best for:**
- Tool integration and automation
- Structured data extraction
- Machine parsing requirements
- Graph generation or visualization tools

**Advantages:**
- Strict structure for parsing
- Embedded metadata
- Hierarchical organization
- Standard schemas possible

**Use when:** Output will be consumed by tools or requires strict structure.

---

### When to Use Plain Text

**Best for:**
- Maximum compatibility
- Minimal token overhead
- Simple grep/search operations
- Configuration analysis

**Advantages:**
- No markup overhead
- Universal compatibility
- Clean separation
- Lightweight

**Use when:** Simple processing or maximum compatibility needed.

---

## Configuration Quick Reference

| Use Case | Compression | Format | Line# | Security | Token Impact |
|----------|-------------|--------|-------|----------|--------------|
| **Documentation** | Interface | Markdown | No | Optional | ⭐⭐ Low |
| **Bug Debug** | None | Markdown | Yes | No | ⭐⭐⭐⭐⭐ High |
| **Architecture** | Interface | Markdown | No | No | ⭐⭐ Low |
| **Review (High-Level)** | Interface | Markdown | No | Optional | ⭐⭐ Low |
| **Review (Deep)** | Standard | Markdown | Yes | Yes | ⭐⭐⭐⭐ Med-High |
| **Security Audit** | None | Markdown | Yes | Yes | ⭐⭐⭐⭐⭐ High |
| **Test Generation** | Interface | Markdown | No | No | ⭐⭐ Low |
| **Config Analysis** | Minimal | Plain | No | Yes | ⭐ Minimal |
| **Onboarding** | Interface | Markdown | No | No | ⭐⭐ Low |
| **Dependencies** | Minimal | Plain/XML | No | No | ⭐ Minimal |

---

## Common Scenarios Decision Matrix

### "I need to share this codebase with external consultant"

**Considerations:**
- Security scan is MANDATORY
- Consider interface mode to limit exposed implementation
- Verify no secrets before sharing

**Recommended:**
```bash
npx repomix \
  --config-override '{
    "compression": {"enabled": true, "keep_interfaces": true},
    "security": {"enable_security_check": true, "exclude_suspicious_files": true}
  }' \
  --output external-snapshot.md \
  --style markdown
```

---

### "I'm hitting token limits with my LLM"

**Solutions (in order of preference):**
1. Enable interface compression
2. Focus on specific modules using `include` patterns
3. Use minimal compression for high-level analysis
4. Split into multiple module-specific snapshots

**Recommended:**
```bash
# Try interface mode first
npx repomix --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' -o compressed.md

# If still too large, focus on module
npx repomix --config-override '{"include": ["src/core/**"], "compression": {"enabled": true, "keep_interfaces": true}}' -o core-module.md
```

---

### "I need to analyze a public GitHub repo"

**Recommended:**
```bash
npx repomix \
  --remote https://github.com/user/repo.git \
  --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' \
  --output repo-analysis.md
```

**Follow-up:** If interested in specific areas, clone and generate focused snapshots.

---

### "I'm preparing for a code review meeting"

**Recommended:**
```bash
# High-level overview for discussion
npx repomix \
  --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' \
  --output review-overview.md

# Plus detailed snapshot for reference
npx repomix \
  --config-override '{"compression": {"enabled": true, "keep_signatures": true}}' \
  --output review-detailed.md
```

**Strategy:** Use interface snapshot to drive discussion, detailed snapshot for drilling down.

---

### "I'm investigating a production bug under time pressure"

**Recommended:**
```bash
# Full context for the affected module
npx repomix \
  --config-override '{
    "include": ["src/module-with-bug/**"],
    "output": {"show_line_numbers": true}
  }' \
  --output urgent-debug.md
```

**Why:** Focus on relevant module, full implementation, line numbers for precise debugging.
