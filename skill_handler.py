"""
OpenClaw Skill Handler for Adaptive Vendor Evaluation
Entry point for OpenClaw platform integration
"""

import asyncio
import logging
import os
import json
from typing import Dict, Any, Optional
from datetime import datetime

# Import our evaluation components
from orchestrator import EvaluationOrchestrator
from agents.synthesizer import RecommendationSynthesizer

logger = logging.getLogger(__name__)

# Global orchestrator instance
_orchestrator: Optional[EvaluationOrchestrator] = None
_conversation_states: Dict[str, Dict] = {}


async def initialize():
    """
    Initialize the skill when OpenClaw loads it.
    Called once on skill registration.
    """
    global _orchestrator
    
    logger.info("=" * 60)
    logger.info("Initializing Vendor Evaluation Skill for OpenClaw")
    logger.info("=" * 60)
    
    try:
        # Verify OpenAI API key (should be set by OpenClaw)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY not set. Check OpenClaw configuration.")
            return False
        
        # Initialize orchestrator
        _orchestrator = EvaluationOrchestrator()
        logger.info("✅ Orchestrator initialized")
        
        # Load SOUL.md
        try:
            with open("SOUL.md", "r") as f:
                soul_content = f.read()
            logger.info("✅ SOUL.md loaded")
        except FileNotFoundError:
            logger.warning("⚠️  SOUL.md not found, agent personality may be limited")
        
        logger.info("=" * 60)
        logger.info("✅ Vendor Evaluation Skill Ready")
        logger.info("=" * 60)
        
        return True
    
    except Exception as e:
        logger.error(f"❌ Initialization failed: {str(e)}", exc_info=True)
        return False


async def handle_message(message: str, context: Dict[str, Any]) -> str:
    """
    Main handler for incoming messages from OpenClaw.
    
    Args:
        message: User's message text
        context: OpenClaw context containing:
            - user_id: Unique user identifier
            - channel: Channel (telegram, webchat, etc.)
            - session_id: Session identifier
            - metadata: Additional context
    
    Returns:
        Response message to send back to user
    """
    global _orchestrator, _conversation_states
    
    user_id = context.get("user_id", "unknown")
    session_id = context.get("session_id", user_id)
    
    logger.info(f"[{user_id}] Received message: {message[:100]}")
    
    try:
        # Check if orchestrator is initialized
        if _orchestrator is None:
            await initialize()
            if _orchestrator is None:
                return "⚠️ Service initialization failed. Please try again later."
        
        # Parse message intent
        intent = _parse_intent(message)
        
        if intent == "help":
            return _get_help_message()
        
        elif intent == "evaluate":
            # Start or continue evaluation
            return await _handle_evaluation(message, session_id, context)
        
        elif intent == "compare":
            # Direct comparison request
            return await _handle_comparison(message, session_id, context)
        
        elif intent == "research":
            # Single vendor research
            return await _handle_research(message, session_id, context)
        
        else:
            # General query - try to extract evaluation context
            return await _handle_general_query(message, session_id, context)
    
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}", exc_info=True)
        return f"❌ Error processing request: {str(e)}\n\nPlease try rephrasing or type 'help' for assistance."


async def _handle_evaluation(message: str, session_id: str, context: Dict) -> str:
    """Handle full vendor evaluation request."""
    global _conversation_states, _orchestrator
    
    # Get or create conversation state
    if session_id not in _conversation_states:
        _conversation_states[session_id] = {
            "stage": "gathering",
            "data": {},
            "started_at": datetime.now().isoformat()
        }
    
    state = _conversation_states[session_id]
    
    # Extract context from message
    extracted = _extract_evaluation_context(message)
    state["data"].update(extracted)
    
    # Check if we have enough information
    required = ["category"]
    missing = [r for r in required if not state["data"].get(r)]
    
    if missing:
        # Need more information
        return _ask_for_missing_info(missing, state["data"])
    
    # We have enough info - run evaluation
    try:
        response = "🚀 **Starting Evaluation**\n\n"
        response += f"Category: {state['data']['category']}\n"
        if state["data"].get("tech_stack"):
            response += f"Tech Stack: {', '.join(state['data']['tech_stack'])}\n"
        if state["data"].get("domain"):
            response += f"Domain: {state['data']['domain']}\n"
        response += "\n⏳ This will take ~3-4 minutes. Analyzing vendors...\n"
        
        # Send initial response (OpenClaw should support streaming)
        # For now, we'll do a single comprehensive response
        
        # Run evaluation
        eval_context = {
            "category": state["data"]["category"],
            "tech_stack": state["data"].get("tech_stack", []),
            "domain": state["data"].get("domain", "technology"),
            "region": state["data"].get("region", "Global"),
            "scale": state["data"].get("scale", "startup"),
            "priorities": state["data"].get("priorities", []),
            "compliance": state["data"].get("compliance", [])
        }
        
        recommendation = await _orchestrator.run_evaluation(eval_context)
        
        # Format recommendation for chat
        formatted = _format_recommendation_for_chat(recommendation)
        
        # Clear conversation state
        del _conversation_states[session_id]
        
        return response + "\n" + formatted
    
    except Exception as e:
        logger.error(f"Evaluation failed: {str(e)}", exc_info=True)
        return f"❌ Evaluation failed: {str(e)}\n\nPlease try again with more specific criteria."


