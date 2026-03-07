# Guard — Spec Guard Reference

Full pattern library for detecting underspecified inputs. Merges the Trail of Bits 6-category audit checklist with structured interview frameworks (SCAMPER, First Principles, Systems Thinking).

---

## Core Principle

**Garbage in, garbage out.** Most agent failures trace to underspecified inputs, not bad reasoning. Guard catches gaps *before* execution, not after.

---

## 6 Detection Categories

### 1. Objective (Weight: 20%)

**What we're checking:** Is there a clear, measurable outcome?

| Signal | Score | Example |
|--------|-------|---------|
| Explicit goal with success metric | PRESENT (0%) | "Reduce login time to <2s" |
| Implicit goal, inferable | PARTIAL (10%) | "Make login faster" |
| No stated goal | MISSING (20%) | "Fix the login" |

**Question template:**
```
What specific outcome do you need?
  Context: Without a clear objective, we risk solving the wrong problem.
  Options:
    a. {Inferred objective from context}
    b. {Alternative interpretation}
    c. Let me describe it differently
  Default: {Best inference from input}
```

**Interview frameworks for Objective:**
- **First Principles:** What is the fundamental problem being solved?
- **Jobs to Be Done:** What job is the user hiring this solution for?
- **Theory of Constraints:** What is the one bottleneck this must address?

---

### 2. Scope (Weight: 20%)

**What we're checking:** Are boundaries defined? What's in/out?

| Signal | Score | Example |
|--------|-------|---------|
| Explicit in/out boundaries | PRESENT (0%) | "Only the /api/auth endpoints, not UI" |
| Partial boundaries, some ambiguity | PARTIAL (10%) | "The auth system" |
| No boundaries stated | MISSING (20%) | "Add auth" |

**Question template:**
```
What's included and what's excluded?
  Context: Unbounded scope leads to unbounded work.
  Options:
    a. {Narrow scope: specific files/components}
    b. {Medium scope: feature area}
    c. {Broad scope: system-wide}
  Default: {Narrowest reasonable interpretation}
```

**Interview frameworks for Scope:**
- **SCAMPER — Eliminate:** What can we explicitly exclude?
- **Systems Thinking:** Where are the system boundaries?
- **Cynefin:** Is this scope simple, complicated, complex, or chaotic?

---

### 3. Constraints (Weight: 15%)

**What we're checking:** Technical, time, budget, compatibility limits?

| Signal | Score | Example |
|--------|-------|---------|
| Explicit constraints listed | PRESENT (0%) | "Must work with Node 18+, no new deps" |
| Some constraints implied | PARTIAL (7.5%) | "Keep it simple" |
| No constraints mentioned | MISSING (15%) | (silence) |

**Question template:**
```
Any constraints I should know about?
  Context: Hidden constraints cause rework. Better to surface them now.
  Areas to consider:
    - Technology: language, framework, version requirements
    - Compatibility: backward compat, existing API contracts
    - Performance: latency, throughput, memory budgets
    - Time: deadline, phasing requirements
    - Dependencies: what can/can't we change
  Default: {Infer from project context: package.json, tsconfig, etc.}
```

**Interview frameworks for Constraints:**
- **Theory of Constraints:** What is the binding constraint?
- **TRIZ:** What contradictions exist between desired properties?
- **Six Thinking Hats — Black Hat:** What are the risks and limitations?

---

### 4. Environment (Weight: 15%)

**What we're checking:** Where does this run? What already exists?

| Signal | Score | Example |
|--------|-------|---------|
| Environment specified | PRESENT (0%) | "Next.js 14 app, Vercel deployment, Postgres" |
| Partial environment | PARTIAL (7.5%) | "It's a web app" |
| No environment info | MISSING (15%) | (silence) |

**Question template:**
```
What's the current environment?
  Context: Solutions differ drastically by environment.
  I can detect:
    - package.json → framework + deps
    - tsconfig.json → TypeScript config
    - .env → service connections
    - Dockerfile → deployment target
  Detected: {auto-detected environment summary}
  Anything to add or correct?
  Default: {Use auto-detected environment}
```

**Auto-detection strategy:**
```bash
# Detect framework
[ -f package.json ] && jq -r '.dependencies | keys[]' package.json 2>/dev/null | head -5
[ -f requirements.txt ] && head -5 requirements.txt
[ -f Cargo.toml ] && grep -A5 '\[dependencies\]' Cargo.toml | head -5

# Detect deployment
[ -f Dockerfile ] && echo "Docker"
[ -f vercel.json ] && echo "Vercel"
[ -f fly.toml ] && echo "Fly.io"
[ -d .github/workflows ] && echo "GitHub Actions CI"
```

