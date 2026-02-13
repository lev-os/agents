# Work FSM v3.0 — Validation Gate Design

> Gate designs for every state transition in the v3 concurrent FSM.
> Written for auditor review before integration into `~/.agents/skills/work/SKILL.md`.

---

## Design Principles

1. **Gates are transition guards, not checkpoints.** A gate fires at the edge between two states, not inside a state.
2. **Layer modulation is continuous, not binary.** Strictness scales with Brand layer + depth, not just on/off.
3. **Confidence routing short-circuits, never bypasses.** High confidence skips non-critical gates; it never skips CATASTROPHIC or CRITICAL gates.
4. **Guard scoring is orthogonal.** The constant guard (6-category underspec scorer) runs every turn regardless of gates. Gates consume the guard score; they do not replace it.
5. **Failure actions are graduated.** BLOCK prevents transition, ASK requests clarification inline, WARN logs and continues, LOG records silently.

---

## Confidence Formula (Reference)

```
base_confidence = 1.0 - (guard_score / 100)
layer_modifier:
  Site/Structure  → -0.10
  Skin/Services   → +0.00
  Space Plan      → +0.05
  Stuff           → +0.10
think_modifier:
  agreement > 80% → +0.10
  agreement 50-80% → +0.00
  agreement < 50% → -0.10

final_confidence = clamp(base + layer_modifier + think_modifier, 0.0, 1.0)
```

### Confidence Routing Table

| Confidence | Gate Behavior |
|------------|---------------|
| >= 0.90 | Skip INFO + WARNING gates; execute MANDATORY+ only |
| 0.80 - 0.89 | Standard: all gates at their declared severity |
| 0.60 - 0.79 | All gates fire + deliberation mode (Think 5-role) required before PROPOSE |
| < 0.60 | All gates + extended checks + human review required before SPEC |

---

## Layer-Dependent Strictness Matrix

| Layer | Depth | Persistence | Strictness Tier | Think Mode | Review Type |
|-------|-------|-------------|-----------------|------------|-------------|
| Site | L0-L1 | System | FORMAL | All 5 roles + devil's advocate | Architecture review |
| Structure | L1 | System | DELIBERATE | All 5 roles | Design review |
| Skin/Services | L1-L2 | System/CDO | STANDARD | Advocate + Critic | Visual + code review |
| Space Plan | L2 | CDO | BRIEF | Light deliberation | Feature review |
| Stuff | L3 | CDO | DIRECT | Skip | Self-review |

### How strictness modulates gates

- **FORMAL**: All gates fire regardless of confidence. Every gate's checks are expanded (see per-gate expansions). Devil's advocate think role required at PROPOSE and SPEC gates.
- **DELIBERATE**: All gates fire at confidence < 0.90. Think deliberation (5 roles) required at PROPOSE.
- **STANDARD**: Gates fire at their declared severity level. Advocate + Critic think at PROPOSE.
- **BRIEF**: WARNING and INFO gates skipped. Light deliberation at PROPOSE.
- **DIRECT**: Only CATASTROPHIC and CRITICAL gates fire. No deliberation required.

---

## Gate Definitions

### Gate 1: DISCOVER -> ALIGN

**Gate Name:** `gate:discover-align` / "Context Sufficiency Gate"

**Severity:** MANDATORY

**Trigger Condition:** DISCOVER phase signals readiness — all three concurrent tracks (interview, prior art, search) have either completed or timed out, AND the constant guard score has stabilized (two consecutive turns with delta < 5%).

**Checks:**

| # | Check | Pass Condition | Layer Expansion |
|---|-------|---------------|-----------------|
| 1 | Guard score threshold | guard_score <= 60% (not in INTERVIEW-required territory) | Site/Structure: <= 40% required |
| 2 | Minimum context gathered | At least one of: prior art results returned, codebase matches found, or 2+ interview answers captured | Site: all three required |
| 3 | Custom:report bead exists | At least one `custom:report` bead created during DISCOVER | All layers: required |
| 4 | Objective clarity | Guard category "Objective" scored PRESENT or PARTIAL | All layers: must be PRESENT for Site/Structure |
| 5 | Scope bounded | Guard category "Scope" not MISSING | Site/Structure: must be PRESENT |

**Layer Modulation:**

