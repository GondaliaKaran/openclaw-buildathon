# OpenClaw Deployment Guide - Vendor Evaluation Skill

## Prerequisites

✅ Hostinger VPS with OpenClaw installed (Docker)  
✅ OpenClaw configured with Telegram gateway  
✅ OpenAI API key configured in OpenClaw  
✅ SSH access to VPS  

---

## Step 1: Verify OpenClaw is Running

```bash
# SSH to your VPS
ssh root@<your-vps-ip>

# Check OpenClaw container
docker ps | grep openclaw

# Should show: openclaw container running
```

**Expected output:**
```
CONTAINER ID   IMAGE              STATUS         PORTS
abc123def456   openclaw:latest   Up 2 hours     0.0.0.0:8080->8080/tcp
```

---

## Step 2: Check OpenClaw Dashboard

Visit: `http://<your-vps-ip>:<port>`

**Verify:**
- ✅ Dashboard loads
- ✅ WebChat responds to "Hello"
- ✅ Telegram gateway connected
- ✅ OpenAI API key configured

---

## Step 3: Find OpenClaw Skills Directory

```bash
# Common locations:
docker exec -it openclaw ls /app/skills
# OR
docker exec -it openclaw ls /opt/openclaw/skills
# OR
docker exec -it openclaw env | grep SKILLS

# Find it:
docker exec -it openclaw find / -type d -name "skills" 2>/dev/null
```

**Note the path** (e.g., `/app/skills` or `/opt/openclaw/skills`)

---

## Step 4: Upload Skill to VPS

### Option A: Using Git (Recommended)

```bash
# On your local machine
cd openclaw-buildathon
git add .
git commit -m "Vendor evaluation skill for OpenClaw"
git push origin main

# On VPS
ssh root@<your-vps-ip>
cd /tmp
git clone <your-repo-url> vendor-evaluation-skill
```

### Option B: Using SCP

```bash
# On your local machine
cd openclaw-buildathon

# Upload entire directory
scp -r . root@<your-vps-ip>:/tmp/vendor-evaluation-skill/
```

---

## Step 5: Install Skill into OpenClaw

```bash
# On VPS
cd /tmp/vendor-evaluation-skill

# Copy to OpenClaw skills directory
docker cp . openclaw:/app/skills/vendor-evaluation/

# Verify files copied
docker exec -it openclaw ls -la /app/skills/vendor-evaluation/
```

**Should see:**
```
skill.json
skill_handler.py
orchestrator.py
SOUL.md
agents/
integrations/
utils/
config.py
requirements.txt
```

---

## Step 6: Install Python Dependencies

```bash
# Enter OpenClaw container
docker exec -it openclaw bash

# Navigate to skill directory
cd /app/skills/vendor-evaluation

# Install dependencies
pip install -r requirements.txt

# Exit container
exit
```

---

## Step 7: Register Skill with OpenClaw

### Method 1: Auto-register (Restart OpenClaw)

```bash
# Restart OpenClaw to auto-discover skills
docker restart openclaw

# Wait 30 seconds
sleep 30

# Check logs
docker logs openclaw -f
```

**Look for:**
```
✅ Loading skill: vendor-evaluation
✅ Vendor Evaluation Skill Ready
```

### Method 2: Manual registration (if OpenClaw has API)

```bash
# Check if OpenClaw has skill registration endpoint
curl http://localhost:8080/api/skills/register -X POST \
  -H "Content-Type: application/json" \
  -d '{"skill_path": "/app/skills/vendor-evaluation"}'
```

---

## Step 8: Verify Skill is Loaded

```bash
# Check OpenClaw logs
docker logs openclaw | grep -i "vendor"

# Should see:
# ✅ Vendor Evaluation Skill Ready

# List registered skills
docker exec -it openclaw curl http://localhost:8080/api/skills
# Should include "vendor_evaluation"
```

---

## Step 9: Test via Telegram

Open Telegram and message your bot:

### Test 1: Help
```
help evaluation
```

**Expected:** Help message about vendor evaluation

### Test 2: Simple Query
```
evaluate payment gateways
```

**Expected:** Skill responds with clarifying questions or starts evaluation

### Test 3: Full Request
```
evaluate payment gateways for fintech startup in India with Python and AWS
```

**Expected:** 
```
🚀 Starting Evaluation

Category: payment gateway
Tech Stack: Python, AWS
Domain: fintech

⏳ This will take ~3-4 minutes. Analyzing vendors...
```

Then after ~3-4 minutes:
```
✅ Evaluation Complete!

Candidates Evaluated: Stripe, Razorpay, Cashfree, PayPal

🔍 Key Discoveries:
1. Razorpay has native RBI compliance
   Impact: Increased Compliance weight from 20% to 30%

🎯 Recommended: Razorpay

Why: Native RBI compliance critical for Indian fintech...
```

---

## Step 10: Test via WebChat

Navigate to: `http://<your-vps-ip>:<port>`

