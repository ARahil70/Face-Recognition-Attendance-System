import csv
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from keras.models import load_model


# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Model and Haar Cascade paths
CASCADE_PATH = BASE_DIR / "models" / "haarcascade_frontalface_default.xml"
MODEL_PATH = BASE_DIR / "models" / "final_model.h5"

# Attendance file
ATTENDANCE_FILE = BASE_DIR / "attendance.csv"


# Load Haar Cascade and trained model
classifier = cv2.CascadeClassifier(str(CASCADE_PATH))
model = load_model(MODEL_PATH)


# Trained person names
labels = ["MD RAHIL AKHTER"]

# Attendance dictionary
attendance = {}


def get_pred_label(pred):
    return labels[pred]


def preprocess(img):

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (100, 100))
    img = cv2.equalizeHist(img)
    img = img.reshape(1, 100, 100, 1)
    img = img / 255

    return img


def update_attendance(name):

    now = datetime.now()

    if name not in attendance:
        # First appearance → Entry
        attendance[name] = {
            "entry": now,
            "exit": now
        }

    else:
        # Update last seen time → Exit
        attendance[name]["exit"] = now


def save_attendance():

    file_exists = ATTENDANCE_FILE.exists()

    with open(ATTENDANCE_FILE, "a", newline="") as f:

        writer = csv.writer(f)

        # Add header only when the file is created
        if not file_exists:
            writer.writerow([
                "Name",
                "Date",
                "Entry Time",
                "Exit Time",
                "Duration (Hours)"
            ])

        for name, times in attendance.items():

            entry = times["entry"]
            exit_time = times["exit"]

            duration = (
                exit_time - entry
            ).total_seconds() / 3600

            writer.writerow([
                name,
                entry.strftime("%Y-%m-%d"),
                entry.strftime("%H:%M:%S"),
                exit_time.strftime("%H:%M:%S"),
                f"{duration:.2f}"
            ])

    print("Attendance saved to attendance.csv")


# Use USB camera
cap = cv2.VideoCapture(0)


while True:

    ret, frame = cap.read()

    if not ret:
        print("Could not access the camera.")
        break

    faces = classifier.detectMultiScale(
        frame,
        1.5,
        5
    )

    for x, y, w, h in faces:

        face = frame[y:y+h, x:x+w]

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (255, 0, 0),
            5
        )

        prediction = model.predict(
            preprocess(face),
            verbose=0
        )

        pred = np.argmax(prediction)

        name = get_pred_label(pred)

        cv2.putText(
            frame,
            name,
            (x, y-10),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (255, 0, 0),
            2
        )

        update_attendance(name)

    cv2.imshow("Face Recognition Attendance", frame)

    if cv2.waitKey(1) == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()


# Save attendance log
save_attendance()