import os
import json
import requests
from plyer import notification

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")

def _load_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    return {}

def _save_settings(data):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(data, f, indent=4)

def set_webhook_url(url, log):
    settings = _load_settings()
    settings["webhook_url"] = url
    _save_settings(settings)
    log("✅ Webhook URL saved.")

def get_webhook_url():
    return _load_settings().get("webhook_url", "")

def enable_desktop_notifications(log):
    log("✅ Desktop Notifications Enabled.")

def disable_desktop_notifications(log):
    log("❌ Desktop Notifications Disabled.")

def test_desktop_notification(log):
    try:
        notification.notify(title="RTM Server Manager", message="This is a desktop test notification.")
        log("✅ Desktop Notification Test Passed.")
    except Exception as e:
        log(f"❌ Desktop Notification Test Failed: {e}")

def enable_webhook_notifications(log):
    log("✅ Webhook Notifications Enabled.")

def disable_webhook_notifications(log):
    log("❌ Webhook Notifications Disabled.")

def test_webhook(log):
    url = get_webhook_url()
    if not url:
        log("❌ Webhook URL not set.")
        return
    try:
        data = {"content": "🔔 This is a test notification from RTM Server Manager."}
        response = requests.post(url, json=data)
        if response.status_code == 204:
            log("✅ Webhook Notification Test Passed.")
        else:
            log(f"❌ Webhook Test Failed: {response.status_code} - {response.text}")
    except Exception as e:
        log(f"❌ Webhook Test Error: {e}")

def send_desktop_notification(title, message):
    try:
        notification.notify(title=title, message=message, app_name="RTM Server Manager")
    except Exception:
        pass

def send_webhook(message):
    settings = _load_settings()
    if settings.get("enable_webhook") and settings.get("webhook_url"):
        try:
            requests.post(settings["webhook_url"], json={"content": message})
        except Exception:
            pass

def send_terminal_webhook_desktop(log, terminal_msg, title, message):
    log(terminal_msg)
    send_desktop_notification(title, message)
    send_webhook(f"🔔 {message}")
