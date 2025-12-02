# Usage Guide

Learn how to effectively use Wisper Typer for voice dictation on Linux.

## Basic Usage

Wisper Typer runs in the background and activates when you press the hotkey.

### Standard Workflow

1. **Press and hold** the hotkey (default: `ctrl+win`)
2. **Speak** clearly into your microphone
3. **Release** the hotkey when done
4. Text is automatically transcribed and typed

## Running Wisper Typer

### With Systemd Service (Recommended)

If you've installed the service, it starts automatically on boot:

```bash
# Check if running
systemctl status wisper_typer

# Start manually if needed
sudo systemctl start wisper_typer

# Stop
sudo systemctl stop wisper_typer

# Restart
sudo systemctl restart wisper_typer
```

### Manual Execution

Run without the service:
```bash
sudo wisper
```

**Note**: Requires `sudo` for global hotkey detection and keyboard simulation.

## Usage Tips

### Getting Best Results

1. **Speak Clearly**: Enunciate words for better accuracy
2. **Minimize Background Noise**: Use in quiet environments
3. **Use a Good Microphone**: Better input = better transcription
4. **Short Bursts**: Shorter recordings transcribe faster
5. **Practice Makes Perfect**: Learn optimal speaking pace

### Common Use Cases

#### Writing Emails
1. Focus cursor in email body
2. Press hotkey and dictate
3. Release - text appears automatically

#### Coding Comments
```python
# Press hotkey: "This function calculates the factorial of n"
# Result typed automatically
```

#### Chat Messages
Works in Slack, Discord, WhatsApp Web, etc.

#### Document Writing
Use with LibreOffice, Google Docs, or any text editor

### Punctuation

Simply speak punctuation naturally:
- "Hello comma world period" → "Hello, world."
- "Question mark" → "?"
- "Exclamation point" → "!"

## Monitoring Activity

### View Real-Time Logs

**Application logs:**
```bash
tail -f ~/.wisper-typer.log
```

**Service logs:**
```bash
journalctl -u wisper_typer -f
```

### Understanding Logs

Logs show:
- Hotkey press/release events
- Audio recording duration
- API request/response
- Transcription results
- Typing actions
- Errors (if any)

## Performance Expectations

- **Transcription Speed**: Usually 1-3 seconds
- **Accuracy**: Very high for clear speech
- **Memory Usage**: ~10-20MB
- **CPU Usage**: Minimal when idle

## Privacy & Security

- **Audio**: Recorded audio is sent to Groq API for processing
- **No Storage**: Audio is not stored locally or on Groq servers
- **API Key**: Keep your `GROQ_API_KEY` secure
- **Logs**: May contain transcribed text; review `~/.wisper-typer.log` periodically

## Keyboard Shortcuts

| Hotkey | Action |
|--------|--------|
| `ctrl+win` (default) | Record and transcribe |
| Configurable in `~/.wisper-typer` | Change to your preference |

## Advanced Usage

### Using in Scripts

You can trigger Wisper Typer programmatically if needed:
```bash
# Example: Check if service is running
if systemctl is-active --quiet wisper_typer; then
    echo "Wisper Typer is running"
fi
```

### Multiple Configurations

Create different configs for different scenarios:
```bash
# Work config
GROQ_API_KEY=work_key wisper

# Personal config
GROQ_API_KEY=personal_key wisper
```

## Next Steps

- [Configure advanced settings](Advanced-Configuration.md)
- [Troubleshoot issues](Troubleshooting.md)
- [Learn about systemd service](Systemd-Service.md)
