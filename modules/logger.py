# modules/logger.py
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

def log_to_file(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
    log_path = os.path.join(LOGS_DIR, log_filename)

    full_message = f"[{timestamp}] {message}\n"

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(full_message)
