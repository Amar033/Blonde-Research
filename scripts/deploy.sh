#!/bin/bash

# ============================================
# LLAMA CHATBOT DEPLOYMENT SCRIPT
# ============================================
# Usage:
#   ./deploy.sh local   # Test locally with mock AI
#   ./deploy.sh runpod  # Deploy to Runpod with real GPU
# ============================================

set -e  # Exit on error

MODE=${1:-local}

echo "🚀 Deploying LLaMA Chatbot in $MODE mode..."

cd "$(dirname "$0")/.."

# -----------------
# LOCAL MODE
# -----------------
if [ "$MODE" = "local" ]; then
    echo "📦 Building containers for local testing..."
    
    # Create .env if not exists
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "✅ Created .env file - please configure it"
    fi
    
    # Build and run without GPU
    docker-compose -f docker/docker-compose.yml up --build -d backend frontend
    
    echo ""
    echo "✅ Local deployment complete!"
    echo ""
    echo "🌐 Access the app:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend:  http://localhost:8080"
    echo ""
    echo "📝 Test credentials:"
    echo "   Create a new account at http://localhost:3000/login"
    echo ""
    echo "⚠️  AI is running in MOCK mode (no GPU required)"
    echo ""
    echo "To stop: docker-compose -f docker/docker-compose.yml down"

# -----------------
# RUNPOD MODE
# -----------------
elif [ "$MODE" = "runpod" ]; then
    echo "🎯 Deploying to Runpod with GPU..."
    
    # Update .env for production
    sed -i 's/VLLM_API_URL=mock/VLLM_API_URL=http:\/\/vllm:8000\/v1/' .env
    
    # Build and run with GPU
    docker-compose -f docker/docker-compose.yml --profile gpu up --build -d
    
    echo ""
    echo "✅ Runpod deployment complete!"
    echo ""
    echo "🔥 Real LLaMA-70B is loading..."
    echo "   This takes 3-5 minutes on first run"
    echo ""
    echo "Monitor logs:"
    echo "   docker-compose -f docker/docker-compose.yml logs -f vllm"
    echo ""
    echo "When you see 'Uvicorn running', the model is ready!"
    
else
    echo "❌ Unknown mode: $MODE"
    echo "Usage: ./deploy.sh [local|runpod]"
    exit 1
fi