async def _handle_comparison(message: str, session_id: str, context: Dict) -> str:
    """Handle direct vendor comparison request."""
    # Extract vendor names
    vendors = _extract_vendor_names(message)
    
    if len(vendors) < 2:
        return "I need at least 2 vendors to compare. Please specify which vendors you'd like to compare."
    
    return f"🔍 **Comparing {' vs '.join(vendors)}**\n\nThis feature is coming soon! For now, use 'evaluate' to get recommendations."


async def _handle_research(message: str, session_id: str, context: Dict) -> str:
    """Handle single vendor research request."""
    vendor = _extract_vendor_names(message)
    
    if not vendor:
        return "Please specify which vendor you'd like me to research."
    
    return f"🔬 **Researching {vendor[0]}**\n\nThis feature is coming soon! For now, use 'evaluate' to compare multiple vendors."


async def _handle_general_query(message: str, session_id: str, context: Dict) -> str:
    """Handle general evaluation queries."""
    # Try to extract evaluation intent
    extracted = _extract_evaluation_context(message)
    
    if extracted.get("category"):
        # User is asking about a category - start evaluation
        return await _handle_evaluation(message, session_id, context)
    
    # Default helpful response
    return """I can help you evaluate and compare vendors intelligently!

**What I do:**
• Find relevant vendor candidates
• Research deeply across 10+ criteria
• Adapt my evaluation based on discoveries
• Provide evidence-based recommendations

**How to use me:**
Just tell me what you're looking for, for example:

• "Evaluate payment gateways for my fintech startup in India"
• "Find best CRM for enterprise with Salesforce integration"
• "Compare observability tools for Python microservices on AWS"

Or type **"help"** for more details.

What would you like to evaluate?"""


def _parse_intent(message: str) -> str:
    """Parse user intent from message."""
    msg_lower = message.lower().strip()
    
    if any(word in msg_lower for word in ["help", "how to", "what can you"]):
        return "help"
    
    if msg_lower.startswith("evaluate") or "evaluate" in msg_lower:
        return "evaluate"
    
    if msg_lower.startswith("compare") or " vs " in msg_lower or " versus " in msg_lower:
        return "compare"
    
    if msg_lower.startswith("research") or msg_lower.startswith("analyze"):
        return "research"
    
    return "general"


def _extract_evaluation_context(message: str) -> Dict[str, Any]:
    """Extract evaluation context from natural language message."""
    context = {}
    msg_lower = message.lower()
    
    # Extract category
    categories = [
        "payment gateway", "crm", "database", "observability", "monitoring",
        "analytics", "cdn", "cms", "email service", "hosting", "storage",
        "authentication", "messaging", "video", "search", "cache"
    ]
    
    for cat in categories:
        if cat in msg_lower:
            context["category"] = cat
            break
    
    # Extract tech stack
    tech_keywords = ["python", "golang", "go", "javascript", "java", "ruby", "php",
                     "aws", "azure", "gcp", "kubernetes", "docker", "react", "vue"]
    found_tech = [tech for tech in tech_keywords if tech in msg_lower]
    if found_tech:
        context["tech_stack"] = found_tech
    
    # Extract domain
    domains = ["fintech", "e-commerce", "healthcare", "saas", "enterprise", "startup"]
    for domain in domains:
        if domain in msg_lower:
            context["domain"] = domain
            break
    
    # Extract region
    regions = ["india", "us", "usa", "europe", "asia", "global"]
    for region in regions:
        if region in msg_lower:
            context["region"] = region.title()
            break
    
    # Extract scale
    if "startup" in msg_lower or "early stage" in msg_lower:
        context["scale"] = "startup"
    elif "enterprise" in msg_lower or "large scale" in msg_lower:
        context["scale"] = "enterprise"
    
    # Extract priorities
    priorities = []
    if "security" in msg_lower or "secure" in msg_lower:
        priorities.append("security")
    if "uptime" in msg_lower or "reliability" in msg_lower:
        priorities.append("uptime")
    if "cost" in msg_lower or "cheap" in msg_lower or "affordable" in msg_lower:
        priorities.append("cost-effective")
    if "integration" in msg_lower or "easy to integrate" in msg_lower:
        priorities.append("easy integration")
    
    if priorities:
        context["priorities"] = priorities
    
    # Extract compliance
    compliance = []
    if "pci" in msg_lower or "pci-dss" in msg_lower:
        compliance.append("PCI-DSS")
    if "soc2" in msg_lower or "soc 2" in msg_lower:
        compliance.append("SOC2")
    if "hipaa" in msg_lower:
        compliance.append("HIPAA")
    if "rbi" in msg_lower:
        compliance.append("RBI")
    
    if compliance:
        context["compliance"] = compliance
    
    return context


