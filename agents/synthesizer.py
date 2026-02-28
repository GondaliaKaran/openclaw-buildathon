"""
Recommendation Synthesizer Agent
Logic Layer Component (30 min)

Produces final structured comparison with justified recommendation.
Shows:
- How discoveries influenced final weights
- Evidence-based comparison matrix
- Clear recommendation with trade-offs
- Alternative suggestions for different contexts
"""

import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from agents.researcher import ResearchFindings
from agents.weight_adjuster import CriterionWeight, WeightAdjustment

logger = logging.getLogger(__name__)


@dataclass
class VendorScore:
    """Score for a single vendor."""
    vendor_name: str
    criterion_scores: Dict[str, float]  # criterion -> score (0-10)
    weighted_score: float
    strengths: List[str]
    weaknesses: List[str]
    evidence: Dict[str, str]  # criterion -> evidence


@dataclass
class FinalRecommendation:
    """Final recommendation output."""
    recommended_vendor: str
    rationale: str
    trade_offs: List[str]
    alternatives: List[Dict[str, str]]  # condition -> alternative vendor
    next_steps: List[str]
    
    # Full evaluation data
    context_summary: str
    candidates: List[str]
    key_discoveries: List[Dict[str, str]]
    weight_adjustments: List[WeightAdjustment]
    final_weights: Dict[str, float]
    vendor_scores: List[VendorScore]
    comparison_matrix: str  # Formatted table
    hidden_risks: List[Dict[str, any]]


