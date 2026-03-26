# Anti-Patterns

> What NOT to do when extracting skills from session history.

---

## The Meta Anti-Pattern

**Summarizing instead of extracting.**

Your session history is not a story to summarize. It's a corpus of evidence for a **generative grammar**. The goal is to find the rules that PRODUCED your behaviors, not to describe the behaviors themselves.

```
WRONG: "I often run tests before committing"
RIGHT: "When preparing to publish code, always validate it first"
```

The first is an observation. The second is a rule that generates behavior.

---

## Extraction Anti-Patterns

### 1. First Hypothesis Lock-In

**Pattern:** Committing to the first generalization that fits.

**Why it fails:** First hypotheses are often the most obvious, not the most accurate. You miss deeper patterns.

**The fix:** Always generate 3+ hypotheses (⊟) before selecting.

```
# WRONG
Instance: "Added error handling to API call"
Hypothesis: "Always add error handling"
Done!

# RIGHT
Instance: "Added error handling to API call"
Hypotheses:
  1. "Always add error handling"
  2. "External calls need error boundaries"
  3. "Failure modes must be explicit at system boundaries"
Select: #3 (most generalizable, covers more cases)
```

---

### 2. Project-Specific Leakage

**Pattern:** The extracted skill contains project names, file paths, or domain-specific terms.

**Why it fails:** The skill won't transfer to other projects.

**The fix:** Strip all specifics during transformation. Ask: "Would this make sense to someone who's never seen this project?"

```
# WRONG
"When editing the UserAuth component, always check the JWT token"

# RIGHT
"When editing authentication components, always verify token validity"
```

---

### 3. Over-Generalization

**Pattern:** The rule is so broad it's useless.

**Why it fails:** If a rule applies to everything, it tells you nothing.

**The fix:** Add scope constraints. Use counter-examples to narrow.

```
# WRONG
"Always validate input"

# RIGHT
"Validate input at system boundaries (API endpoints, file readers, user forms).
Don't validate between trusted internal components."
```

---

### 4. Counter-Example Avoidance

**Pattern:** Ignoring or explaining away instances that don't fit the rule.

**Why it fails:** The rule is wrong. Counter-examples are signal, not noise.

**The fix:** If counter-examples exceed 20%, kill the generalization (†) and restart.

```
# WRONG
Rule: "Always use async for API calls"
Counter-example: "But in this case sync was better because..."
Counter-example: "But here async caused problems because..."
Conclusion: "The rule is fine, these are just exceptions"

# RIGHT
Rule: "Always use async for API calls"
Counter-example count: 4/15 (27%)
Conclusion: Rule is wrong. Kill it. Find a better one.
```

---

### 5. Convergence Blindness

**Pattern:** Not tracking whether refinements are actually improving.

**Why it fails:** You can refine forever without getting closer to a good skill.

**The fix:** Measure convergence signals. If score isn't improving, stop and diagnose.

```
# WRONG
Round 5: "This is better!"
Round 6: "This is better!"
Round 7: "This is better!"
(No metrics, just vibes)

# RIGHT
Round 5: Score 0.62, changes: 4
Round 6: Score 0.68, changes: 2
Round 7: Score 0.71, changes: 1
(Measurable progress, converging)
```

---

### 6. Ritual Without Understanding

**Pattern:** Extracting a ritual just because it's frequent, without understanding WHY it works.

**Why it fails:** The skill has no predictive power. You can't tell when NOT to use it.

**The fix:** The "Why This Works" section is mandatory. If you can't explain it, you don't understand it.

```
# WRONG
Ritual: "run cargo clippy" (47 times)
Skill: "Run cargo clippy"
(No explanation)

# RIGHT
Ritual: "run cargo clippy" (47 times)
Skill: "Run cargo clippy before implementing changes"
Why: "Clippy catches issues faster than the compiler. Running it first
      means you fix issues once, not after building solutions on top of them."
```

---

### 7. Phantom Patterns

**Pattern:** Seeing patterns that aren't really there (low count, coincidence).

**Why it fails:** You're extracting noise, not signal.

