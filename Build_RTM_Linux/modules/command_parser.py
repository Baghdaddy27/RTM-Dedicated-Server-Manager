from modules import server_control, restart_scheduler

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
    else:
        log(f"❓ Unknown command: {cmd}")