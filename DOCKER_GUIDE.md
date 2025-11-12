# 🐳 Docker Containerization Guide

## ✅ Complete Docker Setup

Your DAST security platform is now **fully containerized**!

---

## 📦 What's Been Dockerized

### 1. **Vulnerable Web Application** (`Dockerfile`)
- Node.js 18 Alpine (lightweight)
- Runs as non-root user
- Health checks enabled
- Production-optimized

### 2. **DAST Scanner & AI Analyzer** (`Dockerfile.scanner`)
- Python 3.10 with all dependencies
- AI classification (Gemini)
- Remediation engine
- Build breaker
- Slack integration

### 3. **OWASP ZAP Scanner**
- Official ZAP image from GitHub Container Registry
- Pre-configured for baseline scanning

---

## 🚀 Quick Start

### Option 1: Automated Script (Recommended)

**Windows:**
```cmd
docker-run.bat full
```

**Linux/Mac:**
```bash
chmod +x docker-run.sh
./docker-run.sh full
```

### Option 2: Docker Compose

```bash
# Full automated scan
docker-compose up --profile scan

# Just start the vulnerable app
docker-compose up web-app

# Build images
docker-compose build
```

---

## 📋 Available Commands

### `docker-run.sh` / `docker-run.bat`

| Command | Description |
|---------|-------------|
| `full` | **Complete automated scan** (default) |
| `app` | Start vulnerable application only |
| `scan` | Run security scan (requires app running) |
| `build` | Build Docker images |
| `clean` | Clean up containers and reports |
| `logs` | Show container logs |
| `test` | Test Docker setup |
| `help` | Show help message |

---

## 🔧 Configuration

### Environment Variables

Create `.env` file with:

```bash
# Required
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_CHANNEL=#security-alerts
GEMINI_API_KEY=your-gemini-key

# Optional
USE_AI_CLASSIFICATION=true
MAX_CRITICAL_VULNS=0
MAX_HIGH_VULNS=3
MAX_MEDIUM_VULNS=10
AI_SEVERITY_THRESHOLD=8.0
BREAK_BUILD_ON_CRITICAL=true
```

### Docker Compose Profiles

```yaml
# Default: Only web app
docker-compose up

# With scanning
docker-compose --profile scan up
```

---

## 📊 Complete Workflow

When you run `docker-run.sh full`:

```
┌─────────────────────────────────────────┐
│ [1/5] Start Vulnerable Application     │
│   • Build & start Node.js app          │
│   • Wait for health check              │
│   • App running on localhost:3000      │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│ [2/5] Run OWASP ZAP Scan               │
│   • ZAP baseline scan                   │
│   • 2-minute spider                     │
│   • Generate HTML + JSON reports        │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│ [3/5] AI Analysis & Reporting          │
│   • AI classification (Gemini)          │
│   • Remediation generation              │
│   • Send to Slack                       │
│   • Security gate evaluation            │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│ [4/5] Results Available                │
│   • reports/report.html                 │
│   • reports/report.json                 │
│   • Slack notification                  │
└──────────────┬──────────────────────────┘
               ▼
┌─────────────────────────────────────────┐
│ [5/5] Cleanup                          │
│   • Stop containers                     │
│   • Keep reports                        │
└─────────────────────────────────────────┘
```

---

## 🎯 Use Cases

### 1. **CI/CD Integration**

```yaml
# .gitlab-ci.yml
security-scan:
  stage: test
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker-compose up --profile scan --exit-code-from dast-analyzer
  artifacts:
    paths:
      - reports/
```

### 2. **Local Development**

```bash
# Start app for manual testing
docker-run.sh app

# In another terminal, access the app
curl http://localhost:3000
```

### 3. **Scheduled Scans**

```bash
# Cron job (Linux)
0 2 * * * cd /path/to/dast && ./docker-run.sh full
```

```powershell
# Task Scheduler (Windows)
schtasks /create /tn "DAST Scan" /tr "C:\path\to\dast\docker-run.bat full" /sc daily /st 02:00
```

### 4. **Multi-Environment Testing**

```bash
# Test staging
TARGET_URL=https://staging.example.com docker-compose --profile scan up

# Test production
TARGET_URL=https://production.example.com docker-compose --profile scan up
```

---

## 🏗️ Architecture

### Container Network

```
┌────────────────────────────────────────────┐
│         Docker Network: dast-network       │
│                                            │
│  ┌──────────────┐     ┌───────────────┐   │
│  │   Web App    │     │  ZAP Scanner  │   │
│  │  (Node.js)   │◄────┤   (OWASP)     │   │
│  │  Port: 3000  │     │               │   │
│  └──────────────┘     └───────┬───────┘   │
│                               │           │
│                               ▼           │
│                     ┌──────────────────┐  │
│                     │  DAST Analyzer   │  │
│                     │  (AI + Slack)    │  │
│                     └──────────────────┘  │
└────────────────────────────────────────────┘
         │
         ▼
   ┌─────────────┐
   │   Reports   │
   │  (Volume)   │
   └─────────────┘
```

### Image Sizes

