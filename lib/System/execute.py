import os
import subprocess

def shell(command):
    try:
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd())
        out, err = proc.communicate()
        return (out + err).decode(errors='ignore')
    except Exception as e:
        return str(e)
