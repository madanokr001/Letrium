import ctypes
import threading

def msgbox(tittle, text, style=0):
    ctypes.windll.user32.MessageBoxW(0, text, tittle, style)

def close():
    threading.Thread(target=msgbox, args=()).start()
