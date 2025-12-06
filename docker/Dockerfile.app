# Unified app image: vLLM + Backend (FastAPI) + Frontend (Next.js)
# Base on NVIDIA CUDA runtime to access GPUs
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Install system deps: Python, Node.js, git, curl, supervisor
RUN apt-get update && apt-get install -y \
    python3.10 python3.10-venv python3-pip \
    curl ca-certificates gnupg \
    git \
    supervisor \
 && rm -rf /var/lib/apt/lists/*

# Install Node.js 18 (LTS)
RUN mkdir -p /etc/apt/keyrings \
 && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
 && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_18.x nodistro main" > /etc/apt/sources.list.d/nodesource.list \
 && apt-get update && apt-get install -y nodejs \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ----------------------------
# Frontend build (Next.js)
# ----------------------------
COPY frontend/package*.json frontend/
WORKDIR /app/frontend
RUN npm ci || npm install
COPY frontend/ /app/frontend/
RUN npm run build

# ----------------------------
# Backend setup (FastAPI)
# ----------------------------
WORKDIR /app
COPY backend/requirements.txt /app/backend/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /app/backend/requirements.txt
COPY backend/ /app/backend/

# ----------------------------
# vLLM installation
# ----------------------------
RUN pip3 install --no-cache-dir \
    vllm==0.6.0 \
    fastapi==0.115.0 \
    uvicorn[standard]==0.30.0

# Ensure Postgres driver is present for SQLAlchemy
RUN python3 -m pip install --no-cache-dir psycopg2-binary==2.9.9

# Expose ports: 3000 (frontend), 8080 (backend), 8000 (vLLM)
EXPOSE 3000 8080 8000

# Add supervisord configuration
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Healthcheck: ensure vLLM is responsive
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
 CMD curl -fsS http://localhost:8000/v1/models || exit 1

# Default command: run all services under supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
