# ⚡ Quick Start Guide

## 🏠 Local Testing (FREE - No GPU)

```bash
# 1. Setup
cd llama-chatbot
cp .env.example .env
# Edit .env: Set VLLM_API_URL=mock

# 2. Deploy
chmod +x scripts/*.sh
./scripts/deploy.sh local

# 3. Test
./scripts/test_local.sh

# 4. Use
# Open: http://localhost:3000
# Create account, start chatting!
```

---

## 🚀 Runpod Deployment (PAID - With GPU)

### Before Runpod ($10 credit):

1. **Test locally first** ✅
2. **Verify everything works** ✅
3. **Upload to Docker Hub**:
   ```bash
   docker login
   docker build -t yourusername/llama-backend backend
   docker push yourusername/llama-backend
   # Repeat for vllm and frontend
   ```

### On Runpod:

```bash
# 1. Create A40 pod on Runpod.io
# 2. SSH into pod
# 3. Deploy
git clone your-repo
cd llama-chatbot
nano .env  # Change VLLM_API_URL=http://vllm:8000/v1
./scripts/deploy.sh runpod

# 4. Wait 3-5 minutes for model to load
docker-compose logs -f vllm

# 5. Access
# http://<pod-ip>:3000
```

---

## 🐛 Troubleshooting

```bash
# Check what's running
docker ps

# View logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs vllm

# Restart service
docker-compose restart backend

# Stop everything
docker-compose down

# Fresh start
docker-compose down -v
./scripts/deploy.sh local
```

---

## 🔑 Important URLs

| Service | Local | Runpod |
|---------|-------|--------|
| Frontend | http://localhost:3000 | http://POD-IP:3000 |
| Backend API | http://localhost:8080 | http://POD-IP:8080 |
| vLLM API | http://localhost:8000 | http://POD-IP:8000 |

---

## 💡 Key Files

```
.env                     # Configuration (CHANGE THIS!)
docker-compose.yml       # All services
scripts/deploy.sh        # One-click deploy
backend/app/main.py      # Backend entry point
frontend/app/page.tsx    # Chat interface
```

---

## ⚠️ CRITICAL: Before Runpod

✅ Backend health check passes  
✅ Frontend loads correctly  
✅ Can create account  
✅ Can login  
✅ Mock chat works  
✅ Docker images built  
✅ Pushed to Docker Hub  

**If any ❌ → Fix locally first!**

---

## 💰 Cost Calculator

| Mode | Cost |
|------|------|
| Local testing | $0.00 |
| Runpod A40 (On-Demand) | $0.79/hour |
| 1 hour/day for 30 days | ~$24/month |
| 2 hours/day for 30 days | ~$48/month |

**Pro tip**: Test locally, deploy only when needed, stop pod immediately after.

---

## 🎯 Deployment Checklist

### Phase 1: Local (Today)
- [ ] Install Docker
- [ ] Create project structure
- [ ] Copy all code files
- [ ] Configure .env
- [ ] Run `./scripts/deploy.sh local`
- [ ] Run `./scripts/test_local.sh`
- [ ] Test in browser

### Phase 2: Runpod (When you have $10)
- [ ] Create Docker Hub account
- [ ] Push images to Docker Hub
- [ ] Add $10 to Runpod
- [ ] Create A40 pod
- [ ] SSH and deploy
- [ ] Test with real model
- [ ] Stop pod to save money

---

## 🆘 Emergency Commands

```bash
# Backend won't start
docker-compose logs backend
docker-compose restart backend

# Port already in use
sudo lsof -i :8080
kill -9 <PID>

# Out of disk space
docker system prune -a

# Reset everything
docker-compose down -v
rm -rf data/*.db
./scripts/deploy.sh local
```

---

## 📊 How to Know It's Working

### Local Mode
1. Terminal shows "Uvicorn running"
2. http://localhost:8080/health returns {"status":"healthy"}
3. Frontend loads at http://localhost:3000
4. Chat shows mock responses

### Runpod Mode  
1. `docker logs` shows "Model loaded successfully"
2. Health check returns GPU info
3. Chat shows intelligent responses
4. Responses are contextually relevant

---

## 🔐 Security Notes

**Change these in production**:
- `SECRET_KEY` in .env
- `VLLM_API_KEY` in .env
- Default admin password
- Add HTTPS/SSL
- Enable rate limiting