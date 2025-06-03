import os
import socket
import platform
import psutil

def sysinfo():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        uname = platform.uname()
        ram = round(psutil.virtual_memory().total / (1024**3))
        return (
            f"OS : {uname.system}\n"
            f"Version : {uname.version}\n"
            f"Arch : {platform.architecture()[0]}\n"
            f"CPU : {uname.processor}\n"
            f"Hostname : {uname.node}\n"
            f"IP : {ip}\n"
            f"Cores : {os.cpu_count()}\n"
            f"RAM : {ram} GB\n"
            f"User : {os.getlogin()}"
        )
    except Exception as e:
        return str(e)