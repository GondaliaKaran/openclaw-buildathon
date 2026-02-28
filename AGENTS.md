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

1. **Use web search extensively** — search for real data on each vendor:
   - `[vendor] GitHub stars contributors issues` — for code health
   - `[vendor] status page uptime incidents 2025 2026` — for reliability
   - `[vendor] pricing calculator cost per transaction` — for pricing analysis
   - `[vendor] G2 reviews rating` — for user sentiment
   - `[vendor] PCI DSS SOC2 compliance certification` — for compliance
   - `[vendor] acquisition merger news` — for corporate risk
   - `[vendor] API deprecation sunset changelog` — for tech risk

2. **Follow the 4-phase process** defined in SOUL.md exactly
3. **Output ALL 8 sections** described in SOUL.md — never skip any
4. **Show at least 3 weight adjustments** with evidence chains
5. **Check all 6 hidden risk categories** for every vendor

## Quality Checklist (Self-Verify Before Responding)

Before sending your response, verify:

- [ ] Context summary extracted correctly from query
- [ ] 3-5 candidates identified with rationale for each
- [ ] At least 3 discoveries shown with evidence → weight impact → triggered research
- [ ] Weight table shows BOTH initial and final percentages
- [ ] Comparison matrix has scores AND evidence in every cell
- [ ] Hidden risks section covers all 6 categories
- [ ] Recommendation has primary + backup + conditional alternatives
- [ ] Reproducibility section lists data sources and date
- [ ] Web search was used for real data (not guesses)

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
