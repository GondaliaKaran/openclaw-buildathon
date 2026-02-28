"""
Candidate Identifier Agent
Logic Layer Component (30 min)

Autonomously discovers 3-5 relevant vendor candidates based on:
- Category (e.g., payment gateway, observability, CRM)
- Context (tech stack, domain, scale, region)
- Public data sources (web search, GitHub, G2, Stack Overflow)
"""

import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from config import config

logger = logging.getLogger(__name__)


@dataclass
class Candidate:
    """Represents a vendor candidate."""
    name: str
    category: str
    description: str
    website: Optional[str] = None
    github_url: Optional[str] = None
    rationale: str = ""
    discovery_source: str = ""


class CandidateIdentifier:
    """Identifies relevant vendor candidates based on evaluation request."""
    
    def __init__(self, clawhub_client, openai_client):
        """
        Initialize candidate identifier.
        
        Args:
            clawhub_client: ClawHub integration for web search
            openai_client: OpenAI client for intelligent candidate selection
        """
        self.clawhub = clawhub_client
        self.openai = openai_client
        self.max_candidates = config.agent.max_candidates
    
    async def identify_candidates(
        self,
        category: str,
        context: Dict[str, any]
    ) -> List[Candidate]:
        """
        Identify vendor candidates for the given category and context.
        
        Args:
            category: Vendor category (e.g., "payment gateway", "observability")
            context: Context dictionary containing:
                - tech_stack: List of technologies (e.g., ["Golang", "AWS"])
                - domain: Industry domain (e.g., "fintech", "e-commerce")
                - region: Geographic region (e.g., "India", "Global")
                - scale: Usage scale (e.g., "startup", "enterprise")
                - compliance: Compliance requirements (e.g., ["PCI-DSS", "RBI"])
        
        Returns:
            List of Candidate objects
        """
        logger.info(f"Identifying candidates for category: {category}")
        logger.info(f"Context: {context}")
        
        # Step 1: Generate search queries based on category and context
        search_queries = self._generate_search_queries(category, context)
        
        # Step 2: Execute searches via ClawHub
        search_results = await self._execute_searches(search_queries)
        
        # Step 3: Use AI to select most relevant candidates
        candidates = await self._select_candidates(
            category,
            context,
            search_results
        )
        
        logger.info(f"Identified {len(candidates)} candidates")
        return candidates
    
    def _generate_search_queries(
        self,
        category: str,
        context: Dict[str, any]
    ) -> List[str]:
        """
        Generate targeted search queries based on category and context.
        
        Args:
            category: Vendor category
            context: Evaluation context
        
        Returns:
            List of search query strings
        """
        queries = []
        
        # Base query: category + "vendors" or "solutions"
        queries.append(f"best {category} vendors 2026")
        queries.append(f"{category} solutions comparison")
        
        # Add technology-specific queries
        tech_stack = context.get("tech_stack", [])
        if tech_stack:
            tech_str = " ".join(tech_stack[:2])  # Use top 2 technologies
            queries.append(f"{category} for {tech_str}")
        
        # Add domain-specific queries
        domain = context.get("domain")
        if domain:
            queries.append(f"{category} for {domain}")
        
        # Add region-specific queries
        region = context.get("region")
        if region and region.lower() != "global":
            queries.append(f"{category} {region}")
        
        # Add compliance-specific queries
        compliance = context.get("compliance", [])
        if compliance:
            comp_str = compliance[0]  # Use primary compliance requirement
            queries.append(f"{category} {comp_str} compliant")
        
        # Add alternative/open-source queries
        queries.append(f"{category} open source alternatives")
        queries.append(f"{category} startups 2026")
        
        logger.debug(f"Generated search queries: {queries}")
        return queries
    
    async def _execute_searches(self, queries: List[str]) -> List[Dict]:
        """
        Execute web searches via ClawHub.
        
        Args:
            queries: List of search query strings
        
        Returns:
            Combined search results
        """
        all_results = []
        
        for query in queries:
            try:
                results = await self.clawhub.web_search(
                    query=query,
                    num_results=5
                )
                all_results.extend(results)
                logger.debug(f"Search '{query}' returned {len(results)} results")
            except Exception as e:
                logger.warning(f"Search failed for query '{query}': {str(e)}")
                continue
        
        logger.info(f"Total search results collected: {len(all_results)}")
        return all_results
    
    async def _select_candidates(
        self,
        category: str,
        context: Dict[str, any],
        search_results: List[Dict]
    ) -> List[Candidate]:
        """
        Use AI to intelligently select most relevant candidates from search results.
        
        Args:
            category: Vendor category
            context: Evaluation context
            search_results: Raw search results from ClawHub
        
        Returns:
            List of selected Candidate objects
        """
        # Read SOUL.md to understand agent personality
        try:
            with open("SOUL.md", "r") as f:
                soul_context = f.read()
        except FileNotFoundError:
            soul_context = "You are a senior tech evaluator."
        
        # Build prompt for candidate selection
        prompt = self._build_selection_prompt(
            category,
            context,
            search_results,
            soul_context
        )
        
        # Get AI response
        response = await self.openai.chat_completion(
            messages=[
                {"role": "system", "content": soul_context[:3000]},  # Truncate for token limits
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # Parse AI response into Candidate objects
        candidates = self._parse_candidates_from_response(response)
        
        # Limit to max_candidates
        return candidates[:self.max_candidates]
    
    def _build_selection_prompt(
        self,
        category: str,
        context: Dict[str, any],
        search_results: List[Dict],
        soul_context: str
    ) -> str:
        """Build prompt for AI candidate selection."""
        # Format search results
        results_text = "\n\n".join([
            f"Source: {r.get('url', 'N/A')}\n"
            f"Title: {r.get('title', 'N/A')}\n"
            f"Snippet: {r.get('snippet', 'N/A')}"
            for r in search_results[:30]  # Limit to 30 results for token economy
        ])
        
        # Format context
        context_items = []
        if context.get("tech_stack"):
            context_items.append(f"Tech Stack: {', '.join(context['tech_stack'])}")
        if context.get("domain"):
            context_items.append(f"Domain: {context['domain']}")
        if context.get("region"):
            context_items.append(f"Region: {context['region']}")
        if context.get("scale"):
            context_items.append(f"Scale: {context['scale']}")
        if context.get("compliance"):
            context_items.append(f"Compliance: {', '.join(context['compliance'])}")
        
        context_text = "\n".join(context_items)
        
        prompt = f"""Based on the following search results, identify {self.max_candidates} most relevant vendor candidates for evaluation.

CATEGORY: {category}

CONTEXT:
{context_text}

SEARCH RESULTS:
{results_text}

YOUR TASK:
1. Identify {self.max_candidates} diverse, relevant vendors (mix of established leaders, emerging alternatives, and region-specific options)
2. For each candidate, provide:
   - Name
   - Brief description (one line)
   - Website URL (if found)
   - GitHub URL (if applicable)
   - Rationale for inclusion (why relevant to this context)
   - Discovery source (which search result led you to this candidate)

OUTPUT FORMAT (JSON):
{{
  "candidates": [
    {{
      "name": "Vendor Name",
      "description": "Brief description",
      "website": "https://...",
      "github_url": "https://github.com/...",
      "rationale": "Why this vendor is relevant",
      "discovery_source": "Search query or URL"
    }}
  ]
}}

Focus on candidates that match the context (tech stack, domain, region, scale, compliance).
Include a mix of: established leaders, emerging alternatives, and any region-specific or open-source options.
"""
        return prompt
    
    def _parse_candidates_from_response(self, response: str) -> List[Candidate]:
        """
        Parse AI response into Candidate objects.
        
        Args:
            response: AI response string (should be JSON)
        
        Returns:
            List of Candidate objects
        """
        import json
        
        try:
            # Try to parse as JSON
            data = json.loads(response)
            candidates_data = data.get("candidates", [])
            
            candidates = []
            for c in candidates_data:
                candidate = Candidate(
                    name=c.get("name", "Unknown"),
                    category="",  # Will be set by caller
                    description=c.get("description", ""),
                    website=c.get("website"),
                    github_url=c.get("github_url"),
                    rationale=c.get("rationale", ""),
                    discovery_source=c.get("discovery_source", "")
                )
                candidates.append(candidate)
            
            return candidates
        
        except json.JSONDecodeError:
            logger.error("Failed to parse AI response as JSON")
            # Fallback: extract vendor names from text
            return self._fallback_parse(response)
    
    def _fallback_parse(self, response: str) -> List[Candidate]:
        """Fallback parser if JSON parsing fails."""
        # Simple extraction of vendor names
        # This is a basic fallback - the actual implementation would be more robust
        candidates = []
        lines = response.split("\n")
        
        for line in lines:
            # Look for patterns like "1. Vendor Name" or "- Vendor Name"
            if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith("-")):
                # Extract vendor name (very basic)
                name = line.strip().lstrip("0123456789.-) ").split(":")[0].strip()
                if name and len(name) > 2:
                    candidates.append(Candidate(
                        name=name,
                        category="",
                        description="",
                        rationale="Extracted from AI response"
                    ))
        
        return candidates[:self.max_candidates]
