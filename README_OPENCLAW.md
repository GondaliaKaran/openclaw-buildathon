# OpenClaw Skill: Adaptive Vendor Evaluation

An intelligent vendor evaluation system that runs as OpenClaw skills.

## Architecture for OpenClaw

This project provides OpenClaw skills for adaptive vendor evaluation:

```
OpenClaw Platform (Docker)
├── Gateway: Telegram
├── AI: OpenAI (gpt-4o)
└── Skills:
    ├── vendor_evaluation_main.py    (Main orchestrator skill)
    ├── candidate_identifier.py       (Find candidates)
    ├── vendor_researcher.py          (Research vendors)
    ├── criteria_adjuster.py          (Dynamic weighting)
    └── recommendation_generator.py   (Final recommendation)
```

## OpenClaw Integration

### Skills Directory Structure

```
openclaw-skills/
├── vendor-evaluation/
│   ├── skill.json                   # Skill manifest
│   ├── main.py                      # Entry point
│   ├── soul.md                      # Agent personality
│   └── agents/
│       ├── candidate_identifier.py
│       ├── researcher.py
│       ├── weight_adjuster.py
│       └── synthesizer.py
```

### How It Works

1. **User sends message via Telegram** → OpenClaw Gateway
2. **OpenClaw routes to skill** → `vendor_evaluation_main.py`
3. **Skill orchestrates evaluation** → Uses other sub-skills
4. **Results sent back** → Through OpenClaw Gateway → Telegram

## Installation on OpenClaw

### 1. SSH to VPS
```bash
ssh root@<your-vps-ip>
```

### 2. Navigate to OpenClaw skills directory
```bash
cd /opt/openclaw/skills  # or wherever OpenClaw skills are
# OR
cd ~/openclaw-skills
```

### 3. Clone/upload this project
```bash
# If using git
git clone <your-repo> vendor-evaluation

# Or upload via scp
scp -r openclaw-buildathon root@<vps-ip>:/opt/openclaw/skills/vendor-evaluation
```

### 4. Verify OpenClaw sees the skill
```bash
docker exec -it openclaw curl http://localhost:PORT/api/skills
# Should list "vendor_evaluation"
```

### 5. Test via Telegram
Send to your bot:
```
@yourbot evaluate payment gateway for fintech startup
```

## OpenClaw Configuration

### Environment Variables (Already set during OpenClaw setup)
- `OPENAI_API_KEY` - Set during OpenClaw onboarding
- `OPENCLAW_GATEWAY_TOKEN` - For Telegram integration
- `OPENCLAW_GATEWAY=telegram` - Gateway type

### Skill Registration

The skill auto-registers when OpenClaw starts if:
1. Placed in correct directory
2. Has valid `skill.json` manifest
3. OpenClaw is restarted: `docker restart openclaw`

## Usage

### Via Telegram (through OpenClaw Gateway)

**Start evaluation:**
```
evaluate payment gateway
Tech: Python, AWS
Domain: fintech
Region: India
```

**Quick evaluation:**
```
@bot find best CRM for startup with Salesforce integration
```

### Via OpenClaw WebChat

Navigate to `http://<vps-ip>:<port>` and type:
```
I need to evaluate payment gateways for my fintech startup in India
```

## Commands Recognized

- `evaluate [category]` - Start vendor evaluation
- `compare [vendor1] vs [vendor2]` - Compare specific vendors
- `research [vendor]` - Deep dive on one vendor
- `help evaluation` - Show evaluation help

## Skill Capabilities

✅ Autonomous candidate identification
✅ Multi-dimensional research (10+ criteria)
✅ Dynamic weight adjustment based on discoveries
✅ Context-aware recommendations
✅ Hidden risk detection
✅ Evidence-based reasoning

## Development

### Local Testing (before deploying to OpenClaw)
```bash
python main.py --local-test
```

### Logs
```bash
# On VPS
docker logs openclaw -f | grep "vendor_evaluation"
```

### Updates
```bash
# Update skill code
scp -r agents/ root@<vps-ip>:/opt/openclaw/skills/vendor-evaluation/

# Restart OpenClaw to reload
ssh root@<vps-ip>
docker restart openclaw
```

## Troubleshooting

### Skill not loading
```bash
docker exec -it openclaw ls /opt/openclaw/skills/vendor-evaluation
# Verify files are there

docker logs openclaw | grep -i error
# Check for errors
```

### Telegram not responding
```bash
docker exec -it openclaw env | grep GATEWAY
# Verify gateway configured

# Test gateway
docker exec -it openclaw curl http://localhost:PORT/gateway/status
```

### OpenAI errors
```bash
docker exec -it openclaw env | grep OPENAI
# Verify API key set
```

## Performance

- Evaluation time: ~3-4 minutes
- OpenAI cost per evaluation: ~$0.10-0.30 (gpt-4o)
- Concurrent evaluations: Limited by OpenAI rate limits

## Architecture Notes

### Why Skills Instead of Standalone?

**Benefits of running in OpenClaw:**
- ✅ OpenClaw handles Telegram gateway (no custom bot code)
- ✅ Shared OpenAI API management
- ✅ Built-in message routing
- ✅ Unified logging and monitoring
- ✅ WebChat interface included
- ✅ Multi-channel support (Telegram, WhatsApp, etc.)

**Trade-offs:**
- Must follow OpenClaw skill API
- Shared resources with other skills
- OpenClaw restart needed for updates

## Next Steps

1. ✅ OpenClaw installed with Telegram + OpenAI
2. ⏳ Upload skill to VPS
3. ⏳ Register skill with OpenClaw
4. ⏳ Test via Telegram
5. ⏳ Monitor and optimize

See `OPENCLAW_DEPLOYMENT.md` for detailed deployment steps.
