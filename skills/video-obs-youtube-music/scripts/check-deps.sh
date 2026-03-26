#!/bin/bash
# Check dependencies for video-obs-youtube-music skill

errors=0

check_cmd() {
    if ! command -v "$1" &>/dev/null; then
        echo "❌ Missing: $1"
        errors=$((errors + 1))
    else
        version=$("$1" --version 2>&1 | head -1)
        echo "✓ $1: $version"
    fi
}

echo "=== video-obs-youtube-music dependencies ==="
echo
check_cmd ffmpeg
check_cmd ffprobe
check_cmd yt-dlp

# Check playwright (optional, for card generation)
echo
echo "=== Optional (for song credit cards) ==="

# Check node (optional - don't increment errors)
if command -v node &>/dev/null; then
    version=$(node --version 2>&1)
    echo "✓ node: $version"

    # Check if playwright is installed as npm package
    if node -e "require('playwright')" 2>/dev/null; then
        echo "✓ playwright: installed"
    else
        echo "⚠ playwright: not installed (optional)"
        echo "  Install: npm install playwright && npx playwright install chromium"
    fi
else
    echo "⚠ node: not installed (optional)"
    echo "  Install: brew install node"
    echo "  Then: npm install playwright && npx playwright install chromium"
fi

echo
if [ $errors -eq 0 ]; then
    echo "✓ All core dependencies installed"
    exit 0
else
    echo "❌ Missing $errors core dependencies"
    echo "Install: brew install ffmpeg yt-dlp"
    exit 1
fi
