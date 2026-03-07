---
name: authorize
description: Manage persistent allowlist for pre_tool_use hook bypass
triggers:
  - /authorize
  - authorize path
  - allow file access
---

# Authorize

Manage the persistent allowlist at `~/.claude/authorized-paths.txt` that bypasses pre_tool_use.py security checks.

## Commands

| Command | Action |
|---------|--------|
| `/authorize add <pattern>` | Add path pattern to allowlist |
| `/authorize remove <pattern>` | Remove pattern from allowlist |
| `/authorize list` | Show current allowlist |
| `/authorize clear` | Clear all authorized paths |

## Usage

```bash
# Allow a specific file
/authorize add ~/.secrets/api-keys.json

# Allow a directory pattern
/authorize add ~/.config/myapp/*

# Allow by extension
/authorize add *.local

# Remove authorization
/authorize remove ~/.secrets/api-keys.json

# View all authorized paths
/authorize list
```

## Implementation

When user invokes `/authorize`:

### add <pattern>
```bash
echo "<pattern>" >> ~/.claude/authorized-paths.txt
sort -u ~/.claude/authorized-paths.txt -o ~/.claude/authorized-paths.txt
```
Confirm: "✓ Added `<pattern>` to authorized paths"

### remove <pattern>
```bash
grep -v "^<pattern>$" ~/.claude/authorized-paths.txt > /tmp/auth.tmp
mv /tmp/auth.tmp ~/.claude/authorized-paths.txt
```
Confirm: "✓ Removed `<pattern>` from authorized paths"

### list
```bash
cat ~/.claude/authorized-paths.txt 2>/dev/null || echo "(empty)"
```
Display as formatted list.

### clear
```bash
rm -f ~/.claude/authorized-paths.txt
```
Confirm: "✓ Cleared all authorized paths"

## Pattern Matching

The hook uses these matching rules:
- Exact match: `/path/to/file.txt`
- Glob patterns: `*.local`, `~/.config/*`
- Directory prefix: `/path/to/dir/` (trailing slash = all children)

## Security Notes

- Authorizations persist across sessions
- Review periodically with `/authorize list`
- Use narrow patterns (specific files > broad globs)
- `.env` files have built-in allowlist in hook (`.env.local`, `.env.sample`, `.env.example`)
