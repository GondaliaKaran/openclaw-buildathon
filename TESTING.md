# Testing Guide

## Pre-Deployment Testing

Before deploying to your VPS, test locally to ensure everything works.

---

## 1. Installation Test

### Verify Python Version
```bash
python3 --version
# Should be 3.10 or higher
```

### Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Expected:** No errors, all packages installed successfully.

---

## 2. Configuration Test

### Create .env File
```bash
cp .env.example .env
```

### Add Your Keys
Edit `.env`:
```env
OPENAI_API_KEY=sk-your-actual-key
TELEGRAM_BOT_TOKEN=your-actual-token
```

### Test OpenAI Connection
```bash
python3 << 'EOF'
from integrations.openai_client import OpenAIClient
import asyncio

async def test():
    client = OpenAIClient()
    response = await client.chat_completion(
        messages=[{"role": "user", "content": "Say hello"}],
        temperature=0.7
    )
    print(f"✅ OpenAI API working: {response[:50]}")

asyncio.run(test())
EOF
```

**Expected:** "✅ OpenAI API working: Hello! ..."

### Test Telegram Bot Token
```bash
# Replace YOUR_TOKEN with your actual token
curl "https://api.telegram.org/botYOUR_TOKEN/getMe"
```

**Expected:** JSON response with your bot info.

---

## 3. Component Tests

### Test Candidate Identifier
```bash
python3 << 'EOF'
from agents.candidate_identifier import CandidateIdentifier
from integrations.clawhub import ClawHubClient
from integrations.openai_client import OpenAIClient
import asyncio

async def test():
    clawhub = ClawHubClient()
    openai = OpenAIClient()
    identifier = CandidateIdentifier(clawhub, openai)
    
    context = {
        "tech_stack": ["Python", "AWS"],
        "domain": "fintech",
        "region": "India"
    }
    
    candidates = await identifier.identify_candidates("payment gateway", context)
    print(f"✅ Found {len(candidates)} candidates:")
    for c in candidates:
        print(f"   - {c.name}")

asyncio.run(test())
EOF
```

**Expected:** List of 3-5 payment gateway vendors.

### Test Researcher
```bash
python3 << 'EOF'
from agents.researcher import MultiCriteriaResearcher
from agents.candidate_identifier import Candidate
from integrations.clawhub import ClawHubClient
from integrations.openai_client import OpenAIClient
import asyncio

async def test():
    clawhub = ClawHubClient()
    openai = OpenAIClient()
    researcher = MultiCriteriaResearcher(clawhub, openai)
    
    # Mock candidate
    candidate = Candidate(
        name="Stripe",
        category="payment gateway",
        description="Payment processing platform",
        website="https://stripe.com"
    )
    
    context = {"tech_stack": ["Python"], "domain": "fintech"}
    findings = await researcher.research_single_candidate(candidate, context)
    
    print(f"✅ Research complete for {findings.vendor_name}")
    print(f"   SDK Quality: {len(findings.sdk_quality)} data points")
    print(f"   Hidden Risks: {len(findings.hidden_risks)} detected")

asyncio.run(test())
EOF
```

**Expected:** Research findings with data points.

### Test Weight Adjuster
```bash
python3 << 'EOF'
from agents.weight_adjuster import DynamicWeightAdjuster
from integrations.openai_client import OpenAIClient

def test():
    openai = OpenAIClient()
    adjuster = DynamicWeightAdjuster(openai)
    
    context = {"priorities": ["security", "uptime"]}
    weights = adjuster.get_initial_weights(context)
    
    print("✅ Initial weights calculated:")
    for name, weight in sorted(weights.items(), key=lambda x: x[1].current_weight, reverse=True)[:5]:
        print(f"   {name}: {weight.current_weight:.1f}%")

test()
EOF
```

**Expected:** Weight distribution summing to 100%.

---

## 4. Integration Test

### Full Evaluation Test
```bash
python3 << 'EOF'
from orchestrator import EvaluationOrchestrator
import asyncio

async def test():
    orchestrator = EvaluationOrchestrator()
    
    context = {
        "category": "payment gateway",
        "tech_stack": ["Python", "AWS"],
        "domain": "e-commerce",
        "region": "US",
        "scale": "startup",
        "priorities": ["easy integration", "low cost"],
        "compliance": ["PCI-DSS"]
    }
    
    print("🚀 Running full evaluation...")
    recommendation = await orchestrator.run_evaluation(context)
    
    print(f"\n✅ Evaluation complete!")
    print(f"Recommended: {recommendation.recommended_vendor}")
    print(f"Candidates: {', '.join(recommendation.candidates)}")
    print(f"Adjustments made: {len(recommendation.weight_adjustments)}")
    
    await orchestrator.close()

asyncio.run(test())
EOF
```

