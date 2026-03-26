---
name: changelog-md-workmanship
description: >-
  Rebuild CHANGELOG.md files and release histories from git, tags, releases, and
  issue trackers. Use when writing changelogs, version timelines, or agent-facing
  project history summaries.
---

<!-- TOC: Core | Problem | Prompt | Quick Start | Modes | Research | Chunking | Structure | Troubleshooting | Validation | References | Tools | Subagents | Self-Validation -->

# Changelog.md Workmanship

> **Core Insight:** A real changelog is a research artifact. If the history work is weak, the prose is fake.

## The Problem

Most changelogs fail in one of two ways:

- they are fake summaries written from vague memory
- they are unusable diff dumps that preserve chronology but destroy comprehension

The job is to build an orientation layer that lets another agent answer:

- what materially changed?
- when did it change?
- why did it change?
- which commits and workstreams should I inspect first?

## The One Rule

**Never draft a serious changelog from memory. Research exhaustively, then write incrementally while the evidence is still in hand.**

For large repos, do not wait until the end to write `CHANGELOG.md`. After each research chunk, update:

- the changelog itself
- a compaction-resistant research memo

That is how you survive long histories without losing findings to context pressure.

---

## THE EXACT PROMPT

```text
Create or rebuild a serious CHANGELOG.md for this project.

Requirements:
1. Research the real history first: git commits, tags, releases, issue tracker, and existing docs.
2. Cover the requested scope window completely, from the beginning if needed.
3. Distinguish actual GitHub Releases from plain git tags.
4. Use live links for representative commits and version pages.
5. Include issue-tracker workstreams when available.
6. Organize by landed capabilities, not raw diff order, but keep a clear version timeline.
7. For large histories, split research into chunks and update CHANGELOG.md incrementally after each chunk.
8. Make it agent-friendly: another agent should be able to understand what changed without reading every diff.

Output:
- A canonical CHANGELOG.md
- A short note describing the evidence sources used
```

---

## Quick Start

```bash
# 1. Read the repo's intent and rules first
cat AGENTS.md README.md 2>/dev/null

# 2. Create a compaction-resistant worklog immediately
touch CHANGELOG_RESEARCH.md

# 3. Build the version spine
git for-each-ref refs/tags --sort=creatordate --format='%(refname:short)%x09%(creatordate:short)%x09%(subject)'
gh release list --limit 100

# 4. Get early and recent history
git log --reverse --oneline --decorate=no --no-merges | head -n 50
git log --oneline --decorate=no --no-merges --max-count 120

# 5. Start writing the changelog skeleton early
cp .claude/skills/changelog-md-workmanship/assets/CHANGELOG-TEMPLATE.md CHANGELOG.md 2>/dev/null || true
cp .claude/skills/changelog-md-workmanship/assets/CHANGELOG-RESEARCH-TEMPLATE.md CHANGELOG_RESEARCH.md 2>/dev/null || true
```

### Fast Track

```text
1. Read AGENTS.md and README.md first.
2. Create CHANGELOG_RESEARCH.md immediately.
3. Gather the version spine: tags, releases, dates.
4. Slice history into chunks if the repo is large.
5. After each chunk, update the live CHANGELOG.md.
6. Finish with validation: dates, links, coverage, and structure.
```

One-page version: [QUICK-REFERENCE.md](references/QUICK-REFERENCE.md)
Bootstrap script: `scripts/bootstrap-changelog-workdir.sh [repo-dir]`

---

## Modes

| Mode | Time | Depth | Use When |
|------|------|-------|----------|
| **Small update** | 10-20 min | Single version or narrow window | Recent release notes, point update |
| **Standard rebuild** | 30-90 min | Full version spine + capability waves | Mid-size repo or partial rewrite |
| **Large-history reconstruction** | Multi-pass | Chunked sequential research | Long-lived or sprawling project |
| **Ultra-large history reconstruction** | Multi-pass + staged artifacts | Chunk files, coverage ledger, automation aids | Histories that obviously exceed one context window |

If the repo is large enough that you cannot confidently hold the history in context, use chunked reconstruction immediately. Do not try to "just be more careful."

