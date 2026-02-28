# Agent Instructions for Vendor Evaluation

## Purpose
This skill provides adaptive vendor evaluation with dynamic criteria re-weighting based on context.

## When to Use This Skill

Trigger vendor evaluation when the user requests any of the following:
- "evaluate [vendor category] for [context]"
- "compare [vendor category]"
- "recommend [vendor category] for [use case]"
- "find the best [vendor category]"
- "which [vendor category] should I use"
- "help me choose [vendor category]"

Examples:
- "evaluate payment gateways for Indian startup"
- "compare authentication solutions for healthcare"
- "recommend CRM for enterprise with 50k users"
- "find the best CDN for video streaming"

## ⚠️ CRITICAL: How to Execute Evaluation

**When a user makes a vendor evaluation request, you MUST immediately run the evaluation command. DO NOT ask clarifying questions first.**

### Step 1: Identify Evaluation Request
If the user's message contains evaluation keywords (evaluate, compare, recommend, find, choose) + vendor category → proceed to Step 2

### Step 2: Run Evaluation Immediately
Execute this command:
```bash
cd /data/.openclaw/workspace/vendor-evaluation && python3 run_evaluation.py --query "USER_EXACT_QUERY_HERE"
```

Replace `USER_EXACT_QUERY_HERE` with the user's exact message.

**Example:**
User says: "evaluate payment gateways for startup expecting 1M transactions/month"
You run:
```bash
cd /data/.openclaw/workspace/vendor-evaluation && python3 run_evaluation.py --query "evaluate payment gateways for startup expecting 1M transactions/month"
```

### Step 3: Present Results
After the command completes (3-4 minutes), present the structured results to the user:
- Recommended vendor
- Key discoveries
- Hidden risks detected
- Weight adjustments made
- Detailed reasoning

## What Makes This Skill Special

### 1. Dynamic Criteria Re-weighting
The system automatically adjusts evaluation criteria weights based on context:
- Startup (50 users) → Focus on ease of use, cost
- Enterprise (50k users) → Focus on scalability, security, compliance
- Healthcare → Emphasize compliance (HIPAA), security
- E-commerce → Prioritize payment security, performance
- Developer tools → Code quality, documentation, community

### 2. Hidden Risk Detection
The system goes beyond basic comparisons to detect:
- **Maintainer Health**: GitHub activity patterns, bus factor, maintainer burnout
- **Pricing Traps**: Scale-based cost explosions, hidden fees, tier jumping
- **Vendor Lock-in**: Proprietary formats, migration difficulty, ecosystem capture
- **Acquisition Risks**: Recent acquisitions that may affect roadmap
- **Compliance Drift**: Changing regulatory requirements
- **Technology Deprecation**: Outdated tech stacks, declining community support

### 3. Context-Aware Recommendations
Same category, different context = different recommendations:
- "Auth for healthcare" → Emphasizes HIPAA compliance, audit trails
- "Auth for e-commerce" → Emphasizes social login, UX, conversion optimization
- "Auth for enterprise" → Emphasizes SSO, AD integration, role management

## Response Format

When evaluation completes, structure your response as:

```
📊 Vendor Evaluation Results

**Category:** [category]
**Recommended:** [vendor name]

**Top 3 Candidates Evaluated:**
1. [Vendor 1] - [Score]
2. [Vendor 2] - [Score]
3. [Vendor 3] - [Score]

**Key Discoveries:**
• [Discovery 1]
• [Discovery 2]
• [Discovery 3]

**🚨 Hidden Risks Detected:**
⚠️ [Risk Type]: [Description]
⚠️ [Risk Type]: [Description]

**💡 Recommendation:**
[Detailed reasoning for why this vendor is best for their specific context]

**⚖️ Weight Adjustments Made:**
[Explain how criteria were weighted for this specific context]
```

## Important Notes

1. **DO NOT** ask clarifying questions before running evaluation - the orchestrator will extract context from the query
2. **DO** run the evaluation immediately when triggered
3. **DO** present results in a clear, structured format
4. **DO** highlight hidden risks prominently
5. **DO** explain the reasoning behind weight adjustments

## Technical Details

- Runtime: 3-4 minutes per evaluation
- Uses: OpenAI GPT-4 Turbo, ClawHub web search
- Output: Structured JSON + formatted text
- Location: `/data/.openclaw/workspace/vendor-evaluation/`

## Error Handling

If evaluation fails:
1. Check if query contains valid vendor category
2. Verify OpenAI API key is set
3. Check Python environment and dependencies
4. Review logs for specific error messages
5. Inform user and suggest rephrasing query if category unclear