Type in WebChat:
```
Find best CRM for startup
```

Same evaluation flow should work.

---

## Troubleshooting

### Skill Not Loading

**Check files:**
```bash
docker exec -it openclaw ls /app/skills/vendor-evaluation/skill.json
# Should exist
```

**Check permissions:**
```bash
docker exec -it openclaw ls -la /app/skills/vendor-evaluation/
# All files should be readable
```

**Check OpenClaw logs:**
```bash
docker logs openclaw | grep -i error
```

### Import Errors

**Missing dependencies:**
```bash
docker exec -it openclaw bash
cd /app/skills/vendor-evaluation
pip install -r requirements.txt
exit
docker restart openclaw
```

**Python path issues:**
```bash
# Check if skill_handler.py has correct imports
docker exec -it openclaw cat /app/skills/vendor-evaluation/skill_handler.py | grep import
```

### OpenAI API Errors

**Verify API key:**
```bash
docker exec -it openclaw env | grep OPENAI_API_KEY
# Should show: OPENAI_API_KEY=sk-...
```

**If missing:**
```bash
# Stop OpenClaw
docker stop openclaw

# Add environment variable
docker run -d \
  --name openclaw \
  -e OPENAI_API_KEY=sk-your-key-here \
  -p 8080:8080 \
  openclaw:latest

# Or update via Hostinger hPanel:
# Docker Manager → openclaw → Environment Variables
```

### Telegram Not Responding

**Check gateway:**
```bash
docker exec -it openclaw env | grep GATEWAY
# Should show: OPENCLAW_GATEWAY=telegram
```

**Check bot token:**
```bash
docker exec -it openclaw env | grep BOT_TOKEN
```

**Test webhook:**
```bash
curl -X GET "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

### Skill Responds but Evaluation Fails

**Check logs in real-time:**
```bash
docker logs openclaw -f | grep "vendor_evaluation"
```

**Common issues:**
- Rate limiting: Wait 60 seconds between tests
- Timeout: Increase timeout in skill.json
- Memory: Check VPS has enough RAM (`free -h`)

---

## Updating the Skill

### After code changes:

```bash
# On local machine
git push

# On VPS
cd /tmp/vendor-evaluation-skill
git pull

# Update in OpenClaw
docker cp . openclaw:/app/skills/vendor-evaluation/

# Restart
docker restart openclaw
```

---

## Monitoring

### View Logs
```bash
# All logs
docker logs openclaw -f

# Skill-specific logs
docker logs openclaw -f | grep "vendor_evaluation"

# Errors only
docker logs openclaw 2>&1 | grep -i error
```

### Performance
```bash
# Check container stats
docker stats openclaw

# Check OpenAI usage
# Visit: https://platform.openai.com/usage
```

---

## Configuration

### Adjust Skill Behavior

Edit `skill.json` configuration:
```bash
docker exec -it openclaw nano /app/skills/vendor-evaluation/skill.json
```

**Available settings:**
```json
{
  "configuration": {
    "max_candidates": 5,              // Max vendors to compare
    "research_depth": "comprehensive", // or "quick"
    "enable_dynamic_weighting": true,  // Adaptive criteria
    "enable_hidden_risk_detection": true,
    "evaluation_timeout": 300          // 5 minutes
  }
}
```

After changes:
```bash
docker restart openclaw
```

---

## Uninstalling

```bash
# Remove skill directory
docker exec -it openclaw rm -rf /app/skills/vendor-evaluation

# Restart OpenClaw
docker restart openclaw
```

---

## Success Checklist

✅ OpenClaw running on VPS  
✅ Skill files uploaded  
✅ Dependencies installed  
✅ Skill appears in logs: "Vendor Evaluation Skill Ready"  
✅ Telegram bot responds to "help evaluation"  
✅ Test evaluation completes successfully  
✅ WebChat works  
✅ Logs show no errors  

---

## Next Steps

1. **Test thoroughly** with various evaluation requests
2. **Monitor costs** at platform.openai.com/usage
3. **Customize SOUL.md** for different personality
4. **Tune configuration** in skill.json
5. **Add more data sources** in researcher.py

---

## Support

**OpenClaw issues:**
- Check OpenClaw documentation
- Review Docker logs: `docker logs openclaw`

**Skill issues:**
- Check skill logs: `docker logs openclaw | grep vendor_evaluation`
- Review this guide's troubleshooting section

**OpenAI issues:**
- Verify API key
- Check usage/credits: platform.openai.com

---

## Quick Reference

```bash
# Status
docker ps | grep openclaw

# Logs
docker logs openclaw -f

# Restart
docker restart openclaw

# Enter container
docker exec -it openclaw bash

# Update skill
docker cp . openclaw:/app/skills/vendor-evaluation/
docker restart openclaw

# Test
# Send "evaluate payment gateways" via Telegram
```

---

You're ready! 🚀

Send "**evaluate payment gateways for startup**" to your Telegram bot to test!