- **FORMAL (Site/Structure):** All 5 checks required. Guard score must be <= 40%. All three concurrent tracks must have returned results (not just timed out). Objective AND Scope must be PRESENT (not PARTIAL).
- **DELIBERATE (Structure):** Checks 1-4 required. Guard score <= 50%.
- **STANDARD (Skin/Services):** Checks 1-3 required.
- **BRIEF (Space Plan):** Checks 1, 3 required.
- **DIRECT (Stuff):** Check 3 only (bead exists). Auto-pass if guard_score <= 30%.

**Confidence Routing:**

- >= 0.90: Gate auto-passes (MANDATORY, but confidence override applies at this tier).
- 0.80-0.89: Standard checks.
- 0.60-0.79: All checks + guard must show all 6 categories at PARTIAL or better.
- < 0.60: All checks + require human confirmation ("Enough context gathered to proceed?").

**Failure Action:**

- **BLOCK transition.** Return to DISCOVER with structured prompt: list which checks failed, suggest specific actions (e.g., "Scope is MISSING — ask user to bound the scope" or "No prior art search completed — run `br search` and `cass search`").
- Log failure to `custom:report` bead for audit trail.

---

### Gate 2: ALIGN -> RESEARCH

**Gate Name:** `gate:align-research` / "Alignment Verdict Gate"

**Severity:** CRITICAL

**Trigger Condition:** ALIGN phase completes — layer classification done, north star checked (or created if absent), alignment verdict rendered.

**Checks:**

| # | Check | Pass Condition | Layer Expansion |
|---|-------|---------------|-----------------|
| 1 | Layer classified | Brand layer (Site/Structure/Skin/Services/Space/Stuff) assigned | All: required |
| 2 | Depth assigned | L0-L3 depth determined | All: required |
| 3 | Persistence tagged | System graph vs CDO graph determined | All: required |
| 4 | Alignment verdict | One of: `aligned`, `drift`, `gap` rendered | All: required |
| 5 | Drift resolution | If verdict == `drift`: drift type classified (Stale Docs / Product Pivot / Coverage Gap / Status Drift / Path Drift) | Site/Structure: must also propose resolution |
| 6 | North star exists | `lev-align` found or created a north star document | Site/Structure: required |
| 7 | System bead created | If no prior project context, `custom:system` bead created | Site/Structure: required |

**Layer Modulation:**

- **FORMAL:** All 7 checks. If drift detected at Site layer, BLOCK until drift resolution plan approved by human.
- **DELIBERATE:** Checks 1-6. Drift requires classification but not resolution plan.
- **STANDARD:** Checks 1-5.
- **BRIEF:** Checks 1-4.
- **DIRECT:** Checks 1-2 only (layer + depth). Verdict inferred as `aligned` if no contradicting signals.

**Confidence Routing:**

- >= 0.90: Checks 1-3 only (classification). Skip alignment verdict if prior session established alignment.
- 0.80-0.89: Standard checks per layer tier.
- 0.60-0.79: All checks + if verdict is `drift` or `gap`, require Think deliberation (Advocate + Critic minimum) before proceeding.
- < 0.60: All checks + human review of alignment verdict required.

**Failure Action:**

- **BLOCK transition** for FORMAL/DELIBERATE tiers.
- **ASK inline** for STANDARD tier (present verdict options, let user confirm).
- **WARN and continue** for BRIEF/DIRECT tiers (log missing checks, proceed).
- If verdict == `gap` at Site/Structure layer: hard BLOCK, cannot proceed to RESEARCH without resolving the gap (create north star, re-align).

---

### Gate 3: RESEARCH -> PROPOSE

**Gate Name:** `gate:research-propose` / "Research Depth Gate"

**Severity:** MANDATORY

**Trigger Condition:** RESEARCH phase signals depth sufficient — code analysis, content review, and/or design review complete. DoR (Definition of Ready) categories progressing.

**Checks:**

| # | Check | Pass Condition | Layer Expansion |
|---|-------|---------------|-----------------|
| 1 | Research artifacts exist | At least one `custom:report` bead from RESEARCH phase (distinct from DISCOVER reports) | All: required |
| 2 | DoR progress | At least 60% of DoR categories have data | Site: 90% required; Structure: 80% |
| 3 | Code analysis done | If code changes implied: codebase search completed, relevant files identified | Skin+: required if code implied |
| 4 | C1-C4 mapping | Concern mapping completed (C1: functional, C2: quality, C3: cross-cutting, C4: constraints) | Site/Structure: required; others: skip |
| 5 | Prior art reconciled | Prior art from DISCOVER reviewed and integrated into research findings | FORMAL/DELIBERATE: required |
| 6 | Guard score stable | Guard score has not increased since DISCOVER (context not degrading) | All: warning if violated |

