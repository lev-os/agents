# Max

1. Build the prompt package defined in `SKILL.md`, including explicit coverage gates.
2. Inspect it with `lev research <query> -s max --prompt-plan-only`.
3. Run `lev research <query> -s max --no-wikify`; execute every available configured adapter.
4. Record every provider outcome, then check source-class coverage and unresolved contradictions.
5. Synthesize only after the coverage gates pass; otherwise return the exact gaps and stop.
