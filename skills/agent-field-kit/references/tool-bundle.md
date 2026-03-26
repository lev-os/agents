# Agent Field Kit — Tool Bundle

## Bundle Contents

### Core baseline

| Tool | Why it belongs |
|------|----------------|
| `ripgrep` / `rg` | Fast repo-aware text search |
| `fd` | Fast file discovery |
| `fzf` | Interactive narrowing |
| `tree` | Directory snapshots |
| `duckdb` | Ad hoc SQL over local data |
| `git-delta` | Readable diffs |
| `xh` | Readable HTTP client |
| `watchexec` | Rerun on file changes |
| `just` | Simple task runner |
| `semgrep` | Deterministic static analysis |
| `tmux` | Required for `ntm` |

### Niche leaf tools

| Tool | Install path | Skill |
|------|--------------|-------|
| `dcg` | `brew install dicklesworthstone/tap/dcg` | `dcg` |
| `cass` | `brew install dicklesworthstone/tap/cass` | `cass` |
| `ubs` | `brew install dicklesworthstone/tap/ubs` | `ubs` |
| `ntm` | `brew install dicklesworthstone/tap/ntm` | `ntm` |
| `agentmail-cli` | `npm install -g agentmail-cli` | `agentmail-cli` |

## Opinionated Usage

### Search and structure

- `rg PATTERN .` when you know the text.
- `fd NAME .` when you know the file shape.
- `tree -L 2 PATH` when you need to show structure quickly.
- `fd -t f | fzf` when you need interactive picking.

### Data and HTTP

- `duckdb -c "SELECT * FROM 'file.csv' LIMIT 20"` for quick data inspection.
- `xh GET :3000/health` or `xh POST :3000/api key=value` for readable HTTP testing.

### Diff and automation

- `git -c core.pager=delta diff` for readable review.
- `watchexec -e ts -r -- pnpm test` for tight edit/run loops.
- `just` when a repo already exposes task recipes.

### Static analysis

- `semgrep --config auto --json TARGET_DIR` for quick broad checks.
- `ubs --staged --format=json --ci` when UBS is installed and you want bug scanning, not just SAST.
- `defendr` when the code is untrusted or you are about to install external dependencies.

## Shell Notes

- On Debian/Ubuntu, `fd` may install as `fdfind`. The installer writes an alias for `fd`.
- `ntm` works best with shell integration:

```bash
eval "$(ntm shell zsh)"
```

- The installer writes `~/.agent-field-kit/env.sh` so a remote shell can recover quickly.

