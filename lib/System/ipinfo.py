import requests
import json

def getip():
    try:
        r = requests.get("https://ipinfo.io/json")
        return json.dumps(r.json(), indent=2)
    except:
        pass