---
name: repomix-prompt-packet
description: Use when creating AI-optimized repository snapshots paired with sophisticated prompts for LLM consumption. Combines repomix configuration selection with prompt engineering to generate complete "prompt packets" for code analysis, documentation, debugging, or architectural planning.
skill_evolver:
  enabled: true
  version: 1.0.0
  log_path: ~/.config/lev/logs/skills.jsonl
  hooks:
    - on_invoke
    - on_fail
    - on_success
---

# Repomix Prompt Packet Generator

## Purpose

This skill guides the creation of comprehensive "prompt packets" - AI-optimized repository snapshots paired with engineered prompts that maximize LLM effectiveness. A prompt packet consists of three components:

1. **Repository snapshot** - Repomix-generated codebase consolidation
2. **Contextual prompt** - Engineered query optimized for the use case
3. **AI primer** - Context-setting information that guides model interpretation

## When to Use This Skill

Use this skill when:
- Preparing codebase context for AI-assisted analysis, refactoring, or documentation
- Creating comprehensive bug investigation packages for LLMs
- Generating architectural overviews for planning discussions
- Building reusable code context for recurring AI workflows
- Sharing codebase snapshots with team members or external AI assistants
- Optimizing repository context for specific LLM models or use cases

Do not use this skill for:
- Simple file concatenation (use basic repomix instead)
- Single-file analysis (read the file directly)
- Tasks where full repo context isn't beneficial

## Core Workflow

### Step 1: Analyze Intent and Use Case

Before generating a prompt packet, identify the specific use case. Ask clarifying questions if unclear:

- **What is the goal?** (e.g., "find bugs", "generate docs", "plan refactoring")
- **What scope is needed?** (entire codebase, specific modules, API layer only)
- **What format is preferred?** (markdown for readability, XML for structured parsing, plain text for compatibility)
- **Are there security concerns?** (private repo, sensitive data, credentials)
- **What LLM will consume this?** (Claude, GPT-4, Gemini - affects token optimization)

Map the use case to one of these primary patterns:
- **Documentation Generation** - Extract API signatures and generate comprehensive docs
- **Bug Investigation** - Provide full implementation context for debugging
- **Architectural Planning** - Overview of structure and patterns for design decisions
- **Code Review** - Comprehensive snapshot for quality assessment
- **Security Audit** - Complete codebase with security scanning enabled
- **Test Generation** - Interface-focused snapshot for test case creation
- **Onboarding** - Readable overview for new developers

### Step 2: Select Repomix Configuration

Based on the identified use case, select the appropriate repomix configuration. Consult `references/use-case-matrix.md` for detailed decision trees.

**Configuration Dimensions:**

1. **Compression Mode** (See `references/repomix-patterns.md` for details)
   - **None** - Full code for debugging/implementation
   - **Standard Mode** - Balanced compression for general use
   - **Interface Mode** - API signatures only for documentation
   - **Minimal Mode** - Maximum compression for config/constants focus

2. **Output Format**
   - **Markdown** - Best for human readability and general LLM consumption
   - **XML** - Structured parsing and tool integration
   - **Plain Text** - Maximum compatibility and minimal overhead

3. **Security Settings**
   - **Enable security check** - Always for repos with potential secrets
   - **Exclude suspicious files** - Recommended for shared snapshots

4. **Line Numbers**
   - **Enable** - For debugging and code review use cases
   - **Disable** - For cleaner documentation generation

**Quick Reference Commands:**

```bash
# Documentation Generation (Interface Mode)
npx repomix --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' --output api-docs.md --style markdown

# Bug Investigation (Full Context)
npx repomix --output debug-context.md --style markdown --config-override '{"output": {"show_line_numbers": true}}'

# Architectural Overview (Interface Mode + Markdown)
npx repomix --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' --output architecture.md --style markdown

# Security Audit (Full + Security Scan)
npx repomix --config-override '{"security": {"enable_security_check": true}}' --output security-review.md --style markdown

# Code Review (Standard Compression)
npx repomix --config-override '{"compression": {"enabled": true, "keep_signatures": true}}' --output review.md --style markdown

# Test Generation (Interface Focus)
npx repomix --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' --output test-context.md --style markdown
```

