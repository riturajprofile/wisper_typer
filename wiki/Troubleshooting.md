# Troubleshooting

Common issues and solutions for Wisper Typer.

## Installation Issues

### Python Version Errors

**Problem**: Error about Python version when installing

**Solution**:
```bash
# Check Python version
python3 --version

# Ensure it's 3.8 or higher
# If not, install newer Python:
sudo apt install python3.10  # Debian/Ubuntu
```

### Pip Installation Fails

**Problem**: `pip install wisper_typer` fails

**Solutions**:
1. Try with user flag:
   ```bash
   pip install --user wisper_typer
   ```

2. Upgrade pip:
   ```bash
   pip install --upgrade pip
   ```

3. Install system dependencies first:
   ```bash
   sudo apt install portaudio19-dev
   ```

### Missing portaudio

**Problem**: `portaudio.h: No such file or directory`

**Solution**:
```bash
# Debian/Ubuntu
sudo apt install portaudio19-dev

# Fedora
sudo dnf install portaudio-devel

# Arch
sudo pacman -S portaudio
```

## Runtime Issues

### Permission Denied

**Problem**: `PermissionError` when running wisper

**Solution**: Run with sudo (required for global hotkeys):
```bash
sudo wisper
```

For service:
```bash
sudo systemctl start wisper_typer
```

### Hotkey Not Working

**Problem**: Pressing hotkey doesn't trigger recording

**Diagnosis**:
1. Check if wisper is running:
   ```bash
   ps aux | grep wisper
   ```

2. Check logs:
   ```bash
   tail -f ~/.wisper-typer.log
   ```

**Solutions**:
1. Ensure running with sudo/root
2. Try different hotkey in config
3. Check for conflicting hotkeys
4. Restart the service

### No Text Typed (Wayland)

**Problem**: Transcription works but text doesn't appear

**Solution**: Install wl-clipboard:
```bash
sudo apt install wl-clipboard  # Debian/Ubuntu
sudo dnf install wl-clipboard  # Fedora
sudo pacman -S wl-clipboard    # Arch
```

Verify installation:
```bash
which wl-copy
```

### No Text Typed (X11)

**Problem**: Text not being typed on X11

**Solutions**:
1. Ensure running as root
2. Check keyboard module is loaded
3. Verify uinput permissions

### Microphone Not Detected

**Problem**: No audio input / microphone errors

**Diagnosis**:
```bash
# List audio devices
arecord -l

# Test recording
arecord -d 5 test.wav
aplay test.wav
```

**Solutions**:
1. Select correct microphone in system settings
2. Ensure microphone is not muted
3. Check microphone permissions
4. Try different audio device in config

## API Issues

### Invalid API Key

**Problem**: `401 Unauthorized` or API key errors

**Solution**:
1. Verify API key in `~/.wisper-typer`:
   ```bash
   cat ~/.wisper-typer | grep GROQ_API_KEY
   ```

2. Get new key from [console.groq.com](https://console.groq.com)

3. Update config:
   ```bash
   nano ~/.wisper-typer
   # Set: GROQ_API_KEY=gsk_your_new_key
   ```

4. Restart service:
   ```bash
   sudo systemctl restart wisper_typer
   ```

### Rate Limit Exceeded

**Problem**: API returns rate limit error

**Solutions**:
1. Wait before trying again
2. Check your Groq quota
3. Upgrade Groq plan if needed
4. Use shorter recordings

### Network Errors

**Problem**: Connection timeout or network errors

**Solutions**:
1. Check internet connection
2. Verify DNS resolution:
   ```bash
   ping api.groq.com
   ```
3. Check firewall settings
4. Try with VPN if blocked

## Service Issues

### Service Won't Start

**Problem**: `systemctl start wisper_typer` fails

**Diagnosis**:
```bash
systemctl status wisper_typer
journalctl -u wisper_typer -n 50
```

**Solutions**:
1. Check service file path:
   ```bash
   which wisper
   ```
   Update ExecStart in `/etc/systemd/system/wisper_typer.service`

2. Reload systemd:
   ```bash
   sudo systemctl daemon-reload
   ```

3. Check configuration file exists:
   ```bash
   ls -la ~/.wisper-typer
   ```

### Service Keeps Restarting

**Problem**: Service continuously restarts

**Solutions**:
1. View detailed logs:
   ```bash
   journalctl -u wisper_typer -f
   ```

2. Test manual run:
   ```bash
   sudo wisper
   ```

3. Check for configuration errors

4. Verify API key is valid

## Performance Issues

### Slow Transcription

**Problem**: Takes too long to transcribe

**Solutions**:
1. Check internet speed
2. Use shorter recordings
3. Verify using turbo model in config:
   ```bash
   MODEL=whisper-large-v3-turbo
   ```

### High CPU Usage

**Problem**: wisper using too much CPU

**Solutions**:
1. Check for multiple instances:
   ```bash
   ps aux | grep wisper
   ```

2. Kill duplicates:
   ```bash
   sudo pkill -f wisper
   sudo systemctl start wisper_typer
   ```

## Accuracy Issues

### Poor Transcription Quality

**Problem**: Incorrect transcriptions

**Solutions**:
1. Speak clearly and slowly
2. Reduce background noise
3. Use better microphone
4. Increase sample rate in config
5. Try different Whisper model

### Wrong Language

**Problem**: Transcribes in wrong language

**Solution**: Whisper auto-detects language. For consistent results:
1. Speak clearly in target language
2. Configure language if supported in future versions

## Logging Issues

### No Logs Appearing

**Problem**: Log file empty or not created

**Solutions**:
1. Check log file path:
   ```bash
   ls -la ~/.wisper-typer.log
   ```

2. Check permissions:
   ```bash
   chmod 644 ~/.wisper-typer.log
   ```

3. Set DEBUG level in config:
   ```bash
   LOG_LEVEL=DEBUG
   ```

### Too Many Logs

**Problem**: Log file too large

**Solutions**:
1. Rotate logs:
   ```bash
   mv ~/.wisper-typer.log ~/.wisper-typer.log.old
   ```

2. Change log level:
   ```bash
   LOG_LEVEL=WARNING
   ```

## Getting Help

If you're still experiencing issues:

1. **Check logs**:
   ```bash
   tail -f ~/.wisper-typer.log
   journalctl -u wisper_typer -f
   ```

2. **Search existing issues**: [GitHub Issues](https://github.com/riturajprofile/wisper_typer/issues)

3. **Create new issue**: Include:
   - OS and version
   - Python version
   - Error messages
   - Log excerpts
   - Steps to reproduce

4. **Community support**: Check wiki discussions

## Useful Commands

```bash
# Check everything
systemctl status wisper_typer
tail -n 50 ~/.wisper-typer.log
which wisper
python3 --version
arecord -l

# Full restart
sudo systemctl stop wisper_typer
sudo pkill -f wisper
sudo systemctl start wisper_typer

# Reset config
rm ~/.wisper-typer
wisper  # Regenerates default config
```