**Layer Modulation:**

- **FORMAL:** All 6 checks. C1-C4 mapping required with documented trade-offs. DoR at 90%.
- **DELIBERATE:** Checks 1-5. C1-C4 mapping required. DoR at 80%.
- **STANDARD:** Checks 1-3, 6. DoR at 60%.
- **BRIEF:** Checks 1, 3. Minimal research sufficient.
- **DIRECT:** Check 1 only. Any research artifact is sufficient.

**Confidence Routing:**

- >= 0.90: Check 1 only. Prior art + code search results deemed sufficient.
- 0.80-0.89: Standard checks per layer tier.
- 0.60-0.79: All checks + extended research required (online sources, skill search, related project analysis).
- < 0.60: All checks + human review of research completeness + Think deliberation (all 5 roles assess whether research is sufficient).

**Failure Action:**

- **BLOCK transition** if check 1 fails (no research artifacts at all).
- **ASK inline** if DoR progress insufficient ("Research is at {X}% DoR coverage. Continue to proposal or deepen research?").
- **WARN** if guard score increased (context may be degrading, suggest re-running interview).
- Log gaps to `custom:report` bead.

---

### Gate 4: PROPOSE -> SPEC

**Gate Name:** `gate:propose-spec` / "Proposal Approval Gate"

**Severity:** CRITICAL

**Trigger Condition:** PROPOSE phase completes — Think deliberation rendered, `custom:proposal` bead created, proposal ready for crystallization.

**Checks:**

| # | Check | Pass Condition | Layer Expansion |
|---|-------|---------------|-----------------|
| 1 | Proposal bead exists | `custom:proposal` bead created with complete content | All: required |
| 2 | Think deliberation complete | Layer-appropriate Think mode executed (see matrix) | FORMAL/DELIBERATE: all 5 roles; STANDARD: Advocate+Critic; BRIEF/DIRECT: skip |
| 3 | Think agreement threshold | Think role agreement >= 60% (no unresolved fundamental disagreements) | Site: >= 80%; Structure: >= 70% |
| 4 | Devil's advocate pass | If FORMAL: devil's advocate role challenged proposal and concerns addressed | Site/Structure only |
| 5 | Proposal sections complete | Executive summary, approach, trade-offs, risks, and recommended path present | FORMAL/DELIBERATE: all; STANDARD: summary+approach+risks |
| 6 | Layer-risk acknowledged | If Site/Structure: explicit risk assessment with rollback strategy | Site/Structure only |
| 7 | Alignment re-check | Proposal does not contradict alignment verdict from ALIGN phase | All: required |

**Layer Modulation:**

- **FORMAL:** All 7 checks. Devil's advocate must run. Agreement >= 80%. Full risk assessment with rollback. Human approval of proposal required before proceeding to SPEC.
- **DELIBERATE:** Checks 1-3, 5, 7. All 5 Think roles. Agreement >= 70%.
- **STANDARD:** Checks 1-2, 5(partial), 7. Advocate + Critic only. Summary + approach + risks required.
- **BRIEF:** Checks 1, 7. Light deliberation optional. Proposal can be inline (ephemeral-style).
- **DIRECT:** Check 1 only. Proposal can be a single-paragraph inline decision. No deliberation required.

**Confidence Routing:**

- >= 0.90: Checks 1, 7 only. Proposal auto-approved if alignment holds.
- 0.80-0.89: Standard checks per layer tier.
- 0.60-0.79: All checks + extended Think deliberation (5 roles + dissent round) + human review of proposal.
- < 0.60: All checks + human must explicitly approve proposal before transition. Think must include external reference validation.

**Failure Action:**

- **BLOCK transition** if Think agreement < threshold (unresolved disagreements → return to PROPOSE for revision).
- **BLOCK transition** if FORMAL and no devil's advocate pass.
- **ASK inline** if proposal sections incomplete ("Proposal missing: {sections}. Add them or proceed anyway?").
- **BLOCK at Site layer** if no human approval received.
- If alignment re-check fails: BLOCK, return to ALIGN with drift notification.

