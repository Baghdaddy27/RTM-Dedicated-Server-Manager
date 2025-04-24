import os
import sys

from modules import server_control, restart_scheduler

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def handle_command(cmd, log):
    cmd = cmd.lower()

    if cmd == "start":
        server_control.start_server(log)
    elif cmd == "stop":
        server_control.stop_server(log)
    elif cmd == "restart":
        log("🔁 Restarting server...")
        server_control.stop_server(log)
        server_control.start_server(log)
    elif cmd == "status":
        running = server_control.is_server_running()
        log("✅ Server is running." if running else "❌ Server is stopped.")
    elif cmd == "watchdog on":
        restart_scheduler.start_watchdog(log)
    elif cmd == "watchdog off":
        restart_scheduler.stop_watchdog()
        log("❌ Restart watchdog stopped.")
    elif cmd == "update":
        from modules.version_checker import check_for_update_gui
        check_for_update_gui(parent=None, log=log)
    elif cmd == "monitor on":
        from modules import performance_monitor
        performance_monitor.start_monitoring(log)
    elif cmd == "monitor off":
        from modules import performance_monitor
        performance_monitor.stop_monitoring()
        log("❌ Performance monitor stopped.")
    elif cmd == "help":
        from modules import welcome
        welcome.print_welcome(log)
    else:
        log(f"❓ Unknown command: {cmd}")
