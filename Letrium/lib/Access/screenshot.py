import pyautogui
from io import BytesIO

def screenshot():
    screenshots = pyautogui.screenshot()
    Bytes = BytesIO()
    screenshots.save(Bytes, format='PNG')
    Bytes.seek(0)
    return Bytes 
