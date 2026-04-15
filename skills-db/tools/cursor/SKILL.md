---
name: cursor
description: >-
  Control Cursor AI code editor via CLI. Use when opening files, comparing diffs,
  managing extensions, or configuring Cursor as git editor.
---

<!-- TOC: Quick Start | THE EXACT PROMPT | Commands | Settings | References -->

# Cursor CLI

> **Core Capability:** Control the Cursor AI-powered code editor (VS Code fork) from the command line.

## Quick Start

```bash
# Open current directory
cursor .

# Open file at specific line
cursor /path/to/file.ts:42

# Compare two files
cursor --diff file1.ts file2.ts

# Use as git editor
git config --global core.editor "cursor --wait"
```

---

## THE EXACT PROMPT — Open Files

```
# Open file
cursor /path/to/file.ts

# Open at specific line
cursor /path/to/file.ts:42

# Open at line and column
cursor /path/to/file.ts:42:10

# Open multiple files
cursor file1.ts file2.ts file3.ts

# Open in new window
cursor -n /path/to/project

# Reuse existing window
cursor -r /path/to/file
```

---

## THE EXACT PROMPT — Diff and Wait

```
# Compare two files
cursor --diff file1.ts file2.ts
cursor -d file1.ts file2.ts

# Wait for file to close (scripts/git)
cursor --wait /path/to/file
cursor -w /path/to/file

# Use as git editor
git config --global core.editor "cursor --wait"
```

---

## THE EXACT PROMPT — Extensions

```
# List installed extensions
cursor --list-extensions

# Install extension
cursor --install-extension <extension-id>

# Uninstall extension
cursor --uninstall-extension <extension-id>

# Disable all extensions
cursor --disable-extensions
```

---

## Essential Commands

| Command | Description |
|---------|-------------|
| `cursor .` | Open current directory |
| `cursor file.ts:42` | Open file at line |
| `cursor -n path` | Open in new window |
| `cursor -r path` | Reuse existing window |
| `cursor --diff a b` | Compare two files |
| `cursor --wait file` | Wait for close (scripting) |
| `cursor --add folder` | Add to current workspace |

---

## Settings Locations

| File | macOS Path |
|------|------------|
| User settings | `~/Library/Application Support/Cursor/User/settings.json` |
| Keybindings | `~/Library/Application Support/Cursor/User/keybindings.json` |

| File | Linux Path |
|------|------------|
| User settings | `~/.config/Cursor/User/settings.json` |
| Keybindings | `~/.config/Cursor/User/keybindings.json` |

---

## Portable Mode

```bash
# Custom user data directory
cursor --user-data-dir /path/to/data

# Custom extensions directory
cursor --extensions-dir /path/to/extensions
```

---

## Piping Input

```bash
# Read from stdin
echo "console.log('hello')" | cursor -

# Pipe file contents
cat script.ts | cursor -
```

---

## Debugging

```bash
# Show version
cursor --version

# Show help
cursor --help

# Verbose output
cursor --verbose /path/to/file

# Inspect extensions
cursor --inspect-extensions
```

---

## References

| Topic | Reference |
|-------|-----------|
| Full command reference | [COMMANDS.md](references/COMMANDS.md) |
