#!/bin/bash

# Deployment script for Hostinger VPS

set -e

echo "==========================================
echo "Adaptive Vendor Evaluation Agent"
echo "Deployment Script for Hostinger VPS"
echo "=========================================="

# Configuration
APP_DIR="/home/$(whoami)/openclaw-buildathon"
VENV_DIR="$APP_DIR/venv"
SERVICE_NAME="vendor-agent"

echo "Step 1: Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv
else
    echo "Python 3 found: $(python3 --version)"
fi

echo ""
echo "Step 2: Setting up application directory..."
cd $APP_DIR
echo "Working directory: $APP_DIR"

echo ""
echo "Step 3: Creating virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

echo ""
echo "Step 4: Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Step 5: Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "Dependencies installed"

echo ""
echo "Step 6: Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your API keys:"
    echo "   - OPENAI_API_KEY"
    echo "   - TELEGRAM_BOT_TOKEN"
    echo ""
    echo "   Run: nano .env"
    echo ""
    read -p "Press Enter after configuring .env..."
else
    echo ".env file found"
fi

echo ""
echo "Step 7: Setting up systemd service..."
sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null <<EOF
[Unit]
Description=Adaptive Vendor Evaluation Agent
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "Systemd service created"

echo ""
echo "Step 8: Enabling and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "Service Status:"
sudo systemctl status $SERVICE_NAME --no-pager
echo ""
echo "Useful Commands:"
echo "  View logs:     sudo journalctl -u $SERVICE_NAME -f"
echo "  Stop service:  sudo systemctl stop $SERVICE_NAME"
echo "  Start service: sudo systemctl start $SERVICE_NAME"
echo "  Restart:       sudo systemctl restart $SERVICE_NAME"
echo ""
echo "Next Steps:"
echo "1. Verify your .env configuration"
echo "2. Check logs for any errors"
echo "3. Send /start to your Telegram bot"
echo ""
