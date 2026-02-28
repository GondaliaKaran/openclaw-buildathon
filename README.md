# Adaptive Vendor Evaluation Agent

**OpenClaw Buildathon — Challenge #104**

Research like a team of 5 analysts, decide like a CTO — adaptive tech evaluation with dynamic criteria weighting.

## What This Does

An AI agent that evaluates vendors/tools/platforms with **adaptive criteria weighting**. Unlike static comparison matrices, this agent changes its evaluation criteria based on what it discovers during research.

**Example**: Discovering a vendor had 3 outages last month automatically increases the "Uptime/Reliability" weight and triggers deeper investigation of all vendors' status pages.

## Architecture (Three-Layer Breakdown)

### Interface Layer (SOUL.md)
- Senior tech evaluator/CTO advisor persona
- Produces structured comparison with full reasoning chain
- 8-section mandatory output format ensuring every evaluation is thorough

### Logic Layer (Python Orchestrator)
- **Candidate Identifier** (30 min) — Finds 3-5 relevant vendors based on context
- **Multi-Criteria Researcher** (1 hr) — Deep investigation across technical, operational, business, and hidden risk dimensions
- **Dynamic Weight Adjuster** (45 min) — Reshapes criteria weights based on research discoveries
- **Recommendation Synthesizer** (30 min) — Produces final comparison with justified recommendation

### Integration Layer (ClawHub + OpenAI)
- ClawHub web search for vendor sites, GitHub, G2, status pages, compliance registries
- OpenAI GPT-4o for analysis and synthesis

## Key Deliverables

### ✅ Accepts evaluation request and autonomously identifies candidates
The agent extracts context (category, tech stack, domain, region, scale) from natural language queries and identifies 3-5 relevant candidates with rationale for each inclusion.

### ✅ Dynamic criteria re-weighting (3+ instances per evaluation)
Every evaluation shows explicit weight adjustment tables:

| Criterion | Initial Weight | Final Weight | Reason for Change |
|-----------|---------------|--------------|-------------------|
| Payment Success Rate | 20% | 28% | Razorpay status page: 4 UPI incidents in 90 days |
| Pricing/MDR | 10% | 18% | Stripe USD pricing = 3.4% effective vs Razorpay 2% |
| Vendor Health | 5% | 12% | PayU parent Prosus restructured fintech division |

### ✅ Structured comparison with reasoning chain
Full output includes: context summary → candidates → discoveries → weight table → comparison matrix → hidden risks → recommendation → reproducibility notes.

### ✅ Same category, different context = different evaluation
"Payment gateways for Indian startup" produces completely different weights, scores, and recommendations than "Payment gateways for US enterprise" — demonstrated with different starting weight templates, different vendor pools, and different discoveries.

## 🔍 Research Methodology: What the Agent Actually Scans

The agent performs **real-time internet research** across 7 data dimensions for each vendor. Here's what it searches and fetches:

### 1. Technical Health & Quality
**What it checks:**
- GitHub repository metrics (stars, forks, issues, last commit)
- SDK/library availability and maintenance
- Documentation quality and completeness
- API design patterns and developer experience

**Example searches per scenario:**

**Payment Gateway:**
```
• "razorpay github python SDK"
  → Finds: github.com/razorpay/razorpay-python
• Fetch: https://api.github.com/repos/razorpay/razorpay-python
  → Gets: 487 stars, last push 12 days ago, 23 open issues
• "stripe API documentation quality review"
• Fetch: https://docs.stripe.com/api
```

**CDN:**
```
• "cloudflare terraform provider github"
  → Finds: github.com/cloudflare/terraform-provider-cloudflare
• Fetch: https://api.github.com/repos/cloudflare/terraform-provider-cloudflare/contributors
  → Bus factor check: top 3 contributors = 67% of commits
• "fastly edge compute documentation"
```

**Observability:**
```
• "datadog agent github stars"
• "prometheus exporter ecosystem npm"
• "grafana plugin marketplace size"
```

---

### 2. Reliability & Uptime History
**What it checks:**
- Status page incident history (last 90 days)
- Current service health across regions
- Planned maintenance windows
- SLA claims vs actual performance

**Example searches per scenario:**

