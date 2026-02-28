# 🚀 Quick Start Guide - 5 Minutes to Running Agent

## Prerequisites
- Python 3.10+
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Telegram bot token ([create with @BotFather](https://t.me/botfather))

## Step 1: Get Your Keys (2 minutes)

### OpenAI API Key
1. Visit https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-...`)

### Telegram Bot Token
1. Open Telegram, search for `@BotFather`
2. Send `/newbot`
3. Choose a name and username for your bot
4. Copy the token (looks like `1234567890:ABCdef...`)

## Step 2: Configure (1 minute)

```bash
cd openclaw-buildathon

# Copy environment template
cp .env.example .env

# Edit with your keys
nano .env  # or use your preferred editor
```

Add your keys:
```env
OPENAI_API_KEY=sk-your-key-here
TELEGRAM_BOT_TOKEN=1234567890:your-token-here
```

Save and exit (Ctrl+X, then Y, then Enter in nano)

## Step 3: Install & Run (2 minutes)

### Option A: Quick Start Script (Recommended)
```bash
chmod +x start.sh
./start.sh
```

### Option B: Manual
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

## Step 4: Test Your Bot

1. Open Telegram
2. Search for your bot (the name you gave it)
3. Send `/start` - you should get a welcome message
4. Send `/example` - see a sample evaluation
5. Send `/evaluate` - run your own evaluation!

---

## Example Evaluation

Try this in your bot:

```
/evaluate

Category: Payment Gateway
Tech Stack: Python, AWS
Domain: E-commerce  
Region: US
Scale: Startup
Priorities: Easy integration, low fees
Compliance: PCI-DSS
```

The agent will:
- Find 3-5 relevant payment gateways
- Research each deeply
- Adaptively adjust criteria based on findings
- Recommend the best fit with reasoning

Takes ~3-4 minutes.

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Invalid token" error
- Double-check your Telegram bot token in `.env`
- Make sure there are no spaces or quotes around it

### "OpenAI API error"
- Verify your API key in `.env`
- Check you have credits at https://platform.openai.com/usage

### Bot doesn't respond
- Check the terminal for errors
- Make sure `main.py` is running
- Verify internet connection

---

## Commands

- `/start` - Welcome message
- `/evaluate` - Start new evaluation
- `/example` - See example evaluation
- `/help` - Get help
- `/cancel` - Cancel current evaluation

---

## What's Next?

### Deploy to VPS
See [SETUP.md](SETUP.md) for Hostinger VPS deployment

### Customize
- Edit [SOUL.md](SOUL.md) to change agent personality
- Modify weights in `agents/weight_adjuster.py`
- Add more research sources in `agents/researcher.py`

### Monitor
```bash
# View logs
tail -f agent.log

# On VPS
sudo journalctl -u vendor-agent -f
```

---

## Cost Estimate

**Per evaluation:**
- OpenAI API (GPT-4): ~$0.10-0.30
- OpenAI API (GPT-3.5): ~$0.02-0.05

**To use cheaper model:**
Edit `.env`:
```env
OPENAI_MODEL=gpt-3.5-turbo
```

---

## Need Help?

1. Check logs: `tail -f agent.log`
2. Read [SETUP.md](SETUP.md) for detailed guide
3. See [README.md](README.md) for architecture
4. Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for overview

---

## Success!

If you see this in terminal:
```
🚀 Agent is running!
Send /start to your Telegram bot to begin
```

You're all set! 🎉

Go try `/evaluate` in your Telegram bot!
