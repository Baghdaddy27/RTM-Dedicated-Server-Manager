import os
import sys
import zipfile
import subprocess
import json
import platform
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer
from urllib.request import urlretrieve
from modules.logger import log_error
from modules.config import SETTINGS_PATH


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

STEAMCMD_ZIP = os.path.join(BASE_DIR, "steamcmd.zip")
STEAMCMD_DIR = os.path.join(BASE_DIR, "steamcmd")
IS_WINDOWS = platform.system() == "Windows"

steamcmd_exe = os.path.join(
    STEAMCMD_DIR, "steamcmd.exe" if IS_WINDOWS else "steamcmd.sh"
)

def verify_steamcmd(log):
    log(f"🔍 Looking for SteamCMD at: {steamcmd_exe}")
    if not os.path.exists(steamcmd_exe):
        log("📦 SteamCMD not found. Installing...")
        os.makedirs(STEAMCMD_DIR, exist_ok=True)

        if IS_WINDOWS:
            try:
                with zipfile.ZipFile(STEAMCMD_ZIP, 'r') as zip_ref:
                    zip_ref.extractall(STEAMCMD_DIR)
                log("✅ SteamCMD extracted.")
            except Exception as e:
                log_error(f"[setup] SteamCMD extraction failed: {e}")
                log("❌ Error extracting SteamCMD.")
                return
        else:
            try:
                linux_url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
                tar_path = os.path.join(STEAMCMD_DIR, "steamcmd_linux.tar.gz")
                urlretrieve(linux_url, tar_path)
                subprocess.run(["tar", "-xvzf", tar_path, "-C", STEAMCMD_DIR], check=True)
                log("✅ SteamCMD downloaded and extracted for Linux.")
            except Exception as e:
                log_error(f"[setup] SteamCMD download/extract failed (Linux): {e}")
                log("❌ Error downloading SteamCMD.")
                return

    log("✅ SteamCMD is set up and ready.")

def verify_rtm_files(log):
    if not os.path.exists(steamcmd_exe):
        log("❌ SteamCMD is not available. Please verify SteamCMD first.")
        return

    install_dir = None
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                settings = json.load(f)
                install_dir = settings.get("rtm_server_path")
        except Exception as e:
            log_error(f"[setup] Failed to read settings.json: {e}")
            log("⚠️ Failed to read settings.json.")

    if not install_dir or not os.path.isdir(install_dir):
        log("📁 No RTM server directory found. Please select or create one.")
        QTimer.singleShot(200, lambda: _select_rtm_path(log))
        return

    log(f"🔄 Installing/updating Return to Moria server at: {install_dir}")
    QTimer.singleShot(200, lambda: _run_steamcmd_update(log, install_dir))

def _select_rtm_path(log):
    selected = QFileDialog.getExistingDirectory(None, "Select RTM Server Install Directory")
    if not selected:
        log("❌ Operation cancelled by user.")
        return

    try:
        with open(SETTINGS_PATH, "w") as f:
            json.dump({"rtm_server_path": selected}, f, indent=4)
        log(f"✅ Saved RTM install location to settings.json: {selected}")
        log(f"🔄 Installing/updating Return to Moria server at: {selected}")
        QTimer.singleShot(200, lambda: _run_steamcmd_update(log, selected))
    except Exception as e:
        log_error(f"[setup] Failed to save install directory to settings.json: {e}")
        log("❌ Failed to save RTM install location.")

def _run_steamcmd_update(log, install_dir):
    try:
        result = subprocess.run([
            steamcmd_exe,
            "+force_install_dir", install_dir,
            "+login", "anonymous",
            "+app_update", "3349480", "validate",
            "+quit"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        output = result.stdout + result.stderr
        if "Success! App '3349480'" in output:
            log("✅ RTM server installed/updated successfully.")
        else:
            log("⚠️ SteamCMD completed, but success message not found.")
            log_error("[setup] Output:\n" + output)
    except Exception as e:
        log_error(f"[setup] RTM update/install failed: {e}")
        log("❌ RTM server update failed.")
