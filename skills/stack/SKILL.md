---
name: stack
description: Use when listing, inspecting, running, or managing prompt-stack sessions. Triggers on "stack", "list stacks", "show stack", "init stack", "run stack", "stack status".
---

# Stack

Thin launcher for the prompt-stack runtime at
`$HOME/digital/leviathan/plugins/prompt-stack`.

Runtime ownership stays with the plugin. This skill teaches agents how to
call it correctly and present results as a dashboard, not raw JSON.

## Autopilot Rule

When the user says `/stack next`, treat it as an autopilot command, not a checkpoint request.

- Prefer the most recent active session for the current project before initializing a new stack.
- If an active session exists:
  1. run `next` or `status` to confirm the true active step
  2. finish that step
  3. run `record`
  4. immediately follow the CLI response
  5. continue until the stack completes or a real blocker occurs
- Do not stop after each successful step to ask for permission to continue.
- Send short progress updates, but keep the session moving.

Only stop for:
- missing required artifact or context that cannot be inferred from disk
- contradictory session state after re-checking with `status`
- failed `record` that cannot be corrected locally
- a true product decision that is not covered by existing plan/spec/proposal artifacts

## Run Modes

Once launch is approved, do not ask again until completion or blocker.

- `foreground` = current agent/session drives the run in-process through the returned CLI contract
- `background` = detached execution managed by prompt-stack and `lev exec`
- chained runs continue across stacks without stopping
- blockers come from merged runtime + project + invocation policy

## Hard Rules

- Respect the chosen run mode after launch approval.
- Never ask “should I continue?” after go.
- Stack session serialization stays single-writer per session.
- Git checkpoint serialization stays single-writer per repo through `.lev/steering/checkpoint.lock`.
- Use the prompt-stack checkpoint helper, not ad hoc repo-local scripts.

## Checkpoint Mode

Use the canonical prompt-stack helper layer when multiple runs share one repo and need serialized git checkpoints:

```bash
cd $HOME/digital/leviathan

prompt-stack checkpoint-lock status --project-dir <path>
prompt-stack checkpoint-lock acquire --project-dir <path> --owner-tag <tag>
prompt-stack checkpoint-lock release --project-dir <path> --owner-tag <tag>
```

Rules:

- concurrent prompt-stack runs keep runtime state under `.lev/steering/runs/<run-id>/...`
- git checkpointing is serialized through `.lev/steering/checkpoint.lock`
- dirty worktrees are warning-only, not automatic blockers

## Session Serialization

A stack session is single-writer state.

- Never run `next`, `record`, `status`, or `validate` in parallel against the same session.
- Always use this order:
  1. `status` or `next`
  2. do the step work
  3. `record`
  4. `status` or `next` again
  5. repeat
- After any interruption, timeout, or aborted turn, re-run `status` and trust the session file over memory.

## Dashboard Mode (`/stack list`)

When the user says `/stack list`, do NOT dump raw JSON. Instead:

1. Run `cd $HOME/digital/leviathan && bun plugins/prompt-stack/src/cli.ts list`
2. Parse the JSON response
3. Format as a grouped dashboard — one line per stack:

```
━━━ CORE-LEV (9 stacks) ━━━

  handoff              (4 steps)  gather → distill → write → validate
  lev-align            (4 steps)  load north-star → inspect → classify drift → propose action
  plan-align-gates     (5 steps)  governance → refresh plan → align canon → gates → emit proposal
  research-propose-spec(3 steps)  research evidence → proposal synthesis → spec crystallization
  validate-emit-learn  (4 steps)  review artifacts → validate → emit → capture learnings
  work-deepen          (5 steps)  decompose → discover skills → parallel research → review → brief
  work-full-lifecycle  (9 steps)  governance → plan → align → gates → proposal → review → validate → emit → learn
  work-proof-loop      (3 steps)  handoff update → spec delta → validation report
  robot-readme-harden  (3 steps)  robot-mode hardening → cli error tolerance → readme sync

━━━ JEFF (5 stacks) ━━━

  jeff-delivery-loop   (10 steps) primer → ideation → synthesis → premortem → robot → cli → readme → review → e2e → commit
  jeff-ideation-risk   (4 steps)  idea wizard → multi-model synthesis → premortem → readme
  jeff-primer-quality  (4 steps)  deep primer → e2e validator → peer review → bug hunter
  jeff-quality-gauntlet(5 steps)  bug hunter → peer review → e2e → deploy verify → de-slopify
  jeff-robot-launch    (4 steps)  robot-mode → idea wizard → readme → git commit

━━━ SDLC (7 stacks) ━━━

  sdlc-deepen-plan     (3 steps)  decompose → parallel research → synthesize
  sdlc-exec-validate   (3 steps)  implement → fitness functions → route verdict
  sdlc-handoff-close   (4 steps)  verify handoff → extract decisions → approve → process
  sdlc-handoff-rollup  (4 steps)  scan unprocessed → pick one → extract all → process items
  sdlc-hygiene         (4 steps)  scan staleness → check alignment → propose updates → report
  sdlc-plan-to-beads   (5 steps)  extract items → create issues → review pass 1 → pass 2 → pass 3
  sdlc-spec-lifecycle  (5 steps)  validate completeness → check transition → quality gates → route → approve/iterate

━━━ OTHER ━━━

  knowledge-6r         (6 steps)  record → reduce → reflect → reweave → verify → rethink
  drift-detection      (5 steps)  positive drift → negative → undocumented → stale → alignment
  spec-driven-dev      (5 steps)  detect divergence → classify → push/pull → arbitrate → sync
  cass-cm-audit        (6 steps)  health check → memory scan → playbook audit → gap analysis → reindex → report
  research-worker      (3 steps)  orient → research rounds → synthesize
```

