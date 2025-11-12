@echo off
REM DAST Docker Runner for Windows
REM Automated security scanning with Docker

echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║   AI-Powered DAST Security Scanner (Docker)          ║
echo ║   Containerized Security Testing Platform            ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

REM Check if .env file exists
if not exist .env (
    echo [WARNING] .env file not found
    echo Creating from .env.example...
    copy .env.example .env
    echo [ERROR] Please configure .env with your API keys before continuing
    exit /b 1
)

REM Create reports directory
if not exist reports mkdir reports
if not exist zap-config mkdir zap-config

echo [OK] Environment validated
echo.

REM Parse command
set COMMAND=%1
if "%COMMAND%"=="" set COMMAND=full

if "%COMMAND%"=="full" goto full
if "%COMMAND%"=="app" goto app
if "%COMMAND%"=="scan" goto scan
if "%COMMAND%"=="build" goto build
if "%COMMAND%"=="clean" goto clean
if "%COMMAND%"=="logs" goto logs
if "%COMMAND%"=="test" goto test
if "%COMMAND%"=="help" goto help
if "%COMMAND%"=="--help" goto help
if "%COMMAND%"=="-h" goto help

echo [ERROR] Unknown command: %COMMAND%
echo Run 'docker-run.bat help' for usage
exit /b 1

:full
echo [1/5] Starting vulnerable web application...
docker-compose up -d web-app

echo Waiting for application to be healthy...
timeout /t 10 /nobreak >nul

echo [2/5] Running OWASP ZAP security scan...
docker-compose --profile scan up zap-scanner

echo [3/5] Running AI-powered analysis...
docker-compose --profile scan up dast-analyzer

echo.
echo [4/5] Scan complete! Results:
if exist reports\report.json (
    echo   HTML Report: reports\report.html
    echo   JSON Report: reports\report.json
    echo   Slack: Check your channel for detailed report
) else (
    echo   [ERROR] No report generated
)

echo.
echo [5/5] Cleaning up containers...
docker-compose down

echo.
echo [SUCCESS] DAST scan completed successfully!
goto end

:app
echo Starting vulnerable web application only...
docker-compose up web-app
goto end

:scan
echo Running security scan (requires app running)...
docker-compose --profile scan up zap-scanner dast-analyzer
goto end

:build
echo Building Docker images...
docker-compose build
echo [SUCCESS] Build complete
goto end

:clean
echo Cleaning up Docker resources...
docker-compose down -v
docker system prune -f
if exist reports rmdir /s /q reports
mkdir reports
echo [SUCCESS] Cleanup complete
goto end

:logs
echo Showing container logs...
docker-compose logs -f
goto end

:test
echo Testing Docker setup...
echo.

echo [1/4] Building images...
docker-compose build

echo [2/4] Starting application...
docker-compose up -d web-app
timeout /t 5 /nobreak >nul

echo [3/4] Checking health...
curl -f http://localhost:3000/health >nul 2>&1
if %errorlevel%==0 (
    echo   [OK] Application is healthy
) else (
    echo   [ERROR] Application health check failed
)

echo [4/4] Cleaning up...
docker-compose down

echo.
echo [SUCCESS] Test complete
goto end

:help
echo Usage: docker-run.bat [COMMAND]
echo.
echo Commands:
echo   full     - Run complete DAST scan (default)
echo   app      - Start vulnerable application only
echo   scan     - Run security scan (requires app running)
echo   build    - Build Docker images
echo   clean    - Clean up containers and reports
echo   logs     - Show container logs
echo   test     - Test Docker setup
echo   help     - Show this help message
echo.
echo Examples:
echo   docker-run.bat full      # Full automated scan
echo   docker-run.bat app       # Start app for manual testing
echo   docker-run.bat test      # Validate setup
echo.
goto end

:end
exit /b 0
