# Deployment Instructions

## What's Ready

✅ **run_evaluation.py** - CLI wrapper to execute vendor evaluation directly  
✅ **AGENTS.md** - Instructions for OpenClaw agent to trigger evaluation  
✅ **test_local.sh** - Local testing script (optional)  
✅ **All fixes applied** - Config access pattern corrected  

## Quick Deploy to VPS

### Step 1: Push to GitHub
```bash
cd /Users/karan/Documents/openclaw-buildathon

# Add new files
git add AGENTS.md run_evaluation.py test_local.sh

# Commit
git commit -m "Add run_evaluation.py CLI wrapper and OpenClaw instructions"

# Push
git push origin main
```

### Step 2: Deploy on VPS
```bash
# SSH to VPS
ssh root@187.77.190.61

# Run deployment script
/root/deploy-vendor-eval.sh
```

The deployment script will:
1. Pull latest changes from GitHub
2. Copy files to OpenClaw workspace
3. Set permissions
4. Restart OpenClaw if needed

### Step 3: Test via Telegram

Send to @karan_oc_bot:
```
evaluate authentication solutions for healthcare startup with 5000 users
```

Expected behavior:
- Agent should run: `python3 run_evaluation.py --query "..."`
- Wait 3-4 minutes for evaluation
- Return structured results with recommendations and hidden risks

## Files Updated This Session

### New Files Created
1. **run_evaluation.py** (93 lines)
   - CLI wrapper with argparse
   - Proper config access: `config.openai.api_key`
   - Formatted output with JSON export
   - Error handling

2. **AGENTS.md** (159 lines)
   - When/how to trigger evaluation
   - Command to execute: `cd /data/.openclaw/workspace/vendor-evaluation && python3 run_evaluation.py --query "..."`
   - Response format guidelines
   - Hidden risk types explained

3. **test_local.sh** (Bash script)
   - Setup venv, install dependencies
   - Check .env file
   - Run test evaluation
   - Optional - for local testing only

### Existing Files (No Changes Needed)
- orchestrator.py ✅
- agents/* ✅
- config.py ✅
- requirements.txt ✅
- SOUL.md ✅ (already comprehensive)

## Key Fixes Applied

### 1. Config Access Pattern
**Before:** `orchestrator = EvaluationOrchestrator(openai_api_key=config.openai.api_key)`
**After:** `orchestrator = EvaluationOrchestrator()` (uses global config)

**Reason:** Orchestrator's `__init__()` doesn't accept parameters, relies on imported config

### 2. AGENTS.md Instructions
**Added:** Explicit command execution instructions
**Critical:** "IMMEDIATELY run this command" to prevent conversational fallback

## Expected Behavior After Deploy

### When User Sends: "evaluate X for Y"

1. ✅ OpenClaw reads AGENTS.md instructions
2. ✅ Agent recognizes evaluation trigger
3. ✅ Executes: `python3 run_evaluation.py --query "evaluate X for Y"`
4. ✅ Orchestrator runs 4-phase pipeline (3-4 minutes)
5. ✅ Returns structured results with:
   - Recommended vendor
   - 3-5 candidates evaluated
   - Key discoveries
   - Hidden risks detected
   - Weight adjustments explained

### If Agent Still Asks Questions Instead

**Troubleshooting:**
1. Check AGENTS.md is in `/data/.openclaw/workspace/AGENTS.md`
2. Verify SOUL.md isn't overriding execution behavior
3. Add more explicit trigger phrases to AGENTS.md
4. Test command directly: `docker exec openclaw-l8o7-openclaw-1 bash -c "cd /data/.openclaw/workspace/vendor-evaluation && python3 run_evaluation.py --query 'test'"`

## Demo Testing Queries

After deployment, test with these:

### 1. Basic Evaluation
```
evaluate payment gateways for Indian startup with 10K transactions/month
```
Expected: Razorpay vs Stripe comparison, India-specific recommendations

### 2. Hidden Risk Detection
```
evaluate authentication for healthcare with HIPAA requirements
```
Expected: Compliance-focused weights, hidden risks around audit trails

### 3. Same Category, Different Context
**Query A:** `evaluate CRM for startup with 50 users`
**Query B:** `evaluate CRM for enterprise with 50,000 users`
Expected: Different recommendations, different weight adjustments

### 4. Scaling Concerns
```
evaluate CDN for video platform expecting 1M users
```
Expected: Bandwidth pricing traps detected, scaling cost projections

## Rollback Plan

If deployment breaks something:
```bash
# SSH to VPS
ssh root@187.77.190.61

# Remove new files
docker exec openclaw-l8o7-openclaw-1 rm /data/.openclaw/workspace/vendor-evaluation/run_evaluation.py
docker exec openclaw-l8o7-openclaw-1 rm /data/.openclaw/workspace/AGENTS.md

# Restart OpenClaw
cd /root/openclaw-l8o7
docker-compose restart
```

## Questions to Validate After Deploy

1. ✅ Does `@karan_oc_bot` respond to "evaluate" queries?
2. ✅ Does it execute the command instead of asking questions?
3. ✅ Does evaluation complete in 3-4 minutes?
4. ✅ Are hidden risks displayed in output?
5. ✅ Are weight adjustments explained?

## Next Steps After Successful Deploy

1. **Test all demo queries** above
2. **Document actual output** for buildathon submission
3. **Record demo video** showing:
   - Same category, different context → different recommendations
   - Hidden risk detection in action
   - Dynamic weight adjustment explanations
4. **Prepare buildathon presentation** highlighting:
   - Adaptive evaluation (not static scoring)
   - 5+ hidden risk types detected
   - Context-aware recommendations

---

**Ready to deploy!** Just run the commands in Step 1 and Step 2 above.
