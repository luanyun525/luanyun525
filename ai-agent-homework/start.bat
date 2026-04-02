@echo off
echo ========================================
echo AI Assistant - Quick Start
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Checking Python...
python --version
if errorlevel 1 (
    echo Python not found! Please install Python 3.8+
    pause
    exit /b 1
)
echo.

echo [2/4] Installing dependencies...
pip install -r requirements.txt
echo.

echo [3/4] Running tests...
python tests/test_agent.py
echo.

echo [4/4] Starting service...
echo.
echo ========================================
echo Service started!
echo Visit: http://localhost:5000
echo Press Ctrl+C to stop
echo ========================================
echo.

cd agent
python app.py

pause
