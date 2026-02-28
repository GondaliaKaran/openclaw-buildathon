#!/bin/bash
# Deploy vendor evaluation to OpenClaw on VPS
# Usage: ssh root@187.77.190.61 'bash -s' < deploy.sh

set -e

CONTAINER="openclaw-l8o7-openclaw-1"
WORKSPACE="/data/.openclaw/workspace"
SKILL_DIR="$WORKSPACE/vendor-evaluation"
REPO_DIR="/root/openclaw-buildathon"

echo "=== Deploying Vendor Evaluation Agent ==="

# Step 1: Pull latest from GitHub
echo ""
echo "Step 1: Pulling latest from GitHub..."
cd $REPO_DIR
git pull origin main

# Step 2: Copy Python code to vendor-evaluation skill directory
echo ""
echo "Step 2: Copying Python files to skill directory..."
docker exec $CONTAINER mkdir -p $SKILL_DIR/agents $SKILL_DIR/integrations $SKILL_DIR/utils $SKILL_DIR/interfaces

# Core files
for f in orchestrator.py config.py run_evaluation.py skill_handler.py main.py skill.json requirements.txt .env.example start.sh; do
    if [ -f "$REPO_DIR/$f" ]; then
        docker cp "$REPO_DIR/$f" "$CONTAINER:$SKILL_DIR/$f"
    fi
done

# Agent modules
for f in $REPO_DIR/agents/*.py; do
    docker cp "$f" "$CONTAINER:$SKILL_DIR/agents/$(basename $f)"
done

# Integration modules
for f in $REPO_DIR/integrations/*.py; do
    docker cp "$f" "$CONTAINER:$SKILL_DIR/integrations/$(basename $f)"
done

# Utility modules
for f in $REPO_DIR/utils/*.py; do
    docker cp "$f" "$CONTAINER:$SKILL_DIR/utils/$(basename $f)"
done

# Interface modules
for f in $REPO_DIR/interfaces/*.py; do
    docker cp "$f" "$CONTAINER:$SKILL_DIR/interfaces/$(basename $f)"
done

# Step 3: CRITICAL - Copy SOUL.md and AGENTS.md to WORKSPACE ROOT
# OpenClaw reads these from the workspace root, NOT from skill subdirectory
echo ""
echo "Step 3: Copying SOUL.md and AGENTS.md to workspace root..."
docker cp "$REPO_DIR/SOUL.md" "$CONTAINER:$WORKSPACE/SOUL.md"
docker cp "$REPO_DIR/AGENTS.md" "$CONTAINER:$WORKSPACE/AGENTS.md"

# Also keep copies in skill dir for reference
docker cp "$REPO_DIR/SOUL.md" "$CONTAINER:$SKILL_DIR/SOUL.md"
docker cp "$REPO_DIR/AGENTS.md" "$CONTAINER:$SKILL_DIR/AGENTS.md"

# Step 4: Verify deployment
echo ""
echo "Step 4: Verifying deployment..."
echo ""
echo "--- SOUL.md first line (workspace root) ---"
docker exec $CONTAINER head -1 $WORKSPACE/SOUL.md
echo ""
echo "--- AGENTS.md first line (workspace root) ---"
docker exec $CONTAINER head -1 $WORKSPACE/AGENTS.md
echo ""
echo "--- Skill files ---"
docker exec $CONTAINER ls $SKILL_DIR/
echo ""
echo "--- Agent modules ---"
docker exec $CONTAINER ls $SKILL_DIR/agents/
echo ""

# Step 5: Install dependencies if needed
echo "Step 5: Installing Python dependencies..."
docker exec $CONTAINER pip install --break-system-packages -q openai pydantic aiohttp tenacity python-dotenv 2>/dev/null || true

echo ""
echo "=== Deployment Complete ==="
echo ""
echo "Verify SOUL.md is new version:"
docker exec $CONTAINER head -3 $WORKSPACE/SOUL.md
echo ""
echo "Test: Send to Telegram bot:"
echo '  "evaluate payment gateways for Indian startup with 10K transactions/month"'
echo ""