**Payment Gateway:**
```
• "razorpay status page"
  → Finds: status.razorpay.com
• Fetch: https://status.razorpay.com/api/v2/incidents.json
  → 4 UPI-related incidents in last 90 days
• "cashfree outage 2025 site:twitter.com"
  → Social signals for unreported incidents
```

**CDN:**
```
• Fetch: https://www.cloudflarestatus.com/api/v2/summary.json
  → Real-time PoP health: Mumbai operational, Ahmedabad under_maintenance
• "akamai cdn outage incident 2025 2026"
• "fastly status page api"
```

**Observability:**
```
• "datadog downtime incident 2025"
• "new relic status page API"
• "grafana cloud reliability SLA"
```

---

### 3. Compliance & Security Certifications
**What it checks:**
- PCI DSS, SOC 2, ISO 27001 status
- Region-specific compliance (RBI in India, GDPR in EU, HIPAA in US)
- Security audit reports and attestations
- Data residency and sovereignty claims

**Example searches per scenario:**

**Payment Gateway:**
```
• "razorpay PCI DSS level compliance certificate"
• "stripe SOC2 report 2025"
• "cashfree RBI payment aggregator license"
  → Critical for India operations
• Fetch: https://razorpay.com/security
  → Claims: PCI DSS Level 1, ISO 27001
```

**CDN:**
```
• "cloudflare GDPR compliance data residency"
• "akamai FedRAMP certification government"
• "fastly HIPAA BAA business associate agreement"
```

**Observability:**
```
• "datadog SOC2 Type II audit report"
• "new relic HIPAA compliance healthcare"
• "grafana ISO 27001 certificate"
```

---

### 4. Pricing Structure & Hidden Costs
**What it checks:**
- Base pricing tiers and volume breakpoints
- Regional pricing variations (India vs US vs EU)
- Hidden fees (setup, support, API calls, bandwidth)
- Non-linear cost scaling (10x traffic ≠ 10x cost)

**Example searches per scenario:**

**Payment Gateway:**
```
• "razorpay pricing india MDR 2025"
• Fetch: https://razorpay.com/pricing-india
  → 2% for UPI, 2.5% for cards
• "stripe pricing currency conversion fees"
• Calculate: 10K tx/month at ₹500 avg → ₹1,00,000 vs $2,900
  → At 100K tx/month → non-linear jump due to forex
```

**CDN:**
```
• Fetch: https://www.fastly.com/pricing
  → India region: $0.28/GB (100GB-10TB)
  → Constraint: "No more than 10% traffic from India" on packages
• "cloudflare enterprise pricing negotiation"
• Calculate: 1TB → 3TB → 10TB to find pricing cliffs
```

**Observability:**
```
• "datadog pricing calculator ingestion cost"
• "grafana cloud pricing per user vs self-hosted"
• "prometheus managed service cost comparison"
```

---

### 5. User Sentiment & Real Experiences
**What it checks:**
- G2/Capterra aggregate ratings and review count
- Reddit/HN discussions about pain points
- Common complaints (support, billing surprises, integration complexity)
- Migration stories (switching from competitor)

**Example searches per scenario:**

**Payment Gateway:**
```
• "razorpay G2 reviews 2025"
  → 4.3/5 from 830 reviews
• "stripe review site:reddit.com"
  → Common themes: great docs, expensive at scale
• "cashfree integration problems issues"
```

**CDN:**
```
• "cloudflare vs fastly comparison site:news.ycombinator.com"
• "akamai customer support review G2"
• "vercel edge network performance reddit"
```

**Observability:**
```
• "datadog vs new relic cost comparison 2025"
• "grafana cloud review site:reddit.com"
• "self-hosted prometheus challenges"
```

---

### 6. Corporate Stability & Risk Signals
**What it checks:**
- Recent acquisitions or mergers
- Funding rounds and runway estimates
- Layoffs or restructuring announcements
- Executive turnover (CEO changes)
- Product sunset/pivot signals

**Example searches per scenario:**

**Payment Gateway:**
```
• "payu acquisition prosus restructuring 2025"
  → Finds: Parent company Prosus restructured fintech division
• "cashfree funding series round 2025 2026"
• "stripe IPO layoffs 2025"
```

**CDN:**
```
• "fastly acquisition rumors 2025"
• "cloudflare layoffs workforce reduction"
• "akamai merger news 2026"
```

