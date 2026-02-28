"""
Evaluation Orchestrator
Main coordination logic that ties all agents together.
"""

import logging
from typing import Dict, Optional, Callable
import asyncio
from agents.candidate_identifier import CandidateIdentifier
from agents.researcher import MultiCriteriaResearcher
from agents.weight_adjuster import DynamicWeightAdjuster
from agents.synthesizer import RecommendationSynthesizer, FinalRecommendation
from integrations.clawhub import ClawHubClient
from integrations.openai_client import OpenAIClient

logger = logging.getLogger(__name__)


class EvaluationOrchestrator:
    """Orchestrates the entire evaluation process across all agents."""
    
    def __init__(self):
        """Initialize orchestrator and all agents."""
        # Initialize integration clients
        self.clawhub = ClawHubClient()
        self.openai = OpenAIClient()
        
        # Initialize agents (Logic Layer)
        self.candidate_identifier = CandidateIdentifier(self.clawhub, self.openai)
        self.researcher = MultiCriteriaResearcher(self.clawhub, self.openai)
        self.weight_adjuster = DynamicWeightAdjuster(self.openai)
        self.synthesizer = RecommendationSynthesizer(self.openai)
        
        logger.info("Evaluation orchestrator initialized")
    
    async def run_evaluation(
        self,
        context: Dict[str, any],
        progress_callback: Optional[Callable] = None
    ) -> FinalRecommendation:
        """
        Run complete vendor evaluation process.
        
        Args:
            context: Evaluation context containing:
                - category: Vendor category
                - tech_stack: List of technologies
                - domain: Industry domain
                - region: Geographic region
                - scale: Usage scale
                - priorities: List of priorities
                - compliance: List of compliance requirements
            progress_callback: Optional callback for progress updates
        
        Returns:
            FinalRecommendation object
        """
        logger.info("="*60)
        logger.info("Starting vendor evaluation")
        logger.info(f"Category: {context.get('category')}")
        logger.info(f"Context: {context}")
        logger.info("="*60)
        
        try:
            # Phase 1: Candidate Identification (30 min)
            await self._progress(progress_callback, "🔍 Identifying vendor candidates...")
            candidates = await self.candidate_identifier.identify_candidates(
                category=context["category"],
                context=context
            )
            
            candidate_names = [c.name for c in candidates]
            logger.info(f"Identified candidates: {candidate_names}")
            await self._progress(
                progress_callback,
                f"✅ Found {len(candidates)} candidates: {', '.join(candidate_names)}"
            )
            
            # Phase 2: Multi-Criteria Research (1 hr)
            await self._progress(progress_callback, "🔬 Researching candidates (deep analysis)...")
            research_findings = await self.researcher.research_candidates(
                candidates=candidates,
                context=context
            )
            logger.info(f"Research completed for {len(research_findings)} candidates")
            await self._progress(
                progress_callback,
                f"✅ Research complete! Analyzed {len(research_findings)} vendors across 10+ dimensions"
            )
            
            # Phase 3: Dynamic Weight Adjustment (45 min)
            await self._progress(progress_callback, "⚖️ Adjusting evaluation criteria based on discoveries...")
            initial_weights = self.weight_adjuster.get_initial_weights(context)
            
            final_weights, weight_adjustments = await self.weight_adjuster.adjust_weights(
                initial_weights=initial_weights,
                research_findings=research_findings,
                context=context
            )
            
            if weight_adjustments:
                logger.info(f"Applied {len(weight_adjustments)} weight adjustments")
                await self._progress(
                    progress_callback,
                    f"✅ Adapted criteria! Made {len(weight_adjustments)} adjustments based on discoveries"
                )
            else:
                logger.info("No weight adjustments made")
                await self._progress(progress_callback, "✅ Criteria weights finalized")
            
            # Phase 4: Recommendation Synthesis (30 min)
            await self._progress(progress_callback, "📊 Synthesizing final recommendation...")
            recommendation = await self.synthesizer.synthesize_recommendation(
                context=context,
                candidates=candidate_names,
                research_findings=research_findings,
                initial_weights=initial_weights,
                final_weights=final_weights,
                weight_adjustments=weight_adjustments
            )
            
            logger.info(f"Recommendation: {recommendation.recommended_vendor}")
            await self._progress(
                progress_callback,
                f"✅ Recommendation ready! Best fit: {recommendation.recommended_vendor}"
            )
            
            logger.info("="*60)
            logger.info("Evaluation completed successfully")
            logger.info("="*60)
            
            return recommendation
        
        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}", exc_info=True)
            await self._progress(progress_callback, f"❌ Evaluation failed: {str(e)}")
            raise
    
    async def _progress(self, callback: Optional[Callable], message: str):
        """Send progress update via callback."""
        logger.info(f"Progress: {message}")
        if callback:
            try:
                await callback(message)
            except Exception as e:
                logger.warning(f"Progress callback failed: {str(e)}")
    
    async def close(self):
        """Cleanup resources."""
        logger.info("Closing orchestrator resources")
        # ClawHub session cleanup if needed
        if hasattr(self.clawhub, 'session') and self.clawhub.session:
            await self.clawhub.session.close()


async def create_orchestrator() -> EvaluationOrchestrator:
    """Create and initialize orchestrator."""
    return EvaluationOrchestrator()
