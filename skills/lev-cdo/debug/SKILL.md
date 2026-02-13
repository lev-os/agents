---
name: lev-cdo-debug
description: |
  [WHAT] 7-step systematic Root Cause Analysis (RCA) workflow for debugging
  [HOW] REPRODUCE → ISOLATE → TRACE → HYPOTHESIZE → VERIFY → FIX → VALIDATE
  [WHEN] Triggered by "uld" or "ultradebug" keywords, or explicit debug request
  [WHY] Structured debugging prevents guess-and-check, ensures minimal fixes

  Triggers: "uld", "ultradebug", "debug rca", "root cause analysis"
skill_type: workflow
category: process-debug

lifecycle_integration:
  stage: execution
  input_artifact: bug report or error description
  output_artifact: FINAL-validation.md (fix + verification)

related_skills:
  - skill://lev-ultra        # Routes ultra-mode keywords to this skill
  - skill://lev-find         # Legacy skill name (`lev get` backend used in TRACE phase)
  - skill://ralph            # Adversarial validation in VALIDATE phase

plankton: false
---

# CDO Debug - Root Cause Analysis Workflow

## Lev Concept

**What is this?**
A 7-step systematic debugging workflow that prevents guess-and-check and ensures minimal, targeted fixes. Each step builds evidence, narrows scope, and validates hypotheses before applying fixes.

**Why does it exist?**
Debugging without structure leads to:
- Fixing symptoms instead of root causes
- Scope creep (refactoring while debugging)
- Regression introduction
- Lost time on wrong hypotheses

**When to use it:**
- Complex bugs with unknown root cause
- Intermittent failures
- Multi-component system failures
- When "uld" or "ultradebug" keywords appear in user request

---

## CLI Commands

### Primary Command

```bash
# Invoke debug RCA workflow
lev cdo debug "{error description}"

# Triggered automatically by keywords
lev ultra "uld fix the gateway crash"
```

### Workflow Structure

```
workflow: debug-rca
complexity: deep
turns: 7
convergence:
  type: turn_count
  required_turns: 7
  exit_condition: "All turns complete + PASS verdict"
```

---

## Workflows

### Debug RCA - 7-Step Systematic Analysis

**Workflow structure:**

```
tmp/debug-rca-<timestamp>/
├── 00-input.md              # Error description
├── 01-reproduce.md          # REPRODUCE step
├── 02-isolate.md            # ISOLATE step
├── 03a-call-path.md         # TRACE step (agent A)
├── 03b-working-code.md      # TRACE step (agent B)
├── 04-hypotheses.md         # HYPOTHESIZE step
├── 05-verified.md           # VERIFY step
├── 06-fix.md                # FIX step
└── FINAL-validation.md      # VALIDATE step
```

---

### Turn 1: REPRODUCE

**Goal:** Define exact failure condition

**Agent:** define-failure

**Prompt:**
```
Define exact failure condition:
- Error message/behavior
- Steps to reproduce
- Expected vs actual
- Environment details
```

**Output:** 01-reproduce.md

**Example:**
```yaml
error: "Gateway crashes on Telegram message"
steps_to_reproduce:
  1. Send message to Telegram bot
  2. Gateway receives webhook
  3. Crash with "Cannot read property 'text' of undefined"
expected: Message processed successfully
actual: Process crashes, restarts
environment:
  - Node.js v20.11.0
  - clawdbot@latest
  - macOS 14.2
```

---

### Turn 2: ISOLATE

**Goal:** Narrow to smallest failing case

**Agent:** narrow-scope

**Input:** 01-reproduce.md

**Prompt:**
```
Narrow to smallest failing case:
- Minimal reproduction
- Isolated variables
- Boundary identification
```

**Output:** 02-isolate.md

