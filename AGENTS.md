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

For EACH candidate vendor, gather data across these dimensions. **Adapt your research strategy** — if one URL pattern doesn't work, try alternatives:

---

**1. TECHNICAL HEALTH (GitHub, SDKs, Documentation)**

What you need: Repository activity, maintainer health, SDK quality, community engagement

How to find it:
- Try GitHub API: `https://api.github.com/repos/[org]/[repo-name]` → stars, forks, open issues, last push
- Try contributors API: `https://api.github.com/repos/[org]/[repo-name]/contributors` → bus factor
- If no GitHub, search: `[vendor] SDK github npm pypi repository`
- Check docs site: `https://docs.[vendor].com` or `https://[vendor].com/docs`
- If blocked, search: `[vendor] API documentation quality review`

---

**2. RELIABILITY & UPTIME (Status Pages, Incident History)**

What you need: Recent incidents, planned maintenance, uptime %, SLA claims

How to find it:
- Try common status page patterns: `status.[vendor].com`, `[vendor].statuspage.io`, `[vendor].com/status`
- Try status page APIs: `[status-url]/api/v2/summary.json`, `[status-url]/api/v2/incidents.json`
- If no status page, search: `[vendor] outage incident 2025 2026 site:twitter.com`
- Check vendor blog: `[vendor].com/blog` for "incident" or "postmortem"
- Search: `[vendor] downtime reliability uptime 2025`

---

**3. COMPLIANCE & SECURITY (Certifications, Audit Reports)**

What you need: PCI DSS, SOC2, ISO 27001, HIPAA BAA, GDPR, region-specific (RBI in India, etc.)

How to find it:
- Try security pages: `[vendor].com/security`, `[vendor].com/compliance`, `[vendor].com/trust`
- Try docs: `docs.[vendor].com/security`, `docs.[vendor].com/compliance`
- Search: `[vendor] PCI DSS SOC2 ISO 27001 certification 2025 2026`
- For India payments: `[vendor] RBI payment aggregator license`
- For healthcare: `[vendor] HIPAA BAA business associate agreement`
- If blocked, search: `[vendor] compliance certifications audit reports`

---

**4. PRICING & COST STRUCTURE (Avoid Traps)**

What you need: Base pricing, volume tiers, regional pricing, hidden fees, scale cliffs

How to find it:
- Try pricing pages: `[vendor].com/pricing`, `[vendor].com/pricing-[region]` (e.g., `/in/pricing`, `/pricing-india`)
- Try docs: `docs.[vendor].com/pricing`
- Search: `[vendor] pricing [region] [metric] 2025 2026` (e.g., "razorpay pricing india MDR 2025")
- **DO THE MATH**: Calculate cost at user's volume, 3×, and 10× to find non-linear jumps
- Look for: setup fees, monthly minimums, request fees, bandwidth fees, support tiers

---

**5. USER SENTIMENT & REVIEWS (Real Experiences)**

What you need: Recent reviews, common complaints, satisfaction scores

How to find it:
- Search: `[vendor] G2 reviews 2025`
- Search: `[vendor] capterra reviews 2025`
- Search: `[vendor] review site:reddit.com`
- Search: `"[vendor]" review problems issues site:news.ycombinator.com`
- Look for patterns: setup complexity, support quality, surprise fees, migration difficulty

---

**6. CORPORATE STABILITY & RISK (Acquisitions, Layoffs, Strategy)**

What you need: Recent funding, acquisitions, ownership changes, layoffs, product shutdowns

How to find it:
- Search: `[vendor] acquisition merger 2025 2026`
- Search: `[vendor] funding series round 2025 2026`
- Search: `[vendor] layoffs restructuring 2025 2026`
- Check: `[vendor].com/about`, `[vendor].com/newsroom`, `[vendor].com/blog`
- Look for: new CEO, pivot announcements, sunset notices

---

**7. TECHNOLOGY RISK (Deprecation, Breaking Changes, Lock-in)**

What you need: API versioning policy, deprecation notices, migration paths, data portability

How to find it:
- Search: `[vendor] API deprecation sunset changelog`
- Check docs: `docs.[vendor].com/changelog`, `[vendor].com/changelog`
- Search GitHub issues: `repo:[org]/[repo] label:deprecated OR label:breaking`
- Check: migration guides, export APIs, data portability
- Look for: proprietary formats, vendor-specific features that create lock-in

---

**RESEARCH CHECKLIST (verify for EACH vendor before moving to scoring):**
- [ ] Attempted 2+ different URL patterns or search strategies per dimension
- [ ] If primary data source failed (403, 404, no results), tried alternative approach
- [ ] Documented what you tried when data unavailable
- [ ] Compared apples-to-apples across all vendors (same metrics, same time period)

**ACCEPTABLE N/A format:**
`7/10 — Unable to verify after checking [vendor].com/security (404), docs.[vendor].com/compliance (no cert page), searching "[vendor] PCI DSS 2025" (no results) — recommend manual verification`

**UNACCEPTABLE N/A format:**
`N/A (7/10) — not pulled here` ← LAZY, GO RESEARCH IT

If you write "not pulled", "not validated", or "not checked" for ANY vendor on ANY criterion, STOP and go fetch the data using alternative strategies above.

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
