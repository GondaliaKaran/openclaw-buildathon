"""
Multi-Criteria Researcher Agent
Logic Layer Component (1 hr)

Performs deep investigation across multiple dimensions:
- Technical: SDK quality, API, integration complexity, performance
- Operational: Uptime, support, scalability
- Business: Pricing, vendor health, compliance
- Hidden Risks: Maintainer health, pricing traps, lock-in, acquisition, compliance, deprecation
"""

import logging
import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
from agents.candidate_identifier import Candidate
from agents.advanced_risk_detector import AdvancedRiskDetector
from config import config

logger = logging.getLogger(__name__)


@dataclass
class ResearchFindings:
    """Research findings for a single vendor."""
    vendor_name: str
    
    # Technical dimensions
    sdk_quality: Dict[str, any] = field(default_factory=dict)
    api_quality: Dict[str, any] = field(default_factory=dict)
    integration_complexity: Dict[str, any] = field(default_factory=dict)
    performance: Dict[str, any] = field(default_factory=dict)
    
    # Operational dimensions
    uptime_reliability: Dict[str, any] = field(default_factory=dict)
    support_quality: Dict[str, any] = field(default_factory=dict)
    scalability: Dict[str, any] = field(default_factory=dict)
    
    # Business dimensions
    pricing: Dict[str, any] = field(default_factory=dict)
    vendor_health: Dict[str, any] = field(default_factory=dict)
    compliance: Dict[str, any] = field(default_factory=dict)
    
    # Hidden risks
    hidden_risks: List[Dict[str, str]] = field(default_factory=list)
    
    # Metadata
    research_timestamp: datetime = field(default_factory=datetime.now)
    evidence_sources: List[str] = field(default_factory=list)