### Step 3: Generate the Repository Snapshot

Execute the selected repomix command to generate the snapshot. Verify the output:

1. **Check token count** - Ensure it fits within target LLM context window
2. **Verify security** - Review for any accidentally included secrets
3. **Validate structure** - Confirm all expected files are included
4. **Test readability** - Spot-check formatting and organization

If the output exceeds token limits:
- Enable or increase compression
- Use `includePaths` to focus on specific directories
- Generate multiple focused snapshots for different modules

### Step 4: Engineer the Contextual Prompt

Craft a sophisticated prompt that maximizes LLM effectiveness. Consult `references/prompt-engineering.md` for detailed patterns.

**Prompt Engineering Framework:**

1. **Context Primer** (2-3 sentences)
   - Explain what the codebase does
   - Mention key technologies/frameworks
   - Identify any unusual patterns or architecture

2. **Task Specification** (Clear and specific)
   - State the exact goal
   - Define scope and boundaries
   - Specify output format expectations

3. **Constraints and Preferences** (When relevant)
   - Coding standards to follow
   - Patterns to maintain
   - Things to avoid

4. **Guidance for Analysis** (Optional but powerful)
   - Suggest analysis approach
   - Highlight areas to focus on
   - Request specific deliverables

**Example Prompts by Use Case:**

**Documentation Generation:**
```
This codebase is a TypeScript REST API built with Express.js and PostgreSQL.
It follows a layered architecture with routes, controllers, services, and repositories.

Based on the provided repository snapshot, generate comprehensive API documentation
that includes:
1. All available endpoints with HTTP methods
2. Request/response schemas with examples
3. Authentication requirements
4. Error codes and handling

Focus on the public API surface. Organize documentation by resource type
(Users, Projects, etc.). Use OpenAPI 3.0 specification format.
```

**Bug Investigation:**
```
This is a React frontend application using Redux for state management and
React Router for navigation. We recently migrated from v5 to v6 of React Router.

I'm experiencing an issue where navigation to /dashboard results in a blank screen
with console error: "Cannot read property 'user' of undefined". This started after
the router migration.

Analyze the codebase to:
1. Identify where the error originates
2. Trace the data flow for the 'user' property
3. Explain what changed with the router migration that caused this
4. Suggest a fix with code examples

Pay special attention to:
- Redux selectors and state structure
- Route component prop handling
- Component lifecycle and data fetching
```

**Architectural Planning:**
```
This monolithic Node.js application handles user authentication, content management,
and payment processing. It's becoming difficult to maintain and deploy.

Review the architecture and provide:
1. Analysis of current coupling points and dependencies
2. Suggested microservice boundaries with justification
3. Migration strategy prioritizing low-risk extractions first
4. Data consistency considerations for the suggested boundaries

Consider: we have 500K active users and can't afford downtime during migration.
```

### Step 5: Assemble the Prompt Packet

Combine the snapshot and prompt into a complete package. The typical structure:

```markdown
# Prompt Packet: [Use Case Description]

## Context Primer
[2-3 sentences about the codebase]

## Task
[Detailed task specification with constraints]

## Repository Snapshot
[Paste the repomix-generated content here]

## Expected Output
[Specific deliverables and format]
```

**Delivery Options:**

1. **Single File** - Combine prompt + snapshot in one markdown file
2. **Separate Files** - Keep prompt.md and repo-snapshot.md separate
3. **Gist/Paste** - Upload to GitHub Gist or pastebin for easy sharing
4. **Direct LLM Input** - Copy/paste directly into AI interface

### Step 6: Optimize and Iterate

After using the prompt packet with an LLM:

1. **Evaluate effectiveness** - Did the LLM understand the context?
2. **Check token efficiency** - Was the snapshot size appropriate?
3. **Assess prompt clarity** - Were outputs aligned with expectations?
4. **Refine for reuse** - Save successful patterns for similar tasks

If results aren't optimal:
- Adjust compression settings for better context
- Refine prompt engineering for clearer guidance
- Split large snapshots into focused modules
- Add more specific constraints or examples

