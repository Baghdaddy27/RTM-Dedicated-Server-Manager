import os
import subprocess
import threading
import time
import platform
import json

from modules import notifications
from modules.logger import log_error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")
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

    with open(SETTINGS_PATH, "r") as f:
        settings = json.load(f)

    server_dir = settings.get("rtm_server_path")
    if not server_dir:
        log("❌ RTM Server path not found in settings.json.")
        return

    server_exe = os.path.join(server_dir, "MoriaServer.exe")
    if not os.path.exists(server_exe):
        log(f"❌ Could not find MoriaServer.exe in: {server_dir}")
        return

    # Notify and update server
    log("🔄 Checking for updates via SteamCMD...")
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
        log_error(f"SteamCMD update failed: {e}")
        log(f"❌ SteamCMD update failed: {e}")
        return

    # Launch the server
    log("🚀 Launching Return to Moria server...")
    notifications.send_terminal_webhook_desktop(
        log, "🚀 Launching Return to Moria Dedicated Server...", "RTM Server Manager", "Server is launching."
    )
    time.sleep(0.5)

    try:
        server_process = subprocess.Popen(
            [server_exe],
            cwd=server_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True
        )
        threading.Thread(target=read_server_output, args=(log,), daemon=True).start()
        log("✅ Server process started.")
    except Exception as e:
        log_error(f"Error starting server: {e}")
        log(f"❌ Error starting server: {e}")

def stop_server(log):
    global server_process

    if not is_server_running():
        log("⚠️ Server is not running.")
        return

    log("⏹ Sending 'Exit' to server...")
    notifications.send_terminal_webhook_desktop(
        log, "⏹ Attempting graceful shutdown...", "RTM Server Manager", "Stopping the server."
    )
    time.sleep(0.5)

    try:
        server_process.stdin.write("Exit\n")
        server_process.stdin.flush()
        time.sleep(5)

        server_process.terminate()
        server_process = None
        log("✅ Server stopped successfully.")
        notifications.send_terminal_webhook_desktop(
            log, "✅ Server stopped successfully.", "RTM Server Manager", "The server has been shut down."
        )
    except Exception as e:
        log_error(f"Error stopping server: {e}")
        log(f"❌ Error stopping server: {e}")

def read_server_output(log):
    global server_process
    if not server_process:
        return

    for line in server_process.stdout:
        if line:
            log(f"[SERVER] {line.strip()}")
