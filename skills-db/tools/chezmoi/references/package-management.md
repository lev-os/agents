# Package Management with Chezmoi

Sync CLI tools and packages across machines automatically using chezmoi's `run_onchange_` scripts.

## Overview

When you install a new CLI tool on one machine, you want it automatically available on all your machines. This guide shows how to maintain package manifests in chezmoi that auto-install when changed.

## Package Manifests Location

```
~/.local/share/chezmoi/exact_dot_dotfiles/exact_install/
├── Brewfile              # Homebrew packages (formulae, casks, fonts)
├── bun-globals.txt       # Bun global packages
└── pnpm-globals.txt      # PNPM global packages

~/.nvm/default-packages   # npm/nvm packages (already tracked by chezmoi)
```

## How It Works

1. **Edit package manifest** in chezmoi source
2. **Chezmoi detects change** via hash in `run_onchange_after_packages.sh.tmpl`
3. **Auto-installs** on next `chezmoi apply`
4. **New machine:** `chezmoi init --apply` installs everything

## Adding Packages

### Homebrew (formulae, casks, fonts)

Edit `~/.dotfiles/install/Brewfile`:

```ruby
# Add a CLI tool
brew "ripgrep"

# Add an application
cask "visual-studio-code"

# Add a font
cask "font-jetbrains-mono-nerd-font"
```

Then sync:
```bash
chezmoi re-add ~/.dotfiles/install/Brewfile
chezmoi apply
```

### Bun Global Packages

Edit `~/.dotfiles/install/bun-globals.txt`:

```
# Add package name (one per line)
netlify-cli
clawdhub

# GitHub packages supported
github:user/repo#commit
```

Then sync:
```bash
chezmoi re-add ~/.dotfiles/install/bun-globals.txt
chezmoi apply
```

### PNPM Global Packages

Edit `~/.dotfiles/install/pnpm-globals.txt`:

```
# Add package name (one per line)
@mixedbread/mgrep
turbo
```

Then sync:
```bash
chezmoi re-add ~/.dotfiles/install/pnpm-globals.txt
chezmoi apply
```

### npm/nvm Packages

Edit `~/.nvm/default-packages`:

```
# Add package name (one per line)
typescript
prettier
eslint
```

**Note:** nvm auto-installs these when you install a new Node version via `nvm install`.

To sync immediately:
```bash
chezmoi re-add ~/.nvm/default-packages
chezmoi apply
# Then manually: npm install -g <package>
```

## Workflow Recipes

### Quick Add: Install on Current Machine + Track

```bash
# Homebrew
brew install ripgrep
echo 'brew "ripgrep"' >> ~/.dotfiles/install/Brewfile
chezmoi re-add ~/.dotfiles/install/Brewfile

# Bun
bun install -g netlify-cli
echo 'netlify-cli' >> ~/.dotfiles/install/bun-globals.txt
chezmoi re-add ~/.dotfiles/install/bun-globals.txt

# PNPM
pnpm add -g turbo
echo 'turbo' >> ~/.dotfiles/install/pnpm-globals.txt
chezmoi re-add ~/.dotfiles/install/pnpm-globals.txt
```

### Sync to New Machine

```bash
# One-liner bootstrap
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply <github-username>

# Packages auto-install via run_onchange_after_packages.sh.tmpl
```

### Update All Packages

```bash
# Pull latest manifests from git
chezmoi update

# Packages auto-install if manifests changed
```

### Manual Install (without waiting for chezmoi apply)

```bash
# Homebrew
brew bundle --file=~/.dotfiles/install/Brewfile

# Bun
cat ~/.dotfiles/install/bun-globals.txt | grep -v '^#' | xargs -I {} bun install -g {}

# PNPM
cat ~/.dotfiles/install/pnpm-globals.txt | grep -v '^#' | xargs -I {} pnpm add -g {}
```

## XDG Paths to Track

### ✅ Track These (Config Files)

| Path | What | Why |
|------|------|-----|
| `~/.config/git/` | Git config | User settings, aliases |
| `~/.config/gh/` | GitHub CLI config | Hosts, preferences (not tokens) |
| `~/.config/nvim/` | Neovim config | Editor setup |
| `~/.config/iterm2/` | iTerm2 prefs | Terminal settings |
| `~/.config/chezmoi/` | Chezmoi config | Machine-specific data |
| `~/.nvm/default-packages` | npm defaults | Auto-install list |

### ❌ Don't Track These (Generated/Cache)

| Path | What | Why |
|------|------|-----|
| `~/.local/share/pnpm/global/` | PNPM installs | Generated from manifest |
| `~/.bun/install/global/` | Bun installs | Generated from manifest |
| `~/.cache/` | Cache files | Temporary, machine-specific |
| `~/.local/state/` | State files | Runtime data |
| `~/.npm/` | npm cache | Temporary |

### ⚠️ Maybe Track (Case-by-Case)

| Path | What | Consider |
|------|------|----------|
| `~/.config/raycast/` | Raycast settings | Large, changes often |
| `~/.config/vscode/` | VS Code settings | May prefer Settings Sync |
| `~/.ssh/config` | SSH config | Track, but encrypt keys |

## Troubleshooting

### Packages not installing on `chezmoi apply`

Check if script ran:
```bash
chezmoi apply -v
# Look for: "Running .chezmoiscripts/run_onchange_after_packages.sh.tmpl"
```

Force re-run:
```bash
# Edit the script to change hash (add a comment)
chezmoi edit ~/.local/share/chezmoi/.chezmoiscripts/run_onchange_after_packages.sh.tmpl
# Then apply
chezmoi apply
```

### Brewfile syntax errors

Validate:
```bash
brew bundle check --file=~/.dotfiles/install/Brewfile
```

### Package manager not found

The script skips missing package managers. Install them first:
```bash
# Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Bun
brew install oven-sh/bun/bun

# PNPM
brew install pnpm
```

## Advanced: Custom Package Managers

To add support for other package managers (cargo, pip, gem, etc.), edit:

```bash
chezmoi edit ~/.local/share/chezmoi/.chezmoiscripts/run_onchange_after_packages.sh.tmpl
```

Add a new section following the existing pattern:

```bash
# Cargo crates
if command -v cargo &>/dev/null; then
    echo ""
    echo "🦀 Installing Cargo crates..."
    while IFS= read -r pkg; do
        [[ -z "$pkg" || "$pkg" =~ ^[[:space:]]*# ]] && continue
        echo "  → $pkg"
        cargo install "$pkg" 2>/dev/null || echo "    ⚠️  Failed to install $pkg"
    done < "{{ joinPath .chezmoi.sourceDir "exact_dot_dotfiles/exact_install/cargo-crates.txt" }}"
fi
```

Then create the manifest file and update the hash calculation at the top of the script.
