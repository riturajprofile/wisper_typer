# Wisper Typer Wiki

Welcome to the **Wisper Typer** documentation! This wiki provides comprehensive guides for installation, configuration, usage, and troubleshooting.

## 📚 Contents

- **[Home](Home.md)** - This page
- **[Installation](Installation.md)** - Step-by-step installation guide
- **[Configuration](Configuration.md)** - Configuring Wisper Typer
- **[Usage Guide](Usage-Guide.md)** - How to use Wisper Typer effectively
- **[Systemd Service](Systemd-Service.md)** - Setting up autostart with systemd
- **[Troubleshooting](Troubleshooting.md)** - Common issues and solutions
- **[API Setup](API-Setup.md)** - Getting your Groq API key
- **[Advanced Configuration](Advanced-Configuration.md)** - Advanced settings and customization

## 🚀 Quick Start

1. Install: `pip install wisper_typer`
2. Install system dependencies: `sudo apt install portaudio19-dev wl-clipboard`
3. Configure: Run `wisper` to create config, then edit `~/.wisper-typer` with your API key
4. Setup service: `sudo wisper --install-service`
5. Use: Press `ctrl+win`, speak, and release!

## 🌟 Features

- **Ultra-Fast Transcription**: Uses Groq's whisper-large-v3-turbo model
- **Wayland & X11 Support**: Works on modern Linux desktops
- **Global Hotkey**: Background operation with customizable hotkey
- **Auto-Typing**: Automatically types transcribed text
- **Systemd Integration**: Auto-start on boot
- **Minimal Resource Usage**: CLI-based design for maximum efficiency

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests on [GitHub](https://github.com/riturajprofile/wisper_typer).

## 📝 License

MIT License - See [LICENSE](https://github.com/riturajprofile/wisper_typer/blob/main/LICENSE) for details.
