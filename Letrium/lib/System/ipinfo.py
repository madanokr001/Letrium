import requests

def getip():
    try:
        res = requests.get("https://ipinfo.io/json")
        data = res.json() if res.status_code == 200 else {}
        return "\n".join(f"{k.capitalize()}: {v}" for k, v in data.items())
    except Exception as e:
        return f"{e}"