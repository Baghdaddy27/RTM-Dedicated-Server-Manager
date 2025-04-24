import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QLineEdit, QSizePolicy, QFrame,
    QDialog, QFormLayout, QTimeEdit, QCheckBox, QComboBox, QButtonGroup
)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QTime, pyqtSignal
from datetime import datetime
from modules import setup, server_control, server_settings, notifications, restart_scheduler, command_parser, welcome, performance_monitor
from modules.config import SETTINGS_PATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# --- Path Handling for Windows Executable ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VERSION_FILE = os.path.join(BASE_DIR, "modules", "version.txt")
if os.path.exists(VERSION_FILE):
    with open(VERSION_FILE, "r") as f:
        APP_VERSION = f.read().strip()
else:
    APP_VERSION = "0.0.0"

WELCOME_PATH = os.path.join(BASE_DIR, ".wm")

SETTINGS_PATH = os.path.join(BASE_DIR, "modules", "settings.json")

# Ensure directory exists
os.makedirs(BASE_DIR, exist_ok=True)

# Default settings
default_settings = {
    "rtm_server_path": "",
    "webhook_url": "",
    "enable_webhook": False,
    "enable_desktop_notifications": False,
    "notify_server_start": True,
    "notify_server_stop": True,
    "notify_crash_detect": True,
    "restart_schedule": {
        "enabled": False,
        "warnings": False,
        "frequency": 4,
        "start_time": "00:00"
    }
}

# Create settings.json if it doesn't exist
if not os.path.exists(SETTINGS_PATH):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(default_settings, f, indent=4)

DEDICATED_SERVER_DIR = os.path.join(BASE_DIR, "Dedicated Server")
LOGO_PATH = os.path.join(BASE_DIR, "assets", "RTMSM.png")

class MainWindow(QMainWindow):
    def load_welcome_message(self):
        try:
            from modules import welcome
            welcome.print_welcome(self.log)
        except Exception as e:
            self.log(f"❌ Failed to load welcome message: {e}")

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Return to Moria Server Manager")
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR, "RTMSM.ico")))
        self.setMinimumSize(1000, 600)

        central_widget = QWidget()
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # --- Left Panel (1/3 Width) ---
        left_panel = QVBoxLayout()
        left_panel.setSpacing(20)

        logo_container = QVBoxLayout()
        logo_container.setSpacing(5)  # Small spacing between logo and text
        logo_container.setContentsMargins(0, 10, 0, 10)  # Add padding above/below

        logo_label = QLabel()
        if os.path.exists(LOGO_PATH):
            pixmap = QPixmap(LOGO_PATH).scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        title_label = QLabel("<h2 style='white-space: normal;'>RTM Server Manager</h2>")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)

        author_label = QLabel(f"<small><i>Version {APP_VERSION}</i></small>")
        author_label.setAlignment(Qt.AlignCenter)

        logo_container.addWidget(logo_label)
        logo_container.addWidget(title_label)
        logo_container.addWidget(author_label)

        logo_widget = QWidget()
        logo_widget.setLayout(logo_container)

        left_panel.addWidget(logo_widget, alignment=Qt.AlignTop)

        # --- Setup Section ---
        setup_label = QLabel("<b>Setup</b>")
        verify_steamcmd_btn = QPushButton("Verify SteamCMD")
        verify_rtm_btn = QPushButton("Verify RTM Files")
        setup_notifications_btn = QPushButton("Setup Notifications")

        verify_steamcmd_btn.clicked.connect(lambda: setup.verify_steamcmd(self.terminal.log))
        verify_rtm_btn.clicked.connect(lambda: setup.verify_rtm_files(self.terminal.log))
        setup_notifications_btn.clicked.connect(lambda: NotificationSetupDialog(self.terminal.log).exec_())

        left_panel.addWidget(setup_label)
        left_panel.addWidget(verify_steamcmd_btn)
        left_panel.addWidget(verify_rtm_btn)
        left_panel.addWidget(setup_notifications_btn)

        # --- Server Control Section ---
        control_label = QLabel("<b>Server Control</b>")
        start_btn = QPushButton("Start Server")
        stop_btn = QPushButton("Stop Server")
        restart_btn = QPushButton("Auto Restart")

        start_btn.clicked.connect(lambda: server_control.start_server(self.terminal.log))
        stop_btn.clicked.connect(lambda: server_control.stop_server(self.terminal.log))
        restart_btn.clicked.connect(lambda: RestartSchedulerDialog(self.terminal.log).exec_())

        left_panel.addWidget(control_label)
        left_panel.addWidget(start_btn)
        left_panel.addWidget(stop_btn)
        left_panel.addWidget(restart_btn)

        # --- Server Settings Section ---
        settings_label = QLabel("<b>Server Settings</b>")
        config_btn = QPushButton("Edit Config")
        permissions_btn = QPushButton("Edit Permissions")
        rules_btn = QPushButton("Edit Rules")

        config_btn.clicked.connect(lambda: server_settings.open_config_editor(self.terminal.log))
        permissions_btn.clicked.connect(lambda: server_settings.open_permissions_editor(self.terminal.log))
        rules_btn.clicked.connect(lambda: server_settings.open_rules_editor(self.terminal.log))

        left_panel.addWidget(settings_label)
        left_panel.addWidget(config_btn)
        left_panel.addWidget(permissions_btn)
        left_panel.addWidget(rules_btn)

        left_panel.addStretch()

        self.terminal = TerminalWidget()
        left_frame = QFrame()
        left_frame.setLayout(left_panel)

        main_layout.addWidget(left_frame, 1)
        main_layout.addWidget(self.terminal, 2)

