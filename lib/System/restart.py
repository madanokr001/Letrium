import os

def restart():
    try:
        os.system("shutdown /r /t 0")
        return "sucess shutdown."
    except:
        pass
