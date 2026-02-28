"""
Prompt templates and utilities.
"""

from typing import Dict, List


class PromptTemplates:
    """Collection of prompt templates for the agent."""
    
    @staticmethod
    def candidate_selection(
        category: str,
        context: Dict[str, any],
        search_results: List[Dict]
    ) -> str:
        """Prompt for candidate selection."""
        return f"""Based on search results, identify relevant vendor candidates.

Category: {category}
Context: {context}
Search Results: {len(search_results)} results

Identify 3-5 diverse, relevant vendors. Include:
- Established leaders
- Emerging alternatives
- Region-specific options (if applicable)
- Open-source options (if relevant)

For each candidate, provide:
- Name
- Brief description
- Why relevant to this context
"""
    
    @staticmethod
    def research_analysis(
        vendor_name: str,
        dimension: str,
        search_results: List[Dict]
    ) -> str:
        """Prompt for research analysis."""
        return f"""Analyze {dimension} for {vendor_name}.

Search Results:
{search_results}

Provide a concise analysis (2-3 sentences) with specific evidence.
If data is insufficient, state that clearly.
"""
    
    @staticmethod
    def weight_adjustment_reasoning(
        discovery: str,
        current_weights: Dict[str, float]
    ) -> str:
        """Prompt for weight adjustment reasoning."""
        return f"""Given this discovery: {discovery}

Current evaluation weights: {current_weights}

Should any weights be adjusted? If yes, explain:
1. Which criterion weight should change
2. By how much
3. Why this discovery matters
4. What additional research it triggers
"""
    
    @staticmethod
    def final_recommendation(
        context: Dict[str, any],
        vendor_scores: List[tuple],
        discoveries: List[str]
    ) -> str:
        """Prompt for final recommendation."""
        return f"""Provide a final vendor recommendation.

Context: {context}
Vendor Scores: {vendor_scores}
Key Discoveries: {discoveries}

Format:
RECOMMENDED: [vendor name]
RATIONALE: [why for this context]
TRADE-OFFS: [weaknesses and mitigations]
ALTERNATIVES: [if X then Y]
NEXT STEPS: [actionable steps]
"""
