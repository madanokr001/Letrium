import os

def restart():
    try:
        os.system("shutdown /r /t 0")
        return "sucess"
    except Exception as e:
        return f"{str(e)}"