class RecommendationSynthesizer:
    """Synthesizes final recommendation from all research and analysis."""
    
    def __init__(self, openai_client):
        """
        Initialize synthesizer.
        
        Args:
            openai_client: OpenAI client for generating recommendations
        """
        self.openai = openai_client
    
    async def synthesize_recommendation(
        self,
        context: Dict[str, any],
        candidates: List[str],
        research_findings: List[ResearchFindings],
        initial_weights: Dict[str, CriterionWeight],
        final_weights: Dict[str, CriterionWeight],
        weight_adjustments: List[WeightAdjustment]
    ) -> FinalRecommendation:
        """
        Synthesize final recommendation from all data.
        
        Args:
            context: Evaluation context
            candidates: List of candidate names
            research_findings: Research findings for all candidates
            initial_weights: Initial criterion weights
            final_weights: Final adjusted weights
            weight_adjustments: List of weight adjustments made
        
        Returns:
            FinalRecommendation object
        """
        logger.info("Synthesizing final recommendation")
        
        # Step 1: Score each vendor across criteria
        vendor_scores = await self._score_vendors(
            research_findings,
            final_weights
        )
        
        # Step 2: Identify key discoveries
        key_discoveries = self._extract_key_discoveries(weight_adjustments)
        
        # Step 3: Collect all hidden risks
        hidden_risks = self._collect_hidden_risks(research_findings)
        
        # Step 4: Generate comparison matrix
        comparison_matrix = self._generate_comparison_matrix(
            vendor_scores,
            final_weights
        )
        
        # Step 5: Use AI to generate final recommendation
        recommendation_text = await self._generate_recommendation(
            context,
            vendor_scores,
            key_discoveries,
            hidden_risks
        )
        
        # Step 6: Parse recommendation into structured format
        final_rec = self._parse_recommendation(
            recommendation_text,
            context,
            candidates,
            research_findings,
            key_discoveries,
            weight_adjustments,
            final_weights,
            vendor_scores,
            comparison_matrix,
            hidden_risks
        )
        
        logger.info(f"Recommendation: {final_rec.recommended_vendor}")
        return final_rec
    
    async def _score_vendors(
        self,
        research_findings: List[ResearchFindings],
        weights: Dict[str, CriterionWeight]
    ) -> List[VendorScore]:
        """
        Score each vendor across all criteria.
        
        Args:
            research_findings: Research findings for all vendors
            weights: Final criterion weights
        
        Returns:
            List of VendorScore objects
        """
        vendor_scores = []
        
        for findings in research_findings:
            # Extract scores for each criterion
            criterion_scores = {
                "sdk_quality": self._score_from_analysis(findings.sdk_quality.get("analysis", "")),
                "api_quality": self._score_from_analysis(findings.api_quality.get("analysis", "")),
                "integration_complexity": self._score_from_analysis(findings.integration_complexity.get("analysis", ""), inverse=True),
                "performance": self._score_from_analysis(findings.performance.get("analysis", "")),
                "uptime_reliability": self._score_from_analysis(findings.uptime_reliability.get("analysis", "")),
                "support_quality": self._score_from_analysis(findings.support_quality.get("analysis", "")),
                "scalability": self._score_from_analysis(findings.scalability.get("analysis", "")),
                "pricing": self._score_from_analysis(findings.pricing.get("analysis", ""), inverse=True),
                "vendor_health": self._score_from_analysis(findings.vendor_health.get("analysis", "")),
                "compliance": self._score_from_analysis(findings.compliance.get("analysis", ""))
            }
            
            # Calculate weighted score
            weighted_score = sum(
                criterion_scores[criterion] * (weights[criterion].current_weight / 100.0)
                for criterion in criterion_scores
                if criterion in weights
            )
            
            # Extract strengths and weaknesses
            strengths, weaknesses = self._extract_strengths_weaknesses(
                findings,
                criterion_scores
            )
            
            # Collect evidence
            evidence = {
                "sdk_quality": findings.sdk_quality.get("analysis", "")[:150],
                "api_quality": findings.api_quality.get("analysis", "")[:150],
                "uptime_reliability": findings.uptime_reliability.get("analysis", "")[:150],
                "pricing": findings.pricing.get("analysis", "")[:150],
            }
            
            vendor_score = VendorScore(
                vendor_name=findings.vendor_name,
                criterion_scores=criterion_scores,
                weighted_score=weighted_score,
                strengths=strengths,
                weaknesses=weaknesses,
                evidence=evidence
            )
            
            vendor_scores.append(vendor_score)
        
        # Sort by weighted score (descending)
        vendor_scores.sort(key=lambda x: x.weighted_score, reverse=True)
        
        return vendor_scores
    
    def _score_from_analysis(self, analysis: str, inverse: bool = False) -> float:
        """
        Extract a score (0-10) from analysis text.
        
        Args:
            analysis: Analysis text
            inverse: If True, negative indicators increase score
        
        Returns:
            Score from 0-10
        """
        if not analysis:
            return 5.0  # Neutral score if no data
        
        analysis_lower = analysis.lower()
        
        # Positive indicators
        positive_words = ["excellent", "great", "strong", "robust", "high quality", "reliable", "fast", "comprehensive"]
        negative_words = ["poor", "weak", "limited", "slow", "unreliable", "lacking", "difficult", "complex", "expensive"]
        
        positive_count = sum(1 for word in positive_words if word in analysis_lower)
        negative_count = sum(1 for word in negative_words if word in analysis_lower)
        
        if inverse:
            positive_count, negative_count = negative_count, positive_count
        
        # Base score calculation
        if positive_count > negative_count:
            score = 7.0 + min(positive_count, 3) * 1.0
        elif negative_count > positive_count:
            score = 5.0 - min(negative_count, 4) * 1.0
        else:
            score = 6.0
        
        return max(1.0, min(10.0, score))
    
    def _extract_strengths_weaknesses(
        self,
        findings: ResearchFindings,
        scores: Dict[str, float]
    ) -> tuple:
        """Extract top strengths and weaknesses."""
        # Sort criteria by score
        sorted_criteria = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Top 3 as strengths (if score >= 7)
        strengths = [
            self._format_strength(criterion, score)
            for criterion, score in sorted_criteria[:3]
            if score >= 7.0
        ]
        
        # Bottom 3 as weaknesses (if score <= 5)
        weaknesses = [
            self._format_weakness(criterion, score)
            for criterion, score in sorted_criteria[-3:]
            if score <= 5.0
        ]
        
        # Add hidden risks as weaknesses
        for risk in findings.hidden_risks:
            weaknesses.append(f"{risk['type'].replace('_', ' ').title()}: {risk['description'][:80]}")
        
        return strengths[:3], weaknesses[:3]
    
    def _format_strength(self, criterion: str, score: float) -> str:
        """Format a strength description."""
        criterion_display = criterion.replace("_", " ").title()
        return f"Strong {criterion_display} (Score: {score:.1f}/10)"
    
    def _format_weakness(self, criterion: str, score: float) -> str:
        """Format a weakness description."""
        criterion_display = criterion.replace("_", " ").title()
        return f"Weaker {criterion_display} (Score: {score:.1f}/10)"
    
    def _extract_key_discoveries(
        self,
        weight_adjustments: List[WeightAdjustment]
    ) -> List[Dict[str, str]]:
        """Extract key discoveries from weight adjustments."""
        discoveries = []
        
        for adj in weight_adjustments:
            discovery = {
                "finding": adj.discovery,
                "evidence": adj.evidence[:150],
                "impact": f"Increased {adj.criterion.replace('_', ' ').title()} weight from {adj.weight_before:.1f}% to {adj.weight_after:.1f}%",
                "triggered": ", ".join(adj.additional_research_triggered) if adj.additional_research_triggered else "None"
            }
            discoveries.append(discovery)
        
        return discoveries
    
    def _collect_hidden_risks(
        self,
        research_findings: List[ResearchFindings]
    ) -> List[Dict[str, any]]:
        """Collect all hidden risks found."""
        all_risks = []
        
        for findings in research_findings:
            for risk in findings.hidden_risks:
                risk_with_vendor = risk.copy()
                risk_with_vendor["vendor"] = findings.vendor_name
                all_risks.append(risk_with_vendor)
        
        return all_risks
    
    def _generate_comparison_matrix(
        self,
        vendor_scores: List[VendorScore],
        weights: Dict[str, CriterionWeight]
    ) -> str:
        """Generate comparison matrix as formatted string."""
        # Sort weights by current weight (descending)
        sorted_weights = sorted(
            weights.items(),
            key=lambda x: x[1].current_weight,
            reverse=True
        )
        
        # Build table
        lines = []
        lines.append("| Criterion (Weight) | " + " | ".join([v.vendor_name for v in vendor_scores]) + " |")
        lines.append("|" + "---|" * (len(vendor_scores) + 1))
        
        for criterion, weight_obj in sorted_weights[:8]:  # Top 8 criteria
            if weight_obj.current_weight < 1.0:
                continue
            
            criterion_display = criterion.replace("_", " ").title()
            row = f"| {criterion_display} ({weight_obj.current_weight:.1f}%) | "
            
            scores = [
                f"{v.criterion_scores.get(criterion, 0):.1f}/10"
                for v in vendor_scores
            ]
            row += " | ".join(scores) + " |"
            lines.append(row)
        
        # Add weighted total
        lines.append("|---|" + "---|" * len(vendor_scores))
        total_row = "| **Weighted Score** | "
        total_row += " | ".join([f"**{v.weighted_score:.1f}/10**" for v in vendor_scores]) + " |"
        lines.append(total_row)
        
        return "\n".join(lines)
    
    async def _generate_recommendation(
        self,
        context: Dict[str, any],
        vendor_scores: List[VendorScore],
        key_discoveries: List[Dict[str, str]],
        hidden_risks: List[Dict[str, any]]
    ) -> str:
        """Use AI to generate final recommendation text."""
        # Read SOUL.md for context
        try:
            with open("SOUL.md", "r") as f:
                soul_context = f.read()
        except FileNotFoundError:
            soul_context = "You are a senior tech evaluator providing vendor recommendations."
        
        # Build prompt
        prompt = self._build_recommendation_prompt(
            context,
            vendor_scores,
            key_discoveries,
            hidden_risks
        )
        
        # Get AI recommendation
        response = await self.openai.chat_completion(
            messages=[
                {"role": "system", "content": soul_context[:2000]},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response
    
    def _build_recommendation_prompt(
        self,
        context: Dict[str, any],
        vendor_scores: List[VendorScore],
        key_discoveries: List[Dict[str, str]],
        hidden_risks: List[Dict[str, any]]
    ) -> str:
        """Build prompt for recommendation generation."""
        # Format context
        context_lines = []
        if context.get("tech_stack"):
            context_lines.append(f"Tech Stack: {', '.join(context['tech_stack'])}")
        if context.get("domain"):
            context_lines.append(f"Domain: {context['domain']}")
        if context.get("scale"):
            context_lines.append(f"Scale: {context['scale']}")
        if context.get("priorities"):
            context_lines.append(f"Priorities: {', '.join(context['priorities'])}")
        
        context_text = "\n".join(context_lines)
        
        # Format vendor scores
        scores_text = "\n\n".join([
            f"**{v.vendor_name}**: Weighted Score {v.weighted_score:.1f}/10\n"
            f"Strengths: {', '.join(v.strengths)}\n"
            f"Weaknesses: {', '.join(v.weaknesses)}"
            for v in vendor_scores
        ])
        
        # Format discoveries
        discoveries_text = "\n".join([
            f"- {d['finding']}: {d['impact']}"
            for d in key_discoveries
        ])
        
        # Format risks
        risks_text = "\n".join([
            f"- {r['vendor']}: {r['description'][:100]}"
            for r in hidden_risks
        ]) if hidden_risks else "None detected"
        
        prompt = f"""Based on the following evaluation data, provide a final recommendation.

CONTEXT:
{context_text}

VENDOR SCORES:
{scores_text}

KEY DISCOVERIES THAT SHAPED THIS EVALUATION:
{discoveries_text}

HIDDEN RISKS DETECTED:
{risks_text}

YOUR TASK:
Provide a structured recommendation in the following format:

RECOMMENDED VENDOR: [vendor name]

RATIONALE:
[2-3 sentences explaining why this vendor is recommended for this specific context]

TRADE-OFFS:
- [Weakness 1 and why it's acceptable]
- [Weakness 2 and why it's acceptable]

ALTERNATIVES:
- If [condition]: Consider [alternative vendor] because [reason]
- If [condition]: Consider [alternative vendor] because [reason]

NEXT STEPS:
1. [Actionable step]
2. [What to validate]
3. [Suggested pilot approach if applicable]

Be specific, evidence-based, and context-aware. Show how the discoveries influenced your recommendation.
"""
        return prompt
    
    def _parse_recommendation(
        self,
        recommendation_text: str,
        context: Dict[str, any],
        candidates: List[str],
        research_findings: List[ResearchFindings],
        key_discoveries: List[Dict[str, str]],
        weight_adjustments: List[WeightAdjustment],
        final_weights: Dict[str, CriterionWeight],
        vendor_scores: List[VendorScore],
        comparison_matrix: str,
        hidden_risks: List[Dict[str, any]]
    ) -> FinalRecommendation:
        """Parse AI recommendation text into structured format."""
        lines = recommendation_text.split("\n")
        
        # Extract sections
        recommended_vendor = ""
        rationale = ""
        trade_offs = []
        alternatives = []
        next_steps = []
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if "RECOMMENDED VENDOR:" in line.upper():
                recommended_vendor = line.split(":", 1)[1].strip()
                current_section = None
            elif "RATIONALE:" in line.upper():
                current_section = "rationale"
            elif "TRADE-OFFS:" in line.upper() or "TRADE-OFF:" in line.upper():
                current_section = "tradeoffs"
            elif "ALTERNATIVES:" in line.upper() or "ALTERNATIVE:" in line.upper():
                current_section = "alternatives"
            elif "NEXT STEPS:" in line.upper():
                current_section = "nextsteps"
            elif line:
                if current_section == "rationale":
                    rationale += line + " "
                elif current_section == "tradeoffs" and line.startswith("-"):
                    trade_offs.append(line.lstrip("- "))
                elif current_section == "alternatives" and line.startswith("-"):
                    # Parse "If X: Consider Y because Z"
                    alt_text = line.lstrip("- ")
                    alternatives.append({"text": alt_text})
                elif current_section == "nextsteps" and (line.startswith("-") or line[0].isdigit()):
                    next_steps.append(line.lstrip("0123456789.-) "))
        
        # If parsing failed, use top-scored vendor
        if not recommended_vendor and vendor_scores:
            recommended_vendor = vendor_scores[0].vendor_name
            rationale = f"Recommended based on highest weighted score ({vendor_scores[0].weighted_score:.1f}/10)"
        
        # Build context summary
        context_summary = self._format_context_summary(context)
        
        # Format final weights
        final_weights_dict = {
            name: weight.current_weight
            for name, weight in final_weights.items()
        }
        
        return FinalRecommendation(
            recommended_vendor=recommended_vendor,
            rationale=rationale.strip(),
            trade_offs=trade_offs,
            alternatives=alternatives,
            next_steps=next_steps,
            context_summary=context_summary,
            candidates=candidates,
            key_discoveries=key_discoveries,
            weight_adjustments=weight_adjustments,
            final_weights=final_weights_dict,
            vendor_scores=vendor_scores,
            comparison_matrix=comparison_matrix,
            hidden_risks=hidden_risks
        )
    
    def _format_context_summary(self, context: Dict[str, any]) -> str:
        """Format context as summary string."""
        parts = []
        if context.get("tech_stack"):
            parts.append(f"Tech Stack: {', '.join(context['tech_stack'])}")
        if context.get("domain"):
            parts.append(f"Domain: {context['domain']}")
        if context.get("region"):
            parts.append(f"Region: {context['region']}")
        if context.get("scale"):
            parts.append(f"Scale: {context['scale']}")
        if context.get("priorities"):
            parts.append(f"Priorities: {', '.join(context['priorities'])}")
        
        return " | ".join(parts)
    
    def format_as_markdown(self, recommendation: FinalRecommendation) -> str:
        """Format recommendation as markdown for display."""
        md = []
        
        md.append(f"# Vendor Evaluation Report")
        md.append(f"\n## Context\n{recommendation.context_summary}")
        md.append(f"\n## Candidates Evaluated\n" + ", ".join(recommendation.candidates))
        
        # Key discoveries
        md.append(f"\n## Key Discoveries That Shaped This Evaluation")
        for i, discovery in enumerate(recommendation.key_discoveries, 1):
            md.append(f"\n### Discovery {i}: {discovery['finding']}")
            md.append(f"**Evidence**: {discovery['evidence']}")
            md.append(f"**Impact**: {discovery['impact']}")
            if discovery['triggered'] != "None":
                md.append(f"**Triggered**: {discovery['triggered']}")
        
        # Weight adjustments
        if recommendation.weight_adjustments:
            md.append(f"\n## Criteria Weight Adjustments")
            md.append("| Criterion | Initial | Final | Change | Reason |")
            md.append("|-----------|---------|-------|--------|--------|")
            for adj in recommendation.weight_adjustments:
                change = f"+{adj.weight_after - adj.weight_before:.1f}%"
                criterion_display = adj.criterion.replace("_", " ").title()
                md.append(f"| {criterion_display} | {adj.weight_before:.1f}% | {adj.weight_after:.1f}% | {change} | {adj.discovery[:40]}... |")
        
        # Comparison matrix
        md.append(f"\n## Comparison Matrix")
        md.append(recommendation.comparison_matrix)
        
        # Recommendation
        md.append(f"\n## Recommendation")
        md.append(f"\n### Recommended: **{recommendation.recommended_vendor}**")
        md.append(f"\n**Why:**\n{recommendation.rationale}")
        
        if recommendation.trade_offs:
            md.append(f"\n**Trade-offs:**")
            for tradeoff in recommendation.trade_offs:
                md.append(f"- ❌ {tradeoff}")
        
        if recommendation.alternatives:
            md.append(f"\n**Alternatives:**")
            for alt in recommendation.alternatives:
                md.append(f"- {alt['text']}")
        
        # Hidden risks
        if recommendation.hidden_risks:
            md.append(f"\n## Hidden Risks Detected")
            for risk in recommendation.hidden_risks:
                severity_emoji = "🚨" if risk['severity'] == "high" else "⚠️"
                md.append(f"\n{severity_emoji} **{risk['vendor']}**: {risk['description'][:100]}")
        
        # Next steps
        if recommendation.next_steps:
            md.append(f"\n## Next Steps")
            for i, step in enumerate(recommendation.next_steps, 1):
                md.append(f"{i}. {step}")
        
        return "\n".join(md)
