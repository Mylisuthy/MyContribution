#!/bin/bash

# System Break Agent - Ubuntu Setup Script
# This script installs the agent as a systemd service with admin privileges.

echo "--- System Break Agent Setup ---"

# 1. Check for sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (use sudo)"
  exit 1
fi

# 2. Install system dependencies
echo "[1/5] Installing system dependencies..."
apt-get update
apt-get install -y python3 python3-venv net-tools iproute2 libpcap0.8 tcpdump util-linux

# 3. Setup Virtual Environment
echo "[2/5] Setting up Python virtual environment..."
AGENT_DIR=$(pwd)
python3 -m venv $AGENT_DIR/venv
source $AGENT_DIR/venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Create Systemd Service
echo "[3/5] Creating systemd service..."
SERVICE_FILE="/etc/systemd/system/sb-agent.service"

cat <<EOF > $SERVICE_FILE
[Unit]
Description=System Break Agent Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$AGENT_DIR
ExecStart=$AGENT_DIR/venv/bin/python3 main.py
Restart=always
Environment=PATH=$AGENT_DIR/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

[Install]
WantedBy=multi-user.target
EOF

# 5. Enable and Start Service
echo "[4/5] Enabling and starting service..."
systemctl daemon-reload
systemctl enable sb-agent
systemctl start sb-agent

echo "[5/5] Setup complete! Status:"
systemctl status sb-agent --no-pager

echo "-----------------------------------"
echo "Agent is now running as a daemon."
echo "Use 'sudo systemctl status sb-agent' to check status."
