# API Setup Guide

Learn how to get and configure your Groq API key for Wisper Typer.

## What is Groq?

Groq provides ultra-fast AI inference, including Whisper models for speech-to-text transcription. Wisper Typer uses Groq's API for lightning-fast voice transcription.

## Getting Your API Key

### Step 1: Create Groq Account

1. Visit [console.groq.com](https://console.groq.com)
2. Click "Sign Up" or "Get Started"
3. Sign up with:
   - Email and password, or
   - Google account, or
   - GitHub account

### Step 2: Access API Keys

1. Once logged in, navigate to **API Keys** section
2. Click "Create API Key"
3. Give it a name (e.g., "wisper-typer")
4. Copy the generated key (starts with `gsk_`)

**Important**: Save the key immediately! You won't be able to see it again.

### Step 3: Configure Wisper Typer

Add the API key to your configuration:

```bash
# Edit config file
nano ~/.wisper-typer

# Add this line (replace with your actual key)
GROQ_API_KEY=gsk_your_actual_api_key_here
```

Save and exit (`Ctrl+X`, then `Y`, then `Enter`).

### Step 4: Verify Setup

Restart Wisper Typer:
```bash
sudo systemctl restart wisper_typer
```

Test by pressing your hotkey and speaking!

## API Key Security

### Best Practices

1. **Never commit to Git**: Add `~/.wisper-typer` to `.gitignore`
2. **Don't share**: Keep your API key private
3. **Use environment variables**: For scripts:
   ```bash
   export GROQ_API_KEY="gsk_your_key"
   ```
4. **Rotate regularly**: Create new keys periodically
5. **Delete unused keys**: Remove old keys from Groq console

### If Your Key is Compromised

1. Go to [console.groq.com](https://console.groq.com)
2. Navigate to API Keys
3. Delete the compromised key
4. Create a new key
5. Update `~/.wisper-typer` with new key
6. Restart Wisper Typer

## Groq Pricing & Limits

### Free Tier

Groq offers a generous free tier:
- **Rate Limits**: Check [console.groq.com](https://console.groq.com) for current limits
- **Monthly Quota**: Sufficient for personal use
- **No Credit Card**: Free tier doesn't require payment method

### Paid Plans

For heavy usage:
- Higher rate limits
- More monthly quota
- Priority support

Check [Groq's pricing page](https://groq.com/pricing) for details.

### Monitoring Usage

1. Log into [console.groq.com](https://console.groq.com)
2. View usage dashboard
3. Check API call statistics
4. Monitor quota remaining

## API Models

Wisper Typer supports Groq's Whisper models:

### whisper-large-v3-turbo (Default)
- **Speed**: Fastest
- **Accuracy**: Very high
- **Recommended**: Yes
- **Use case**: Real-time dictation

### whisper-large-v3
- **Speed**: Slower
- **Accuracy**: Slightly higher
- **Recommended**: For maximum accuracy
- **Use case**: Transcribing difficult audio

To change model, edit `~/.wisper-typer`:
```bash
MODEL=whisper-large-v3-turbo
```

## Environment Variables

Alternative to config file:

```bash
# Set in shell
export GROQ_API_KEY="gsk_your_key"
export MODEL="whisper-large-v3-turbo"

# Run wisper
sudo -E wisper
```

For systemd service, add to service file:
```ini
Environment="GROQ_API_KEY=gsk_your_key"
```

## Troubleshooting API Issues

### Authentication Errors

**Error**: `401 Unauthorized`

**Solutions**:
1. Verify key in config:
   ```bash
   cat ~/.wisper-typer | grep GROQ_API_KEY
   ```
2. Check key is valid (no typos)
3. Ensure key starts with `gsk_`
4. Try creating new key

### Rate Limit Errors

**Error**: `429 Too Many Requests`

**Solutions**:
1. Wait a few minutes
2. Check usage in Groq console
3. Upgrade to paid plan if needed
4. Use shorter audio clips

### Network Errors

**Error**: Connection timeout

**Solutions**:
1. Check internet connection
2. Verify DNS:
   ```bash
   ping api.groq.com
   ```
3. Check firewall settings
4. Try different network

## Testing Your API Key

Test manually with curl:

```bash
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer gsk_your_key_here"
```

Should return list of available models.

## Multiple API Keys

For different use cases:

**Work:**
```bash
# ~/.wisper-typer-work
GROQ_API_KEY=gsk_work_key
```

**Personal:**
```bash
# ~/.wisper-typer-personal
GROQ_API_KEY=gsk_personal_key
```

Point to different config:
```bash
CONFIG_FILE=~/.wisper-typer-work wisper
```

## Next Steps

- [Configure Wisper Typer](Configuration.md)
- [Set up systemd service](Systemd-Service.md)
- [Learn usage tips](Usage-Guide.md)

## Useful Links

- [Groq Console](https://console.groq.com)
- [Groq Documentation](https://console.groq.com/docs)
- [Groq Pricing](https://groq.com/pricing)
- [Groq Models](https://console.groq.com/docs/models)
