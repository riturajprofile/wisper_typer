# Wisper Typer

**Ultra-fast**, CLI-based AI Dictation tool for Linux using Groq API.
Designed for **Wayland** and **X11** with a focus on speed and minimalism.

## Features
- **Ultra-Fast**: Uses Groq's `whisper-large-v3-turbo` model for near-instant transcription.
- **Wayland Native**: Uses `uinput` (via `keyboard`) and `wl-clipboard` for compatibility with modern Linux desktops.
- **Global Hotkey**: Press and hold to record (default: F4).
- **Auto-Typing**: Automatically types the text into any application.

## Why CLI-Based?

wisper-typer is intentionally designed as a **no-GUI, CLI-based tool** for several key advantages:

### 🚀 Performance & Resources
- **Minimal Memory Footprint**: ~10-20MB vs 200-500MB for GUI apps
- **Zero UI Overhead**: No window rendering, no graphics libraries
- **Instant Startup**: Launches in milliseconds, not seconds
- **Runs in Background**: No screen clutter or visual distraction

### 🌍 Universal Compatibility
- **Works Everywhere**: Browser, terminal, text editors, chat apps - anywhere you can paste
- **No App Integration**: Doesn't need plugins for Chrome, Firefox, VS Code, etc.
- **System-Level**: One tool for all applications instead of per-app extensions
- **Future-Proof**: Works with apps that don't exist yet

### ⚙️ Simple Deployment
- **Systemd Service**: Auto-start on boot, runs silently
- **No Display Required**: Can run on headless systems (with audio)
- **Remote SSH Friendly**: Control via command line
- **Easy Automation**: Scriptable and configurable

### 🎯 Design Philosophy
- **Do One Thing Well**: Transcribe speech and type it - that's it
- **Stay Out of Your Way**: No windows to manage, no UI to learn
- **Power User Friendly**: Configure via files, control via hotkeys

A GUI would add complexity without adding value - the global hotkey **is** the interface!

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
Run `wisper` once to generate the configuration file:
```bash
wisper
```
It will create `~/.wisper-typer`. Edit it to add your API key:
```bash
nano ~/.wisper-typer
# Add your key: GROQ_API_KEY=gsk_XXXX
# Default hotkey is ctrl+win
```

### 4. Setup Autostart Service (Optional but Recommended)
Run this once to install the systemd service so it runs automatically on startup:
```bash
sudo wisper --install-service
```

## Usage

### 🚀 How to Use
Once installed (manually or via service), **Wisper Typer runs in the background**.

1.  **Press and Hold** the hotkey (Default: `ctrl+win`).
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

### Logs
All activity is logged to `~/.wisper-typer.log`. View logs with:
```bash
tail -f ~/.wisper-typer.log
```

For service logs, use:
```bash
journalctl -u wisper_typer -f
```

### Common Issues
- **Permission Denied**: If it crashes or doesn't type, ensure you are running with `sudo`.
- **No Typing on Wayland**: Ensure `wl-copy` is installed.
- **Microphone Not Working**: Check your audio input device with `arecord -l`.
- **API Errors**: Verify your `GROQ_API_KEY` is correct in `~/.wisper-typer`.
