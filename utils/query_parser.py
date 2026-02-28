"""
Query Parser - Extracts structured context from natural language queries
"""
import json
import logging
from typing import Dict, Any
from integrations.openai_client import OpenAIClient

logger = logging.getLogger(__name__)


class QueryParser:
    """Parses natural language queries into structured evaluation context."""
    
    def __init__(self, openai_client: OpenAIClient = None):
        """Initialize parser."""
        self.openai = openai_client or OpenAIClient()
    
    async def parse_query(self, raw_query: str) -> Dict[str, Any]:
        """
        Parse a natural language query into structured context.
        
        Args:
            raw_query: Natural language query like "evaluate payment gateways for Indian startup"
        
        Returns:
            Structured context dict with:
                - category: Vendor category (e.g., "payment gateway")
                - tech_stack: List of technologies mentioned
                - domain: Industry domain
                - region: Geographic region
                - scale: Usage scale
                - priorities: List of priorities
                - compliance: List of compliance requirements
                - raw_query: Original query
        """
        logger.info(f"Parsing query: {raw_query}")
        
        prompt = f"""Extract structured evaluation context from this vendor evaluation query.

Query: "{raw_query}"

Extract and return a JSON object with these fields:
- category: The type of vendor/tool being evaluated (e.g., "payment gateway", "authentication", "CRM", "CDN")
- tech_stack: Array of technologies/languages mentioned (e.g., ["Python", "React", "AWS"]) or empty array if none
- domain: Industry/domain (e.g., "healthcare", "fintech", "e-commerce", "general") - infer from context
- region: Geographic region (e.g., "India", "US", "Global", "Europe") - default to "Global" if not specified
- scale: Usage scale as a string (e.g., "10K transactions/month", "5000 users", "startup", "enterprise")
- priorities: Array of stated priorities (e.g., ["compliance", "cost", "ease of use", "scalability"])
- compliance: Array of compliance requirements mentioned (e.g., ["HIPAA", "PCI-DSS", "GDPR", "RBI"])

Rules:
- If no specific values are mentioned, use reasonable defaults
- Be concise - extract only what's explicitly stated or strongly implied
- For scale, preserve the original phrasing if given (e.g., "10K transactions/month" not "10000")
- Infer domain from context clues (e.g., "transactions" → fintech, "patients" → healthcare)

Return ONLY the JSON object, no other text.

Example:
Query: "evaluate authentication for healthcare startup with 5000 users"
Output: {{"category": "authentication", "tech_stack": [], "domain": "healthcare", "region": "Global", "scale": "5000 users", "priorities": [], "compliance": []}}
"""
        
        response = await self.openai.generate_text(
            prompt=prompt,
            max_tokens=500,
            temperature=0.1
        )
        
        # Parse JSON response
        try:
            # Extract JSON from response (handle cases where model adds explanation)
            response_text = response.strip()
            
            # Find JSON object
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON object found in response")
            
            json_str = response_text[start_idx:end_idx]
            context = json.loads(json_str)
            
            # Add raw query
            context['raw_query'] = raw_query
            
            # Validate required fields
            required = ['category', 'tech_stack', 'domain', 'region', 'scale', 'priorities', 'compliance']
            for field in required:
                if field not in context:
                    logger.warning(f"Missing field '{field}' in parsed context, using default")
                    context[field] = [] if field in ['tech_stack', 'priorities', 'compliance'] else "unknown"
            
            logger.info(f"Parsed context: {json.dumps(context, indent=2)}")
            return context
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse OpenAI response as JSON: {e}")
            logger.error(f"Response was: {response}")
            
            # Fallback: create minimal context from query
            logger.warning("Using fallback context extraction")
            return self._fallback_parse(raw_query)
    
    def _fallback_parse(self, raw_query: str) -> Dict[str, Any]:
        """
        Fallback parser using simple heuristics if OpenAI parsing fails.
        """
        query_lower = raw_query.lower()
        
        # Try to extract category (first meaningful noun phrase)
        category = "software vendor"
        for keyword in ["payment gateway", "authentication", "crm", "cdn", "database", "analytics", 
                       "email", "sms", "monitoring", "logging", "storage"]:
            if keyword in query_lower:
                category = keyword
                break
        
        # Extract region
        region = "Global"
        for r in ["india", "indian", "us", "usa", "europe", "asia", "global"]:
            if r in query_lower:
                region = r.title()
                break
        
        # Extract scale indicators
        scale = "unknown"
        if "startup" in query_lower:
            scale = "startup"
        elif "enterprise" in query_lower:
            scale = "enterprise"
        elif "transaction" in query_lower:
            # Try to extract number
            import re
            match = re.search(r'(\d+[kKmM]?)\s*transactions?', query_lower)
            if match:
                scale = f"{match.group(1)} transactions/month"
        
        # Extract domain
        domain = "general"
        for d in ["healthcare", "fintech", "e-commerce", "saas", "education"]:
            if d in query_lower:
                domain = d
                break
        
        # Extract compliance
        compliance = []
        for c in ["hipaa", "pci-dss", "pci", "gdpr", "soc2", "rbi"]:
            if c in query_lower:
                compliance.append(c.upper())
        
        context = {
            "category": category,
            "tech_stack": [],
            "domain": domain,
            "region": region,
            "scale": scale,
            "priorities": [],
            "compliance": compliance,
            "raw_query": raw_query
        }
        
        logger.info(f"Fallback parsed context: {json.dumps(context, indent=2)}")
        return context
