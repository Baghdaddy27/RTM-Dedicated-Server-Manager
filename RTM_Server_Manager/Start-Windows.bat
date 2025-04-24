@echo off
echo 🚀 Launching RTM Server Manager (Windows)...

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install it from https://www.python.org
    pause
    exit /b 1
)

if not exist "venv\" (
    echo 🔧 First-time setup...
    python modules\bootstrap.py
) else (
    echo ✅ Environment detected. Starting application...
    start "" venv\Scripts\python.exe main.py
)
