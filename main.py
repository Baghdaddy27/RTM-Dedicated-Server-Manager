import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QLineEdit, QSizePolicy, QFrame,
    QDialog, QFormLayout, QTimeEdit, QCheckBox, QComboBox
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTime

# --- Import your modules here ---
from modules import setup, server_control, server_settings, notifications, restart_scheduler

# --- Constants ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEDICATED_SERVER_DIR = os.path.join(BASE_DIR, "Dedicated Server")
LOGO_PATH = os.path.join(BASE_DIR, "assets", "RTMSM.png")

class MainWindow(QMainWindow): 
    def load_welcome_message(self):
        welcome_file = os.path.join(os.path.dirname(__file__), "modules", "welcomemsg.txt")
        if os.path.exists(welcome_file):
            with open(welcome_file, "r") as f:
                for line in f:
                    self.output_area.append(line.rstrip())
        else:
            self.output_area.append("Welcome message file not found.")

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Return to Moria Server Manager")
        self.setWindowIcon(QIcon("RTMSM.ico"))
        self.setMinimumSize(1000, 600)

        # --- Central Layout ---
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # --- Left Panel (1/3 Width) ---
        left_panel = QVBoxLayout()
        left_panel.setSpacing(20)

        # -- Logo + Title --
        logo_label = QLabel()
        if os.path.exists(LOGO_PATH):
            pixmap = QPixmap(LOGO_PATH).scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        # Removed scaled contents to preserve aspect ratio
        logo_label.setAlignment(Qt.AlignCenter)

        title_label = QLabel("<h2 style='white-space: normal;'>RTM Server Manager</h2>")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)
        author_label = QLabel("<small><i>Made by Baghdaddy27</i></small>")
        author_label.setAlignment(Qt.AlignCenter)

        left_panel.addWidget(logo_label)
        left_panel.addWidget(title_label)
        left_panel.addWidget(author_label)

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

        # --- Settings Section ---
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

        # Spacer
        left_panel.addStretch()

        # --- Terminal Panel (2/3 Width) ---
        self.terminal = TerminalWidget()

        # --- Add to Main Layout ---
        left_frame = QFrame()
        left_frame.setLayout(left_panel)
        # left_frame.setFixedWidth(300)  # Removed fixed width for better responsiveness

        main_layout.addWidget(left_frame, 1)
        main_layout.addWidget(self.terminal, 2)

class TerminalWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Enter command here...")
        self.input_line.returnPressed.connect(self.send_command)

        layout.addWidget(self.output_area)
        layout.addWidget(self.input_line)
        self.setLayout(layout)

        self.load_welcome_message()

    def load_welcome_message(self):
        welcome_file = os.path.join(os.path.dirname(__file__), "modules", "welcomemsg.txt")
        if os.path.exists(welcome_file):
            with open(welcome_file, "r") as f:
                for line in f:
                    self.output_area.append(line.rstrip())
        else:
            self.output_area.append("Welcome message file not found.")

    def log(self, message):
        self.output_area.append(message)

    def send_command(self):
        cmd = self.input_line.text().strip()
        if cmd:
            self.log(f"> {cmd}")
            # TODO: Send command to running server
        self.input_line.clear()

    def start_server(self):
        self.log("[START] Server starting...")
        # TODO: Start server logic

    def stop_server(self):
        self.log("[STOP] Server stopping...")
        # TODO: Stop server logic

    def update_server(self):
        self.log("[UPDATE] Updating server...")
        # TODO: Run update logic

    def restart_server(self):
        self.log("[RESTART] Restarting server...")
        self.stop_server()
        # Add delay here if needed
        self.start_server()

class NotificationSetupDialog(QDialog):
    def __init__(self, log_callback):
        super().__init__()
        self.setWindowTitle("Setup Notifications")
        self.setMinimumWidth(400)
        self.log = log_callback

        layout = QVBoxLayout()

        # --- Desktop Notifications ---
        layout.addWidget(QLabel("<b>Desktop Notifications</b>"))
        btn_toggle_desktop = QPushButton("Enable/Disable Desktop Notifications")
        btn_test_desktop = QPushButton("Test Desktop Notification")
        btn_toggle_desktop.clicked.connect(lambda: self.toggle_desktop())
        btn_test_desktop.clicked.connect(lambda: notifications.test_desktop_notification(self.log))

        layout.addWidget(btn_toggle_desktop)
        layout.addWidget(btn_test_desktop)

        # --- Webhook Notifications ---
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

        self.enable_box = QCheckBox("Enable Automatic Restarts")
        self.warning_box = QCheckBox("Enable Restart Warnings")
        self.freq_dropdown = QComboBox()
        self.freq_dropdown.addItems(["1", "2", "3", "4"])
        self.time_picker = QTimeEdit()
        self.time_picker.setDisplayFormat("HH:mm")

        layout.addWidget(QLabel("Restart Frequency (Hours):"))
        layout.addWidget(self.freq_dropdown)
        layout.addWidget(QLabel("Starting Time (HH:MM):"))
        layout.addWidget(self.time_picker)
        layout.addWidget(self.enable_box)
        layout.addWidget(self.warning_box)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)

        self.setLayout(layout)
        self.load_settings()

    def load_settings(self):
        settings = restart_scheduler.load_restart_settings()
        self.enable_box.setChecked(settings.get("enabled", False))
        self.warning_box.setChecked(settings.get("warnings", False))
        self.freq_dropdown.setCurrentText(str(settings.get("frequency", "1")))
        start_time = settings.get("start_time", "00:00")
        self.time_picker.setTime(QTime.fromString(start_time, "HH:mm"))

    def save_settings(self):
        data = {
            "enabled": self.enable_box.isChecked(),
            "warnings": self.warning_box.isChecked(),
            "frequency": int(self.freq_dropdown.currentText()),
            "start_time": self.time_picker.time().toString("HH:mm")
        }
        restart_scheduler.save_restart_settings(data)
        self.log(f"✅ Restart schedule saved: every {data['frequency']} hrs starting at {data['start_time']}")
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # ✅ Start the restart watchdog AFTER window is created
    restart_scheduler.start_watchdog(window.terminal.log)

    sys.exit(app.exec_())
