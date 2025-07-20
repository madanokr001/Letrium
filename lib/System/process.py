import psutil

def process():
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            info = proc.info
            processes.append(f"PID: {info['pid']} - Name: {info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return "\n".join(processes)