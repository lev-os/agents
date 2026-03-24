# Validation: BDD Scenario Testing

Run blind behavioral tests on the produced skill.

For each critical node in the skill:
1. Write a pressure scenario (time + sunk cost + exhaustion combined)
2. Load the skill in a subagent
3. Give it the pressure scenario
4. Check: did it follow the instructions?

Score against:
- Did validation strings get executed as commands?
- Did the agent follow the step sequence?
- Did it skip any steps?
- Did it hit any anti-patterns?

If a scenario fails:
1. Capture the rationalization verbatim
2. Add it to anti_patterns
3. Re-test

Continue until zero new rationalizations emerge.
This is the RED-GREEN-REFACTOR cycle from writing-skills.
