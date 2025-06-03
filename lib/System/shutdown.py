import os

def shutdown():
    try:
        os.system("shutdown /s /t 0")
        return "sucess"
    except Exception as e:
        return f"{str(e)}"
