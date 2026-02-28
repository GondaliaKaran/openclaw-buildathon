"""
Dynamic Weight Adjuster Agent
Logic Layer Component (45 min)

Adaptively adjusts evaluation criteria weights based on discoveries during research.
This is what makes the evaluation truly intelligent - not a static comparison matrix.

Key principle: Discoveries during research should reshape what matters.
Examples:
- Finding major outages → increase uptime weight
- Missing SDK → increase integration complexity weight
- Pricing jump at scale → increase pricing transparency weight
"""

import logging
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from agents.researcher import ResearchFindings
from config import config

logger = logging.getLogger(__name__)


@dataclass
class CriterionWeight:
    """Represents a single evaluation criterion with its weight."""
    name: str
    initial_weight: float
    current_weight: float
    adjustment_reason: str = ""
    triggered_by: List[str] = field(default_factory=list)  # Which discoveries triggered adjustments


@dataclass
class WeightAdjustment:
    """Represents a single weight adjustment event."""
    criterion: str
    discovery: str
    evidence: str
    weight_before: float
    weight_after: float
    additional_research_triggered: List[str] = field(default_factory=list)


class DynamicWeightAdjuster:
    """Dynamically adjusts evaluation criteria weights based on research discoveries."""
    
    def __init__(self, openai_client):
        """
        Initialize weight adjuster.
        
        Args:
            openai_client: OpenAI client for intelligent weight adjustment
        """
        self.openai = openai_client
        self.enable_dynamic_weighting = config.agent.enable_dynamic_weighting
    
    def get_initial_weights(self, context: Dict[str, any]) -> Dict[str, CriterionWeight]:
        """
        Get initial evaluation criteria weights based on context.
        
        Args:
            context: Evaluation context (priorities, domain, etc.)
        
        Returns:
            Dictionary of criterion name -> CriterionWeight
        """
        # Default weights (balanced)
        default_weights = {
            "sdk_quality": 15.0,
            "api_quality": 10.0,
            "integration_complexity": 15.0,
            "performance": 10.0,
            "uptime_reliability": 15.0,
            "support_quality": 10.0,
            "scalability": 10.0,
            "pricing": 10.0,
            "vendor_health": 5.0,
            "compliance": 0.0  # Will be adjusted if compliance requirements exist
        }
        
        # Adjust initial weights based on context
        priorities = context.get("priorities", [])
        compliance_reqs = context.get("compliance", [])
        domain = context.get("domain", "")
        
        # If compliance requirements exist, allocate weight
        if compliance_reqs:
            default_weights["compliance"] = 15.0
            # Reduce other weights proportionally
            total_other = sum(v for k, v in default_weights.items() if k != "compliance")
            factor = (100 - default_weights["compliance"]) / total_other
            for key in default_weights:
                if key != "compliance":
                    default_weights[key] *= factor
        
        # Adjust based on stated priorities
        if "security" in str(priorities).lower() or "fintech" in domain.lower():
            default_weights["compliance"] += 5.0
            default_weights["uptime_reliability"] += 5.0
            default_weights["vendor_health"] += 3.0
            # Normalize
            total = sum(default_weights.values())
            default_weights = {k: (v / total) * 100 for k, v in default_weights.items()}
        
        # Convert to CriterionWeight objects
        weights = {
            name: CriterionWeight(
                name=name,
                initial_weight=weight,
                current_weight=weight
            )
            for name, weight in default_weights.items()
        }
        
        logger.info(f"Initial weights: {self._format_weights(weights)}")
        return weights
    
    async def adjust_weights(
        self,
        initial_weights: Dict[str, CriterionWeight],
        research_findings: List[ResearchFindings],
        context: Dict[str, any]
    ) -> Tuple[Dict[str, CriterionWeight], List[WeightAdjustment]]:
        """
        Adjust weights based on research findings.
        
        Args:
            initial_weights: Initial criterion weights
            research_findings: Research findings for all candidates
            context: Evaluation context
        
        Returns:
            Tuple of (adjusted_weights, list_of_adjustments)
        """
        if not self.enable_dynamic_weighting:
            logger.info("Dynamic weighting disabled, using initial weights")
            return initial_weights, []
        
        logger.info("Starting dynamic weight adjustment")
        
        # Make a copy of initial weights
        current_weights = {k: CriterionWeight(
            name=v.name,
            initial_weight=v.initial_weight,
            current_weight=v.current_weight
        ) for k, v in initial_weights.items()}
        
        adjustments = []
        
        # Analyze findings and discover adjustment triggers
        discoveries = self._extract_significant_discoveries(research_findings)
        
        logger.info(f"Found {len(discoveries)} significant discoveries")
        
        # Process each discovery and adjust weights
        for discovery in discoveries:
            adjustment = await self._process_discovery(
                discovery,
                current_weights,
                context
            )
            
            if adjustment:
                adjustments.append(adjustment)
                # Apply adjustment
                current_weights[adjustment.criterion].current_weight = adjustment.weight_after
                current_weights[adjustment.criterion].triggered_by.append(discovery["description"])
        
        # Normalize weights to sum to 100
        current_weights = self._normalize_weights(current_weights)
        
        logger.info(f"Applied {len(adjustments)} weight adjustments")
        logger.info(f"Final weights: {self._format_weights(current_weights)}")
        
        return current_weights, adjustments
    
    def _extract_significant_discoveries(
        self,
        research_findings: List[ResearchFindings]
    ) -> List[Dict[str, any]]:
        """
        Extract significant discoveries from research findings that should trigger weight adjustments.
        
        Args:
            research_findings: All research findings
        
        Returns:
            List of significant discoveries
        """
        discoveries = []
        
        for findings in research_findings:
            vendor_name = findings.vendor_name
            
            # Check uptime/reliability issues
            uptime_analysis = findings.uptime_reliability.get("analysis", "")
            if self._indicates_issue(uptime_analysis, ["outage", "downtime", "incident", "unavailable"]):
                discoveries.append({
                    "type": "uptime_issue",
                    "vendor": vendor_name,
                    "description": f"{vendor_name} has recent uptime issues",
                    "evidence": uptime_analysis[:200],
                    "affected_criterion": "uptime_reliability"
                })
            
            # Check SDK/integration issues
            sdk_support = findings.sdk_quality.get("tech_stack_support", {})
            if sdk_support and not all(sdk_support.values()):
                missing_sdks = [tech for tech, supported in sdk_support.items() if not supported]
                if missing_sdks:
                    discoveries.append({
                        "type": "missing_sdk",
                        "vendor": vendor_name,
                        "description": f"{vendor_name} missing SDK for {', '.join(missing_sdks)}",
                        "evidence": f"No official support for {missing_sdks}",
                        "affected_criterion": "integration_complexity"
                    })
            
            # Check pricing issues
            pricing_analysis = findings.pricing.get("analysis", "")
            if self._indicates_issue(pricing_analysis, ["expensive", "jump", "hidden fee", "trap"]):
                discoveries.append({
                    "type": "pricing_concern",
                    "vendor": vendor_name,
                    "description": f"{vendor_name} has pricing concerns",
                    "evidence": pricing_analysis[:200],
                    "affected_criterion": "pricing"
                })
            
            # Check hidden risks
            for risk in findings.hidden_risks:
                discoveries.append({
                    "type": f"hidden_risk_{risk['type']}",
                    "vendor": vendor_name,
                    "description": f"{vendor_name}: {risk['description'][:100]}",
                    "evidence": risk.get("evidence", ""),
                    "affected_criterion": self._map_risk_to_criterion(risk["type"])
                })
            
            # Check compliance gaps
            compliance_analysis = findings.compliance.get("analysis", "")
            required = findings.compliance.get("required", [])
            if required and self._indicates_issue(compliance_analysis, ["not certified", "lacking", "missing"]):
                discoveries.append({
                    "type": "compliance_gap",
                    "vendor": vendor_name,
                    "description": f"{vendor_name} may have compliance gaps",
                    "evidence": compliance_analysis[:200],
                    "affected_criterion": "compliance"
                })
        
        return discoveries
    
    async def _process_discovery(
        self,
        discovery: Dict[str, any],
        current_weights: Dict[str, CriterionWeight],
        context: Dict[str, any]
    ) -> Optional[WeightAdjustment]:
        """
        Process a single discovery and determine if/how to adjust weights.
        
        Args:
            discovery: Discovery information
            current_weights: Current criterion weights
            context: Evaluation context
        
        Returns:
            WeightAdjustment if adjustment made, None otherwise
        """
        affected_criterion = discovery.get("affected_criterion")
        
        if not affected_criterion or affected_criterion not in current_weights:
            return None
        
        # Determine weight adjustment based on discovery type
        adjustment_amount = self._calculate_adjustment_amount(discovery, context)
        
        if adjustment_amount == 0:
            return None
        
        criterion_weight = current_weights[affected_criterion]
        weight_before = criterion_weight.current_weight
        weight_after = weight_before + adjustment_amount
        
        # Ensure weight stays within reasonable bounds (min 5%, max 40%)
        weight_after = max(5.0, min(40.0, weight_after))
        
        # Create adjustment record
        adjustment = WeightAdjustment(
            criterion=affected_criterion,
            discovery=discovery["description"],
            evidence=discovery["evidence"],
            weight_before=weight_before,
            weight_after=weight_after,
            additional_research_triggered=[]
        )
        
        # Determine if this triggers additional research needs
        if discovery["type"] == "uptime_issue":
            adjustment.additional_research_triggered.append("SLA investigation")
        elif discovery["type"] == "missing_sdk":
            adjustment.additional_research_triggered.append("Custom integration effort estimate")
        
        logger.info(f"Weight adjustment: {affected_criterion} {weight_before:.1f}% -> {weight_after:.1f}%")
        logger.info(f"  Reason: {discovery['description']}")
        
        return adjustment
    
    def _calculate_adjustment_amount(
        self,
        discovery: Dict[str, any],
        context: Dict[str, any]
    ) -> float:
        """
        Calculate how much to adjust weight based on discovery.
        
        Args:
            discovery: Discovery information
            context: Evaluation context
        
        Returns:
            Adjustment amount (positive to increase, negative to decrease)
        """
        discovery_type = discovery["type"]
        
        # Base adjustments by discovery type
        adjustments = {
            "uptime_issue": 10.0,  # Increase uptime weight by 10%
            "missing_sdk": 8.0,     # Increase integration complexity by 8%
            "pricing_concern": 7.0, # Increase pricing weight by 7%
            "compliance_gap": 12.0, # Increase compliance weight by 12%
            "hidden_risk_maintainer_health": 5.0,  # Increase vendor health by 5%
            "hidden_risk_pricing_trap": 8.0,       # Increase pricing by 8%
            "hidden_risk_vendor_lockin": 4.0       # Moderate concern
        }
        
        base_adjustment = adjustments.get(discovery_type, 5.0)
        
        # Adjust based on context priorities
        priorities = context.get("priorities", [])
        affected_criterion = discovery.get("affected_criterion", "")
        
        # If discovery relates to a stated priority, increase adjustment
        if any(priority.lower() in affected_criterion.lower() for priority in priorities):
            base_adjustment *= 1.5
        
        return base_adjustment
    
    def _normalize_weights(
        self,
        weights: Dict[str, CriterionWeight]
    ) -> Dict[str, CriterionWeight]:
        """
        Normalize weights to sum to 100.
        
        Args:
            weights: Dictionary of weights
        
        Returns:
            Normalized weights
        """
        total = sum(w.current_weight for w in weights.values())
        
        if total == 0:
            # Fallback to equal weights
            equal_weight = 100.0 / len(weights)
            for weight in weights.values():
                weight.current_weight = equal_weight
        else:
            # Normalize to 100
            factor = 100.0 / total
            for weight in weights.values():
                weight.current_weight *= factor
        
        return weights
    
    def _map_risk_to_criterion(self, risk_type: str) -> str:
        """Map hidden risk type to evaluation criterion."""
        mapping = {
            "maintainer_health": "vendor_health",
            "pricing_trap": "pricing",
            "vendor_lockin": "integration_complexity"
        }
        return mapping.get(risk_type, "vendor_health")
    
    def _indicates_issue(self, text: str, keywords: List[str]) -> bool:
        """Check if text indicates an issue based on keywords."""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    def _format_weights(self, weights: Dict[str, CriterionWeight]) -> str:
        """Format weights for logging."""
        return ", ".join([
            f"{w.name}: {w.current_weight:.1f}%"
            for w in sorted(weights.values(), key=lambda x: x.current_weight, reverse=True)
        ])