class MultiCriteriaResearcher:
    """Conducts deep multi-dimensional research on vendor candidates."""
    
    def __init__(self, clawhub_client, openai_client):
        """
        Initialize researcher.
        
        Args:
            clawhub_client: ClawHub integration for web search
            openai_client: OpenAI client for analysis
        """
        self.clawhub = clawhub_client
        self.openai = openai_client
        self.research_depth = config.agent.research_depth
        self.enable_hidden_risk_detection = config.agent.enable_hidden_risk_detection
        
        # Initialize advanced risk detector for bonus challenge
        self.risk_detector = AdvancedRiskDetector(clawhub_client, openai_client)
    
    async def research_candidates(
        self,
        candidates: List[Candidate],
        context: Dict[str, any]
    ) -> List[ResearchFindings]:
        """
        Research all candidates in parallel.
        
        Args:
            candidates: List of candidates to research
            context: Evaluation context
        
        Returns:
            List of ResearchFindings for each candidate
        """
        logger.info(f"Starting research on {len(candidates)} candidates")
        
        # Research candidates in parallel
        research_tasks = [
            self.research_single_candidate(candidate, context)
            for candidate in candidates
        ]
        
        findings_list = await asyncio.gather(*research_tasks)
        
        logger.info(f"Research completed for {len(findings_list)} candidates")
        return findings_list
    
    async def research_single_candidate(
        self,
        candidate: Candidate,
        context: Dict[str, any]
    ) -> ResearchFindings:
        """
        Research a single candidate across all dimensions.
        
        Args:
            candidate: Candidate to research
            context: Evaluation context
        
        Returns:
            ResearchFindings for this candidate
        """
        logger.info(f"Researching: {candidate.name}")
        
        findings = ResearchFindings(vendor_name=candidate.name)
        
        # Execute research in parallel across dimensions
        research_tasks = [
            self._research_technical_dimensions(candidate, context, findings),
            self._research_operational_dimensions(candidate, context, findings),
            self._research_business_dimensions(candidate, context, findings),
        ]
        
        # Add hidden risk detection if enabled
        if self.enable_hidden_risk_detection:
            research_tasks.append(
                self._detect_hidden_risks(candidate, context, findings)
            )
        
        await asyncio.gather(*research_tasks)
        
        logger.info(f"Research completed for {candidate.name}")
        return findings
    
    async def _research_technical_dimensions(
        self,
        candidate: Candidate,
        context: Dict[str, any],
        findings: ResearchFindings
    ):
        """Research technical aspects: SDK, API, integration, performance."""
        vendor_name = candidate.name
        tech_stack = context.get("tech_stack", [])
        
        # SDK Quality Research
        if candidate.github_url:
            findings.sdk_quality = await self._research_sdk_quality(
                candidate.github_url,
                tech_stack
            )
        else:
            # Search for GitHub repo
            github_search = await self.clawhub.web_search(
                f"{vendor_name} github repository",
                num_results=3
            )
            findings.sdk_quality = await self._analyze_sdk_from_search(
                github_search,
                tech_stack
            )
        
        # API Quality Research
        findings.api_quality = await self._research_api_quality(
            vendor_name,
            candidate.website
        )
        
        # Integration Complexity
        findings.integration_complexity = await self._research_integration_complexity(
            vendor_name,
            tech_stack
        )
        
        # Performance
        findings.performance = await self._research_performance(vendor_name)
    
    async def _research_operational_dimensions(
        self,
        candidate: Candidate,
        context: Dict[str, any],
        findings: ResearchFindings
    ):
        """Research operational aspects: uptime, support, scalability."""
        vendor_name = candidate.name
        
        # Uptime/Reliability Research
        findings.uptime_reliability = await self._research_uptime(vendor_name)
        
        # Support Quality
        findings.support_quality = await self._research_support(vendor_name)
        
        # Scalability
        scale = context.get("scale", "")
        findings.scalability = await self._research_scalability(vendor_name, scale)
    
    async def _research_business_dimensions(
        self,
        candidate: Candidate,
        context: Dict[str, any],
        findings: ResearchFindings
    ):
        """Research business aspects: pricing, vendor health, compliance."""
        vendor_name = candidate.name
        
        # Pricing Research
        findings.pricing = await self._research_pricing(
            vendor_name,
            candidate.website
        )
        
        # Vendor Health
        findings.vendor_health = await self._research_vendor_health(vendor_name)
        
        # Compliance
        compliance_reqs = context.get("compliance", [])
        findings.compliance = await self._research_compliance(
            vendor_name,
            compliance_reqs
        )
    
    async def _detect_hidden_risks(
        self,
        candidate: Candidate,
        con
        Detect hidden risks using both basic and advanced detection.
        
        Detects 8 types of hidden risks for bonus challenge:
        1. GitHub maintainer health (commit patterns, bus factor)
        2. Pricing explosions at scale
        3. Vendor lock-in risks
        4. Recent acquisitions/mergers
        5. Compliance drift/expiry
        6. Technology deprecation
        7. Community health decline
        8. Support degradation
        """
        vendor_name = candidate.name
        risks = []
        
        # Run all risk detection in parallel for speed
        risk_tasks = []
        
        # 1. GitHub Maintainer Risk (Advanced)
        if candidate.github_url:
            risk_tasks.append(
                self.risk_detector.detect_github_maintainer_risks(candidate.github_url)
            )
        
        # 2. Pricing Explosion Risk (Advanced)
        risk_tasks.append(
            self.risk_detector.detect_scaling_pricing_risks(vendor_name, context)
        )
        
        # 3. Acquisition Risk (Advanced)
        risk_tasks.append(
            self.risk_detector.detect_acquisition_risks(vendor_name)
        )
        
        # 4. Compliance Drift Risk (Advanced)
        compliance_reqs = context.get('compliance', [])
        if compliance_reqs:
            risk_tasks.append(
                self.risk_detector.detect_compliance_drift_risks(vendor_name, compliance_reqs)
            )
        
        # 5. Technology Deprecation Risk (Advanced)
        tech_stack = context.get('tech_stack', [])
        risk_tasks.append(
            self.risk_detector.detect_technology_deprecation_risks(vendor_name, tech_stack)
        )
        
        # 6. Basic Lock-in Risk (fallback)
        risk_tasks.append(
            self._detect_lockin_risk(vendor_name)
        )
        
        # Execute all risk detections in parallel
        risk_results = await asyncio.gather(*risk_tasks, return_exceptions=True)
        
        # Flatten results and filter out exceptions/None
        for result in risk_results:
            if isinstance(result, list):
                risks.extend(result)
            elif isinstance(result, dict) and result:
                risks.append(result)
            elif isinstance(result, Exception):
                logger.warning(f"Risk detection failed: {result}")
        
        logger.info(f"Detected {len(risks)} hidden risks for {vendor_name}")lockin_risk = await self._detect_lockin_risk(vendor_name)
        if lockin_risk:
            risks.append(lockin_risk)
        
        findings.hidden_risks = risks
    
    # ==================== Individual Research Methods ====================
    
    async def _research_sdk_quality(
        self,
        github_url: str,
        tech_stack: List[str]
    ) -> Dict[str, any]:
        """Research SDK quality from GitHub."""
        # Search for GitHub metrics
        search_query = f"{github_url} stars issues pull requests"
        results = await self.clawhub.web_search(search_query, num_results=5)
        
        # Use AI to analyze results
        analysis = await self._ai_analyze(
            f"Analyze SDK quality for {github_url}",
            f"Tech stack requirements: {tech_stack}",
            results
        )
        
        return {
            "github_url": github_url,
            "analysis": analysis,
            "tech_stack_support": self._check_tech_stack_support(analysis, tech_stack)
        }
    
    async def _analyze_sdk_from_search(
        self,
        search_results: List[Dict],
        tech_stack: List[str]
    ) -> Dict[str, any]:
        """Analyze SDK when GitHub URL not directly available."""
        analysis = await self._ai_analyze(
            "Analyze SDK availability and quality",
            f"Tech stack: {tech_stack}",
            search_results
        )
        
        return {
            "analysis": analysis,
            "tech_stack_support": self._check_tech_stack_support(analysis, tech_stack)
        }
    
    async def _research_api_quality(
        self,
        vendor_name: str,
        website: Optional[str]
    ) -> Dict[str, any]:
        """Research API quality and documentation."""
        search_query = f"{vendor_name} API documentation quality review"
        results = await self.clawhub.web_search(search_query, num_results=5)
        
        analysis = await self._ai_analyze(
            f"Analyze API quality for {vendor_name}",
            "Consider: documentation, ease of use, community feedback",
            results
        )
        
        return {"analysis": analysis}
    
    async def _research_integration_complexity(
        self,
        vendor_name: str,
        tech_stack: List[str]
    ) -> Dict[str, any]:
        """Research integration complexity."""
        tech_str = " ".join(tech_stack[:2]) if tech_stack else ""
        search_query = f"{vendor_name} integration {tech_str} difficulty time"
        results = await self.clawhub.web_search(search_query, num_results=5)
        
        analysis = await self._ai_analyze(
            f"Analyze integration complexity for {vendor_name}",
            f"Tech stack: {tech_stack}",
            results
        )
        
        return {"analysis": analysis}
    
    async def _research_performance(self, vendor_name: str) -> Dict[str, any]:
        """Research performance benchmarks."""
        search_query = f"{vendor_name} performance benchmark latency throughput"
        results = await self.clawhub.web_search(search_query, num_results=5)
        
        analysis = await self._ai_analyze(
            f"Analyze performance for {vendor_name}",
            "Look for: latency, throughput, reliability metrics",
            results
        )
        
        return {"analysis": analysis}
    
    async def _research_uptime(self, vendor_name: str) -> Dict[str, any]:
        """Research uptime and reliability history."""
        search_query = f"{vendor_name} status page uptime history incidents outages"
        results = await self.clawhub.web_search(search_query, num_results=5)
        
        analysis = await self._ai_analyze(
            f"Analyze uptime history for {vendor_name}",
            "Focus on: recent incidents, frequency, duration, SLA",
            results
        )
        
        return {"analysis": analysis}
    
    async def _research_support(self, vendor_name: str) -> Dict[str, any]:
        """Research support quality."""
        search_query = f"{vendor_name} customer support quality response time reviews"
        results = await self.clawhub.web_search(search_query, num_results=5)
        
        analysis = await self._ai_analyze(
            f"Analyze support quality for {vendor_name}",
            "Consider: response time, support channels, user reviews",
            results
        )
        
        return {"analysis": analysis}
    
    async def _research_scalability(
        self,
        vendor_name: str,
        scale: str
    ) -> Dict[str, any]:
        """Research scalability limits and performance at scale."""
        search_query = f"{vendor_name} scalability limits {scale} enterprise"
        results = await self.clawhub.web_search(search_query, num_results=5)
        
        analysis = await self._ai_analyze(
            f"Analyze scalability for {vendor_name}",
            f"Target scale: {scale}",
            results
        )
        
        return {"analysis": analysis}
    
    async def _research_pricing(
        self,
        vendor_name: str,
        website: Optional[str]
    ) -> Dict[str, any]:
        """Research pricing structure and hidden costs."""
        search_query = f"{vendor_name} pricing costs tiers hidden fees"
        results = await self.clawhub.web_search(search_query, num_results=5)
        
        analysis = await self._ai_analyze(
            f"Analyze pricing for {vendor_name}",
            "Look for: base cost, usage tiers, hidden fees, cost at scale",
            results
        )
        
        return {"analysis": analysis}
    
    async def _research_vendor_health(self, vendor_name: str) -> Dict[str, any]:
        """Research vendor financial health and stability."""
        search_query = f"{vendor_name} company funding employees growth news"
        results = await self.clawhub.web_search(search_query, num_results=5)
        
        analysis = await self._ai_analyze(
            f"Analyze vendor health for {vendor_name}",
            "Consider: funding, team size, growth trajectory, recent news",
            results
        )
        
        return {"analysis": analysis}
    
    async def _research_compliance(
        self,
        vendor_name: str,
        compliance_reqs: List[str]
    ) -> Dict[str, any]:
        """Research compliance certifications."""
        comp_str = " ".join(compliance_reqs) if compliance_reqs else "compliance"
        search_query = f"{vendor_name} {comp_str} certification audit"
        results = await self.clawhub.web_search(search_query, num_results=5)
        
        analysis = await self._ai_analyze(
            f"Analyze compliance for {vendor_name}",
            f"Required: {compliance_reqs}",
            results
        )
        
        return {
            "analysis": analysis,
            "required": compliance_reqs
        }
    
    # ==================== Hidden Risk Detection ====================
    
    async def _detect_maintainer_risk(self, github_url: str) -> Optional[Dict[str, str]]:
        """Detect maintainer churn or bus factor risk."""
        search_query = f"{github_url} contributors commits activity maintainers"
        results = await self.clawhub.web_search(search_query, num_results=5)
        
        analysis = await self._ai_analyze(
            "Detect maintainer risks",
            "Look for: contributor churn, single maintainer, decreased activity",
            results
        )
        
        # Check if risk detected
        if "risk" in analysis.lower() or "concern" in analysis.lower():
            return {
                "type": "maintainer_health",
                "severity": "medium",
                "description": analysis,
                "evidence": github_url
            }
        
        return None
    
    async def _detect_pricing_traps(
        self,
        vendor_name: str,
        pricing_info: Dict[str, any]
    ) -> Optional[Dict[str, str]]:
        """Detect pricing traps (sudden jumps at scale)."""
        analysis = pricing_info.get("analysis", "")
        
        # Look for keywords indicating pricing traps
        trap_keywords = ["sudden", "jump", "expensive at scale", "hidden fee", "surprise"]
        
        if any(keyword in analysis.lower() for keyword in trap_keywords):
            return {
                "type": "pricing_trap",
                "severity": "medium",
                "description": f"Potential pricing trap detected for {vendor_name}",
                "evidence": analysis[:200]
            }
        
        return None
    
    async def _detect_lockin_risk(self, vendor_name: str) -> Optional[Dict[str, str]]:
        """Detect vendor lock-in risks."""
        search_query = f"{vendor_name} migration export data portability lock-in"
        results = await self.clawhub.web_search(search_query, num_results=5)
        
        analysis = await self._ai_analyze(
            f"Assess lock-in risk for {vendor_name}",
            "Consider: data export, migration difficulty, proprietary formats",
            results
        )
        
        if "lock-in" in analysis.lower() or "difficult to migrate" in analysis.lower():
            return {
                "type": "vendor_lockin",
                "severity": "low",
                "description": analysis,
                "evidence": "Migration difficulty reported"
            }
        
        return None
    
    # ==================== Helper Methods ====================
    
    async def _ai_analyze(
        self,
        task: str,
        context: str,
        search_results: List[Dict]
    ) -> str:
        """Use AI to analyze search results."""
        # Format search results
        results_text = "\n\n".join([
            f"Source: {r.get('title', 'N/A')}\n{r.get('snippet', 'N/A')}"
            for r in search_results[:10]
        ])
        
        prompt = f"""Task: {task}

Context: {context}

Search Results:
{results_text}

Provide a concise analysis (2-3 sentences) with specific evidence. If data is insufficient, state that clearly.
"""
        
        response = await self.openai.chat_completion(
            messages=[
                {"role": "system", "content": "You are analyzing vendor research data. Be specific and evidence-based."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )
        
        return response
    
    def _check_tech_stack_support(
        self,
        analysis: str,
        tech_stack: List[str]
    ) -> Dict[str, bool]:
        """Check which tech stack items are supported."""
        support_map = {}
        
        for tech in tech_stack:
            # Simple keyword matching
            supported = tech.lower() in analysis.lower()
            support_map[tech] = supported
        
        return support_map
