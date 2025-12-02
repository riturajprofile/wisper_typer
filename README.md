# Wisper Typer

**Ultra-fast**, CLI-based AI Dictation tool for Linux using Groq API.
Designed for **Wayland** and **X11** with a focus on speed and minimalism.

## Features
- **Ultra-Fast**: Uses Groq's `whisper-large-v3-turbo` model for near-instant transcription.
- **Wayland Native**: Uses `uinput` (via `keyboard`) and `wl-clipboard` for compatibility with modern Linux desktops.
- **Global Hotkey**: Press and hold to record (default: F4).
- **Auto-Typing**: Automatically types the text into any application.

## Prerequisites
- Linux OS
- Python 3.8+
- `portaudio` (usually `libportaudio2` or `portaudio19-dev`)
- **Root Privileges**: Required for global hotkey detection and simulated typing (`uinput`).
- **Wayland Users**: Ensure `wl-clipboard` is installed (`sudo apt install wl-clipboard` or equivalent).

## Installation

### 1. Install via Pip
```bash
pip install wisper_typer
```

### 2. Install System Dependencies
Ensure you have the required system libraries:
- **Debian/Ubuntu**: `sudo apt install portaudio19-dev wl-clipboard`
- **Fedora**: `sudo dnf install portaudio-devel wl-clipboard`
- **Arch**: `sudo pacman -S portaudio wl-clipboard`

### 3. Configure
Create `~/.wisper-typer` with your API key:
```bash
# ~/.wisper-typer
GROQ_API_KEY=gsk_XXXX
WISPER_HOTKEY=f4
```

### 4. Setup Autostart Service (Optional but Recommended)
Run this once to install the systemd service so it runs automatically on startup:
```bash
sudo wisper --install-service
```

## Usage

### 🚀 How to Use
Once installed (manually or via service), **Wisper Typer runs in the background**.

1.  **Press and Hold** the hotkey (Default: `F4`).
2.  **Speak** into your microphone.
3.  **Release** the hotkey.
4.  The text will be **automatically typed** into your active window.

### 🛠️ Managing the Service
If you installed the service (`sudo wisper --install-service`), it starts automatically on boot.

- **Check Status**: `systemctl status wisper_typer`
- **Restart**: `sudo systemctl restart wisper_typer`
- **Stop**: `sudo systemctl stop wisper_typer`
- **Logs**: `journalctl -u wisper_typer -f` (View real-time logs)

### 🏃 Manual Run (No Service)
If you didn't install the service, you must run it manually **every time** you want to use it:
```bash
sudo wisper
```
*(Must use `sudo` for global hotkey detection)*

## Autostart (Systemd)
To run automatically at startup:
1.  Edit `wisper_typer.service` to point to your installation.
2.  Copy to `/etc/systemd/system/`.
3.  Enable and start: `sudo systemctl enable --now wisper_typer`.

## Troubleshooting
- **Permission Denied**: If it crashes or doesn't type, ensure you are running with `sudo`.
- **No Typing on Wayland**: Ensure `wl-copy` is installed.
