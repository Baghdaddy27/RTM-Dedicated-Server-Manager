@echo off
cd /d "%~dp0"
echo 🚀 Launching RTM Server Manager (Windows)...

:: Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install it from https://www.python.org
    pause
    exit /b 1
)

:: First-time setup
if not exist "venv\" (
    echo 🔧 First-time setup...
    python modules\bootstrap.py
    if %errorlevel% neq 0 (
        echo ❌ Setup failed.
        pause
        exit /b 1
    )
)

echo ✅ Environment detected. Starting application...

:: Launch GUI using pythonw.exe (no terminal window)
if exist "venv\Scripts\pythonw.exe" (
    start "" "venv\Scripts\pythonw.exe" main.py
) else (
    echo ❌ pythonw.exe not found in venv\Scripts\
    pause
    exit /b 1
)

timeout /t 2 >nul
exit
