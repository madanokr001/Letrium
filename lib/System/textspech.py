import pyttsx3

def audio(text: str) -> str:
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        return f"{e}"