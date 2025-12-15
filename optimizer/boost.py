import psutil
import time

def get_memory_usage():
    ram = psutil.virtual_memory()
    return {
        "total": round(ram.total / (1024 ** 3), 2),
        "used": round(ram.used / (1024 ** 3), 2),
        "percent": ram.percent
    }

def kill_heavy_processes(threshold=10.0):
    killed = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            cpu = proc.info['cpu_percent']
            if cpu is None:
                continue
            if cpu > threshold and proc.info['name'] not in ['System', 'explorer.exe', 'python.exe']:
                proc.kill()
                killed.append((proc.info['name'], proc.info['pid'], cpu))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return killed

def optimize_system():
    before = get_memory_usage()
    time.sleep(1)  # дати системі оновити RAM
    killed = kill_heavy_processes()
    time.sleep(1)
    after = get_memory_usage()

    freed = round(before['used'] - after['used'], 2)
    return {
        "before": before,
        "after": after,
        "freed_gb": freed,
        "killed_processes": killed
    }