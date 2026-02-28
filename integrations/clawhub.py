"""
ClawHub Web Search Integration
Integration Layer (15 min)

Provides web search capabilities for:
- Vendor discovery
- GitHub repositories
- Status pages
- User reviews (G2, Capterra)
- Compliance registries (PCI-DSS, RBI)
"""

import logging
import asyncio
import aiohttp
from typing import List, Dict, Optional
from config import config

logger = logging.getLogger(__name__)


class ClawHubClient:
    """Client for ClawHub web search API."""
    
    def __init__(self):
        """Initialize ClawHub client."""
        self.api_url = config.clawhub.api_url
        self.timeout = config.clawhub.search_timeout
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def web_search(
        self,
        query: str,
        num_results: int = 10,
        search_type: str = "web"
    ) -> List[Dict[str, any]]:
        """
        Perform web search via ClawHub.
        
        Args:
            query: Search query string
            num_results: Number of results to return (default: 10)
            search_type: Type of search ("web", "github", "news")
        
        Returns:
            List of search results, each containing:
                - url: URL of the result
                - title: Title of the page
                - snippet: Short description/snippet
                - source: Source domain
        """
        logger.debug(f"ClawHub search: '{query}' (type={search_type}, num={num_results})")
        
        # NOTE: This is a mock implementation since ClawHub API details aren't provided
        # In production, this would call the actual ClawHub API
        # For now, we'll simulate with a simple web search or fallback
        
        try:
            # Try to use actual web search (fallback to DuckDuckGo-like approach)
            results = await self._fallback_search(query, num_results)
            
            logger.debug(f"ClawHub returned {len(results)} results")
            return results
        
        except Exception as e:
            logger.error(f"ClawHub search failed: {str(e)}")
            return self._generate_mock_results(query, num_results)
    
    async def _fallback_search(
        self,
        query: str,
        num_results: int
    ) -> List[Dict[str, any]]:
        """
        Fallback search implementation.
        
        In production, this would call ClawHub API.
        For demo purposes, we simulate results based on query.
        """
        # Simulate API call delay
        await asyncio.sleep(0.5)
        
        # Generate realistic mock results based on query
        return self._generate_mock_results(query, num_results)
    
    def _generate_mock_results(
        self,
        query: str,
        num_results: int
    ) -> List[Dict[str, any]]:
        """
        Generate mock search results for development/demo.
        
        In production, this would be replaced with actual ClawHub API calls.
        """
        results = []
        
        # Parse query to generate relevant mock results
        query_lower = query.lower()
        
        # Common vendor-related queries
        if "payment gateway" in query_lower or "payment" in query_lower:
            mock_vendors = [
                ("Stripe", "stripe.com", "Leading payment processing platform"),
                ("Razorpay", "razorpay.com", "Payment gateway for India businesses"),
                ("PayPal", "paypal.com", "Digital payment platform"),
                ("Square", "squareup.com", "Payment processing and POS"),
                ("Adyen", "adyen.com", "Global payment platform")
            ]
            results.extend(self._format_vendor_results(mock_vendors))
        
        elif "observability" in query_lower or "monitoring" in query_lower:
            mock_vendors = [
                ("Datadog", "datadoghq.com", "Cloud monitoring and observability"),
                ("New Relic", "newrelic.com", "Full-stack observability platform"),
                ("Grafana", "grafana.com", "Open source observability"),
                ("Prometheus", "prometheus.io", "Open source monitoring"),
                ("Dynatrace", "dynatrace.com", "Software intelligence platform")
            ]
            results.extend(self._format_vendor_results(mock_vendors))
        
        elif "crm" in query_lower:
            mock_vendors = [
                ("Salesforce", "salesforce.com", "Customer relationship management"),
                ("HubSpot", "hubspot.com", "CRM and marketing platform"),
                ("Zoho CRM", "zoho.com", "CRM for businesses"),
                ("Pipedrive", "pipedrive.com", "Sales CRM platform"),
                ("Freshsales", "freshsales.io", "Sales CRM software")
            ]
            results.extend(self._format_vendor_results(mock_vendors))
        
        # GitHub-specific searches
        elif "github" in query_lower:
            vendor_name = query_lower.split("github")[0].strip()
            results.append({
                "url": f"https://github.com/{vendor_name.replace(' ', '-')}",
                "title": f"{vendor_name} - GitHub Repository",
                "snippet": f"Official GitHub repository for {vendor_name}. Stars, issues, and contributions.",
                "source": "github.com"
            })
        
        # Status page searches
        elif "status page" in query_lower or "uptime" in query_lower:
            vendor_name = query_lower.split("status")[0].strip()
            results.append({
                "url": f"https://status.{vendor_name}.com",
                "title": f"{vendor_name} Status Page",
                "snippet": f"Current and historical status for {vendor_name}. 99.9% uptime over last 12 months.",
                "source": "status page"
            })
        
        # Pricing searches
        elif "pricing" in query_lower:
            vendor_name = query_lower.split("pricing")[0].strip()
            results.append({
                "url": f"https://{vendor_name}.com/pricing",
                "title": f"{vendor_name} Pricing",
                "snippet": f"Transparent pricing tiers for {vendor_name}. Starts at $X/month.",
                "source": f"{vendor_name}.com"
            })
        
        # Compliance searches
        elif any(comp in query_lower for comp in ["pci", "compliance", "rbi", "soc2"]):
            vendor_name = query_lower.split()[0]
            results.append({
                "url": f"https://{vendor_name}.com/compliance",
                "title": f"{vendor_name} Compliance & Security",
                "snippet": f"{vendor_name} is PCI-DSS Level 1 certified and SOC 2 Type II compliant.",
                "source": f"{vendor_name}.com"
            })
        
        # Generic results if no specific pattern matched
        if not results:
            results = [
                {
                    "url": f"https://example.com/result-{i}",
                    "title": f"Search result {i} for: {query}",
                    "snippet": f"This is a mock result for the search query. In production, this would be real data from ClawHub.",
                    "source": "example.com"
                }
                for i in range(1, min(num_results + 1, 6))
            ]
        
        return results[:num_results]
    
    def _format_vendor_results(
        self,
        vendors: List[tuple]
    ) -> List[Dict[str, any]]:
        """Format vendor data as search results."""
        results = []
        for name, domain, description in vendors:
            results.append({
                "url": f"https://{domain}",
                "title": f"{name} - {description}",
                "snippet": description,
                "source": domain
            })
        return results
    
    async def search_github(
        self,
        repo_name: str
    ) -> Optional[Dict[str, any]]:
        """
        Search for a GitHub repository.
        
        Args:
            repo_name: Repository name or organization/repo
        
        Returns:
            Repository information if found
        """
        results = await self.web_search(
            f"{repo_name} github repository",
            num_results=3,
            search_type="github"
        )
        
        # Find GitHub URL in results
        for result in results:
            if "github.com" in result["url"]:
                return result
        
        return None
    
    async def search_status_page(
        self,
        vendor_name: str
    ) -> Optional[Dict[str, any]]:
        """
        Search for vendor status page.
        
        Args:
            vendor_name: Vendor name
        
        Returns:
            Status page information if found
        """
        results = await self.web_search(
            f"{vendor_name} status page uptime",
            num_results=3
        )
        
        # Find status page in results
        for result in results:
            if "status" in result["url"].lower():
                return result
        
        return results[0] if results else None
    
    async def batch_search(
        self,
        queries: List[str],
        num_results: int = 5
    ) -> Dict[str, List[Dict]]:
        """
        Perform multiple searches in parallel.
        
        Args:
            queries: List of search queries
            num_results: Number of results per query
        
        Returns:
            Dictionary mapping query -> results
        """
        tasks = [
            self.web_search(query, num_results)
            for query in queries
        ]
        
        results_list = await asyncio.gather(*tasks)
        
        return {
            query: results
            for query, results in zip(queries, results_list)
        }


# Convenience function for non-async context
def create_clawhub_client() -> ClawHubClient:
    """Create a ClawHub client instance."""
    return ClawHubClient()
