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

### ⚠️ CRITICAL ANTI-BIAS RULE ⚠️

**Research ALL candidates with EQUAL DEPTH before scoring.**

❌ **BAD**: Research Vendor A deeply (10 URLs) → score 9/10 with evidence. Then fill Vendor B, C, D with "N/A — not pulled" and guess 7/10.

✅ **GOOD**: Research Vendor A (10 URLs), Vendor B (10 URLs), Vendor C (10 URLs), Vendor D (10 URLs). THEN compare fairly.

If you find yourself writing "not pulled" or "not validated here" for ANY vendor on ANY criterion, STOP and go fetch the data. The comparison must be fair.

### Step 1: Research DEEPLY — Do NOT just read homepages

**CRITICAL RULE: Research ALL candidates with EQUAL DEPTH before scoring. Do NOT research only the winner deeply and fill others with N/A.**

For EACH candidate vendor, fetch these specific URLs (adapt org/repo names):

**GitHub (real data, not claims):**
- `https://api.github.com/repos/[org]/[sdk-repo]` → stars, forks, open_issues_count, pushed_at
- `https://api.github.com/repos/[org]/[sdk-repo]/contributors?per_page=5` → bus factor, top contributors
- `https://github.com/[org]/[sdk-repo]/releases` → last release date, release frequency

**Status & Reliability:**
- `https://status.[vendor].com` or `https://[vendor].statuspage.io` → incident history
- `https://www.cloudflarestatus.com/api/v2/components.json` (for Cloudflare, filter by vendor name)
- Search: `[vendor] outage incident 2025 2026 site:twitter.com OR site:reddit.com`

**Compliance & Security:**
- `https://[vendor].com/security` or `https://[vendor].com/compliance` → certifications page
- `https://docs.[vendor].com/security` → security documentation
- Search: `[vendor] PCI DSS SOC2 ISO 27001 certification 2025`
- Search: `[vendor] RBI payment aggregator license` (for India payment gateways)

**Pricing (use India/region-specific URLs):**
- `https://[vendor].com/pricing` (check for geo-redirect — try `/in/pricing` or `/pricing-india`)
- Search: `[vendor] pricing MDR India 2025 2026 per transaction`
- **DO THE MATH**: Calculate actual monthly cost at user's stated volume, then at 3x and 10x

**Reviews & Sentiment:**
- Search: `[vendor] G2 reviews rating 2025`
- Search: `[vendor] review site:reddit.com`

**Corporate Risk:**
- Search: `[vendor] acquisition merger funding 2025 2026`
- Search: `[vendor] layoffs restructuring 2025 2026`

**Tech Risk:**
- Search: `[vendor] API deprecation sunset changelog breaking changes`
- Check GitHub issues for `deprecated` or `breaking` labels

**RESEARCH CHECKLIST (verify for EACH vendor before moving to scoring):**
- [ ] Checked at least 2 compliance/security URLs (docs site + marketing page)
- [ ] Checked status page or incident history (try main site, StatusPage.io, Twitter)
- [ ] Checked pricing page (main + region-specific if applicable)
- [ ] Checked GitHub repo data (API endpoint, not just homepage)

If after trying 2+ sources you STILL can't find data, then mark N/A with explanation: "Unable to verify after checking [source 1], [source 2] — recommend manual verification"

**NEVER write "not pulled" — if you didn't pull it, GO FETCH IT NOW.**

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
- [ ] **EQUAL RESEARCH DEPTH**: Every candidate has 2+ URLs checked for each criterion (not just the winner)
- [ ] At least 3 discoveries shown with evidence → weight impact → triggered research
- [ ] Each weight shift is ≥5 percentage points (not just 2-3%)
- [ ] Weight table shows BOTH initial and final percentages that sum to 100%
- [ ] **Comparison matrix**: Scores AND evidence in every cell for EVERY vendor
  - ❌ REJECT any cell that says "not pulled" or "not validated" — GO FETCH THE DATA
  - ✅ ACCEPT N/A only if you tried 2+ sources and explain what you tried
  - Example of ACCEPTABLE N/A: "7/10 — Unable to verify PCI cert after checking docs.vendor.com/security (404) and searching 'vendor PCI DSS 2025' (no results)"
  - Example of UNACCEPTABLE N/A: "N/A (7/10) — not pulled compliance docs here" ← THIS MEANS YOU WERE LAZY
- [ ] Hidden risks section covers all 6 categories with specific evidence for ALL vendors
- [ ] Cost projection table included (at current scale, 3x, and 10x) with MATH SHOWN
- [ ] Recommendation has primary + backup + conditional alternatives
- [ ] Reproducibility section lists data sources and date
- [ ] **At least 8 web fetches PER VENDOR** (not total across all vendors)
- [ ] If a vendor scores below 6/10 on any criterion, the evidence must explain WHY (with URL proof)

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
