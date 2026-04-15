---
name: cdo
description: "Adaptive multi-agent deliberation for cdo/think/deep/debug/parliament workflows. Fractal context loop (CONTEXT→PLAN→ACT→VERIFY) at every level. Mandatory Turn 0 context gathering (skills, codebase, web). Convergence requires evidence, not just agreement. Use autoresearch/adaptive-runtime for long CDOs that need scheduler state, hard minimum turns, hard minimum agent counts, and pause/resume."
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
        - Modifiers: hitl, bd, team, adaptive, autoresearch, adaptive-runtime, lev-exec, exec
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
        - autoresearch | adaptive-runtime: use codex-autoresearch as the long-run scheduler/runtime for CDO. CDO still owns reasoning; autoresearch owns run state, counters, health checks, pause/resume, and exit-gate enforcement.
        - lev-exec: route roles to different models via codex/openrouter
        - exec <domain>: inject domain team shape for T1

      For deep+ or hitl: show planning dashboard before T1 — proposed DAG
      with turns, agents, roles, skills. Two seconds of preview saves minutes.

      Load sub-files only as needed (see references/architecture.md for table).
    validation: "width, max_turns, team_mode, and convergence_type are all set"
    on_failure: "Default to think preset if configuration is ambiguous"

  - id: resolve_autoresearch_scheduler_mode
    action: "If requested, convert CDO into a scheduler-managed autoresearch run"
    instruction: |
      If `autoresearch` or `adaptive-runtime` is present, OR if the problem declares hard scheduling KPIs (`min_turns`, `min_total_agents`, `skills_per_agent`), enter CDO Autoresearch Scheduler Mode.

      This mode is for long-running deliberation only. It is not a normal CDO preset.

      Load the `codex-autoresearch` skill as the runtime contract:
        - `references/core-principles.md`
        - `references/runtime-hard-invariants.md`
        - `references/loop-workflow.md`
        - `references/pivot-protocol.md`
        - `references/health-check-protocol.md`
        - `references/parallel-experiments-protocol.md`

      Then initialize a scheduler state object before Turn 1:

      ```yaml
      cdo_scheduler:
        mode: autoresearch
        run_tag: "cdo-{slug}"
        min_turns: 10              # default for deep unknowns runs unless user specifies otherwise
        min_total_agents: 50       # default for deep unknowns runs unless user specifies otherwise
        skills_per_agent: 2        # default when user requests skill rotation
        adaptive_turn_width: true
        turn_count: 0
        total_agents: 0
        unique_skills: []
        open_tensions: []
        exit_eligible: false
      ```

      The scheduler state is the run contract. The DAG is not.

      Hard rules in this mode:
        - Do not plan all turns upfront.
        - Do not pre-generate a 50-agent roster as the execution plan.
        - Plan only the next scheduling quantum.
        - Every turn chooses strategy from current evidence, open tensions, remaining metrics, and health checks.
        - Final synthesis is blocked until `turn_count >= min_turns` AND `total_agents >= min_total_agents`, unless the user explicitly interrupts with "ship it", "just do it", or another clear stop signal.
        - Each turn must emit a scheduler update.

      Scheduler update format:

      ```yaml
      scheduler_update:
        turn_count: <int>
        agents_this_turn: <int>
        total_agents: <int>
        skills_used_this_turn: [skill-id]
        unique_skills: [skill-id]
        exit_eligible: <bool>
        remaining_turns_min: <int>
        remaining_agents_min: <int>
        next_turn_strategy: research | fanout | debate | negotiate | synthesize | devil_advocate | reduce | checkpoint
      ```

      The mental model is CPU scheduling:
        - a turn is a scheduling quantum
        - agents are runnable tasks
        - skill pairs are execution contexts
        - synthesis is scheduler feedback
        - hard metrics are exit gates
    validation: "If autoresearch/adaptive-runtime or hard scheduling KPIs are present, cdo_scheduler exists and final synthesis is blocked until hard metrics are met"
    on_failure: "Do not continue with normal CDO. Rebuild scheduler state and continue from the next turn."

  - id: execute_turns
    action: "Run the adaptive turn loop"
    instruction: |
      For each turn, execute this sequence:

      COMPOSE: Read previous synthesis directive (or problem statement for T1).
        - Decide width from directive (or preset default for T1)
        - Decide roles from directive (or preset/domain default for T1)
        - For deep+: discover 2-3 skills per agent via skill-discovery
        - Generate agent briefs with role, context, constraints, output format
        - In Autoresearch Scheduler Mode: first read `cdo_scheduler`, compute unmet metrics, then decide this turn's width and strategy. Do not follow a preplanned roster if current evidence says to change strategy.

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
            scheduler_update: {turn_count, agents_this_turn, total_agents, unique_skills, exit_eligible, remaining_turns_min, remaining_agents_min, next_turn_strategy}

      ADAPT: Check exit criteria.
        - confidence >= threshold AND convergence_met → go to synthesize_final
        - Max turns reached → go to synthesize_final (forced)
        - All tensions resolved, no new gaps in 2 consecutive turns → synthesize_final
        - hitl active → present updated dashboard, user decides
        - Autoresearch Scheduler Mode: even if confidence is high, final synthesis is blocked until hard scheduler metrics are met. If progress stalls for 3 consecutive turns, use codex-autoresearch pivot/refine escalation instead of brute-force repeating the same fanout.
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
| "I'll write a complete 50-agent roster and execute it" | In autoresearch/adaptive-runtime mode, the roster is only a candidate queue. The scheduler chooses the next quantum from live evidence and unmet metrics. |
| "The agents mostly agree, so we're done" | >70% agreement is a groupthink smell. Add a devil's advocate, don't exit. |
| "I'll skip the dashboard for this one" | Dashboard catches bad composition before you waste 5 agent calls. Show it. |
| "This is simple enough for CDO" | If the answer fits in one sentence, just answer it. CDO is for genuine multi-perspective problems. |
| "I'll just run one more fix attempt" | 3 failed fixes = wrong architecture. Stop fixing. Report the pattern. |
| "The directive says X but I think Y is better" | You do not override the synthesis directive. Ever. Execute what it says. |
| "I'll let agents see each other's work for context" | Independence produces genuine diversity. Cross-pollination happens only through synthesis. |

