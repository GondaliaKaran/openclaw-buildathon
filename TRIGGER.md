# EVALUATION TRIGGER - READ THIS FIRST

## Execution Priority: HIGHEST

When you see a message that matches ANY of these patterns:

**Trigger phrases:**
- "evaluate [X]"
- "compare [X]"  
- "recommend [X]"
- "find the best [X]"
- "which [X] should"
- "help me choose [X]"

**Where X is a vendor category like:**
- payment gateway/gateways
- authentication/auth
- CRM
- CDN
- database
- monitoring
- analytics
- email service
- SMS gateway
- etc.

## What to do IMMEDIATELY:

**STOP. Do not respond conversationally.**

**Execute this command:**
```bash
cd /data/.openclaw/workspace/vendor-evaluation && python3 run_evaluation.py --query "PASTE_USER_MESSAGE_HERE"
```

**Example:**
User: "evaluate payment gateways for Indian startup with 10K transactions/month"

You execute:
```bash
cd /data/.openclaw/workspace/vendor-evaluation && python3 run_evaluation.py --query "evaluate payment gateways for Indian startup with 10K transactions/month"
```

Wait 3-4 minutes for the orchestrator to complete.

Then present the results.

## Why this matters

The orchestrator performs:
1. Candidate identification (3-5 vendors)
2. Multi-criteria research (8 dimensions)
3. Hidden risk detection (8 types)
4. Dynamic weight adjustment (context-aware)
5. Final synthesis with evidence

Your conversational response, while helpful, **skips the hidden risk detection and weight adjustment** which is the core value proposition of this system.

## After results are shown

THEN you can:
- Answer follow-up questions
- Clarify specific points
- Dive deeper into any vendor
- Suggest additional considerations

But the FIRST response to an evaluation query MUST be the orchestrator output.
