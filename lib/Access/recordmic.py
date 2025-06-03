import pyaudio
import wave
import os
import tempfile

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

def records(duration_sec):
    try:
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        frames = [stream.read(CHUNK) for _ in range(int(RATE / CHUNK * duration_sec))]

        stream.stop_stream()
        stream.close()
        audio.terminate()

        path = os.path.join(tempfile.gettempdir(), "TheMasterMind.wav")
        with wave.open(path, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        return path
    except Exception as e:
        print(f"{e}")
        return None

