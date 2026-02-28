"""
Advanced Hidden Risk Detector
Enhanced risk detection for bonus challenge
"""

import logging
import re
from typing import Dict, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AdvancedRiskDetector:
    """Advanced risk detection for vendors."""
    
    def __init__(self, clawhub_client, openai_client):
        self.clawhub = clawhub_client
        self.openai = openai_client
    
    async def detect_github_maintainer_risks(self, github_url: str) -> List[Dict]:
        """
        Detect maintainer risks from GitHub activity patterns.
        
        Checks:
        - Commit frequency decline
        - Key contributor departures
        - Unmerged critical PRs
        - Issue response time degradation
        """
        risks = []
        
        # Search for recent activity
        search_query = f"{github_url} commits contributors activity last 6 months"
        results = await self.clawhub.web_search(search_query, num_results=10)
        
        analysis_prompt = f"""Analyze GitHub activity patterns for: {github_url}

Search Results: {self._format_results(results)}

Detect these HIDDEN RISKS:
1. **Commit Frequency Decline**: Has daily commits dropped to weekly/monthly?
2. **Key Contributor Loss**: Any maintainers with 1000+ commits stopped contributing?
3. **Stale PRs**: Are critical pull requests sitting unmerged for months?
4. **Issue Backlog**: Is issue count growing with slower response times?
5. **Fork Activity**: Are there active forks suggesting maintainer abandonment?

Format: If risk found, output:
RISK: [type]
SEVERITY: [high/medium/low]
EVIDENCE: [specific data points]
IMPACT: [what this means for users]

If no clear risk, output: NO_RISK"""
        
        response = await self.openai.chat_completion(
            messages=[
                {"role": "system", "content": "You are a GitHub health analyst. Be specific with evidence."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.2,
            max_tokens=400
        )
        
        # Parse AI response
        if "NO_RISK" not in response:
            risk = self._parse_risk_response(response, "github_maintainer")
            if risk:
                risks.append(risk)
        
        return risks
    
    async def detect_scaling_pricing_risks(
        self,
        vendor_name: str,
        current_context: Dict
    ) -> List[Dict]:
        """
        Detect pricing that explodes at scale.
        
        Checks:
        - Exponential cost growth patterns
        - Hidden per-operation fees
        - Volume discount cliffs
        - "Contact sales" thresholds
        """
        risks = []
        
        # Extract scale indicators from context
        scale_hint = current_context.get('scale', 'startup')
        
        search_query = f"{vendor_name} pricing calculator cost at scale enterprise pricing"
        results = await self.clawhub.web_search(search_query, num_results=10)
        
        analysis_prompt = f"""Analyze pricing structure for: {vendor_name}

User Context: {scale_hint}
Search Results: {self._format_results(results)}

Detect PRICING EXPLOSION RISKS:
1. **Non-linear Scaling**: Does cost grow faster than usage? (e.g., 10x users = 50x cost)
2. **Hidden Op Fees**: Per-API-call, per-transaction fees that multiply at scale?
3. **Discount Cliffs**: Does friendly SMB pricing vanish at enterprise tier?
4. **Threshold Traps**: "Contact sales" at volumes reachable in 6-12 months?
5. **Bandwidth/Storage**: Are overage fees disproportionately expensive?

Example of REAL risk:
- Auth0: $0.023/MAU looks cheap, but 1M users = $23k/month
- Stripe: 2.9% is fine until high volume, then per-transaction adds up

Format: If risk found:
RISK: pricing_explosion
SEVERITY: [high/medium/low]
EVIDENCE: [specific pricing tier data]
IMPACT: [cost projection at user's scale]

If pricing is transparent and scales reasonably: NO_RISK"""
        
        response = await self.openai.chat_completion(
            messages=[
                {"role": "system", "content": "You are a SaaS pricing analyst. Focus on hidden costs."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.2,
            max_tokens=400
        )
        
        if "NO_RISK" not in response:
            risk = self._parse_risk_response(response, "pricing_explosion")
            if risk:
                risks.append(risk)
        
        return risks
    
    async def detect_acquisition_risks(self, vendor_name: str) -> List[Dict]:
        """
        Detect recent acquisition/merger risks.
        
        Checks:
        - Recent acquisitions (< 12 months)
        - Integration disruptions
        - Pricing changes post-acquisition
        - Feature deprecations
        """
        risks = []
        
        search_query = f"{vendor_name} acquisition merger acquired bought {datetime.now().year}"
        results = await self.clawhub.web_search(search_query, num_results=10)
        
        analysis_prompt = f"""Check acquisition status for: {vendor_name}

Search Results: {self._format_results(results)}

Detect ACQUISITION RISKS:
1. **Recent Acquisition**: Was company acquired in last 12 months?
2. **Integration Chaos**: Reports of service disruption, breaking changes?
3. **Pricing Increases**: Sudden price hikes post-acquisition?
4. **Feature Sunset**: Deprecated features, forced migrations?
5. **Support Degradation**: Slower support, reduced documentation?

Format: If risk found:
RISK: acquisition_disruption
SEVERITY: [high/medium/low]
EVIDENCE: [who acquired, when, what changed]
IMPACT: [how this affects current users]

If no recent acquisition or stable integration: NO_RISK"""
        
        response = await self.openai.chat_completion(
            messages=[
                {"role": "system", "content": "You are M&A analyst focusing on customer impact."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.2,
            max_tokens=400
        )
        
        if "NO_RISK" not in response:
            risk = self._parse_risk_response(response, "acquisition")
            if risk:
                risks.append(risk)
        
        return risks
    
    async def detect_compliance_drift_risks(
        self,
        vendor_name: str,
        required_compliance: List[str]
    ) -> List[Dict]:
        """
        Detect compliance certification expiry or loss.
        
        Checks:
        - Expired certifications
        - Failed audits
        - Removed compliance badges
        - Regional license issues
        """
        risks = []
        
        if not required_compliance:
            return risks
        
        compliance_str = ", ".join(required_compliance)
        search_query = f"{vendor_name} {compliance_str} certification audit status {datetime.now().year}"
        results = await self.clawhub.web_search(search_query, num_results=10)
        
        analysis_prompt = f"""Check compliance status for: {vendor_name}

Required Compliance: {compliance_str}
Search Results: {self._format_results(results)}

Detect COMPLIANCE RISKS:
1. **Expired Certs**: Are certifications current or expired?
2. **Failed Audits**: Any failed SOC 2, ISO, HIPAA audits?
3. **Regional Issues**: Lost licenses in specific regions?
4. **Pending Renewals**: Certifications up for renewal soon?

Format: If risk found:
RISK: compliance_drift
SEVERITY: [high/medium/low]
EVIDENCE: [which cert, status, date]
IMPACT: [legal/regulatory implications]

If all compliances current and valid: NO_RISK"""
        
        response = await self.openai.chat_completion(
            messages=[
                {"role": "system", "content": "You are compliance auditor. Be precise with dates."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.2,
            max_tokens=400
        )
        
        if "NO_RISK" not in response:
            risk = self._parse_risk_response(response, "compliance")
            if risk:
                risks.append(risk)
        
        return risks
    
    async def detect_technology_deprecation_risks(
        self,
        vendor_name: str,
        tech_stack: List[str]
    ) -> List[Dict]:
        """
        Detect deprecated APIs or forced migrations.
        
        Checks:
        - API version sunsets
        - SDK deprecations
        - Breaking changes announced
        - Migration deadlines
        """
        risks = []
        
        tech_str = ", ".join(tech_stack[:3]) if tech_stack else ""
        search_query = f"{vendor_name} deprecated sunset breaking changes API {tech_str}"
        results = await self.clawhub.web_search(search_query, num_results=10)
        
        analysis_prompt = f"""Check for deprecation risks: {vendor_name}

Tech Stack: {tech_str}
Search Results: {self._format_results(results)}

Detect DEPRECATION RISKS:
1. **API Sunsets**: Are current APIs being deprecated?
2. **Forced Migration**: Mandatory version upgrades with breaking changes?
3. **Short Timelines**: Less than 6 months to migrate?
4. **SDK Abandonment**: Official SDKs no longer maintained?

Format: If risk found:
RISK: technology_deprecation
SEVERITY: [high/medium/low]
EVIDENCE: [what's deprecated, deadline]
IMPACT: [migration effort required]

If no imminent deprecations: NO_RISK"""
        
        response = await self.openai.chat_completion(
            messages=[
                {"role": "system", "content": "You are technical migration analyst."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.2,
            max_tokens=400
        )
        
        if "NO_RISK" not in response:
            risk = self._parse_risk_response(response, "deprecation")
            if risk:
                risks.append(risk)
        
        return risks
    
    # Helper methods
    
    def _format_results(self, results: List[Dict]) -> str:
        """Format search results for AI analysis."""
        return "\n\n".join([
            f"- {r.get('title', 'N/A')}: {r.get('snippet', 'N/A')}"
            for r in results[:8]
        ])
    
    def _parse_risk_response(self, response: str, risk_category: str) -> Optional[Dict]:
        """Parse AI response into structured risk."""
        lines = response.strip().split('\n')
        
        risk_data = {
            "category": risk_category,
            "type": "",
            "severity": "medium",
            "description": "",
            "evidence": "",
            "impact": ""
        }
        
        for line in lines:
            line = line.strip()
            if line.startswith("RISK:"):
                risk_data["type"] = line.replace("RISK:", "").strip()
            elif line.startswith("SEVERITY:"):
                risk_data["severity"] = line.replace("SEVERITY:", "").strip()
            elif line.startswith("EVIDENCE:"):
                risk_data["evidence"] = line.replace("EVIDENCE:", "").strip()
            elif line.startswith("IMPACT:"):
                risk_data["impact"] = line.replace("IMPACT:", "").strip()
            elif not line.startswith(("RISK:", "SEVERITY:", "EVIDENCE:", "IMPACT:")):
                # Accumulate description
                risk_data["description"] += line + " "
        
        # Validate we got meaningful data
        if risk_data["type"] and (risk_data["evidence"] or risk_data["description"]):
            return risk_data
        
        return None