# Fractal Context Loop (CONTEXT → PLAN → ACT → VERIFY)

Every layer of CDO execution follows the same loop. Context gathering comes FIRST — you cannot plan what you don't understand. This is non-negotiable.

```yaml
fractal_loop:
  description: "The same cycle applies at every level of the CDO"
  levels:
    session:
      context: "Turn 0 — gather evidence: read code, search cass, web research, acquire skills"
      plan: "Gauge problem, select preset, compose DAG from what you learned"
      act: "Execute turns per synthesis directives"
      verify: "Final synthesis confirms convergence with evidence"

    turn:
      context: "Calibrate context depth per agent, discover relevant skills, read actual files"
      plan: "Read synthesis directive, compose agent briefs with gathered context"
      act: "Dispatch agents in parallel"
      verify: "Synthesis checks for evidence, not just agreement"

    agent:
      context: "Scan codebase/docs/web per calibrated depth BEFORE forming opinions"
      plan: "Agent identifies approach based on what it actually read"
      act: "Agent produces artifact with citations"
      verify: "Agent self-checks: did I cite evidence or reason abstractly?"
```

## Skill Acquisition (Part of Context Phase)

Before planning any CDO, discover which skills are relevant. This is context gathering, not planning.

```yaml
skill_acquisition:
  purpose: "Surface the right skills from 800-1000 available before composing agent briefs"
  methods:
    1_decompose_to_tags:
      action: "Break the problem into keyword tags"
      example: "protocol design → [protocol, interop, agent, registry, manifest, capability, discovery, mesh]"

    2_search_skills_db:
      action: "rg the tags across ~/.agents/skills/ and ~/.agents/skills-db/"
      command: "rg -l '<tag>' ~/.agents/skills/ ~/.agents/skills-db/ --type md | head -20"
      fallback: "If rg misses, try ~/.agents/lev-skills.sh or skill-discovery skill"

    3_check_thinking_patterns:
      action: "Browse ~/.agents/skills-db/thinking/patterns/ for relevant mental models"
      example: "protocol design → mechanism-design, protocol-networks, nash-equilibrium, requisite-variety"

    4_inject_into_briefs:
      action: "Each CDO agent gets 1-3 relevant skills injected as context in their system prompt"
      rule: "Skills are context, not instructions. The agent reads the skill to understand patterns, not to follow a script."

  anti_pattern: "Dispatching CDO agents without checking what skills exist is like coding without reading the docs."
```

