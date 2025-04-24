import os
import sys
import shutil
import json
import subprocess
import platform
from modules.logger import log_error
from modules.config import SETTINGS_PATH


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
        log_error(f"[server_settings] Failed to read settings.json: {e}")
        log("❌ Failed to read settings.json.")
        return None

def _open_editor(path, log):
    try:
        if not (path.endswith(".ini") or path.endswith(".txt")):
            log("❌ Refused to open file with unsupported extension.")
            return False

        if platform.system() == "Linux":
            subprocess.Popen(["xdg-open", path])
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        elif platform.system() == "Windows":
            os.startfile(path)

        log(f"📝 Opened file: {path}")
        return True
    except Exception as e:
        log_error(f"[server_settings] Failed to open editor for {path}: {e}")
        log("❌ Failed to open file.")
        return False

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
                log_error(f"[server_settings] Failed to copy {file_name}: {e}")
                log(f"❌ Failed to copy {file_name}.")
                return None
        else:
            log(f"❌ Default file not found: {default_path}")
            return None
    return file_path

def open_config_editor(log):
    path = _check_or_copy("MoriaServerConfig.ini", log)
    if path:
        return _open_editor(path, log)
    return False

def open_permissions_editor(log):
    path = _check_or_copy("MoriaServerPermissions.txt", log)
    if path:
        return _open_editor(path, log)
    return False

def open_rules_editor(log):
    path = _check_or_copy("MoriaServerRules.txt", log)
    if path:
        return _open_editor(path, log)
    return False
