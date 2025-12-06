# 🚀 LLaMA-70B Chatbot - Complete Setup Guide

## 📋 What You're Building

A production-ready AI chatbot with:
- ✅ LLaMA-3.3-70B GPTQ model
- ✅ Streaming chat responses
- ✅ User authentication
- ✅ Web search integration (optional)
- ✅ Beautiful Next.js UI
- ✅ **Works locally WITHOUT GPU** (mock mode)
- ✅ **Deploys to Runpod in 5 minutes**

---

## 🏗️ Architecture

```
Frontend (Next.js)  →  Backend (FastAPI)  →  vLLM (GPU)
   Port 3000             Port 8080             Port 8000
```

**Key Feature**: Backend works with MOCK AI locally, switches to real GPU automatically on Runpod.

---

## 📦 Prerequisites

Install these on your computer:

1. **Docker Desktop** - https://www.docker.com/products/docker-desktop/
2. **Git** - https://git-scm.com/downloads
3. **VS Code** (optional) - https://code.visualstudio.com/

---

## 🛠️ Local Setup (No GPU Required)

### Step 1: Clone/Create Project

```bash
# If starting fresh
mkdir llama-chatbot
cd llama-chatbot

# Copy all the code files I provided into this structure:
# backend/
# frontend/
# docker/
# scripts/
# .env
```

### Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and set:
# - SECRET_KEY (use any random long string)
# - VLLM_API_URL=mock  (for local testing)
```

### Step 3: Make Deploy Script Executable

```bash
chmod +x scripts/deploy.sh
```

### Step 4: Deploy Locally

```bash
./scripts/deploy.sh local
```

**This will:**
- Build Docker containers
- Start backend API
- Start frontend UI
- Use MOCK AI (no GPU needed)

### Step 5: Test It!

1. Open http://localhost:3000/login
2. Create an account (username: test, password: test123)
3. Start chatting!

**The AI responses are mocked**, but everything else works perfectly.

---

## 🔥 Runpod Deployment (Real GPU)

### Step 1: Prepare Docker Images

We need to upload your containers to Docker Hub so Runpod can access them.

```bash
# Login to Docker Hub (create free account at hub.docker.com)
docker login

# Build and tag images
docker build -f docker/Dockerfile.backend -t yourusername/llama-backend:latest backend
docker build -f docker/Dockerfile.vllm -t yourusername/llama-vllm:latest docker
docker build -f docker/Dockerfile.frontend -t yourusername/llama-frontend:latest frontend

# Push to Docker Hub
docker push yourusername/llama-backend:latest
docker push yourusername/llama-vllm:latest
docker push yourusername/llama-frontend:latest
```

### Step 2: Create Runpod Template

1. Go to https://www.runpod.io/console/pods
2. Click "New Pod"
3. Select **GPU**: A40 (48GB VRAM)
4. Select **Container Image**: `yourusername/llama-vllm:latest`
5. Set **Container Disk**: 50 GB
6. **Expose Ports**: 8000, 8080, 3000
7. **Volume**: Add 20GB persistent volume
8. **Environment Variables**:
   ```
   VLLM_API_KEY=sk-your-secure-key
   ```

### Step 3: Connect and Deploy

Once pod starts:

```bash
# SSH into pod
ssh root@<pod-ip>

# Clone your project
git clone https://github.com/yourusername/llama-chatbot
cd llama-chatbot

# Update .env for production
nano .env
# Change: VLLM_API_URL=http://vllm:8000/v1

# Deploy everything
./scripts/deploy.sh runpod
```

### Step 4: Access Your App

- Frontend: `http://<pod-ip>:3000`
- API: `http://<pod-ip>:8080`

**The model takes 3-5 minutes to load on first run.**

Monitor with:
```bash
docker-compose -f docker/docker-compose.yml logs -f vllm
```

When you see "Uvicorn running on http://0.0.0.0:8000" → **Model is ready!**

---

## 💰 Cost Optimization

**You only pay when the pod is running.**

**Workflow:**
1. ✅ Build everything locally (FREE)
2. ✅ Test with mock AI (FREE)
3. ✅ Deploy to Runpod only when ready (~$0.79/hour)
4. ✅ Stop pod after testing
5. ✅ Data persists on volume (restart anytime)

**Monthly cost for 1 hour/day**: ~$24/month

---

## 🧪 Testing Checklist

### Local Testing (Before Runpod)

- [ ] Backend starts: `http://localhost:8080/health`
- [ ] Frontend loads: `http://localhost:3000`
- [ ] Can create account
- [ ] Can login
- [ ] Chat shows mock responses
- [ ] Messages stream word-by-word

### Runpod Testing

- [ ] vLLM container starts
- [ ] Model loads successfully (check logs)
- [ ] Health check passes: `curl http://localhost:8000/health`
- [ ] Backend connects to vLLM
- [ ] Chat shows REAL AI responses
- [ ] Responses are intelligent and coherent

---

## 🔧 Troubleshooting

### "Cannot connect to backend"
```bash
# Check backend logs
docker-compose -f docker/docker-compose.yml logs backend

# Restart backend
docker-compose -f docker/docker-compose.yml restart backend
```

### "vLLM not loading"
```bash
# Check GPU availability
nvidia-smi

# Check vLLM logs
docker logs <vllm-container-id>

# Common issue: Out of memory
# Solution: Reduce max_model_len in Dockerfile.vllm
```

### "Frontend can't reach backend"
Check CORS settings in `backend/app/main.py` - add your Runpod IP to allowed origins.

---

## 🚀 Next Steps (After Basic Setup Works)

1. **Add Web Search**
   - Get Tavily API key: https://tavily.com
   - Set in .env: `TAVILY_API_KEY=your-key`
   - Set: `ENABLE_WEB_SEARCH=true`

2. **Add LoRA Adapters**
   - Fine-tune model for specific tasks
   - Load adapters via API

3. **Multi-user Management**
   - Admin dashboard
   - Usage tracking
   - Rate limiting

4. **API Access**
   - OpenAI-compatible endpoint
   - Python client library
   - curl examples

---

## 📞 Support

If you get stuck:
1. Check logs: `docker-compose logs <service-name>`
2. Verify .env configuration
3. Test components individually
4. Ask me specific error messages!

---

## 🎯 Quick Command Reference

```bash
# Local development
./scripts/deploy.sh local

# Check status
docker-compose -f docker/docker-compose.yml ps

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop everything
docker-compose -f docker/docker-compose.yml down

# Runpod deployment
./scripts/deploy.sh runpod

# Restart specific service
docker-compose restart backend
```

---

**You're ready to build!** Start with local testing, then deploy to Runpod when everything works.