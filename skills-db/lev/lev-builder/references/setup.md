# Skill_Seekers Installation Guide

Complete installation instructions with automatic environment detection (uv/venv/pip).

## Prerequisites

- **Python 3.10+** (required for Skill_Seekers)
- **Git 2.30+** (for cloning the repository)
- Working directory with read/write permissions

## Quick Install (Recommended)

The installation process automatically detects your environment and chooses the best installation method:

```bash
# This command handles everything:
# 1. Checks for uv, venv, or falls back to pip
# 2. Clones Skill_Seekers if needed
# 3. Installs dependencies
# 4. Verifies installation

python3 -c "$(curl -fsSL https://raw.githubusercontent.com/yusufkaraaslan/Skill_Seekers/main/setup.py)"
```

## Manual Installation

### Step 1: Check Python Version

```bash
python3 --version
# Should be 3.10 or higher
```

If Python 3.10+ is not installed:
- **macOS**: `brew install python@3.11`
- **Ubuntu/Debian**: `sudo apt install python3.11`
- **Windows**: Download from python.org

### Step 2: Clone Skill_Seekers

Choose a location for the Skill_Seekers tool:

```bash
# Option A: Clone to project directory (recommended for project-specific use)
git clone https://github.com/yusufkaraaslan/Skill_Seekers.git
cd Skill_Seekers

# Option B: Clone to global location (for system-wide use)
git clone https://github.com/yusufkaraaslan/Skill_Seekers.git ~/.local/share/skill-seekers
cd ~/.local/share/skill-seekers
```

### Step 3: Environment Detection & Installation

**The installation method depends on what's available in your project:**

#### Option A: Using uv (Fastest - Recommended)

If your project uses `uv` (modern Python package manager):

```bash
cd Skill_Seekers

# Check if uv is available
command -v uv

# Install with uv
uv tool install skill-seekers

# Or run directly without installing
uv tool run --from skill-seekers skill-seekers --version
```

**Benefits of uv:**
- ⚡ 10-100x faster than pip
- 🔒 Automatic dependency resolution
- 📦 Isolated tool installation
- ✅ Works without activating environments

#### Option B: Using venv (Standard)

If your project uses traditional virtual environments:

```bash
cd Skill_Seekers

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR on Windows:
venv\Scripts\activate

# Install skill-seekers
pip install -e .

# Verify installation
skill-seekers --version
```

**Remember:** Always activate venv before using:
```bash
source venv/bin/activate  # Run this each session
```

#### Option C: Using pip (Global Install)

If you prefer global installation:

```bash
cd Skill_Seekers

# Install globally (may require sudo)
pip3 install -e .

# Or install from PyPI
pip3 install skill-seekers

# Verify
skill-seekers --version
```

⚠️ **Warning:** Global pip install may conflict with system packages. Use venv or uv instead.

### Step 4: Verify Installation

Test that everything works:

```bash
# Test command availability
skill-seekers --version

# List available configs
ls configs/

# Quick test scrape (20 pages, ~2 minutes)
skill-seekers scrape --name test --url https://react.dev/ --max-pages 20
```

## Environment Detection Script

For automatic environment detection, use this approach in the current project:

```bash
#!/bin/bash
# Detects and uses best available Python environment

detect_and_install() {
    # Check for uv first (fastest)
    if command -v uv &> /dev/null; then
        echo "✅ Using uv (fast mode)"
        uv tool install skill-seekers
        return 0
    fi

    # Check for active venv
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "✅ Using active virtual environment: $VIRTUAL_ENV"
        pip install -e .
        return 0
    fi

    # Check for project venv
    if [ -d "venv" ] || [ -d ".venv" ]; then
        echo "✅ Found project venv, activating..."
        source venv/bin/activate 2>/dev/null || source .venv/bin/activate
        pip install -e .
        return 0
    fi

    # Offer to create venv
    echo "⚠️  No uv or venv found."
    read -p "Create virtual environment? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 -m venv venv
        source venv/bin/activate
        pip install -e .
        return 0
    fi

    # Fall back to pip
    echo "⚠️  Installing globally with pip (not recommended)"
    pip3 install -e .
}

detect_and_install
```

## Troubleshooting

### Command Not Found After Installation

**Problem:** `skill-seekers: command not found`

**Solutions:**

1. **Check if venv is activated:**
   ```bash
   which python3  # Should show venv path if activated
   source venv/bin/activate
   ```

2. **Use Python module syntax:**
   ```bash
   python3 -m skill_seekers scrape --help
   ```

3. **Check PATH:**
   ```bash
   echo $PATH | grep -o "[^:]*bin"
   # Should include venv/bin or .local/bin
   ```

### Permission Denied

**Problem:** Permission errors during installation

**Solution:**
```bash
# Use venv instead of global install
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Python Version Too Old

**Problem:** `Python 3.10+ required`

**Solution:**
```bash
# macOS
brew install python@3.11
python3.11 -m venv venv

# Ubuntu/Debian
sudo apt install python3.11
python3.11 -m venv venv
```

### uv Not Found

**Problem:** `uv: command not found`

**Solution:**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or use pip
pip install uv
```

## Project-Specific Installation

When working in a specific project that needs documentation codified:

```bash
# Navigate to your project
cd /path/to/your/project

# Clone Skill_Seekers to project directory
git clone https://github.com/yusufkaraaslan/Skill_Seekers.git

# Use project's environment
cd Skill_Seekers

# If project uses uv:
uv tool install skill-seekers

# If project uses venv:
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Now skill-seekers is available in project context
```

## Verification Checklist

After installation, verify these work:

- [ ] `skill-seekers --version` shows version number
- [ ] `skill-seekers --help` shows command options
- [ ] `ls configs/` shows preset configurations
- [ ] Python 3.10+ is active: `python3 --version`
- [ ] Git is available: `git --version`

## Next Steps

Once installed:

1. Return to main SKILL.md for workflow instructions
2. See `references/config-guide.md` for configuration options
3. Check `references/advanced-workflows.md` for optimization
4. Run a test scrape with a small documentation site

## Quick Reference

| Environment | Install Command | Usage |
|------------|-----------------|-------|
| **uv** | `uv tool install skill-seekers` | `skill-seekers <command>` |
| **venv** | `pip install -e .` (in activated venv) | `skill-seekers <command>` |
| **pip** | `pip3 install skill-seekers` | `skill-seekers <command>` |
| **module** | No install needed | `python3 -m skill_seekers <command>` |