- **Web App**: ~170 MB (Node.js Alpine)
- **DAST Scanner**: ~500 MB (Python + dependencies)
- **ZAP**: ~1.2 GB (Java + ZAP tools)

**Total**: ~1.9 GB

---

## 🧪 Testing

### Test Docker Setup

```bash
# Windows
docker-run.bat test

# Linux/Mac
./docker-run.sh test
```

This will:
1. Build all images
2. Start the application
3. Check health endpoint
4. Clean up

### Manual Testing

```bash
# Build images
docker-compose build

# Start app
docker-compose up -d web-app

# Check health
curl http://localhost:3000/health

# Check vulnerabilities
curl http://localhost:3000/search?q=<script>alert('XSS')</script>

# Stop
docker-compose down
```

---

## 📁 File Structure

```
DAST-test/
├── Dockerfile                  # Web app container
├── Dockerfile.scanner          # Scanner container
├── docker-compose.yml          # Orchestration
├── .dockerignore              # Build exclusions
├── docker-run.sh              # Linux/Mac runner
├── docker-run.bat             # Windows runner
├── .env                       # Configuration (don't commit!)
├── .env.example               # Template
├── reports/                   # Generated reports (volume)
└── zap-config/                # ZAP configuration (volume)
```

---

## 🔒 Security Best Practices

### 1. **Non-Root Users**
Both containers run as non-root:
```dockerfile
USER nodejs    # Web app
USER scanner   # DAST analyzer
```

### 2. **Health Checks**
All containers have health checks:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### 3. **Network Isolation**
Containers communicate on isolated bridge network

### 4. **Secrets Management**
Use environment variables, not embedded secrets:
```bash
# GOOD: Load from .env
docker-compose up

# BAD: Don't hardcode secrets in Dockerfile
```

### 5. **Image Scanning**
```bash
# Scan for vulnerabilities
docker scan dast-vulnerable-app
docker scan dast-analyzer
```

---

## 🚨 Troubleshooting

### Issue: "Cannot connect to Docker daemon"

**Solution:**
```bash
# Linux
sudo systemctl start docker

# Windows/Mac
# Start Docker Desktop
```

### Issue: "Port 3000 already in use"

**Solution:**
```bash
# Find and kill process
lsof -ti:3000 | xargs kill -9   # Linux/Mac
netstat -ano | findstr :3000    # Windows (then taskkill)

# Or change port in docker-compose.yml
ports:
  - "3001:3000"
```

### Issue: "No space left on device"

**Solution:**
```bash
# Clean up Docker
docker system prune -a --volumes
```

### Issue: "Container exits immediately"

**Solution:**
```bash
# Check logs
docker-compose logs web-app
docker-compose logs zap-scanner
docker-compose logs dast-analyzer
```

### Issue: "Reports not generated"

**Solution:**
```bash
# Ensure reports directory exists and is writable
mkdir -p reports
chmod 777 reports   # Linux/Mac

# Check ZAP scanner logs
docker-compose logs zap-scanner
```

---

## 🎯 Production Deployment

### Option 1: Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml dast
```

### Option 2: Kubernetes

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vulnerable-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vulnerable-app
  template:
    metadata:
      labels:
        app: vulnerable-app
    spec:
      containers:
      - name: app
        image: your-registry/dast-vulnerable-app:latest
        ports:
        - containerPort: 3000
```

### Option 3: AWS ECS / Azure Container Instances

Use the same Docker images with your cloud provider's container service.

---

## 📊 Performance

### Build Times
- **First build**: 5-10 minutes (downloads base images)
- **Subsequent builds**: 1-2 minutes (uses cache)

### Scan Times
- **ZAP scan**: 2-5 minutes (depends on app complexity)
- **AI analysis**: 30-60 seconds
- **Total**: ~5-7 minutes

### Resource Usage
- **CPU**: 2-4 cores recommended
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk**: 5 GB for images + reports

---

## 🎉 Benefits of Dockerization

✅ **Consistency** - Same environment everywhere  
✅ **Isolation** - No conflicts with host system  
✅ **Portability** - Run anywhere Docker runs  
✅ **Scalability** - Easy to scale horizontally  
✅ **CI/CD Ready** - Integrates with any CI/CD platform  
✅ **Version Control** - Infrastructure as code  
✅ **Fast Setup** - One command to start everything  
✅ **Clean Teardown** - Complete cleanup in seconds  

---

## 📚 Additional Resources

- **Docker Docs**: https://docs.docker.com
- **Docker Compose**: https://docs.docker.com/compose
- **OWASP ZAP Docker**: https://www.zaproxy.org/docs/docker
- **Best Practices**: https://docs.docker.com/develop/dev-best-practices

---

## 🚀 Quick Reference

```bash
# Complete scan
docker-run.sh full

# Start app only
docker-compose up web-app

# View logs
docker-compose logs -f

# Clean up
docker-compose down -v

# Rebuild
docker-compose build --no-cache
```

---

## ✨ Summary

Your DAST platform is now:
✅ Fully containerized  
✅ Production-ready  
✅ CI/CD compatible  
✅ Cloud-deployable  
✅ Easy to maintain  

**One command. Complete security scan. Anywhere.** 🐳🔒
