import ctypes
import threading

def msgbox(title, message):
    def show():
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)
    threading.Thread(target=show, daemon=True).start()
