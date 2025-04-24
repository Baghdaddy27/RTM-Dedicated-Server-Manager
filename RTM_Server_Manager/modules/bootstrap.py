import sys
import subprocess
import venv
import platform
from pathlib import Path

# Directories
BASE_DIR = Path(__file__).resolve().parent          # modules/
ROOT_DIR = BASE_DIR.parent                          # main project folder

# Key Paths
VENV_DIR = ROOT_DIR / "venv"
PYTHON = VENV_DIR / ("Scripts/python.exe" if platform.system() == "Windows" else "bin/python")
REQUIREMENTS = BASE_DIR / "requirements.txt"
MAIN_SCRIPT = ROOT_DIR / "main.py"
ICON_PATH = ROOT_DIR / "assets" / "RTMSM.ico"
ICON_PNG = ROOT_DIR / "assets" / "RTMSM.png"

def create_venv():
    if not VENV_DIR.exists():
        print("🔧 Creating virtual environment...")
        venv.create(VENV_DIR, with_pip=True)
    else:
        print("✅ Virtual environment already exists.")

def install_requirements():
    print("📦 Installing requirements...")
    subprocess.check_call([str(PYTHON), "-m", "pip", "install", "-r", str(REQUIREMENTS)])

def launch_main():
    print("🚀 Launching main.py...")
    subprocess.run([str(PYTHON), str(MAIN_SCRIPT)])

def create_shortcut():
    if platform.system() == "Windows":
        try:
            import winshell
            from win32com.client import Dispatch
            desktop = winshell.desktop()
            path = desktop + "\\RTM Server Manager.lnk"
            shell = Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = str(PYTHON)
            shortcut.Arguments = str(MAIN_SCRIPT)
            shortcut.WorkingDirectory = str(ROOT_DIR)
            shortcut.IconLocation = str(ICON_PATH)
            shortcut.save()
            print("🖥️ Windows shortcut created on desktop.")
        except Exception as e:
            print(f"⚠️ Failed to create Windows shortcut: {e}")

    elif platform.system() == "Linux":
        shortcut = Path.home() / ".local/share/applications/rtm-server-manager.desktop"
        try:
            with open(shortcut, "w") as f:
                f.write(f"""[Desktop Entry]
Type=Application
Name=RTM Server Manager
Exec={PYTHON} {MAIN_SCRIPT}
Path={ROOT_DIR}
Icon={ICON_PNG}
Terminal=false
""")
            shortcut.chmod(0o755)
            print("🖥️ Linux desktop entry created.")
        except Exception as e:
            print(f"⚠️ Failed to create Linux shortcut: {e}")

if __name__ == "__main__":
    create_venv()
    install_requirements()
    create_shortcut()
    launch_main()