---

### Gate 5: SPEC -> EXECUTE

**Gate Name:** `gate:spec-execute` / "Spec Completeness Gate"

**Severity:** CATASTROPHIC

**Trigger Condition:** SPEC phase completes — `custom:spec` bead created, BDD scenarios written, contracts defined, acceptance criteria set, BD tasks created.

**Checks:**

| # | Check | Pass Condition | Layer Expansion |
|---|-------|---------------|-----------------|
| 1 | Spec bead exists | `custom:spec` bead created | All: required |
| 2 | Executive summary | Present and <= 3 paragraphs | All: required |
| 3 | Context defined | Existing state AND target state documented | All: required |
| 4 | BDD scenarios | Given/When/Then scenarios covering primary flows | Site: comprehensive (all flows); Stuff: happy path only |
| 5 | Input/Processing/Output | I/P/O triples defined for each scenario | FORMAL/DELIBERATE: required; STANDARD: at least primary flow |
| 6 | Dependencies declared | All external dependencies listed with versions/contracts | All: required |
| 7 | Integration points | All integration boundaries documented | FORMAL/DELIBERATE/STANDARD: required |
| 8 | Breaking changes | Breaking changes explicitly noted (even if "none") | FORMAL/DELIBERATE: required |
| 9 | Recommended skills | Execution skills listed | All: required |
| 10 | Team structure | If complex: team structure defined with workstreams | FORMAL/DELIBERATE: required if complexity > Simple |
| 11 | Unit test cases | Test cases defined | FORMAL/DELIBERATE/STANDARD: required |
| 12 | Integration tests | Integration test scenarios | FORMAL/DELIBERATE: required |
| 13 | E2E verification | E2E verification command specified | FORMAL/DELIBERATE: required |
| 14 | Success criteria | Measurable success criteria with acceptance thresholds | All: required |
| 15 | BD tasks created | Spec decomposed into BD epics/tasks | FORMAL/DELIBERATE/STANDARD: required |
| 16 | Rollback plan | How to undo if execution fails | Site/Structure: required |

**Layer Modulation:**