**Observability:**
```
• "datadog acquisition splunk 2025"
• "new relic layoffs restructuring"
• "grafana labs funding series"
```

---

### 7. Technology Risk & Lock-in
**What it checks:**
- API deprecation schedules and breaking changes
- SDK maintenance status
- Data export capabilities (lock-in risk)
- Proprietary formats vs open standards
- Migration complexity from vendor

**Example searches per scenario:**

**Payment Gateway:**
```
• "stripe API deprecation sunset 2025"
• "razorpay webhook format change breaking"
• Search GitHub issues: repo:razorpay/razorpay-python label:breaking
• "payment gateway migration guide switching"
```

**CDN:**
```
• "cloudflare workers API breaking changes"
• "fastly VCL deprecation timeline"
• "migrating from cloudflare to fastly"
```

**Observability:**
```
• "datadog agent version EOL support"
• "prometheus remote write API changes"
• "grafana dashboard export migration"
```

---

## Research Depth: Numbers

For a typical evaluation with 4 candidates:
- **40-60 web searches** (10-15 per vendor)
- **20-30 URL fetches** (GitHub API, status pages, pricing pages)
- **15-20 specific evidence citations** in the final report
- **All vendors researched equally** (no "N/A — not checked" lazy shortcuts)

**Time**: 30-90 seconds for full evaluation (OpenAI API + web search latency)

## ⭐ Bonus: Hidden Risk Detection

The agent checks 6 categories of hidden risks that standard comparisons miss:

1. **🔧 Maintainer/Team Health** — GitHub commit patterns, bus factor, contributor churn
2. **💰 Pricing Traps** — Non-linear cost scaling, hidden fees at volume thresholds
3. **🔒 Vendor Lock-in** — Proprietary formats, migration difficulty, data export limits
4. **🏢 Acquisition Risk** — Recent M&A, parent company changes, roadmap uncertainty
5. **📋 Compliance Drift** — Expired certifications, failed audits
6. **🛠️ Technology Deprecation** — API sunsets, SDK abandonment

## Files

```
SOUL.md                              # Agent persona + evaluation process + output format
AGENTS.md                            # Skill trigger conditions + execution instructions
orchestrator.py                      # Main coordination logic (4-phase pipeline)
agents/
  candidate_identifier.py            # Phase 1: Find 3-5 candidates
  researcher.py                      # Phase 2: Multi-criteria deep research
  advanced_risk_detector.py          # Phase 2b: 6-type hidden risk detection
  weight_adjuster.py                 # Phase 3: Dynamic weight adjustment
  synthesizer.py                     # Phase 4: Final recommendation
integrations/
  clawhub.py                         # ClawHub web search integration
  openai_client.py                   # OpenAI API client
utils/
  query_parser.py                    # Natural language → structured context
  logger.py                          # Logging
config.py                            # Configuration (pydantic models)
run_evaluation.py                    # CLI entry point
skill.json                           # OpenClaw skill manifest
skill_handler.py                     # OpenClaw skill handler
```

## How to Test

Send to the Telegram bot:

**Test 1 — India context:**
```
evaluate payment gateways for Indian startup with 10K transactions/month
```

**Test 2 — US context (same category, different output):**
```
evaluate payment gateways for US enterprise with 500K transactions/month
```

**Test 3 — Different category:**
```
evaluate authentication solutions for healthcare startup with 5000 users
```

Each response will include all 8 sections with different weights, different candidates, different discoveries, and different recommendations.

## Evaluation Rubric Mapping

| Rubric Criteria | Weight | How We Address It |
|---|---|---|
| Adaptive Evaluation | 30% | Explicit weight tables with before/after + evidence chains for each adjustment |
| Research Depth | 25% | Web search for GitHub, status pages, G2, pricing, compliance; hidden risk detection |
| Contextual Awareness | 20% | Different starting weights per context; region/stack/domain affect candidate pool |
| Recommendation Quality | 15% | Primary + backup + conditional alternatives; honest trade-offs with evidence |
| Reproducibility | 10% | Date-stamped; data sources listed; can re-run with updated data |

## Setup

1. OpenClaw on Hostinger VPS with GPT-4o
2. Telegram bot gateway
3. Place SOUL.md and AGENTS.md in OpenClaw workspace
4. Place Python files in workspace/vendor-evaluation/

## Channel

Telegram
