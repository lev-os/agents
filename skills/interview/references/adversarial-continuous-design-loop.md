# Adversarial Continuous Design Loop — Rubric

Use this reference only when a user asks for an iterative, non-leading interview plus independent adversarial architecture review.

## Turn record

Keep these fields in the design artifact for every turn:

```yaml
turn: <integer>
active_branch: <responsibility-based name>
evidence:
  - path_or_symbol: <what it proves>
user_judgment: <verbatim summary without promoting chat wording to domain language>
branches_opened: []
branches_closed: []
ambiguity:
  topic_percent: <0-100>
  overall_percent: <0-100>
readiness:
  semantic: <0-100>
  ownership: <0-100>
  behavior: <0-100>
  migration: <0-100>
  proof: <0-100>
arch_verdict: APPROVED | NEEDS_REVIEW
arch_evidence: []
required_corrections: []
```

## Scoring discipline

- **Ambiguity** measures unresolved meaning, not writing quality.
- Score every material branch and every list item separately; create a branch when a single score would hide different decisions.
- Lower a score only after a human decision is recorded or workspace evidence resolves the branch.
- Increase ambiguity when review exposes a missing dependency, competing semantic authority, or untested failure mode.
- Closure requires each item below 5%, overall below 10%, concrete proof gates, and the most recent independent Arch verdict `APPROVED`.

## Non-leading question test

A compliant question:

- asks about behavior, authority, outcome, or constraint in the user's own terms;
- contains no suggested answer, ranked option, or hidden recommendation;
- names the active branch and why it is next;
- is preceded by evidence lookup.

Reject questions that ask the user to choose an implementation label before their desired behavior is understood.

## Adversarial review minimum

Require the reviewer to inspect for:

1. existing abstraction collisions;
2. ownership and dependency-direction violations;
3. authority, admission, authorization, and evidence ambiguity;
4. lifecycle, cancellation, retry, recovery, replay, and migration failure modes;
5. provider/infrastructure leakage into domain language;
6. missing executable proof gates;
7. conversational-artifact naming.

## Required final inline design

When the closure gate passes, show the resolved design inline with:

- problem and operator JTBD;
- bounded contexts and vocabulary;
- responsibility/port/adapter boundaries;
- lifecycle and failure semantics;
- migration sequence and rollback;
- fitness functions and owners;
- ambiguity/readiness scorecard;
- final Arch verdict and evidence.
