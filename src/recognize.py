from pathlib import Path

import cv2
import numpy as np
from keras.models import load_model


# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Model and Haar Cascade paths
CASCADE_PATH = BASE_DIR / "models" / "haarcascade_frontalface_default.xml"
MODEL_PATH = BASE_DIR / "models" / "final_model.h5"


# Load Haar Cascade and trained model
classifier = cv2.CascadeClassifier(str(CASCADE_PATH))
model = load_model(MODEL_PATH)


# Trained person labels
labels = ["MD RAHIL AKHTER"]


def get_pred_label(pred):
    return labels[pred]


def preprocess(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (100, 100))
    img = cv2.equalizeHist(img)
    img = img.reshape(1, 100, 100, 1)
    img = img / 255
    return img


# Start laptop/USB camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()


while True:

    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read camera frame.")
        break

    faces = classifier.detectMultiScale(frame, 1.5, 5)

    for x, y, w, h in faces:

        face = frame[y:y+h, x:x+w]

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (255, 0, 0),
            3
        )

        prediction = model.predict(
            preprocess(face),
            verbose=0
        )

        predicted_label = get_pred_label(
            np.argmax(prediction)
        )

        cv2.putText(
            frame,
            predicted_label,
            (x, y - 10),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (255, 0, 0),
            2
        )

    cv2.imshow("Face Recognition", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()