**Example:**
```yaml
minimal_repro:
  - ANY Telegram message triggers crash
  - Does NOT happen with WhatsApp messages
  - Happens even with empty message body

isolated_variables:
  - Message source: Telegram (fails) vs WhatsApp (works)
  - Message content: irrelevant
  - Gateway plugin: telegram-plugin.ts

boundary:
  - Crash occurs in handleTelegramWebhook() function
  - Line: message.text.toLowerCase()
  - Condition: message.text is undefined for some messages
```

---

### Turn 3: TRACE (Parallel)

**Goal:** Find call path + working code comparison

**Agents:** 2 parallel (Explore subagents)

#### Agent A: Find Call Path

**Input:** 02-isolate.md

**Prompt:** "Find call path for failing code using lev-find"

**Output:** 03a-call-path.md

**Example:**
```yaml
call_path:
  1. telegram-webhook-handler.ts:42 (entry)
  2. plugins/telegram-plugin.ts:89 (handleTelegramWebhook)
  3. message.text.toLowerCase() (CRASH HERE)

file_locations:
  - vendor/clawdbot/src/plugins/telegram-plugin.ts:89
  - vendor/clawdbot/src/handlers/telegram-webhook-handler.ts:42
```

#### Agent B: Find Working Code

**Prompt:** "Find similar code that works using lev-find"

**Output:** 03b-working-code.md

**Example:**
```yaml
working_code_found:
  - plugins/whatsapp-plugin.ts:67
  - Uses optional chaining: message.text?.toLowerCase()

difference:
  telegram: message.text.toLowerCase()  # UNSAFE
  whatsapp: message.text?.toLowerCase() # SAFE
```

---

### Turn 4: HYPOTHESIZE

**Goal:** Form 2-3 theories about root cause

**Agent:** root-cause-theories

**Input:** ["03a-call-path.md", "03b-working-code.md"]

**Prompt:**
```
Form 2-3 theories about root cause:
- Theory 1: {hypothesis}
  Evidence FOR: {file:line}
  Evidence AGAINST: {file:line}
- Theory 2: ...
- Theory 3: ...
```

**Output:** 04-hypotheses.md

**Example:**
```yaml
theory_1:
  hypothesis: "Telegram sends messages without text field (stickers, images)"
  evidence_for:
    - whatsapp-plugin.ts:67 uses optional chaining
    - Telegram API docs: text field optional
  evidence_against:
    - None

theory_2:
  hypothesis: "message object is undefined"
  evidence_for:
    - Error message suggests undefined access
  evidence_against:
    - Would crash earlier if message was undefined

theory_3:
  hypothesis: "Race condition in message parsing"
  evidence_for:
    - None
  evidence_against:
    - Happens consistently, not intermittently

verdict: Theory 1 most likely (95% confidence)
```

---

### Turn 5: VERIFY

**Goal:** Test each hypothesis with evidence

**Agent:** hypothesis-testing

**Input:** 04-hypotheses.md

**Prompt:**
```
Test each hypothesis with evidence:
- Check git blame/history
- Add minimal logging
- Run targeted tests
Verdict: Theory {N} confirmed/refuted
```

**Output:** 05-verified.md

**Example:**
```yaml
theory_1_test:
  method: "Check Telegram API docs + git blame"
  result: CONFIRMED
  evidence:
    - Telegram API: text field is optional
    - Git blame: telegram-plugin.ts:89 never had null check
    - WhatsApp plugin: added optional chaining 3 months ago (commit a3f8e9)

theory_2_test:
  method: "Add console.log before crash"
  result: REFUTED
  evidence:
    - message object exists
    - message.text is undefined for sticker/image messages

theory_3_test:
  result: REFUTED (not tested, inconsistent with evidence)

verdict: Theory 1 CONFIRMED - missing optional chaining for message.text
```

---

### Turn 6: FIX

**Goal:** Apply MINIMAL fix for root cause

**Agent:** minimal-fix

**Input:** 05-verified.md

