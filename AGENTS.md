# AGENTS: Vendor Evaluation Skill

## Trigger Conditions

Activate this skill when the user's message matches ANY of:
- "evaluate [category]"
- "compare [vendors/tools]"
- "recommend [category/vendor]"
- "find the best [category]"
- "which [category] should I use"
- "help me choose [category]"
- Any message requesting vendor/tool/platform comparison or selection

## Execution Instructions

When triggered:

### Step 1: Research DEEPLY — Do NOT just read homepages

For EACH candidate vendor, fetch these specific URLs (adapt org/repo names):

**GitHub (real data, not claims):**
- `https://api.github.com/repos/[org]/[sdk-repo]` → stars, forks, open_issues_count, pushed_at
- `https://api.github.com/repos/[org]/[sdk-repo]/contributors?per_page=5` → bus factor, top contributors
- `https://github.com/[org]/[sdk-repo]/releases` → last release date, release frequency

**Status & Reliability:**
- `https://status.[vendor].com` or `https://[vendor].statuspage.io` → incident history
- Search: `[vendor] outage incident 2025 2026 site:twitter.com OR site:reddit.com`

**Pricing (use India/region-specific URLs):**
- `https://[vendor].com/pricing` (check for geo-redirect — try `/in/pricing` or `/pricing-india`)
- Search: `[vendor] pricing MDR India 2025 2026 per transaction`
- **DO THE MATH**: Calculate actual monthly cost at user's stated volume, then at 3x and 10x

**Reviews & Sentiment:**
- Search: `[vendor] G2 reviews rating 2025`
- Search: `[vendor] review site:reddit.com`

**Compliance:**
- Search: `[vendor] PCI DSS SOC2 ISO 27001 certification`
- Search: `[vendor] RBI payment aggregator license` (for India payment gateways)

**Corporate Risk:**
- Search: `[vendor] acquisition merger funding 2025 2026`
- Search: `[vendor] layoffs restructuring 2025 2026`

**Tech Risk:**
- Search: `[vendor] API deprecation sunset changelog breaking changes`
- Check GitHub issues for `deprecated` or `breaking` labels

### Step 2: Follow the 4-phase process defined in SOUL.md exactly

### Step 3: Output ALL 8 sections described in SOUL.md — never skip any

### Step 4: Make BOLD weight adjustments
- Minimum 5 percentage point shifts per discovery
- At least 3 discoveries with real evidence chains
- Show the cascade effect: how one discovery changes which vendor wins

### Step 5: Check all 6 hidden risk categories for every vendor
- Use GitHub API data for maintainer health (not just "repo exists")
- Calculate pricing at 10x to find traps
- Check news for acquisitions

## Quality Checklist (Self-Verify Before Responding)

Before sending your response, verify:

- [ ] Context summary extracted correctly from query
- [ ] 3-5 candidates identified with rationale for each
- [ ] At least 3 discoveries shown with evidence → weight impact → triggered research
- [ ] Each weight shift is ≥5 percentage points (not just 2-3%)
- [ ] Weight table shows BOTH initial and final percentages that sum to 100%
- [ ] Comparison matrix has scores AND evidence in every cell (minimize N/A — try 2+ sources before giving up)
- [ ] Hidden risks section covers all 6 categories with specific evidence
- [ ] Cost projection table included (at current scale, 3x, and 10x)
- [ ] Recommendation has primary + backup + conditional alternatives
- [ ] Reproducibility section lists data sources and date
- [ ] Web search was used for real data (not guesses) — GitHub API, status pages, pricing pages fetched
- [ ] At least 8 web fetches were performed across all vendors

## Context-Awareness Requirement

**Different context MUST produce different output:**

"evaluate payment gateways for Indian startup" →
- Include Razorpay, Cashfree (India-specific)
- Weight UPI support, RBI compliance highly
- Check MDR in INR terms

"evaluate payment gateways for US enterprise" →
- Include Stripe, Adyen, Braintree
- Weight enterprise SLAs, global coverage
- Check volume pricing, PCI Level 1

"evaluate payment gateways for healthcare startup" →
- Weight HIPAA compliance, audit trails
- Check BAA availability
- Flag any vendor without healthcare compliance

The weight tables, scores, and recommendations MUST differ across these contexts.

## Error Handling

If you cannot find reliable data for a criterion:
- State explicitly: "Unable to verify [X] — recommend manual check before decision"
- Do NOT fabricate data
- Score as N/A and note the gap

If the query is too vague:
- Still perform the evaluation with reasonable assumptions
- List your assumptions explicitly in the Context section
- Note where more specificity would change the recommendation
