# Face Recognition Attendance System

A Python-based Face Recognition Attendance System that uses Computer Vision and Deep Learning to detect and recognize registered faces and automatically record attendance with date and time.

---

## 📌 About the Project

The Face Recognition Attendance System is developed to make the attendance process easier and more automatic.

The system collects face images using a camera, prepares the collected data, trains a deep learning model, and uses a camera for real-time face detection and recognition.

When a registered person is recognized, the system can record their attendance along with the date and time.

---

## ✨ Features

- Face detection using OpenCV Haar Cascade
- Face data collection using a camera
- Image preprocessing
- Dataset preparation
- Deep learning model training
- Real-time face recognition
- Automatic attendance recording
- Date and time tracking
- CSV-based attendance records
- Phone camera support using IP Webcam
- Python virtual environment support

---

## 🛠️ Technologies Used

- Python 3.11
- TensorFlow
- Keras
- OpenCV
- NumPy
- Scikit-learn
- Matplotlib
- Visual Studio Code (VS Code)
- Git
- GitHub

---

## 📂 Project Structure

```text
Face-Recognition-Attendance-System/
│
├── models/
│   ├── final_model.h5
│   └── haarcascade_frontalface_default.xml
│
├── src/
│   ├── collect_data.py
│   ├── consolidate_data.py
│   ├── train_model.py
│   ├── recognize.py
│   └── attendance_system.py
│
├── .gitignore
├── README.md
└── requirements.txt