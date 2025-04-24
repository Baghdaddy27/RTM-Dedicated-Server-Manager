#!/bin/bash

echo "🚀 Launching RTM Server Manager (Linux)..."

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install it and try again."
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if python3-venv is available
if ! python3 -m venv --help &> /dev/null; then
    echo "❌ python3-venv is not installed. Run: sudo apt install python3-venv"
    read -p "Press Enter to exit..."
    exit 1
fi

# If venv doesn't exist, bootstrap
if [ ! -d "venv" ]; then
    echo "🔧 First-time setup..."
    python3 modules/bootstrap.py
    status=$?
else
    echo "✅ Environment detected. Starting application..."
    nohup ./venv/bin/python main.py > /dev/null 2>&1 &
    sleep 2
    exit 0
fi

# Hold terminal open if there was an error
if [ $status -ne 0 ]; then
    echo ""
    echo "❌ Application exited with error code $status."
    read -p "Press Enter to close..."
fi