**Interview frameworks for Environment:**
- **Systems Thinking:** What adjacent systems interact with this?
- **McKinsey 7S — Systems:** What processes and tools support this?

---

### 5. Dependencies (Weight: 15%)

**What we're checking:** What must exist first? What else breaks if this changes?

| Signal | Score | Example |
|--------|-------|---------|
| Dependencies mapped | PRESENT (0%) | "Depends on user-service PR #42 being merged" |
| Some deps mentioned | PARTIAL (7.5%) | "After the API is ready" |
| No deps discussed | MISSING (15%) | (silence) |

**Question template:**
```
What does this depend on, and what depends on it?
  Context: Dependency blindness causes cascade failures.
  Upstream: What must be done/exist before this?
  Downstream: What breaks or changes because of this?
  Default: {Infer from imports, API calls, config references}
```

**Dependency detection:**
```bash
# Import graph (TypeScript)
rg "^import .* from ['\"]" --glob="*.ts" --glob="*.tsx" | head -20

# API calls
rg "fetch\(|axios\.|http\." --glob="*.ts" --glob="*.tsx" | head -10

# Config references
rg "process\.env\.|config\." --glob="*.ts" | head -10
```

**Interview frameworks for Dependencies:**
- **Systems Thinking:** Map the causal loops
- **First Principles:** What are the atomic dependencies?
- **Ladder of Inference:** Are we assuming dependencies that don't exist?

---

### 6. Success Criteria (Weight: 15%)

**What we're checking:** How do we know it's done? How do we know it's correct?

| Signal | Score | Example |
|--------|-------|---------|
| Measurable criteria | PRESENT (0%) | "Tests pass, <200ms p95 latency, no regressions" |
| Vague criteria | PARTIAL (7.5%) | "It should work" |
| No criteria stated | MISSING (15%) | (silence) |

**Question template:**
```
How will we know this is done and correct?
  Context: Without criteria, "done" is subjective.
  Consider:
    - Tests: what should pass?
    - Performance: what are the thresholds?
    - User experience: what should the user see?
    - Regression: what must NOT break?
  Default: {Existing tests pass + no type errors + builds clean}
```

**Interview frameworks for Success Criteria:**
- **Jobs to Be Done:** What does "hired successfully" look like?
- **Design Thinking — Test:** How would we validate this with users?
- **Stoicism:** What is within our control to verify?

---

## Scoring Algorithm

```
underspec_score = 0
for each category:
  if MISSING:  underspec_score += full_weight
  if PARTIAL:  underspec_score += half_weight
  if PRESENT:  underspec_score += 0

# Thresholds
if underspec_score > 60%: BLOCK — too vague to proceed
if underspec_score > 30%: WARN — ask missing categories
if underspec_score ≤ 30%: PASS — sufficient spec
```

## Confidence Integration

Guard score feeds into the work FSM's confidence routing:

```
Guard score 0-30%   → Confidence boost: +0.2
Guard score 30-60%  → Confidence neutral: +0
Guard score 60-100% → Confidence penalty: -0.3
```

---

## Resume Logic

When a guard session is interrupted:

```
1. Save current state:
   - Categories scored so far
   - Questions asked + answers received
   - Remaining categories
   - Current underspec_score

2. On resume, detect saved state:
   - "I see a previous guard session for '{topic}' with score {n}%."
   - "Categories still missing: {list}. Continue?"

3. Resume from last incomplete category
```

---

## Integration with Interview Frameworks

Guard can leverage the interview skill's framework library for deeper exploration:

| Guard Category | Recommended Frameworks |
|---------------|----------------------|
| Objective | First Principles, Jobs to Be Done, Theory of Constraints |
| Scope | SCAMPER (Eliminate), Systems Thinking, Cynefin |
| Constraints | Theory of Constraints, TRIZ, Six Hats (Black) |
| Environment | Systems Thinking, McKinsey 7S |
| Dependencies | Systems Thinking, First Principles, Ladder of Inference |
| Success Criteria | Jobs to Be Done, Design Thinking (Test), Stoicism |

**Usage:** When a category scores MISSING and the user wants deeper exploration:
```
"Let me explore your {category} using {framework}..."
→ Switch to interview-style questioning for that category
→ Return to guard scoring when category is resolved
```

---

## Quick Reference Card

```
🛡️ GUARD — 6 checks, 30 seconds

1. Objective?   — What outcome?
2. Scope?       — What's in/out?
3. Constraints? — What limits?
4. Environment? — Where does it run?
5. Dependencies?— What connects?
6. Success?     — How do we know?

Score ≤ 30% → GO
Score > 30% → ASK
Score > 60% → STOP
```
