---
name: cdo
description: "Adaptive multi-agent deliberation for cdo/think/deep/debug/parliament workflows."
skill_type: playbook
category: process-thinking
protocol_handlers:
  - lev://cdo?preset={quick|think|deep|full|debug}
plankton: false
metadata:
  triggers: [cdo, think, deliberate, parliament, multi-agent, deep analysis, debug rca]
  tools: [Read, Write, Edit, Bash, Grep, Glob, Agent]
---

# CDO — Adaptive Multi-Agent Deliberation

You are a ROUTER. You dispatch agents, collect artifacts, and route to synthesis.
You never think, analyze, or synthesize yourself. All reasoning happens in agents.

**The one rule you cannot break:** Turn N+1's shape comes from Turn N's synthesis
directive. You do not pre-plan turns. You do not override the directive. You read
the YAML block from synthesis and execute exactly what it says.

```yaml
steps:

  - id: parse_args
    action: "Parse invocation and resolve preset + modifiers + problem"
    instruction: |
      Parse the input: `/cdo <args,...> <problem>`

      Args are composable, comma-separated. Split tokens and classify:
        - Base preset: quick | think | deep | full | debug
        - Modifiers: hitl, bd, team, adaptive, lev-exec, exec
        - Domain: token after "exec" (dev, arch, or <tag>)
        - Problem: everything remaining

      If no preset specified, GAUGE the problem:
        - Single question, known domain → quick
        - Trade-off or design question → think
        - Multi-stakeholder or high-uncertainty → deep
        - Strategic or high-stakes → full
        - Bug, failure, unexpected behavior → debug

      If modifiers present but no preset → default to deep.
      If "debug" → ignore all modifiers (fixed protocol).
    validation: "preset variable is set to one of: quick, think, deep, full, debug"
    on_failure: "Ask the user to clarify what they want analyzed"

  - id: select_preset
    action: "Load preset config and resolve execution parameters"
    instruction: |
      Apply the preset table:

      | Preset | Width | Max Turns | BD  | Team Mode  | Dashboard | Convergence  |
      |--------|-------|-----------|-----|------------|-----------|--------------|
      | quick  | 1-2   | 1         | No  | Subagents  | No        | N/A          |
      | think  | 2-4   | 2-3       | No  | Subagents  | No        | Perspective  |
      | deep   | 3-8   | 3-5       | Yes | TeamCreate | Yes       | Confidence   |
      | full   | 5-20  | 5-10      | Yes | TeamCreate | Yes       | Resonance    |
      | debug  | 1-3   | 7 fixed   | No  | Subagents  | No        | Turn count   |

      Then apply modifiers — they override specific settings:
        - hitl: user checkpoint between every turn
        - bd: force beads tracking (`bd create epic "CDO: {problem}"`)
        - team: force TeamCreate even for quick/think
        - adaptive: width varies per turn based on synthesis
        - lev-exec: route roles to different models via codex/openrouter
        - exec <domain>: inject domain team shape for T1

      For deep+ or hitl: show planning dashboard before T1 — proposed DAG
      with turns, agents, roles, skills. Two seconds of preview saves minutes.

      Load sub-files only as needed (see references/architecture.md for table).
    validation: "width, max_turns, team_mode, and convergence_type are all set"
    on_failure: "Default to think preset if configuration is ambiguous"

  - id: execute_turns
    action: "Run the adaptive turn loop"
    instruction: |
      For each turn, execute this sequence:

      COMPOSE: Read previous synthesis directive (or problem statement for T1).
        - Decide width from directive (or preset default for T1)
        - Decide roles from directive (or preset/domain default for T1)
        - For deep+: discover 2-3 skills per agent via skill-discovery
        - Generate agent briefs with role, context, constraints, output format

      DISPATCH: Send agents in parallel.
        - Subagent mode: parallel Agent calls in single message
        - Team mode: SendMessage to teammates, spawn new if needed
        - Each agent writes to: tmp/cdo-{session}/t{N}-{role}.md
        - Agents cannot see each other's work during a turn

      SYNTHESIZE: Dispatch a dedicated synthesis agent (never yourself).
        - Reads ALL turn N artifacts from disk
        - Produces: common ground, tensions, gaps, surprises
        - Anti-groupthink: if >70% agreement, auto-add devil's advocate next turn
        - Emits YAML directive block:
            confidence: <float>
            convergence_met: <bool>
            gaps: [list]
            tensions: [list]
            recommended_next_turn:
              width: <int>
              agents: [{role, skills, focus}]

      ADAPT: Check exit criteria.
        - confidence >= threshold AND convergence_met → go to synthesize_final
        - Max turns reached → go to synthesize_final (forced)
        - All tensions resolved, no new gaps in 2 consecutive turns → synthesize_final
        - hitl active → present updated dashboard, user decides
        - Otherwise → next turn using the directive
    validation: "Each turn has artifact files on disk AND a synthesis with YAML directive block"
    on_failure: "If synthesis missing, re-dispatch synthesis agent. If agents produced no output, check briefs and re-dispatch with clearer constraints."

  - id: synthesize_final
    action: "Produce FINAL.md — the only user-facing deliverable"
    instruction: |
      Dispatch the final synthesis agent. It reads ALL artifacts across ALL turns.

      FINAL.md contains:
        - Decision/Answer: the actual output
        - Confidence: numeric + qualitative
        - Key Tensions: what was debated, what won, why
        - Minority Reports: dissenting views preserved, not buried
        - Action Items: concrete next steps if applicable

      If bd tracking active: close the epic.
      Turn artifacts are audit trail only — FINAL.md is the deliverable.
    validation: "FINAL.md exists at tmp/cdo-{session}/FINAL.md with all five sections"
    on_failure: "Re-run final synthesis with explicit section checklist in the brief"
```

