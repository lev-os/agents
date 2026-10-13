# Conflict-resolution brief

When a merge or pull conflict appears, do not only list conflicted files.
Before stopping, inspect enough context to give the user actionable resolution
paths.

Required conflict inspection:
- `git status --short`
- `git diff --name-only --diff-filter=U`
- `git ls-files -u <conflicted-paths>`
- `git diff --cc -- <conflicted-files>`
- for submodules: `git -C <submodule> log --oneline --decorate --graph --all --max-count=20`
- for code conflicts: inspect both sides with `git show :2:<path>` and `git show :3:<path>` when useful

Required conflict brief:
```yaml
sync_conflict:
  state: blocked
  conflicted_paths:
    - <path>
  inferred_intents:
    ours: <what the local side was trying to preserve>
    theirs: <what the incoming side was trying to preserve>
  solution_paths:
    - option: <merge both | take ours | take theirs | advance submodule pointer | manual synthesis>
      blast_radius: <low|medium|high>
      why: <one sentence>
      risks:
        - <specific risk>
      validation:
        - <command that would prove this option>
  recommended_strategy: <one option plus why>
  next_command_sequence:
    - <minimal non-destructive commands to apply the recommendation>
```

Guidance:
- Infer intent from both sides before recommending a resolution.
- Prefer a synthesis that preserves both sides' intended behavior when the
  combined behavior is coherent and testable.
- Treat submodule conflicts as pointer-selection problems backed by submodule
  commit ancestry. State whether one pointer contains the other, whether a
  merge commit exists, or whether a new submodule merge is required.
- Include blast radius in practical terms: affected module, tests likely to
  break, deployment/runtime surfaces touched, and whether generated artifacts or
  submodule pointers are involved.
- If the correct strategy is clear and low-risk, recommend it explicitly; do not
  hide behind "resolve conflicts manually."
- Do not run the resolution automatically unless the user asked sync to continue
  and the resolution is low-risk, non-destructive, and fully justified by the
  brief.

