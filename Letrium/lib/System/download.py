from telebot.types import InputFile
import os

def download(path):
    if not os.path.exists(path):
        return None, f"{path}"
    try:
        return InputFile(path), None
    except Exception as e:
        return None, f"{e}"