## Advanced Techniques

### Multi-Snapshot Workflows

For large codebases, create specialized snapshots:

```bash
# Backend API snapshot
npx repomix --config-override '{"include": ["src/api/**", "src/services/**"]}' --output backend-api.md

# Frontend UI snapshot
npx repomix --config-override '{"include": ["src/components/**", "src/pages/**"]}' --output frontend-ui.md

# Database layer snapshot
npx repomix --config-override '{"include": ["src/models/**", "migrations/**"]}' --output database.md
```

Then craft prompts that reference multiple snapshots:
```
I'm providing three repository snapshots from our application:
1. backend-api.md - REST API implementation
2. frontend-ui.md - React component library
3. database.md - Data models and schema

Analyze how authentication flows across these layers and identify
potential security vulnerabilities in the integration points.
```

### Progressive Disclosure Pattern

Start with high-level overview, then drill down:

```bash
# Step 1: Interface-only overview
npx repomix --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' --output overview.md

# Step 2: After identifying area of interest, full implementation
npx repomix --config-override '{"include": ["src/auth/**"]}' --output auth-detailed.md
```

### Remote Repository Analysis

Analyze repositories without cloning:

```bash
npx repomix --remote https://github.com/user/repo.git --output remote-analysis.md
```

Useful for:
- Evaluating open-source libraries before adoption
- Studying reference implementations
- Competitive analysis

### Configuration Templates

Create reusable `repomix.config.json` files for recurring patterns:

**docs-generation.config.json:**
```json
{
  "output": {
    "file_path": "api-docs.md",
    "style": "markdown",
    "show_line_numbers": false
  },
  "compression": {
    "enabled": true,
    "keep_interfaces": true
  }
}
```

Use with: `npx repomix --config docs-generation.config.json`

## Integration with Other Skills

This skill pairs well with:
- **brainstorming** - Use prompt packets to inform design discussions
- **systematic-debugging** - Provide comprehensive context for bug investigation
- **writing-plans** - Generate architectural snapshots for implementation planning
- **code-reviewer** - Create review-ready codebase packages

## Common Pitfalls to Avoid

1. **Over-compression** - Don't compress so much that critical context is lost
2. **Under-engineering prompts** - Generic prompts get generic results; be specific
3. **Ignoring security** - Always scan for secrets before sharing snapshots
4. **Token blindness** - Check token counts before assuming full context fits
5. **One-size-fits-all** - Different use cases need different configurations
6. **Forgetting context primer** - LLMs benefit from architectural overview first
7. **Skipping validation** - Always verify snapshot includes expected files

## Quality Checklist

Before delivering a prompt packet, verify:

- [ ] Use case clearly identified and appropriate for full-repo context
- [ ] Repomix configuration matches use case requirements
- [ ] Snapshot successfully generated and validated
- [ ] Token count fits within target LLM context window
- [ ] Security check performed (if applicable)
- [ ] Prompt includes context primer, task specification, and constraints
- [ ] Expected output format clearly defined
- [ ] Prompt packet assembled and ready for delivery

## Quick Start Examples

**"I need to document our API"**
```bash
npx repomix --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' --output api.md

# Then use prompt:
"This is a [framework] API. Generate OpenAPI 3.0 documentation covering all endpoints,
request/response schemas, and authentication. Organize by resource type."
```

**"Help me debug this error"**
```bash
npx repomix --output debug.md --config-override '{"output": {"show_line_numbers": true}}'

# Then use prompt:
"Error: [exact error message]. This happens when [reproduction steps].
Analyze the codebase to identify root cause and suggest fix."
```

**"Plan a refactoring"**
```bash
npx repomix --config-override '{"compression": {"enabled": true, "keep_interfaces": true}}' --output refactor.md

# Then use prompt:
"Review this architecture for [specific goal: microservices, clean architecture, etc.].
Suggest refactoring approach with migration strategy."
```

## Additional Resources

- `references/repomix-patterns.md` - Comprehensive command patterns and configuration options
- `references/prompt-engineering.md` - Advanced prompt engineering techniques for code analysis
- `references/use-case-matrix.md` - Decision trees for configuration selection