class TerminalWidget(QWidget):
    append_text_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.append_text_signal.connect(self._append_text)
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setFont(QFont("Courier New", 10))


        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Enter command here...")
        self.input_line.returnPressed.connect(self.send_command)

        layout.addWidget(self.output_area)
        layout.addWidget(self.input_line)
        self.setLayout(layout)

        self.load_welcome_message()

    def load_welcome_message(self):
        try:
            welcome.print_welcome(self.log)
        except Exception as e:
            self.log(f"❌ Failed to load welcome message: {e}")

    def log(self, message):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        self.append_text_signal.emit(f"{timestamp} {message}")

    def send_command(self):
        cmd = self.input_line.text().strip()
        if cmd:
            self.log(f"> {cmd}")
            command_parser.handle_command(cmd, self.log)
        self.input_line.clear()

    def _append_text(self, message):
        self.output_area.append(message)
        self.output_area.moveCursor(self.output_area.textCursor().End)
        self.output_area.ensureCursorVisible()

class NotificationSetupDialog(QDialog):
    def __init__(self, log_callback):
        super().__init__()
        self.setWindowTitle("Setup Notifications")
        self.setMinimumWidth(400)
        self.log = log_callback

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<b>Desktop Notifications</b>"))
        btn_toggle_desktop = QPushButton("Enable/Disable Desktop Notifications")
        btn_test_desktop = QPushButton("Test Desktop Notification")
        btn_toggle_desktop.clicked.connect(lambda: self.toggle_desktop())
        btn_test_desktop.clicked.connect(lambda: notifications.test_desktop_notification(self.log))
        layout.addWidget(btn_toggle_desktop)
        layout.addWidget(btn_test_desktop)

        layout.addSpacing(10)
        layout.addWidget(QLabel("<b>Webhook Notifications</b>"))
        self.webhook_input = QLineEdit()
        self.webhook_input.setPlaceholderText("Enter Webhook URL")
        self.webhook_input.setText(notifications.get_webhook_url())
        btn_save_webhook = QPushButton("Enable/Disable Webhook Notifications")
        btn_test_webhook = QPushButton("Test Webhook Notification")
        btn_save_webhook.clicked.connect(lambda: self.save_webhook())
        btn_test_webhook.clicked.connect(lambda: notifications.test_webhook(self.log))
        layout.addWidget(self.webhook_input)
        layout.addWidget(btn_save_webhook)
        layout.addWidget(btn_test_webhook)

        self.setLayout(layout)

    def toggle_desktop(self):
        if not hasattr(self, 'desktop_enabled'):
            self.desktop_enabled = False
        self.desktop_enabled = not self.desktop_enabled
        if self.desktop_enabled:
            notifications.enable_desktop_notifications(self.log)
        else:
            notifications.disable_desktop_notifications(self.log)

    def save_webhook(self):
        if not hasattr(self, 'webhook_enabled'):
            self.webhook_enabled = False
        url = self.webhook_input.text().strip()
        if url:
            notifications.set_webhook_url(url, self.log)
            self.webhook_enabled = not self.webhook_enabled
            if self.webhook_enabled:
                notifications.enable_webhook_notifications(self.log)
            else:
                notifications.disable_webhook_notifications(self.log)
        else:
            self.log("❌ Webhook URL is empty.")

