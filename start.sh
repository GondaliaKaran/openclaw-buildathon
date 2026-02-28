#!/bin/bash

# Quick start script for local development

set -e

echo "=========================================="
echo "Adaptive Vendor Evaluation Agent"
echo "Quick Start (Local Development)"
echo "=========================================="

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Configure your API keys in .env"
    echo "   Edit .env and add:"
    echo "   - OPENAI_API_KEY=your_key_here"
    echo "   - TELEGRAM_BOT_TOKEN=your_token_here"
    echo ""
    read -p "Press Enter after configuring .env..."
fi

# Check if venv exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Starting agent..."
python main.py
