# Research Workflow

Use this when the repo history is large enough that one pass will lose accuracy.

## Phase 0: Establish the research spine

Read first:

- `AGENTS.md`
- `README.md`
- any existing `CHANGELOG.md`, `HISTORY.md`, or release notes

Create a durable memo immediately:

```bash
touch CHANGELOG_RESEARCH.md
```

If history is large, prefer:

```bash
mkdir -p CHANGELOG_RESEARCH
touch CHANGELOG_RESEARCH/00-overview.md
```

Also create the live skeleton early:

```bash
touch CHANGELOG.md
```

## Phase 1: Build the version spine

Minimum commands:

```bash
git for-each-ref refs/tags --sort=creatordate --format='%(refname:short)%x09%(creatordate:short)%x09%(subject)'
gh release list --limit 100
git log --reverse --oneline --decorate=no --no-merges | head -n 50
git log --oneline --decorate=no --no-merges --max-count 120
```

Write these findings into both:

- `CHANGELOG_RESEARCH.md`
- the version timeline in `CHANGELOG.md`

Do not leave the version spine as a scratchpad only.

## Phase 2: Choose chunk boundaries

Use one of these chunking modes:

- tag range: `v0.1.10..v0.1.20`
- date range: one sprint or one month
- commit window: 50-150 non-merge commits
- epic/capability wave from the issue tracker

Good default for sprawling repos:

- start with release/tag windows
- refine within each window using issue-tracker epics

## Phase 3: Research one chunk at a time

Typical commands:

```bash
git log --oneline --decorate=no --no-merges <range>
git log --stat --decorate=no --no-merges <range>
gh issue list --state all --limit 200
```

If the repo uses checked-in tracker history:

```bash
jq -r 'select(.status=="closed") | [.id,.title,.closed_at] | @tsv' .beads/issues.jsonl
```

For each chunk, answer:

- what major capability landed?
- what major fix or regression mattered?
- what issue tracker workstream explains intent?
- which commits are the best representative evidence?

## Phase 4: Distill immediately

After each chunk, update:

- the version timeline if new versions were covered
- one or more thematic sections
- the research memo with any unresolved questions

Never postpone synthesis until the end of all research.

## Phase 5: Merge chunk findings into themes

Once all chunks are researched, merge them into capability waves such as:

- initial architecture and core command surface
- sync safety and correctness
- test and release infrastructure
- output modes and agent ergonomics
- routing and cross-project coordination
- reliability and failure modeling
- concurrency correctness
- performance and throughput

The goal is not one section per chunk. The goal is coherent thematic navigation.

## Final audit

Ask these before finishing:

- Can another agent answer "what changed materially?" without reading diffs?
- Are releases and tags distinguished correctly?
- Are dates concrete and consistent?
- Are the most important commits clickable?
- Are issue-tracker links useful rather than decorative?
- Did any research chunk fail to get distilled into the live changelog?

If any answer is "no," the changelog is not done.
