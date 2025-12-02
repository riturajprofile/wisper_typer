#!/bin/bash
set -e

echo "🚀 Preparing to publish to PyPI..."

# 1. Install Twine
echo "📦 Installing build tools..."
pip install --upgrade build twine

# 2. Clean previous builds
echo "🧹 Cleaning up..."
rm -rf dist/ build/ *.egg-info

# 3. Build Package
echo "🔨 Building package..."
python3 -m build

# 4. Upload
echo "📤 Uploading to PyPI..."
echo "⚠️  You will need your PyPI API token (username: __token__)"
python3 -m twine upload dist/*

echo "✅ Published! Install with: pip install wisper_typer"