Huge-repo playbook: [ULTRA-LARGE-REPOS.md](references/ULTRA-LARGE-REPOS.md)

---

## Research Doctrine

### Source Priority

Trust sources in this order:

1. Git history
2. Tags and release metadata
3. Issue tracker or beads history
4. Existing changelogs and release notes
5. README and other docs

If sources disagree, history wins.

### Minimum Evidence Set

For a serious changelog, gather at least:

- commit history
- version tags
- release metadata if available
- issue tracker history if available
- existing changelog or release notes if they exist

### What You Are Actually Reconstructing

You are not listing every commit. You are identifying:

- the version spine
- the major capability waves
- the major fixes and regressions
- the workstreams or epics behind those changes
- the commits another agent should inspect first

Link discipline and evidence rules: [LINKING-RULES.md](references/LINKING-RULES.md)
Quality bar by repo size: [QUALITY-BAR.md](references/QUALITY-BAR.md)
Tracker source handling: [TRACKER-ADAPTERS.md](references/TRACKER-ADAPTERS.md)

---

## Chunking Workflow for Large Histories

Large repos must be researched sequentially in bounded slices. Good chunk boundaries:

- one release/tag range
- one month or one sprint window
- 50-150 non-merge commits
- one major epic/capability wave

### Mandatory Process

- Create `CHANGELOG_RESEARCH.md` or `CHANGELOG_RESEARCH/NN-*.md` before deep history work.
- Create the `CHANGELOG.md` skeleton early.
- Research one chunk.
- Distill that chunk immediately into:
  - version timeline entries
  - one or more thematic sections
  - representative commit links
  - relevant issue-tracker links
- Only then move to the next chunk.

If you delay writing until all research is done, you will lose detail and create slop.

Chunking procedure, command patterns, and stopping rules: [RESEARCH-WORKFLOW.md](references/RESEARCH-WORKFLOW.md)

### Coverage Ledger

For large histories, maintain a ledger in the research memo:

- chunk name
- date or tag range
- status: not started / researching / distilled / validated
- major themes found
- unresolved questions

This prevents silent gaps and duplicate coverage.

---

## Golden Structure

For most substantial repos, this structure works best:

1. Scope + methodology note
2. Version timeline table
3. Thematic capability sections
4. Notes for agents

The strongest section shape is:

- short narrative paragraph
- `Delivered capability`
- `Closed workstreams`
- `Representative commits`

Copy-paste templates: [SECTION-TEMPLATES.md](references/SECTION-TEMPLATES.md)

### Critical Structural Rules

- Keep chronology visible with a version timeline.
- Keep comprehension high with thematic sections.
- Do not flatten everything into one giant date-ordered bullet list.
- Do not write a marketing page. This is orientation infrastructure.
- Do not stop at commits alone; connect the commits to project intent.

Templates and scaffolds: [SECTION-TEMPLATES.md](references/SECTION-TEMPLATES.md)
Command recipes: [COMMAND-RECIPES.md](references/COMMAND-RECIPES.md)

---

## Release and Link Discipline

Three rules matter a lot:

1. **Release vs tag is not the same thing.** If a GitHub Release does not exist, do not pretend it does.
2. **Use live URLs, not bare hashes.** Raw commit IDs are lower-utility than clickable commit pages.
3. **Scope tracker links tightly.** If the repo uses checked-in issue history such as `.beads/issues.jsonl`, link to that record instead of broad repo search when possible.

Direct examples and rules: [LINKING-RULES.md](references/LINKING-RULES.md)

---

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Write from memory | Gather evidence first |
| Dump commits chronologically | Build a version spine + thematic synthesis |
| Link naked hashes | Link live commit URLs |
| Pretend every tag is a release | Distinguish Releases, tags, and drafts |
| Wait until all research is done | Update the changelog after each chunk |
| Use generic tracker links | Scope to the real tracker record |
| Write vague summaries | Name the capability, fix, or regression concretely |
| Treat generated release notes as canonical history | Keep `CHANGELOG.md` separate and durable |

---

