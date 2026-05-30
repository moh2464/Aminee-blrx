#!/bin/bash

# Free Fire Bot Launcher - Linux/macOS

echo ""
echo "╔════════════════════════════════════════╗"
echo "║   Free Fire Bot - Launcher             ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install from https://www.python.org/"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create venv
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check .env
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✅ Created .env - please edit it"
    exit 0
fi

echo ""
echo "╔════════════════════════════════════════╗"
echo "║   Starting Free Fire Bot...            ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Run bot
python3 main.py

# Cleanup
deactivate