import psutil

def processkill(pid: int) -> str:
    try:
        proc = psutil.Process(pid)
        proc.kill()
        return f"sucess {pid}."
    except psutil.NoSuchProcess:
        return f"sucess {pid}."
    except psutil.AccessDenied:
        return f"Access denied {pid}."
    except:
        pass