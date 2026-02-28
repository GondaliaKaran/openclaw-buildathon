# Adaptive Vendor Evaluation Agent - Setup Guide

## Quick Start (5 minutes)

### 1. Get Your API Keys

**OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (starts with `sk-...`)

**Telegram Bot Token:**
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the bot token

### 2. Configure Environment

```bash
cd openclaw-buildathon
cp .env.example .env
nano .env  # or use your preferred editor
```

Add your keys:
```env
OPENAI_API_KEY=sk-your-openai-key-here
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 3. Run Locally

```bash
chmod +x start.sh
./start.sh
```

### 4. Test Your Bot

1. Open Telegram
2. Search for your bot (the name you gave to BotFather)
3. Send `/start`
4. Send `/example` to see a sample evaluation
5. Send `/evaluate` to run your own evaluation

---

## Deployment to Hostinger VPS

### Prerequisites

- Hostinger VPS running Ubuntu/Debian
- SSH access to your VPS
- Domain/subdomain (optional)

### Deployment Steps

#### 1. Connect to Your VPS

```bash
ssh user@your-vps-ip
```

#### 2. Clone Repository

```bash
cd ~
git clone <your-repo-url>
cd openclaw-buildathon
```

Or if you're uploading files directly:
```bash
scp -r openclaw-buildathon/* user@your-vps-ip:~/openclaw-buildathon/
```

#### 3. Run Deployment Script

```bash
cd openclaw-buildathon
chmod +x deploy.sh
./deploy.sh
```

The script will:
- Install Python and dependencies
- Create virtual environment
- Setup systemd service
- Start the agent

#### 4. Configure Environment

```bash
nano .env
```

Add your API keys, then restart:
```bash
sudo systemctl restart vendor-agent
```

#### 5. Verify Deployment

```bash
# Check service status
sudo systemctl status vendor-agent

# View logs
sudo journalctl -u vendor-agent -f

# Test bot
# Send /start to your Telegram bot
```

---

## Service Management

### View Logs
```bash
sudo journalctl -u vendor-agent -f
```

### Stop Service
```bash
sudo systemctl stop vendor-agent
```

### Start Service
```bash
sudo systemctl start vendor-agent
```

### Restart Service
```bash
sudo systemctl restart vendor-agent
```

### Disable Auto-start
```bash
sudo systemctl disable vendor-agent
```

---

## Troubleshooting

### Bot Not Responding

1. Check service is running:
   ```bash
   sudo systemctl status vendor-agent
   ```

2. Check logs for errors:
   ```bash
   sudo journalctl -u vendor-agent -n 50
   ```

3. Verify API keys in `.env`

4. Test Telegram token:
   ```bash
   curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe
   ```

### OpenAI API Errors

1. Verify API key is valid
2. Check you have credits: https://platform.openai.com/usage
3. Ensure model (gpt-4-turbo-preview) is accessible

### Memory Issues on VPS

If your VPS has limited RAM:

1. Edit `.env` and use a smaller model:
   ```env
   OPENAI_MODEL=gpt-3.5-turbo
   ```

2. Reduce concurrent operations in code

---

## Updating the Agent

### On VPS

```bash
cd ~/openclaw-buildathon
git pull  # or upload new files
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart vendor-agent
```

---

## Security Best Practices

1. **Never commit API keys to git**
   - `.env` is in `.gitignore`
   - Keep keys secure

2. **Restrict SSH access**
   ```bash
   # Use SSH keys, disable password auth
   sudo nano /etc/ssh/sshd_config
   # Set: PasswordAuthentication no
   ```

3. **Setup firewall**
   ```bash
   sudo ufw enable
   sudo ufw allow ssh
   sudo ufw allow 443  # if using webhooks
   ```

4. **Keep system updated**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

---

## Advanced Configuration

### Using Webhook Instead of Polling

For better performance on VPS, use webhooks:

1. Get SSL certificate (Let's Encrypt):
   ```bash
   sudo apt install certbot
   sudo certbot certonly --standalone -d yourdomain.com
   ```

2. Update bot code to use webhooks (see Telegram bot docs)

### Monitoring

Setup monitoring with:
- **Logs**: `journalctl`
- **Uptime**: `uptimerobot.com` or similar
- **Alerts**: Configure systemd to email on failure

---

## Support

- **Issues**: Check logs first
- **Documentation**: See README.md for architecture details
- **Updates**: Pull latest from repository

---

## Performance Optimization

### Caching Research Results

To avoid re-researching vendors:
1. Results are logged to `agent.log`
2. Can add Redis/file-based cache

### Rate Limiting

OpenAI API has rate limits:
- Implement request queuing
- Add delays between calls
- Monitor usage at platform.openai.com

---

## Cost Estimate

**Per Evaluation:**
- OpenAI API: ~$0.10-0.30 (GPT-4)
- VPS: $5-10/month (Hostinger)

**Optimization:**
- Use GPT-3.5-turbo: ~$0.02-0.05 per evaluation
- Cache research results
- Implement smart query batching

---

## Next Steps

1. ✅ Deploy to VPS
2. ✅ Test with sample evaluations
3. 📊 Monitor performance and costs
4. 🎯 Tune evaluation criteria for your domain
5. 🚀 Share bot with team

Happy evaluating! 🎉
