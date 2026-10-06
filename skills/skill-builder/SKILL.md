---
name: skill-builder
description: Use when creating skills, converting docs/repos/PDFs to skills, installing external skills, auditing skill quality or security, or merging skills
---

# Skill Builder

Skill edits are candidates until relevant behavioral checks pass. Preserve existing
work; missing baseline evidence is evaluation work, not authority to delete it.
An explicit skills-first update may precede trials, but must remain unqualified.

## Contents

- [Qualification and selectors](#qualification-states-and-selectors)
- [Source inventory and IR](#scrape-and-analyze-skill-structure)
- [Expertise acquisition](#operational-expertise-acquisition)
- [Route the request](#routing)
- [Pointers and invocation](#pointer-repair-and-invocation)
- [References and freedom](#reference-navigation-and-degrees-of-freedom)
- [Output templates](#output-sections)
- [Audit and behavior checks](#read-only-audit-and-behavior-checks)
- [Absorb into the owner](#absorb-learn-and-test-in-the-existing-owner)
- [Intake and install](#workflow-1-intake--install)
- [Author a skill](#workflow-2-author-from-scratch-tdd)
- [Extract source material](#workflow-3-extraction-pipeline)
- [Security scan](#workflow-4-security-scan)
- [Merge skills](#workflow-5-merge)
- [Generate candidates](#workflow-6-fractal-auto-generation)
- [Reference index](#references)
- [Observed rationalizations](#rationalization-table)

## Qualification states and selectors

Keep these states separate in every report: **structural** (the file parses and
source obligations map), **behavioral** (bounded fresh scenarios show the
intended judgment), and **integration** (the target host loads, routes and
authorizes it). A structural pass never upgrades the other states.

The following are skill selectors, not invented runtime APIs:

- `--scrape <url|repo>` collects exact source snapshots and a coverage manifest for analysis.
- `--analyze <source|snapshot>` builds per-skill JSON IRs and a graph report without installing or executing the subject.
- `--absorb <source>` learns into an existing owner; starts with the quick fixture comparison below.
- `--audit <skill|folder|all>` performs a read-only quality audit.
- `--behavior` requests bounded fresh behavioral trials within an explicit
  budget; it does not install, promote or edit the subject or grader.
- `--security` enters the existing mandatory security intake scan.

For `--audit <target> --security`, select the existing security scan. For
`--audit <target> --behavior`, inspect the target and then run the requested
bounded trials. If both modifiers are present, run security before behavioral
trials within their declared scope and budget. A bare `--behavior` needs an
explicit target or an unambiguous current subject.

Do not compute an aggregate expertise score. Report findings, evidence and
remaining gaps by state and by artifact.

## Scrape and analyze skill structure

For the AIUX Playground corpus, reuse the source-backed analyzer at
`/Users/jean-patricksmith/ops/audits/skill-ir-20260930/build_ir.py` when that file
is available: inspect `--help`, use `--acquire` for permitted public GETs, run
without that selector for cached analysis, and run `--check` for integrity.
Its catalog-specific acquisition is an implementation reference; other sources
follow the same IR obligations below rather than silently using that catalog.

`--scrape` and `--analyze` are skill selectors. For skill catalogs, collect each
listed entry and its actual package source; keep catalog descriptions separate.
For repositories or local folders, pin the revision or file digests. Preserve
source attribution and license information, and record inaccessible sources.

1. Collect exact source bytes into the authorized staging location. Resolve
   package-local references recursively and inventory bundled scripts without
   running them. Bound external-link traversal by the chosen source/package
   scope; record unresolved, missing, excluded and unsafe paths explicitly.
2. Emit one JSON IR per skill: identity and provenance; heading taxonomy and
   bullet TOC; triggers and exclusions; rules; ordered workflow and branch
   routes; inputs and outputs; tools and script dependencies; declared side
   effects; gates, verification and recovery. Attach source file, line and
   digest to extracted facts; label inferred relations. Distinguish operative
   instructions from examples/templates and declared effects from observed runs.
3. Build a typed graph linking skills, resources, steps, routes, tools, effects,
   gates and artifacts. Use an available graph library or standard algorithms
   for components, cycles, shared dependencies and overlap candidates. Explain
   the edge definitions; similarity is a review cue, not behavioral parity.
4. Validate catalog coverage, source digests, reference containment, IR schema
   and graph endpoints. Deliver JSON plus a browsable report with per-skill
   bullet TOCs, comparisons and explicit coverage gaps. If requested, register
   metadata-only candidates in skills-db/_todo; keep them inactive and unaudited.

Completion requires every listed entry to have an IR or an explicit source
failure, every bundled script to have a static-analysis record, and every
reachable reference to have a resolution status. Scraping and analysis do not
qualify installation, promotion, execution, or source retirement. Route a later
learning request to `--absorb` and activation to the existing intake checks.

## Operational expertise acquisition

When turning a repeated method or source material into a skill, every resulting
skill must cover these obligations; they are not a fixed execution sequence:

1. **Purpose** — name the user decision or outcome and the branch that needs the method.
2. **Evidence** — collect source passages, observed failures and counterexamples; label supplied, observed, inferred and unknown separately.
3. **Judgment** — state the distinction that changes the decision, including the boundary where it stops applying.
4. **Action** — turn the distinction into the smallest ordered action that produces an inspectable artifact or state.
5. **Verification** — name the command, observation or comparison that can falsify the action's claim.
6. **Recovery** — define what to preserve, what to retry, and when to stop or escalate after a failed check.

Map each source obligation to its destination before compression, deletion or
merging. Keep lossless source mapping in a ledger; unresolved mappings remain
open. Use the operationalizing-expertise method's sentence form, “When X, do Y
because Z,” and validate against counterexamples. Its corpus, quote-bank,
operator-count and triangulation deliverables are for that larger program; do
not impose them on a bounded skill edit unless that scope is explicitly chosen.

The acquisition sequence is distinct from those six obligations:

1. Define competence, success conditions and limits from the task and owner evidence; ask the operator only about unresolved consequential choices.
2. Acquire anchored successes, failures and corrections from representative cases and source passages.
3. Extract the fact or distinction that changes the action, including what remains unknown.
4. Challenge it with counterfactuals, missing-evidence cases and boundary exceptions.
5. Encode `notice → why → test → bad/good → exception` as a trigger, action, invariant, evidence check and recovery path.
6. Test held-out transfer on a fresh case and retain the result as pending until the evidence supports it.

For each encoded rule, make the teaching pattern explicit: **notice** the signal,
state **why** the distinction matters, name the **test**, show a **bad** and a
**good** case, and state the **exception** or boundary. Use the examples as
anchors for judgment, not as a substitute for case evidence.

## Routing

```yaml
steps:
  - id: route
    action: Classify the request and dispatch
    instruction: |
      | Input                          | Workflow         | Jump to     |
      |-------------------------------|------------------|-------------|
      | URL, skills.sh link, skill:// | Intake & Install | intake      |
      | "new skill", "from scratch"   | Author (TDD)     | author_red  |
      | Docs site, GitHub repo, PDF   | Extraction       | extract     |
      | "--audit", audit               | Read-only Audit  | [Audit section](#read-only-audit-and-behavior-checks) |
      | "--security", "is this safe"  | Security Scan    | security    |
      | "--behavior"                   | Behavior Checks  | [Behavior section](#read-only-audit-and-behavior-checks) |
      | "--scrape", "--analyze"       | Source Analysis  | [Scrape and analyze](#scrape-and-analyze-skill-structure) |
      | "--absorb", "learn from this"  | Absorb           | [Absorb](#absorb-learn-and-test-in-the-existing-owner) |
      | "merge these skills"          | Merge            | merge       |
      Ambiguous? Ask: "Are you converting existing material or authoring from scratch?"
    validation: "Primary workflow, target and any explicitly requested additional checks are identified"
    on_failure: "Ask a clarifying question. Do not guess."
```

## Pointer Repair and Invocation

Every context pointer names both its material and the branch or condition that
triggers loading it. When a required reference is missed, sharpen that pointer
first; inline its operative content only if sharpening fails, except for
explicitly requested baked-in rules. When a step ends prematurely, sharpen its
completion bound before splitting the sequence. Replace repeated explanatory
phrases with a defined, established domain term when that improves retrieval; do
not coin opaque slogans. Delete a demonstrated no-op sentence as a whole rather
than cosmetically trimming it. A stronger leading word is useful only if
observed behavior changes.

Treat always-loaded descriptions as the most expensive context surface: prune
their words aggressively and retain only words that change routing or invocation.
Separate that context cost from the human cost of remembering explicit entry
points. Treat cognitive load as the price of human agency: spend it where human judgment
matters and remove it where deterministic routing or existing conventions can carry
the decision. Add an independently discoverable skill only
when its own trigger or a real caller warrants that cost. Otherwise keep a
conditional branch or shared reference under the existing owner. A router
reduces the human index burden by naming destinations and when to use them, not
by bypassing invocation or authorization policy.

Use the least costly sufficient information tier: keep ordered actions inline,
use an in-file reference for on-demand material when that is enough, and disclose
external material behind a pointer only when a branch needs it. An in-file reference
is a valid hierarchy tier, not an automatic reason to split a skill.

Inspect the target host's supported invocation metadata before setting flags.
Preserve existing invocation choice unless the user requests a change. Portable
skills keep a meaningful description; do not assume description presence grants
automatic dispatch, or that a foreign disable-model-invocation flag hides content
on every host. Where the host enforces explicit-only invocation, routers suggest
the skill rather than dispatch it. Shared material needed by such skills belongs
in an accessible reference, not behind an unreachable invocation. Test explicit
reachability, automatic-trigger positives/negatives and caller routing on the
actual host before claiming these properties. Host-specific metadata is not a
universal Lev contract. These operative rules are inline; loading the source
SKILL-MECHANICS document is not a runtime prerequisite.

## Reference navigation and degrees of freedom

For authoring, absorption and audit, choose freedom **per step** from its
requirements, variability and failure consequence:

| Freedom | Fit | Instruction form |
|---------|-----|------------------|
| High | Several valid approaches; context changes the judgment | Outcome, evidence and boundaries in prose |
| Medium | Preferred method with permitted variation | Template or parameterized procedure; name allowed choices |
| Low | Fragile operation; consistency or sequence is required | Verified command or script with constrained inputs |

One skill may mix all three. Record the requirement, chosen freedom, permitted
variation, failure consequence and verifier together. Freedom governs method;
authorization still governs effects. Reuse a proven command before creating a
script. Constrain sensitive inputs, preview effects when supported, and define
recovery or rollback for consequential changes.

Reference files over 100 lines need an early TOC matching actual headings.
Give branch-needed references a direct SKILL.md pointer and a loading condition;
check paths and anchors. Keep nested references explicit in the coverage ledger.
Review bytes or tokens and branch count alongside line count: dense single-line
prose still needs navigation. Keep structured references valid; use comment/key
indexes or a separate guide instead of inserting Markdown into schemas or data.
Treat Anthropic's 500-line body guidance as a navigation review trigger under
this owner's existing context policy, not a universal rejection threshold.

Test intended models and hosts separately. Declare supported targets and
observed results in evidence; use frontmatter only when the host supports it.
For ordered workflows, track completion with evidence. Validate outputs,
repair failed checks and retry within a finite budget; leave unresolved failures
visible when that budget ends. Place dependency detection and scoped setup
instructions beside script entrypoints. Installation still needs its existing
authority; a missing tool is not permission for a global install.

Source: [Anthropic skill authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices),
reviewed with [Simon Scrapes' video](https://www.youtube.com/watch?v=e7TY56-yIvM)
on 2026-10-03. These are design recommendations; neither a universal 100-line
read cutoff nor zero context cost for script execution is established here.

For exhaustive audits, freeze the top-level inventory and file digests first.
Give every skill and bundled reference a coverage row, including orphaned files,
symlink targets, unreadable resources and excluded external links. Trace local
pointers recursively, distinguish literal examples from operative instructions,
and record reference cycles and unresolved targets. Reading bytes or running
pattern checks establishes inventory coverage only; label semantic inspection
and behavioral observations separately. Never report exhaustive review while
files remain unexamined without explicit per-file gaps.

Additional checks: trigger positives, negatives and competing owners; output
contract and falsifier; permission and effect boundaries; idempotency, recovery
and retry limits where effects occur; dependency availability in a clean
environment; reference freshness and source ownership. These extend the local
qualification contract. An audit recommends repairs without executing subject
scripts or modifying audited packages.

## Output Sections

Use XML sections directly in the skill body for reusable output templates and semantic response blocks. Do not wrap active XML sections in fenced Markdown or XML code blocks. Fenced blocks are for literal examples only; active templates live as real sections.

<decision>
## {Decision Title}

Recommended: {option} — {reason}

a. {option_a}
b. {option_b}
c. {option_c}
</decision>

YAML is for contracts, FSM/process steps, validation rules, and machine-checkable state. Templates are Markdown prose inside live XML sections.

## Read-only Audit and Behavior Checks

For `--audit <skill|folder|all>`, read the selected subject and its reachable
references without changing files, activation state, credentials or runtime
settings. `all` inventories every selected top-level skill and its bundled and
reachable references, then inspects each with per-file coverage and explicit
limitations. Prioritize findings by consequence and evidence gap without dropping
subjects from an exhaustive request. Use deterministic batching for inventory;
make no automatic subject edits or executions. The default finding is:

`source → distinction → consequence → evidence → minimal repair → test`

Attach the source line or artifact pointer, state whether the distinction is
observed or inferred, and name the smallest repair and check. Report each
finding under structural, behavioral or integration status. Do not turn a
quality grade into a promotion decision and do not apply an automatic effect.

For `--behavior`, freeze the subject and reference digests, scenario packet,
allowed effects and finite budget first. Use fresh contexts, keep source,
reference and absorbed arms identifiable, and preserve raw outputs. A fresh
prompt is not OS isolation; label shared-workspace trials
`representative_nonhermetic`. A no-op or inconclusive result stays visible.

For FlowMind-backed checks, keep semantic observations, schema validity,
observable outcome and acceptance evidence as separate checks. Jev may be used
as an optional bounded observer; it is never a new evaluator or promotion
authority. `--security` uses the existing mandatory intake scan below, with no
gate weakening.

<report>
## Skill Builder Audit — {subject}

Status: structural={pass|pending|blocked}; behavioral={pass|pending|blocked}; integration={pass|pending|blocked}

Finding: {source} → {distinction} → {consequence} → {evidence} → {minimal repair} → {test}

Open evidence gaps: {none or exact gaps}
Effects: read-only; no automatic install, promotion, activation or settings change
</report>

## Absorb: learn and test in the existing owner

`--absorb <source>` selects learning from a skill, document, bundle, or observed
method. Resolve its existing owner and the user's concrete task. Keep the source
as attributed reference; author the candidate in the owner's vocabulary and
contracts. A useful specialist may remain task-local instead of changing a skill.
This selector is skill syntax; it does not claim a runtime CLI command exists.

Start with a quick three-arm comparison before a broad mapping or rewrite:

1. Inspect the source and current owner, choose a fixture tied to the user's actual work, and
   draft the smallest complete candidate. Use a real read-only artifact or a
   disposable worktree when possible; label a supplied example as synthetic.
   State the expected artifact and why it changes the next action. A synthetic
   falsifier alone does not establish usefulness for the user's actual task.
2. Freeze the fixture, question, source, unchanged-owner and candidate digests, model, tools,
   permitted effects, and finite trial budget. Define observable checks before
   dispatch and keep their expected answers out of the subjects' prompts.
3. Give three fresh subagents the same fixture and task:
   - Contender alone: paste the complete original source skill and references.
   - Lev alone: paste the complete unchanged owner skill and references.
   - Contender plus Lev: paste the complete Lev candidate with independently
     authored adaptations from the contender and its required references.
   Verify required references are reachable under the same access policy.
   None receives another arm's results, the grader, or a proposed winner. Any
   skill instruction change uses these three arms, including a method supplied
   as prose. If an arm exceeds scope or budget, report the comparison incomplete;
   do not fabricate a baseline or switch to direct application.
4. Compare actual outputs against the frozen checks. Compare the combined
   candidate against unchanged Lev to identify added benefit or regression, and
   contender against unchanged Lev to identify useful alternatives. Contender
   versus combined alone cannot show whether the addition helps Lev. Record
   useful decisions,
   correctness, lost obligations, regressions, and measured effort separately.
   A tie, failure, missing runtime, or inconclusive comparison is a valid result.
   Fresh context with shared filesystem access is representative_nonhermetic;
   it does not establish OS isolation or broad behavioral qualification.
5. If the candidate helps the user's task, complete the source-to-owner obligation map and name
   the next held-out check. Otherwise preserve the result and revise, defer, or
   keep task-local use. One comparison never authorizes installation, promotion,
   source retirement, product edits, or a new truth-deciding path. Apply only the
   effects already authorized by the user, preserving generated-source ownership.

Direct specialist use produces an artifact, assessment, or task output without
changing skill instructions. It is task application, not evidence of absorption.
Return the useful artifact itself, not only test counts or a status summary.

Save frozen inputs, literal full prompts, agent identities, actual artifacts, raw outputs,
comparison observations, commands and failures as JSON in the resolved Lev XDG
state/artifact route or a fresh system-temp directory; record the absolute path.
Reuse the environment's path resolver instead of a hardcoded project folder.
Report structural, behavioral and integration states separately. Code checks
identity, digests, scope and observable results; LLMs supply semantic observations.
Canonical Lev acceptance, when required, remains with core/eval.

Roll the JSON evidence into the user's requested output. Show what was learned,
what was applied to which owner, what remains unproved, and the next action. When no presentation is
specified, choose suitable tools, skills, inline visuals and reporting for a rich
report at your discretion. Preserve private source text in the evidence store;
share findings and original formulations rather than publishing source prompts.

## Workflow 1: Intake & Install

```yaml
steps:
  - id: intake_acquire
    action: Clone and stage the skill
    instruction: |
      ```bash
      git clone --depth 1 {repo} /tmp/skill-intake-{ts}/
      cp -r /tmp/skill-intake-{ts}/skills/{name}/ ~/.agents/skills-db/_workshop/{source}/{name}/
      rm -rf /tmp/skill-intake-{ts}/
      ```
      Never use WebFetch — it summarizes and destroys content. Never use haiku-tier agents — they hallucinate. Always git clone and cp verbatim.
    validation: "ls ~/.agents/skills-db/_workshop/{source}/{name}/SKILL.md exists and head -1 shows ---"
    on_failure: "Clone failed or SKILL.md missing. Check URL and retry."

  - id: intake_validate
    action: Run hard gates on staged copy
    instruction: |
      ```bash
      file=~/.agents/skills-db/_workshop/{source}/{name}/SKILL.md
      head -1 "$file" | grep -q "^---$" && grep -q "^name:" "$file" && grep -q "^description:" "$file"
      ```
      Any gate fails → reject. Move to .archive/ or delete.
    validation: "All grep commands exit 0"
    on_failure: "Reject the skill. Explain which gate failed."

  - id: intake_security
    action: Run security audit (mandatory for external skills)
    instruction: |
      Jump to security workflow (id: security). Required for anything not authored locally.
    validation: "Security verdict is PASS or PASS-WITH-WARNINGS"
    on_failure: "Hard reject. Quarantine to .archive/ with reason."

  - id: intake_score
    action: Record imported quality triage without promotion
    instruction: |
      Inspect the five source dimensions without collapsing them into an
      expertise score: actionability (concrete next actions), depth (expert
      distinctions and limits), structure (usable organization), triggers
      (when to invoke and when not to), and uniqueness (useful contribution
      beyond existing skills). Record evidence, gaps and specific repairs.
      If an imported source already has numeric dimensions or a letter grade,
      preserve them as triage metadata only: they guide human attention but do
      not prove behavior, authorize promotion or replace security, behavioral
      or integration checks. Explain the basis and uncertainty of any grade.
    validation: "Triage note and evidence basis recorded; promotion remains blocked on the separate qualification states."
    on_failure: "Record the missing basis and keep the subject pending human review."

  - id: intake_catalog
    action: Move from staging to final location
    instruction: |
      Catalog placement may use the supplied triage grade, but it never means
      behavioral promotion:
      A/B → `mv` to `~/.agents/skills-db/{domain}/{name}/`
      C → `mv` to `~/.agents/skills-db/_todo/{name}/`
      D → `mv` to `~/.agents/skills-db/.archive/{name}/`
      Keep unresolved subjects in a reviewable candidate or todo location;
      archive only with a recorded reason. Activation to ~/.agents/skills/
      requires explicit user authorization. Report security, behavioral and
      integration checks separately. An explicitly authorized skills-first
      installation may precede full behavioral trials and stays unqualified;
      mandatory security checks and permission boundaries still apply.
    validation: "Catalog destination and separate qualification states are recorded; activation requires explicit user authorization, and incomplete qualification stays explicit."
    on_failure: "Check permissions and path. Retry mv."
```

## Workflow 2: Author from Scratch (TDD)

```yaml
steps:
  - id: author_red
    action: "RED — Establish baseline failure"
    instruction: |
      Establish source obligations and baseline evidence for behavioral qualification:
      1. Map each required behavior and failure mode to an observable scenario
      2. Freeze fixture, skill/source digests, allowed effects and finite trial budget
      3. Run fresh-context subagents without the target skill; keep source/reference and absorbed arms separate
      3. Capture verbatim: what choices, what rationalizations (exact words), which pressures triggered violations
      Distinguish observed failure, already-satisfied behavior, inconclusive result
      and infrastructure error. Never manufacture RED. Fresh prompts are not OS
      isolation; label shared-workspace trials representative_nonhermetic.
    validation: "Obligations have cases or explicit observability gaps; observed outcomes and trial limits are recorded."
    on_failure: "Keep behavioral qualification pending; preserve authorized candidate edits."

  - id: author_green
    action: "GREEN — Write minimal skill addressing observed failures"
    instruction: |
      Write SKILL.md addressing the specific rationalizations from RED.

      Format: standard skill frontmatter + body:
      - Frontmatter contains `name` and `description`; optional metadata only if the local runtime consumes it
      - Do not invent version/status/provenance keys
      - description starts with "Use when..." — trigger conditions ONLY, never workflow summary
      - Steps are verbs not states. "Search these sources" not "DISCOVER"
      - YAML blocks define contracts, FSM/process, validation, and state
      - Reusable output templates are live XML sections with Markdown prose inside, e.g. `<report>...</report>` or `<decision>...</decision>`
      - Do not put active XML templates inside fenced markdown or fenced XML code blocks
      - First step = most important output, not background theory
      - Bake the operative writing rules into this skill; writing-for-agents remains a separate top-level reference, not a runtime prerequisite.
      - Make every context pointer name its material and triggering branch; front-load only the distinguishing trigger words, collapse synonyms, and prune always-loaded words aggressively.
      - Keep mandatory steps inline. Disclose branch-only material with an explicit condition and load validation.
      - Use an in-file reference for on-demand material when it is the least costly sufficient hierarchy tier; disclose it externally only when a branch needs a separate context load.
      - Co-locate a concept's definition, constraints, and caveats; maintain one operative statement per rule.
      - Completion criteria must be observable and cover every required result; a heading or self-report is not completion.
      - Split a sequence only when later steps cause observed premature completion; a fresh context boundary must enforce the split.
      - Use established domain terms and positive action instructions. Keep a prohibition only for a hard guardrail that cannot be phrased positively, and pair it immediately with the positive target.
      - Treat code, config, schemas, directory layout and live help as the environment's source of truth; keep documentation as a cache only when lookup is costly, and preserve rationale and non-obvious constraints rather than stale copies.
      - Check every line for relevance to what the skill does; prune duplicate, stale and no-op prose, and measure context load separately from the operator's discovery burden.
      - Choose automatic versus explicit invocation deliberately; test trigger negatives and competing routes as well as happy paths.
      - validation: strings are concrete verifiable checks (commands or binary states)
      - Artifact-producing skills need a canon write gate plus lifecycle ledger: compiled_intent, disk vs memory state, artifact ref, route, blocker, confidence
      - Natural language in instruction blocks. Never LLM_MUST directives
      - Fit the operative body to the host context and task. There is no universal line ceiling; split only when a later branch needs an explicit context boundary and the pointer names its trigger.

      Run the frozen scenarios WITH the candidate skill using fresh contexts.
      Retain raw outputs and artifact deltas; independent review assesses semantic
      outcomes, not repeated instruction wording. A changed fixture/rubric starts
      a new evaluator generation; do not repair subject and grader in one attempt.
    validation: "Frontmatter has supported keys. All steps have validation: strings. Artifact-producing skills include a fidelity/memory/ledger table. Reusable templates use live XML sections, not fenced code blocks. Context size and any split have a stated basis. Subagent passes scenarios that failed in RED."
    on_failure: "Scenarios still fail → skill doesn't address the right rationalizations. Back to RED captures."

  - id: author_refactor
    action: "REFACTOR — Plug holes and build rationalization table"
    instruction: |
      1. Run combined-pressure scenarios (time + sunk cost + exhaustion)
      2. Capture NEW rationalizations, add explicit counters
      3. Build rationalization table (prolepsis — pre-refute evasions):
         | Excuse | Reality |
         | "{exact phrase from baseline}" | {short refutation} |
         Include only observed entries. Use agent's exact words, not invented quotas.
      4. Add red flags list quoting the THOUGHT not the behavior
      5. Re-test within the declared finite budget; unresolved failures remain open

      Three enforcement primitives (see references/techniques.yaml):
      - Prolepsis: rationalization table pre-refutes evasions
      - Positioned commands: validation strings become executable
      - Procedural chains: step IDs create presuppositional sequences
    validation: "Required cases pass within budget or pending failures and evidence gaps are explicit."
    on_failure: "Record the remaining obligation and stop the trial series at its budget."
```

## Workflow 3: Extraction Pipeline

```yaml
steps:
  - id: extract_prior_art
    action: Check if this skill already exists
    instruction: |
      `ls ~/.agents/skills/ | grep -i "{name}"` and `rg -l "{name}" ~/.agents/skills/*/SKILL.md`
      Exact match → enhance existing. Partial overlap → recommend merge. No match → proceed.
    validation: "Prior art search completed. Decision: new / enhance / merge."
    on_failure: "Search unavailable → proceed as new, note the gap."

  - id: extract_source
    action: Extract raw content
    instruction: |
      | Source  | Command                                              |
      |---------|------------------------------------------------------|
      | Website | skill-seekers scrape --name {name} --url {url}       |
      | GitHub  | skill-seekers github --repo {owner/repo}             |
      | PDF     | skill-seekers pdf --pdf {file} --name {name}         |
      | Multi   | skill-seekers unified --config {config.json}         |
      Not installed? `command -v skill-seekers` — see references/setup.md.
    validation: "output/{name}/ directory exists with extracted content"
    on_failure: "Check installation. See references/troubleshooting.md."

  - id: extract_enhance
    action: Enhance and apply authoring standards
    instruction: |
      Bug in skill-seekers ≤2.7.4: use scripts/enhance-workaround.sh output/{name}
      Then apply author_green rules: trigger-only description, proportionate context, and validation on every step.
      Package: `echo "y" | skill-seekers package output/{name}/ [--target claude|gemini|openai|markdown]`
      Then follow intake_score → intake_catalog for installation.
    validation: "SKILL.md has YAML frontmatter, description starts with 'Use when', and every operative step has a concrete validation check"
    on_failure: "Enhancement failed. Manually apply author_green standards."
```

## Workflow 4: Security Scan

```yaml
steps:
  - id: security
    action: Run 3-scanner security audit (sequential, early termination)
    instruction: |
      Scanner 1 — Structural Decompile (instant):
      `python3 ~/.agents/skills-db/security/skill-decompile/decompile.py "$file" --output yaml`
      risk_score >= 60 → HARD REJECT.

      Scanner 2 — Semantic Scan (~10s):
      Load security-scanner skill in sandboxed read-only subagent. Checks malicious NL, social engineering.

      Scanner 3 — AgentShield (~5s):
      `npx ecc-agentshield scan --path "$staged_dir" --min-severity medium`

      All pass → proceed. S1 pass + S2/S3 warn → user confirmation. Any hard fail → REJECT + quarantine.
      Full rubric: references/security-audit-gates.md
    validation: "All 3 scanners ran. Verdict recorded as PASS, WARN, or REJECT."
    on_failure: "Tooling unavailable → flag UNAUDITED, require user sign-off before activation."
```

## Workflow 5: Merge

For absorption into existing lifecycle owners, use a source-step ledger before
combining text. Each adopted instruction, result, insight and context technique
names its source, destination and represented/superseded/rejected disposition
with rationale; unresolved mappings remain gaps. Include referenced source
resources. Retaining an unchanged specialist is not proof its behavior reached
the lifecycle owner. Preserve source snapshots and keep duplicate activation
until source-disabled parity supports demotion. Prefer existing owner protocols
over a new router or parallel tracker. Domain-neutral versus SDLC-overlay rules
must remain explicit; eligible follow-ups use `skill://<name>` tables.

```yaml
steps:
  - id: merge
    action: Analyze overlap and produce merged skill
    instruction: |
      1. Read all source skills, identify trigger overlap (>30% = merge candidate)
      2. If the merged material fits one owner and context, keep one SKILL.md (LEAF or HUB).
      3. If a branch needs a separate context boundary, write a concise routing header plus independent sub-skills; add `skill_type: router` and `subsumes: [list]` only when the host supports those fields.
      4. Run author_red → author_green → author_refactor on the result
    validation: "Merged skill exists. No source triggers lost. Any split has a named branch trigger, destination and load check."
    on_failure: "Context boundary is unclear. Keep one owner or record the exact branch that requires a split."
```

## Workflow 6: Fractal Auto-Generation

```yaml
steps:
  - id: autogen_detect
    action: Detect repeated handler patterns that lack a dedicated skill
    instruction: |
      Sources of auto-generation signals (check in order):
      1. FlowMind flow metadata — skills can be emitted from typed flow YAML
         (ref: proposals/20260412-flowmind-typed-schemas.yaml)
      2. lifecycle-manifest.yaml — any verb without a matching skill is a scaffold candidate
      3. Agent telemetry — 3+ identical handler invocations across sessions = repetition signal
      Pattern: observe agent behavior → detect repetition → propose skill scaffold → validate → promote.
    validation: "At least one signal source checked. Candidate list is non-empty or explicitly empty."
    on_failure: "No signals found. Skip auto-generation. Do not fabricate candidates."

  - id: autogen_scaffold
    action: Generate candidate SKILL.md from detected pattern
    instruction: |
      Dogfood approach — pipe flow YAML to stdin, dry-run without writing:
      ```bash
      cat flow.yaml | lev skill scaffold --dry-run --from-flow -
      ```
      Output goes to stdout for review, never directly to disk.
      Scaffold must satisfy author_green rules: trigger-only description and validation on every step; use proportionate context and split only for a named branch.
      Reusable output templates must use live XML sections with Markdown prose inside, not fenced code blocks.
      For lifecycle verbs: extract the verb's handler signature as the skill's first step.
    validation: "Dry-run output parses as valid SKILL.md frontmatter + steps. Live XML sections wrap reusable templates. No files written."
    on_failure: "Scaffold invalid. Fix or discard. Never auto-promote broken output."

  - id: autogen_promote
    action: Validate scaffold and promote to intake pipeline
    instruction: |
      1. Run author_red baseline — does an agent fail WITHOUT this skill?
      2. If yes → run intake_score and intake_catalog (Workflow 1)
      3. If no → the pattern is not worth a skill. Archive the candidate.
      Auto-generated skills are NEVER activated without passing the full intake pipeline.
    validation: "Candidate either promoted through intake or archived with reason."
    on_failure: "Ambiguous value. Hold in _todo/ for human review."
```

## References

| Material | Load when |
|----------|-----------|
| [Setup](references/setup.md) | Extraction needs skill-seekers installation |
| [Troubleshooting](references/troubleshooting.md) | Setup or extraction fails |
| [Advanced commands](references/advanced-commands.md) | Large documentation, async processing or source splitting is needed |
| [Advanced workflows](references/advanced-workflows.md) | Extraction needs custom configs, agents or MCP integration |
| [Skill-seekers source README](references/skill-seekers-readme.md) | Verify a source-tool capability not covered by local commands; recheck live help |
| [Enforcement techniques](references/techniques.yaml) | Refactor or audit needs concrete validation and sequencing examples |
| [Technique archive](references/techniques-full.yaml) | Investigate provenance or a technique absent from the compact reference; claims remain unqualified |
| [Security gates](references/security-audit-gates.md) | Security workflow needs detailed scanner and quarantine rules |
| [Enhancement workaround](scripts/enhance-workaround.sh) | The verified affected skill-seekers version requires this workaround; inspect before authorized execution |

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "The prose edit is complete, so absorption is proven" | Qualification still needs source-obligation coverage and observed behavioral outcomes. |
| "This skill is obviously clear" | Clear to you ≠ clear to agents. Baseline proves it or it doesn't ship. |
| "Another authoring tool proves this skill works" | Authoring tools produce candidates; evaluate the actual installed instructions. |
| "This is too much context" | Identify the branch that needs it, move only on-demand detail behind a validated pointer, and preserve the operative rule inline. |
| "validation: strings are busywork" | Validation strings are the highest-leverage technique. Agents literally execute them. |
| "Operational instructions go in references/" | Agents don't cat references/. If it matters for execution, it lives in SKILL.md. |
| "Description should explain what the skill does" | Description = trigger conditions ONLY. Workflow summaries cause agents to shortcut the body. |
| "WebFetch can grab the SKILL.md content" | WebFetch summarizes. git clone and cp verbatim. Always. |

Load `references/techniques.yaml` when `author_refactor` or `--audit` needs
concrete examples of prolepsis, positioned validation or procedural chains.
Validate that pointer and the referenced example before relying on it; the
reference is reusable detail, not a hidden runtime dependency.
