# Cursor CLI Command Reference

## Table of Contents
- [Opening Files](#opening-files)
- [Window Options](#window-options)
- [Diff Mode](#diff-mode)
- [Wait Mode](#wait-mode)
- [Workspace](#workspace)
- [Extensions](#extensions)
- [Debugging](#debugging)
- [Portable Mode](#portable-mode)

---

## Opening Files

```bash
# Open current directory
cursor .

# Open specific file
cursor /path/to/file.ts

# Open file at specific line
cursor /path/to/file.ts:42

# Open file at line and column
cursor /path/to/file.ts:42:10

# Open folder
cursor /path/to/project

# Open multiple files
cursor file1.ts file2.ts file3.ts
```

---

## Window Options

```bash
# Open in new window
cursor -n /path/to/project
cursor --new-window /path/to/project

# Reuse existing window
cursor -r /path/to/file
cursor --reuse-window /path/to/file
```

---

## Diff Mode

```bash
# Compare two files
cursor -d file1.ts file2.ts
cursor --diff file1.ts file2.ts
```

---

## Wait Mode

Wait for file to close (useful in scripts):

```bash
cursor --wait /path/to/file
cursor -w /path/to/file
```

### Use as Git Editor

```bash
git config --global core.editor "cursor --wait"
```

---

## Workspace

```bash
# Add folder to current workspace
cursor --add /path/to/folder
```

---

## Extensions

```bash
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

## Debugging

```bash
# Show version
cursor --version

# Show help
cursor --help

# Verbose output
cursor --verbose /path/to/file

# Open developer tools
cursor --inspect-extensions
```

---

## Portable Mode

```bash
# Specify user data directory
cursor --user-data-dir /path/to/data

# Specify extensions directory
cursor --extensions-dir /path/to/extensions
```

---

## Piping Input

```bash
# Read from stdin
echo "console.log('hello')" | cursor -
```

---

## Settings Locations

### macOS

| File | Path |
|------|------|
| User settings | `~/Library/Application Support/Cursor/User/settings.json` |
| Keybindings | `~/Library/Application Support/Cursor/User/keybindings.json` |

### Linux

| File | Path |
|------|------|
| User settings | `~/.config/Cursor/User/settings.json` |
| Keybindings | `~/.config/Cursor/User/keybindings.json` |

---

## Remote Development

Cursor supports remote development similar to VS Code. SSH remotes are configured in:

```
~/.ssh/config
```

Then use command palette or remote explorer in the GUI.

---

## CLI Location

```bash
/usr/local/bin/cursor
```

If not found, install the shell command from Cursor:
1. Open Cursor
2. Command Palette (Cmd/Ctrl+Shift+P)
3. "Shell Command: Install 'cursor' command in PATH"
