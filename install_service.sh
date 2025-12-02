#!/bin/bash

echo "🚀 Installing Wisper Typer Service..."

# Ensure running as root
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root (sudo)."
  exit 1
fi

# Install package
echo "📦 Installing Python package..."
pip install .

# Copy service file
echo "⚙️  Configuring Systemd..."
cp wisper_typer.service /etc/systemd/system/wisper_typer.service

# Reload and enable
systemctl daemon-reload
systemctl enable wisper_typer
systemctl start wisper_typer

echo "✅ Installation Complete!"
echo "   Service status: systemctl status wisper_typer"