## Turn 0 — Mandatory Research Phase

Before Turn 1 dispatches any deliberation agents, execute a research phase:

```yaml
turn_0:
  purpose: "Establish ground truth before opinions form"
  actions:
    - "Read actual source code relevant to the problem"
    - "Check cass for prior session evidence"
    - "Web search for prior art if the problem involves external standards"
    - "Generate a context manifest: files read, facts established, unknowns identified"
  output: "tmp/cdo-{session}/t0-research.md"
  rule: "Turn 1 agents receive t0-research.md as part of their brief"
```

## Context Depth Calibration

Not every agent needs 112k tokens. Calibrate per problem shape:

```yaml
context_depth:
  trivial:
    signal: "1 file, known path, clear answer"
    tools: "Read the file directly"
    cost: "~100 tokens of context"

  focused:
    signal: "2-5 files, clear scope"
    tools: "grep + glob, maybe 1 explore agent"
    cost: "~2k tokens of context"

  broad:
    signal: "Unknown scope, multiple modules"
    tools: "rp-cli context_builder OR multi-agent explore"
    cost: "~20k-50k tokens of context"

  deep:
    signal: "Protocol design, architecture review, cross-cutting"
    tools: "rp-cli + web research + cass history + prior art scan"
    cost: "~100k+ tokens of context"
```

## Convergence Requirements

Convergence now requires EVIDENCE, not just agreement:

```yaml
convergence_check:
  required:
    - "All blocking tensions resolved"
    - "At least 1 agent cited specific code/docs (not abstract reasoning)"
    - "Anti-groupthink check passed (>70% agreement triggers devil's advocate)"

  skeptical_convergence:
    rule: "Before declaring convergence, ask: what did we ASSUME without evidence?"
    action: "If any assumption is load-bearing and unverified, add a depth probe turn"
    budget: "Use all budgeted turns. Early convergence is a smell, not a feature."
```

## Delegation with Budget Inheritance (from Hermes, Wave 5 — hm-05)

When dispatching child agents in the `team` modifier mode, apply these constraints borrowed from Hermes delegation semantics:

```yaml
child_agent_contract:
  iteration_budget: <int>        # max turns child can run autonomously
  tool_inheritance: <bool>       # inherits parent's available tools by default
  skip_memory: <bool>            # optionally isolate child from shared memory
  return_on: [done, budget_exceeded, blocked]
```

**Why this matters**: Standard CDO dispatch doesn't cap per-child work. Hermes's model gives each child agent its own iteration budget, inherits tools from parent, and can optionally skip shared memory to enforce isolation. Parent sets constraints; child executes autonomously within them.

Practical application: use `iteration_budget: 3` for quick sub-tasks in a `team` preset CDO. Use `skip_memory: true` when you need clean deliberation without contaminating session state from one child spilling into another.

Source: `.lev/pm/parity/hermes.yaml`

## Per-Entity Expert Agents

When the problem has distinct entities (e.g., multiple runners, multiple modules, multiple protocols), spawn a specialist agent per entity:

```yaml
per_entity_experts:
  trigger: "Problem involves 3+ distinct entities that each have their own docs/code"
  action: "Spawn 1 expert agent per entity who reads that entity's actual documentation"
  example: "Protocol design → Claude Expert, Codex Expert, Gemini Expert (each reads real docs)"
  why: "Generic reasoning misses entity-specific behavior. ChatGPT beat CDO on this."
```