- **FORMAL (Site + L0-L1):** ALL 16 checks required. No exceptions. Human sign-off required. Architecture review by Think (all 5 roles + devil's advocate on spec). Multi-gate execution plan (phased rollout).
- **DELIBERATE (Structure + L1):** Checks 1-15 required. Check 16 recommended. Design review by Think (all 5 roles).
- **STANDARD (Skin/Services + L1-L2):** Checks 1-7, 9, 11, 14, 15 required. Visual + code review.
- **BRIEF (Space Plan + L2):** Checks 1-4, 6, 9, 14 required. Feature review.
- **DIRECT (Stuff + L3 + CDO):** Checks 1, 3, 14 required. Self-review. Spec can be minimal (acceptance criteria + brief context).

**Confidence Routing:**

- >= 0.90: Layer-minimum checks only (cannot skip CATASTROPHIC gate entirely, but reduces check count to layer minimum).
- 0.80-0.89: Standard checks per layer tier.
- 0.60-0.79: All checks for layer + extended review + Think deliberation on spec completeness.
- < 0.60: All 16 checks regardless of layer + human review + Think full parliament + explicit approval required.

**Failure Action:**

- **CATASTROPHIC BLOCK.** Cannot proceed to EXECUTE under any circumstances if this gate fails.
- List every failing check with specific remediation instructions.
- Return to SPEC phase with structured gap list.
- If 3+ consecutive failures: escalate to human with full diagnostic ("Spec cannot pass gate after 3 attempts. Issues: {list}").
- Never auto-waive. Never skip. Never degrade severity.

---

### Gate 6: EXECUTE -> VALIDATE

**Gate Name:** `gate:execute-validate` / "Work Artifacts Gate"

**Severity:** MANDATORY

**Trigger Condition:** EXECUTE phase signals completion — all planned work items report done, artifacts created, inline learnings captured.

**Checks:**

| # | Check | Pass Condition | Layer Expansion |
|---|-------|---------------|-----------------|
| 1 | Artifacts exist | Work products (code, docs, configs) created as specified in spec | All: required |
| 2 | BD tasks updated | All BD tasks for this spec moved to completed/review status | FORMAL/DELIBERATE/STANDARD: required |
| 3 | No unresolved blockers | No BD tasks in blocked status | All: required |
| 4 | Inline learnings captured | Any gotchas/bugs discovered during execution saved via `cm add` | All: required (even if "none discovered" is logged) |
| 5 | Spec coverage | All BDD scenarios from spec addressed (not necessarily passing, but addressed) | FORMAL/DELIBERATE: all scenarios; STANDARD: primary flows |
| 6 | Files manifest | List of all files created/modified available | All: required |
| 7 | Build passes | If code: project builds without errors | All if code: required |
| 8 | No regressions introduced | If code: existing tests still pass | FORMAL/DELIBERATE/STANDARD: required |

**Layer Modulation:**

- **FORMAL:** All 8 checks. Every BDD scenario must be addressed. Build + full test suite must pass. Files manifest must be complete with diff summaries.
- **DELIBERATE:** Checks 1-7. All BDD scenarios addressed. Build must pass.
- **STANDARD:** Checks 1-4, 6-7. Primary flow BDD scenarios addressed.
- **BRIEF:** Checks 1, 3, 6. Artifacts exist and no blockers.
- **DIRECT:** Checks 1, 6. Artifacts exist and manifest available.

**Confidence Routing:**

- >= 0.90: Checks 1, 6, 7 only (artifacts exist, manifest available, build passes).
- 0.80-0.89: Standard checks per layer tier.
- 0.60-0.79: All checks + code review required (Think: Advocate + Critic review diffs).
- < 0.60: All checks + human review of all artifacts + Think full parliament review.

**Failure Action:**

- **BLOCK transition** if check 1 fails (no artifacts — nothing to validate).
- **BLOCK transition** if check 7 fails (broken build — must fix before validation).
- **ASK inline** if check 5 partial ("X of Y BDD scenarios addressed. Continue to validation or complete remaining?").
- **WARN** if check 4 empty (no learnings — unusual for non-trivial work, prompt: "Any gotchas worth capturing?").
- Return to EXECUTE with gap list if blocked.

---

### Gate 7: VALIDATE -> EMIT

**Gate Name:** `gate:validate-emit` / "Quality Assurance Gate"

**Severity:** CRITICAL

**Trigger Condition:** VALIDATE phase completes — all quality checks run, results available.

**Checks:**

| # | Check | Pass Condition | Layer Expansion |
|---|-------|---------------|-----------------|
| 1 | BDD scenarios pass | All Given/When/Then scenarios from spec verified | FORMAL: 100%; DELIBERATE: 95%; STANDARD: primary flows; BRIEF/DIRECT: happy path |
| 2 | Unit tests pass | All defined unit tests green | FORMAL/DELIBERATE/STANDARD: required |
| 3 | Integration tests pass | Integration test scenarios verified | FORMAL/DELIBERATE: required |
| 4 | E2E verification | E2E command runs successfully | FORMAL/DELIBERATE: required |
| 5 | Success criteria met | Measurable criteria from spec evaluated and met | All: required |
| 6 | No drift detected | File paths resolve, symlinks valid, no broken references | All: warning if violated |
| 7 | Architecture alignment | If Site/Structure: no anti-patterns introduced, XDG/fractal ownership preserved | Site/Structure: required |
| 8 | Prior art re-check | No conflicting work merged during execution | FORMAL/DELIBERATE: required |
| 9 | Visual validation | If UI changes: screenshot taken and reviewed (per HARD GATE protocol) | All if UI: CATASTROPHIC sub-gate |
| 10 | Security scan | No OWASP top-10 vulnerabilities introduced | Site/Structure: required; others: recommended |

**Layer Modulation:**

- **FORMAL:** All 10 checks. 100% BDD pass rate. Architecture review confirms no regression. Security scan mandatory. Human sign-off on validation results.
- **DELIBERATE:** Checks 1-8. 95% BDD pass rate acceptable (document exceptions). Security scan recommended.
- **STANDARD:** Checks 1-2, 5-6, 9(if UI). Primary flow BDD. Code review (Advocate + Critic).
- **BRIEF:** Checks 1, 5, 6. Happy path BDD. Feature review.
- **DIRECT:** Check 5 only. Success criteria met = pass.

**Confidence Routing:**

- >= 0.90: Layer-minimum checks only.
- 0.80-0.89: Standard checks per layer tier.
- 0.60-0.79: All checks + extended validation (edge cases, error paths) + Think review.
- < 0.60: All checks + human review of validation results + Think full parliament assessment.

**Failure Action:**

- **BLOCK transition** if check 5 fails (success criteria not met — the work is not done).
- **BLOCK transition** if check 9 fires and fails (UI changes not visually validated — per project HARD GATE).
- **ASK inline** if BDD pass rate below threshold ("X% BDD pass rate vs Y% required. Fix failures or accept with documented exceptions?").
- **WARN** if drift detected (check 6) — may indicate concurrent work conflicts.
- Return to EXECUTE if critical failures require rework.
- Return to VALIDATE if minor failures can be fixed in-place.

---

### Gate 8: EMIT -> LEARN

**Gate Name:** `gate:emit-learn` / "Artifact Emission Gate"

**Severity:** WARNING

**Trigger Condition:** EMIT phase completes — bead created, status updated, user notified.

**Checks:**

| # | Check | Pass Condition | Layer Expansion |
|---|-------|---------------|-----------------|
| 1 | Artifact bead created | Bead exists with correct custom type and labels | All: required |
| 2 | Bead closed | Custom bead status updated (not left open/draft) | All: required |
| 3 | BD status updated | Related BD tasks moved to completed | FORMAL/DELIBERATE/STANDARD: required |
| 4 | Bead metadata valid | Labels, type, and description populated correctly | FORMAL/DELIBERATE: required |
| 5 | Bead ID recorded | Bead ID logged for audit trail | All: warning if missing |
| 6 | User notified | Bead ID reported to user | All: required |

**Layer Modulation:**

- **FORMAL:** All 6 checks. Bead must have complete metadata, BD linkage.
- **DELIBERATE:** Checks 1-4, 6.
- **STANDARD:** Checks 1-3, 6.
- **BRIEF:** Checks 1, 2, 6.
- **DIRECT:** Checks 1, 6 only. Bead closure recommended but not blocking.

**Confidence Routing:**

- >= 0.90: Checks 1, 6 only. Bead exists and user notified.
- 0.80-0.89: Standard checks per layer tier.
- 0.60-0.79: All checks (emission is low-risk, confidence mainly affects earlier gates).
- < 0.60: All checks (same — emission is a formality at this point).

**Failure Action:**

- **WARN** if bead not created (attempt recovery: retry `br create`).
- **WARN** if bead not closed (attempt: close bead programmatically).
- **LOG** metadata issues (non-blocking, cosmetic).
- **Never BLOCK** the LEARN transition — learning should always happen even if emission had issues. Capture the emission failure itself as a learning.

---

## Special Gates

### UI Visual Validation Sub-Gate (Cross-Cutting)

**Gate Name:** `gate:ui-visual` / "Visual Verification Sub-Gate"

**Severity:** CATASTROPHIC (when applicable)

**Trigger Condition:** Any transition where the work involves SwiftUI views, components, storybook pages, or theme files. Fires as a sub-gate within `gate:execute-validate` and `gate:validate-emit`.

**Checks (from project HARD GATE protocol):**

| # | Step | Pass Condition |
|---|------|---------------|
| 1 | Build | `pnpm mac:build` / `pnpm ios:build` succeeds |
| 2 | Relaunch | App relaunched via `pnpm dev --target ...` |
| 3 | Screenshot | `./bin/apple-tester screenshot /tmp/<name>.png` taken AND image file read with Read tool |
| 4 | Tests | `pnpm test` + apple-tester smoke tests pass |

**All 4 steps MANDATORY. No exceptions. No substitutions.**

- Element counts are NOT visual validation.
- Snapshot JSON is NOT visual validation.
- BUILD SUCCEEDED alone is NOT sufficient.
- The ONLY valid verification is: screenshot -> Read image file -> visually inspect pixels.

**Failure Action:** CATASTROPHIC BLOCK. Cannot mark any UI task complete without all 4 steps.

---

### Constant Guard (Not a Transition Gate)

**Name:** `guard:underspec` / "Underspec Guard"

**Type:** Continuous monitor (fires every turn, not at transitions)

**Relationship to Gates:** The guard score feeds INTO gate checks (especially `gate:discover-align`) but is not itself a gate. It runs inside DISCOVER and persists across all states.

**Categories and Weights:**

| Category | Weight | Scoring |
|----------|--------|---------|
| Objective | 20% | MISSING = 20, PARTIAL = 10, PRESENT = 0 |
| Scope | 20% | MISSING = 20, PARTIAL = 10, PRESENT = 0 |
| Constraints | 15% | MISSING = 15, PARTIAL = 7.5, PRESENT = 0 |
| Environment | 15% | MISSING = 15, PARTIAL = 7.5, PRESENT = 0 |
| Dependencies | 15% | MISSING = 15, PARTIAL = 7.5, PRESENT = 0 |
| Success Criteria | 15% | MISSING = 15, PARTIAL = 7.5, PRESENT = 0 |

**Routing:**

- Score <= 30%: PASS (sufficient spec)
- Score 30-60%: ASK (structured questions for MISSING categories)
- Score > 60%: Route to interview skill (wizard-mode)

---

## Gate Summary Matrix

| Gate | Transition | Severity | FORMAL Checks | DIRECT Checks | Confidence Skip |
|------|-----------|----------|---------------|---------------|-----------------|
| `gate:discover-align` | DISCOVER -> ALIGN | MANDATORY | 5/5 (strict) | 1/5 | >= 0.90 auto-pass |
| `gate:align-research` | ALIGN -> RESEARCH | CRITICAL | 7/7 | 2/7 | >= 0.90 skip to 3 |
| `gate:research-propose` | RESEARCH -> PROPOSE | MANDATORY | 6/6 | 1/6 | >= 0.90 skip to 1 |
| `gate:propose-spec` | PROPOSE -> SPEC | CRITICAL | 7/7 + human | 1/7 | >= 0.90 skip to 2 |
| `gate:spec-execute` | SPEC -> EXECUTE | CATASTROPHIC | 16/16 + human | 3/16 | Never fully skip |
| `gate:execute-validate` | EXECUTE -> VALIDATE | MANDATORY | 8/8 | 2/8 | >= 0.90 skip to 3 |
| `gate:validate-emit` | VALIDATE -> EMIT | CRITICAL | 10/10 + human | 1/10 | >= 0.90 layer-min |
| `gate:emit-learn` | EMIT -> LEARN | WARNING | 6/6 | 2/6 | >= 0.90 skip to 2 |

---

## Gate Interaction with FSM Backtracking

Gates can trigger backtracking. The backtrack targets are:

| Gate Failure | Backtrack To | Condition |
|-------------|-------------|-----------|
| `gate:discover-align` | DISCOVER | Insufficient context — re-interview or re-search |
| `gate:align-research` | ALIGN (re-classify) or DISCOVER (if gap found) | Misclassification or missing north star |
| `gate:research-propose` | RESEARCH | Insufficient depth — deepen analysis |
| `gate:propose-spec` | PROPOSE (revise) or RESEARCH (if fundamentally wrong) | Think disagreement or alignment drift |
| `gate:spec-execute` | SPEC (fix) or PROPOSE (if spec reveals proposal flaw) | Missing sections or invalid contracts |
| `gate:execute-validate` | EXECUTE | Incomplete work — finish remaining items |
| `gate:validate-emit` | EXECUTE (rework) or VALIDATE (minor fixes) | Test failures or visual validation failure |
| `gate:emit-learn` | EMIT (retry) | Write failure — never blocks LEARN |

**Max backtrack depth:** 3 consecutive failures at the same gate before escalating to human review, regardless of layer or confidence.

---

## Implementation Notes

1. **Gate state is persisted in beads.** Each gate evaluation creates a `custom:report` bead entry with gate name, checks run, pass/fail results, and confidence at evaluation time. This enables audit trails and post-mortem analysis.

2. **Gates are idempotent.** Running a gate twice with the same inputs produces the same result. No side effects from gate evaluation itself.

3. **Confidence is recalculated at each gate.** The formula uses the latest guard score, current layer classification, and most recent Think agreement score. Confidence can change between gates.

4. **CATASTROPHIC gates never degrade.** The `gate:spec-execute` gate cannot be reduced to CRITICAL or lower by any mechanism (confidence, layer, user override). The only way past is to pass it.

5. **Human review requests are async.** When a gate requires human review, the FSM pauses at that transition. It does not auto-timeout or auto-proceed. The human must explicitly approve or reject.
