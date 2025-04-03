
#!/bin/bash

# Path to your project root
PROJECT_DIR="/home/jordan/Projects/RTMServerManager"

# Path to the virtual environment
VENV_DIR="$PROJECT_DIR/venv"

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv "$VENV_DIR"
    echo "✅ Virtual environment created at $VENV_DIR"
fi

# Activate the virtual environment
echo "🔄 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Confirm and open interactive shell
echo "✅ Virtual environment activated. You're now in the RTM venv."
echo "💡 Run 'python main.py' to launch the server manager."
$SHELL