**Prompt:**
```
Apply MINIMAL fix for root cause:
- ONLY fix the root cause
- NO scope creep
- NO refactoring
- Document what changed
```

**Output:** 06-fix.md

**Example:**
```yaml
root_cause: "Missing optional chaining on message.text"

fix:
  file: vendor/clawdbot/src/plugins/telegram-plugin.ts
  line: 89
  before: |
    const command = message.text.toLowerCase();
  after: |
    const command = message.text?.toLowerCase();

  scope: MINIMAL (1 line change)
  refactoring: NONE
  additional_changes: NONE

justification: |
  Matches working pattern in whatsapp-plugin.ts:67.
  Handles optional text field per Telegram API spec.
```

---

### Turn 7: VALIDATE

**Goal:** Adversarial validation of fix

**Agent:** ralph-verify (adversarial validation)

**Input:** "all" (reads 00-06)

**Prompt:**
```
Adversarial validation:
- Original issue resolved?
- Tests pass?
- No regression introduced?
- Physical evidence exists?
VERDICT: PASS/FAIL with file:line evidence
```

**Output:** FINAL-validation.md

**Example:**
```yaml
validation:
  original_issue_resolved: YES
    evidence: "Sent sticker to Telegram bot - no crash"

  tests_pass: YES
    evidence: "pnpm test passes (42/42)"

  regression_check: PASS
    evidence: "Text messages still work, WhatsApp unchanged"

  physical_evidence: YES
    evidence: |
      File: vendor/clawdbot/src/plugins/telegram-plugin.ts:89
      Git diff shows 1-line change (optional chaining added)

verdict: PASS

adversarial_critique:
  - "Why not add null check instead of optional chaining?"
    response: "Optional chaining is idiomatic, matches WhatsApp plugin pattern"
  - "Should we add error logging?"
    response: "Out of scope - minimal fix only"
  - "What about other message.* accesses?"
    response: "Not in scope - only fixing reported crash"

final_verdict: FIX APPROVED - Deploy to production
```

---

## Convergence Criteria

**Type:** Turn count (fixed structure)

**Exit conditions:**
- All 7 turns complete
- FINAL-validation.md exists
- Verdict: PASS

**Safety checks:**
- If verdict = FAIL → Report blocker, do NOT deploy
- If missing turn output → Report incomplete workflow
- If fix scope > 10 lines → Escalate (not minimal)

---

## Integration with lev-ultra

**Router:** lev-ultra skill routes ultra-mode keywords

**Trigger mapping:**
```yaml
keywords:
  - "uld" → lev-cdo/debug (this skill)
  - "ult" → lev-cdo (main CDO)
  - "ulr" → lev-research
  - "ulw" → planning + ralph
```

**Example:**
```bash
# User input
"uld fix the gateway crash"

# lev-ultra routes to
lev cdo debug "fix the gateway crash"

# Which invokes this 7-step workflow
```

---

## Anti-Patterns to Avoid

| Don't | Do Instead |
|-------|------------|
| Fix symptoms without root cause | Complete all 7 turns |
| Refactor while debugging | Minimal fix only (1-10 lines) |
| Skip hypothesis testing | VERIFY step required |
| Deploy without validation | VALIDATE step must PASS |
| Guess-and-check debugging | Evidence-based hypotheses |

---

## Relates

### Depends On
- `skill://lev-find` - Used in TRACE step to find code (legacy skill name for `lev get` backend)
- `skill://lev-ultra` - Routes "uld" keyword to this skill

### Works With
- `skill://ralph` - Adversarial validation in VALIDATE step
- `skill://lev-cdo/workflows` - Uses Deep workflow pattern

### Blocks/Enables
- Blocks: Deployment if validation FAIL
- Enables: Systematic debugging without scope creep

### Lifecycle Position
- **Before:** Bug report or error description
- **After:** FINAL-validation.md → deployment or escalation
- **Parallel:** None (sequential 7-step process)

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for debug, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