# Debug Preset — 7-Turn RCA Protocol

When preset is "debug", ignore the adaptive loop above and run this fixed sequence:

```yaml
debug_steps:

  - id: debug_reproduce
    action: "T1 REPRODUCE — define exact failure condition"
    instruction: |
      Dispatch reproduction specialist. Output: exact steps, expected result,
      actual result, environment. No theorizing, no fixes. Just reproduce.
      Load modes/debug.md for full protocol.
    validation: "01-reproduce.md exists with reproduction steps and confidence level"
    on_failure: "Cannot proceed without reproduction. Ask user for more context."

  - id: debug_isolate
    action: "T2 ISOLATE — find minimal failing case"
    instruction: |
      Dispatch isolation specialist. Strip away everything unnecessary.
      Find the smallest case that still fails.
    validation: "02-isolate.md exists with minimal reproduction and isolation boundary"

  - id: debug_trace
    action: "T3 TRACE — parallel call path + working code comparison"
    instruction: |
      Two agents in parallel:
        Agent A: Trace exact execution path, find divergence point
        Agent B: Find nearest working code path, compare structural differences
    validation: "Both 03a-call-path.md and 03b-working-code.md exist"

  - id: debug_hypothesize
    action: "T4 HYPOTHESIZE — form 2-3 evidence-backed theories"
    instruction: |
      Dispatch hypothesis agent. Exactly 2-3 theories, each citing evidence
      from T3 traces. Ranked by likelihood. No fixes proposed yet.
    validation: "04-hypotheses.md exists with 2-3 hypotheses, each with evidence citations"

  - id: debug_verify
    action: "T5 VERIFY — test each hypothesis"
    instruction: |
      Test each hypothesis. Check predictions, attempt temporary modifications.
      Mark each as CONFIRMED, ELIMINATED, or INCONCLUSIVE.
      Exactly one should be CONFIRMED. If zero → return to T4.
    validation: "05-verified.md exists with exactly one CONFIRMED root cause"
    on_failure: "Return to debug_hypothesize with new evidence from verification"

  - id: debug_fix
    action: "T6 FIX — apply minimal fix"
    instruction: |
      Fix ONLY the confirmed root cause. No refactoring. No improvements.
      No touching unrelated files. If fix exceeds ~20 lines, justify.

      THE 3-FIX ESCALATION RULE:
      Count how many fix attempts have been made for this bug.
      If this is fix attempt 3 or higher → STOP. Do not attempt another fix.
      3+ failed fixes means the architecture is wrong, not the fix.
      Report to user: "3 fixes failed. This is an architectural problem, not
      a bug. Here's what each attempt revealed about the underlying design."
    validation: "06-fix.md exists with files changed, rationale, and scope check"
    on_failure: "If 3+ fixes failed, skip to FINAL with architectural assessment instead of fix"

  - id: debug_validate
    action: "T7 VALIDATE — adversarial validation"
    instruction: |
      Dispatch adversarial validator. Try to break the fix:
        1. Original reproduction case passes?
        2. Edge cases that could still trigger the bug?
        3. Regression — did fix break anything else?
        4. Root cause addressed, not just symptom?
      Verdict: PASS or FAIL. No partial pass. No "looks good enough."
    validation: "FINAL-validation.md exists with PASS or FAIL verdict"
    on_failure: "If FAIL, return to the T-step indicated by the validator. Do not restart from T1."
```

# User Signal Awareness

When the user says any of these, STOP your current approach immediately:

```yaml
  signals:
    - trigger: "Stop guessing"
      meaning: "You are proposing actions without evidence"
      response: "Drop current approach. Return to evidence gathering. Read code, run commands, trace data flow."

    - trigger: "Ultrathink this"
      meaning: "You are treating symptoms, not causes"
      response: "Widen scope. Question the framing. Is the problem statement itself wrong? Are you solving the right problem?"

    - trigger: "We're stuck?"
      meaning: "Your approach is failing and you haven't acknowledged it"
      response: "Admit the approach isn't working. Enumerate what you've tried and what each attempt revealed. Propose a fundamentally different angle."

    - trigger: "Just do it" / "Ship it"
      meaning: "Over-deliberating. The answer is clear enough."
      response: "Skip remaining turns. Emit FINAL.md from current state. Done."

    - trigger: "More agents" / "Go wider"
      meaning: "Current perspective set is too narrow"
      response: "Double width on next turn. Add roles not yet represented."

    - trigger: "Focus" / "Narrow down"
      meaning: "Too scattered, too many threads"
      response: "Cut width to 1-2 on next turn. Pick the highest-tension thread only."
```

# Anti-Patterns — Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Let me synthesize the agents' output myself" | You are the router. Synthesis is always a separate agent. Dispatch it. |
| "I'll plan all turns upfront for efficiency" | Pre-planning defeats adaptive deliberation. Turn N+1 comes from Turn N's synthesis. |
| "The agents mostly agree, so we're done" | >70% agreement is a groupthink smell. Add a devil's advocate, don't exit. |
| "I'll skip the dashboard for this one" | Dashboard catches bad composition before you waste 5 agent calls. Show it. |
| "This is simple enough for CDO" | If the answer fits in one sentence, just answer it. CDO is for genuine multi-perspective problems. |
| "I'll just run one more fix attempt" | 3 failed fixes = wrong architecture. Stop fixing. Report the pattern. |
| "The directive says X but I think Y is better" | You do not override the synthesis directive. Ever. Execute what it says. |
| "I'll let agents see each other's work for context" | Independence produces genuine diversity. Cross-pollination happens only through synthesis. |
