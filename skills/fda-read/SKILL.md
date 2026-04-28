---
name: fda-read
description: Use macOS Terminal.app Full Disk Access as a proxy to copy TCC-protected files such as Messages/chat.db or AddressBook into a readable location for agent workflows.
---

# fda-read — macOS Full Disk Access proxy

Read macOS TCC-protected files (Messages/chat.db, AddressBook, etc.) from a shell that does NOT have Full Disk Access, by delegating through Terminal.app which does.

## Usage

```bash
# Copy a protected file to a readable location
fda-read <source_path> [<dest_dir>]

# Examples
fda-read ~/Library/Messages/chat.db           # → /tmp/fda-read-chat.db (+ WAL + SHM)
fda-read ~/Library/Messages/chat.db /tmp/live  # → /tmp/live/chat.db (+ WAL + SHM)
```

## CRITICAL: SQLite WAL mode

macOS Messages.app uses SQLite WAL (Write-Ahead Log) mode. Recent messages live in `chat.db-wal`, NOT in `chat.db`. **Copying only chat.db gives stale data.** You MUST copy all 3 files:
- `chat.db` — main database
- `chat.db-wal` — write-ahead log (WHERE RECENT MESSAGES ARE)
- `chat.db-shm` — shared memory index

SQLite automatically reads the WAL when all 3 files are co-located. If you only copy `chat.db`, you'll miss messages that Messages.app shows but haven't been checkpointed to the main db yet.

**This was discovered the hard way:** session 2026-04-16, user could see Josh's 6:30pm messages in Messages.app GUI but our queries returned nothing until we copied WAL+SHM alongside chat.db.

## How it works

Terminal.app was granted Full Disk Access in System Settings (macOS pop-up accepted by user). Any process Terminal.app spawns inherits that FDA grant. Claude Code's shell does NOT have FDA directly.

The skill invokes:
```bash
osascript -e "tell application \"Terminal\" to do script \"cp '$SRC' '$DEST' && echo DONE > '$DEST.done'\""
```

Then waits for `$DEST.done` to appear (max 10s), confirming the copy completed.

## When to use

- Before querying live iMessage data (`~/Library/Messages/chat.db`)
- Before reading AddressBook (`~/Library/Application Support/AddressBook/`)
- Before any macOS TCC-protected file access from agent context
- When `sqlite3 ~/Library/Messages/chat.db` returns "unable to open database file"

## When NOT to use

- If your shell already has FDA (test: `sqlite3 ~/Library/Messages/chat.db "SELECT 1;"`)
- For files that aren't TCC-protected (regular project files, /tmp, etc.)
- In CI/CD or headless environments (Terminal.app requires a display)

## Canonical pattern

This is the official Leviathan pattern for protected macOS resource access:
1. FDA-granted GUI app (Terminal.app) acts as proxy
2. Shell requests copy via osascript
3. Copy lands in /tmp (unrestricted)
4. All downstream tools read from /tmp

Documented at: `.lev/pm/captures/20260415-fda-canonical-path.yaml`

## Implementation

For agents: execute this sequence in Bash:

```bash
SRC="$1"
DEST_DIR="${2:-/tmp/fda-read-$(basename "$SRC" .db)}"
DONE_MARKER="${DEST_DIR}.done"
rm -f "$DONE_MARKER"

# Copy main db + WAL + SHM (all 3 required for fresh SQLite reads)
osascript -e "tell application \"Terminal\" to do script \"mkdir -p '$DEST_DIR' && cp '$SRC' '${SRC}-wal' '${SRC}-shm' '$DEST_DIR/' 2>/dev/null && chmod 644 '$DEST_DIR/'* && echo DONE > '$DONE_MARKER'\""

for i in $(seq 1 20); do [ -f "$DONE_MARKER" ] && break; sleep 0.5; done
if [ -f "$DONE_MARKER" ]; then
  DB_FILE="$DEST_DIR/$(basename "$SRC")"
  echo "fda-read: copied $SRC + WAL + SHM → $DEST_DIR/ ($(stat -f%z "$DB_FILE") bytes)"
  rm -f "$DONE_MARKER"
  # Verify WAL was included
  if [ -f "$DEST_DIR/$(basename "$SRC")-wal" ]; then
    echo "fda-read: WAL included ($(stat -f%z "$DEST_DIR/$(basename "$SRC")-wal") bytes)"
  else
    echo "fda-read: WARNING — WAL not found, recent data may be missing"
  fi
else
  echo "fda-read: TIMEOUT — Terminal.app may not have FDA or file doesn't exist" >&2
  exit 1
fi

# Usage: query the copied db (WAL auto-read when co-located)
# sqlite3 "$DEST_DIR/$(basename "$SRC")" "SELECT ..."
```

## Supersedes

- `~/digital/cyber/josh-imessage/dist/imessage_loader` (PyInstaller binary with FDA) — still works but this is simpler
- `~/digital/cyber/josh-imessage/manage_scheduler.sh` — daemon scheduler can delegate to this pattern instead

## Prerequisites

- Terminal.app listed in System Settings → Privacy & Security → Full Disk Access
- Terminal.app must be installed (ships with macOS)
- A display session (not headless/SSH)
