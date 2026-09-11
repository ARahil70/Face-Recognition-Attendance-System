import cv2
import urllib.request
import numpy as np
from pathlib import Path


# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# File and folder paths
CASCADE_PATH = BASE_DIR / "models" / "haarcascade_frontalface_default.xml"
IMAGE_DIR = BASE_DIR / "images"

# Create images folder if it does not exist
IMAGE_DIR.mkdir(exist_ok=True)

# Load Haar Cascade
classifier = cv2.CascadeClassifier(str(CASCADE_PATH))

# IP camera URL
url = "http://192.168.137.110:8080/shot.jpg"

data = []

while len(data) < 100:

    image_from_url = urllib.request.urlopen(url)

    frame = np.array(
        bytearray(image_from_url.read()),
        np.uint8
    )

    frame = cv2.imdecode(frame, -1)

    face_points = classifier.detectMultiScale(frame, 1.3, 5)

    if len(face_points) > 0:

        for x, y, w, h in face_points:

            face_frame = frame[y:y+h+1, x:x+w+1]

            cv2.imshow("Only face", face_frame)

            if len(data) <= 100:
                print(len(data) + 1, "/100")
                data.append(face_frame)
                break

    cv2.putText(
        frame,
        str(len(data)),
        (100, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        5,
        (0, 0, 255)
    )

    cv2.imshow("frame", frame)

    if cv2.waitKey(30) == ord("q"):
        break


cv2.destroyAllWindows()


if len(data) == 100:

    name = input("Enter Face holder name: ")

    for i in range(100):

        image_path = IMAGE_DIR / f"{name}_{i}.jpg"
        cv2.imwrite(str(image_path), data[i])

    print("Done")

else:
    print("Need more data")