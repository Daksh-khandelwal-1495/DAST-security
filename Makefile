# Makefile for DAST Security Platform
# Simplifies Docker operations

.PHONY: help build up down scan clean test logs

# Default target
help:
	@echo "╔═══════════════════════════════════════════════════════╗"
	@echo "║   AI-Powered DAST Security Scanner (Docker)          ║"
	@echo "╚═══════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Available commands:"
	@echo "  make build    - Build Docker images"
	@echo "  make up       - Start vulnerable application"
	@echo "  make scan     - Run full security scan"
	@echo "  make down     - Stop all containers"
	@echo "  make clean    - Clean up containers and images"
	@echo "  make test     - Test Docker setup"
	@echo "  make logs     - Show container logs"
	@echo ""

# Build Docker images
build:
	@echo "🔨 Building Docker images..."
	docker-compose build
	@echo "✅ Build complete"

# Start vulnerable application
up:
	@echo "🚀 Starting vulnerable web application..."
	docker-compose up -d web-app
	@echo "✅ Application running at http://localhost:3000"
	@echo "   Health check: http://localhost:3000/health"

# Run full security scan
scan:
	@echo "🔍 Running full security scan..."
	@echo "[1/3] Starting application..."
	docker-compose up -d web-app
	@sleep 10
	@echo "[2/3] Running ZAP scan..."
	docker-compose --profile scan up zap-scanner
	@echo "[3/3] Running AI analysis..."
	docker-compose --profile scan up dast-analyzer
	@echo "✅ Scan complete! Check reports/ directory"

# Stop all containers
down:
	@echo "🛑 Stopping containers..."
	docker-compose down
	@echo "✅ Containers stopped"

# Clean up everything
clean:
	@echo "🧹 Cleaning up Docker resources..."
	docker-compose down -v
	docker system prune -f
	rm -rf reports/*
	@echo "✅ Cleanup complete"

# Test Docker setup
test:
	@echo "🧪 Testing Docker setup..."
	@echo "[1/4] Building images..."
	docker-compose build
	@echo "[2/4] Starting application..."
	docker-compose up -d web-app
	@sleep 5
	@echo "[3/4] Checking health..."
	@curl -f http://localhost:3000/health || echo "❌ Health check failed"
	@echo "[4/4] Cleaning up..."
	docker-compose down
	@echo "✅ Test complete"

# Show logs
logs:
	@echo "📋 Showing container logs (Ctrl+C to exit)..."
	docker-compose logs -f