4. After the full list, add context-aware suggestions:

```
━━━ SUGGESTED FOR CURRENT CONTEXT ━━━

Based on: {describe what you detected — active handoff, case folder, recent work}

  (1) {stack-id}  — {why this stack fits right now}
  (2) {stack-id}  — {why}
  (3) {stack-id}  — {why}

  (s)how <id>  — Inspect a specific stack
  (r)un <id>   — Init a session immediately
```

Context detection rules:
- `.lev/osint/` exists → suggest `research-worker`, `work-deepen`
- `.lev/pm/handoffs/` has unprocessed handoffs → suggest `sdlc-handoff-rollup`
- Conversation mentions case/legal/research → suggest `jeff-ideation-risk`, `research-propose-spec`
- Recent code changes or implementation work → suggest `jeff-quality-gauntlet`, `sdlc-exec-validate`
- Session ending or handoff requested → suggest `handoff`, `validate-emit-learn`
- First time seeing the stacks → suggest `work-deepen`, `jeff-ideation-risk`, `sdlc-exec-validate`

## Commands

```bash
cd $HOME/digital/leviathan

# List (then format as dashboard above)
bun plugins/prompt-stack/src/cli.ts list

# Inspect (show steps, schemas, no hidden prompts)
bun plugins/prompt-stack/src/cli.ts show <stack-id>

# Init session
bun plugins/prompt-stack/src/cli.ts init --stack <stack-id> --project-dir <path>

# Get active step prompt
bun plugins/prompt-stack/src/cli.ts next --session <id> --project-dir <path>

# Record step output (validates and advances)
bun plugins/prompt-stack/src/cli.ts record --session <id> --step <step-id> --report <path> --project-dir <path>

# Check progress
bun plugins/prompt-stack/src/cli.ts status --session <id> --project-dir <path>

# Validate completed session
bun plugins/prompt-stack/src/cli.ts validate --session <id> --project-dir <path>
```

## Workflow

1. `/stack list` → dashboard with suggestions
2. User picks a stack (by number or name)
3. `init --stack <id>` → creates session
4. `next --session <id>` → reveals active step prompt
5. Agent does the work, writes report matching schema
6. `record --session <id> --step <step-id> --report <path>` → validates + advances
7. Repeat 4-6 until all steps complete
8. `validate --session <id>` → checks lifecycle integrity

For `/stack next`, steps 4-8 are one continuous autopilot loop. Do not pause between them unless blocked.

## Skill Discovery Integration

Before executing the first step of any stack, run `lev-skills <domain>` to surface
relevant skills from the skills-db. The domain is inferred from context:

- Stack family `legal-osint` → `lev-skills legal`
- Stack family `sdlc` → `lev-skills sdlc`
- Stack family `jeff` → skip (jeff prompts are self-contained)
- Active case folder detected → `lev-skills` with case domain keywords
- Unknown → `lev-skills` with the stack's `title` as query

Inject discovered skill names + one-line descriptions into the first step's context.
Workers then know what specialized skills are available during execution.

## Operator Notes

- Always use absolute paths for `--project-dir` and `--report`
- Session state lives in `<project>/.lev/steering/sessions/`
- `record` REJECTS invalid reports — fix and re-submit
- Report format: YAML frontmatter + required sections (varies by stack)
- If part of active `$work` handoff, keep planning there — stack is execution only
- If the stack is being used inside active `$work`, stack state is **not** the only artifact. You must also persist the corresponding disk-backed `work` template artifact:
  - planning / execution slice -> `.lev/pm/plans/plan-*.md`
  - research lane -> `.lev/pm/reports/report-*.md`
  - shaping / architecture lane -> `.lev/pm/designs/*.md`, `.lev/pm/proposals/*.md`, or `.lev/pm/specs/*.md`
- For large or multi-workstream implementation planning, route through `writing-plans` and split independent workstreams into separate plan files. Do not keep one thin coordination plan where the actual execution detail belongs in child plans.
- A good default: stack session for runtime state, `work` artifact for durable repo state, handoff for continuity. All three should agree.
- For subagent orchestration: `plugins/prompt-stack/references/subagent-contract.md`

## References

- CLI: `plugins/prompt-stack/src/cli.ts`
- Catalog: `plugins/prompt-stack/prompts/prompt-stack.prompts.yaml`
- Subagent contract: `plugins/prompt-stack/references/subagent-contract.md`
- FlowMind path (optional): `plugins/prompt-stack/flows/prompt-stack.flow.yaml`
