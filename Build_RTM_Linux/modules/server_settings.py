import os
import shutil
import json
import subprocess
import platform

from . import notifications
from modules.logger import log_error


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")
DEFAULT_FILES_DIR = os.path.join(BASE_DIR, "Default Files")

def _get_rtm_path(log):
    if not os.path.exists(SETTINGS_PATH):
        log("❌ settings.json not found. Please verify RTM files first.")
        return None
    try:
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
            return settings.get("rtm_server_path")
    except Exception as e:
        log_error(f"Failed to read settings.json: {e}")
        log(f"❌ Failed to read settings.json: {e}")
        return None

def _open_editor(path, log):
    try:
        if platform.system() == "Linux":
            subprocess.Popen(["xdg-open", path])
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        elif platform.system() == "Windows":
            os.startfile(path)
        
        log(f"📝 Opened file: {path}")
        notifications.send_desktop_notification("RTM Server Manager", f"Opened file: {os.path.basename(path)}")
        notifications.send_webhook(f"📂 Opened file: `{os.path.basename(path)}`")
    except Exception as e:
        error_msg = f"❌ Failed to open editor: {e}"
        log(error_msg)
        notifications.send_webhook(error_msg)

def _check_or_copy(file_name, log):
    rtm_dir = _get_rtm_path(log)
    if not rtm_dir:
        return None

    file_path = os.path.join(rtm_dir, file_name)
    if not os.path.exists(file_path):
        default_path = os.path.join(DEFAULT_FILES_DIR, file_name)
        if os.path.exists(default_path):
            try:
                shutil.copy(default_path, file_path)
                log(f"📄 Copied default {file_name} to server directory.")
            except Exception as e:
                log(f"❌ Failed to copy {file_name}: {e}")
                return None
        else:
            log(f"❌ Default file not found: {default_path}")
            return None
    return file_path

def open_config_editor(log):
    path = _check_or_copy("MoriaServerConfig.ini", log)
    if path:
        _open_editor(path, log)

def open_permissions_editor(log):
    path = _check_or_copy("MoriaServerPermissions.txt", log)
    if path:
        _open_editor(path, log)

def open_rules_editor(log):
    path = _check_or_copy("MoriaServerRules.txt", log)
    if path:
        _open_editor(path, log)
