#!/bin/bash
set -e

echo "🔧 Installing Valyu CLI..."

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js not found. Install from https://nodejs.org"
    exit 1
fi

# Check for npm
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm not found"
    exit 1
fi

# Navigate to CLI directory
cd "$(dirname "$0")"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build TypeScript
echo "🔨 Building CLI..."
npm run build

# Link globally
echo "🔗 Linking globally..."
npm link

# Create config directory
mkdir -p ~/.valyu

# Check for API key
if [ ! -f ~/.valyu/.env ]; then
    echo ""
    echo "⚠️  VALYU_API_KEY not configured"
    echo ""
    echo "Create ~/.valyu/.env with:"
    echo "VALYU_API_KEY=your-api-key-here"
    echo ""
    echo "Get your API key from: https://platform.valyu.ai"
else
    echo "✓ API key configured in ~/.valyu/.env"
fi

echo ""
echo "✅ Valyu CLI installed successfully!"
echo ""
echo "Usage:"
echo "  valyu search \"your query\""
echo "  valyu answer \"your question\""
echo "  valyu research \"deep research topic\" --turns 5"
echo ""
echo "Run 'valyu --help' for more information"