**Expected:** Full evaluation completing in 3-4 minutes with recommendation.

---

## 5. Bot Test

### Start the Bot
```bash
python main.py
```

**Expected output:**
```
Adaptive Vendor Evaluation Agent
Powered by OpenClaw, SOUL.md, and ClawHub
============================================
Initializing evaluation orchestrator...
Initializing Telegram bot...
Starting bot...
============================================
🚀 Agent is running!
Send /start to your Telegram bot to begin
============================================
```

### Test Commands in Telegram

1. **Test /start**
   - Send: `/start`
   - Expected: Welcome message with instructions

2. **Test /help**
   - Send: `/help`
   - Expected: Help text with command list

3. **Test /example**
   - Send: `/example`
   - Expected: Example evaluation with reasoning

4. **Test /evaluate**
   - Send: `/evaluate`
   - Follow prompts
   - Expected: Full evaluation (takes 3-4 min)

---

## 6. Error Handling Test

### Test Invalid API Key
```bash
# Temporarily set invalid key in .env
OPENAI_API_KEY=sk-invalid

python main.py
```

**Expected:** Clear error message about invalid API key.

### Test Missing Dependencies
```bash
pip uninstall openai -y
python main.py
```

**Expected:** Import error for openai.

### Test Bot Token Issues
```bash
# Set invalid token
TELEGRAM_BOT_TOKEN=invalid

python main.py
```

**Expected:** Error about invalid bot token.

---

## 7. Load Test

### Multiple Concurrent Evaluations
```bash
python3 << 'EOF'
from orchestrator import EvaluationOrchestrator
import asyncio

async def run_evaluation(id):
    orchestrator = EvaluationOrchestrator()
    context = {
        "category": f"tool-{id}",
        "tech_stack": ["Python"],
        "domain": "tech",
        "region": "US",
        "scale": "startup",
        "priorities": ["cost"],
        "compliance": []
    }
    
    print(f"[{id}] Starting...")
    recommendation = await orchestrator.run_evaluation(context)
    print(f"[{id}] Complete: {recommendation.recommended_vendor}")
    await orchestrator.close()

async def test():
    # Run 3 evaluations in parallel
    await asyncio.gather(
        run_evaluation(1),
        run_evaluation(2),
        run_evaluation(3)
    )

asyncio.run(test())
EOF
```

**Expected:** All 3 complete successfully.

---

## 8. Log Test

### Check Logs
```bash
tail -f agent.log
```

**Expected logs:**
- Initialization messages
- Candidate identification
- Research progress
- Weight adjustments
- Final recommendations
- No ERROR level messages (warnings are OK)

---

## 9. Performance Test

### Measure Evaluation Time
```bash
time python3 << 'EOF'
from orchestrator import EvaluationOrchestrator
import asyncio

async def test():
    orchestrator = EvaluationOrchestrator()
    context = {
        "category": "database",
        "tech_stack": ["Python"],
        "domain": "SaaS",
        "region": "Global",
        "scale": "enterprise",
        "priorities": ["scalability"],
        "compliance": []
    }
    await orchestrator.run_evaluation(context)
    await orchestrator.close()

asyncio.run(test())
EOF
```

**Expected:** 2-5 minutes total time.

---

## 10. Cleanup Test

### Stop Bot Gracefully
- Ctrl+C in terminal running `main.py`
- Expected: Clean shutdown with no errors

### Check for Orphaned Resources
```bash
# No hanging connections
lsof -i | grep python
```

---

## Success Criteria

✅ All dependencies installed  
✅ OpenAI API connected  
✅ Telegram bot responds  
✅ Candidate identification works  
✅ Research returns data  
✅ Weight adjustment works  
✅ Full evaluation completes  
✅ Bot handles /evaluate command  
✅ Logs are clean  
✅ Performance is acceptable (3-4 min)  
✅ Graceful shutdown  

---

## Common Issues

### "Rate limit exceeded"
- OpenAI API has rate limits
- Wait 60 seconds between tests
- Or use GPT-3.5-turbo (faster, cheaper)

### "Timeout error"
- ClawHub searches may be slow
- Increase timeout in config.py
- Check internet connection

### "Bot not responding"
- Check bot is running: `ps aux | grep python`
- Check logs: `tail agent.log`
- Verify token: `curl https://api.telegram.org/bot<TOKEN>/getMe`

---

## Ready for Deployment?

If all tests pass ✅, you're ready to deploy to VPS!

See [SETUP.md](SETUP.md) for deployment instructions.
