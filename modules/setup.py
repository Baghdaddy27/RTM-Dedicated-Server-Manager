import os
import zipfile
import subprocess
import json
import platform
import time
from PyQt5.QtWidgets import QFileDialog, QApplication
from urllib.request import urlretrieve

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEAMCMD_ZIP = os.path.join(BASE_DIR, "steamcmd.zip")
STEAMCMD_DIR = os.path.join(BASE_DIR, "steamcmd")
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")
IS_WINDOWS = platform.system() == "Windows"

steamcmd_exe = os.path.join(
    STEAMCMD_DIR, "steamcmd.exe" if IS_WINDOWS else "steamcmd.sh"
)

def verify_steamcmd(log):
    if not os.path.exists(steamcmd_exe):
        log("📦 SteamCMD not found. Installing...")
        QApplication.processEvents()
        time.sleep(0.5)

        os.makedirs(STEAMCMD_DIR, exist_ok=True)

        if IS_WINDOWS:
            try:
                with zipfile.ZipFile(STEAMCMD_ZIP, 'r') as zip_ref:
                    zip_ref.extractall(STEAMCMD_DIR)
                log("✅ SteamCMD extracted.")
            except Exception as e:
                log(f"❌ Error extracting SteamCMD: {e}")
                return
        else:
            try:
                linux_url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
                tar_path = os.path.join(STEAMCMD_DIR, "steamcmd_linux.tar.gz")
                log("🌐 Downloading SteamCMD for Linux...")
                QApplication.processEvents()
                time.sleep(0.5)

                urlretrieve(linux_url, tar_path)
                subprocess.run(["tar", "-xvzf", tar_path, "-C", STEAMCMD_DIR], check=True)
                log("✅ SteamCMD downloaded and extracted for Linux.")
            except Exception as e:
                log(f"❌ Error downloading SteamCMD: {e}")
                return

    log("🔄 Running SteamCMD to check for updates...")
    QApplication.processEvents()
    time.sleep(0.5)

    try:
        if not IS_WINDOWS:
            subprocess.run(["chmod", "+x", steamcmd_exe])
        subprocess.run([steamcmd_exe, "+quit"], check=True)
        log("✅ SteamCMD updated successfully.")
    except Exception as e:
        log(f"❌ SteamCMD run failed: {e}")

def verify_rtm_files(log):
    log("🔄 Installing / Updating Return to Moria Dedicated Server...")
    QApplication.processEvents()
    time.sleep(0.5)

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
            log(f"⚠️ Failed to read settings.json: {e}")

    if not install_dir or not os.path.isdir(install_dir):
        log("📁 No RTM server directory found. Please select or create one.")
        QApplication.processEvents()
        time.sleep(0.5)

        selected = QFileDialog.getExistingDirectory(None, "Select RTM Server Install Directory")
        if not selected:
            log("❌ Operation cancelled by user.")
            return
        install_dir = selected
        try:
            with open(SETTINGS_PATH, "w") as f:
                json.dump({"rtm_server_path": install_dir}, f, indent=4)
            log(f"✅ Saved RTM install location to settings.json: {install_dir}")
        except Exception as e:
            log(f"❌ Failed to save settings.json: {e}")
            return

    log(f"📦 Starting install/update at: {install_dir}")
    QApplication.processEvents()
    time.sleep(0.5)

    try:
        subprocess.run([
            steamcmd_exe,
            "+force_install_dir", install_dir,
            "+login", "anonymous",
            "+app_update", "3349480", "validate",
            "+quit"
        ], check=True)
        log("✅ RTM server installed/updated successfully.")
    except Exception as e:
        log(f"❌ RTM server update failed: {e}")