def _extract_vendor_names(message: str) -> list:
    """Extract vendor names from message."""
    # Common vendor names
    vendors = [
        "stripe", "razorpay", "paypal", "square", "adyen",
        "salesforce", "hubspot", "zoho", "pipedrive",
        "datadog", "new relic", "grafana", "prometheus",
        "aws", "azure", "gcp", "digitalocean", "heroku"
    ]
    
    msg_lower = message.lower()
    found = [v for v in vendors if v in msg_lower]
    return found


def _ask_for_missing_info(missing: list, current_data: Dict) -> str:
    """Ask user for missing information."""
    if "category" in missing:
        return """What type of vendor are you evaluating?

Examples:
• Payment gateway
• CRM
• Observability platform
• Database
• CDN
• Email service

Please specify the category."""
    
    return "Please provide more details about what you're looking for."


def _format_recommendation_for_chat(recommendation) -> str:
    """Format recommendation for chat display."""
    # Create a concise chat-friendly version
    msg = "✅ **Evaluation Complete!**\n\n"
    
    # Candidates
    msg += f"**Candidates Evaluated:** {', '.join(recommendation.candidates)}\n\n"
    
    # Key discoveries
    if recommendation.key_discoveries:
        msg += "**🔍 Key Discoveries:**\n"
        for i, disc in enumerate(recommendation.key_discoveries[:2], 1):
            msg += f"{i}. {disc['finding']}\n"
            msg += f"   Impact: {disc['impact']}\n"
        msg += "\n"
    
    # Recommendation
    msg += f"**🎯 Recommended: {recommendation.recommended_vendor}**\n\n"
    msg += f"**Why:**\n{recommendation.rationale}\n\n"
    
    # Trade-offs
    if recommendation.trade_offs:
        msg += "**⚖️ Trade-offs:**\n"
        for trade in recommendation.trade_offs[:2]:
            msg += f"• {trade}\n"
        msg += "\n"
    
    # Comparison scores
    msg += "**📊 Scores:**\n"
    for vendor_score in recommendation.vendor_scores[:3]:
        msg += f"• {vendor_score.vendor_name}: {vendor_score.weighted_score:.1f}/10\n"
    
    # Hidden risks
    if recommendation.hidden_risks:
        msg += f"\n**🚨 Hidden Risks Detected: {len(recommendation.hidden_risks)}**\n"
        for risk in recommendation.hidden_risks[:2]:
            msg += f"• {risk['vendor']}: {risk['type']}\n"
    
    # Next steps
    if recommendation.next_steps:
        msg += "\n**📋 Next Steps:**\n"
        for step in recommendation.next_steps[:3]:
            msg += f"• {step}\n"
    
    msg += "\n_Full details available in logs_"
    
    return msg


def _get_help_message() -> str:
    """Return help message."""
    return """**🤖 Adaptive Vendor Evaluation Agent**

I help you find and compare vendors with intelligent, context-aware analysis.

**What makes me different:**
• Dynamic criteria weighting based on discoveries
• Deep research across 10+ dimensions
• Hidden risk detection
• Evidence-based recommendations

**How to use:**

**Option 1: Natural language**
Just describe what you need:
• "Find best payment gateway for Indian fintech startup"
• "Evaluate CRM tools for enterprise with Salesforce integration"

**Option 2: Structured request**
```
evaluate payment gateways
Tech: Python, AWS
Domain: fintech
Region: India
Priorities: security, compliance
```

**Available commands:**
• `evaluate [category]` - Full vendor evaluation
• `compare [vendor1] vs [vendor2]` - Direct comparison
• `research [vendor]` - Deep dive on one vendor
• `help` - Show this message

**Example:**
"Evaluate observability platforms for Python microservices on AWS with focus on cost and ease of integration"

What would you like to evaluate?"""


# Cleanup function called when OpenClaw unloads the skill
async def cleanup():
    """Cleanup resources when skill is unloaded."""
    global _orchestrator
    
    logger.info("Cleaning up Vendor Evaluation Skill...")
    
    if _orchestrator:
        await _orchestrator.close()
    
    logger.info("✅ Cleanup complete")
