import psutil
import GPUtil
import platform

def get_cpu_info():
    return {
        "usage_percent": psutil.cpu_percent(interval=1),
        "cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True),
        "frequency": psutil.cpu_freq().current
    }

def get_ram_info():
    ram = psutil.virtual_memory()
    return {
        "total": round(ram.total / (1024 ** 3), 2),
        "used": round(ram.used / (1024 ** 3), 2),
        "percent": ram.percent
    }

def get_gpu_info():
    gpus = GPUtil.getGPUs()
    if not gpus:
        return {"available": False}
    gpu = gpus[0]
    return {
        "available": True,
        "name": gpu.name,
        "load": round(gpu.load * 100, 1),
        "temperature": gpu.temperature
    }

def get_disk_info():
    disk = psutil.disk_usage('/')
    return {
        "total": round(disk.total / (1024 ** 3), 2),
        "used": round(disk.used / (1024 ** 3), 2),
        "percent": disk.percent
    }

def get_system_summary():
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "cpu": get_cpu_info(),
        "ram": get_ram_info(),
        "gpu": get_gpu_info(),
        "disk": get_disk_info()
    }