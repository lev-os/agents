# Authoring: Apply the Format Spec

Every skill must follow this format:

1. **1-2 lines of prose** explaining what the skill does (procedural, not descriptive)
2. **YAML blocks** for every step with: id, action, instruction, validation, on_failure
3. **validation strings are concrete** — commands the agent can run or states it can check
4. **on_failure is specific** — not "handle the error" but "do THIS specific thing"
5. **anti_patterns table** at the end with 5+ entries from real agent failure modes
6. **All YAML in markdown must be fenced** — wrap every `steps:`, config, or example YAML block in ` ```yaml ` / ` ``` ` code fences. Bare YAML in markdown is invisible structure that agents parse as prose.

Decide the skill's interaction mode:
- **Autonomous**: runs without stopping (validation gates are the only checkpoints)
- **HITL/Dashboard**: pauses for user input at key nodes
- **Looping**: retries until condition met (needs max_iterations)
- **Knobs**: configurable between autonomous and HITL

Top 3 reference points go INLINE in the YAML. Everything else links to a .md file.
Do NOT put critical instructions in references/ — agents don't read them.

Under 300 lines total. Prose is the enemy.
