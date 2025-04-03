import json
import os
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")

def load_restart_settings():
    if not os.path.exists(SETTINGS_PATH):
        return {}

    with open(SETTINGS_PATH, "r") as f:
        return json.load(f).get("restart_schedule", {})

def save_restart_settings(data):
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)

    settings["restart_schedule"] = data

    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)

def get_next_restart_time(start_time_str, frequency_hours):
    now = datetime.now()
    start_time = datetime.strptime(start_time_str, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day
    )
    while start_time < now:
        start_time += timedelta(hours=frequency_hours)
    return start_time

import threading
import time
from datetime import datetime, timedelta
from . import notifications, server_control

_restart_thread = None
_stop_flag = False

def start_watchdog(log_func):
    global _restart_thread, _stop_flag
    _stop_flag = False

    if _restart_thread and _restart_thread.is_alive():
        log_func("🔁 Restart watchdog already running.")
        return

    _restart_thread = threading.Thread(target=_watchdog_loop, args=(log_func,), daemon=True)
    _restart_thread.start()
    log_func("🕒 Restart watchdog started.")

def stop_watchdog():
    global _stop_flag
    _stop_flag = True

def _watchdog_loop(log_func):
    last_warning = None

    while not _stop_flag:
        settings = load_restart_settings()
        if not settings.get("enabled", False):
            time.sleep(10)
            continue

        freq = int(settings.get("frequency", 1))
        start_str = settings.get("start_time", "00:00")
        warnings_enabled = settings.get("warnings", False)

        next_restart = get_next_restart_time(start_str, freq)
        now = datetime.now()
        minutes_left = int((next_restart - now).total_seconds() / 60)

        if warnings_enabled and minutes_left in [90, 60, 30, 10, 5] and last_warning != minutes_left:
            msg = f"⏰ Server will restart in {minutes_left} minutes."
            log_func(msg)
            notifications.send_desktop_notification("RTM Server Manager", msg)
            notifications.send_webhook(f"⏰ {msg}")
            last_warning = minutes_left

        if minutes_left <= 0:
            log_func("♻️ Scheduled restart time reached. Restarting server...")
            server_control.stop_server(log_func)
            time.sleep(3)
            server_control.start_server(log_func)
            last_warning = None
            time.sleep(60)

        time.sleep(30)
