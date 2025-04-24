import threading
import time
import psutil

_pid_check_interval = 30
_perf_thread = None
_stop_flag = False

def start_monitoring(log):
    global _perf_thread, _stop_flag
    _stop_flag = False

    if _perf_thread and _perf_thread.is_alive():
        log("📊 Performance monitor already running.")
        return

    _perf_thread = threading.Thread(target=_monitor_loop, args=(log,), daemon=True)
    _perf_thread.start()
    log("📊 Performance monitor started.")

def stop_monitoring():
    global _stop_flag
    _stop_flag = True

def _monitor_loop(log):
    while not _stop_flag:
        server_proc = _find_server_process()
        if not server_proc:
            time.sleep(_pid_check_interval)
            continue

        try:
            cpu = server_proc.cpu_percent(interval=None)
            mem = server_proc.memory_info().rss / (1024 ** 2)  # in MB
            log(f"📊 RTM Server | PID: {server_proc.pid} | CPU: {cpu:.1f}% | MEM: {mem:.1f} MB")
        except Exception as e:
            log(f"⚠️ Failed to read server stats: {e}")

        # ✅ Always sleep here, regardless of success or error
        time.sleep(_pid_check_interval)

def _find_server_process():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'MoriaServer' in proc.info['name']:
            return psutil.Process(proc.info['pid'])
    return None