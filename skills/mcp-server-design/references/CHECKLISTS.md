# MCP Server Design Checklists

## Table of Contents
- [Pre-Design Checklist](#pre-design-checklist)
- [Tool Design Checklist](#tool-design-checklist)
- [Error Handling Checklist](#error-handling-checklist)
- [Documentation Checklist](#documentation-checklist)
- [Input Validation Checklist](#input-validation-checklist)
- [Agent UX Checklist](#agent-ux-checklist)
- [Testing Checklist](#testing-checklist)
- [Pre-Ship Checklist](#pre-ship-checklist)

---

## Pre-Design Checklist

Before writing any code, answer these questions:

### Domain Understanding
- [ ] What problem does this MCP server solve?
- [ ] Who are the target agents (Claude Code, Codex, Gemini CLI, etc.)?
- [ ] Is this single-agent or multi-agent coordination?
- [ ] What are the core workflows?

### Tool Clustering
- [ ] Can tools be grouped by workflow (≤7 per cluster)?
- [ ] What are the natural "primitives" vs "macros"?
- [ ] Which operations are read-only vs write?
- [ ] Which operations are idempotent?

### Failure Mode Analysis
- [ ] List 10 ways agents might misuse each tool
- [ ] What invalid inputs will they try?
- [ ] What implicit assumptions will they make?
- [ ] What state dependencies exist?

### Discovery Requirements
- [ ] How will agents discover valid parameter values?
- [ ] What resources should be exposed?
- [ ] Are there relationships between entities that need to be discoverable?

---

## Tool Design Checklist

For each tool:

### Parameters
- [ ] Required parameters minimized (can any be optional with defaults?)
- [ ] Optional parameters have sensible defaults
- [ ] Parameter names are self-documenting
- [ ] Types are precise (avoid `str` when enum is appropriate)
- [ ] Constraints are explicit in docstring

### Returns
- [ ] Return type is documented
- [ ] All fields are explained
- [ ] Example return value provided
- [ ] Error cases documented

### Idempotency
- [ ] Operation is idempotent OR clearly documented as not
- [ ] Safe to retry after transient failures
- [ ] Duplicate input behavior is defined

### Scope
- [ ] Tool does ONE thing well
- [ ] No hidden side effects
- [ ] Related operations are separate tools
- [ ] Macro tool exists for common multi-step workflows

---

## Error Handling Checklist

### ToolExecutionError Structure
- [ ] Every error has `error_type` (machine-parseable category)
- [ ] Every error has `message` (human-readable explanation)
- [ ] Every error has `recoverable` flag
- [ ] Every error has `data` payload with structured hints

### Data Payload Contents
- [ ] `provided`: The invalid input that was given
- [ ] `suggestions`: Similar valid options (fuzzy matched)
- [ ] `available`: List of all valid options (when small)
- [ ] `fix_hint`: Specific action to take
- [ ] `example_valid`: Working example value

### Error Types Coverage
- [ ] Input validation errors (INVALID_ARGUMENT, INVALID_TIMESTAMP)
- [ ] Intent detection errors (PROGRAM_NAME_AS_AGENT, BROADCAST_ATTEMPT)
- [ ] Lookup errors (NOT_FOUND, ALREADY_EXISTS)
- [ ] Configuration errors (CONFIGURATION_ERROR, AUTH_ERROR)
- [ ] Resource errors (FILE_RESERVATION_CONFLICT, RATE_LIMITED)

### Error Messages
- [ ] WHAT went wrong is clear
- [ ] WHY it's wrong is explained
- [ ] HOW to fix is actionable
- [ ] No stack traces exposed
- [ ] No generic "error occurred" messages

---

## Documentation Checklist

### Docstring Sections

Each tool docstring must include:

```
- [ ] Brief one-liner (front-loaded verb)
- [ ] Discovery section (how to find parameter values)
- [ ] When to use section (triggers for tool selection)
- [ ] Parameters section (NumPy style with constraints)
- [ ] Returns section (type and field descriptions)
- [ ] Do / Don't section (behavioral guidance)
- [ ] Examples section (JSON-RPC format, realistic values)
- [ ] Common mistakes section (pitfall avoidance)
- [ ] Idempotency section (retry safety)
```

### Discovery Section
- [ ] Every parameter with non-obvious values has discovery hint
- [ ] Resource URIs documented
- [ ] Related tool outputs mentioned
- [ ] Shell commands for dynamic values (e.g., `pwd`)

### Examples
- [ ] At least one simple example
- [ ] At least one complex example (optional parameters used)
- [ ] JSON-RPC format used
- [ ] Realistic values (not "X", "Y", "test")
- [ ] Comments explain non-obvious choices

### Do / Don't
- [ ] At least 3 "Do" items
- [ ] At least 3 "Don't" items
- [ ] Each item explains WHY
- [ ] Common anti-patterns addressed
- [ ] Best practices from production usage

---

## Input Validation Checklist

### Enforcement Modes
- [ ] `strict` mode available (reject with detailed error)
- [ ] `coerce` mode available (auto-fix when possible)
- [ ] `always_auto` mode available (ignore input, generate valid)
- [ ] Default mode is configurable
- [ ] Mode can be overridden per-call if appropriate

### Mistake Detection
- [ ] Program names detected (claude-code, codex-cli, cursor)
- [ ] Model names detected (gpt-4, opus, sonnet, llama)
- [ ] Email addresses detected
- [ ] Broadcast keywords detected (all, *, everyone)
- [ ] Descriptive role names detected (BackendWorker, Migrator)
- [ ] Unix usernames detected ($USER values)
- [ ] Placeholder values detected (YOUR_PROJECT, $PROJECT)

### Normalization
- [ ] Whitespace trimmed
- [ ] Case normalized where appropriate
- [ ] Special characters handled
- [ ] Length limits enforced
- [ ] Format standardized (e.g., PascalCase for names)

### Fuzzy Matching
- [ ] Similar options suggested on NOT_FOUND
- [ ] Similarity scores included in suggestions
- [ ] Minimum score threshold configured
- [ ] Reasonable limit on suggestions (3-5)

### Pre-computed Validation
- [ ] Valid value sets computed at module load
- [ ] O(1) lookup via frozenset/dict
- [ ] Wordlists available for partial matching

---

## Agent UX Checklist

### CLI Confusion Prevention
- [ ] Fake CLI stub installed in PATH
- [ ] All naming variations covered (kebab-case, snake_case)
- [ ] Clear message explaining MCP vs CLI usage
- [ ] Tool names listed in stub output
- [ ] Symlinks created for common typos

### Broadcast Prevention
- [ ] Broadcast keywords explicitly rejected
- [ ] Error explains WHY broadcast isn't supported
- [ ] Error includes available recipients
- [ ] Design philosophy documented

### Macro Tools
- [ ] Common multi-step workflows bundled
- [ ] Macro returns intermediate results for debugging
- [ ] Macro documents individual steps
- [ ] Macro suitable for smaller models (Haiku)

### Resources
- [ ] Entity lists exposed as resources
- [ ] Resources documented in tool Discovery sections
- [ ] Resource URIs are intuitive
- [ ] Resources return useful metadata

### State Management
- [ ] Expiration/TTL on long-lived state
- [ ] Background cleanup of expired resources
- [ ] Grace period before hard deletion
- [ ] Renewal mechanism for extending TTL

---

## Testing Checklist

### Mistake Detection Tests
- [ ] Test all known program names detected
- [ ] Test all known model patterns detected
- [ ] Test email format detection
- [ ] Test broadcast keyword detection
- [ ] Test descriptive name detection
- [ ] Test Unix username detection
- [ ] Test placeholder detection
- [ ] Test valid names NOT detected as mistakes

### Fuzzy Matching Tests
- [ ] Test exact match returns 1.0 score
- [ ] Test close typos return high score
- [ ] Test unrelated strings return low score
- [ ] Test case insensitivity
- [ ] Test limit parameter

### Error Payload Tests
- [ ] Test error_type is correct category
- [ ] Test message is descriptive
- [ ] Test recoverable flag is accurate
- [ ] Test data contains required fields
- [ ] Test suggestions are relevant

### Validation Mode Tests
- [ ] Test strict mode rejects invalid
- [ ] Test coerce mode auto-corrects
- [ ] Test always_auto ignores input
- [ ] Test mode configuration works

### Haiku Canary Test
- [ ] Test with Claude Haiku model
- [ ] Verify tool selection works
- [ ] Verify parameter inference works
- [ ] Verify error recovery works
- [ ] Document any Haiku-specific issues

### Integration Tests
- [ ] Test full workflow (register → use → cleanup)
- [ ] Test idempotency (call same tool twice)
- [ ] Test concurrent access (multiple agents)
- [ ] Test state expiration and cleanup

---

## Pre-Ship Checklist

### Error Handling
- [ ] Every error has `error_type`, `message`, `recoverable`, `data`
- [ ] `data` includes suggestions, fix_hint, available_options
- [ ] Fuzzy matching suggests alternatives on NOT_FOUND
- [ ] Mistake detectors catch program/model names, broadcast, etc.
- [ ] No generic errors ("Invalid input", "Error occurred")
- [ ] No stack traces exposed to agents

### Documentation
- [ ] Every tool has Do/Don't section
- [ ] Every tool has Examples with JSON-RPC format
- [ ] Every tool has Discovery section
- [ ] Common mistakes documented with fixes
- [ ] Idempotency documented for all tools
- [ ] README explains overall architecture

### Input Handling
- [ ] coerce mode auto-corrects invalid inputs
- [ ] strict mode provides detailed guidance
- [ ] Placeholders detected and rejected
- [ ] Case-insensitive matching where appropriate
- [ ] Pre-computed validation for O(1) lookup

### Agent UX
- [ ] Fake CLI stub installed for confused agents
- [ ] Macros bundle common multi-step workflows
- [ ] Broadcast explicitly prevented with explanation
- [ ] Resources expose discoverable data
- [ ] State has TTL and cleanup

### Testing
- [ ] Test with Haiku (canary for unclear APIs)
- [ ] Test mistake detection for all detector types
- [ ] Test fuzzy matching suggestions
- [ ] Test error payloads are machine-parseable
- [ ] Test all validation modes
- [ ] Test idempotency

### Security
- [ ] No command injection vulnerabilities
- [ ] No path traversal vulnerabilities
- [ ] Input length limits enforced
- [ ] Rate limiting implemented
- [ ] Authentication validated (if applicable)

### Performance
- [ ] Pre-computed validation sets used
- [ ] Database queries optimized
- [ ] Expensive operations are async
- [ ] Caching for frequently accessed data

---

## Quick Reference: The 7 Principles

| # | Principle | Verification |
|---|-----------|--------------|
| 1 | **Anticipate Intent** | Mistake detectors catch common errors |
| 2 | **Fail Helpfully** | Errors include suggestions and fix hints |
| 3 | **Intercept Early** | CLI stub, placeholder detection |
| 4 | **Forgive by Default** | Coerce mode auto-corrects |
| 5 | **Document for Agents** | Do/Don't, Discovery, Examples |
| 6 | **Scope Narrowly** | No broadcast, targeted tools |
| 7 | **Provide Macros** | Multi-step workflows bundled |

---

## Sign-Off Template

```markdown
# MCP Server Review: [Server Name]

## Reviewer: _______________
## Date: _______________

### Checklist Completion
- [ ] Pre-Design (N/A for existing servers)
- [ ] Tool Design: ___/___
- [ ] Error Handling: ___/___
- [ ] Documentation: ___/___
- [ ] Input Validation: ___/___
- [ ] Agent UX: ___/___
- [ ] Testing: ___/___
- [ ] Pre-Ship: ___/___

### Issues Found
1. ...
2. ...

### Recommendations
1. ...
2. ...

### Approval
- [ ] Ready to ship
- [ ] Needs revision (see issues)
```
