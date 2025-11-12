# Slack Integration Setup Guide

This guide will help you set up Slack integration for DAST security scan reporting.

## Overview

The Slack integration automatically sends formatted security scan results to your Slack workspace, providing:

- 🔒 **Summary of findings** with severity counts
- 📊 **Detailed vulnerability listings** organized by risk level
- 🎯 **Target URL and scan timestamps**
- 🔗 **Pull Request integration** (when applicable)
- 🎨 **Color-coded messages** based on severity

## Setup Options

You can choose between two methods to integrate with Slack:

### Option 1: Slack Bot Token (Recommended)

**Pros:** More control, richer formatting, supports threads
**Cons:** Requires creating a Slack app

1. **Create a Slack App:**
   - Go to https://api.slack.com/apps
   - Click "Create New App" → "From scratch"
   - Give it a name (e.g., "DAST Security Reporter")
   - Select your workspace

2. **Configure Bot Permissions:**
   - Go to "OAuth & Permissions" in your app settings
   - Add the following Bot Token Scopes:
     - `chat:write` - Send messages
     - `chat:write.public` - Send messages to public channels
     - `files:write` - Upload files (for detailed reports)

3. **Install App to Workspace:**
   - Click "Install to Workspace"
   - Authorize the app
   - Copy the "Bot User OAuth Token" (starts with `xoxb-`)

4. **Add Bot to Channel:**
   - In Slack, go to your target channel (e.g., `#security-alerts`)
   - Type `/invite @YourBotName`

### Option 2: Incoming Webhook (Simpler)

**Pros:** Quick setup, no app creation needed
**Cons:** Less formatting options, no threading

1. **Create Incoming Webhook:**
   - Go to https://api.slack.com/apps
   - Create a new app (or use existing)
   - Go to "Incoming Webhooks"
   - Activate incoming webhooks
   - Click "Add New Webhook to Workspace"
   - Select the channel where you want notifications
   - Copy the webhook URL

## Configuration

### Environment Variables

Set up the following environment variables in your system or CI/CD:

```bash
# Option 1: Bot Token
export SLACK_BOT_TOKEN="xoxb-your-bot-token-here"
export SLACK_CHANNEL="#security-alerts"

# Option 2: Webhook URL
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# Report configuration
export ZAP_REPORT_PATH="report.json"
```

### GitHub Secrets (for CI/CD)

In your GitHub repository, go to Settings → Secrets and variables → Actions, and add:

**For Bot Token method:**
- `SLACK_BOT_TOKEN`: Your bot token (xoxb-...)
- Optionally set `SLACK_CHANNEL` as a repository variable

**For Webhook method:**
- `SLACK_WEBHOOK_URL`: Your webhook URL

## Testing the Integration

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   # Copy and edit the example file
   cp .env.example .env
   # Edit .env with your actual values
   ```

3. **Run the test script:**
   ```bash
   python test_slack_integration.py
   ```

This will:
- Generate sample vulnerability data
- Create a formatted Slack message
- Send a test message to your channel (if credentials are configured)
- Show you the message format

## Message Format

The Slack integration sends messages with the following format:

```
🔒 **DAST Security Scan Results** - PR #123
📊 **Findings:** 🔴 1 High, 🟠 2 Medium, 🟡 1 Low
🎯 **Target:** https://your-app.com
🕐 **Scan Time:** 2025-09-30 14:30:00

**High Risk Vulnerabilities (1):**
• Cross Site Scripting (Reflected)

**Medium Risk Vulnerabilities (2):**
• Open Redirect
• Missing Anti-clickjacking Header

**Low Risk Vulnerabilities (1):**
• X-Content-Type-Options Header Missing
```

## Customization

### Channel Configuration

You can customize which channel receives notifications by:

1. **Environment variable:** Set `SLACK_CHANNEL` to your preferred channel
2. **GitHub variable:** Set repository variable `SLACK_CHANNEL`
3. **Direct configuration:** Modify the `slack_reporter.py` script

### Message Formatting

Edit `slack_reporter.py` to customize:

- **Colors:** Modify `severity_colors` dictionary
- **Emojis:** Change the emoji mappings in `create_summary_message()`
- **Message content:** Customize the message templates
- **Severity thresholds:** Adjust when to send notifications

### Filtering

You can modify the script to:
- Only send notifications for High/Medium severity issues
- Filter specific vulnerability types
- Set minimum vulnerability counts before sending

## Troubleshooting

### Common Issues

1. **"channel_not_found" error:**
   - Make sure the bot is added to the channel
   - Check channel name format (use # prefix)
   - Verify channel exists and is accessible

2. **"not_authed" error:**
   - Check your bot token is correct
   - Verify token permissions include `chat:write`

3. **"No JSON object could be decoded":**
   - Ensure ZAP report file exists and is valid JSON
   - Check the `ZAP_REPORT_PATH` environment variable

4. **Webhook errors:**
   - Verify webhook URL is correct and active
   - Check that the webhook hasn't been disabled

### Debug Mode

To enable verbose logging, modify the script to include debug information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Considerations

- **Store tokens securely:** Never commit tokens to version control
- **Use repository secrets:** Store sensitive values in GitHub Secrets
- **Limit permissions:** Only grant necessary Slack permissions
- **Regular rotation:** Consider rotating bot tokens periodically

## Advanced Features

### Thread Replies

For high-volume channels, you can modify the script to:
- Send summary as main message
- Reply with detailed findings in thread

### File Uploads

For very detailed reports, you can upload the full JSON/HTML report:

```python
# Upload file example
self.client.files_upload(
    channels=self.channel,
    file="report.html",
    title="Detailed DAST Report"
)
```

### Custom Fields

Add custom fields based on your needs:
- Git commit hash
- Build number
- Environment information
- Previous scan comparison

## Integration with Other Tools

The Slack reporter can be extended to work with:
- **Microsoft Teams:** Modify webhook payload format
- **Discord:** Use Discord webhook format
- **Email:** Add SMTP notification option
- **JIRA:** Create tickets for high-severity findings