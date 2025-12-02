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

The easiest way to install, build, and configure everything (including the service) is to run the setup script:

```bash
cd wisper_typer
sudo ./setup.sh
```

This script will:
1.  Install system dependencies (`portaudio`, `wl-clipboard`).
2.  Create the config file at `~/.wisper-typer`.
3.  Build and install the python package.
4.  Set up and start the systemd service.

### Manual Installation
If you prefer to install manually:
```bash
pip install .
```

## Usage

### 1. Configuration
Create `~/.wisper-typer` with your API key:
```bash
# ~/.wisper-typer
GROQ_API_KEY=gsk_XXXX
WISPER_HOTKEY=f4
```

### 2. Running
**Crucial**: You must run with `sudo` **EVERY TIME**.

```bash
sudo wisper
```

#### ❓ Why Sudo?
The `keyboard` library needs root access to:
1.  **Read all keystrokes** (to detect your hotkey globally).
2.  **Inject keystrokes** (to simulate Ctrl+V).
Without `sudo`, the tool cannot see your hotkey or type the text.

#### 🔄 Autostart (Recommended)
If you use the systemd service (see below), it runs as root automatically in the background, so you **never** have to type `sudo` manually once it's set up.

## Autostart (Systemd)
To run automatically at startup:
1.  Edit `wisper_typer.service` to point to your installation.
2.  Copy to `/etc/systemd/system/`.
3.  Enable and start: `sudo systemctl enable --now wisper_typer`.

## Troubleshooting
- **Permission Denied**: If it crashes or doesn't type, ensure you are running with `sudo`.
- **No Typing on Wayland**: Ensure `wl-copy` is installed.
