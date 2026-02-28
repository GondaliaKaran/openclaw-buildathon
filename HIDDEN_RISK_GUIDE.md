# 🔍 Hidden Risk Detection - Bonus Challenge Guide

## What Makes This a "Hidden Risk"?

Hidden risks are **NOT found in standard vendor comparison tables**. They require:
- Deep research beyond marketing materials
- Pattern analysis from GitHub/community data
- Reading between the lines of pricing pages
- Tracking vendor health indicators

---

## ✅ Already Implemented (Basic)

Your system already detects 3 types of hidden risks in `researcher.py`:

### 1. **Maintainer Health Risk**
```python
# Detects:
- Contributor churn (key maintainers leaving)
- Bus factor (single maintainer dependency)
- Decreased commit activity
- Stale pull requests

# Example Output:
{
  "type": "maintainer_health",
  "severity": "medium",
  "description": "Project has single active maintainer with decreasing commit frequency",
  "evidence": "github.com/vendor/sdk - 80% commits from 1 person, -50% activity vs 2025"
}
```

### 2. **Pricing Trap Risk**
```python
# Detects:
- Sudden cost jumps at scale thresholds
- Hidden per-operation fees
- "Contact sales" barriers

# Example Output:
{
  "type": "pricing_trap",
  "severity": "medium",
  "description": "Pricing explodes from $99/mo to $2,500/mo at 100k operations",
  "evidence": "Enterprise tier forces 'contact sales' at reachable volume"
}
```

### 3. **Vendor Lock-in Risk**
```python
# Detects:
- Migration difficulty reports
- Proprietary data formats
- No data export features

# Example Output:
{
  "type": "vendor_lockin",
  "severity": "low",
  "description": "Users report 2-3 month migration time due to proprietary format",
  "evidence": "No automated export, manual data extraction required"
}
```

---

## 🚀 Advanced Detection (Enhanced)

The `advanced_risk_detector.py` adds 5 more sophisticated checks:

### 1. **GitHub Maintainer Pattern Analysis**

**What it detects:**
- Commit frequency decline (daily → weekly → monthly)
- Key contributor departures (1000+ commit maintainers leaving)
- Unmerged critical PRs sitting for months
- Issue response time degradation
- Active forks suggesting abandonment

**Example Real-World Risk:**
```
RISK: maintainer_exodus
SEVERITY: high
EVIDENCE: Core maintainer (60% of commits) last commit 4 months ago. 
         23 open critical issues, 15 unmerged security PRs.
         Fork with 2x stars suggests community migration.
IMPACT: SDK may become unmaintained. Security patches delayed.
        Consider alternative or plan migration budget.
```

---

### 2. **Pricing Explosion at Scale**

**What it detects:**
- Non-linear cost growth (10x users = 50x cost)
- Hidden per-operation fees that multiply
- Volume discount cliffs
- "Contact sales" at reachable volumes
- Overage fees disproportionate to base cost

**Example Real-World Risk:**
```
RISK: pricing_explosion
SEVERITY: high
EVIDENCE: Auth0 pricing: $23/1000 MAU looks reasonable.
         But 1M users = $23,000/month.
         Competitors charge flat $500/month for same scale.
IMPACT: At your projected 500k users in Year 2:
        - Auth0: $11,500/month
        - Alternative: $500/month flat
        Hidden cost: $132,000/year difference
```

**Real Examples:**
- **Auth0**: Per-MAU pricing fine until you hit scale
- **Twilio**: Per-message costs add up fast for high-volume apps
- **AWS Lambda**: Looks cheap until you hit millions of invocations

---

### 3. **Acquisition Disruption**

**What it detects:**
- Recent acquisitions (< 12 months)
- Service disruption reports post-acquisition
- Sudden pricing increases
- Feature deprecations/forced migrations
- Support quality degradation

**Example Real-World Risk:**
```
RISK: acquisition_disruption
SEVERITY: medium
EVIDENCE: Acquired by Enterprise Corp 3 months ago.
         Reddit reports: support response 2 days → 2 weeks.
         Pricing increased 40% for new customers.
         3 features deprecated, forced migration by Q3.
IMPACT: Expect:
        - Higher renewal costs (40-60% increase likely)
        - Slower support (enterprise bureaucracy)
        - Breaking changes (integration rework needed)
```

**Real Examples:**
- **Mailchimp → Intuit**: Price increases, Intuit products forced upon users
- **GitHub → Microsoft**: Initially worried but stable (good acquisition)
- **Quip → Salesforce**: Forced Salesforce ecosystem integration

---

### 4. **Compliance Drift**

**What it detects:**
- Expired certifications (SOC 2, ISO, HIPAA)
- Failed recent audits
- Removed compliance badges from website
- Regional license losses
- Pending renewals with uncertain outcomes

**Example Real-World Risk:**
```
RISK: compliance_drift
SEVERITY: high
EVIDENCE: SOC 2 Type II expired 2025-12-01 (3 months ago).
         Website still shows badge but cert portal shows "renewal pending".
         HIPAA audit failed in 2025-Q4, reaudit scheduled.
IMPACT: Legal risk:
        - Cannot use for healthcare data until HIPAA passes
        - SOC 2 lapse blocks enterprise contracts
        - Potential regulatory fines if breach occurs
```

---

### 5. **Technology Deprecation**

**What it detects:**
- API version sunsets announced
- SDK deprecations (Python 2.7, Node 12 SDKs)
- Breaking changes with short timelines
- Official SDK abandonment

**Example Real-World Risk:**
```
RISK: technology_deprecation
SEVERITY: medium
EVIDENCE: API v2 sunset announced for 2026-06-30 (4 months away).
         v3 requires complete rewrite (not backward compatible).
         Python SDK: last update 18 months ago, stuck on v2.
IMPACT: Migration required:
        - 2-3 week development effort
        - Testing/QA: 1 week
        - Must complete before June or service breaks
        - Python SDK may need custom wrapper
```

