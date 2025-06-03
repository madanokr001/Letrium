import cv2
from io import BytesIO
from PIL import Image

def webcam():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    webcam = Image.fromarray(frame)

    Bytes = BytesIO()
    webcam.save(Bytes, format="JPEG")
    Bytes.seek(0)

    return Bytes