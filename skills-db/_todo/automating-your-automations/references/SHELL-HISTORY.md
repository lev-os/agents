# Shell History Parsing

Prefer atuin (covers all shells). Fall back to these when atuin DB is unavailable.

## Zsh Extended Format

Location: `~/.zsh_history` — Format: `: <epoch>:<duration>;command`

```
: 1707849600:0;command here
: 1707849605:3;another command
```

```bash
# Top 20 most repeated commands
grep -oP '(?<=;).*' ~/.zsh_history | sort | uniq -c | sort -rn | head -20

# Command pairs (always followed by another)
grep -oP '(?<=;).*' ~/.zsh_history | paste - - | sort | uniq -c | sort -rn | head -20
```

Multi-line commands use backslash continuation — join before counting.

**Session boundaries:** Timestamp gaps >30 minutes = new session. Use to detect:
- Session-start rituals (always run first)
- Session-end patterns (cleanup, push, sync)

---

## Bash History

Location: `~/.bash_history` — one command per line, no timestamps by default.

If `HISTTIMEFORMAT` was set, timestamps appear as `#epoch` before each command.

```bash
sort ~/.bash_history | uniq -c | sort -rn | head -20
```

---

## Fish History

Location: `~/.local/share/fish/fish_history` — YAML format:

```yaml
- cmd: command here
  when: 1707849600
```

```bash
grep '^- cmd:' ~/.local/share/fish/fish_history | sed 's/- cmd: //' | sort | uniq -c | sort -rn | head -20
```

---

## Cross-Shell Combined

```bash
{
  grep -oP '(?<=;).*' ~/.zsh_history 2>/dev/null
  cat ~/.bash_history 2>/dev/null
} | grep -v '^#' | grep -v '^$' | sort | uniq -c | sort -rn | head -20
```