---

## 🎯 How to Demo This

### Test Scenario 1: GitHub Maintainer Risk

**Query to Telegram bot:**
```
evaluate open-source monitoring tools for production use
```

**Expected Hidden Risk:**
```
🚨 HIDDEN RISK DETECTED:

Tool: Prometheus
Risk: Maintainer Health
Severity: LOW ✅

Evidence: While core project is stable, official Python client has 
decreased maintainer activity. Last release 8 months ago with 
45 open issues.

Impact: Not critical (core is healthy), but Python users may need 
to contribute PRs or use community fork.

Recommendation: Safe to use, but monitor Python client status.
```

---

### Test Scenario 2: Pricing Explosion

**Query to Telegram bot:**
```
evaluate payment gateways for startup expecting 1M transactions/month in year 2
```

**Expected Hidden Risk:**
```
🚨 HIDDEN RISK DETECTED:

Vendor: Stripe
Risk: Pricing Explosion at Scale
Severity: MEDIUM ⚠️

Evidence: 
- Current (10k tx/mo): $290/month (2.9% per tx)
- At 1M tx/mo: $29,000/month (2.9% still applies)
- Competitors offer volume pricing: 1.5% above 500k tx

Impact: Year 2 cost projection:
- Stripe: $348,000/year at 2.9%
- Razorpay: $180,000/year at 1.5% (Enterprise tier)
- Hidden cost: $168,000/year difference

Recommendation: Negotiate enterprise pricing NOW or choose 
volume-friendly alternative.
```

---

### Test Scenario 3: Acquisition Risk

**Query to Telegram bot:**
```
evaluate CRM for B2B sales team, need stability
```

**Expected Hidden Risk:**
```
🚨 HIDDEN RISK DETECTED:

Vendor: Pipedrive
Risk: Recent Acquisition
Severity: MEDIUM ⚠️

Evidence: Acquired by Vista Equity Partners (9 months ago).
- Pricing increased 25% for new customers
- Community reports slower support response
- API v1 deprecated (forced migration to v2 by Q4)

Impact: Expect:
- Renewal increase: 15-30% likely
- Feature bloat: Private equity playbook includes upselling
- Integration rework: API v1 sunset means dev time

Recommendation: Negotiate multi-year pricing lock NOW before 
next increase. Budget 2 weeks for API migration.
```

---

## 📊 Output Format for Hidden Risks

Your system formats hidden risks like this:

```json
{
  "hidden_risks": [
    {
      "category": "github_maintainer",
      "type": "maintainer_exodus",
      "severity": "high",
      "description": "Core maintainer left, project slowing",
      "evidence": "60% of commits from departed maintainer, 4 months since last commit",
      "impact": "SDK may become unmaintained, security patches delayed"
    },
    {
      "category": "pricing_explosion",
      "type": "volume_pricing_trap",
      "severity": "medium",
      "description": "Cost grows faster than usage",
      "evidence": "$99 → $2,500 at reachable threshold",
      "impact": "$30k annual surprise cost at projected scale"
    }
  ]
}
```

---

## 🎪 Judging Criteria - What to Show

**For Bonus Challenge Points:**

1. ✅ **Show at least 1 detected hidden risk** that's NOT in standard comparisons
2. ✅ **Explain HOW it was found** (GitHub patterns, pricing analysis, etc.)
3. ✅ **Demonstrate IMPACT** ($ cost, migration time, business risk)
4. ✅ **Provide EVIDENCE** (specific data points, not vague handwaving)

**Winning Demo:**
```
"Here's a hidden risk the judges wouldn't find on vendor comparison sites:

Twilio looks cheap at $0.0075 per SMS. But at our projected volume of 
100k SMS/month, that's $750/month or $9,000/year.

I discovered by analyzing their pricing API that bulk SMS providers 
charge $0.002 per SMS at this volume - that's $200/month or $2,400/year.

Hidden cost: $6,600/year that standard comparisons wouldn't reveal.

This was detected by my pricing explosion algorithm analyzing volume 
tiers and competitor data."
```

---

## 🚀 Quick Integration

To add advanced detection to your deployed system:

1. **Upload new file:**
```bash
scp advanced_risk_detector.py root@187.77.190.61:/tmp/vendor-evaluation/agents/
docker cp /tmp/vendor-evaluation/agents/advanced_risk_detector.py openclaw-l8o7-openclaw-1:/data/.openclaw/workspace/vendor-evaluation/agents/
```

2. **Import in researcher.py:**
```python
from agents.advanced_risk_detector import AdvancedRiskDetector

# In Researcher class __init__:
self.advanced_detector = AdvancedRiskDetector(self.clawhub, self.openai)

# In _detect_hidden_risks method:
advanced_risks = await self.advanced_detector.detect_github_maintainer_risks(github_url)
risks.extend(advanced_risks)
```

3. **Restart OpenClaw:**
```bash
docker restart openclaw-l8o7-openclaw-1
```

---

## 💡 Pro Tips

**Make it obvious in demo:**
- Use 🚨 emoji for hidden risks
- Show the evidence clearly
- Quantify the impact ($, time, effort)
- Contrast with what "normal" comparison would show

**Strong hidden risk examples:**
- "Vendor comparison shows both cost $99/month. But hidden cost: one scales to $10k/mo at our volume"
- "All reviews mention 'great support'. But GitHub shows maintainer left 6 months ago - no one's home"
- "Looks cheap now, but recent acquisition increased prices 40% for existing customers"

The key is **revealing what's hidden** - things that require research beyond marketing pages! 🔍
