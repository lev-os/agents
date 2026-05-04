#!/bin/bash
#
# Setup Script for Skill_Seekers
# Ensures Skill_Seekers is properly installed and configured for project documentation codification
#

set -e  # Exit on error

SKILL_SEEKERS_DIR="$HOME/.claude/vendors/Skill_Seekers"
PYTHON_MIN_VERSION="3.10"

echo "🔧 Setting up Skill_Seekers for documentation codification..."
echo

# Check Python version
check_python_version() {
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 is not installed. Please install Python ${PYTHON_MIN_VERSION}+ first."
        exit 1
    fi

    python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    required_version=$(echo $PYTHON_MIN_VERSION)

    if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
        echo "❌ Python ${PYTHON_MIN_VERSION}+ is required. Found: $python_version"
        exit 1
    fi

    echo "✅ Python version: $python_version"
}

# Check if Skill_Seekers is installed
check_installation() {
    if [ ! -d "$SKILL_SEEKERS_DIR" ]; then
        echo "❌ Skill_Seekers not found at $SKILL_SEEKERS_DIR"
        echo "   Please clone the repository first:"
        echo "   git clone https://github.com/yusufkaraaslan/Skill_Seekers ~/.claude/vendors/Skill_Seekers"
        exit 1
    fi
    echo "✅ Skill_Seekers found at: $SKILL_SEEKERS_DIR"
}

# Install dependencies
install_dependencies() {
    echo
    echo "📦 Installing dependencies..."

    cd "$SKILL_SEEKERS_DIR"

    # Check if skill-seekers is already installed
    if command -v skill-seekers &> /dev/null; then
        echo "✅ skill-seekers CLI already installed"
    else
        echo "Installing skill-seekers package..."
        pip3 install -e . || {
            echo "❌ Failed to install skill-seekers"
            exit 1
        }
        echo "✅ skill-seekers CLI installed"
    fi

    # Verify installation
    if command -v skill-seekers &> /dev/null; then
        echo "✅ skill-seekers command is available"
        skill-seekers --version 2>/dev/null || echo "   (Version info unavailable)"
    else
        echo "⚠️  skill-seekers command not found in PATH"
        echo "   You may need to add it to your PATH or use: python3 -m skill_seekers"
    fi
}

# Display available configs
show_configs() {
    echo
    echo "📋 Available preset configurations:"
    echo

    cd "$SKILL_SEEKERS_DIR"

    if [ -d "configs" ]; then
        echo "Documentation configs:"
        ls -1 configs/*.json 2>/dev/null | grep -v "_unified\|_github\|_test\|example" | head -10

        echo
        echo "Unified multi-source configs:"
        ls -1 configs/*_unified.json 2>/dev/null | head -5

        echo
        echo "Total configs available: $(ls -1 configs/*.json 2>/dev/null | wc -l | tr -d ' ')"
    else
        echo "⚠️  configs directory not found"
    fi
}

# Main execution
main() {
    check_python_version
    check_installation
    install_dependencies
    show_configs

    echo
    echo "✅ Setup complete!"
    echo
    echo "📚 Quick start examples:"
    echo "   # Scrape documentation website:"
    echo "   cd $SKILL_SEEKERS_DIR"
    echo "   skill-seekers scrape --config configs/react.json --enhance-local"
    echo
    echo "   # GitHub repository analysis:"
    echo "   skill-seekers github --repo facebook/react"
    echo
    echo "   # Interactive mode:"
    echo "   skill-seekers scrape --interactive"
    echo
}

main "$@"
