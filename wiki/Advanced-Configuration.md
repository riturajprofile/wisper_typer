# Advanced Configuration

Advanced settings and customization options for power users.

## Advanced Audio Configuration

### Custom Audio Devices

List available audio devices:
```bash
python3 -c "import pyaudio; p = pyaudio.PyAudio(); print('\n'.join([f'{i}: {p.get_device_info_by_index(i)[\"name\"]}' for i in range(p.get_device_count())]))"
```

Configure specific device in `~/.wisper-typer`:
```bash
AUDIO_DEVICE_INDEX=2
```

### Audio Quality Settings

High-quality recording (larger files, better accuracy):
```bash
SAMPLE_RATE=48000
CHANNELS=2
CHUNK_SIZE=2048
```

Low-bandwidth (faster upload, lower quality):
```bash
SAMPLE_RATE=8000
CHANNELS=1
CHUNK_SIZE=512
```

### Noise Reduction

Enable noise filtering (experimental):
```bash
ENABLE_NOISE_REDUCTION=true
NOISE_REDUCTION_STRENGTH=0.5
```

## Advanced Hotkey Configuration

### Custom Key Combinations

Examples of advanced hotkeys:
```bash
# Single key
HOTKEY=f4

# Modifier + key
HOTKEY=ctrl+alt+v

# Multiple modifiers
HOTKEY=ctrl+shift+alt+r

# Function keys
HOTKEY=shift+f12
```

### Multiple Hotkeys

Set different hotkeys for different actions (if supported):
```bash
RECORD_HOTKEY=ctrl+win
CANCEL_HOTKEY=escape
```

## Performance Tuning

### Recording Optimization

```bash
# Minimum recording duration (ms)
MIN_RECORDING_DURATION=100

# Maximum recording duration (ms)
MAX_RECORDING_DURATION=60000

# Recording buffer size
AUDIO_BUFFER_SIZE=4096
```

### Network Optimization

```bash
# API timeout (seconds)
API_TIMEOUT=30

# Retry attempts on failure
API_RETRY_COUNT=3

# Retry delay (seconds)
API_RETRY_DELAY=1
```

### Memory Management

```bash
# Clear audio buffer after processing
CLEAR_BUFFER_AFTER_PROCESSING=true

# Maximum cached API responses
MAX_CACHE_SIZE=0
```

## Custom Typing Behavior

### Typing Speed

```bash
# Delay between keystrokes (ms)
# Lower = faster, 0 = instant
TYPING_DELAY=0

# Simulate human typing
SIMULATE_HUMAN_TYPING=false
```

### Post-Processing

```bash
# Auto-capitalize first letter
AUTO_CAPITALIZE=true

# Add space after typing
ADD_TRAILING_SPACE=true

# Convert newlines to spaces
CONVERT_NEWLINES=false
```

## Advanced Logging

### Detailed Logging

```bash
# Log level
LOG_LEVEL=DEBUG

# Log format
LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Date format
DATE_FORMAT="%Y-%m-%d %H:%M:%S"

# Multiple log files
LOG_TO_SYSLOG=true
SYSLOG_ADDRESS=/dev/log
```

### Separate Log Files

```bash
# Error logs
ERROR_LOG_FILE=~/.wisper-typer-errors.log

# API logs
API_LOG_FILE=~/.wisper-typer-api.log

# Audio logs
AUDIO_LOG_FILE=~/.wisper-typer-audio.log
```

## Model Configuration

### Model Selection

```bash
# Default model
MODEL=whisper-large-v3-turbo

# Language hint (optional)
LANGUAGE=en

# Temperature (0.0-1.0, lower = more focused)
TEMPERATURE=0.0
```

### Response Formatting

```bash
# Response format
RESPONSE_FORMAT=json

# Include timestamps
INCLUDE_TIMESTAMPS=false

# Word-level timestamps
WORD_TIMESTAMPS=false
```

## Custom Scripts

### Pre/Post Processing Hooks

Create custom scripts:

**~/.wisper-typer.d/pre-record.sh**:
```bash
#!/bin/bash
# Run before recording
echo "Starting recording at $(date)"
```

**~/.wisper-typer.d/post-transcribe.sh**:
```bash
#!/bin/bash
# Run after transcription
echo "Transcribed: $1"
```

Configure in `~/.wisper-typer`:
```bash
PRE_RECORD_HOOK=~/.wisper-typer.d/pre-record.sh
POST_TRANSCRIBE_HOOK=~/.wisper-typer.d/post-transcribe.sh
```

## Multi-User Configuration

