# Gum Recipes for Installer Scripts

Charmbracelet Gum (https://github.com/charmbracelet/gum) recipes used in production installers.

---

## Detection

```bash
HAS_GUM=0
if command -v gum &> /dev/null && [ -t 1 ]; then
  HAS_GUM=1
fi
```

Always check `[ -t 1 ]` (stdout is a terminal). Gum output breaks piped/redirected contexts.

---

## Styled Text

```bash
# Bold colored text
gum style --foreground 42 --bold 'Success message'

# Dim/muted text
gum style --foreground 245 'Secondary info'

# Warning color
gum style --foreground 214 'Warning message'

# Error color
gum style --foreground 196 'Error message'

# Info/primary color
gum style --foreground 39 'Info message'

# Magenta accent (used in RCH)
gum style --foreground 212 'Accent text'
```

---

## Bordered Boxes

```bash
# Simple info box
gum style \
  --border normal \
  --border-foreground 39 \
  --padding "0 1" \
  --margin "1 0" \
  "$(gum style --foreground 42 --bold 'Title')" \
  "$(gum style --foreground 245 'Subtitle')"

# Upgrade/warning box (double border)
gum style \
  --border double \
  --border-foreground 214 \
  --padding "1 2" \
  --margin "0 0 1 0" \
  "$(gum style --foreground 214 --bold 'UPGRADE DETECTED')" \
  "" \
  "$(gum style --foreground 252 'Found predecessor: old_tool')" \
  "$(gum style --foreground 42 '+ New feature 1')" \
  "$(gum style --foreground 42 '+ New feature 2')"

# Summary box (green border)
{
  gum style --foreground 42 --bold "Tool is now active!"
  echo ""
  for line in "${summary_lines[@]}"; do
    gum style --foreground 245 "$line"
  done
} | gum style --border normal --border-foreground 42 --padding "1 2"

# Agent scan notice
gum style \
  --border normal \
  --border-foreground 244 \
  --padding "0 1" \
  "$(gum style --foreground 212 --bold 'Agent scan')" \
  "$(gum style --foreground 247 'Scanning for installed coding agents...')" \
  "$(gum style --foreground 245 'This can take several minutes.')"
```

---

## Spinners

```bash
# Dot spinner (preferred style)
gum spin --spinner dot --title "Downloading artifact..." -- \
  curl -fsSL "$URL" -o "$TMP/$TAR"

# Wrapper function (recommended)
run_with_spinner() {
  local title="$1"; shift
  if [ "$HAS_GUM" -eq 1 ] && [ "$NO_GUM" -eq 0 ] && [ "$QUIET" -eq 0 ]; then
    gum spin --spinner dot --title "$title" -- "$@"
  else
    info "$title"
    "$@"
  fi
}

# Usage
run_with_spinner "Resolving latest version..." resolve_version
run_with_spinner "Downloading $TAR..." curl -fsSL "$URL" -o "$TMP/$TAR"
run_with_spinner "Verifying checksum..." verify_checksum "$TMP/$TAR" "$CHECKSUM"
```

---

## Confirmations

```bash
# Interactive confirmation
if [ "$HAS_GUM" -eq 1 ] && [ "$NO_GUM" -eq 0 ]; then
  if gum confirm "Remove predecessor and upgrade?"; then
    REMOVE=1
  fi
else
  echo -n "Remove predecessor and upgrade? (Y/n): "
  read -r ans
  case "$ans" in
    n|N|no|No|NO) REMOVE=0 ;;
    *) REMOVE=1 ;;
  esac
fi
```

---

## Italic / Muted Footer

```bash
# Uninstall instructions (footer style)
gum style --foreground 245 --italic \
  "To uninstall: rm $DEST/binary && remove hooks from settings"

# Revert instructions
gum style --foreground 245 --italic \
  "To revert: restore from backup files listed above"
```

---

## ANSI Fallback Equivalents

Every gum call needs an ANSI fallback for `--no-gum` or non-TTY:

| Gum | ANSI Equivalent |
|-----|-----------------|
| `gum style --foreground 39 "-> $*"` | `echo -e "\033[0;34m->\033[0m $*"` |
| `gum style --foreground 42 "✓ $*"` | `echo -e "\033[0;32m✓\033[0m $*"` |
| `gum style --foreground 214 "⚠ $*"` | `echo -e "\033[1;33m⚠\033[0m $*"` |
| `gum style --foreground 196 "✗ $*"` | `echo -e "\033[0;31m✗\033[0m $*"` |
| `gum style --bold "text"` | `echo -e "\033[1mtext\033[0m"` |
| `gum style --foreground 245 "text"` | `echo -e "\033[0;90mtext\033[0m"` |
| `gum spin --spinner dot --title "t" -- cmd` | `info "t" && cmd` |
| `gum confirm "question?"` | `echo -n "question? (Y/n): "; read -r ans` |

### Box Drawing Fallback

```bash
draw_box() {
  local color="$1"; shift
  local lines=("$@")
  local max_width=0
  local esc=$(printf '\033')
  local strip_ansi_sed="s/${esc}\\[[0-9;]*m//g"

  for line in "${lines[@]}"; do
    local stripped=$(printf '%b' "$line" | LC_ALL=C sed "$strip_ansi_sed")
    local len=${#stripped}
    [ "$len" -gt "$max_width" ] && max_width=$len
  done

  local inner_width=$((max_width + 4))
  local border=""
  for ((i=0; i<inner_width; i++)); do border+="═"; done

  printf "\033[%sm╔%s╗\033[0m\n" "$color" "$border"
  for line in "${lines[@]}"; do
    local stripped=$(printf '%b' "$line" | LC_ALL=C sed "$strip_ansi_sed")
    local len=${#stripped}
    local padding=$((max_width - len))
    local pad_str=""
    for ((i=0; i<padding; i++)); do pad_str+=" "; done
    printf "\033[%sm║\033[0m  %b%s  \033[%sm║\033[0m\n" "$color" "$line" "$pad_str" "$color"
  done
  printf "\033[%sm╚%s╝\033[0m\n" "$color" "$border"
}
```

---

## Color Numbers Quick Reference

| Number | Color | Use |
|--------|-------|-----|
| 39 | Blue | Info, primary actions |
| 42 | Green | Success, checkmarks |
| 196 | Red | Errors |
| 214 | Orange/Yellow | Warnings |
| 212 | Magenta | Accents, headers |
| 245 | Gray | Secondary text, descriptions |
| 247 | Light gray | Body text |
| 252 | Near-white | Emphasized body text |