## Quick Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| The repo has too many commits to hold in context | No chunking strategy | Split by tag/date/epic and maintain a coverage ledger |
| Tag dates and release dates disagree | Tag-only versions or draft releases | Distinguish Releases from plain tags explicitly |
| The tracker links feel noisy or useless | Links are too broad | Scope directly to the real tracker record |
| The changelog feels like fluff | Themes are vague | Restate sections in terms of actual capabilities and fixes |
| The changelog feels like a commit dump | No synthesis layer | Add capability-wave sections above raw history |
| You cannot tell whether coverage is complete | No research memo | Use a durable worklog and mark chunk status |

Deeper fixes: [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)

---

## Validation

Before finishing, check all of this:

- [ ] Scope window is explicit
- [ ] Version timeline covers the intended history
- [ ] Release links and tag links are historically accurate
- [ ] Representative commits are live-linked
- [ ] Major capability waves are visible
- [ ] Major fixes/regressions are captured
- [ ] Issue-tracker workstreams are included when available
- [ ] Another agent can navigate from summary to evidence quickly
- [ ] No section feels like padded release-note fluff

Validation details and final audit questions: [RESEARCH-WORKFLOW.md](references/RESEARCH-WORKFLOW.md)
Quality thresholds: [QUALITY-BAR.md](references/QUALITY-BAR.md)
Audit script: `scripts/validate-changelog-md.py /path/to/CHANGELOG.md`
Network verification mode: `scripts/validate-changelog-md.py --verify-links /path/to/CHANGELOG.md`

### Trigger Tests

If this skill is unclear, these should still obviously trigger it:

- "rebuild this repo's CHANGELOG.md from the git history"
- "write a real version timeline for this project"
- "summarize the full project history for agents"
- "turn this repo's tags, releases, and issue tracker into a proper changelog"

---

## Reference Index

### By Task

| I need to... | Read |
|--------------|------|
| **Start fast** | [QUICK-REFERENCE.md](references/QUICK-REFERENCE.md) |
| **Run a full research workflow** | [RESEARCH-WORKFLOW.md](references/RESEARCH-WORKFLOW.md) |
| **Copy-paste a structure/template** | [SECTION-TEMPLATES.md](references/SECTION-TEMPLATES.md) |
| **Choose prompts for repo size** | [PROMPTS.md](references/PROMPTS.md) |
| **Fix a weak or confusing draft** | [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) |
| **Understand the quality threshold** | [QUALITY-BAR.md](references/QUALITY-BAR.md) |
| **See distilled design lessons** | [EXAMPLES.md](references/EXAMPLES.md) |
| **Get link rules right** | [LINKING-RULES.md](references/LINKING-RULES.md) |
| **Copy concrete command recipes** | [COMMAND-RECIPES.md](references/COMMAND-RECIPES.md) |
| **Handle different tracker ecosystems** | [TRACKER-ADAPTERS.md](references/TRACKER-ADAPTERS.md) |
| **Run the ultra-large workflow** | [ULTRA-LARGE-REPOS.md](references/ULTRA-LARGE-REPOS.md) |

### By Topic

| Topic | Reference |
|-------|-----------|
| Chunking long histories | [RESEARCH-WORKFLOW.md](references/RESEARCH-WORKFLOW.md) |
| Version timeline skeletons | [SECTION-TEMPLATES.md](references/SECTION-TEMPLATES.md) |
| Capability-wave section structure | [SECTION-TEMPLATES.md](references/SECTION-TEMPLATES.md) |
| Release vs tag correctness | [LINKING-RULES.md](references/LINKING-RULES.md) |
| Tracker-link scoping | [LINKING-RULES.md](references/LINKING-RULES.md) |
| Small/medium/huge repo prompts | [PROMPTS.md](references/PROMPTS.md) |
| Failure modes and recovery | [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) |
| Quality thresholds | [QUALITY-BAR.md](references/QUALITY-BAR.md) |
| Example patterns to emulate | [EXAMPLES.md](references/EXAMPLES.md) |
| Exact git/gh/jq recipes | [COMMAND-RECIPES.md](references/COMMAND-RECIPES.md) |
| Tracker normalization across ecosystems | [TRACKER-ADAPTERS.md](references/TRACKER-ADAPTERS.md) |
| Huge multi-pass scaffolding | [ULTRA-LARGE-REPOS.md](references/ULTRA-LARGE-REPOS.md) |