## Meta-Agent: "What Would Deep Research Find?"

Add this agent to any `deep` or `full` CDO:

```yaml
meta_agent:
  role: "Deep Research Proxy"
  prompt: "If a single model with 100k+ tokens of real source code were analyzing this problem, what would it find that our multi-agent survey missed?"
  when: "deep or full preset, Turn 2+"
  why: "Multi-agent CDO excels at breadth and adversarial testing. Single-model deep research excels at ground truth. This agent forces CDO to consider what it's missing."
```

## Implementation Spike Agents Early

Don't wait until Turn 2+ for real probes:

```yaml
early_spikes:
  rule: "Turn 1 should include at least 1 agent that actually RUNS something"
  examples:
    - "Invoke the binary with --help and parse the output"
    - "Read the actual source file and report what it exports"
    - "Run a test and report what passes/fails"
  why: "Abstract reasoning about code you haven't read produces hallucinated architectures (see: lev-builder fabricated paths)"
```

## Negotiate Phase (Claim vs Reality)

From the ChatGPT vs CDO comparison: CDO agents reason abstractly about what code CAN do. ChatGPT reads the code and knows what it ACTUALLY does. The negotiate phase closes that gap.

```yaml
negotiate:
  trigger: "Any turn where agents make architectural claims"
  process:
    1: "Agent makes a claim: 'ExecTransport handles this'"
    2: "Negotiate agent reads the actual code (grep, read file)"
    3: "Reports fidelity: exact (code does this) | approximate (partial) | rejected (code doesn't do this)"
  output: "Annotated claims with fidelity scores"

  fidelity_levels:
    exact: "Code confirms the claim. Agent cited the right file and function."
    approximate: "Code partially supports the claim. Missing pieces identified."
    rejected: "Code contradicts the claim. Agent was reasoning abstractly."

  rule: "For deep+ presets, add a negotiate agent to Turn 2+ that reads actual code to verify Turn 1 claims. This is the single biggest quality improvement from the ChatGPT comparison."

  anti_pattern: "Accepting architectural claims without code evidence is the #1 cause of CDO producing designs that don't fit the codebase."
```

## Structured Debate Mode

When a CDO has two clear opposing positions (not just multiple perspectives), use debate format instead of independent analysis:

```yaml
debate:
  trigger: "Binary architectural question — e.g., 'should X live in poly or domain?'"
  structure:
    round_1:
      - "Advocate A argues FOR position 1 (with code evidence)"
      - "Advocate B argues FOR position 2 (with code evidence)"
    round_2:
      - "Advocate A rebuts B's strongest point"
      - "Advocate B rebuts A's strongest point"
    round_3:
      - "Synthesis agent reads all 4 artifacts, picks winner with reasoning"

  rules:
    - "Each advocate MUST cite actual files/functions, not abstract principles"
    - "Rebuttals must address the other side's evidence, not restate their own"
    - "Synthesis must explain why the losing position was wrong, not just why the winner was right"

  when_to_use: "Module placement, protocol ownership, 'should this exist?', binary trade-offs"
  when_NOT_to_use: "Open-ended design (use standard CDO width), research tasks, debugging"
```

## Depth vs Breadth Gauge

Add this to the parse_args step:

```yaml
depth_breadth_gauge:
  question: "Does this problem need per-entity depth, or architectural breadth?"
  per_entity_depth:
    signal: "Multiple implementations of the same concept (runners, adapters, protocols)"
    action: "Spawn per-entity experts. Reduce breadth agents. Add research phase."
  architectural_breadth:
    signal: "Cross-cutting concern, module placement, trade-off analysis"
    action: "Standard CDO breadth. Multiple perspectives. No per-entity drill."
  both:
    signal: "Protocol design, system unification"
    action: "Research phase (depth) + CDO turns (breadth). Budget 5 turns minimum."
```
