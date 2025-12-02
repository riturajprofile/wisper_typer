# Systemd Service Setup

Configure Wisper Typer to start automatically on system boot using systemd.

## Automatic Installation (Recommended)

The easiest way to set up the service:

```bash
sudo wisper --install-service
```

This command:
1. Locates the wisper installation
2. Creates the service file
3. Installs it to `/etc/systemd/system/`
4. Enables the service to start on boot
5. Starts the service immediately

## Manual Installation

If automatic installation doesn't work, you can set it up manually.

### Step 1: Locate Service File

Find where wisper_typer is installed:
```bash
pip show wisper_typer | grep Location
```

### Step 2: Create Service File

Create `/etc/systemd/system/wisper_typer.service`:

```ini
[Unit]
Description=Wisper Typer - AI Voice Dictation Service
After=network.target sound.target

[Service]
Type=simple
ExecStart=/usr/local/bin/wisper
Restart=always
RestartSec=3
User=root
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Important**: Adjust `/usr/local/bin/wisper` to match your installation path.

### Step 3: Find Wisper Path

```bash
which wisper
```

Update `ExecStart` in the service file with the correct path.

### Step 4: Enable and Start

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable wisper_typer

# Start service now
sudo systemctl start wisper_typer
```

## Managing the Service

### Check Status
```bash
systemctl status wisper_typer
```

### Start Service
```bash
sudo systemctl start wisper_typer
```

### Stop Service
```bash
sudo systemctl stop wisper_typer
```

### Restart Service
```bash
sudo systemctl restart wisper_typer
```

### Disable Autostart
```bash
sudo systemctl disable wisper_typer
```

### Re-enable Autostart
```bash
sudo systemctl enable wisper_typer
```

## Viewing Logs

### Real-time Service Logs
```bash
journalctl -u wisper_typer -f
```

### Recent Logs
```bash
journalctl -u wisper_typer -n 50
```

### Logs Since Boot
```bash
journalctl -u wisper_typer -b
```

### Application Log File
```bash
tail -f ~/.wisper-typer.log
```

## Troubleshooting Service

### Service Won't Start

1. **Check service status:**
   ```bash
   systemctl status wisper_typer
   ```

2. **Check for errors:**
   ```bash
   journalctl -u wisper_typer -n 20
   ```

3. **Verify wisper path:**
   ```bash
   which wisper
   ```
   Update service file if path is different.

4. **Check permissions:**
   Service must run as root for global hotkey access.

### Service Crashes

If the service keeps restarting:

1. **View crash logs:**
   ```bash
   journalctl -u wisper_typer -n 100
   ```

2. **Check configuration:**
   Ensure `~/.wisper-typer` has valid API key

3. **Test manual run:**
   ```bash
   sudo wisper
   ```
   See if errors appear

### Configuration Not Loading

If changes to `~/.wisper-typer` aren't applied:

```bash
sudo systemctl restart wisper_typer
```

## Service File Customization

### Change User

To run as a specific user (not recommended, needs root for hotkeys):
```ini
User=yourusername
```

### Environment Variables

Add environment variables:
```ini
Environment="GROQ_API_KEY=gsk_your_key"
Environment="HOTKEY=ctrl+alt"
```

### Restart Policy

Modify restart behavior:
```ini
Restart=on-failure
RestartSec=5
```

## Uninstalling Service

```bash
# Stop service
sudo systemctl stop wisper_typer

# Disable service
sudo systemctl disable wisper_typer

# Remove service file
sudo rm /etc/systemd/system/wisper_typer.service

# Reload systemd
sudo systemctl daemon-reload
```

## Next Steps

- [Configure Wisper Typer](Configuration.md)
- [Usage tips](Usage-Guide.md)
- [Troubleshooting](Troubleshooting.md)
