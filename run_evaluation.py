#!/usr/bin/env python3
"""
Simple CLI wrapper for vendor evaluation.
Usage: python3 run_evaluation.py --query "evaluate payment gateways for startup"
"""
import asyncio
import sys
import argparse
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator import EvaluationOrchestrator
from config import config
from utils.query_parser import QueryParser
import json


async def run_evaluation(query: str):
    """Run evaluation from command line."""
    print(f"🚀 Starting evaluation for: {query}\n")
    print("⏳ This will take 3-4 minutes...\n")
    
    # Verify API key is configured
    if not config.openai.api_key:
        raise ValueError("OPENAI_API_KEY not set in environment. Please check .env file.")
    
    # Parse query into structured context
    print("📝 Parsing query...\n")
    parser = QueryParser()
    context = await parser.parse_query(query)
    
    print(f"   Category: {context.get('category')}")
    print(f"   Region: {context.get('region')}")
    print(f"   Scale: {context.get('scale')}")
    print(f"   Domain: {context.get('domain')}\n")
    
    # Create orchestrator (uses config from environment)
    orchestrator = EvaluationOrchestrator()
    
    try:
        # Run evaluation with parsed context
        result = await orchestrator.run_evaluation(context)
        
        # Format output
        print("\n" + "="*80)
        print("✅ EVALUATION COMPLETE")
        print("="*80 + "\n")
        
        print(f"📊 Context: {result.context_summary}")
        print(f"🎯 Recommended: {result.recommended_vendor}\n")
        
        print("📋 Candidates Evaluated:")
        for candidate in (result.candidates or []):
            if isinstance(candidate, str):
                print(f"   • {candidate}")
            else:
                print(f"   • {candidate.get('name', str(candidate))}")
        
        print("\n🔍 Key Discoveries:")
        for i, discovery in enumerate((result.key_discoveries or [])[:5], 1):
            if isinstance(discovery, dict):
                print(f"   {i}. {discovery.get('finding', str(discovery))}")
            else:
                print(f"   {i}. {discovery}")
        
        print("\n🚨 Hidden Risks:")
        hidden_risks = result.hidden_risks or []
        if hidden_risks:
            for risk in hidden_risks:
                if isinstance(risk, dict):
                    print(f"   ⚠️  {risk.get('type', 'Unknown')}: {risk.get('description', 'No description')}")
                else:
                    print(f"   ⚠️  {risk}")
        else:
            print("   ✅ No significant hidden risks detected")
        
        print(f"\n💡 Recommendation:")
        print(f"   {result.rationale}\n")
        
        if result.trade_offs:
            print("⚖️ Trade-offs:")
            for trade in result.trade_offs:
                print(f"   • {trade}")
        
        if result.next_steps:
            print("\n📋 Next Steps:")
            for step in result.next_steps:
                print(f"   • {step}")
        
        print("\n" + "="*80)
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error during evaluation: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='Run vendor evaluation')
    parser.add_argument('--query', required=True, help='Evaluation query')
    
    args = parser.parse_args()
    
    # Run evaluation
    result = asyncio.run(run_evaluation(args.query))
    
    # Exit with appropriate code
    sys.exit(0 if result else 1)


if __name__ == '__main__':
    main()
