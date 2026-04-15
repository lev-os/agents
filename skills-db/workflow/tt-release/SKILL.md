---
name: workflow-tt-release
description: Full release pipeline for the timetravel plugin — test, version, changelog, build, publish, tag. Invoke with /workflow tt-release.
skill_type: workflow
category: process-workflow
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
---

# Workflow: Timetravel Release

Full release pipeline for `~/digital/leviathan/plugins/timetravel/`.

Every step spawns a **fresh subagent** (poly sparkle pattern). State flows only through handoff artifacts at `.lev/pm/handoffs/tt-release-*.md`.

## Trigger

- Ready to cut a new version of the timetravel plugin
- `/workflow tt-release [--bump major|minor|patch] [--dry-run] [--skip-publish]`

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `bump` | no | Semver bump type. Default: `patch` |
| `dry_run` | no | If true, simulate everything but don't publish or tag. Default: false |
| `skip_publish` | no | Skip npm publish step. Default: false |
| `pre_tag` | no | Pre-release tag (e.g. `alpha`, `beta`, `rc`). Default: none |

## Steps

### Step 1: Run Tests

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read `~/digital/leviathan/plugins/timetravel/package.json` for current version and test scripts

**Action**:
- Run `cd ~/digital/leviathan/plugins/timetravel && pnpm test`
- Run `cd ~/digital/leviathan/plugins/timetravel && pnpm build`
- If either fails: STOP workflow, report failures
- Record: test count, pass count, coverage (if available)

**Handoff**: `.lev/pm/handoffs/tt-release-1-tests.md`
```yaml
current_version: <x.y.z>
test_result: pass | fail
test_count: <n>
build_result: pass | fail
gate: pass | fail
failure_details: null | "<details>"
```

---

### Step 2: Version Bump

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoff from Step 1 (current version, gate status)
- If gate=fail, STOP

**Action**:
- Calculate new version: apply `bump` type to current version
  - If `pre_tag` set: e.g. `0.2.0-alpha.1`
- Update `version` field in `package.json`
- Do NOT run `npm version` (we manage git separately)

**Handoff**: `.lev/pm/handoffs/tt-release-2-version.md`
```yaml
previous_version: <x.y.z>
new_version: <x.y.z>
bump_type: major | minor | patch
pre_tag: null | alpha | beta | rc
```

---

### Step 3: Changelog

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoff from Step 2
- Read git log since last tag: `cd ~/digital/leviathan/plugins/timetravel && git log --oneline $(git describe --tags --abbrev=0 2>/dev/null || echo HEAD~20)..HEAD -- .`
- Read existing CHANGELOG.md if present

**Action**:
- Group commits by type: feat, fix, refactor, docs, test, chore
- Generate changelog entry for new version:
  ```markdown
  ## [x.y.z] - YYYY-MM-DD

  ### Added
  - ...

  ### Fixed
  - ...

  ### Changed
  - ...
  ```
- Prepend to CHANGELOG.md (create if missing)

**Handoff**: `.lev/pm/handoffs/tt-release-3-changelog.md`
```yaml
changelog_path: CHANGELOG.md
commits_processed: <n>
sections: [Added, Fixed, Changed, ...]
```

---

### Step 4: Build

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoff from Step 2 (new version)

**Action**:
- Clean previous build: `rm -rf dist/`
- Run `cd ~/digital/leviathan/plugins/timetravel && pnpm build`
- Verify `dist/` contains expected files: `index.js`, `index.d.ts`, `cli.js`, adapter files
- Verify `dist/cli.js` has shebang line
- Check package.json `files` field matches dist output

**Handoff**: `.lev/pm/handoffs/tt-release-4-build.md`
```yaml
build_result: pass | fail
dist_files: [<list>]
dist_size_kb: <n>
shebang_present: true | false
```

---

### Step 5: Publish

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoffs from Steps 2 and 4
- Check: `dry_run` and `skip_publish` flags

**Action**:
- If `dry_run=true`: run `cd ~/digital/leviathan/plugins/timetravel && npm pack --dry-run` and report contents
- If `skip_publish=true`: skip this step entirely
- Otherwise: run `cd ~/digital/leviathan/plugins/timetravel && npm publish --access public`
  - If pre-release tag: add `--tag <pre_tag>`
- Verify publish succeeded (check npm registry)

**Handoff**: `.lev/pm/handoffs/tt-release-5-publish.md`
```yaml
action: publish | dry-run | skipped
result: success | failed | skipped
package: "@lev-os/timetravel"
version: <x.y.z>
registry_url: <url or null>
```

---

### Step 6: Git Tag

**Agent Type**: general-purpose
**Skills**: None
**Research**:
- Read handoffs from Steps 2-3

**Action**:
- Stage changed files: `package.json`, `CHANGELOG.md`, `dist/` (if tracked)
- Create commit: `release: timetravel v<x.y.z>`
- Create annotated tag: `git tag -a timetravel-v<x.y.z> -m "Release timetravel v<x.y.z>"`
- If `dry_run=true`: show what would be committed/tagged but don't execute
- Do NOT push (user must explicitly push)

**Handoff**: `.lev/pm/handoffs/tt-release-6-tag.md`
```yaml
commit_sha: <sha or null if dry-run>
tag: timetravel-v<x.y.z>
pushed: false
dry_run: true | false
```

---

### Step 7: Update Downstream

**Agent Type**: general-purpose
**Skills**: `skill://lev-research`
**Research**:
- Read all handoffs from Steps 1-6
- Search for downstream dependencies:
  - `grep -r "@lev-os/timetravel" ~/.agents/skills/` for skill references
  - `grep -r "timetravel" ~/digital/leviathan/plugins/` for plugin references
  - Check `~/.agents/skills/lev-research/SKILL.md` for version references

**Action**:
- List all files referencing timetravel with current version
- Suggest updates for each (do NOT auto-edit downstream — report only)
- Update version in `lev-research` SKILL.md version history table
- Print release summary: version, changelog highlights, publish status, tag, downstream suggestions

**Handoff**: `.lev/pm/handoffs/tt-release-7-downstream.md`
```yaml
downstream_references:
  - file: <path>
    current_ref: <old version or import>
    suggested_update: "<what to change>"
version_updated_in:
  - ~/.agents/skills/lev-research/SKILL.md
release_summary:
  version: <x.y.z>
  published: true | false
  tagged: true | false
  pushed: false
status: complete
```

## Outputs

- Updated `package.json` with new version
- `CHANGELOG.md` with release entry
- Clean `dist/` build
- npm package (if published)
- Git commit + annotated tag (not pushed)
- Downstream update suggestions
- 7 handoff artifacts in `.lev/pm/handoffs/tt-release-*.md`

## Validation

- [ ] All tests pass before release
- [ ] Version bump follows semver correctly
- [ ] Changelog covers all commits since last tag
- [ ] Build produces valid dist/ output
- [ ] Publish succeeds (or dry-run validates package)
- [ ] Git tag created with correct format
- [ ] No auto-push (user must confirm)
- [ ] Downstream references identified
- [ ] All 7 handoff files created

## Usage

```bash
/workflow tt-release                         # Patch release (default)
/workflow tt-release --bump minor            # Minor version bump
/workflow tt-release --bump major            # Major version bump
/workflow tt-release --dry-run               # Simulate everything
/workflow tt-release --skip-publish          # Local only, no npm
/workflow tt-release --bump minor --pre-tag alpha  # Pre-release: 0.2.0-alpha.1
```

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for workflow-tt-release, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
