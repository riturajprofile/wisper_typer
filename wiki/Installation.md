# Installation Guide

This guide covers installing Wisper Typer on Linux systems.

## Prerequisites

Before installing, ensure you have:
- Linux OS (Wayland or X11)
- Python 3.8 or higher
- Root/sudo access (for global hotkey and typing functionality)

## Method 1: Install from PyPI (Recommended)

### Step 1: Install Wisper Typer
```bash
pip install wisper_typer
```

### Step 2: Install System Dependencies

#### Debian/Ubuntu
```bash
sudo apt update
sudo apt install portaudio19-dev wl-clipboard
```

#### Fedora
```bash
sudo dnf install portaudio-devel wl-clipboard
```

#### Arch Linux
```bash
sudo pacman -S portaudio wl-clipboard
```

### Step 3: Verify Installation
```bash
wisper --version
```

## Method 2: Install from Source

### Step 1: Clone Repository
```bash
git clone https://github.com/riturajprofile/wisper_typer.git
cd wisper_typer
```

### Step 2: Install Dependencies
```bash
sudo apt install portaudio19-dev wl-clipboard  # Debian/Ubuntu
pip install -e .
```

### Step 3: Verify Installation
```bash
wisper --version
```

## Next Steps

After installation:
1. [Configure your API key](Configuration.md)
2. [Set up the systemd service](Systemd-Service.md) for autostart
3. [Learn how to use Wisper Typer](Usage-Guide.md)

## Troubleshooting Installation

### Python Version Issues
Ensure you're using Python 3.8+:
```bash
python3 --version
```

### Permission Issues
If you encounter permission errors, use `pip install --user wisper_typer` instead.

### Missing Dependencies
If modules are missing, reinstall dependencies:
```bash
pip install --upgrade --force-reinstall wisper_typer
```

For more help, see [Troubleshooting](Troubleshooting.md).
