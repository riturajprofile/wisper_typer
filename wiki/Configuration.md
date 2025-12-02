# Configuration Guide

Learn how to configure Wisper Typer for your needs.

## Configuration File

Wisper Typer uses a configuration file located at `~/.wisper-typer`.

### Initial Setup

Run Wisper Typer once to generate the default configuration:
```bash
wisper
```

This creates `~/.wisper-typer` with default settings.

### Configuration Options

Edit the configuration file:
```bash
nano ~/.wisper-typer
```

#### Available Settings

```bash
# Groq API Key (Required)
GROQ_API_KEY=gsk_your_api_key_here

# Hotkey Configuration (Default: ctrl+win)
HOTKEY=ctrl+win

# Audio Settings
SAMPLE_RATE=16000
CHANNELS=1

# Model Configuration
MODEL=whisper-large-v3-turbo

# Logging
LOG_LEVEL=INFO
LOG_FILE=~/.wisper-typer.log
```

## Configuration Details

### API Key Setup

1. Get your Groq API key from [console.groq.com](https://console.groq.com)
2. Add it to `~/.wisper-typer`:
   ```bash
   GROQ_API_KEY=gsk_your_actual_key_here
   ```

See [API Setup](API-Setup.md) for detailed instructions.

### Hotkey Customization

The default hotkey is `ctrl+win`. You can customize it:

**Examples:**
- `ctrl+alt` - Control + Alt
- `f4` - Function key F4
- `shift+f5` - Shift + F5

**Syntax:**
- Use `+` to combine modifiers
- Valid modifiers: `ctrl`, `alt`, `shift`, `win`
- Valid keys: `f1-f12`, `a-z`, etc.

### Audio Settings

**SAMPLE_RATE**: Audio sample rate in Hz (default: 16000)
- Higher values = better quality but larger files
- Whisper models work best with 16000 Hz

**CHANNELS**: Audio channels (default: 1 for mono)
- 1 = Mono (recommended)
- 2 = Stereo

### Model Selection

Current default: `whisper-large-v3-turbo`

Available Groq models:
- `whisper-large-v3-turbo` (fastest, recommended)
- `whisper-large-v3` (more accurate, slower)

### Logging Configuration

**LOG_LEVEL**: Controls log verbosity
- `DEBUG` - Detailed debugging information
- `INFO` - General information (default)
- `WARNING` - Warning messages only
- `ERROR` - Error messages only

**LOG_FILE**: Log file location (default: `~/.wisper-typer.log`)

## Viewing Logs

### Application Logs
```bash
tail -f ~/.wisper-typer.log
```

### Service Logs (if using systemd)
```bash
journalctl -u wisper_typer -f
```

## Environment Variables

You can also use environment variables instead of the config file:

```bash
export GROQ_API_KEY="gsk_your_key"
export HOTKEY="ctrl+alt"
wisper
```

## Next Steps

- [Set up systemd service](Systemd-Service.md)
- [Learn usage tips](Usage-Guide.md)
- [Troubleshooting](Troubleshooting.md)
