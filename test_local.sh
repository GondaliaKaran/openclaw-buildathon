#!/bin/bash
# Local test script for vendor evaluation system

echo "🧪 Testing Vendor Evaluation System Locally"
echo "============================================"
echo ""

# Check Python version
echo "1️⃣ Checking Python version..."
python3 --version

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "2️⃣ Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo ""
echo "3️⃣ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "4️⃣ Installing dependencies..."
pip install -q -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your OPENAI_API_KEY before running tests!"
    echo ""
fi

# Check if OPENAI_API_KEY is set
source .env 2>/dev/null
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your-openai-api-key-here" ]; then
    echo ""
    echo "❌ OPENAI_API_KEY not set in .env file"
    echo ""
    echo "Please edit .env and add your OpenAI API key:"
    echo "  OPENAI_API_KEY=sk-your-actual-key-here"
    echo ""
    exit 1
fi

# Test import of modules
echo ""
echo "5️⃣ Testing module imports..."
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from orchestrator import EvaluationOrchestrator
    from config import config
    print('   ✅ Orchestrator imports OK')
    print('   ✅ Config imports OK')
    print(f'   ✅ OpenAI model: {config.openai.model}')
except Exception as e:
    print(f'   ❌ Import error: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Module import test failed!"
    exit 1
fi

# Run a quick test evaluation
echo ""
echo "6️⃣ Running quick test evaluation..."
echo "   Query: 'evaluate payment gateways for startup'"
echo ""
echo "   ⏳ This will take 3-4 minutes and use OpenAI API credits..."
echo ""

read -p "   Continue with API test? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 run_evaluation.py --query "evaluate payment gateways for startup"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Test completed successfully!"
        echo ""
        echo "📝 Next steps:"
        echo "   1. Review the output above"
        echo "   2. If it looks good, commit and push: git add . && git commit -m 'Add run_evaluation.py' && git push"
        echo "   3. Deploy to VPS: ssh root@187.77.190.61 '/root/deploy-vendor-eval.sh'"
    else
        echo ""
        echo "❌ Test failed! Check the error messages above"
    fi
else
    echo ""
    echo "ℹ️  Test skipped. To test manually:"
    echo "   source venv/bin/activate"
    echo "   python3 run_evaluation.py --query 'your query here'"
fi

echo ""
echo "Done!"
