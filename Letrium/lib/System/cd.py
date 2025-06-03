import os

def cd(path):
    try:
        if path:
            os.chdir(path)
        return os.getcwd()
    except Exception as e:
        return str(e)
