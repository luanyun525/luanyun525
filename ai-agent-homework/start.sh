#!/bin/bash

echo "========================================"
echo "AI Assistant - Quick Start"
echo "========================================"
echo ""

cd "$(dirname "$0")"

echo "[1/4] Checking Python..."
if ! command -v python3 &> /dev/null
then
    echo "Python3 not found! Please install Python 3.8+"
    exit 1
fi
python3 --version
echo ""

echo "[2/4] Installing dependencies..."
pip3 install -r requirements.txt
echo ""

echo "[3/4] Running tests..."
python3 tests/test_agent.py
echo ""

echo "[4/4] Starting service..."
echo ""
echo "========================================"
echo "Service started!"
echo "Visit: http://localhost:5000"
echo "Press Ctrl+C to stop"
echo "========================================"
echo ""

cd agent
python3 app.py
