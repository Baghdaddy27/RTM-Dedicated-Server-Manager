import os
import sys
import subprocess
import threading
import time
import platform
import json
from PyQt5.QtWidgets import QApplication
from modules import notifications
from modules.logger import log_error
from modules.config import SETTINGS_PATH


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

STEAMCMD_DIR = os.path.join(BASE_DIR, "steamcmd")
STEAMCMD_EXE = os.path.join(STEAMCMD_DIR, "steamcmd.exe" if platform.system() == "Windows" else "steamcmd.sh")
STEAM_APP_ID = "3349480"

server_process = None

def is_server_running():
    return server_process is not None and server_process.poll() is None

def start_server(log):
    global server_process

    if is_server_running():
        log("⚠️ Server is already running. Start aborted.")
        return

    if not os.path.exists(SETTINGS_PATH):
        log("❌ Cannot find settings.json! Please verify RTM files first.")
        return

    try:
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
    except Exception as e:
        log_error(f"[server_control] Failed to read settings.json: {e}")
        log("❌ Failed to read settings.json.")
        return

    server_dir = settings.get("rtm_server_path")
    if not server_dir:
        log("❌ RTM Server path not found in settings.json.")
        return

    server_exe = os.path.join(server_dir, "MoriaServer.exe")
    if not os.path.exists(server_exe):
        log(f"❌ Could not find MoriaServer.exe in: {server_dir}")
        return

    log("🔄 Checking for updates via SteamCMD...")
    QApplication.processEvents()
    time.sleep(0.3)

    notifications.send_terminal_webhook_desktop(
        log, "🔄 Server update in progress...", "Return to Moria Server", "Server is being updated."
    )
    time.sleep(0.5)

    update_command = [
        STEAMCMD_EXE,
        "+force_install_dir", server_dir,
        "+login", "anonymous",
        "+app_update", STEAM_APP_ID, "validate",
        "+quit"
    ]

    try:
        subprocess.run(update_command, check=True)
        log("✅ Server updated.")
    except Exception as e:
        log_error(f"[server_control] SteamCMD update failed: {e}")
        log(f"❌ SteamCMD update failed: {e}")
        return

    log("🚀 Launching Return to Moria server...")
    QApplication.processEvents()
    time.sleep(0.3)

    notifications.send_terminal_webhook_desktop(
        log, "🚀 Launching Return to Moria Dedicated Server...", "RTM Server Manager", "Server is launching."
    )

    try:
        server_process = subprocess.Popen(
            [server_exe],
            cwd=server_dir,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        threading.Thread(target=read_server_output, args=(log,), daemon=True).start()
        log("✅ Server process started.")
        log(f"🆔 PID: {server_process.pid}")
    except Exception as e:
        log_error(f"[server_control] Error starting server: {e}")
        log(f"❌ Error starting server: {e}")

def stop_server(log):
    global server_process

    if not is_server_running():
        log("⚠️ Server is not running.")
        return

    log("⏹ Sending shutdown to server...")
    QApplication.processEvents()
    time.sleep(0.3)

    try:
        server_process.stdin.write("Exit\n")
        server_process.stdin.flush()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            log("⚠️ Server did not exit within timeout.")

        if platform.system() == "Windows":
            try:
                subprocess.run(["taskkill", "/F", "/IM", "MoriaServer-Win64-Shipping.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                log(f"⚠️ Failed to force kill process on Windows: {e}")
        else:
            try:
                server_process.terminate()
                server_process.wait(timeout=10)
            except Exception as e:
                log(f"⚠️ Failed to terminate server process on Linux/macOS: {e}")

        server_process = None
        log("✅ Server stopped successfully.")
    except Exception as e:
        log_error(f"[server_control] Error stopping server: {e}")
        log(f"❌ Error stopping server: {e}")

def read_server_output(log):
    global server_process
    if not server_process:
        return

    try:
        for line in server_process.stdout:
            if line:
                log(f"[SERVER] {line.strip()}")
    except Exception as e:
        log_error(f"[server_control] Error reading server output: {e}")
