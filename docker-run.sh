#!/bin/bash
# DAST Docker Runner - Automated security scanning with Docker

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════╗"
echo "║   AI-Powered DAST Security Scanner (Docker)          ║"
echo "║   Containerized Security Testing Platform            ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Warning: .env file not found${NC}"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo -e "${RED}❌ Please configure .env with your API keys before continuing${NC}"
    exit 1
fi

# Load environment variables
set -a
source .env
set +a

# Validate required variables
if [ -z "$SLACK_BOT_TOKEN" ] || [ "$SLACK_BOT_TOKEN" = "your-slack-bot-token-here" ]; then
    echo -e "${RED}❌ SLACK_BOT_TOKEN not configured in .env${NC}"
    exit 1
fi

if [ -z "$GEMINI_API_KEY" ] || [ "$GEMINI_API_KEY" = "your-gemini-api-key-here" ]; then
    echo -e "${YELLOW}⚠️  GEMINI_API_KEY not configured - AI features will be limited${NC}"
fi

# Create reports directory
mkdir -p reports
mkdir -p zap-config

echo -e "${GREEN}✅ Environment validated${NC}"
echo ""

# Parse command line arguments
COMMAND=${1:-full}

case $COMMAND in
    "full")
        echo -e "${BLUE}🚀 Running FULL security scan (App + ZAP + AI Analysis)${NC}"
        echo ""
        
        # Step 1: Start vulnerable app
        echo -e "${YELLOW}[1/5] Starting vulnerable web application...${NC}"
        docker-compose up -d web-app
        
        # Wait for app to be healthy
        echo "Waiting for application to be healthy..."
        sleep 10
        
        # Step 2: Run ZAP scan
        echo -e "${YELLOW}[2/5] Running OWASP ZAP security scan...${NC}"
        docker-compose --profile scan up zap-scanner
        
        # Step 3: Run AI analysis
        echo -e "${YELLOW}[3/5] Running AI-powered analysis...${NC}"
        docker-compose --profile scan up dast-analyzer
        
        # Step 4: Show results
        echo ""
        echo -e "${GREEN}[4/5] Scan complete! Results:${NC}"
        if [ -f reports/report.json ]; then
            echo "  📄 HTML Report: reports/report.html"
            echo "  📊 JSON Report: reports/report.json"
            echo "  💬 Slack: Check ${SLACK_CHANNEL} for detailed report"
        else
            echo -e "${RED}  ❌ No report generated${NC}"
        fi
        
        # Step 5: Cleanup
        echo ""
        echo -e "${YELLOW}[5/5] Cleaning up containers...${NC}"
        docker-compose down
        
        echo ""
        echo -e "${GREEN}✨ DAST scan completed successfully!${NC}"
        ;;
        
    "app")
        echo -e "${BLUE}🌐 Starting vulnerable web application only${NC}"
        docker-compose up web-app
        ;;
        
    "scan")
        echo -e "${BLUE}🔍 Running security scan (requires app running)${NC}"
        docker-compose --profile scan up zap-scanner dast-analyzer
        ;;
        
    "build")
        echo -e "${BLUE}🔨 Building Docker images${NC}"
        docker-compose build
        echo -e "${GREEN}✅ Build complete${NC}"
        ;;
        
    "clean")
        echo -e "${BLUE}🧹 Cleaning up Docker resources${NC}"
        docker-compose down -v
        docker system prune -f
        rm -rf reports/*
        echo -e "${GREEN}✅ Cleanup complete${NC}"
        ;;
        
    "logs")
        echo -e "${BLUE}📋 Showing container logs${NC}"
        docker-compose logs -f
        ;;
        
    "test")
        echo -e "${BLUE}🧪 Testing Docker setup${NC}"
        echo ""
        
        # Test 1: Build images
        echo -e "${YELLOW}[1/4] Building images...${NC}"
        docker-compose build
        
        # Test 2: Start app
        echo -e "${YELLOW}[2/4] Starting application...${NC}"
        docker-compose up -d web-app
        sleep 5
        
        # Test 3: Check health
        echo -e "${YELLOW}[3/4] Checking health...${NC}"
        if curl -f http://localhost:3000/health > /dev/null 2>&1; then
            echo -e "${GREEN}  ✅ Application is healthy${NC}"
        else
            echo -e "${RED}  ❌ Application health check failed${NC}"
        fi
        
        # Test 4: Cleanup
        echo -e "${YELLOW}[4/4] Cleaning up...${NC}"
        docker-compose down
        
        echo ""
        echo -e "${GREEN}✅ Test complete${NC}"
        ;;
        
    "help"|"--help"|"-h")
        echo "Usage: ./docker-run.sh [COMMAND]"
        echo ""
        echo "Commands:"
        echo "  full     - Run complete DAST scan (default)"
        echo "  app      - Start vulnerable application only"
        echo "  scan     - Run security scan (requires app running)"
        echo "  build    - Build Docker images"
        echo "  clean    - Clean up containers and reports"
        echo "  logs     - Show container logs"
        echo "  test     - Test Docker setup"
        echo "  help     - Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./docker-run.sh full      # Full automated scan"
        echo "  ./docker-run.sh app       # Start app for manual testing"
        echo "  ./docker-run.sh test      # Validate setup"
        echo ""
        ;;
        
    *)
        echo -e "${RED}❌ Unknown command: $COMMAND${NC}"
        echo "Run './docker-run.sh help' for usage"
        exit 1
        ;;
esac
