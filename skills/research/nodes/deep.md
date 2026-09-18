# Deep

1. Build the prompt package defined in `SKILL.md`.
2. Inspect it with `lev research <query> -s deep --prompt-plan-only`.
3. Run `lev research <query> -s deep --no-wikify`; provider fanout is fixed by runtime strategy metadata.
4. Require source URLs from at least two provider results; record empty and failed providers.
5. Deduplicate URLs, preserve contradictions, synthesize with citations, and stop.
