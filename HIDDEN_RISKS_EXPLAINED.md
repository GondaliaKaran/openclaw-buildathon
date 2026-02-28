# Hidden Risk Detection - Bonus Challenge Implementation

## Overview
The system detects **8 types of hidden risks** that don't appear in standard vendor comparisons.

## Hidden Risk Types Detected

### 1. 🔧 GitHub Maintainer Health
**What it detects:**
- Commit frequency decline (daily → weekly → monthly)
- Key contributor departures (1000+ commits, suddenly stopped)
- Stale pull requests (critical PRs unmerged for months)
- Issue backlog explosion
- Active forks suggesting abandonment

**Example findings:**
```
⚠️ Maintainer Health Risk
Evidence: Lead maintainer (60% of commits) last active 8 months ago
Impact: Bus factor = 1, sustainability concerns
Severity: High
```

### 2. 💰 Pricing Explosions at Scale
**What it detects:**
- Non-linear cost scaling (10x users = 50x cost)
- Hidden per-operation fees
- Volume discount cliffs
- "Contact sales" at reachable thresholds
- Bandwidth/storage overage traps

**Example findings:**
```
⚠️ Pricing Explosion Risk
Evidence: Auth0 at $0.023/MAU → 1M users = $23k/month
Impact: Cost explodes 40x when scaling from 25K to 1M users
Severity: High
```

### 3. 🔒 Vendor Lock-in
**What it detects:**
- Proprietary data formats
- Export limitations
- Migration complexity
- Ecosystem capture
- API incompatibility with alternatives

**Example findings:**
```
⚠️ Vendor Lock-in Risk
Evidence: Proprietary database format, no standard export
Impact: 6-month migration effort, potential data loss
Severity: Medium
```

### 4. 🏢 Acquisition/Merger Disruption
**What it detects:**
- Recent acquisitions (< 12 months)
- Post-acquisition price increases
- Service disruptions
- Feature deprecations
- Support quality decline

**Example findings:**
```
⚠️ Acquisition Risk
Evidence: Acquired by Oracle 3 months ago, pricing increased 40%
Impact: Roadmap uncertainty, forced tier upgrades
Severity: High
```

### 5. 📋 Compliance Drift
**What it detects:**
- Expired certifications
- Failed audits
- Lost regional licenses
- Pending renewals
- Removed compliance badges

**Example findings:**
```
⚠️ Compliance Drift Risk
Evidence: SOC 2 Type II certification expired April 2025
Impact: Cannot use for HIPAA-regulated workloads
Severity: High
```

### 6. 🛠️ Technology Deprecation
**What it detects:**
- API version sunsets
- SDK abandonment
- Breaking changes announced
- Short migration deadlines
- Forced upgrades

**Example findings:**
```
⚠️ Technology Deprecation Risk
Evidence: Legacy API sunset in 4 months, SDK v2 required
Impact: 2-week migration effort, breaking changes
Severity: Medium
```

### 7. 📉 Community Health Decline
**What it detects:**
- Declining Stack Overflow activity
- Reduced documentation updates
- Abandoned forum/Discord
- Growing unanswered issues

**Example findings:**
```
⚠️ Community Health Risk
Evidence: Last documentation update 14 months ago
Impact: Harder onboarding, fewer code examples
Severity: Low
```

### 8. 🆘 Support Degradation
**What it detects:**
- Increased response times
- Tier restructuring (removing free support)
- Staff departures
- Outsourced support
- Degraded SLA compliance

**Example findings:**
```
⚠️ Support Degradation Risk
Evidence: Average response time increased from 2h to 48h
Impact: Incidents take longer to resolve
Severity: Medium
```

## How It Works

### Architecture

```
Query → QueryParser → Orchestrator → [Candidate Identifier]
                                   ↓
                          [Multi-Criteria Researcher]
                                   ↓
                          [Advanced Risk Detector] ← 8 parallel checks
                                   ↓
                          [Weight Adjuster] ← Adjust based on risks
                                   ↓
                          [Synthesizer] → Final Recommendation
```

### Risk Detection Process

1. **Parallel Execution**: All 8 risk types checked simultaneously
2. **AI-Powered Analysis**: OpenAI analyzes web search results for patterns
3. **Evidence Collection**: Specific data points extracted
4. **Severity Scoring**: High/Medium/Low based on impact
5. **Integration**: Risks influence weight adjustments and final scores

### Example Code Flow

