# Interview: Question Loop

Ask questions one at a time until you can write the full YAML contract.

You need to know:
1. What does the skill DO? (one sentence)
2. What are the steps? (list them)
3. For each step: what's the input? What's the output? What does failure look like?
4. Are there conditional routes? (if X, do Y, else Z)
5. What are the anti-patterns? (what will agents try to skip?)

Stop asking when you can write this for EVERY step:
```yaml
- id: step_name
  action: "what to do"
  instruction: |
    How to do it.
  validation: "concrete check"
  on_failure: "what to do when it fails"
```

If you can't fill in validation and on_failure, you don't understand the step yet. Keep asking.

Also ask:
- Does this skill need a schema for its output?
- Does it need templates or scaffolding?
- Is it autonomous or human-in-the-loop?
- Does it have loops (retry until condition)?
