---
name: skill-builder
description: Use when creating skills, converting docs/repos/PDFs to skills, installing external skills, auditing skill security, or merging skills
---

# Skill Builder

No skill ships without testing. RED baseline first, GREEN write second, REFACTOR plug holes third.
If you wrote a skill before watching an agent fail without it, delete it and start over.

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
      | "audit", "is this safe"       | Security Scan    | security    |
      | "merge these skills"          | Merge            | merge       |
      Ambiguous? Ask: "Are you converting existing material or authoring from scratch?"
    validation: "User intent classified into exactly one workflow"
    on_failure: "Ask a clarifying question. Do not guess."
```

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
    action: Score quality on 5 dimensions (1-10 each)
    instruction: |
      Actionability (concrete steps vs vague), Depth (expert vs surface), Structure (tables vs wall of text), Triggers (WHAT/WHEN + tags vs bare), Uniqueness (novel vs generic).
      A (8+) promote. B (7-7.9) promote with note. C (5-6.9) hold in _todo. D (<5) reject.
    validation: "Grade letter assigned. Destination directory determined."
    on_failure: "Default to C grade, hold in _todo for human review."

  - id: intake_catalog
    action: Move from staging to final location
    instruction: |
      A/B → `mv` to `~/.agents/skills-db/{domain}/{name}/`
      C → `mv` to `~/.agents/skills-db/_todo/{name}/`
      D → `mv` to `~/.agents/skills-db/.archive/{name}/`
      Activation to ~/.agents/skills/ happens ONLY if user explicitly requests it.
    validation: "Skill no longer in _workshop/. ls confirms new location."
    on_failure: "Check permissions and path. Retry mv."
```

## Workflow 2: Author from Scratch (TDD)

```yaml
steps:
  - id: author_red
    action: "RED — Establish baseline failure"
    instruction: |
      Before writing anything, run pressure scenarios WITHOUT the skill:
      1. Define 3+ scenarios testing what the skill should enforce
      2. Run each with a subagent (no skill loaded)
      3. Capture verbatim: what choices, what rationalizations (exact words), which pressures triggered violations
      This is the failing test. You must see what agents do wrong before writing a skill that fixes it.
    validation: "3+ baseline scenarios run. Rationalizations captured verbatim."
    on_failure: "You skipped baseline testing. Stop. Run the scenarios. No exceptions."

  - id: author_green
    action: "GREEN — Write minimal skill addressing observed failures"
    instruction: |
      Write SKILL.md addressing the specific rationalizations from RED.

      Format: YAML frontmatter + steps with id/action/instruction:/validation:/on_failure:
      - description starts with "Use when..." — trigger conditions ONLY, never workflow summary
      - Steps are verbs not states. "Search these sources" not "DISCOVER"
      - Inline templates at each step — if it produces an artifact, show the skeleton
      - First step = most important output, not background theory
      - Operational content lives in SKILL.md, not references/ (agents don't cat them)
      - validation: strings are concrete verifiable checks (commands or binary states)
      - Natural language in instruction blocks. Never LLM_MUST directives
      - Under 300 lines total. Prose is the enemy.

      Run the same pressure scenarios WITH the skill. Agent should now comply.
    validation: "wc -l SKILL.md under 300. All steps have validation: strings. Subagent passes scenarios that failed in RED."
    on_failure: "Scenarios still fail → skill doesn't address the right rationalizations. Back to RED captures."

  - id: author_refactor
    action: "REFACTOR — Plug holes and build rationalization table"
    instruction: |
      1. Run combined-pressure scenarios (time + sunk cost + exhaustion)
      2. Capture NEW rationalizations, add explicit counters
      3. Build rationalization table (prolepsis — pre-refute evasions):
         | Excuse | Reality |
         | "{exact phrase from baseline}" | {short refutation} |
         Minimum 5 entries. Use agent's exact words, not paraphrases.
      4. Add red flags list quoting the THOUGHT not the behavior
      5. Re-test until zero new rationalizations emerge

      Three enforcement primitives (see references/techniques.yaml):
      - Prolepsis: rationalization table pre-refutes evasions
      - Positioned commands: validation strings become executable
      - Procedural chains: step IDs create presuppositional sequences
    validation: "Rationalization table has 5+ real entries. Re-test produces zero new evasions."
    on_failure: "New rationalization found. Add to table. Re-test. Repeat until clean."
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
      Then apply author_green rules: trigger-only description, under 300 lines, validation on every step.
      Package: `echo "y" | skill-seekers package output/{name}/ [--target claude|gemini|openai|markdown]`
      Then follow intake_score → intake_catalog for installation.
    validation: "SKILL.md has YAML frontmatter, description starts with 'Use when', wc -l under 300"
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

```yaml
steps:
  - id: merge
    action: Analyze overlap and produce merged skill
    instruction: |
      1. Read all source skills, identify trigger overlap (>30% = merge candidate)
      2. If merged content ≤ 300 lines → single SKILL.md (LEAF or HUB)
      3. If > 300 lines → ROUTER: write <100L routing header + independent sub-skills
         Add `skill_type: router` and `subsumes: [list]` to frontmatter
      4. Run author_red → author_green → author_refactor on the result
    validation: "Merged skill exists. No source triggers lost. wc -l under ceiling."
    on_failure: "Too large. Split into router + sub-skills."
```

## References

| File | Content |
|------|---------|
| references/setup.md | Installation (uv/venv/pip auto-detection) |
| references/advanced-commands.md | Large docs, async, splitting |
| references/techniques.yaml | 3 enforcement primitives + evidence |
| references/security-audit-gates.md | Scoring rubric, quarantine protocol |
| scripts/enhance-workaround.sh | Fix for broken skill-seekers enhance |

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "I'll test the skill later" | Later = never. RED baseline BEFORE writing. Iron law. |
| "This skill is obviously clear" | Clear to you ≠ clear to agents. Baseline proves it or it doesn't ship. |
| "I'll just route to skill-creator" | There is no skill-creator. This IS the skill creator. Author workflow, step author_red. |
| "Too complex for 300 lines" | Cut prose. Lead with format. Move API docs to references/. 300 is the ceiling. |
| "validation: strings are busywork" | Validation strings are the highest-leverage technique. Agents literally execute them. |
| "Operational instructions go in references/" | Agents don't cat references/. If it matters for execution, it lives in SKILL.md. |
| "Description should explain what the skill does" | Description = trigger conditions ONLY. Workflow summaries cause agents to shortcut the body. |
| "WebFetch can grab the SKILL.md content" | WebFetch summarizes. git clone and cp verbatim. Always. |
