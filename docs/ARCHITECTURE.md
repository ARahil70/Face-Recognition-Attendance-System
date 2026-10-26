# Architecture

CampusFlow is a local Windows application with a browser dashboard. The Python process serves the front end and handles camera and storage actions.

~~~mermaid
flowchart LR
    UI["HTML / CSS / JavaScript dashboard"] --> Server["Python server on 127.0.0.1"]
    Server --> Camera["OpenCV camera input"]
    Camera --> Detect["Face detection and quality checks"]
    Detect --> Model["Local recognition model"]
    Model --> Store["SQLite profiles and daily records"]
    Store --> Reports["Role-specific CSV exports"]
    Capture["New profile samples"] --> Train["Automatic model training"]
    Train --> Model
~~~

## Main files

- **src/attendance_app.py** starts the browser dashboard.
- **src/campusflow/webapp.py** serves the dashboard, handles local API requests and coordinates registration, training, attendance and exit scans.
- **src/campusflow/camera.py** reads from a system camera or IP Webcam and saves clear face crops during registration.
- **src/campusflow/recognition.py** trains the model, checks strong duplicate matches and recognizes faces during scans.
- **src/campusflow/storage.py** maintains the SQLite database and writes CSV reports.
- **src/campusflow/config.py** defines local paths and recognition settings.
- **src/campusflow/web/** contains the dashboard HTML, CSS and JavaScript.
- **models/haarcascade_frontalface_default.xml** is the face detector shipped with the project. The trained model and its label file are generated on the local computer.

**src/campusflow/app.py** contains an older Tkinter interface. It is not used by the supported launcher.

## Record flow

Registration collects face samples and profile details. Once there are at least two active profiles, the app trains a model in the background. An attendance or exit scan uses that model to identify a profile. SQLite stores the daily attendance row and exit time; CSV files are refreshed for reporting.

The web server binds to 127.0.0.1, so the dashboard is intended for one computer. This is not a central server or a multi-user deployment.
