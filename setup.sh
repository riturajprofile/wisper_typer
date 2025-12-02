#!/bin/bash
set -e

echo "🚀 Starting Wisper Typer Setup..."

# 1. Check Root
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root (sudo ./setup.sh)"
  exit 1
fi

# Get real user (who ran sudo)
REAL_USER=${SUDO_USER:-$USER}
USER_HOME=$(getent passwd "$REAL_USER" | cut -d: -f6)

# 2. Install System Dependencies
echo "📦 Installing system dependencies..."
if command -v apt &> /dev/null; then
    apt update && apt install -y python3-pip python3-venv portaudio19-dev wl-clipboard
elif command -v dnf &> /dev/null; then
    dnf install -y python3-pip portaudio-devel wl-clipboard
elif command -v pacman &> /dev/null; then
    pacman -S --noconfirm python-pip portaudio wl-clipboard
else
    echo "⚠️  Package manager not detected. Please ensure 'portaudio' and 'wl-clipboard' are installed."
fi

# 3. Create Config (User & Root)
CONFIG_CONTENT="# Wisper-Linux Configuration
# Get your API key from https://console.groq.com/keys
GROQ_API_KEY=
# Hotkey to trigger recording (default: f4)
WISPER_HOTKEY=f4"

# User Config
USER_CONFIG="$USER_HOME/.wisper-typer"
if [ ! -f "$USER_CONFIG" ]; then
    echo "📝 Creating user config at $USER_CONFIG..."
    echo "$CONFIG_CONTENT" > "$USER_CONFIG"
    chown "$REAL_USER:$REAL_USER" "$USER_CONFIG"
    echo "⚠️  IMPORTANT: Edit $USER_CONFIG to add your GROQ_API_KEY!"
else
    echo "✅ User config already exists."
fi

# Root Config (for Service/Sudo)
ROOT_CONFIG="/root/.wisper-typer"
if [ ! -f "$ROOT_CONFIG" ]; then
    echo "📝 Creating root config (linked to user config)..."
    ln -sf "$USER_CONFIG" "$ROOT_CONFIG"
fi

# 4. Build Pip Package
echo "🔨 Building Pip Package..."
pip install --upgrade build
python3 -m build

# 5. Install Package
echo "📦 Installing Wisper Typer..."
pip install .

# 6. Service Setup
echo "⚙️  Configuring Systemd Service..."
SERVICE_FILE="wisper_typer.service"
DEST_SERVICE="/etc/systemd/system/wisper_typer.service"

cp "$SERVICE_FILE" "$DEST_SERVICE"
systemctl daemon-reload
systemctl enable wisper_typer
systemctl restart wisper_typer

echo "✅ Setup Complete!"
echo "   - Config: $USER_CONFIG"
echo "   - Service: active (check with 'systemctl status wisper_typer')"
echo "   - To run manually: sudo wisper"
