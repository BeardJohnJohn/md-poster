#!/bin/bash
# XHS Card Generator — Quick Setup
# One command to install all dependencies

echo "📦 Installing Python dependencies..."
pip install playwright

echo "🌐 Installing Chromium browser..."
playwright install chromium

echo ""
echo "✅ Setup complete!"
echo ""
echo "Quick start:"
echo "  cd examples/basic"
echo "  python xhs_pages.py"
echo "  python ../../scripts/screenshot.py --auto-height"
echo ""
echo "Your card images will be in examples/basic/output/"
