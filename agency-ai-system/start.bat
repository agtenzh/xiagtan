@echo off
echo ========================================
echo   Agency AI System - Startup Script
echo ========================================
echo.

cd /d "%~dp0"

echo [1/5] Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo   [ERROR] Python not installed or not in PATH
    echo   Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo   [OK] Python is ready

echo.
echo [2/5] Checking Node.js environment...
node --version >nul 2>&1
if errorlevel 1 (
    echo   [ERROR] Node.js not installed or not in PATH
    echo   Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)
echo   [OK] Node.js is ready

echo.
echo [3/5] Installing backend dependencies...
cd orchestrator
if not exist "venv" (
    echo   Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
if errorlevel 1 (
    echo   [ERROR] Backend dependencies installation failed
    pause
    exit /b 1
)
echo   [OK] Backend dependencies installed

echo.
echo [4/5] Installing frontend dependencies...
cd ..\dashboard
if not exist "node_modules" (
    echo   Installing frontend dependencies...
    npm install
    if errorlevel 1 (
        echo   [ERROR] Frontend dependencies installation failed
        pause
        exit /b 1
    )
)
echo   [OK] Frontend dependencies installed

echo.
echo [5/5] Creating necessary directories...
cd ..\
if not exist "orchestrator\data" mkdir orchestrator\data
if not exist "orchestrator\logs" mkdir orchestrator\logs
echo   [OK] Directories created

echo.
echo ========================================
echo   Environment Setup Complete!
echo ========================================
echo.
echo Startup Methods:
echo.
echo Method 1: Using Docker (Recommended)
echo   docker-compose up -d
echo.
echo Method 2: Local Development
echo   Terminal 1: cd orchestrator ^&^& venv\Scripts\activate ^&^& python main.py
echo   Terminal 2: cd dashboard ^&^& npm run dev
echo.
echo Access URLs:
echo   - API Docs: http://localhost:8000/docs
echo   - Frontend: http://localhost:3000
echo   - Health Check: http://localhost:8000/health
echo.
pause