### System-Wide Config

Create `/etc/wisper-typer.conf`:
```bash
# System-wide defaults
DEFAULT_MODEL=whisper-large-v3-turbo
DEFAULT_SAMPLE_RATE=16000
```

User-specific config overrides in `~/.wisper-typer`.

### Service per User

Create user-specific services:

**/etc/systemd/system/wisper_typer@.service**:
```ini
[Unit]
Description=Wisper Typer for %i
After=network.target sound.target

[Service]
Type=simple
User=%i
ExecStart=/usr/local/bin/wisper
Restart=always
Environment="HOME=/home/%i"

[Install]
WantedBy=multi-user.target
```

Enable for user:
```bash
sudo systemctl enable wisper_typer@username
sudo systemctl start wisper_typer@username
```

## Integration with Other Tools

### Clipboard Integration

Send to clipboard instead of typing:
```bash
OUTPUT_MODE=clipboard
```

### File Output

Save transcriptions to file:
```bash
OUTPUT_MODE=file
OUTPUT_FILE=~/transcriptions.txt
APPEND_MODE=true
TIMESTAMP_ENTRIES=true
```

### HTTP Webhook

Send transcriptions to webhook:
```bash
OUTPUT_MODE=webhook
WEBHOOK_URL=https://example.com/webhook
WEBHOOK_METHOD=POST
WEBHOOK_HEADERS=Authorization: Bearer token123
```

## Security & Privacy

### Encrypted Config

Store API key encrypted:
```bash
# Install age encryption
sudo apt install age

# Encrypt config
age -e -R ~/.ssh/id_ed25519.pub -o ~/.wisper-typer.enc < ~/.wisper-typer

# Load encrypted config (in systemd)
ExecStartPre=/bin/sh -c 'age -d -i /home/user/.ssh/id_ed25519 /home/user/.wisper-typer.enc > /tmp/wisper-typer'
Environment="CONFIG_FILE=/tmp/wisper-typer"
ExecStopPost=/bin/rm -f /tmp/wisper-typer
```

### Audit Logging

Log all transcriptions:
```bash
AUDIT_LOG=true
AUDIT_LOG_FILE=~/.wisper-typer-audit.log
AUDIT_LOG_FORMAT="%(timestamp)s - %(audio_duration)s - %(transcription)s"
```

## Development Mode

### Debug Configuration

```bash
# Enable debug mode
DEBUG=true

# Save audio files for debugging
SAVE_AUDIO_FILES=true
AUDIO_FILE_DIR=~/wisper-debug

# Verbose API logging
VERBOSE_API=true

# Mock mode (don't call API)
MOCK_MODE=false
MOCK_RESPONSE="This is a test transcription"
```

## Custom Build Options

### Build from Source with Optimizations

```bash
git clone https://github.com/riturajprofile/wisper_typer.git
cd wisper_typer

# Install with optimizations
CFLAGS="-O3 -march=native" pip install -e .
```

### Compile Dependencies

For better performance:
```bash
# Install with compiled dependencies
pip install --no-binary :all: wisper_typer
```

## Configuration Validation

Validate your configuration:
```bash
wisper --validate-config
```

Check for issues:
```bash
wisper --check-dependencies
```

## Example Advanced Configuration

Complete advanced `~/.wisper-typer`:
```bash
# API Configuration
GROQ_API_KEY=gsk_your_key_here
MODEL=whisper-large-v3-turbo
TEMPERATURE=0.0
LANGUAGE=en

# Hotkey
HOTKEY=ctrl+win

# Audio Settings
SAMPLE_RATE=16000
CHANNELS=1
CHUNK_SIZE=1024
AUDIO_DEVICE_INDEX=0

# Performance
API_TIMEOUT=30
API_RETRY_COUNT=3
MIN_RECORDING_DURATION=100
MAX_RECORDING_DURATION=60000

# Typing
TYPING_DELAY=0
AUTO_CAPITALIZE=true
ADD_TRAILING_SPACE=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=~/.wisper-typer.log
AUDIT_LOG=true

# Privacy
SAVE_AUDIO_FILES=false
```

## Platform-Specific Settings

### Wayland-Specific

```bash
WAYLAND_DISPLAY=wayland-0
USE_WL_CLIPBOARD=true
```

### X11-Specific

```bash
DISPLAY=:0
XAUTHORITY=~/.Xauthority
```

## Next Steps

- [Basic Configuration](Configuration.md)
- [Troubleshooting](Troubleshooting.md)
- [Usage Guide](Usage-Guide.md)