## Assets

| Asset | Purpose |
|-------|---------|
| `assets/CHANGELOG-TEMPLATE.md` | Reusable changelog scaffold for a new repo |
| `assets/CHANGELOG-RESEARCH-TEMPLATE.md` | Durable research memo scaffold for chunked history work |
| `assets/CHANGELOG-TEMPLATE-HUGE.md` | Huge-repo changelog scaffold with explicit multi-pass structure |
| `assets/CHANGELOG-RESEARCH-CHUNK-TEMPLATE.md` | Reusable chunk file scaffold for staged history reconstruction |
| `assets/CHANGELOG-COVERAGE-LEDGER-TEMPLATE.md` | Coverage ledger scaffold to prevent silent research gaps |

---

## Tools

| Tool | Purpose |
|------|---------|
| `git log`, `git for-each-ref` | Commit and tag history |
| `gh release list`, `gh issue list` | Release and issue metadata |
| `jq` | Checked-in tracker mining |
| `br` / `bv` | Beads-style issue history and planning context |
| `scripts/bootstrap-changelog-workdir.sh` | Bootstrap `CHANGELOG.md` and `CHANGELOG_RESEARCH.md` from templates |
| `scripts/build-version-spine.py` | Generate a markdown or JSON version timeline skeleton from local tags and GitHub releases |
| `scripts/extract-tracker-workstreams.py` | Normalize tracker evidence from beads, GitHub Issues, Linear/Jira exports, and milestone docs |
| `scripts/cluster-history.py` | Group commit history into candidate capability waves for faster thematic drafting |
| `scripts/validate-changelog-md.py` | Audit a finished changelog for structural and evidence problems |
| `assets/CHANGELOG-TEMPLATE.md` | Faster changelog bootstrap |
| `assets/CHANGELOG-RESEARCH-TEMPLATE.md` | Faster research-memo bootstrap |
| `assets/CHANGELOG-TEMPLATE-HUGE.md` | Huge-repo changelog bootstrap |
| `assets/CHANGELOG-RESEARCH-CHUNK-TEMPLATE.md` | Huge-repo chunk bootstrap |
| `assets/CHANGELOG-COVERAGE-LEDGER-TEMPLATE.md` | Huge-repo coverage-ledger bootstrap |

*Run scripts directly (they have shebangs) rather than invoking `python` manually.*

---

## Quick Search

Useful searches during changelog work:

```bash
# Early history
git log --reverse --oneline --decorate=no --no-merges | head -n 50

# Recent history
git log --oneline --decorate=no --no-merges --max-count 120

# Tags
git for-each-ref refs/tags --sort=creatordate --format='%(refname:short)%x09%(creatordate:short)%x09%(subject)'

# Releases
gh release list --limit 100

# Beads-style tracker history
jq -r 'select(.status=="closed") | [.id,.title,.closed_at] | @tsv' .beads/issues.jsonl

# Tracker normalization
scripts/extract-tracker-workstreams.py --repo . --format markdown

# Capability-wave clustering
scripts/cluster-history.py --repo . --format markdown
```

---

## Subagents

| Subagent | Purpose |
|----------|---------|
| `subagents/history-researcher.md` | Research one bounded historical slice and return changelog-ready findings |
| `subagents/draft-auditor.md` | Review a changelog draft for missing coverage, weak synthesis, and evidence issues |

---

## Self-Validation

Validate the skill itself:

```bash
./scripts/validate-skill.py .claude/skills/changelog-md-workmanship/
```

Trigger tests: [SELF-TEST.md](SELF-TEST.md)

---

## Meta-Note

This skill is intentionally larger than the usual "concise skill" target.

That is deliberate:

- changelog reconstruction is a high-context research task
- large histories need multiple entry points and fast navigation
- reference surfacing is worth the extra size because it prevents bad historical synthesis
