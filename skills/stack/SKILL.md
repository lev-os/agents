---
name: stack
description: Thin global wrapper for the Leviathan prompt-stack plugin runtime. Use when a user or agent wants to list, inspect, initialize, advance, record, validate, or otherwise run named prompt stacks through `plugins/prompt-stack` in `/Users/jean-patricksmith/digital/leviathan`.
---

# Stack

Use this skill as the thin launcher and operator guide for the standalone prompt-stack
runtime owned by the Leviathan plugin at
`/Users/jean-patricksmith/digital/leviathan/plugins/prompt-stack`.

Do not reimplement runtime behavior here. Do not edit plugin files unless the task
explicitly targets the plugin. This wrapper exists to teach agents how to call the
runtime correctly.

## When To Use

Use this skill when the request is about:

- running a named prompt stack
- listing or inspecting available stacks
- creating or advancing a prompt-stack session
- recording step output back into the runtime
- checking prompt-stack session status or validation

If the task is Leviathan-specific and tied to an active `$work` handoff, use that handoff
as the planning source of truth and use this skill only for the execution-plane prompt-stack loop.

## Runtime Surface

Preferred execution path:

```bash
cd /Users/jean-patricksmith/digital/leviathan
bun plugins/prompt-stack/src/cli.ts list
```

Core commands:

```bash
bun plugins/prompt-stack/src/cli.ts list [--project-dir PATH] [--catalog PATH]
bun plugins/prompt-stack/src/cli.ts show <stack-id> [--project-dir PATH] [--catalog PATH]
bun plugins/prompt-stack/src/cli.ts init --stack <stack-id> [--project-dir PATH] [--catalog PATH] [--flow PATH]
bun plugins/prompt-stack/src/cli.ts next --session <session-id> [--project-dir PATH]
bun plugins/prompt-stack/src/cli.ts record --session <session-id> --step <step-id> --report <path> [--project-dir PATH]
bun plugins/prompt-stack/src/cli.ts status --session <session-id> [--project-dir PATH]
bun plugins/prompt-stack/src/cli.ts validate --session <session-id> [--project-dir PATH]
```

Important runtime behavior:

- Session state is written under `<project>/.lev/steering/sessions/`.
- `show` returns stack metadata only. It does not reveal future prompt bodies.
- `next` reveals only the active step prompt.
- `record` advances the session using the report file you provide.
- `validate` checks the session lifecycle after execution.

## Minimal Workflow

1. Discover the available stacks.

```bash
cd /Users/jean-patricksmith/digital/leviathan
bun plugins/prompt-stack/src/cli.ts list
```

2. Inspect one stack without exposing hidden prompts.

```bash
bun plugins/prompt-stack/src/cli.ts show work-deepen
```

3. Create a session against the target project.

```bash
bun plugins/prompt-stack/src/cli.ts init \
  --stack work-deepen \
  --project-dir /absolute/project/path
```

4. Reveal the active step.

```bash
bun plugins/prompt-stack/src/cli.ts next \
  --session <session-id> \
  --project-dir /absolute/project/path
```

5. Save the step output to a report file, then record it.

```bash
bun plugins/prompt-stack/src/cli.ts record \
  --session <session-id> \
  --step <step-id> \
  --report /absolute/project/path/.lev/pm/reports/<report>.md \
  --project-dir /absolute/project/path
```

6. Check progress and validate the finished session.

```bash
bun plugins/prompt-stack/src/cli.ts status \
  --session <session-id> \
  --project-dir /absolute/project/path

bun plugins/prompt-stack/src/cli.ts validate \
  --session <session-id> \
  --project-dir /absolute/project/path
```

## Operator Notes

- Prefer absolute `--project-dir` and `--report` paths when calling the CLI from outside
  the repo root.
- Discover stack ids with `list` instead of assuming names.
- If the stack session is part of an active `$work` stream, keep planning and decisions in
  the active handoff and use `stack` only for the execution-plane prompt loop.
- Record stack step output into `.lev/pm/reports/` when the session feeds a workstream.
- After `record` or `validate`, return to the active handoff and update continuity there if
  the session changed the plan, decisions, or evidence.
- If the task needs subagents, follow the contract in
  `/Users/jean-patricksmith/digital/leviathan/plugins/prompt-stack/references/subagent-contract.md`.
- Keep the wrapper thin. Runtime ownership stays with `plugins/prompt-stack`.

## Optional FlowMind Path

The standalone plugin CLI is the primary runtime.

If you are explicitly validating or dogfooding the optional FlowMind path, the plugin-owned
scaffold is:

`/Users/jean-patricksmith/digital/leviathan/plugins/prompt-stack/flows/prompt-stack.flow.yaml`

Do not treat the FlowMind path as the default execution surface unless the task explicitly
calls for it.

## References

- Runtime CLI:
  `/Users/jean-patricksmith/digital/leviathan/plugins/prompt-stack/src/cli.ts`
- Stack catalog:
  `/Users/jean-patricksmith/digital/leviathan/plugins/prompt-stack/prompts/prompt-stack.prompts.yaml`
- Runtime contract:
  `/Users/jean-patricksmith/digital/leviathan/plugins/prompt-stack/references/subagent-contract.md`
- Active work handoffs:
  `/Users/jean-patricksmith/digital/leviathan/.lev/pm/handoffs/`