```python
# In researcher.py
async def _detect_hidden_risks(candidate, context, findings):
    risks = []
    
    # Run all 8 risk detections in parallel
    risk_tasks = [
        risk_detector.detect_github_maintainer_risks(github_url),
        risk_detector.detect_scaling_pricing_risks(vendor_name, context),
        risk_detector.detect_acquisition_risks(vendor_name),
        risk_detector.detect_compliance_drift_risks(vendor_name, compliance),
        risk_detector.detect_technology_deprecation_risks(vendor_name, tech_stack),
        _detect_lockin_risk(vendor_name),
        # ... more
    ]
    
    risk_results = await asyncio.gather(*risk_tasks)
    
    # Flatten and collect all detected risks
    for result in risk_results:
        if result:
            risks.extend(result)
    
    findings.hidden_risks = risks
```

## Output Format

### JSON Structure
```json
{
  "recommended_vendor": "Razorpay",
  "hidden_risks": [
    {
      "vendor": "Razorpay",
      "category": "github_maintainer",
      "type": "maintainer_health",
      "severity": "medium",
      "evidence": "Commit frequency dropped 60% in last 6 months",
      "impact": "Slower bug fixes, potential sustainability concerns",
      "description": "Lead maintainer reduced activity..."
    },
    {
      "vendor": "Stripe",
      "category": "pricing_explosion",
      "type": "scaling_costs",
      "severity": "high",
      "evidence": "Cost increases from $500/mo to $8,000/mo at 100K tx",
      "impact": "16x cost increase at scale",
      "description": "Pricing jumps dramatically..."
    }
  ]
}
```

### Formatted Output
```
🚨 Hidden Risks Detected:

⚠️ [Razorpay] Maintainer Health (Medium)
   Evidence: Commit frequency dropped 60% in last 6 months
   Impact: Slower bug fixes, potential sustainability concerns

⚠️ [Stripe] Pricing Explosion (High)
   Evidence: Cost increases from $500/mo to $8,000/mo at 100K tx
   Impact: 16x cost increase at scale

⚠️ [PayU] Acquisition Disruption (Medium)
   Evidence: Acquired by Prosus 4 months ago, pricing under review
   Impact: Roadmap uncertainty, potential price increases
```

## Testing Hidden Risk Detection

### Test Query 1: GitHub Maintainer Risk
```bash
python3 run_evaluation.py --query "evaluate open source payment libraries for startup"
```
Expected: Detects maintainer activity patterns

### Test Query 2: Pricing Explosion
```bash
python3 run_evaluation.py --query "evaluate authentication for startup expecting 1M users"
```
Expected: Detects Auth0/similar pricing traps at scale

### Test Query 3: Compliance Drift
```bash
python3 run_evaluation.py --query "evaluate payment gateways for healthcare with HIPAA"
```
Expected: Checks compliance certification status

### Test Query 4: Acquisition Risk
```bash
python3 run_evaluation.py --query "evaluate CRM recently acquired by enterprise vendors"
```
Expected: Detects recent acquisitions and impact

## Demonstration Script

Run this to see all hidden risks in action:

```bash
# Test 1: Basic evaluation with risks
python3 run_evaluation.py --query "evaluate payment gateways for Indian startup with 10K transactions/month"

# Test 2: Scale-focused (pricing risks)
python3 run_evaluation.py --query "evaluate CDN for video platform expecting 1M users"

# Test 3: Compliance-focused
python3 run_evaluation.py --query "evaluate authentication for healthcare with HIPAA and 5000 users"

# Test 4: Open source (maintainer risks)
python3 run_evaluation.py --query "evaluate open source monitoring tools for production use"
```

## Bonus Challenge Checklist

✅ **8 types of hidden risks detected**
- [x] GitHub maintainer health
- [x] Pricing explosions at scale
- [x] Vendor lock-in
- [x] Acquisition/merger disruption
- [x] Compliance drift
- [x] Technology deprecation
- [x] Community health
- [x] Support degradation

✅ **AI-powered pattern detection**
- Uses OpenAI to analyze search results
- Extracts specific evidence
- Scores severity

✅ **Parallel execution**
- All risk checks run simultaneously
- 3-4 minute total runtime

✅ **Structured output**
- JSON format for programmatic use
- Formatted text for human reading
- Evidence + impact for each risk

✅ **Integration with evaluation**
- Risks influence weight adjustments
- Incorporated into final recommendation
- Shown prominently in output

## Example: Full Evaluation with Hidden Risks

Query: "evaluate payment gateways for Indian startup with 10K transactions/month"

Output includes:
1. **Recommended vendor**: Razorpay
2. **3-5 candidates evaluated**: Razorpay, Cashfree, Stripe, PayU
3. **Key discoveries**: UPI dominance in India, local support importance
4. **Hidden risks detected**:
   - Razorpay: None significant
   - Cashfree: Minor GitHub activity slowdown
   - Stripe: High pricing at Indian scale (USD rates)
   - PayU: Recent parent company merger
5. **Weight adjustments**: "Local support" increased 15% → 25%
6. **Detailed reasoning**: Why Razorpay best for this specific context

This demonstrates **adaptive evaluation** - same category, different context produces different recommendations and risk profiles.
