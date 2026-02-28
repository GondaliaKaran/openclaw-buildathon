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
