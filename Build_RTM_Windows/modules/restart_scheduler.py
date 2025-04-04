import json
import os
import sys
import threading
import time
from datetime import datetime, timedelta
from modules import notifications, server_control
from modules.logger import log_error

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SETTINGS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "settings.json"))

_restart_thread = None
_stop_flag = False

def load_restart_settings():
    if not os.path.exists(SETTINGS_PATH):
        return {}

    try:
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f).get("restart_schedule", {})
    except Exception as e:
        log_error(f"[RestartScheduler] Failed to load restart settings: {e}")
        return {}

def save_restart_settings(data):
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                settings = json.load(f)
        except Exception as e:
            log_error(f"[RestartScheduler] Failed to read settings.json: {e}")

    settings["restart_schedule"] = data

    try:
        with open(SETTINGS_PATH, "w") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        log_error(f"[RestartScheduler] Failed to save restart schedule: {e}")

def get_next_restart_time(settings):
    now = datetime.now()
    mode = settings.get("mode", "hourly")

    if mode == "hourly":
        last_start_str = settings.get("last_start")
        freq_hours = int(settings.get("frequency", 1))
        if not last_start_str:
            return now + timedelta(hours=freq_hours)
        last_start = datetime.strptime(last_start_str, "%Y-%m-%d %H:%M:%S")
        while last_start <= now:
            last_start += timedelta(hours=freq_hours)
        return last_start

    elif mode == "designated":
        start_time_str = settings.get("start_time", "00:00")
        try:
            scheduled = datetime.strptime(start_time_str, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day
            )
            if scheduled <= now:
                scheduled += timedelta(days=1)
            return scheduled
        except ValueError:
            log_error(f"[RestartScheduler] Invalid designated time format: {start_time_str}")
            return now + timedelta(days=1)

    return now + timedelta(hours=1)  # fallback

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

        next_restart = get_next_restart_time(settings)
        now = datetime.now()
        minutes_left = int((next_restart - now).total_seconds() / 60)

        if settings.get("warnings", False) and minutes_left in [90, 60, 30, 10, 5] and last_warning != minutes_left:
            msg = f"⏰ RTM Server will restart in {minutes_left} minutes."
            notifications.send_terminal_webhook_desktop(log_func, msg, "RTM Server Manager", msg)
            last_warning = minutes_left

        if minutes_left <= 0:
            log_func("♻️ Scheduled restart time reached. Restarting server...")
            notifications.send_terminal_webhook_desktop(log_func, "♻️ Scheduled Restart Executing", "RTM Server Manager", "RTM Restarting now.")
            server_control.stop_server(log_func)
            time.sleep(3)
            server_control.start_server(log_func)

            # update last_start if hourly
            if settings.get("mode") == "hourly":
                settings["last_start"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_restart_settings(settings)

            last_warning = None
            time.sleep(60)

        time.sleep(30)