**The fix:** Minimum 5 instances, preferably 10+. Use pilot (⚡) to test.

```
# WRONG
Found 2 instances of "check accessibility"
Conclusion: "Accessibility checking is my methodology!"

# RIGHT
Found 2 instances of "check accessibility"
Conclusion: Count too low. Add to watch list. Revisit when count >= 5.
```

---

### 8. Training Data Overfitting

**Pattern:** The skill works perfectly on extraction instances but fails on new problems.

**Why it fails:** The skill memorized specifics instead of learning the pattern.

**The fix:** Always test on NEW instances (Axiom 2: Understanding = Ability to Reproduce).

```
# WRONG
Extracted from 10 instances
Tested on: those same 10 instances
Result: 100% accuracy!
(Overfitted)

# RIGHT
Extracted from 10 instances
Tested on: 5 NEW instances
Result: 3/5 work, 2/5 fail
Action: Refine skill to handle failing cases
```

---

## Mining Anti-Patterns

### 9. Index Staleness

**Pattern:** Searching with an outdated index.

**Why it fails:** Recent sessions aren't included. You miss current patterns.

**The fix:** Always run `cass index --json` before mining.

---

### 10. Workspace Mismatch

**Pattern:** Getting 0 results because workspace path is wrong.

**Why it fails:** Paths are case-sensitive and must be exact.

**The fix:** Use `--aggregate workspace` to discover exact paths first.

```bash
# WRONG
cass search "*" --workspace /data/projects/MyProject  # Case wrong

# RIGHT
cass search "*" --aggregate workspace --limit 1 --json  # Discover paths
# Then use exact path from aggregation
```

---

### 11. Full Output Overload

**Pattern:** Not using `--fields minimal`, flooding context with data.

**Why it fails:** 5x more tokens consumed, less room for analysis.

**The fix:** Always use `--fields minimal` unless you need full content.

---

### 12. Pipe Panic

**Pattern:** Piping cass export instead of using `-o`.

**Why it fails:** Causes broken pipe panic in cass.

**The fix:** Always use `-o /tmp/out.json` for exports.

```bash
# WRONG
cass export file.jsonl --format json | jq ...

# RIGHT
cass export file.jsonl --format json -o /tmp/out.json
cat /tmp/out.json | jq ...
```

---

## Process Anti-Patterns

### 13. Extraction Without Mining

**Pattern:** Trying to extract skills from memory instead of session history.

**Why it fails:** Memory is biased. Session history is ground truth.

**The fix:** Always mine first, extract second. Evidence before generalization.

---

### 14. One-Shot Extraction

**Pattern:** Extracting once and considering it done.

**Why it fails:** First extractions are drafts. They need refinement.

**The fix:** Plan for 5-12 rounds of iterative refinement (∿).

---

### 15. Skill Hoarding

**Pattern:** Extracting skills but never using them.

**Why it fails:** Unvalidated skills degrade. You don't know if they work.

**The fix:** The flywheel requires USE. Extract → Use → Mine → Extract.

---

## Quick Reference: The Anti-Pattern Checklist

Before finalizing a skill, verify:

- [ ] Not just summarizing behaviors (extracted generative rules)
- [ ] No project-specific terms (paths, names, domain jargon)
- [ ] Not over-generalized (has scope constraints)
- [ ] Counter-examples documented (not ignored)
- [ ] Convergence measured (not just vibes)
- [ ] "Why This Works" explained (not ritual without understanding)
- [ ] Count >= 5 instances (not phantom pattern)
- [ ] Tested on NEW instances (not overfitted)
- [ ] Index fresh before mining
- [ ] `--fields minimal` used
- [ ] Exports use `-o` not pipe

---

## The Recovery Protocol

When you've fallen into an anti-pattern:

1. **Recognize** — Which anti-pattern is this?
2. **Stop** — Don't continue refining a broken extraction
3. **Reset** — Go back to the raw instances
4. **Apply operator** — Usually Third Alternative (⊥) or Ruthless Kill (†)
5. **Restart** — Begin extraction fresh with the lesson learned