class RestartSchedulerDialog(QDialog):
    def __init__(self, log_callback):
        super().__init__()
        self.setWindowTitle("Schedule Auto Restart")
        self.setMinimumWidth(400)
        self.log = log_callback

        layout = QVBoxLayout()

        # Mode selection
        self.hourly_check = QCheckBox("Hourly Restart")
        self.designated_check = QCheckBox("Designated Time Restart")

        self.mode_group = QButtonGroup(self)
        self.mode_group.setExclusive(True)
        self.mode_group.addButton(self.hourly_check)
        self.mode_group.addButton(self.designated_check)

        self.hourly_check.clicked.connect(self.toggle_mode)
        self.designated_check.clicked.connect(self.toggle_mode)

        layout.addWidget(self.hourly_check)
        layout.addWidget(self.designated_check)

        # Hourly config
        self.freq_dropdown = QComboBox()
        self.freq_dropdown.addItems([str(i) for i in range(1, 25)])
        self.freq_dropdown.setEnabled(False)

        # Designated time config
        self.time_picker = QTimeEdit()
        self.time_picker.setDisplayFormat("HH:mm")
        self.time_picker.setEnabled(False)

        layout.addWidget(QLabel("Restart Frequency (1–24 hrs):"))
        layout.addWidget(self.freq_dropdown)
        layout.addWidget(QLabel("Restart at specific 24H time (HH:MM):"))
        layout.addWidget(self.time_picker)

        # Common options
        self.enable_box = QCheckBox("Enable Automatic Restarts")
        self.warning_box = QCheckBox("Enable Restart Warnings")
        layout.addWidget(self.enable_box)
        layout.addWidget(self.warning_box)

        # Save
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)

        self.setLayout(layout)
        self.load_settings()

    def toggle_mode(self):
        if self.hourly_check.isChecked():
            self.freq_dropdown.setEnabled(True)
            self.time_picker.setEnabled(False)
        elif self.designated_check.isChecked():
            self.freq_dropdown.setEnabled(False)
            self.time_picker.setEnabled(True)

    def load_settings(self):
        settings = restart_scheduler.load_restart_settings()
        mode = settings.get("mode", "hourly")

        self.enable_box.setChecked(settings.get("enabled", False))
        self.warning_box.setChecked(settings.get("warnings", False))

        self.freq_dropdown.setCurrentText(str(settings.get("frequency", 1)))
        self.time_picker.setTime(QTime.fromString(settings.get("start_time", "00:00"), "HH:mm"))

        if mode == "hourly":
            self.hourly_check.setChecked(True)
        elif mode == "designated":
            self.designated_check.setChecked(True)
        self.toggle_mode()

    def save_settings(self):
        mode = "hourly" if self.hourly_check.isChecked() else "designated"
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "enabled": self.enable_box.isChecked(),
            "warnings": self.warning_box.isChecked(),
            "mode": mode,
            "frequency": int(self.freq_dropdown.currentText()) if mode == "hourly" else 1,
            "start_time": self.time_picker.time().toString("HH:mm"),
            "last_start": now_str if mode == "hourly" else None
        }

        restart_scheduler.save_restart_settings(data)
        self.log(f"✅ Restart schedule saved in {mode} mode.")
        self.accept()

if __name__ == "__main__":
            
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    performance_monitor.start_monitoring(window.terminal.log)
    restart_scheduler.start_watchdog(window.terminal.log)
    from modules.version_checker import check_for_update_gui
    check_for_update_gui(window)
    sys.exit(app.exec_())
